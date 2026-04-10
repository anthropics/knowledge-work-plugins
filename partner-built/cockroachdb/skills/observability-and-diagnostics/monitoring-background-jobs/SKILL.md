---
name: monitoring-background-jobs
description: Monitors CockroachDB background job health by identifying failed, paused, and long-running jobs using SHOW JOBS and SHOW AUTOMATIC JOBS. Surfaces schema changes, backups/restores, automatic statistics collection, and SQL stats compaction jobs without DB Console access. Use when investigating schema change delays, failed backups, or automatic job issues.
compatibility: Requires SQL access with VIEWJOB privilege or CONTROLJOB role option for cluster-wide visibility. Uses SHOW JOBS and SHOW AUTOMATIC JOBS (production-safe).
metadata:
  author: cockroachdb
  version: "1.0"
---

# Monitoring Background Jobs

Monitors background job health by identifying failed, paused, and long-running jobs that are distinct from user queries. Uses SQL-only interfaces (SHOW JOBS and SHOW AUTOMATIC JOBS) to surface schema changes, backups/restores, automatic statistics collection, and SQL stats compaction without requiring DB Console access.

## When to Use This Skill

- Schema changes appear stuck or delayed (ALTER TABLE, CREATE INDEX, DROP operations)
- Backups or restores are failing or taking longer than expected
- Need to verify automatic statistics collection is running
- Investigating "waiting for MVCC GC" status in schema change cleanup
- Troubleshooting failed jobs without DB Console access
- Monitoring long-running operations that don't appear in query metrics

**For live query monitoring:** Use [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) to monitor currently executing user queries. Note that background jobs execute statements that may not appear in SHOW CLUSTER STATEMENTS.

**For historical query analysis:** Use [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) for query pattern trends. Note that background jobs are excluded from statement statistics.

## Prerequisites

**Required SQL access:**
- Connection to any CockroachDB node
- For cluster-wide job visibility: `VIEWJOB` system privilege (read-only monitoring)
- For job control operations: `CONTROLJOB` role option (pause/cancel/resume jobs)
- Without these: Limited visibility into jobs you created

**Check your privileges:**
```sql
SHOW GRANTS ON ROLE <username>;
```

Look for:
- `VIEWJOB` in the `privilege_type` column (system privilege)
- `CONTROLJOB` in role options (check with `SHOW USERS`)

See [permissions reference](references/permissions.md) for detailed RBAC setup.

## Core Concepts

### Jobs vs Statements

**Key distinction:**
- **Statements:** User-initiated SQL queries tracked by SHOW CLUSTER STATEMENTS and statement statistics
- **Background jobs:** Long-running operations tracked separately by SHOW JOBS

**Background jobs are excluded from:**
- `SHOW CLUSTER STATEMENTS` (live query monitoring)
- `crdb_internal.statement_statistics` (historical query analysis)
- Statement fingerprint metrics and DB Console Statements page

**Common job types:**

| Category | Job Types | Examples |
|----------|-----------|----------|
| **User-initiated** | SCHEMA CHANGE, BACKUP, RESTORE, IMPORT, CHANGEFEED | ALTER TABLE, CREATE INDEX, BACKUP DATABASE, RESTORE |
| **Automatic** | SCHEMA CHANGE GC, AUTO CREATE STATS, AUTO SQL STATS COMPACTION | Post-DROP cleanup, table statistics refresh, stats table maintenance |

See [job types reference](references/job-types.md) for complete catalog.

### SHOW JOBS vs SHOW AUTOMATIC JOBS

| Interface | Scope | Time Window | Use Case |
|-----------|-------|-------------|----------|
| `SHOW JOBS` | User-initiated + automatic | Last 12 hours (default) | Monitor backups, schema changes, user operations |
| `SHOW AUTOMATIC JOBS` | Automatic only | Configurable (recommend 24h) | Monitor AUTO CREATE STATS, AUTO SQL STATS COMPACTION, SCHEMA CHANGE GC |

**Time retention:**
- Default retention: 14 days in `crdb_internal.jobs` table
- `SHOW JOBS` display window: 12 hours (configurable with `SHOW JOBS SELECT * FROM [SHOW JOBS] WHERE ...`)
- `SHOW AUTOMATIC JOBS` display window: Configurable with `WHERE created > now() - INTERVAL '...'`

### Job Status Values

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| `running` | Job is actively executing | Monitor progress via `fraction_completed` |
| `succeeded` | Job completed successfully | None |
| `failed` | Job encountered an error | Investigate `error` column, may need to retry |
| `paused` | Job manually paused | Resume with `RESUME JOB` if appropriate |
| `canceled` | Job was canceled (terminal state) | Retry operation if needed |
| `pending` | Job queued but not started | Monitor; may indicate resource constraints |
| `reverting` | Job failed and is rolling back changes | Wait for completion; check error after |

**Running status sub-states:**
- `performing backup`: Backup job actively transferring data
- `restoring`: Restore job actively applying data
- `waiting for MVCC GC`: SCHEMA CHANGE GC waiting for garbage collection eligibility

See [job states reference](references/job-states.md) for detailed state transitions and "waiting for MVCC GC" explanation.

## Core Diagnostic Queries

### Query 1: Failed Jobs (Last 12 Hours)

Identify jobs that failed with error messages:

```sql
-- Failed jobs in last 12 hours
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  finished,
  now() - created AS total_duration,
  error
FROM j
WHERE status = 'failed'
  AND created > now() - INTERVAL '12 hours'
ORDER BY created DESC
LIMIT 50;
```

**Key columns:**
- `error`: Failure reason (check for permission errors, disk space, network issues)
- `description`: Human-readable description of what the job was doing
- `total_duration`: How long the job ran before failing

**Common failure patterns:**
- Permission denied: User lacks required privileges
- Disk space: Backup destination full
- Network timeout: External storage unreachable
- Constraint violation: Restore conflicts with existing data

### Query 2: Long-Running Jobs

Find jobs running longer than expected threshold:

```sql
-- Jobs running longer than 1 hour
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  running_status,
  created,
  now() - created AS running_for,
  fraction_completed,
  coordinator_id
FROM j
WHERE status = 'running'
  AND created < now() - INTERVAL '1 hour'
ORDER BY created
LIMIT 50;
```

**Key columns:**
- `running_for`: Total elapsed time since job started
- `fraction_completed`: Progress estimate (0.0 to 1.0, NULL if unavailable)
- `running_status`: Sub-state details (e.g., "waiting for MVCC GC")

**Customizable thresholds:**
- Schema changes: 30 minutes to several hours (depends on table size)
- Backups: 1-6+ hours (depends on data volume)
- Automatic jobs: Usually < 30 minutes

### Query 3: Paused Jobs

Identify jobs that are paused and may need attention:

```sql
-- Paused jobs needing resume
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS paused_for,
  coordinator_id
FROM j
WHERE status = 'paused'
ORDER BY created
LIMIT 50;
```

**Action required:**
Resume with `RESUME JOB <job_id>` after verifying the pause reason.

**Common reasons for paused jobs:**
- Manual user pause for maintenance
- Resource constraints (cluster paused the job)
- Error requiring manual intervention

### Query 4: Schema Changes Waiting for MVCC GC

Find SCHEMA CHANGE GC jobs waiting for garbage collection:

```sql
-- Schema change cleanup jobs waiting for GC
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS waiting_for,
  running_status
FROM j
WHERE status = 'running'
  AND job_type = 'SCHEMA CHANGE GC'
  AND running_status LIKE '%waiting for MVCC GC%'
ORDER BY created
LIMIT 50;
```

**Interpretation:**
- **Normal:** SCHEMA CHANGE GC jobs wait for data to become garbage-collectable based on `gc.ttlseconds` setting (default 25 hours)
- **Expected duration:** Up to `gc.ttlseconds` + some overhead
- **When to worry:** Waiting > 2x `gc.ttlseconds` (check setting with `SHOW CLUSTER SETTING gc.ttlseconds`)

**Why this happens:**
After DROP TABLE/INDEX operations, CockroachDB must wait for all reads at older timestamps to complete before physically removing data. This prevents "time-travel" queries from failing.

See [job states reference](references/job-states.md) for detailed MVCC GC explanation.

### Query 5: Automatic Job Health (24h Window)

Monitor automatic background jobs like statistics collection:

```sql
-- Automatic jobs in last 24 hours
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  finished,
  COALESCE(finished, now()) - created AS duration
FROM [SHOW AUTOMATIC JOBS]
WHERE created > now() - INTERVAL '24 hours'
  AND job_type IN ('AUTO CREATE STATS', 'AUTO SQL STATS COMPACTION')
ORDER BY created DESC
LIMIT 50;
```

**Key job types:**
- `AUTO CREATE STATS`: Automatic table statistics refresh (critical for query optimizer)
- `AUTO SQL STATS COMPACTION`: Periodic cleanup of statement/transaction statistics tables

**Health indicators:**
- **Healthy:** Regular successful executions (every few hours)
- **Unhealthy:** No recent executions, or high failure rate
- **Impact of failure:** Stale statistics lead to poor query plans and slow queries

### Query 6: Jobs by Type and Status

Aggregated view for pattern analysis:

```sql
-- Job distribution by type and status (last 24h)
WITH j AS (SHOW JOBS)
SELECT
  job_type,
  status,
  COUNT(*) AS job_count,
  MIN(created) AS oldest,
  MAX(created) AS newest
FROM j
WHERE created > now() - INTERVAL '24 hours'
GROUP BY job_type, status
ORDER BY job_type, status;
```

**Use case:**
- Identify patterns (e.g., all BACKUP jobs failing, multiple schema changes stuck)
- Spot anomalies (e.g., unusual job type volume)
- Track job success rates by type

### Query 7: Backup and Restore Progress

Track progress of backup/restore jobs:

```sql
-- Active backup/restore jobs with progress
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS running_for,
  ROUND(COALESCE(fraction_completed, 0) * 100, 2) AS percent_complete,
  CASE
    WHEN fraction_completed > 0 AND fraction_completed < 1 THEN
      ((now() - created) / fraction_completed) - (now() - created)
    ELSE NULL
  END AS estimated_time_remaining,
  running_status
FROM j
WHERE status = 'running'
  AND job_type IN ('BACKUP', 'RESTORE')
ORDER BY created
LIMIT 50;
```

**Key columns:**
- `percent_complete`: Progress percentage (0-100)
- `estimated_time_remaining`: Rough estimate based on current progress rate
- `running_status`: Detailed status (e.g., "performing backup to s3://...")

**Note:** `fraction_completed` may be NULL for some job types or early in execution.

## Common Workflows

### Workflow 1: Schema Change Stuck Investigation

**Scenario:** User reports ALTER TABLE or CREATE INDEX appears stuck.

1. **Check for running schema changes:**
   ```sql
   WITH j AS (SHOW JOBS)
   SELECT job_id, description, created, now() - created AS running_for,
          fraction_completed, running_status
   FROM j
   WHERE status = 'running'
     AND job_type IN ('SCHEMA CHANGE', 'NEW SCHEMA CHANGE')
   ORDER BY created;
   ```

2. **Identify MVCC GC waits:**
   ```sql
   -- Use Query 4 to find "waiting for MVCC GC" jobs
   ```

3. **Interpret results:**
   - If `running_status` = "waiting for MVCC GC": Normal for post-DROP cleanup (wait up to `gc.ttlseconds`)
   - If long-running with low `fraction_completed`: Check for contention, large table size, or resource constraints
   - If failed: Check `error` column for specific failure reason

4. **Next steps:**
   - MVCC GC wait: Verify `SHOW CLUSTER SETTING gc.ttlseconds` and wait
   - Resource constraints: Check cluster CPU/memory usage
   - Failed job: Address error (permissions, constraints) and retry operation

### Workflow 2: Failed Backup Triage

**Scenario:** Scheduled backup job failed.

1. **Find recent failed backups:**
   ```sql
   -- Use Query 1 filtered for BACKUP job type
   WITH j AS (SHOW JOBS)
   SELECT job_id, description, created, finished, error
   FROM j
   WHERE status = 'failed'
     AND job_type = 'BACKUP'
     AND created > now() - INTERVAL '24 hours'
   ORDER BY created DESC;
   ```

2. **Analyze error messages:**
   - "permission denied": Check external storage credentials
   - "timeout": Network connectivity to backup destination
   - "no space left": Destination storage full
   - "connection refused": External storage endpoint unreachable

3. **Verify backup destination:**
   ```sql
   -- Check SHOW BACKUP for successful backups to same destination
   SHOW BACKUP 's3://bucket/path';
   ```

4. **Remediate and retry:**
   - Fix underlying issue (credentials, storage, network)
   - Re-run backup command
   - Monitor with Query 7 for progress

### Workflow 3: Automatic Job Health Check

**Scenario:** Proactive monitoring of automatic background jobs.

1. **Check AUTO CREATE STATS frequency:**
   ```sql
   -- Use Query 5 to see recent automatic statistics jobs
   SELECT job_type, status, COUNT(*) AS job_count,
          MAX(created) AS most_recent
   FROM [SHOW AUTOMATIC JOBS]
   WHERE created > now() - INTERVAL '24 hours'
     AND job_type = 'AUTO CREATE STATS'
   GROUP BY job_type, status;
   ```

2. **Expected pattern:**
   - Multiple successful AUTO CREATE STATS jobs per day (depends on table update frequency)
   - Regular AUTO SQL STATS COMPACTION (typically once per hour)

3. **Warning signs:**
   - No AUTO CREATE STATS in last 24h: Statistics collection may be disabled
   - High failure rate: Check cluster resource constraints or permission issues
   - No AUTO SQL STATS COMPACTION: Stats table may grow unbounded

4. **Verify settings:**
   ```sql
   SHOW CLUSTER SETTING sql.stats.automatic_collection.enabled;  -- Should be true
   SHOW CLUSTER SETTING sql.stats.automatic_collection.min_stale_rows;
   ```

### Workflow 4: Long-Running Job Monitoring

**Scenario:** Track progress of expected long-running operations.

1. **Identify long-running jobs:**
   ```sql
   -- Use Query 2 with custom threshold
   WITH j AS (SHOW JOBS)
   SELECT job_id, job_type, description,
          now() - created AS running_for,
          fraction_completed
   FROM j
   WHERE status = 'running'
     AND created < now() - INTERVAL '30 minutes'
   ORDER BY created;
   ```

2. **Monitor progress over time:**
   ```sql
   -- Re-run every 10-15 minutes, track fraction_completed changes
   -- Example: 0.25 → 0.40 → 0.55 indicates steady progress
   ```

3. **Estimate completion:**
   ```sql
   -- Use Query 7 for backup/restore jobs with time estimates
   ```

4. **Decide on action:**
   - Steady progress: Continue monitoring
   - Stalled progress (fraction_completed not increasing): Investigate with [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md)
   - Failed: Use Query 1 to check error

## Safety Considerations

**Read-only operations (all diagnostic queries):**
All `SHOW JOBS` and `SHOW AUTOMATIC JOBS` queries are read-only and safe to run in production. No performance impact on cluster operations.

**Job control operations (opt-in):**

**CAUTION: Pausing or canceling jobs can have data integrity implications**

Only proceed with job control if:
- You have `CONTROLJOB` role option
- You understand the implications (e.g., canceling a schema change mid-execution may require manual cleanup)
- You have authorization to interrupt cluster operations
- You've verified the job is truly problematic (not just slow)

**Job control commands:**
```sql
-- Pause a running job (can be resumed later)
PAUSE JOB <job_id>;

-- Resume a paused job
RESUME JOB <job_id>;

-- Cancel a job (terminal - cannot be resumed)
CANCEL JOB <job_id>;
```

**Risks by job type:**
- **SCHEMA CHANGE:** Canceling may leave schema in inconsistent state; prefer PAUSE and investigation
- **BACKUP:** Canceling is safe (can retry); pausing is better for temporary issues
- **RESTORE:** Canceling may leave database partially restored; requires cleanup
- **AUTO CREATE STATS:** Canceling is safe (will retry later automatically)

**Best practice:** Focus on monitoring and diagnosis; only use control operations when explicitly required and authorized.

See [permissions reference](references/permissions.md) for CONTROLJOB role option setup.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `SHOW JOBS` returns empty | No jobs in last 12h, or insufficient privileges | Grant `VIEWJOB` privilege; verify cluster has recent job activity |
| "waiting for MVCC GC" for many hours | Normal behavior for SCHEMA CHANGE GC after DROP operations | Wait up to `gc.ttlseconds` (default 25h); check `SHOW CLUSTER SETTING gc.ttlseconds` |
| Can't pause/resume job: "permission denied" | Missing `CONTROLJOB` role option | Use `ALTER ROLE <username> WITH CONTROLJOB` (not GRANT SYSTEM) |
| Job stuck at same `fraction_completed` | Job may be processing large batch, or actually stuck | Wait 15-30 min and re-check; if no change, investigate with live query triage |
| No AUTO CREATE STATS jobs | Automatic collection disabled | Check `sql.stats.automatic_collection.enabled = true` |
| `SHOW AUTOMATIC JOBS` shows old jobs only | Need to filter by time window | Add `WHERE created > now() - INTERVAL '24 hours'` |
| Failed job with "schema change GC" error | Expected for post-DROP cleanup failures | Usually safe to ignore; job will retry automatically |
| Job error: "concurrent schema change" | Multiple schema changes on same table | Wait for first schema change to complete, then retry |

## Key Considerations

- **Jobs vs queries:** Background jobs execute statements that don't appear in SHOW STATEMENTS or statement statistics
- **Time windows:** SHOW JOBS default 12h retention; use `crdb_internal.jobs` for up to 14 days
- **MVCC GC waiting:** Normal and expected for post-DROP cleanup; duration tied to `gc.ttlseconds`
- **LIMIT clauses:** Always include for production safety (prevents overwhelming output)
- **Privilege model:** VIEWJOB (system privilege) for read-only; CONTROLJOB (role option) for control
- **Automatic job health:** Regular AUTO CREATE STATS is critical for query optimizer performance
- **Progress estimates:** `fraction_completed` may be NULL or sparse for some job types
- **Job control risks:** PAUSE is safer than CANCEL; some cancellations require manual cleanup

## References

**Skill references:**
- [RBAC and privilege setup](references/permissions.md)
- [Job states and transitions](references/job-states.md)
- [Job types catalog](references/job-types.md)
- [SQL query variations](references/sql-query-variations.md)

**Related skills:**
- [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) - For live query monitoring (job-executed statements may not appear)
- [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) - For historical query analysis (background jobs excluded)

**Official CockroachDB Documentation:**
- [SHOW JOBS](https://www.cockroachlabs.com/docs/stable/show-jobs.html)
- [SHOW AUTOMATIC JOBS](https://www.cockroachlabs.com/docs/stable/show-automatic-jobs.html)
- [PAUSE JOB](https://www.cockroachlabs.com/docs/stable/pause-job.html)
- [RESUME JOB](https://www.cockroachlabs.com/docs/stable/resume-job.html)
- [CANCEL JOB](https://www.cockroachlabs.com/docs/stable/cancel-job.html)
- [crdb_internal](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)
- [Jobs Page (DB Console)](https://www.cockroachlabs.com/docs/stable/ui-jobs-page.html)
- [VIEWJOB privilege](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

# Job States and Transitions

This reference provides detailed information about CockroachDB job status values, state transitions, and troubleshooting guidance for each state.

## Job Status Values

Jobs in CockroachDB progress through a lifecycle of status values that indicate their current state.

### Primary Status Values

| Status | Meaning | Terminal? | User Action Required |
|--------|---------|-----------|---------------------|
| `pending` | Job queued but not yet started | No | Monitor; may indicate resource constraints if prolonged |
| `running` | Job is actively executing | No | Monitor progress via `fraction_completed` and `running_status` |
| `succeeded` | Job completed successfully | Yes | None |
| `failed` | Job encountered an error and stopped | Yes | Investigate `error` column; may need to retry operation |
| `paused` | Job manually or automatically paused | No | Resume with `RESUME JOB` after addressing pause reason |
| `canceled` | Job was canceled by user or system | Yes | Retry operation if needed; cannot resume canceled jobs |
| `reverting` | Job is rolling back changes after failure | No | Wait for revert to complete; check error after |

**Terminal states:** `succeeded`, `failed`, `canceled` - these jobs will not transition to other states.

**Resumable states:** `paused`, `pending` - these jobs can be resumed or will eventually start.

**Transient states:** `running`, `reverting` - these jobs are actively doing work.

## Running Status Sub-States

When a job has `status = 'running'`, the `running_status` column provides additional detail about what the job is currently doing.

### Common Running Status Values

| Running Status | Job Types | Meaning | Expected Duration |
|----------------|-----------|---------|-------------------|
| `performing backup` | BACKUP | Actively transferring data to backup destination | Minutes to hours (depends on data size) |
| `performing backup <progress>` | BACKUP | Backup with progress indicator (e.g., "performing backup 45.2%") | Ongoing |
| `restoring` | RESTORE | Actively applying backup data to cluster | Minutes to hours (depends on data size) |
| `waiting for MVCC GC` | SCHEMA CHANGE GC | Waiting for garbage collection eligibility | Up to `gc.ttlseconds` (default 25 hours) |
| `waiting for GC TTL` | SCHEMA CHANGE GC | Alternate form of "waiting for MVCC GC" | Up to `gc.ttlseconds` |
| `populating schema` | SCHEMA CHANGE, NEW SCHEMA CHANGE | Building new index or adding column with backfill | Minutes to hours (depends on table size) |
| `backfilling` | SCHEMA CHANGE | Writing data to new index or column | Minutes to hours |
| `validating` | SCHEMA CHANGE | Verifying schema change completed correctly | Seconds to minutes |
| `merging` | SCHEMA CHANGE | Finalizing schema change | Seconds |
| (empty/NULL) | Various | Job running without specific sub-state | Variable |

## Job State Transitions

Jobs typically follow this lifecycle:

```
User initiates operation (ALTER TABLE, BACKUP, etc.)
           ↓
       pending ─────────→ (Job waits for resources/scheduling)
           ↓
       running ─────────→ (Job executes; may have running_status details)
           ↓
    ┌──────┴──────┐
    ↓             ↓
succeeded      failed ────→ reverting ────→ failed
                               (rollback)

Manual intervention:
running ───PAUSE JOB───→ paused ───RESUME JOB───→ running
running ───CANCEL JOB──→ canceled (terminal)
paused ────CANCEL JOB──→ canceled (terminal)
```

### State Transition Details

**pending → running:**
- Triggered when job scheduler assigns resources
- May remain pending if cluster is resource-constrained
- Normal pending duration: seconds to a few minutes

**running → succeeded:**
- Natural completion of job work
- Terminal state; job will remain in history

**running → failed:**
- Job encountered unrecoverable error
- Check `error` column for failure reason
- May automatically trigger `reverting` for some job types

**running → reverting:**
- Job failed mid-execution and needs to roll back changes
- Common for schema changes that partially completed
- Will eventually transition to `failed` after rollback

**running → paused:**
- User ran `PAUSE JOB <job_id>`
- Or system automatically paused (rare; usually resource exhaustion)

**paused → running:**
- User ran `RESUME JOB <job_id>`
- Or system automatically resumed when resources available

**Any non-terminal → canceled:**
- User ran `CANCEL JOB <job_id>`
- Terminal state; cannot be resumed or retried

## Deep Dive: "waiting for MVCC GC"

This is one of the most common sources of confusion when monitoring background jobs.

### What Is "waiting for MVCC GC"?

When you drop a table or index (`DROP TABLE`, `DROP INDEX`), CockroachDB doesn't immediately delete the physical data. Instead:

1. The table/index is marked as dropped (logically removed)
2. A SCHEMA CHANGE GC job is created to physically delete the data
3. The job waits for all reads at older timestamps to complete
4. After the GC threshold passes, the data is physically removed

The `running_status = 'waiting for MVCC GC'` indicates step 3: the job is waiting for garbage collection eligibility.

### Why Does This Happen?

**CockroachDB supports time-travel queries:**
- Historical reads (AS OF SYSTEM TIME)
- Follower reads
- CDC changefeeds

**To prevent these from breaking, CockroachDB waits:**
- Until all ongoing reads at old timestamps complete
- Until the GC threshold (`gc.ttlseconds`) has elapsed since the DROP operation
- To ensure no active transactions reference the dropped data

### Expected Duration

**Normal wait time:**
```
wait_duration ≈ gc.ttlseconds + overhead
```

**Default `gc.ttlseconds`:**
```sql
SHOW CLUSTER SETTING gc.ttlseconds;
-- Default: 90000 seconds = 25 hours
```

**When to worry:**
- **Normal:** Job waiting < 2x `gc.ttlseconds` (e.g., < 50 hours with default setting)
- **Investigate:** Job waiting > 2x `gc.ttlseconds`
- **Red flag:** Job waiting > 3x `gc.ttlseconds` or job failed with GC error

### Verifying MVCC GC Wait Duration

```sql
-- 1. Check gc.ttlseconds setting
SHOW CLUSTER SETTING gc.ttlseconds;

-- 2. Find SCHEMA CHANGE GC jobs waiting for MVCC GC
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  description,
  created,
  now() - created AS waiting_for,
  running_status
FROM j
WHERE status = 'running'
  AND job_type = 'SCHEMA CHANGE GC'
  AND running_status LIKE '%waiting for MVCC GC%'
ORDER BY created;

-- 3. Compare waiting_for to gc.ttlseconds
-- If waiting_for < gc.ttlseconds: Normal, keep waiting
-- If waiting_for > 2x gc.ttlseconds: Investigate
```

### Common Scenarios

**Scenario 1: Dropped a large table 10 hours ago, job still waiting**
```
Status: running
Running status: waiting for MVCC GC
Time elapsed: 10 hours
gc.ttlseconds: 25 hours (default)

Verdict: NORMAL. Wait up to ~25 hours total.
```

**Scenario 2: Dropped an index 48 hours ago, job still waiting**
```
Status: running
Running status: waiting for MVCC GC
Time elapsed: 48 hours
gc.ttlseconds: 25 hours (default)

Verdict: INVESTIGATE. Should have completed by now.
```

**Scenario 3: Job failed with "GC threshold" error**
```
Status: failed
Error: "waiting for GC threshold"

Verdict: RETRY. Job likely timed out; rerun DROP or wait for automatic retry.
```

### Troubleshooting MVCC GC Waits

**If job is waiting longer than expected:**

1. **Check for long-running transactions:**
   ```sql
   -- Find transactions older than gc.ttlseconds
   SELECT id, start, now() - start AS age, application_name
   FROM crdb_internal.cluster_transactions
   WHERE start < now() - INTERVAL '25 hours'
   ORDER BY start;
   ```

2. **Check for active changefeeds:**
   ```sql
   -- Changefeeds may hold back GC
   WITH j AS (SHOW JOBS)
   SELECT job_id, description, created
   FROM j
   WHERE status = 'running'
     AND job_type = 'CHANGEFEED';
   ```

3. **Check cluster settings:**
   ```sql
   -- Verify gc.ttlseconds hasn't been customized
   SHOW CLUSTER SETTING gc.ttlseconds;

   -- Check protected timestamp records (advanced)
   SELECT * FROM system.protected_ts_records;
   ```

4. **Verify zone configurations:**
   ```sql
   -- Check if table had custom GC settings
   SHOW ZONE CONFIGURATION FOR TABLE <dropped_table_name>;
   -- (This will fail if table already dropped, which is expected)
   ```

### When to Take Action

| Waiting Duration | Action |
|------------------|--------|
| < gc.ttlseconds | None; this is normal |
| gc.ttlseconds to 2x gc.ttlseconds | Monitor; may indicate active long-running txns |
| > 2x gc.ttlseconds | Investigate: check for stuck transactions, changefeeds, or protected timestamps |
| > 3x gc.ttlseconds | Escalate: potential issue with GC subsystem |

### Can You Speed This Up?

**Short answer: No, not safely.**

**Long answer:**
- You cannot manually force MVCC GC to complete
- Canceling the SCHEMA CHANGE GC job will leave orphaned data (disk space leak)
- Reducing `gc.ttlseconds` cluster-wide affects all tables and can break:
  - Historical reads (AS OF SYSTEM TIME)
  - Follower reads
  - CDC changefeeds
  - Backup/restore operations

**Best practice:** Wait for the job to complete naturally. The wait ensures data consistency.

## Reverting Status

### What Is Reverting?

When a job fails mid-execution, CockroachDB may automatically roll back changes to restore the cluster to its pre-job state.

**Common triggers:**
- Schema change fails during backfill
- Restore fails due to constraint violation
- Job encounters disk space error mid-execution

**Reverting behavior:**
```
running (performing work)
   ↓
error encountered
   ↓
reverting (rolling back changes)
   ↓
failed (revert complete)
```

### What Gets Reverted?

| Job Type | Revert Behavior |
|----------|-----------------|
| SCHEMA CHANGE | Removes partially created indexes, undoes column additions |
| NEW SCHEMA CHANGE | Modern schema changer with automatic rollback |
| RESTORE | Cleans up partially restored data |
| IMPORT | Removes partially imported rows |
| BACKUP | No revert needed (backup destination may have partial file) |

### Monitoring Reverting Jobs

```sql
-- Find jobs currently reverting
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS total_duration,
  running_status
FROM j
WHERE status = 'reverting'
ORDER BY created;
```

**Expected duration:** Similar to the time the job spent in `running` state before failing. Reverting can take minutes to hours for large operations.

**User action:** Wait for revert to complete. Check `error` column after revert finishes to diagnose root cause.

## Paused vs Canceled

### Paused Jobs

**Characteristics:**
- Job execution temporarily stopped
- Can be resumed with `RESUME JOB <job_id>`
- Progress is preserved (won't start from scratch)
- Job remains in `paused` state until resumed

**Common reasons for pausing:**
- Manual pause for maintenance window
- Automatic pause due to resource exhaustion (rare)
- Pause before canceling to verify job ID

**How to resume:**
```sql
RESUME JOB <job_id>;
```

### Canceled Jobs

**Characteristics:**
- Job execution permanently terminated
- **Cannot** be resumed
- Terminal state (like `succeeded` or `failed`)
- Must re-run original operation to retry

**Common reasons for canceling:**
- User error (wrong backup destination, wrong table)
- Job consuming too many resources
- Change in requirements (no longer need the operation)

**Important:** Once canceled, the job cannot be resumed. You must re-run the original command (ALTER TABLE, BACKUP, etc.).

### Comparison Table

| Aspect | Paused | Canceled |
|--------|--------|----------|
| Resumable? | Yes | No |
| Terminal state? | No | Yes |
| Preserves progress? | Yes | N/A (must retry from start) |
| Use case | Temporary stop | Permanent abort |
| Recovery | `RESUME JOB` | Re-run original operation |

## Status-Based Actions

Recommended actions for each job status:

| Status | Recommended Action | Urgency |
|--------|-------------------|---------|
| `pending` | Monitor; if > 10 minutes, check cluster resources | Low |
| `running` | Monitor `fraction_completed` and `running_status` | Low (unless long-running) |
| `succeeded` | None; verify operation completed as expected | None |
| `failed` | Read `error` column, address root cause, retry | High |
| `paused` | Resume with `RESUME JOB` or cancel if no longer needed | Medium |
| `canceled` | Re-run operation if still needed | Medium |
| `reverting` | Wait for revert to complete, then check `error` | Medium |

### Specific Running Status Actions

| Running Status | Recommended Action |
|----------------|-------------------|
| `waiting for MVCC GC` | Verify duration < gc.ttlseconds; otherwise investigate |
| `performing backup` | Monitor progress; verify backup destination is accessible |
| `restoring` | Monitor progress; ensure sufficient disk space |
| `populating schema` | Monitor `fraction_completed`; normal for large tables |
| `backfilling` | Monitor progress; may take hours for large indexes |
| `validating` | Wait; should complete quickly (seconds to minutes) |

## Querying Job State History

CockroachDB retains job state transition history in the `system.jobs` table:

```sql
-- View state transition history for a specific job
SELECT
  job_id,
  status,
  created,
  finished,
  modified,
  fraction_completed,
  error
FROM crdb_internal.jobs
WHERE job_id = <specific_job_id>
ORDER BY modified DESC;
```

**Note:** The `crdb_internal.jobs` table shows current state. For historical state transitions, you may need to correlate with logs or metrics.

## Job Status Filters

Common query patterns for filtering by status:

```sql
-- All active jobs (not terminal)
WITH j AS (SHOW JOBS)
SELECT * FROM j
WHERE status IN ('pending', 'running', 'paused', 'reverting');

-- All problematic jobs
WITH j AS (SHOW JOBS)
SELECT * FROM j
WHERE status IN ('failed', 'paused', 'reverting')
  OR (status = 'running' AND created < now() - INTERVAL '1 hour');

-- Jobs requiring user intervention
WITH j AS (SHOW JOBS)
SELECT * FROM j
WHERE status IN ('failed', 'paused');

-- Terminal jobs (completed or failed)
WITH j AS (SHOW JOBS)
SELECT * FROM j
WHERE status IN ('succeeded', 'failed', 'canceled');
```

## References

**Official CockroachDB Documentation:**
- [SHOW JOBS](https://www.cockroachlabs.com/docs/stable/show-jobs.html)
- [Job States](https://www.cockroachlabs.com/docs/stable/ui-jobs-page.html#job-status)
- [PAUSE JOB](https://www.cockroachlabs.com/docs/stable/pause-job.html)
- [RESUME JOB](https://www.cockroachlabs.com/docs/stable/resume-job.html)
- [CANCEL JOB](https://www.cockroachlabs.com/docs/stable/cancel-job.html)
- [Garbage Collection](https://www.cockroachlabs.com/docs/stable/architecture/storage-layer.html#garbage-collection)
- [Protected Timestamps](https://www.cockroachlabs.com/docs/stable/architecture/storage-layer.html#protected-timestamps)

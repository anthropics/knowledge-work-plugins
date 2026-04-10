# SQL Query Variations

This reference provides ready-to-use query variations for common background job monitoring scenarios. All queries follow production-safe patterns with LIMIT clauses and time filtering.

## Time Threshold Variations

Adjust time windows based on your use case and expected job durations.

### Long-Running Jobs (Various Thresholds)

**30 minute threshold (for fast operations):**
```sql
-- Jobs running longer than 30 minutes
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  now() - created AS running_for,
  fraction_completed
FROM j
WHERE status = 'running'
  AND created < now() - INTERVAL '30 minutes'
ORDER BY created
LIMIT 50;
```

**1 hour threshold (general purpose):**
```sql
-- Jobs running longer than 1 hour
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  now() - created AS running_for,
  fraction_completed
FROM j
WHERE status = 'running'
  AND created < now() - INTERVAL '1 hour'
ORDER BY created
LIMIT 50;
```

**6 hour threshold (for large operations):**
```sql
-- Jobs running longer than 6 hours
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  now() - created AS running_for,
  fraction_completed,
  running_status
FROM j
WHERE status = 'running'
  AND created < now() - INTERVAL '6 hours'
ORDER BY created
LIMIT 50;
```

### Failed Jobs (Various Time Windows)

**Last 1 hour (recent failures):**
```sql
-- Recently failed jobs
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  finished,
  error
FROM j
WHERE status = 'failed'
  AND created > now() - INTERVAL '1 hour'
ORDER BY created DESC
LIMIT 50;
```

**Last 12 hours (default window):**
```sql
-- Failed jobs in default 12h window
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  finished,
  error
FROM j
WHERE status = 'failed'
  AND created > now() - INTERVAL '12 hours'
ORDER BY created DESC
LIMIT 50;
```

**Last 24 hours (daily summary):**
```sql
-- All failed jobs in last 24 hours
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
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC
LIMIT 100;
```

**Last 7 days (weekly summary):**
```sql
-- Failed jobs in last week (requires crdb_internal.jobs)
SELECT
  job_id,
  job_type,
  description,
  created,
  finished,
  error
FROM crdb_internal.jobs
WHERE status = 'failed'
  AND created > now() - INTERVAL '7 days'
ORDER BY created DESC
LIMIT 200;
```

## Job Type Filtering

Filter for specific job types based on your investigation focus.

### Backup and Restore Jobs

```sql
-- All backup and restore jobs in last 24h
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  COALESCE(finished, now()) - created AS duration,
  fraction_completed,
  error
FROM j
WHERE job_type IN ('BACKUP', 'RESTORE')
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC
LIMIT 50;
```

### Schema Change Jobs

```sql
-- All schema change related jobs
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  now() - created AS running_for,
  fraction_completed,
  running_status
FROM j
WHERE job_type IN ('SCHEMA CHANGE', 'NEW SCHEMA CHANGE', 'SCHEMA CHANGE GC')
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC
LIMIT 50;
```

### Automatic Statistics Jobs

```sql
-- AUTO CREATE STATS jobs in last 24h
SELECT
  job_id,
  description,
  status,
  created,
  finished,
  COALESCE(finished, now()) - created AS duration
FROM [SHOW AUTOMATIC JOBS]
WHERE job_type = 'AUTO CREATE STATS'
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC
LIMIT 100;
```

### Changefeed Jobs

```sql
-- All changefeed jobs (current status)
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  description,
  status,
  created,
  now() - created AS age,
  running_status
FROM j
WHERE job_type = 'CHANGEFEED'
ORDER BY created DESC
LIMIT 50;
```

## Status Combinations

Combine multiple status conditions for advanced filtering.

### Problematic Jobs (Failed OR Paused)

```sql
-- Jobs requiring attention (failed or paused)
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  COALESCE(finished, now()) - created AS duration,
  error
FROM j
WHERE status IN ('failed', 'paused')
  AND created > now() - INTERVAL '24 hours'
ORDER BY status, created DESC
LIMIT 50;
```

### Running Jobs with Long Duration

```sql
-- Long-running jobs that may be stuck
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  running_status,
  created,
  now() - created AS running_for,
  fraction_completed
FROM j
WHERE status = 'running'
  AND created < now() - INTERVAL '2 hours'
ORDER BY created
LIMIT 50;
```

### Pending Jobs Not Starting

```sql
-- Jobs stuck in pending state
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  now() - created AS pending_for,
  coordinator_id
FROM j
WHERE status = 'pending'
  AND created < now() - INTERVAL '10 minutes'
ORDER BY created
LIMIT 50;
```

### Failed OR Reverting Jobs

```sql
-- Jobs in error states (including rollback)
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  running_status,
  error
FROM j
WHERE status IN ('failed', 'reverting')
  AND created > now() - INTERVAL '24 hours'
ORDER BY status, created DESC
LIMIT 50;
```

## Historical Queries (crdb_internal.jobs)

For jobs older than SHOW JOBS retention (12h default), query the internal table directly.

### Jobs Older Than 12 Hours

```sql
-- Access historical jobs (up to 14 days)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  finished,
  COALESCE(finished, now()) - created AS duration
FROM crdb_internal.jobs
WHERE created > now() - INTERVAL '7 days'
  AND created < now() - INTERVAL '12 hours'
ORDER BY created DESC
LIMIT 100;
```

### Historical Failed Jobs by Type

```sql
-- Failed jobs by type in last 7 days
SELECT
  job_type,
  COUNT(*) AS failure_count,
  MIN(created) AS first_failure,
  MAX(created) AS last_failure
FROM crdb_internal.jobs
WHERE status = 'failed'
  AND created > now() - INTERVAL '7 days'
GROUP BY job_type
ORDER BY failure_count DESC;
```

### Historical Job Duration Analysis

```sql
-- Average duration by job type (last 7 days, succeeded only)
SELECT
  job_type,
  COUNT(*) AS job_count,
  ROUND(AVG(EXTRACT(epoch FROM (finished - created))), 2) AS avg_duration_seconds,
  ROUND(MAX(EXTRACT(epoch FROM (finished - created))), 2) AS max_duration_seconds
FROM crdb_internal.jobs
WHERE status = 'succeeded'
  AND created > now() - INTERVAL '7 days'
  AND finished IS NOT NULL
GROUP BY job_type
ORDER BY avg_duration_seconds DESC;
```

## Fraction Completed Analysis

Use progress tracking to monitor job completion and estimate remaining time.

### Jobs with Progress Tracking

```sql
-- Running jobs with completion percentage
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
      ROUND(EXTRACT(epoch FROM ((now() - created) / fraction_completed) - (now() - created)), 0)
    ELSE NULL
  END AS estimated_seconds_remaining
FROM j
WHERE status = 'running'
  AND job_type IN ('BACKUP', 'RESTORE', 'SCHEMA CHANGE', 'NEW SCHEMA CHANGE', 'IMPORT')
ORDER BY created
LIMIT 50;
```

### Stalled Jobs (No Progress)

```sql
-- Jobs with no progress in last hour (requires manual tracking)
-- Run this query, wait 1 hour, and re-run to compare fraction_completed
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS running_for,
  fraction_completed,
  running_status
FROM j
WHERE status = 'running'
  AND created < now() - INTERVAL '1 hour'
  AND fraction_completed IS NOT NULL
ORDER BY created
LIMIT 50;
-- Record fraction_completed values, then re-check after 15-30 minutes
```

### Near-Completion Jobs

```sql
-- Jobs almost finished (>90% complete)
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS running_for,
  ROUND(fraction_completed * 100, 2) AS percent_complete,
  running_status
FROM j
WHERE status = 'running'
  AND fraction_completed > 0.9
ORDER BY fraction_completed DESC
LIMIT 50;
```

## Error Analysis Patterns

Group and analyze error messages to identify patterns.

### Failed Jobs by Error Pattern

```sql
-- Group failures by error message prefix
WITH j AS (SHOW JOBS)
SELECT
  substring(error, 1, 100) AS error_prefix,
  job_type,
  COUNT(*) AS failure_count,
  array_agg(job_id ORDER BY created DESC) AS job_ids
FROM j
WHERE status = 'failed'
  AND created > now() - INTERVAL '24 hours'
GROUP BY substring(error, 1, 100), job_type
ORDER BY failure_count DESC
LIMIT 20;
```

### Permission Denied Errors

```sql
-- Find jobs failing due to permission issues
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  error
FROM j
WHERE status = 'failed'
  AND created > now() - INTERVAL '24 hours'
  AND error LIKE '%permission denied%'
ORDER BY created DESC
LIMIT 50;
```

### Timeout Errors

```sql
-- Find jobs failing due to timeouts
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS duration_before_failure,
  error
FROM j
WHERE status = 'failed'
  AND created > now() - INTERVAL '24 hours'
  AND (error LIKE '%timeout%' OR error LIKE '%timed out%')
ORDER BY created DESC
LIMIT 50;
```

### Constraint Violation Errors

```sql
-- Find jobs failing due to constraint violations
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  error
FROM j
WHERE status = 'failed'
  AND created > now() - INTERVAL '24 hours'
  AND (error LIKE '%constraint%' OR error LIKE '%violation%')
ORDER BY created DESC
LIMIT 50;
```

## Advanced Filtering

Combine multiple conditions for specific use cases.

### Failed Backups to Specific Destination

```sql
-- Failed backups to S3 (adjust pattern for your destination)
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  description,
  created,
  finished,
  error
FROM j
WHERE status = 'failed'
  AND job_type = 'BACKUP'
  AND description LIKE '%s3://%'
  AND created > now() - INTERVAL '7 days'
ORDER BY created DESC
LIMIT 50;
```

### Long-Running Schema Changes on Large Tables

```sql
-- Schema changes running > 2 hours with low progress
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  created,
  now() - created AS running_for,
  fraction_completed,
  running_status
FROM j
WHERE status = 'running'
  AND job_type IN ('SCHEMA CHANGE', 'NEW SCHEMA CHANGE')
  AND created < now() - INTERVAL '2 hours'
  AND (fraction_completed IS NULL OR fraction_completed < 0.5)
ORDER BY created
LIMIT 50;
```

### Automatic Jobs Health Check

```sql
-- Summary of automatic job health in last 24h
SELECT
  job_type,
  status,
  COUNT(*) AS job_count,
  MIN(created) AS first_job,
  MAX(created) AS last_job,
  ROUND(AVG(EXTRACT(epoch FROM (COALESCE(finished, now()) - created))), 2) AS avg_duration_seconds
FROM [SHOW AUTOMATIC JOBS]
WHERE created > now() - INTERVAL '24 hours'
GROUP BY job_type, status
ORDER BY job_type, status;
```

### Jobs by Coordinator Node

```sql
-- Jobs grouped by coordinator node (for cluster-wide analysis)
WITH j AS (SHOW JOBS)
SELECT
  coordinator_id,
  job_type,
  status,
  COUNT(*) AS job_count
FROM j
WHERE created > now() - INTERVAL '24 hours'
GROUP BY coordinator_id, job_type, status
ORDER BY coordinator_id, job_type, status;
```

### MVCC GC Wait Duration Analysis

```sql
-- SCHEMA CHANGE GC jobs with wait duration
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  description,
  created,
  now() - created AS waiting_for,
  running_status,
  CASE
    WHEN now() - created > INTERVAL '50 hours' THEN 'INVESTIGATE'
    WHEN now() - created > INTERVAL '25 hours' THEN 'MONITOR'
    ELSE 'NORMAL'
  END AS assessment
FROM j
WHERE status = 'running'
  AND job_type = 'SCHEMA CHANGE GC'
  AND running_status LIKE '%waiting for MVCC GC%'
ORDER BY created
LIMIT 50;
```

### Jobs by Description Pattern

```sql
-- Find jobs affecting specific table
WITH j AS (SHOW JOBS)
SELECT
  job_id,
  job_type,
  description,
  status,
  created,
  fraction_completed
FROM j
WHERE description LIKE '%your_table_name%'
  AND created > now() - INTERVAL '7 days'
ORDER BY created DESC
LIMIT 50;
```

## Aggregation and Summary Queries

Get high-level views of job activity.

### Daily Job Summary

```sql
-- Job counts by type and status per day (last 7 days)
SELECT
  DATE_TRUNC('day', created) AS day,
  job_type,
  status,
  COUNT(*) AS job_count
FROM crdb_internal.jobs
WHERE created > now() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('day', created), job_type, status
ORDER BY day DESC, job_type, status;
```

### Success Rate by Job Type

```sql
-- Success rate for each job type (last 7 days)
SELECT
  job_type,
  COUNT(*) AS total_jobs,
  SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END) AS succeeded_count,
  SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_count,
  ROUND(
    SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END)::NUMERIC /
    NULLIF(COUNT(*), 0) * 100,
    2
  ) AS success_rate_pct
FROM crdb_internal.jobs
WHERE created > now() - INTERVAL '7 days'
  AND status IN ('succeeded', 'failed')
GROUP BY job_type
ORDER BY total_jobs DESC;
```

### Peak Job Activity Times

```sql
-- Jobs started per hour (last 24 hours)
SELECT
  DATE_TRUNC('hour', created) AS hour,
  COUNT(*) AS jobs_started
FROM crdb_internal.jobs
WHERE created > now() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', created)
ORDER BY hour DESC;
```

## Production Safety Notes

All queries in this reference follow production-safe patterns:

- **LIMIT clauses:** Prevent overwhelming output on large clusters
- **Time filtering:** Reduce result set size and query overhead
- **CTE usage:** Improve readability and enable easy filtering
- **Read-only operations:** No data modification or job control
- **Duration calculations:** Use `now() - created` for consistent timestamps
- **NULL handling:** Use `COALESCE` for fields that may be NULL

**Best practices:**
- Start with shorter time windows (1h, 24h) before expanding to 7d
- Increase LIMIT if you need more results, but be cautious on large clusters
- Add filters for specific job types when investigating targeted issues
- Use `crdb_internal.jobs` for historical analysis beyond 12h
- Combine multiple filters to narrow results efficiently

## References

**Related skill documentation:**
- [Main skill guide](../SKILL.md)
- [Job types catalog](job-types.md)
- [Job states reference](job-states.md)
- [Permissions setup](permissions.md)

**Official CockroachDB Documentation:**
- [SHOW JOBS](https://www.cockroachlabs.com/docs/stable/show-jobs.html)
- [SHOW AUTOMATIC JOBS](https://www.cockroachlabs.com/docs/stable/show-automatic-jobs.html)
- [crdb_internal](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)

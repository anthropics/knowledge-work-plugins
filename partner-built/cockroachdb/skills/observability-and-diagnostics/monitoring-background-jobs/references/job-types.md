# Job Types Catalog

This reference provides detailed information about CockroachDB background job types, their characteristics, and how to filter for specific job types.

## Job Type Categories

CockroachDB background jobs fall into two broad categories:

| Category | Initiated By | Appears In | Examples |
|----------|-------------|------------|----------|
| **User-initiated** | Explicit SQL commands | `SHOW JOBS`, `SHOW AUTOMATIC JOBS` (some) | BACKUP, RESTORE, SCHEMA CHANGE |
| **Automatic** | CockroachDB system | `SHOW AUTOMATIC JOBS` | AUTO CREATE STATS, SCHEMA CHANGE GC |

## User-Initiated Job Types

These jobs are triggered by explicit user SQL commands.

### SCHEMA CHANGE

**Triggered by:**
- `ALTER TABLE ... ADD COLUMN`
- `ALTER TABLE ... DROP COLUMN`
- `ALTER TABLE ... ALTER COLUMN TYPE`
- `CREATE INDEX` (legacy syntax)
- `DROP INDEX`
- `ALTER TABLE ... ADD CONSTRAINT`

**Characteristics:**
- **Expected duration:** Minutes to hours (depends on table size and operation type)
- **Progress tracking:** `fraction_completed` available for backfill operations
- **Running status:** `populating schema`, `backfilling`, `validating`, `merging`
- **Failure risk:** Medium (can fail due to constraints, disk space, or conflicts)

**Common failure patterns:**
- Constraint violations during backfill (e.g., adding NOT NULL to column with NULLs)
- Concurrent schema changes on same table
- Disk space exhaustion during index build
- Cluster node failures during execution

**When to intervene:**
- Schema change running > 6 hours on small table (< 1 GB): Investigate
- Status stuck at same `fraction_completed` for > 1 hour: Check for contention
- Failed with constraint error: Fix data and retry

### NEW SCHEMA CHANGE

**Triggered by:**
- Same operations as SCHEMA CHANGE (modern schema change infrastructure)
- Enabled by default in recent CockroachDB versions

**Differences from legacy SCHEMA CHANGE:**
- Better rollback handling (automatic revert on failure)
- Improved concurrency (fewer conflicts with other schema changes)
- More granular progress tracking

**Characteristics:**
- **Expected duration:** Similar to legacy SCHEMA CHANGE
- **Progress tracking:** More detailed `fraction_completed` and `running_status`
- **Failure risk:** Lower than legacy (better error handling)

**Recommendation:** Prefer NEW SCHEMA CHANGE when available (default in v22.2+).

### BACKUP

**Triggered by:**
- `BACKUP DATABASE`
- `BACKUP TABLE`
- `BACKUP <targets> TO <destination>`

**Characteristics:**
- **Expected duration:** 1-6+ hours (depends on data volume and network bandwidth)
- **Progress tracking:** `fraction_completed` available; `running_status` shows destination
- **Running status:** `performing backup`, `performing backup <percentage>`
- **Failure risk:** Medium (network, permissions, disk space at destination)

**Common failure patterns:**
- External storage authentication failures (S3, GCS, Azure)
- Network timeouts or interruptions
- Insufficient space at backup destination
- Missing permissions on destination bucket

**When to intervene:**
- Backup running > 2x expected duration: Check network bandwidth and destination
- Failed with auth error: Verify credentials and bucket permissions
- Failed with "no space left": Expand destination storage or clean old backups
- Paused or stalled: Resume or cancel and retry

### RESTORE

**Triggered by:**
- `RESTORE DATABASE`
- `RESTORE TABLE`
- `RESTORE <targets> FROM <backup_location>`

**Characteristics:**
- **Expected duration:** Similar to BACKUP (1-6+ hours for large datasets)
- **Progress tracking:** `fraction_completed` available
- **Running status:** `restoring`
- **Failure risk:** Medium to high (constraint violations, disk space)

**Common failure patterns:**
- Constraint violations (restored data conflicts with existing data)
- Disk space exhaustion on cluster nodes
- Backup file corruption or missing files
- Version incompatibility (restoring from newer version to older)

**When to intervene:**
- Failed with constraint error: Drop conflicting objects or use `WITH skip_missing_foreign_keys`
- Failed with disk space error: Expand cluster storage or remove data
- Stuck at low `fraction_completed`: Check backup file accessibility
- Reverting for long time: Wait for rollback to complete, then investigate error

**Important:** Canceled or failed restores may leave partial data. Verify database state after restore failures.

### CHANGEFEED

**Triggered by:**
- `CREATE CHANGEFEED FOR <tables>`
- Enterprise feature for change data capture (CDC)

**Characteristics:**
- **Expected duration:** Infinite (runs continuously until canceled)
- **Progress tracking:** `fraction_completed` not applicable (continuous job)
- **Running status:** Shows sink destination and high-water mark
- **Failure risk:** Medium (sink availability, network, schema changes)

**Common failure patterns:**
- Sink endpoint unavailable (Kafka, webhook, cloud storage)
- Schema changes on watched tables (may require changefeed restart)
- Network interruptions to sink
- Insufficient permissions on sink destination

**When to intervene:**
- Failed or paused: Check sink availability and permissions
- Long-running is normal: Changefeeds run indefinitely
- High retry count in logs: Investigate sink reliability

**Note:** Changefeeds can hold back garbage collection if they lag significantly. Monitor high-water mark.

### IMPORT

**Triggered by:**
- `IMPORT TABLE`
- `IMPORT INTO`

**Characteristics:**
- **Expected duration:** 1-6+ hours (depends on data volume)
- **Progress tracking:** `fraction_completed` available
- **Running status:** Shows import source
- **Failure risk:** Medium (data format errors, constraints, disk space)

**Common failure patterns:**
- CSV/JSON parsing errors (malformed data)
- Constraint violations (duplicate keys, foreign key violations)
- Disk space exhaustion
- Network issues accessing import source

**When to intervene:**
- Failed with parsing error: Fix source data format and retry
- Failed with constraint error: Adjust constraints or clean data
- Stuck at low progress: Check source file accessibility

## Automatic Job Types

These jobs are triggered automatically by CockroachDB for maintenance and optimization.

### SCHEMA CHANGE GC

**Triggered by:**
- Automatically after `DROP TABLE`
- Automatically after `DROP INDEX`
- Automatically after `TRUNCATE TABLE`

**Purpose:** Physically remove dropped table/index data after GC threshold.

**Characteristics:**
- **Expected duration:** Up to `gc.ttlseconds` (default 25 hours)
- **Progress tracking:** `fraction_completed` typically NULL
- **Running status:** `waiting for MVCC GC`, `waiting for GC TTL`
- **Failure risk:** Low (automatic retry)

**Common patterns:**
- **Long "waiting for MVCC GC":** Normal; duration tied to `gc.ttlseconds` setting
- **Failed with GC error:** Usually safe to ignore; will retry automatically
- **Multiple SCHEMA CHANGE GC jobs:** Normal after bulk DROP operations

**When to intervene:**
- Running > 2x `gc.ttlseconds`: Investigate for long-running transactions or protected timestamps
- Failed repeatedly: Check cluster logs for GC subsystem issues
- Usually no intervention needed: These jobs self-manage

See [job states reference](job-states.md) for detailed "waiting for MVCC GC" explanation.

### AUTO CREATE STATS

**Triggered by:**
- Automatically when table row count changes significantly
- Controlled by `sql.stats.automatic_collection.enabled` setting

**Purpose:** Refresh table statistics for query optimizer to generate efficient query plans.

**Characteristics:**
- **Expected duration:** Seconds to minutes (depends on table size)
- **Progress tracking:** `fraction_completed` may be available
- **Running status:** Shows target table
- **Failure risk:** Low to medium

**Common failure patterns:**
- Timeout on very large tables (> 10 GB)
- Resource constraints during high load
- Concurrent schema changes blocking statistics collection

**When to intervene:**
- No AUTO CREATE STATS in last 24h: Check `sql.stats.automatic_collection.enabled = true`
- High failure rate: Increase `sql.stats.automatic_collection.min_stale_rows` or reduce load
- Failed on specific table repeatedly: Manually collect stats with `CREATE STATISTICS`

**Impact of failure:**
- Stale statistics lead to poor query plans
- Queries may become slower over time
- Full table scans instead of index scans

**Health check:**
```sql
-- Should see successful stats jobs regularly
SELECT job_type, status, COUNT(*) AS job_count
FROM [SHOW AUTOMATIC JOBS]
WHERE created > now() - INTERVAL '24 hours'
  AND job_type = 'AUTO CREATE STATS'
GROUP BY job_type, status;
```

### AUTO SQL STATS COMPACTION

**Triggered by:**
- Automatically on a schedule (typically hourly)
- Controlled by system settings

**Purpose:** Truncate old statement and transaction statistics to prevent unbounded table growth.

**Characteristics:**
- **Expected duration:** Seconds to minutes
- **Progress tracking:** `fraction_completed` typically NULL
- **Running status:** Usually empty
- **Failure risk:** Low

**Common failure patterns:**
- Resource constraints during high load
- Very rare failures (highly resilient job)

**When to intervene:**
- No compaction jobs in last 24h: Verify cluster settings
- Failed repeatedly: Check cluster logs for stats system issues
- Usually no intervention needed: Automatic retry handles failures

**Impact of failure:**
- `crdb_internal.statement_statistics` table grows unbounded
- `crdb_internal.transaction_statistics` table grows unbounded
- May impact query performance on statement stats queries

## SHOW JOBS vs SHOW AUTOMATIC JOBS

Different job types appear in different interfaces:

| Job Type | `SHOW JOBS` | `SHOW AUTOMATIC JOBS` |
|----------|-------------|----------------------|
| SCHEMA CHANGE | ✓ | ✗ |
| NEW SCHEMA CHANGE | ✓ | ✗ |
| BACKUP | ✓ | ✗ |
| RESTORE | ✓ | ✗ |
| CHANGEFEED | ✓ | ✗ |
| IMPORT | ✓ | ✗ |
| SCHEMA CHANGE GC | ✓ | ✓ |
| AUTO CREATE STATS | ✓ | ✓ |
| AUTO SQL STATS COMPACTION | ✓ | ✓ |

**Key takeaway:**
- `SHOW JOBS`: All jobs (user-initiated + automatic)
- `SHOW AUTOMATIC JOBS`: Only automatic jobs (subset of SHOW JOBS)

## Job Type Filtering

### Filter by Specific Job Type

```sql
-- Find all backup jobs in last 24 hours
WITH j AS (SHOW JOBS)
SELECT job_id, description, status, created, finished
FROM j
WHERE job_type = 'BACKUP'
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC;
```

### Filter by Multiple Job Types

```sql
-- Find all schema change related jobs
WITH j AS (SHOW JOBS)
SELECT job_id, job_type, description, status, created
FROM j
WHERE job_type IN ('SCHEMA CHANGE', 'NEW SCHEMA CHANGE', 'SCHEMA CHANGE GC')
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC;
```

### Filter Automatic Jobs Only

```sql
-- Find failed automatic jobs
SELECT job_id, job_type, description, error
FROM [SHOW AUTOMATIC JOBS]
WHERE status = 'failed'
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC;
```

### Group by Job Type

```sql
-- Job distribution by type and status
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

### Filter by Job Type Pattern

```sql
-- Find all schema-related jobs
WITH j AS (SHOW JOBS)
SELECT job_id, job_type, description, status
FROM j
WHERE job_type LIKE '%SCHEMA%'
ORDER BY created DESC
LIMIT 50;
```

## Job Type Characteristics Summary

| Job Type | User-Initiated? | Long-Running? | Automatic Retry? | Safe to Cancel? |
|----------|----------------|---------------|------------------|-----------------|
| SCHEMA CHANGE | Yes | Yes (hours) | No | No (may leave inconsistent state) |
| NEW SCHEMA CHANGE | Yes | Yes (hours) | No | No (automatic revert on failure) |
| BACKUP | Yes | Yes (hours) | No | Yes (can re-run) |
| RESTORE | Yes | Yes (hours) | No | Caution (may need cleanup) |
| CHANGEFEED | Yes | Infinite | Configurable | Yes (can recreate) |
| IMPORT | Yes | Yes (hours) | No | Yes (can re-run) |
| SCHEMA CHANGE GC | No | Yes (up to gc.ttlseconds) | Yes | No (causes disk space leak) |
| AUTO CREATE STATS | No | No (minutes) | Yes | Yes (will retry) |
| AUTO SQL STATS COMPACTION | No | No (minutes) | Yes | Yes (will retry) |

## Monitoring Recommendations by Job Type

### High-Priority Monitoring (User Impact)

Monitor these actively as failures impact users:
- **SCHEMA CHANGE / NEW SCHEMA CHANGE:** Monitor for stuck or failed jobs
- **BACKUP:** Monitor for failures (data loss risk)
- **RESTORE:** Monitor for failures and reverting state
- **AUTO CREATE STATS:** Monitor for sustained failure (degrades query performance)

### Medium-Priority Monitoring (Operational)

Monitor periodically:
- **CHANGEFEED:** Check for lag or failures
- **IMPORT:** Monitor during active imports
- **SCHEMA CHANGE GC:** Monitor for excessive wait times (> 2x gc.ttlseconds)

### Low-Priority Monitoring (Self-Healing)

Check only if issues suspected:
- **AUTO SQL STATS COMPACTION:** Rarely fails; self-healing

## Troubleshooting by Job Type

### SCHEMA CHANGE / NEW SCHEMA CHANGE Stuck

**Symptoms:**
- Job running for hours with no progress
- `fraction_completed` not increasing

**Diagnosis:**
```sql
-- Check for concurrent schema changes on same table
WITH j AS (SHOW JOBS)
SELECT job_id, description, status, created,
       fraction_completed, running_status
FROM j
WHERE job_type IN ('SCHEMA CHANGE', 'NEW SCHEMA CHANGE')
  AND status = 'running'
ORDER BY created;
```

**Possible causes:**
- Large table backfill in progress (normal)
- Concurrent schema change blocking (wait for first to complete)
- Resource constraints (CPU, memory, disk)

### BACKUP Failures

**Symptoms:**
- Backup jobs consistently failing
- Error messages about external storage

**Diagnosis:**
```sql
-- Check recent backup failures
WITH j AS (SHOW JOBS)
SELECT job_id, description, created, error
FROM j
WHERE job_type = 'BACKUP'
  AND status = 'failed'
  AND created > now() - INTERVAL '7 days'
ORDER BY created DESC;
```

**Common fixes:**
- Verify external storage credentials
- Check network connectivity to storage endpoint
- Ensure sufficient space at destination
- Verify bucket permissions

### AUTO CREATE STATS Not Running

**Symptoms:**
- No statistics jobs in last 24 hours
- Queries getting slower over time

**Diagnosis:**
```sql
-- Check automatic collection setting
SHOW CLUSTER SETTING sql.stats.automatic_collection.enabled;

-- Check recent stats jobs
SELECT job_type, status, COUNT(*)
FROM [SHOW AUTOMATIC JOBS]
WHERE created > now() - INTERVAL '24 hours'
  AND job_type = 'AUTO CREATE STATS'
GROUP BY job_type, status;
```

**Common fixes:**
- Enable automatic collection: `SET CLUSTER SETTING sql.stats.automatic_collection.enabled = true`
- Check min_stale_rows threshold: `SHOW CLUSTER SETTING sql.stats.automatic_collection.min_stale_rows`
- Manually trigger stats: `CREATE STATISTICS __auto__ FROM <table_name>`

## References

**Official CockroachDB Documentation:**
- [SHOW JOBS](https://www.cockroachlabs.com/docs/stable/show-jobs.html)
- [SHOW AUTOMATIC JOBS](https://www.cockroachlabs.com/docs/stable/show-automatic-jobs.html)
- [BACKUP](https://www.cockroachlabs.com/docs/stable/backup.html)
- [RESTORE](https://www.cockroachlabs.com/docs/stable/restore.html)
- [CREATE CHANGEFEED](https://www.cockroachlabs.com/docs/stable/create-changefeed.html)
- [IMPORT](https://www.cockroachlabs.com/docs/stable/import.html)
- [Online Schema Changes](https://www.cockroachlabs.com/docs/stable/online-schema-changes.html)
- [Table Statistics](https://www.cockroachlabs.com/docs/stable/cost-based-optimizer.html#table-statistics)
- [Garbage Collection](https://www.cockroachlabs.com/docs/stable/architecture/storage-layer.html#garbage-collection)

---
name: profiling-statement-fingerprints
description: Ranks and analyzes statement fingerprints using aggregated SQL statistics from crdb_internal.statement_statistics to identify slow, resource-intensive, or error-prone query patterns. Use when investigating historical performance trends, identifying optimization opportunities, or diagnosing recurring slowness without DB Console access.
compatibility: Requires SQL access with VIEWACTIVITY or VIEWACTIVITYREDACTED cluster privilege. Uses crdb_internal.statement_statistics (production-safe). Execution statistics fields are sampled and may be sparse.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Profiling Statement Fingerprints

Analyzes historical statement performance patterns using aggregated SQL statistics to identify slow, resource-intensive, or error-prone query fingerprints. Uses `crdb_internal.statement_statistics` for time-windowed analysis of latency, CPU, contention, admission delays, and failure rates - entirely via SQL without requiring DB Console access.

**Complement to triaging-live-sql-activity:** This skill analyzes historical patterns; for immediate triage of currently running queries, see [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md).

## When to Use This Skill

- Identify slowest statement fingerprints over past hours/days/weeks
- Find queries with high CPU consumption, contention, or admission waits
- Investigate performance regressions or plan changes
- Locate full table scans or missing indexes via index recommendations
- Analyze resource consumption by application or database
- SQL-only historical analysis without DB Console access

**For immediate incident response:** Use [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) to triage currently running queries and cancel runaway work.
**For transaction-level analysis:** Use [profiling-transaction-fingerprints](../profiling-transaction-fingerprints/SKILL.md) to analyze retry patterns, commit latency, and statement composition at the transaction boundary.
**For background job monitoring:** Use [monitoring-background-jobs](../monitoring-background-jobs/SKILL.md) for long-running schema changes and automatic jobs excluded from statement statistics.

## Prerequisites

- SQL connection to CockroachDB cluster
- `VIEWACTIVITY` or `VIEWACTIVITYREDACTED` cluster privilege for cluster-wide visibility
- Statement statistics collection enabled (default): `sql.stats.automatic_collection.enabled = true`

**Check collection status:**
```sql
SHOW CLUSTER SETTING sql.stats.automatic_collection.enabled;  -- Should return: true
```

See [triaging-live-sql-activity permissions reference](../triaging-live-sql-activity/references/permissions.md) for RBAC setup (same privileges).

## Core Concepts

### Statement Fingerprints vs Live Queries

**Statement fingerprint:** Normalized SQL pattern with parameterized constants (e.g., `SELECT * FROM users WHERE id = $1` vs `SELECT * FROM users WHERE id = 123`)

**Key differences:**
- **Time scope:** Historical hourly buckets vs real-time current state
- **Granularity:** Aggregated pattern statistics vs individual execution instances

### Time-Series Bucketing

**aggregated_ts:** Hourly UTC buckets (e.g., `2026-02-21 14:00:00` = 14:00-14:59 executions)
**Data retention:** Default ~7 days (check `sql.stats.persisted_rows.max`)
**Best practice:** Always filter by time window: `WHERE aggregated_ts > now() - INTERVAL '24 hours'`

### Aggregated vs Sampled Metrics

| Metric Category | JSON Path | Scope | Use Case |
|-----------------|-----------|-------|----------|
| **Aggregated** | `statistics.statistics.*` | All executions | Latency, row counts, execution counts |
| **Sampled** | `statistics.execution_statistics.*` | ~10% sample | CPU, contention, admission wait, memory/disk |

**Critical:** Always check sampled metrics presence: `WHERE (statistics->'execution_statistics'->>'cnt') IS NOT NULL`

### JSON Field Extraction

**Operators:**
- `->`: Extract JSON object (returns JSON)
- `->>`: Extract as text (returns text)
- `::TYPE`: Cast to specific type

**Examples:**
```sql
metadata->>'db'                                              -- Database name
(statistics->'statistics'->>'cnt')::INT                      -- Execution count
(statistics->'statistics'->'runLat'->>'mean')::FLOAT8        -- Mean latency (seconds)
(statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9  -- CPU (convert nanos to seconds)
```

**Units:** Latency = seconds, CPU/admission = nanoseconds (÷ 1e9), Memory/disk = bytes (÷ 1048576 for MB)

See [JSON field reference](references/json-field-reference.md) for complete schema.

## Core Diagnostic Queries

### Query 1: Top Statements by Mean Run Latency

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  metadata->>'query' AS query_text,
  (statistics->'statistics'->>'cnt')::INT AS execution_count,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_run_lat_seconds,
  (statistics->'statistics'->'runLat'->>'max')::FLOAT8 AS max_run_lat_seconds,
  (metadata->>'fullScan')::BOOL AS full_scan,
  metadata->'index_recommendations' AS index_recommendations,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 > 1.0  -- > 1 second mean latency
ORDER BY (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 DESC
LIMIT 20;
```

**Focus:** Slowest queries; check `full_scan` and `index_recommendations` for optimization opportunities.

### Query 2: Admission Control Impact

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  metadata->>'query' AS query_text,
  (statistics->'statistics'->>'cnt')::INT AS execution_count,
  (statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 / 1e9 AS mean_admission_wait_seconds,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_run_lat_seconds,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 > 0
ORDER BY (statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 DESC
LIMIT 20;
```

**Interpretation:** High admission wait = cluster at resource limits (CPU, memory, I/O). Ratio > 1.0 (wait > runtime) indicates severe queueing.

### Query 3: Plan Hash Diversity

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  metadata->>'query' AS query_text,
  COUNT(DISTINCT plan_hash) AS distinct_plan_count,
  array_agg(DISTINCT plan_hash ORDER BY plan_hash) AS plan_hashes,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '7 days'
GROUP BY fingerprint_id, metadata->>'db', metadata->>'query'
HAVING COUNT(DISTINCT plan_hash) > 1
ORDER BY COUNT(DISTINCT plan_hash) DESC, SUM((statistics->'statistics'->>'cnt')::INT) DESC
LIMIT 20;
```

**Interpretation:** Multiple plans indicate instability from schema changes, statistics updates, or routing changes. Performance can vary significantly between plans.

### Query 4: High Contention Statements

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  metadata->>'app' AS application,
  substring(metadata->>'query', 1, 150) AS query_preview,
  (statistics->'statistics'->>'cnt')::INT AS execution_count,
  (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9 AS mean_contention_seconds,
  ROUND(
    ((statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9) /
    NULLIF((statistics->'statistics'->'runLat'->>'mean')::FLOAT8, 0) * 100, 2
  ) AS contention_pct_of_runtime,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 > 0
ORDER BY (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 DESC
LIMIT 20;
```

**Interpretation:** >20% contention = transaction conflicts, hot row access. Remediate with batching, transaction boundary changes, or schema redesign.

### Query 5: High CPU Consumers

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  substring(metadata->>'query', 1, 150) AS query_preview,
  (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9 AS mean_cpu_seconds,
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  ROUND(
    ((statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9) *
    (statistics->'statistics'->>'cnt')::INT, 2
  ) AS estimated_total_cpu_seconds,
  (metadata->>'fullScan')::BOOL AS full_scan,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 > 0
ORDER BY estimated_total_cpu_seconds DESC
LIMIT 20;
```

**Focus:** `estimated_total_cpu_seconds` shows cluster impact. High mean CPU often correlates with `full_scan = true`.

### Query 6: Memory and Disk Spill Detection

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  substring(metadata->>'query', 1, 150) AS query_preview,
  (statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576 AS mean_mem_mb,
  (statistics->'execution_statistics'->'maxMemUsage'->>'max')::FLOAT8 / 1048576 AS max_mem_mb,
  (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1048576 AS mean_disk_mb,
  (statistics->'execution_statistics'->'maxDiskUsage'->>'max')::FLOAT8 / 1048576 AS max_disk_mb,
  metadata->>'stmtType' AS statement_type,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 > 0  -- Has disk spills
ORDER BY (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 DESC
LIMIT 20;
```

**Interpretation:** Disk usage > 0 = memory spill (~100-1000x slower than in-memory). Common for large aggregations, sorts, hash joins. Fix with indexes or increased `sql.distsql.temp_storage.workmem`.

### Query 7: Error-Prone Statements

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  substring(metadata->>'query', 1, 150) AS query_preview,
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) AS failure_count,
  ROUND(
    COALESCE((statistics->'statistics'->>'failureCount')::INT, 0)::NUMERIC /
    NULLIF((statistics->'statistics'->>'cnt')::INT, 0) * 100, 2
  ) AS failure_rate_pct,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'cnt')::INT > 10
  AND COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) > 0
ORDER BY failure_rate_pct DESC, failure_count DESC
LIMIT 20;
```

**Common causes:** Constraint violations, query timeouts, transaction retry errors (40001), permission denied.

## Common Workflows

### Workflow 1: Slowness Investigation

1. **Identify slow fingerprints:** Run Query 1 with 24h window, focus on `mean_run_lat_seconds > 5` and high execution counts
2. **Check for full scans:** Filter `full_scan = true`, review `index_recommendations`
3. **Correlate to applications:** Group by `metadata->>'app'`, contact teams with specific patterns
4. **Cross-reference live activity:** If ongoing, use triaging-live-sql-activity to cancel runaway queries

### Workflow 2: Contention Analysis

1. **Find high-contention statements:** Run Query 4, focus on `contention_pct_of_runtime > 20%`
2. **Check plan stability:** Run Query 3 for contending fingerprints (plan changes affect lock order)
3. **Remediate:** Batch operations, use `SELECT FOR UPDATE`, partition hot tables, denormalize schema

### Workflow 3: Admission Control Debugging

1. **Identify admission waits:** Run Query 2, calculate wait ratio
2. **Correlate with CPU:** Run Query 5 for same window, cross-reference fingerprint IDs
3. **Analyze time patterns:** Group by `aggregated_ts` to find peak periods
4. **Triage:** Short-term: spread batch jobs; Long-term: add capacity, optimize queries

### Workflow 4: Memory Spill Investigation

1. **Find spilling statements:** Run Query 6, focus on `max_disk_mb > 100`
2. **Analyze patterns:** Identify large `GROUP BY`, `ORDER BY`, hash joins
3. **Remediate:** Add indexes, increase workmem (with caution), rewrite queries, use materialized views

## Safety Considerations

**Read-only operations:** All queries are `SELECT` statements against production-approved `crdb_internal.statement_statistics`.

**Performance impact:**

| Consideration | Impact | Mitigation |
|---------------|--------|------------|
| Large table | Many rows with high statement diversity | Always use time filters and `LIMIT` |
| JSON parsing | CPU overhead | Use specific time windows, avoid tight loops |
| Broad windows | 7-day queries = more rows | Default to 24h; expand only when needed |

**Privacy:** Use `VIEWACTIVITYREDACTED` to redact query constants in multi-tenant environments.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Empty results | No data or stats collection disabled | Check `sql.stats.automatic_collection.enabled = true` |
| `column does not exist` | JSON field typo or version mismatch | Verify field names; check CockroachDB version |
| NULL in sampled metrics | Metric not sampled in bucket | Filter: `WHERE (statistics->'execution_statistics'->>'cnt') IS NOT NULL` |
| Query text shows `<hidden>` | Using VIEWACTIVITYREDACTED | Expected; use VIEWACTIVITY if authorized |
| "invalid input syntax for type json" | Malformed JSON path | Check operators: `->` for JSON, `->>` for text |
| Very slow query | Large table, no time filter | Always add time window and LIMIT |
| Empty `index_recommendations` | No recommendations or optimal | Normal if indexes exist |

## Key Considerations

- **Time windows:** Default to 24h; expand to 7d for trends
- **Sampled metrics:** Not all executions captured; check sample size (`cnt`)
- **JSON safety:** Use defensive NULL checks; handle type casting errors
- **Privacy:** Use VIEWACTIVITYREDACTED in production
- **Performance:** Always include time filters and LIMIT
- **Complement to live triage:** Use together for complete coverage (historical + real-time)
- **Data retention:** Default ~7 days; verify with `sql.stats.persisted_rows.max`
- **Plan instability:** Multiple plan hashes indicate optimizer/schema changes

## References

**Skill references:**
- [JSON field schema and extraction](references/json-field-reference.md)
- [Metrics catalog and units](references/metrics-and-units.md)
- [SQL query variations](references/sql-query-variations.md)
- [RBAC and privileges](../triaging-live-sql-activity/references/permissions.md) (shared with triaging-live-sql-activity)

**Official CockroachDB Documentation:**
- [crdb_internal](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)
- [Statements Page (DB Console)](https://www.cockroachlabs.com/docs/stable/ui-statements-page.html)
- [Monitor and Analyze Transaction Contention](https://www.cockroachlabs.com/docs/stable/monitor-and-analyze-transaction-contention.html)
- [VIEWACTIVITY privilege](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

**Related skills:**
- [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) - For immediate triage of currently running queries
- [profiling-transaction-fingerprints](../profiling-transaction-fingerprints/SKILL.md) - For transaction-level analysis including retry patterns and commit latency

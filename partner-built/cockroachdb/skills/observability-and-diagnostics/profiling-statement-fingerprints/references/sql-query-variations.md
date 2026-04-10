# SQL Query Variations

Extended library of query patterns for statement fingerprint analysis. Includes time window variations, filtering patterns, aggregations, trend analysis, and advanced techniques.

## Time Window Variations

### 1-Hour Recent Activity

Quick check for most recent performance issues:

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  substring(metadata->>'query', 1, 100) AS query_preview,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat_sec,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '1 hour'
ORDER BY (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 DESC
LIMIT 10;
```

**Use case:** Real-time performance monitoring, immediate issue detection

### 6-Hour Window

Recent trends without overwhelming data:

```sql
SELECT
  fingerprint_id,
  metadata->>'app' AS application,
  COUNT(DISTINCT aggregated_ts) AS num_hourly_buckets,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS avg_mean_lat_sec,
  MAX((statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS max_mean_lat_sec
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '6 hours'
GROUP BY fingerprint_id, metadata->>'app'
HAVING SUM((statistics->'statistics'->>'cnt')::INT) > 100
ORDER BY avg_mean_lat_sec DESC
LIMIT 20;
```

**Use case:** Shift-over-shift comparison, recent pattern detection

### 7-Day Historical Analysis

Long-term trends and pattern identification:

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  substring(metadata->>'query', 1, 150) AS query_preview,
  COUNT(DISTINCT aggregated_ts) AS num_buckets,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS avg_latency,
  stddev((statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS latency_stddev,
  MIN(aggregated_ts) AS first_seen,
  MAX(aggregated_ts) AS last_seen
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '7 days'
GROUP BY fingerprint_id, metadata->>'db', metadata->>'query'
HAVING SUM((statistics->'statistics'->>'cnt')::INT) > 1000
ORDER BY total_executions DESC
LIMIT 50;
```

**Use case:** Weekly performance review, trend analysis, capacity planning

### Custom Date Range

Analyze specific time periods (e.g., incident windows):

```sql
SELECT
  fingerprint_id,
  metadata->>'query' AS query,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat,
  aggregated_ts
FROM crdb_internal.statement_statistics
WHERE aggregated_ts BETWEEN '2026-02-20 14:00:00' AND '2026-02-20 18:00:00'
ORDER BY aggregated_ts, mean_lat DESC;
```

**Use case:** Post-incident analysis, deployment comparison

## Filtering Patterns

### By Application Name

Isolate specific application performance:

```sql
SELECT
  fingerprint_id,
  metadata->>'app' AS application,
  substring(metadata->>'query', 1, 100) AS query_preview,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat_sec
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND metadata->>'app' = 'payments-api'
ORDER BY mean_lat_sec DESC
LIMIT 20;
```

**Variation - Multiple applications:**
```sql
WHERE metadata->>'app' IN ('payments-api', 'orders-service', 'inventory-api')
```

### By Database

Focus on specific database performance:

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat_sec
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND metadata->>'db' = 'production_db'
ORDER BY executions DESC
LIMIT 30;
```

### By Statement Type

Analyze specific operation types:

```sql
-- Focus on SELECT queries only
SELECT
  fingerprint_id,
  substring(metadata->>'query', 1, 150) AS query,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 AS avg_rows_read
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND metadata->>'stmtType' = 'TypeSelect'
ORDER BY avg_rows_read DESC
LIMIT 20;
```

**Common statement types:**
- `TypeSelect`: Read queries
- `TypeInsert`: Inserts
- `TypeUpdate`: Updates
- `TypeDelete`: Deletes
- `TypeDDL`: Schema changes

### By Full Scan Flag

Find queries lacking proper indexes:

```sql
SELECT
  fingerprint_id,
  metadata->>'db' AS database,
  substring(metadata->>'query', 1, 150) AS query,
  (metadata->>'fullScan')::BOOL AS full_scan,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat_sec,
  (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 AS avg_rows_read,
  metadata->'index_recommendations' AS recommendations
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (metadata->>'fullScan')::BOOL = true
ORDER BY executions DESC
LIMIT 30;
```

### By Distributed Flag

Identify distributed query overhead:

```sql
SELECT
  fingerprint_id,
  (metadata->>'distSQL')::BOOL AS distributed,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat_sec,
  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576
    ELSE NULL
  END AS avg_network_mb
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (metadata->>'distSQL')::BOOL = true
ORDER BY avg_network_mb DESC NULLS LAST
LIMIT 20;
```

## Aggregation Queries

### Top N by Metric

Identify worst performers across multiple dimensions:

```sql
-- Top 10 by total CPU consumption
SELECT
  fingerprint_id,
  substring(metadata->>'query', 1, 100) AS query_preview,
  (statistics->'execution_statistics'->>'cnt')::INT AS sample_size,
  ROUND(
    ((statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9) *
    (statistics->'statistics'->>'cnt')::INT,
    2
  ) AS estimated_total_cpu_sec
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
ORDER BY estimated_total_cpu_sec DESC
LIMIT 10;
```

### Group by Application

Application-level resource attribution:

```sql
SELECT
  metadata->>'app' AS application,
  COUNT(DISTINCT fingerprint_id) AS unique_queries,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  ROUND(AVG((statistics->'statistics'->'runLat'->>'mean')::FLOAT8), 3) AS avg_latency_sec,
  SUM(COALESCE((statistics->'statistics'->>'failureCount')::INT, 0)) AS total_failures,
  ROUND(
    SUM(COALESCE((statistics->'statistics'->>'failureCount')::INT, 0))::NUMERIC /
    NULLIF(SUM((statistics->'statistics'->>'cnt')::INT), 0) * 100,
    2
  ) AS failure_rate_pct
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY metadata->>'app'
ORDER BY total_executions DESC;
```

**Use case:** Application performance scorecard, SLA monitoring

### Group by Database

Database-level resource consumption:

```sql
SELECT
  metadata->>'db' AS database,
  COUNT(DISTINCT fingerprint_id) AS unique_queries,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  ROUND(
    SUM(
      (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 *
      (statistics->'statistics'->>'cnt')::INT
    ),
    2
  ) AS total_runtime_sec,
  COUNT(CASE WHEN (metadata->>'fullScan')::BOOL = true THEN 1 END) AS full_scan_queries
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY metadata->>'db'
ORDER BY total_runtime_sec DESC;
```

### Group by Statement Type

Workload composition analysis:

```sql
SELECT
  metadata->>'stmtType' AS statement_type,
  COUNT(DISTINCT fingerprint_id) AS unique_patterns,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  ROUND(AVG((statistics->'statistics'->'runLat'->>'mean')::FLOAT8), 4) AS avg_latency_sec,
  ROUND(AVG((statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8), 2) AS avg_rows_read
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY metadata->>'stmtType'
ORDER BY total_executions DESC;
```

## Percentile Calculations

### Latency Percentiles (Approximate)

Use bucket aggregation for percentile approximation:

```sql
WITH latency_buckets AS (
  SELECT
    fingerprint_id,
    (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat,
    (statistics->'statistics'->>'cnt')::INT AS executions
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > now() - INTERVAL '24 hours'
),
percentiles AS (
  SELECT
    percentile_cont(0.50) WITHIN GROUP (ORDER BY mean_lat) AS p50,
    percentile_cont(0.90) WITHIN GROUP (ORDER BY mean_lat) AS p90,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY mean_lat) AS p95,
    percentile_cont(0.99) WITHIN GROUP (ORDER BY mean_lat) AS p99
  FROM latency_buckets
)
SELECT * FROM percentiles;
```

**Note:** This approximates percentiles across fingerprints, not individual executions.

### Per-Application Percentiles

```sql
SELECT
  metadata->>'app' AS application,
  percentile_cont(0.50) WITHIN GROUP (ORDER BY (statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS p50_latency,
  percentile_cont(0.95) WITHIN GROUP (ORDER BY (statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS p95_latency,
  percentile_cont(0.99) WITHIN GROUP (ORDER BY (statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS p99_latency
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY metadata->>'app'
ORDER BY p99_latency DESC;
```

## Trend Analysis

### Compare Time Buckets

Detect latency regressions hour-over-hour:

```sql
WITH hourly_stats AS (
  SELECT
    fingerprint_id,
    aggregated_ts,
    (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat,
    (statistics->'statistics'->>'cnt')::INT AS executions
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > now() - INTERVAL '24 hours'
),
current_hour AS (
  SELECT fingerprint_id, mean_lat AS current_lat
  FROM hourly_stats
  WHERE aggregated_ts > now() - INTERVAL '1 hour'
),
previous_hour AS (
  SELECT fingerprint_id, mean_lat AS previous_lat
  FROM hourly_stats
  WHERE aggregated_ts BETWEEN now() - INTERVAL '2 hours' AND now() - INTERVAL '1 hour'
)
SELECT
  c.fingerprint_id,
  c.current_lat,
  p.previous_lat,
  ROUND((c.current_lat - p.previous_lat) / NULLIF(p.previous_lat, 0) * 100, 2) AS pct_change
FROM current_hour c
JOIN previous_hour p USING (fingerprint_id)
WHERE ABS((c.current_lat - p.previous_lat) / NULLIF(p.previous_lat, 0)) > 0.5  -- >50% change
ORDER BY pct_change DESC;
```

**Use case:** Regression detection, deployment impact analysis

### Day-over-Day Comparison

Compare today's performance to yesterday:

```sql
WITH today AS (
  SELECT
    fingerprint_id,
    AVG((statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS avg_lat_today,
    SUM((statistics->'statistics'->>'cnt')::INT) AS executions_today
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > CURRENT_DATE
  GROUP BY fingerprint_id
),
yesterday AS (
  SELECT
    fingerprint_id,
    AVG((statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS avg_lat_yesterday,
    SUM((statistics->'statistics'->>'cnt')::INT) AS executions_yesterday
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts BETWEEN CURRENT_DATE - INTERVAL '1 day' AND CURRENT_DATE
  GROUP BY fingerprint_id
)
SELECT
  t.fingerprint_id,
  t.avg_lat_today,
  y.avg_lat_yesterday,
  ROUND((t.avg_lat_today - y.avg_lat_yesterday) / NULLIF(y.avg_lat_yesterday, 0) * 100, 2) AS latency_change_pct,
  t.executions_today,
  y.executions_yesterday
FROM today t
JOIN yesterday y USING (fingerprint_id)
WHERE t.executions_today > 100  -- Filter low-volume queries
ORDER BY latency_change_pct DESC
LIMIT 20;
```

### Identify New Query Patterns

Find queries that appeared recently:

```sql
WITH recent AS (
  SELECT DISTINCT fingerprint_id
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > now() - INTERVAL '1 hour'
),
historical AS (
  SELECT DISTINCT fingerprint_id
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts BETWEEN now() - INTERVAL '25 hours' AND now() - INTERVAL '1 hour'
)
SELECT
  s.fingerprint_id,
  s.metadata->>'db' AS database,
  s.metadata->>'app' AS application,
  s.metadata->>'query' AS query,
  (s.statistics->'statistics'->>'cnt')::INT AS recent_executions
FROM crdb_internal.statement_statistics s
WHERE s.fingerprint_id IN (SELECT fingerprint_id FROM recent)
  AND s.fingerprint_id NOT IN (SELECT fingerprint_id FROM historical)
  AND s.aggregated_ts > now() - INTERVAL '1 hour'
ORDER BY recent_executions DESC;
```

**Use case:** Deployment validation, new feature monitoring

## Join Patterns

### Correlate Fingerprint Across Multiple Buckets

Track single fingerprint performance over time:

```sql
SELECT
  aggregated_ts,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat_sec,
  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9
    ELSE NULL
  END AS mean_cpu_sec,
  metadata->>'query' AS query
FROM crdb_internal.statement_statistics
WHERE fingerprint_id = '<specific_fingerprint_id>'
  AND aggregated_ts > now() - INTERVAL '7 days'
ORDER BY aggregated_ts;
```

**Use case:** Diagnose specific query performance trends

### Join with Current Cluster State

Correlate historical patterns with live activity:

```sql
-- Find fingerprints both historically slow AND currently running
WITH slow_historical AS (
  SELECT DISTINCT fingerprint_id
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > now() - INTERVAL '24 hours'
    AND (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 > 5.0
),
current_statements AS (SHOW CLUSTER STATEMENTS)
SELECT
  c.query_id,
  c.query AS current_query,
  c.start,
  now() - c.start AS current_runtime,
  s.metadata->>'app' AS historical_app,
  (s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS historical_avg_lat
FROM current_statements c
JOIN crdb_internal.statement_statistics s
  ON encode(digest(c.query, 'sha256'), 'hex') = s.fingerprint_id  -- Approximate join
WHERE s.fingerprint_id IN (SELECT fingerprint_id FROM slow_historical)
  AND s.aggregated_ts > now() - INTERVAL '24 hours'
ORDER BY current_runtime DESC;
```

**Note:** Fingerprint ID calculation may vary; use for correlation, not exact matching.

## Advanced Analysis

### Latency Decomposition

Break down where time is spent:

```sql
SELECT
  fingerprint_id,
  substring(metadata->>'query', 1, 100) AS query_preview,
  (statistics->'statistics'->'parseLat'->>'mean')::FLOAT8 AS parse_sec,
  (statistics->'statistics'->'planLat'->>'mean')::FLOAT8 AS plan_sec,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS run_sec,
  (statistics->'statistics'->'serviceLat'->>'mean')::FLOAT8 AS total_service_sec,
  ROUND(
    (statistics->'statistics'->'parseLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'serviceLat'->>'mean')::FLOAT8, 0) * 100,
    2
  ) AS parse_pct,
  ROUND(
    (statistics->'statistics'->'planLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'serviceLat'->>'mean')::FLOAT8, 0) * 100,
    2
  ) AS plan_pct,
  ROUND(
    (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'serviceLat'->>'mean')::FLOAT8, 0) * 100,
    2
  ) AS run_pct
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'serviceLat'->>'mean')::FLOAT8 > 1.0
ORDER BY total_service_sec DESC
LIMIT 20;
```

**Use case:** Optimize specific latency components (e.g., high planning time → update statistics)

### Resource Attribution

Estimate cluster-wide resource consumption by application:

```sql
SELECT
  metadata->>'app' AS application,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,

  -- Estimated total CPU seconds
  ROUND(
    SUM(
      CASE
        WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
        THEN ((statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9) *
             (statistics->'statistics'->>'cnt')::INT
        ELSE 0
      END
    ),
    2
  ) AS estimated_cpu_sec,

  -- Total runtime (all queries)
  ROUND(
    SUM(
      (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 *
      (statistics->'statistics'->>'cnt')::INT
    ),
    2
  ) AS total_runtime_sec,

  -- Total rows read
  ROUND(
    SUM(
      (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 *
      (statistics->'statistics'->>'cnt')::INT
    ),
    0
  ) AS total_rows_read,

  -- Total failures
  SUM(COALESCE((statistics->'statistics'->>'failureCount')::INT, 0)) AS total_failures

FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY metadata->>'app'
ORDER BY estimated_cpu_sec DESC;
```

**Use case:** Chargeback, capacity planning, application SLA tracking

### Index Recommendation Summary

Aggregate all index recommendations:

```sql
WITH recommendations AS (
  SELECT
    fingerprint_id,
    metadata->>'db' AS database,
    metadata->>'query' AS query,
    jsonb_array_elements(metadata->'index_recommendations') AS recommendation
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > now() - INTERVAL '7 days'
    AND metadata->'index_recommendations' IS NOT NULL
    AND jsonb_array_length(metadata->'index_recommendations') > 0
)
SELECT
  database,
  recommendation->>'SQL' AS create_index_statement,
  COUNT(*) AS num_queries_affected,
  array_agg(DISTINCT fingerprint_id) AS affected_fingerprints
FROM recommendations
GROUP BY database, recommendation->>'SQL'
ORDER BY num_queries_affected DESC;
```

**Use case:** Prioritize index creation by impact (number of queries improved)

## Batch Operations

### Generate Performance Report

Comprehensive daily performance summary:

```sql
-- Executive summary: top slow queries, top CPU consumers, error-prone queries
WITH slow_queries AS (
  SELECT fingerprint_id, metadata->>'query' AS query,
         (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > CURRENT_DATE
  ORDER BY mean_lat DESC LIMIT 5
),
cpu_intensive AS (
  SELECT fingerprint_id, metadata->>'query' AS query,
         (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9 AS mean_cpu
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > CURRENT_DATE
    AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  ORDER BY mean_cpu DESC LIMIT 5
),
error_prone AS (
  SELECT fingerprint_id, metadata->>'query' AS query,
         COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) AS failures
  FROM crdb_internal.statement_statistics
  WHERE aggregated_ts > CURRENT_DATE
  ORDER BY failures DESC LIMIT 5
)
SELECT 'Top Slow Queries' AS category, * FROM slow_queries
UNION ALL
SELECT 'Top CPU Consumers', * FROM cpu_intensive
UNION ALL
SELECT 'Error-Prone Queries', * FROM error_prone;
```

### Export for External Analysis

Format data for CSV export or BI tools:

```sql
SELECT
  fingerprint_id,
  aggregated_ts AT TIME ZONE 'UTC' AS timestamp_utc,
  metadata->>'db' AS database,
  metadata->>'app' AS application,
  metadata->>'stmtType' AS statement_type,
  (metadata->>'fullScan')::BOOL AS full_scan,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_latency_sec,
  (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 AS avg_rows_read,
  COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) AS failures
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '7 days'
ORDER BY aggregated_ts, fingerprint_id;
```

**Use case:** Data warehouse ingestion, Tableau/Looker dashboards

## Additional Resources

- **JSON field details:** [json-field-reference.md](json-field-reference.md)
- **Metric interpretation:** [metrics-and-units.md](metrics-and-units.md)
- **Main skill:** [../SKILL.md](../SKILL.md)

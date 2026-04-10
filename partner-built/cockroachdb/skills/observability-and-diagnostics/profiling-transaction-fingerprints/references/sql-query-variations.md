# SQL Query Variations

Extended query library for transaction fingerprint analysis with time window variations, filtering patterns, and transaction-specific analysis techniques.

## Time Window Variations

### 1-Hour Window

**Use case:** Real-time investigation of recent patterns

```sql
-- Recent high-retry transactions (last hour)
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '1 hour'
  AND (statistics->'statistics'->>'maxRetries')::INT > 5
ORDER BY max_retries DESC
LIMIT 20;
```

### 6-Hour Window

**Use case:** Identify patterns during business hours or specific shifts

```sql
-- Commit latency analysis (last 6 hours)
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'db' AS database,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_sec,
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct,
  aggregated_ts
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '6 hours'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0.05
ORDER BY mean_commit_lat_sec DESC
LIMIT 20;
```

### 24-Hour Window (Default Recommended)

**Use case:** Standard daily performance analysis

```sql
-- Resource consumption analysis (last 24 hours)
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 AS mean_network_mb,
  (statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576 AS mean_mem_mb,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  ROUND(
    ((statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576) *
    (statistics->'statistics'->>'cnt')::INT, 2
  ) AS estimated_total_network_mb
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
ORDER BY estimated_total_network_mb DESC
LIMIT 20;
```

### 7-Day Window (Trend Analysis)

**Use case:** Weekly trends, performance regression detection

```sql
-- Retry trend analysis (last 7 days)
SELECT
  date_trunc('day', aggregated_ts) AS day,
  metadata->>'app' AS application,
  COUNT(DISTINCT encode(fingerprint_id, 'hex')) AS unique_txn_fingerprints,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  MAX((statistics->'statistics'->>'maxRetries')::INT) AS peak_max_retries
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '7 days'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
GROUP BY day, application
ORDER BY day DESC, avg_max_retries DESC;
```

## Filtering Patterns

### Filter by Application

```sql
-- Transactions from specific application
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_sec,
  aggregated_ts
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND metadata->>'app' = 'payments-api'
ORDER BY max_retries DESC
LIMIT 20;
```

### Filter by Database

```sql
-- Transactions in specific database
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND metadata->>'db' = 'production'
  AND (statistics->'statistics'->>'maxRetries')::INT > 10
ORDER BY max_retries DESC
LIMIT 20;
```

### Filter by Retry Threshold

```sql
-- Only high-retry transactions (>20 retries)
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  metadata->>'db' AS database,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_sec,
  (statistics->'statistics'->>'cnt')::INT AS executions
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 20
ORDER BY max_retries DESC;
```

### Filter by Commit Latency Threshold

```sql
-- Only slow-commit transactions (>100ms)
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_sec,
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct,
  (statistics->'statistics'->>'cnt')::INT AS executions
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0.1
ORDER BY mean_commit_lat_sec DESC
LIMIT 20;
```

### Filter by Implicit vs Explicit Transactions

```sql
-- Compare implicit (single-statement) vs explicit (multi-statement) transactions
SELECT
  (metadata->>'implicitTxn')::BOOL AS is_implicit,
  COUNT(*) AS fingerprint_count,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  AVG((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS avg_commit_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY is_implicit
ORDER BY is_implicit;
```

## Aggregation Queries

### Top N by Max Retries

```sql
-- Top 10 transactions by max retries
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  metadata->>'db' AS database,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
ORDER BY max_retries DESC
LIMIT 10;
```

### Group by Application

```sql
-- Application-level retry metrics
SELECT
  metadata->>'app' AS application,
  COUNT(DISTINCT encode(fingerprint_id, 'hex')) AS unique_txn_fingerprints,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  MAX((statistics->'statistics'->>'maxRetries')::INT) AS peak_max_retries,
  AVG((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8) AS avg_retry_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
GROUP BY application
ORDER BY avg_max_retries DESC;
```

### Group by Database

```sql
-- Database-level commit latency analysis
SELECT
  metadata->>'db' AS database,
  COUNT(*) AS transaction_fingerprint_count,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS avg_commit_lat_sec,
  MAX((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS max_commit_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0
GROUP BY database
ORDER BY avg_commit_lat_sec DESC;
```

### Time Bucket Trends

```sql
-- Hourly retry trend
SELECT
  aggregated_ts,
  COUNT(*) AS transaction_fingerprint_count,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  AVG((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8) AS avg_retry_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
GROUP BY aggregated_ts
ORDER BY aggregated_ts DESC;
```

## Transaction-to-Statement Join Patterns

**CRITICAL UNIQUE SECTION:** These patterns are specific to transaction fingerprint analysis and enable drill-down from transactions to constituent statements.

### Basic Join: Transaction to Statements

```sql
-- Join transaction fingerprints with statement fingerprints
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  t.metadata->>'app' AS txn_app,
  (t.statistics->'statistics'->>'maxRetries')::INT AS txn_max_retries,
  stmt_fp_id AS stmt_fingerprint_id_hex,
  s.metadata->>'query' AS statement_query,
  (s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS stmt_mean_run_lat_sec,
  (s.statistics->'statistics'->>'cnt')::INT AS stmt_executions
FROM crdb_internal.transaction_statistics t
CROSS JOIN LATERAL jsonb_array_elements_text(t.metadata->'stmtFingerprintIDs') AS stmt_fp_id
LEFT JOIN crdb_internal.statement_statistics s
  ON s.fingerprint_id = decode(stmt_fp_id, 'hex')
  AND s.aggregated_ts = t.aggregated_ts
WHERE t.aggregated_ts > now() - INTERVAL '24 hours'
  AND t.metadata->'stmtFingerprintIDs' IS NOT NULL
ORDER BY txn_max_retries DESC
LIMIT 50;
```

**Key technique:**
- `jsonb_array_elements_text()` expands stmtFingerprintIDs array to rows
- `decode(stmt_fp_id, 'hex')` converts hex string back to binary for join
- Match on same `aggregated_ts` bucket

### Aggregate Statement Metrics Within Transaction

```sql
-- Aggregate statement metrics for each transaction
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  t.metadata->>'app' AS application,
  (t.statistics->'statistics'->>'maxRetries')::INT AS txn_max_retries,
  jsonb_array_length(t.metadata->'stmtFingerprintIDs') AS num_statements,
  AVG((s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS avg_stmt_run_lat_sec,
  MAX((s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS max_stmt_run_lat_sec,
  SUM((s.statistics->'statistics'->>'cnt')::INT) AS total_stmt_executions
FROM crdb_internal.transaction_statistics t
CROSS JOIN LATERAL jsonb_array_elements_text(t.metadata->'stmtFingerprintIDs') AS stmt_fp_id
LEFT JOIN crdb_internal.statement_statistics s
  ON s.fingerprint_id = decode(stmt_fp_id, 'hex')
  AND s.aggregated_ts = t.aggregated_ts
WHERE t.aggregated_ts > now() - INTERVAL '24 hours'
  AND t.metadata->'stmtFingerprintIDs' IS NOT NULL
  AND (t.statistics->'statistics'->>'maxRetries')::INT > 10
GROUP BY t.fingerprint_id, application, txn_max_retries, num_statements
ORDER BY txn_max_retries DESC
LIMIT 20;
```

### Find All Statements in High-Retry Transactions

```sql
-- Identify all statements contributing to high-retry transactions
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  (t.statistics->'statistics'->>'maxRetries')::INT AS txn_max_retries,
  substring(s.metadata->>'query', 1, 150) AS statement_query_preview,
  (s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS stmt_mean_run_lat_sec,
  (s.statistics->'statistics'->>'maxRetries')::INT AS stmt_max_retries,
  (s.statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9 AS stmt_mean_contention_sec
FROM crdb_internal.transaction_statistics t
CROSS JOIN LATERAL jsonb_array_elements_text(t.metadata->'stmtFingerprintIDs') AS stmt_fp_id
LEFT JOIN crdb_internal.statement_statistics s
  ON s.fingerprint_id = decode(stmt_fp_id, 'hex')
  AND s.aggregated_ts = t.aggregated_ts
WHERE t.aggregated_ts > now() - INTERVAL '24 hours'
  AND (t.statistics->'statistics'->>'maxRetries')::INT > 20
  AND t.metadata->'stmtFingerprintIDs' IS NOT NULL
  AND (s.statistics->'execution_statistics'->>'cnt') IS NOT NULL
ORDER BY txn_max_retries DESC, stmt_mean_contention_sec DESC
LIMIT 100;
```

### Statement Composition Complexity Analysis

```sql
-- Analyze transaction complexity by statement count and types
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  t.metadata->>'app' AS application,
  (t.statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  jsonb_array_length(t.metadata->'stmtFingerprintIDs') AS num_statements,
  COUNT(DISTINCT s.metadata->>'stmtType') AS distinct_stmt_types,
  array_agg(DISTINCT s.metadata->>'stmtType') AS stmt_types,
  AVG((s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8) AS avg_stmt_latency
FROM crdb_internal.transaction_statistics t
CROSS JOIN LATERAL jsonb_array_elements_text(t.metadata->'stmtFingerprintIDs') AS stmt_fp_id
LEFT JOIN crdb_internal.statement_statistics s
  ON s.fingerprint_id = decode(stmt_fp_id, 'hex')
  AND s.aggregated_ts = t.aggregated_ts
WHERE t.aggregated_ts > now() - INTERVAL '24 hours'
  AND t.metadata->'stmtFingerprintIDs' IS NOT NULL
GROUP BY t.fingerprint_id, application, max_retries, num_statements
HAVING jsonb_array_length(t.metadata->'stmtFingerprintIDs') > 5
ORDER BY max_retries DESC
LIMIT 20;
```

## Retry Analysis Patterns

### Retry Rate by Application

```sql
-- Application retry scorecard
SELECT
  metadata->>'app' AS application,
  COUNT(*) AS transaction_fingerprints,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  MAX((statistics->'statistics'->>'maxRetries')::INT) AS peak_max_retries,
  AVG((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8) AS avg_retry_lat_sec,
  AVG(
    ROUND(
      ((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 /
      NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
    )
  ) AS avg_retry_pct_of_service_lat
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
GROUP BY application
ORDER BY avg_max_retries DESC;
```

### Retry Latency Decomposition

```sql
-- Understand retry impact on total latency
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS total_service_lat_sec,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS retry_lat_sec,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS commit_lat_sec,
  (
    (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 -
    COALESCE((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8, 0) -
    COALESCE((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8, 0)
  ) AS estimated_execution_lat_sec,
  ROUND(
    (COALESCE((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8, 0) /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS retry_pct,
  ROUND(
    (COALESCE((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8, 0) /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 10
ORDER BY retry_pct DESC
LIMIT 20;
```

### Retry Trend Over Time

```sql
-- Hourly retry pattern
SELECT
  aggregated_ts,
  metadata->>'app' AS application,
  COUNT(*) AS transaction_fingerprints,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  MAX((statistics->'statistics'->>'maxRetries')::INT) AS peak_max_retries
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
GROUP BY aggregated_ts, application
ORDER BY aggregated_ts DESC, avg_max_retries DESC;
```

### Retry Storm Detection

```sql
-- Detect sudden retry spikes (compare to previous period)
WITH current_period AS (
  SELECT
    metadata->>'app' AS application,
    AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_retries
  FROM crdb_internal.transaction_statistics
  WHERE aggregated_ts > now() - INTERVAL '1 hour'
  GROUP BY application
),
previous_period AS (
  SELECT
    metadata->>'app' AS application,
    AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_retries
  FROM crdb_internal.transaction_statistics
  WHERE aggregated_ts > now() - INTERVAL '2 hours'
    AND aggregated_ts <= now() - INTERVAL '1 hour'
  GROUP BY application
)
SELECT
  c.application,
  c.avg_retries AS current_avg_retries,
  p.avg_retries AS previous_avg_retries,
  ROUND(
    ((c.avg_retries - p.avg_retries) / NULLIF(p.avg_retries, 0)) * 100, 2
  ) AS retry_increase_pct
FROM current_period c
LEFT JOIN previous_period p ON c.application = p.application
WHERE c.avg_retries > p.avg_retries * 2  -- 2x increase threshold
ORDER BY retry_increase_pct DESC;
```

## Commit Latency Analysis

### Commit Latency Percentiles (Approximation)

```sql
-- High commit latency transactions with standard deviation
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_sec,
  sqrt(
    (statistics->'statistics'->'commitLat'->>'sqDiff')::FLOAT8 /
    NULLIF((statistics->'statistics'->>'cnt')::INT, 0)
  ) AS stddev_commit_lat_sec,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0.05
ORDER BY mean_commit_lat_sec DESC
LIMIT 20;
```

### Commit vs Service Latency Ratio

```sql
-- Transactions with high commit overhead
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  metadata->>'db' AS database,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS commit_lat_sec,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS service_lat_sec,
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct_of_service_lat
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0
HAVING commit_pct_of_service_lat > 20
ORDER BY commit_pct_of_service_lat DESC
LIMIT 20;
```

### Time-of-Day Commit Latency Pattern

```sql
-- Commit latency by hour of day
SELECT
  EXTRACT(HOUR FROM aggregated_ts) AS hour_of_day,
  COUNT(*) AS transaction_fingerprints,
  AVG((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS avg_commit_lat_sec,
  MAX((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS max_commit_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '7 days'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0
GROUP BY hour_of_day
ORDER BY hour_of_day;
```

## Advanced Analysis

### Transaction Complexity (Statement Count)

```sql
-- Analyze transaction complexity by statement count
SELECT
  jsonb_array_length(metadata->'stmtFingerprintIDs') AS num_statements,
  COUNT(*) AS transaction_fingerprints,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  AVG((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS avg_commit_lat_sec,
  AVG((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8) AS avg_service_lat_sec
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND metadata->'stmtFingerprintIDs' IS NOT NULL
GROUP BY num_statements
ORDER BY num_statements DESC;
```

### Resource Attribution by Application

```sql
-- Application-level resource consumption scorecard
SELECT
  metadata->>'app' AS application,
  COUNT(*) AS transaction_fingerprints,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576) AS avg_network_mb,
  AVG((statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576) AS avg_mem_mb,
  SUM(
    ROUND(
      ((statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576) *
      (statistics->'statistics'->>'cnt')::INT, 2
    )
  ) AS total_network_mb
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
GROUP BY application
ORDER BY total_network_mb DESC;
```

### Cross-Region Transaction Detection

```sql
-- Identify likely cross-region transactions (high network + commit latency)
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 AS mean_network_mb,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_sec,
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 > 10
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0.05
ORDER BY mean_network_mb DESC
LIMIT 20;
```

### Transaction Health Scorecard

```sql
-- Comprehensive transaction health metrics by application
SELECT
  metadata->>'app' AS application,
  COUNT(*) AS transaction_fingerprints,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  AVG((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8) AS avg_retry_lat_sec,
  AVG((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS avg_commit_lat_sec,
  AVG((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8) AS avg_service_lat_sec,
  AVG(
    ROUND(
      ((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 /
      NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
    )
  ) AS avg_retry_pct,
  AVG(
    ROUND(
      ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
      NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
    )
  ) AS avg_commit_pct
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY application
ORDER BY avg_max_retries DESC;
```

## Additional Resources

- **JSON schema:** [json-field-reference.md](json-field-reference.md)
- **Metrics interpretation:** [metrics-and-units.md](metrics-and-units.md)
- **Main skill:** [../SKILL.md](../SKILL.md)
- **Official docs:** [Transactions Page](https://www.cockroachlabs.com/docs/stable/ui-transactions-page.html)

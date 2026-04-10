# Metrics and Units Reference

Comprehensive guide to interpreting statement statistics metrics, units, conversions, and thresholds for performance analysis.

## Metric Categories

Statement statistics are divided into two collection modes:

| Category | Collection Method | Coverage | Overhead | Use Case |
|----------|------------------|----------|----------|----------|
| **Aggregated** | Always collected | 100% of executions | Low | Latency, counts, rows/bytes |
| **Sampled** | Probabilistic (~10%) | Representative sample | Medium | CPU, memory, contention |

## Latency Metrics

All latency metrics are stored in **seconds** as FLOAT8.

### runLat (Runtime Latency)

**Definition:** Time spent executing the query (excludes parsing and planning).

**Extraction:**
```sql
(statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_run_lat_seconds
```

**Thresholds:**

| Latency | Classification | Action |
|---------|---------------|---------|
| < 0.01s (10ms) | Fast | Acceptable for OLTP |
| 0.01s - 0.1s | Moderate | Investigate if high-frequency |
| 0.1s - 1s | Slow | Optimize if possible |
| 1s - 5s | Very slow | High priority optimization |
| > 5s | Critical | Immediate investigation |

**Interpretation:**
- **OLTP workloads:** Target < 50ms (0.05s) for user-facing queries
- **Batch/reporting:** Up to 60s acceptable for complex aggregations
- **Compare max vs mean:** High variance indicates inconsistent performance

**Example analysis:**
```sql
SELECT
  fingerprint_id,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_sec,
  sqrt(
    (statistics->'statistics'->'runLat'->>'sqDiff')::FLOAT8 /
    NULLIF((statistics->'statistics'->>'cnt')::INT, 0)
  ) AS stddev_sec,
  CASE
    WHEN (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 < 0.01 THEN 'fast'
    WHEN (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 < 0.1 THEN 'moderate'
    WHEN (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 < 1 THEN 'slow'
    ELSE 'critical'
  END AS latency_class
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours';
```

### parseLat (Parse Latency)

**Definition:** Time spent parsing SQL text into an abstract syntax tree (AST).

**Typical values:**
- Simple queries: < 0.001s (1ms)
- Complex queries: 0.001s - 0.01s (1-10ms)

**High parse latency causes:**
- Extremely long SQL strings
- Complex nested subqueries
- Many columns/tables in query

**Optimization:** Use prepared statements to parse once and execute many times.

### planLat (Plan Latency)

**Definition:** Time spent by query optimizer generating execution plan.

**Typical values:**
- Simple queries: < 0.01s (10ms)
- Medium complexity: 0.01s - 0.1s (10-100ms)
- Very complex: > 0.1s

**High planning latency causes:**
- Large number of tables in JOIN
- Complex expressions/functions
- Missing or stale table statistics
- Many columns in SELECT/WHERE

**Optimization:**
- Update table statistics: `ANALYZE table_name`
- Simplify query structure
- Use views for repeated complex logic

### serviceLat (Service Latency)

**Definition:** Total end-to-end latency (parseLat + planLat + runLat).

**Formula:**
```
serviceLat ≈ parseLat + planLat + runLat + (network overhead)
```

**Use for:** Understanding total user-perceived latency.

## Contention Metrics

### contentionTime

**Definition:** Time spent waiting for locks held by other transactions.

**Unit:** Nanoseconds (convert to seconds: divide by 1e9)

**Extraction:**
```sql
(statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9 AS mean_contention_sec
```

**Sampled:** Yes (check for `execution_statistics.cnt`)

**Thresholds:**

| Contention % of Runtime | Severity | Action |
|------------------------|----------|---------|
| < 5% | Low | Normal transactional overhead |
| 5% - 20% | Moderate | Monitor and investigate patterns |
| 20% - 50% | High | Batch operations, optimize transaction boundaries |
| > 50% | Critical | Schema redesign, partition hot tables |

**Calculate contention ratio:**
```sql
SELECT
  fingerprint_id,
  ROUND(
    ((statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9) /
    NULLIF((statistics->'statistics'->'runLat'->>'mean')::FLOAT8, 0) * 100,
    2
  ) AS contention_pct_of_runtime
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 > 0
ORDER BY contention_pct_of_runtime DESC;
```

**Common causes:**
- UPDATE/DELETE on same hot rows
- Serial writes to monotonically increasing keys (timestamps, auto-increment)
- Long-running transactions holding locks
- Insufficient transaction batching

## CPU Metrics

### cpuSQLNanos

**Definition:** CPU time consumed by SQL execution layer (excludes storage/network).

**Unit:** Nanoseconds (convert to seconds: divide by 1e9)

**Extraction:**
```sql
(statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9 AS mean_cpu_sec
```

**Sampled:** Yes

**Thresholds:**

| Mean CPU Time | Classification | Action |
|---------------|---------------|---------|
| < 0.01s (10ms) | Low | Efficient query |
| 0.01s - 0.1s | Moderate | Acceptable for complex queries |
| 0.1s - 1s | High | Consider optimization |
| > 1s | Very high | Index missing or inefficient algorithm |

**Estimated total CPU impact:**
```sql
SELECT
  fingerprint_id,
  (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9 AS mean_cpu_sec,
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  ROUND(
    ((statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9) *
    (statistics->'statistics'->>'cnt')::INT,
    2
  ) AS estimated_total_cpu_sec
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
ORDER BY estimated_total_cpu_sec DESC;
```

**Optimization targets:**
- High mean CPU: Inefficient query logic, missing indexes
- High total CPU: Frequent execution of moderately expensive queries (optimize for batch, cache results)

## Admission Control Metrics

### admissionWaitTime

**Definition:** Time spent queued in admission control before execution starts.

**Unit:** Nanoseconds (convert to seconds: divide by 1e9)

**Extraction:**
```sql
(statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 / 1e9 AS mean_admission_wait_sec
```

**Sampled:** Yes

**Thresholds:**

| Wait Time | Cluster State | Action |
|-----------|--------------|---------|
| 0s | Healthy | Sufficient capacity |
| < 1s | Minor queueing | Monitor during peak hours |
| 1s - 10s | Moderate saturation | Consider scaling or optimization |
| > 10s | Severe saturation | Immediate capacity increase or workload reduction |

**Admission wait ratio:**
```sql
SELECT
  fingerprint_id,
  (statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 / 1e9 AS wait_sec,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS run_sec,
  ROUND(
    ((statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 / 1e9) /
    NULLIF((statistics->'statistics'->'runLat'->>'mean')::FLOAT8, 0),
    2
  ) AS wait_to_run_ratio
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 > 0
ORDER BY wait_to_run_ratio DESC;
```

**Interpretation:**
- **Ratio < 0.1:** Minimal impact
- **Ratio 0.1 - 1.0:** Moderate queueing
- **Ratio > 1.0:** Wait time exceeds execution time (critical)

**Root causes:**
- CPU saturation (most common)
- Memory pressure
- I/O bandwidth limits
- High concurrent query load

## Read Metrics

### rowsRead

**Definition:** Number of rows scanned from storage layer (including rows filtered out).

**Unit:** Count (FLOAT8 for mean)

**Extraction:**
```sql
(statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 AS mean_rows_read
```

**Aggregated:** Yes (all executions)

**Thresholds:**

| Rows Read | Query Type | Consideration |
|-----------|-----------|---------------|
| < 100 | Point lookup/small scan | Optimal |
| 100 - 10,000 | Range scan | Acceptable if indexed |
| 10,000 - 1M | Large scan | Check for index usage |
| > 1M | Full table scan | High priority optimization |

**Read amplification analysis:**
```sql
SELECT
  fingerprint_id,
  (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 AS rows_read,
  (statistics->'statistics'->'rowsWritten'->>'mean')::FLOAT8 AS rows_written,
  CASE
    WHEN (statistics->'statistics'->'rowsWritten'->>'mean')::FLOAT8 > 0
    THEN (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 /
         NULLIF((statistics->'statistics'->'rowsWritten'->>'mean')::FLOAT8, 0)
    ELSE NULL
  END AS read_amplification_ratio,
  (metadata->>'fullScan')::BOOL AS full_scan
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND metadata->>'stmtType' IN ('TypeUpdate', 'TypeDelete')
ORDER BY rows_read DESC;
```

**High read amplification causes:**
- Missing WHERE clause indexes
- Secondary index lookups
- Full table scans for small updates

### bytesRead

**Definition:** Total bytes read from storage (including index and table data).

**Unit:** Bytes

**Conversion to MB:**
```sql
(statistics->'statistics'->'bytesRead'->>'mean')::FLOAT8 / 1048576 AS mean_bytes_read_mb
```

**Thresholds:**
- < 1 MB: Small query
- 1 MB - 100 MB: Medium scan
- 100 MB - 1 GB: Large scan
- \> 1 GB: Very large scan (consider pagination, incremental processing)

## Memory and Disk Metrics

### maxMemUsage

**Definition:** Maximum memory allocated during query execution (including working memory).

**Unit:** Bytes (convert to MB: divide by 1048576)

**Extraction:**
```sql
(statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576 AS mean_mem_mb,
(statistics->'execution_statistics'->'maxMemUsage'->>'max')::FLOAT8 / 1048576 AS max_mem_mb
```

**Sampled:** Yes

**Thresholds:**

| Memory Usage | Classification | Action |
|--------------|---------------|---------|
| < 10 MB | Low | Normal |
| 10 MB - 100 MB | Moderate | Monitor for aggregations/sorts |
| 100 MB - 512 MB | High | Check for large result sets |
| > 512 MB | Very high | Risk of spilling to disk |

**Default workmem limit:** Check `sql.distsql.temp_storage.workmem` setting (often 64 MB).

### maxDiskUsage

**Definition:** Maximum disk space used for temporary storage (memory spill).

**Unit:** Bytes (convert to MB: divide by 1048576)

**Extraction:**
```sql
(statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1048576 AS mean_disk_mb
```

**Sampled:** Yes

**Interpretation:**
- **> 0:** Query exceeded workmem and spilled to disk (performance degradation ~100-1000x)
- **Large values:** Significant I/O overhead

**Spill analysis:**
```sql
SELECT
  fingerprint_id,
  metadata->>'stmtType' AS stmt_type,
  (statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576 AS mean_mem_mb,
  (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1048576 AS mean_disk_mb,
  CASE
    WHEN (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 > 0
    THEN 'SPILLING'
    ELSE 'in-memory'
  END AS spill_status
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 > 0
ORDER BY mean_disk_mb DESC;
```

**Remediation:**
- Add indexes to reduce sort/aggregation memory needs
- Increase `sql.distsql.temp_storage.workmem` (with caution)
- Rewrite query to process smaller chunks
- Use incremental aggregation or materialized views

## Network Metrics

### networkBytes

**Definition:** Bytes sent over network (distributed SQL communication between nodes).

**Unit:** Bytes

**Extraction:**
```sql
(statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 AS mean_network_mb
```

**Sampled:** Yes

**High network bytes causes:**
- Distributed JOINs with large intermediate results
- Full table scans on distributed tables
- GROUP BY on high-cardinality columns without indexes

**Optimization:**
- Use locality-optimized queries
- Add indexes to reduce data movement
- Consider table partitioning by access patterns

## Error Metrics

### failureCount

**Definition:** Number of executions that resulted in errors (any error type).

**Unit:** Count (INT)

**Extraction:**
```sql
COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) AS failures
```

**Aggregated:** Yes

**Failure rate calculation:**
```sql
SELECT
  fingerprint_id,
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) AS failures,
  ROUND(
    COALESCE((statistics->'statistics'->>'failureCount')::INT, 0)::NUMERIC /
    NULLIF((statistics->'statistics'->>'cnt')::INT, 0) * 100,
    2
  ) AS failure_rate_pct
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) > 0
ORDER BY failure_rate_pct DESC;
```

**Thresholds:**

| Failure Rate | Severity | Action |
|--------------|----------|---------|
| < 1% | Low | Transient errors acceptable |
| 1% - 5% | Moderate | Investigate error types |
| 5% - 20% | High | Application or schema issue |
| > 20% | Critical | Immediate investigation |

**Common error causes:**
- Constraint violations (unique, foreign key)
- Transaction retry errors (40001 - serialization failure)
- Timeout errors
- Permission denied

## Retry Metrics

### maxRetries

**Definition:** Maximum number of automatic retries for any execution in the bucket.

**Unit:** Count (INT)

**Extraction:**
```sql
(statistics->'statistics'->>'maxRetries')::INT AS max_retries
```

**Aggregated:** Yes

**Thresholds:**

| Max Retries | Contention Level | Action |
|-------------|-----------------|---------|
| 0 - 2 | Normal | Expected for distributed transactions |
| 3 - 10 | Moderate | Monitor for contention patterns |
| 10 - 50 | High | Transaction conflicts, optimize access patterns |
| > 50 | Severe | Critical contention, schema redesign needed |

**High retry analysis:**
```sql
SELECT
  fingerprint_id,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  metadata->>'app' AS application,
  substring(metadata->>'query', 1, 150) AS query_preview
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 10
ORDER BY max_retries DESC;
```

## Derived Metrics and Formulas

### Standard Deviation (for any metric with sqDiff)

```sql
sqrt(
  (statistics->'statistics'->'runLat'->>'sqDiff')::FLOAT8 /
  NULLIF((statistics->'statistics'->>'cnt')::INT, 0)
) AS stddev_run_lat
```

### Coefficient of Variation (CV)

Measures relative variability (stddev / mean):

```sql
sqrt(
  (statistics->'statistics'->'runLat'->>'sqDiff')::FLOAT8 /
  NULLIF((statistics->'statistics'->>'cnt')::INT, 0)
) / NULLIF((statistics->'statistics'->'runLat'->>'mean')::FLOAT8, 0) AS cv_run_lat
```

**Interpretation:**
- CV < 0.5: Low variability (consistent performance)
- CV 0.5 - 1.0: Moderate variability
- CV > 1.0: High variability (investigate causes)

### Estimated Total Resource Consumption

For sampled metrics, estimate total cluster impact:

```sql
-- Estimated total CPU seconds in time window
(statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9 *
(statistics->'statistics'->>'cnt')::INT AS estimated_total_cpu_sec
```

### Throughput (Executions per Second)

```sql
SELECT
  fingerprint_id,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  EXTRACT(EPOCH FROM (now() - aggregated_ts)) AS window_seconds,
  (statistics->'statistics'->>'cnt')::INT /
  NULLIF(EXTRACT(EPOCH FROM (now() - aggregated_ts)), 0) AS executions_per_sec
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '1 hour';
```

## Unit Conversion Quick Reference

| Metric | Stored Unit | Display Unit | Conversion Formula |
|--------|-------------|--------------|-------------------|
| Latency (runLat, parseLat, planLat) | seconds | seconds | (value)::FLOAT8 |
| CPU time (cpuSQLNanos) | nanoseconds | seconds | (value)::FLOAT8 / 1e9 |
| Contention time | nanoseconds | seconds | (value)::FLOAT8 / 1e9 |
| Admission wait | nanoseconds | seconds | (value)::FLOAT8 / 1e9 |
| Memory (maxMemUsage) | bytes | MB | (value)::FLOAT8 / 1048576 |
| Disk (maxDiskUsage) | bytes | MB | (value)::FLOAT8 / 1048576 |
| Network (networkBytes) | bytes | MB | (value)::FLOAT8 / 1048576 |
| Rows | count | count | (value)::FLOAT8 |

## Additional Resources

- **JSON schema:** [json-field-reference.md](json-field-reference.md)
- **Query examples:** [sql-query-variations.md](sql-query-variations.md)
- **Main skill:** [../SKILL.md](../SKILL.md)
- **Official docs:** [Statements Page](https://www.cockroachlabs.com/docs/stable/ui-statements-page.html)

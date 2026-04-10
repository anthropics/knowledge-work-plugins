# Metrics and Units Reference

Comprehensive guide to interpreting transaction statistics metrics, units, conversions, and thresholds for performance analysis.

## Metric Categories

Transaction statistics are divided into two collection modes:

| Category | Collection Method | Coverage | Overhead | Use Case |
|----------|------------------|----------|----------|----------|
| **Aggregated** | Always collected | 100% of executions | Low | Retries, commit/retry latency, execution counts |
| **Sampled** | Probabilistic (~10%) | Representative sample | Medium | Contention, memory, network, disk |

**Critical difference from statement statistics:** Transaction metrics focus on transaction boundary behavior (retries, commit latency) rather than individual statement execution.

## Transaction-Specific Latency Metrics

All latency metrics are stored in **seconds** as FLOAT8.

### retryLat (Retry Latency)

**Definition:** Time spent retrying the transaction due to conflicts, serialization failures, or aborts.

**Extraction:**
```sql
(statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_seconds
```

**Thresholds:**

| Retry Latency | Classification | Action |
|---------------|---------------|---------|
| 0s | No retries | Ideal; no transaction conflicts |
| < 0.1s (100ms) | Low | Acceptable transient conflicts |
| 0.1s - 1s | Moderate | Monitor for patterns; consider batching |
| 1s - 5s | High | Significant contention; optimize transaction boundaries |
| > 5s | Critical | Severe contention or long-running conflicts |

**Interpretation:**
- **OLTP workloads:** Target < 100ms retry latency
- **High retry latency + high maxRetries:** Indicates persistent contention on hot rows
- **Compare with commitLat:** If retryLat > commitLat, retries dominate latency

**Example analysis:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_sec,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_sec,
  ROUND(
    ((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS retry_pct_of_service_lat,
  CASE
    WHEN (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 < 0.1 THEN 'low'
    WHEN (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 < 1 THEN 'moderate'
    WHEN (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 < 5 THEN 'high'
    ELSE 'critical'
  END AS retry_latency_class
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 > 0;
```

### commitLat (Commit Latency)

**Definition:** Time spent in the 2-phase commit protocol at the transaction boundary (distributed transaction coordination overhead).

**Extraction:**
```sql
(statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_seconds
```

**Thresholds:**

| Commit Latency | Classification | Action |
|---------------|---------------|---------|
| < 0.01s (10ms) | Fast | Optimal for local transactions |
| 0.01s - 0.05s (10-50ms) | Moderate | Acceptable for distributed transactions |
| 0.05s - 0.1s (50-100ms) | Elevated | Investigate replication or cross-region latency |
| 0.1s - 0.5s (100-500ms) | High | Likely cross-region; consider geo-partitioning |
| > 0.5s | Very high | Severe replication delay or network issues |

**Interpretation:**
- **Local transactions:** Target < 10ms commit latency
- **Cross-region transactions:** 50-200ms typical (depends on geography)
- **High commit latency causes:** Distributed writes, slow replicas, cross-AZ/region latency, replication lag

**Commit percentage calculation:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS commit_lat_sec,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS service_lat_sec,
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct_of_service_lat,
  metadata->>'app' AS application
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0.05
ORDER BY commit_pct_of_service_lat DESC;
```

**Optimization targets:**
- **Commit % < 10%:** Well-optimized transaction
- **Commit % 10-20%:** Acceptable distributed transaction overhead
- **Commit % > 20%:** Consider batching, geo-partitioning, or reducing transaction scope

### svcLat (Service Latency)

**Definition:** Total end-to-end transaction latency from start to commit completion.

**Formula:**
```
svcLat ≈ execution_time + retryLat + commitLat
```

**Extraction:**
```sql
(statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_seconds
```

**Use for:** Understanding total user-perceived transaction latency; baseline for calculating retry and commit percentages.

**Latency decomposition:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS total_svc_lat_sec,
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
  AND (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 > 0.1
ORDER BY total_svc_lat_sec DESC;
```

## Retry Metrics

### maxRetries

**Definition:** Maximum number of automatic retries for any transaction execution within the hourly bucket.

**Unit:** Count (INT)

**Extraction:**
```sql
(statistics->'statistics'->>'maxRetries')::INT AS max_retries
```

**Thresholds:**

| Max Retries | Contention Level | Action |
|-------------|-----------------|---------|
| 0 | None | Ideal; no transaction conflicts |
| 1-3 | Low | Expected for distributed transactions |
| 4-10 | Moderate | Monitor patterns; check for hot rows |
| 11-50 | High | Significant contention; optimize access patterns |
| > 50 | Severe | Critical retry storm; schema redesign needed |

**Analysis pattern:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  metadata->>'app' AS application,
  metadata->>'db' AS database,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_sec,
  CASE
    WHEN (statistics->'statistics'->>'maxRetries')::INT = 0 THEN 'none'
    WHEN (statistics->'statistics'->>'maxRetries')::INT <= 3 THEN 'low'
    WHEN (statistics->'statistics'->>'maxRetries')::INT <= 10 THEN 'moderate'
    WHEN (statistics->'statistics'->>'maxRetries')::INT <= 50 THEN 'high'
    ELSE 'severe'
  END AS contention_level
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
ORDER BY max_retries DESC;
```

**Common causes:**
- UPDATE/DELETE on same hot rows across concurrent transactions
- Serial writes to monotonically increasing primary keys
- Long-running transactions holding locks
- Insufficient batching of write operations

**Important:** `maxRetries` is the **maximum** across all executions, not average. A single problematic execution can skew this value.

## Contention Metrics

### contentionTime

**Definition:** Time spent waiting for locks held by other transactions at the transaction level.

**Unit:** Nanoseconds (convert to seconds: divide by 1e9)

**Extraction:**
```sql
(statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9 AS mean_contention_sec
```

**Sampled:** Yes (check for `execution_statistics.cnt`)

**Thresholds:**

| Contention % of Service Latency | Severity | Action |
|--------------------------------|----------|---------|
| < 5% | Low | Normal transactional overhead |
| 5% - 20% | Moderate | Monitor patterns; investigate if persistent |
| 20% - 50% | High | Batch operations, optimize transaction scope |
| > 50% | Critical | Schema redesign, partition hot tables, denormalize |

**Calculate contention ratio:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  ROUND(
    ((statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9), 3
  ) AS mean_contention_sec,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS service_lat_sec,
  ROUND(
    ((statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9) /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0) * 100, 2
  ) AS contention_pct_of_service_lat
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 > 0
ORDER BY contention_pct_of_service_lat DESC;
```

**Transaction vs Statement Contention:**
- **Transaction-level:** Cumulative contention across all statements in transaction
- **Statement-level:** Contention for individual queries
- **Use case:** Transaction contention shows total lock wait; drill to statements for specific bottlenecks

## Resource Metrics

### networkBytes

**Definition:** Bytes sent over network for distributed SQL coordination between nodes.

**Unit:** Bytes (convert to MB: divide by 1048576)

**Extraction:**
```sql
(statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 AS mean_network_mb
```

**Sampled:** Yes

**Thresholds:**

| Network Bytes | Transaction Type | Consideration |
|---------------|-----------------|---------------|
| < 1 MB | Local/single-node | Optimal |
| 1 MB - 10 MB | Small distributed | Acceptable |
| 10 MB - 100 MB | Medium distributed | Monitor for efficiency |
| > 100 MB | Large distributed | Consider partitioning or locality optimization |

**High network causes:**
- Cross-region distributed transactions
- Large intermediate result sets
- Inefficient query plans with excessive data movement

**Example analysis:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 AS mean_network_mb,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  ROUND(
    ((statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576) *
    (statistics->'statistics'->>'cnt')::INT, 2
  ) AS estimated_total_network_mb,
  metadata->>'app' AS application
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 > 0
ORDER BY estimated_total_network_mb DESC;
```

### maxMemUsage

**Definition:** Maximum memory allocated during transaction execution.

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
| 10 MB - 100 MB | Moderate | Monitor for large result sets |
| 100 MB - 512 MB | High | Check query efficiency |
| > 512 MB | Very high | Risk of memory spill to disk |

**Default workmem limit:** Check `sql.distsql.temp_storage.workmem` setting (typically 64 MB).

### maxDiskUsage

**Definition:** Maximum disk space used for temporary storage when memory limit exceeded (memory spill).

**Unit:** Bytes (convert to MB: divide by 1048576)

**Extraction:**
```sql
(statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1048576 AS mean_disk_mb
```

**Sampled:** Yes

**Interpretation:**
- **> 0:** Transaction exceeded workmem and spilled to disk (performance degradation ~100-1000x)
- **Large values:** Significant I/O overhead; immediate optimization needed

**Spill analysis:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576 AS mean_mem_mb,
  (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1048576 AS mean_disk_mb,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  CASE
    WHEN (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 > 0
    THEN 'SPILLING'
    ELSE 'in-memory'
  END AS memory_status,
  metadata->>'app' AS application
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
ORDER BY mean_disk_mb DESC;
```

## Row Metrics

### numRows

**Definition:** Number of rows affected by the transaction (INSERT/UPDATE/DELETE operations).

**Unit:** Count (FLOAT8 for mean)

**Extraction:**
```sql
(statistics->'statistics'->'numRows'->>'mean')::FLOAT8 AS mean_rows_affected
```

**Aggregated:** Yes (all executions)

**Thresholds:**

| Rows Affected | Transaction Type | Consideration |
|---------------|-----------------|---------------|
| < 10 | Small | Typical OLTP |
| 10 - 1,000 | Medium | Acceptable for batch operations |
| 1,000 - 10,000 | Large | Monitor for efficiency |
| > 10,000 | Very large | Consider batching strategy |

**Example:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->'numRows'->>'mean')::FLOAT8 AS avg_rows_affected,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_sec,
  metadata->>'app' AS application
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
ORDER BY avg_rows_affected DESC
LIMIT 20;
```

## Derived Metrics and Formulas

### Retry Rate Percentage

**Formula:** Retry latency as percentage of total service latency

```sql
ROUND(
  ((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 /
  NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
) AS retry_pct_of_service_lat
```

**Interpretation:**
- **< 10%:** Low retry impact
- **10-30%:** Moderate retry overhead
- **> 30%:** Retries dominate latency; high contention

### Commit Latency Percentage

**Formula:** Commit latency as percentage of total service latency

```sql
ROUND(
  ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
  NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
) AS commit_pct_of_service_lat
```

**Interpretation:**
- **< 10%:** Minimal distributed overhead
- **10-20%:** Normal distributed transaction cost
- **> 20%:** High commit overhead; investigate replication or cross-region latency

### Standard Deviation (for any metric with sqDiff)

```sql
sqrt(
  (statistics->'statistics'->'commitLat'->>'sqDiff')::FLOAT8 /
  NULLIF((statistics->'statistics'->>'cnt')::INT, 0)
) AS stddev_commit_lat
```

### Estimated Total Resource Consumption

For sampled metrics, estimate total cluster impact:

```sql
-- Estimated total network MB in time window
ROUND(
  ((statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576) *
  (statistics->'statistics'->>'cnt')::INT, 2
) AS estimated_total_network_mb
```

## Transaction vs Statement Metric Comparison

| Metric | Transaction-Level | Statement-Level | Use Case |
|--------|------------------|----------------|----------|
| **Retries** | maxRetries (transaction boundary) | maxRetries (statement-level) | Transaction: overall retry storm; Statement: specific query conflicts |
| **Commit Latency** | commitLat (2PC overhead) | N/A | Only meaningful at transaction boundary |
| **Retry Latency** | retryLat (total retry time) | N/A | Only meaningful at transaction boundary |
| **Contention** | Cumulative across statements | Per statement | Transaction: total lock wait; Statement: specific bottleneck |
| **Service Latency** | End-to-end transaction time | Individual query time | Transaction: user-perceived latency; Statement: query optimization |

**When to use transaction vs statement profiling:**
- **High retries:** Use transaction profiling to identify retry storms, then drill to statements
- **Slow commits:** Transaction-only metric; analyze commit latency trends
- **Contention:** Transaction shows total; statement shows which query causes locks
- **Latency optimization:** Start with statements, aggregate understanding via transactions

## Unit Conversion Quick Reference

| Metric | Stored Unit | Display Unit | Conversion Formula |
|--------|-------------|--------------|-------------------|
| Retry latency (retryLat) | seconds | seconds | (value)::FLOAT8 |
| Commit latency (commitLat) | seconds | seconds | (value)::FLOAT8 |
| Service latency (svcLat) | seconds | seconds | (value)::FLOAT8 |
| Contention time | nanoseconds | seconds | (value)::FLOAT8 / 1e9 |
| Memory (maxMemUsage) | bytes | MB | (value)::FLOAT8 / 1048576 |
| Disk (maxDiskUsage) | bytes | MB | (value)::FLOAT8 / 1048576 |
| Network (networkBytes) | bytes | MB | (value)::FLOAT8 / 1048576 |
| Rows | count | count | (value)::FLOAT8 |
| Retries | count | count | (value)::INT |

## Additional Resources

- **JSON schema:** [json-field-reference.md](json-field-reference.md)
- **Query examples:** [sql-query-variations.md](sql-query-variations.md)
- **Main skill:** [../SKILL.md](../SKILL.md)
- **Official docs:** [Transactions Page](https://www.cockroachlabs.com/docs/stable/ui-transactions-page.html)

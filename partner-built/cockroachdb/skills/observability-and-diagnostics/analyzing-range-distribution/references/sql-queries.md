# SQL Query Variations for Range Distribution Analysis

This reference provides production-safe query templates for analyzing CockroachDB range distribution. All queries using `WITH DETAILS` include mandatory guardrails to prevent performance impact.

## Table of Contents

1. [Range Count Queries (Production-Safe)](#range-count-queries-production-safe)
2. [Range Size Analysis (Targeted DETAILS)](#range-size-analysis-targeted-details)
3. [Leaseholder Distribution (Hotspot Detection)](#leaseholder-distribution-hotspot-detection)
4. [Replication Health Checks](#replication-health-checks)
5. [Zone Configuration Auditing](#zone-configuration-auditing)
6. [Fragmentation Analysis (Advanced)](#fragmentation-analysis-advanced)
7. [Safety Guardrails Summary](#safety-guardrails-summary)

---

## Range Count Queries (Production-Safe)

### Query 1.1: Basic Range Count by Table

```sql
-- Total range count for a specific table across all indexes
SELECT
  table_name,
  index_name,
  COUNT(*) AS range_count
FROM [SHOW RANGES FROM TABLE your_table_name]
GROUP BY table_name, index_name
ORDER BY range_count DESC;
```

**Output:**
- `table_name`: Table name
- `index_name`: Index name (primary or secondary)
- `range_count`: Number of ranges for this index

**Use case:** Quick assessment of range distribution without DETAILS overhead.

**Safety:** No DETAILS option = minimal CPU, metadata-only query.

---

### Query 1.2: Cluster-Wide Range Count by Database

```sql
-- Range count per database (requires iteration or custom query)
-- NOTE: SHOW RANGES FROM DATABASE is not supported; use per-table queries
SELECT
  database_name,
  schema_name,
  name AS table_name,
  estimated_row_count
FROM crdb_internal.tables
WHERE database_name = 'your_database_name'
ORDER BY estimated_row_count DESC;
```

**Use case:** Identify largest tables to prioritize for range analysis.

**Safety:** Production-safe, uses internal catalog metadata.

---

### Query 1.3: Range Count with Start/End Keys

```sql
-- Show range boundaries (useful for understanding key distribution)
SELECT
  range_id,
  start_key,
  end_key,
  lease_holder,
  replicas
FROM [SHOW RANGES FROM TABLE your_table_name]
ORDER BY start_key
LIMIT 20;
```

**Output:**
- `range_id`: Unique range identifier
- `start_key`, `end_key`: Range key boundaries (hex-encoded)
- `lease_holder`: Node ID holding the leaseholder replica
- `replicas`: Array of node IDs with replicas

**Use case:** Identify key distribution patterns, detect hot key ranges.

**Safety:** No DETAILS, production-safe.

---

## Range Size Analysis (Targeted DETAILS)

**CRITICAL WARNING:** All queries in this section use `WITH DETAILS`. Always include:
1. `LIMIT` clause (default: 50-100)
2. Specific table targeting (`FROM TABLE table_name`)
3. Execute during low-traffic windows in production

---

### Query 2.1: Largest Ranges by Size

```sql
-- Find largest ranges (potential split candidates)
SELECT
  range_id,
  start_key,
  end_key,
  (span_stats->>'approximate_disk_bytes')::BIGINT / 1048576 AS size_mb,
  (span_stats->>'live_bytes')::BIGINT / 1048576 AS live_mb,
  (span_stats->>'key_count')::BIGINT AS key_count,
  lease_holder,
  replicas
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
ORDER BY (span_stats->>'approximate_disk_bytes')::BIGINT DESC
LIMIT 50;
```

**Output:**
- `size_mb`: Total disk bytes (includes MVCC versions, garbage)
- `live_mb`: Live data bytes (current values only)
- `key_count`: Number of keys in range

**Interpretation:**
- `size_mb > 64`: Range exceeds default split threshold (check for split lag or custom `range_max_bytes`)
- `live_mb << size_mb`: High MVCC overhead, may benefit from GC tuning

**Safety:** LIMIT 50 mandatory. Never remove LIMIT.

---

### Query 2.2: Smallest Ranges (Fragmentation Detection)

```sql
-- Identify fragmented ranges (many small ranges)
SELECT
  range_id,
  start_key,
  end_key,
  (span_stats->>'approximate_disk_bytes')::BIGINT / 1048576 AS size_mb,
  (span_stats->>'key_count')::BIGINT AS key_count,
  lease_holder
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
WHERE (span_stats->>'approximate_disk_bytes')::BIGINT < 10485760  -- < 10MB
ORDER BY (span_stats->>'approximate_disk_bytes')::BIGINT ASC
LIMIT 50;
```

**Interpretation:**
- Many ranges < 10MB = fragmentation from load-based splitting
- Check if intentional (high QPS on sequential keys) or anomaly

**Safety:** Filtered query with LIMIT, production-acceptable during maintenance.

---

### Query 2.3: Average Range Size per Index

```sql
-- Calculate average range size per index
SELECT
  table_name,
  index_name,
  COUNT(*) AS range_count,
  ROUND(AVG((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0, 2) AS avg_size_mb,
  ROUND(SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0, 2) AS total_size_gb
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
GROUP BY table_name, index_name
ORDER BY total_size_gb DESC;
```

**Interpretation:**
- `avg_size_mb` near 64MB = healthy, ranges splitting as expected
- `avg_size_mb` < 20MB with high `range_count` = fragmentation

**CRITICAL:** Aggregating DETAILS data across all ranges is expensive. Use only on small-medium tables (< 1000 ranges).

---

## Leaseholder Distribution (Hotspot Detection)

### Query 3.1: Leaseholder Concentration by Node

```sql
-- Identify leaseholder hotspots
SELECT
  lease_holder,
  COUNT(*) AS leaseholder_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM [SHOW RANGES FROM TABLE your_table_name]
GROUP BY lease_holder
ORDER BY leaseholder_count DESC;
```

**Interpretation:**
- **Balanced cluster:** Each node ~(100 / node_count)% leaseholders
- **Hotspot:** Single node > 40% leaseholders (3-node cluster) or > 20% (5+ node cluster)

**Remediation:** Use `ALTER TABLE ... CONFIGURE ZONE USING lease_preferences` to spread leaseholders.

**Safety:** No DETAILS, production-safe.

---

### Query 3.2: Leaseholder Distribution with Replica Count

```sql
-- Cross-reference leaseholder concentration with replica health
SELECT
  lease_holder,
  COUNT(*) AS leaseholder_count,
  ROUND(AVG(array_length(replicas, 1)), 2) AS avg_replica_count,
  MIN(array_length(replicas, 1)) AS min_replicas,
  MAX(array_length(replicas, 1)) AS max_replicas
FROM [SHOW RANGES FROM TABLE your_table_name]
GROUP BY lease_holder
ORDER BY leaseholder_count DESC;
```

**Use case:** Detect if leaseholder concentration correlates with under-replication.

**Safety:** No DETAILS, production-safe.

---

### Query 3.3: Leaseholder Changes Over Time (Requires Historical Data)

```sql
-- Snapshot leaseholder distribution for time-series tracking
-- Run periodically and store results externally
SELECT
  NOW() AS snapshot_time,
  lease_holder,
  COUNT(*) AS leaseholder_count
FROM [SHOW RANGES FROM TABLE your_table_name]
GROUP BY lease_holder
ORDER BY lease_holder;
```

**Use case:** Track leaseholder rebalancing after zone config changes.

**Implementation:** Run via cron, store in monitoring system or separate table.

---

## Replication Health Checks

### Query 4.1: Under-Replicated Ranges

```sql
-- Find ranges with fewer than expected replicas
SELECT
  range_id,
  start_key,
  end_key,
  replicas,
  array_length(replicas, 1) AS replica_count,
  voting_replicas,
  array_length(voting_replicas, 1) AS voting_replica_count,
  lease_holder
FROM [SHOW RANGES FROM TABLE your_table_name]
WHERE array_length(replicas, 1) < 3  -- Adjust based on replication factor
ORDER BY array_length(replicas, 1) ASC, range_id
LIMIT 100;
```

**Interpretation:**
- `replica_count < 3`: Under-replicated (data loss risk if 2 nodes fail)
- Check for node failures, decommissioning, or zone config constraints preventing replication

**Safety:** No DETAILS, production-safe.

---

### Query 4.2: Over-Replicated Ranges (Zone Config Mismatch)

```sql
-- Detect ranges exceeding intended replication factor
SELECT
  range_id,
  start_key,
  replicas,
  array_length(replicas, 1) AS replica_count
FROM [SHOW RANGES FROM TABLE your_table_name]
WHERE array_length(replicas, 1) > 3  -- Adjust based on intended replication factor
ORDER BY array_length(replicas, 1) DESC
LIMIT 50;
```

**Use case:** Identify ranges with excess replicas (wasting storage) after zone config changes.

**Safety:** No DETAILS, production-safe.

---

### Query 4.3: Non-Voting Replica Analysis

```sql
-- Identify ranges with non-voting replicas (learner replicas during rebalancing)
SELECT
  range_id,
  replicas,
  voting_replicas,
  array_length(replicas, 1) - array_length(voting_replicas, 1) AS non_voting_count
FROM [SHOW RANGES FROM TABLE your_table_name]
WHERE array_length(replicas, 1) != array_length(voting_replicas, 1)
ORDER BY non_voting_count DESC
LIMIT 50;
```

**Interpretation:**
- Non-voting replicas = temporary state during rebalancing or node addition
- Persistent non-voting replicas may indicate rebalancing stuck

**Safety:** No DETAILS, production-safe.

---

## Zone Configuration Auditing

### Query 5.1: Show All Custom Zone Configurations

```sql
-- List all non-default zone configurations
SHOW ZONE CONFIGURATIONS;
```

**Output:**
- `target`: Database, table, or index name
- `raw_config_sql`: Zone configuration SQL statement

**Use case:** Audit all custom zone configs in cluster.

**Safety:** Metadata query, production-safe.

---

### Query 5.2: Show Zone Config for Specific Table

```sql
-- Show zone configuration for a specific table
SHOW ZONE CONFIGURATION FOR TABLE your_table_name;
```

**Output:**
- `target`: Table name
- `raw_config_sql`: Zone config SQL (replication factor, constraints, lease_preferences)

**Use case:** Validate table-specific zone config before comparing with actual range placement.

**Safety:** Metadata query, production-safe.

---

### Query 5.3: Inherited Zone Configuration (Show Full Hierarchy)

```sql
-- Show effective zone config (including inherited defaults)
SELECT * FROM [SHOW ZONE CONFIGURATION FOR TABLE your_table_name];
```

**Output includes inherited values:**
- `range_min_bytes`, `range_max_bytes`
- `gc.ttlseconds`
- `num_replicas`
- `constraints`, `lease_preferences`

**Use case:** Understand full effective zone config when no table-level override exists.

---

## Fragmentation Analysis (Advanced)

**CRITICAL:** This section combines DETAILS queries with aggregations. Use only on small-medium tables.

---

### Query 6.1: Ranges per Gigabyte (Fragmentation Metric)

```sql
-- Calculate fragmentation ratio
WITH range_counts AS (
  SELECT
    table_name,
    index_name,
    COUNT(*) AS range_count
  FROM [SHOW RANGES FROM TABLE your_table_name]
  GROUP BY table_name, index_name
),
table_sizes AS (
  SELECT
    table_name,
    SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0 AS size_gb
  FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
  GROUP BY table_name
)
SELECT
  rc.table_name,
  rc.index_name,
  rc.range_count,
  ROUND(ts.size_gb, 2) AS size_gb,
  ROUND(rc.range_count / NULLIF(ts.size_gb, 0), 2) AS ranges_per_gb
FROM range_counts rc
JOIN table_sizes ts ON rc.table_name = ts.table_name
ORDER BY ranges_per_gb DESC;
```

**Interpretation:**
- **1-15 ranges/GB:** Healthy
- **16-50 ranges/GB:** Moderate fragmentation
- **50+ ranges/GB:** Severe fragmentation

**CRITICAL:** This query scans all ranges with DETAILS. Use only on targeted tables, never cluster-wide.

---

### Query 6.2: Range Size Distribution Histogram

```sql
-- Categorize ranges by size buckets
SELECT
  CASE
    WHEN (span_stats->>'approximate_disk_bytes')::BIGINT < 10485760 THEN '< 10MB'
    WHEN (span_stats->>'approximate_disk_bytes')::BIGINT < 33554432 THEN '10-32MB'
    WHEN (span_stats->>'approximate_disk_bytes')::BIGINT < 67108864 THEN '32-64MB'
    WHEN (span_stats->>'approximate_disk_bytes')::BIGINT < 134217728 THEN '64-128MB'
    ELSE '> 128MB'
  END AS size_bucket,
  COUNT(*) AS range_count,
  ROUND(AVG((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0, 2) AS avg_size_mb
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
GROUP BY size_bucket
ORDER BY
  CASE size_bucket
    WHEN '< 10MB' THEN 1
    WHEN '10-32MB' THEN 2
    WHEN '32-64MB' THEN 3
    WHEN '64-128MB' THEN 4
    ELSE 5
  END;
```

**Interpretation:**
- Majority in 32-64MB = healthy
- Many in < 10MB = fragmentation
- Many in > 128MB = split lag or custom `range_max_bytes`

**CRITICAL:** Uses DETAILS on all ranges. Limit to small-medium tables.

---

### Query 6.3: Fragmentation Trend by Index

```sql
-- Compare fragmentation across indexes on same table
SELECT
  index_name,
  COUNT(*) AS range_count,
  ROUND(AVG((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0, 2) AS avg_range_size_mb,
  ROUND(SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0, 2) AS total_size_gb,
  ROUND(COUNT(*) / NULLIF(SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0, 0), 2) AS ranges_per_gb
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
GROUP BY index_name
ORDER BY ranges_per_gb DESC;
```

**Use case:** Identify if specific indexes (e.g., timestamp-based) are more fragmented than primary key.

**CRITICAL:** Aggregates DETAILS data. Use only on targeted tables.

---

## Safety Guardrails Summary

### Mandatory DETAILS Guardrails

**Always apply when using `WITH DETAILS`:**

1. **LIMIT clause:** Default 50-100, never exceed 500
2. **Specific table targeting:** Use `FROM TABLE table_name`, never cluster-wide
3. **Production timing:** Execute during maintenance windows or low-traffic periods
4. **Pre-check range count:** Run basic `SHOW RANGES` (no DETAILS) first to assess table size

**Example of UNSAFE query (NEVER RUN):**
```sql
-- DANGER: No LIMIT, cluster-wide scan
SHOW RANGES WITH DETAILS;  -- DO NOT RUN
```

**Example of SAFE query:**
```sql
-- Safe: Targeted table, LIMIT, specific use case
SELECT range_id, (span_stats->>'approximate_disk_bytes')::BIGINT
FROM [SHOW RANGES FROM TABLE users WITH DETAILS]
ORDER BY range_id
LIMIT 50;
```

---

### Query Complexity Tiers

| Tier | Query Type | Production Safety | Use Case |
|------|------------|-------------------|----------|
| **Safe** | Basic SHOW RANGES (no DETAILS) | Always safe | Quick range counts, leaseholder checks |
| **Moderate** | SHOW RANGES WITH DETAILS + LIMIT 50 | Safe during low-traffic | Targeted size analysis |
| **High** | SHOW RANGES WITH DETAILS + aggregations | Maintenance window only | Fragmentation analysis on small tables |
| **FORBIDDEN** | SHOW RANGES WITH DETAILS (no LIMIT, cluster-wide) | **NEVER USE** | N/A |

---

### Production Checklist

Before running DETAILS queries:

- [ ] Confirmed table has < 5000 ranges (run basic `SHOW RANGES` first)
- [ ] Added `LIMIT` clause (default: 50)
- [ ] Targeted specific table (`FROM TABLE table_name`)
- [ ] Scheduled during maintenance window or low-traffic period
- [ ] Reviewed query timeout settings (increase if needed for large tables)

---

## Quick Reference Card

```sql
-- Production-safe quick reference
-- 1. Range count (always safe)
SELECT COUNT(*) FROM [SHOW RANGES FROM TABLE t];

-- 2. Leaseholder distribution (always safe)
SELECT lease_holder, COUNT(*) FROM [SHOW RANGES FROM TABLE t] GROUP BY lease_holder;

-- 3. Replication health (always safe)
SELECT COUNT(*) FROM [SHOW RANGES FROM TABLE t] WHERE array_length(replicas, 1) < 3;

-- 4. Zone config (always safe)
SHOW ZONE CONFIGURATION FOR TABLE t;

-- 5. Range sizes (DETAILS - use LIMIT)
SELECT range_id, (span_stats->>'approximate_disk_bytes')::BIGINT
FROM [SHOW RANGES FROM TABLE t WITH DETAILS]
ORDER BY range_id LIMIT 50;
```

---

## Related Documentation

- [Main skill documentation](../SKILL.md)
- [Permissions reference](permissions.md)
- [CockroachDB SHOW RANGES documentation](https://www.cockroachlabs.com/docs/stable/show-ranges.html)
- [CockroachDB SHOW ZONE CONFIGURATIONS documentation](https://www.cockroachlabs.com/docs/stable/show-zone-configurations.html)

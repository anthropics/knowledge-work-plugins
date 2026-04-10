# Statistics Thresholds Guide

Detailed guidance for determining when table statistics are stale and require refresh, tailored to different workload types, table sizes, and update patterns.

## Staleness Thresholds by Workload Type

### OLTP (Online Transaction Processing)

**Characteristics:** High-frequency small transactions, latency-sensitive queries, frequent updates

| Table Type | Recommended Refresh Interval | Rationale |
|------------|----------------------------|-----------|
| **Hot tables** (orders, transactions) | 1-3 days | Rapid data changes, query patterns evolve quickly |
| **Reference tables** (users, products) | 3-7 days | Moderate update frequency, stable distribution |
| **Lookup tables** (statuses, categories) | 14-30 days | Rarely updated, stable cardinality |

**Staleness detection query:**
```sql
SELECT
  table_name,
  created,
  now() - created AS stats_age,
  CASE
    WHEN now() - created > INTERVAL '3 days' THEN 'Stale for OLTP'
    ELSE 'Fresh'
  END AS oltp_status
FROM [SHOW STATISTICS FOR TABLE database_name.*]
WHERE column_names = '{}'
ORDER BY stats_age DESC;
```

### OLAP (Online Analytical Processing)

**Characteristics:** Batch-oriented, complex queries, bulk updates, less latency-sensitive

| Table Type | Recommended Refresh Interval | Rationale |
|------------|----------------------------|-----------|
| **Fact tables** (daily/hourly loads) | 7-14 days | Batch update cycles, stable between loads |
| **Dimension tables** (slowly changing) | 14-30 days | Infrequent updates, predictable patterns |
| **Archive tables** (historical data) | 30-90 days | Read-only or append-only, no distribution changes |

**Staleness detection query:**
```sql
SELECT
  table_name,
  created,
  now() - created AS stats_age,
  CASE
    WHEN now() - created > INTERVAL '14 days' THEN 'Consider refresh for OLAP'
    WHEN now() - created > INTERVAL '30 days' THEN 'Stale for OLAP'
    ELSE 'Fresh'
  END AS olap_status
FROM [SHOW STATISTICS FOR TABLE warehouse_db.*]
WHERE column_names = '{}'
ORDER BY stats_age DESC;
```

### Batch Processing Workloads

**Characteristics:** Periodic bulk loads (ETL, data pipelines), predictable update schedules

**Recommended strategy:** Refresh immediately after each bulk load cycle

**Automation example:**
```bash
#!/bin/bash
# ETL pipeline with statistics refresh
set -e

# Step 1: Bulk data load
echo "Loading data..."
cockroach sql -e "IMPORT INTO staging_table CSV DATA ('s3://bucket/data.csv');"

# Step 2: Refresh statistics
echo "Refreshing statistics..."
cockroach sql -e "CREATE STATISTICS __auto__ FROM staging_table;"

# Step 3: Monitor job completion
echo "Waiting for statistics job..."
while true; do
  status=$(cockroach sql --format=tsv -e "
    SELECT status FROM [SHOW JOBS]
    WHERE job_type = 'CREATE STATS'
      AND created > now() - INTERVAL '5 minutes'
    ORDER BY created DESC
    LIMIT 1;
  ")

  if [[ "$status" == "succeeded" ]]; then
    echo "Statistics collection completed"
    break
  elif [[ "$status" == "failed" ]]; then
    echo "Statistics collection failed"
    exit 1
  fi

  sleep 10
done

# Step 4: Downstream processing
echo "Proceeding with downstream queries..."
```

### Real-Time Data Ingestion

**Characteristics:** Continuous high-volume writes (IoT, logging, streaming data)

| Ingestion Rate | Recommended Refresh Interval | Rationale |
|----------------|----------------------------|-----------|
| **Very high** (>10K rows/sec) | 1-3 days | Row count changes rapidly, automatic collection may lag |
| **High** (1K-10K rows/sec) | 3-5 days | Frequent updates, balance freshness vs resource cost |
| **Moderate** (<1K rows/sec) | 5-7 days | Automatic collection likely sufficient |

**Monitoring query:**
```sql
-- Detect tables with high write volume needing frequent refresh
WITH recent_stats AS (
  SELECT
    table_name,
    row_count,
    created
  FROM [SHOW STATISTICS FOR TABLE metrics.*]
  WHERE column_names = '{}'
    AND created > now() - INTERVAL '1 day'
),
current_counts AS (
  SELECT
    table_name,
    (SELECT count(*) FROM metrics.table_name) AS actual_rows  -- Replace dynamically
  FROM information_schema.tables
  WHERE table_schema = 'metrics'
)
SELECT
  r.table_name,
  r.row_count AS stats_rows,
  c.actual_rows,
  c.actual_rows - r.row_count AS growth_since_last_stats,
  ROUND((c.actual_rows - r.row_count)::NUMERIC / NULLIF(r.row_count, 0) * 100, 2) AS growth_pct
FROM recent_stats r
JOIN current_counts c ON r.table_name = c.table_name
WHERE (c.actual_rows - r.row_count)::NUMERIC / NULLIF(r.row_count, 0) > 0.20  -- >20% growth
ORDER BY growth_pct DESC;
```

## Row Count Drift Classification

### Drift Severity Levels

| Drift Percentage | Severity | Impact on Optimizer | Recommended Action |
|------------------|----------|-------------------|-------------------|
| **0-10%** | Minimal | Negligible, estimates remain accurate | No action, normal variance |
| **10-20%** | Low | Minor estimation errors possible | Monitor trend, no immediate action unless performance issues |
| **20-30%** | Medium | Noticeable estimation errors likely | Consider refresh if queries slow or plans change |
| **30-50%** | High | Significant estimation errors, suboptimal plans | Refresh recommended, prioritize high-traffic tables |
| **>50%** | Critical | Very poor estimates, likely full table scans | Urgent refresh required |

### Drift Detection Query with Severity

```sql
WITH current_count AS (
  SELECT count(*) AS actual_rows FROM table_name  -- Replace
),
stats_count AS (
  SELECT row_count, created
  FROM [SHOW STATISTICS FOR TABLE table_name]
  WHERE column_names = '{}'
  ORDER BY created DESC
  LIMIT 1
)
SELECT
  c.actual_rows,
  s.row_count AS stats_rows,
  s.created,
  now() - s.created AS stats_age,
  ABS(c.actual_rows - s.row_count) AS drift_absolute,
  ROUND(ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) * 100, 2) AS drift_pct,
  CASE
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.50 THEN 'CRITICAL (>50%)'
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.30 THEN 'HIGH (30-50%)'
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.20 THEN 'MEDIUM (20-30%)'
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.10 THEN 'LOW (10-20%)'
    ELSE 'MINIMAL (<10%)'
  END AS severity,
  CASE
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.30 THEN 'URGENT: Refresh immediately'
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.20 THEN 'Recommended: Refresh if performance issues'
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.10 THEN 'Optional: Monitor for trends'
    ELSE 'No action needed'
  END AS recommendation
FROM current_count c, stats_count s;
```

### Asymmetric Drift Considerations

**Growth (current > cached):**
- **Impact:** Optimizer underestimates cardinality, may choose nested loops over hash joins
- **Symptoms:** Queries slow down as table grows
- **Priority:** High for tables with frequent joins

**Shrinkage (current < cached):**
- **Impact:** Optimizer overestimates cardinality, may choose hash joins unnecessarily
- **Symptoms:** Excessive memory usage, admission queue delays
- **Priority:** Medium, less common but can impact resource allocation

**Directional drift query:**
```sql
-- Distinguish growth vs shrinkage
WITH drift_analysis AS (
  -- Use drift detection query from above
  ...
)
SELECT
  *,
  CASE
    WHEN actual_rows > stats_rows THEN 'Table growth (underestimation risk)'
    WHEN actual_rows < stats_rows THEN 'Table shrinkage (overestimation risk)'
    ELSE 'No drift'
  END AS drift_direction
FROM drift_analysis;
```

## Table Size Considerations

### Small Tables (<10,000 rows)

**Statistics importance:** Low - optimizer handles small tables efficiently without statistics

**Refresh guidance:**
- **Staleness tolerance:** 30+ days acceptable
- **Drift tolerance:** >50% acceptable
- **Rationale:** Optimizer can scan entire table quickly; inaccurate estimates have minimal impact

**Exception:** Small dimension tables with very high join frequency may still benefit from accurate statistics

### Medium Tables (10K - 10M rows)

**Statistics importance:** High - standard thresholds apply

**Refresh guidance:**
- **Staleness tolerance:** 7-14 days (OLTP), 14-30 days (OLAP)
- **Drift tolerance:** 20-30% threshold
- **Collection time:** Seconds to minutes (minimal impact)

**Recommendation:** Follow workload-specific thresholds (see above)

### Large Tables (10M - 1B rows)

**Statistics importance:** Critical - poor estimates cause severe performance degradation

**Refresh guidance:**
- **Staleness tolerance:** 3-7 days for critical tables
- **Drift tolerance:** 15-20% threshold (lower than medium tables)
- **Collection time:** Minutes to hours
- **Scheduling:** Coordinate with maintenance windows

**Best practices:**
- Schedule CREATE STATISTICS during low-traffic periods (nights/weekends)
- Monitor job progress and cluster resource utilization
- Consider staggered refresh (batch multiple large tables over several days)

**Resource monitoring:**
```sql
-- Monitor CREATE STATISTICS job for large table
SELECT
  job_id,
  description,
  status,
  fraction_completed,
  running_status,
  created,
  now() - created AS elapsed_time
FROM [SHOW JOBS]
WHERE job_type = 'CREATE STATS'
  AND description LIKE '%large_table_name%'
ORDER BY created DESC
LIMIT 1;
```

### Very Large Tables (>1B rows)

**Statistics importance:** Critical - cannot rely on automatic collection (may be delayed indefinitely)

**Refresh guidance:**
- **Staleness tolerance:** 5-7 days maximum
- **Drift tolerance:** 10-15% threshold (aggressive monitoring)
- **Collection time:** Hours to days
- **Scheduling:** Dedicated maintenance windows required

**Special considerations:**
- **Automatic collection may fail or timeout:** Manual CREATE STATISTICS required
- **Partition-aware strategies:** If table is range-partitioned, consider per-partition statistics
- **Resource quotas:** May need to increase `sql.stats.max_timestamp_age` or other limits
- **Cancellation risk:** Jobs may be preempted; use job monitoring to detect failures

**Partition-aware example:**
```sql
-- For range-partitioned table, refresh most recent partition only
CREATE STATISTICS __auto__ FROM large_table WHERE partition_key >= '2026-01-01';
```

## Collection Frequency Matrix

Combines workload type and table size for comprehensive refresh recommendations:

| Table Size | OLTP Hot | OLTP Reference | OLAP Fact | OLAP Dimension | Archive |
|------------|----------|---------------|-----------|----------------|---------|
| **Small (<10K)** | 7 days | 14 days | 30 days | 30 days | 90 days |
| **Medium (10K-10M)** | 3 days | 7 days | 14 days | 30 days | 60 days |
| **Large (10M-1B)** | 1-3 days | 5 days | 7 days | 14 days | 30 days |
| **Very Large (>1B)** | 1-2 days | 3-5 days | 7 days | 14 days | 30 days |

**Usage:**
1. Identify table size (row count)
2. Classify workload pattern (OLTP hot/reference, OLAP fact/dimension, archive)
3. Use intersection for recommended refresh interval
4. Adjust based on observed drift and performance

**Automation script example:**
```bash
#!/bin/bash
# Scheduled statistics refresh based on matrix

# Large OLTP hot tables - daily refresh
for table in orders transactions events; do
  cockroach sql -e "CREATE STATISTICS __auto__ FROM oltp.$table;" &
done
wait

sleep 60  # Delay between batches

# Medium OLTP reference tables - weekly refresh (check day of week)
if [[ $(date +%u) -eq 7 ]]; then  # Sunday
  for table in users products categories; do
    cockroach sql -e "CREATE STATISTICS __auto__ FROM oltp.$table;" &
  done
  wait
fi

# Large OLAP fact tables - weekly refresh
if [[ $(date +%u) -eq 1 ]]; then  # Monday
  for table in sales_facts inventory_facts; do
    cockroach sql -e "CREATE STATISTICS __auto__ FROM analytics.$table;" &
  done
  wait
fi
```

## Automatic Collection Trigger Points

CockroachDB's automatic statistics collection is triggered when row count changes by ~20% (configurable via `sql.stats.automatic_collection.fraction_stale_rows`).

### Default Threshold Behavior

**Setting:** `sql.stats.automatic_collection.fraction_stale_rows = 0.2` (default)

**Trigger condition:**
```
ABS(current_row_count - stats_row_count) / stats_row_count >= 0.2
```

**Example:**
- Table has 1,000,000 rows, statistics collected
- Automatic refresh triggers when row count reaches 1,200,000 (20% growth) or 800,000 (20% shrinkage)

### Adjusting Automatic Collection Threshold

**More aggressive (10% threshold):**
```sql
-- Refresh statistics more frequently
SET CLUSTER SETTING sql.stats.automatic_collection.fraction_stale_rows = 0.10;
```

**Less aggressive (30% threshold):**
```sql
-- Reduce automatic collection frequency (for very large clusters)
SET CLUSTER SETTING sql.stats.automatic_collection.fraction_stale_rows = 0.30;
```

**Use cases:**
- **Lower threshold (0.10):** High-traffic OLTP, latency-sensitive queries, small to medium tables
- **Higher threshold (0.30):** OLAP workloads, very large tables (reduce resource consumption)

**Verification:**
```sql
SHOW CLUSTER SETTING sql.stats.automatic_collection.fraction_stale_rows;
```

### Manual Refresh Schedule Recommendations

Even with automatic collection enabled, manual refresh is recommended for:

1. **Post-bulk-load:** Immediate refresh after IMPORT, COPY, or bulk INSERT
2. **Correlated columns:** Multi-column statistics (automatic collection only creates single-column)
3. **Very large tables:** Automatic collection may be delayed hours to days
4. **Schema changes:** After ADD COLUMN, DROP COLUMN, or CREATE INDEX
5. **Performance incidents:** When queries suddenly slow or plans change unexpectedly

**Manual refresh priority matrix:**

| Scenario | Priority | Recommended Timing |
|----------|----------|-------------------|
| Bulk load >50% row change | URGENT | Immediately after load |
| Schema change (ADD COLUMN) | HIGH | Within 1 hour |
| Drift >30% detected | HIGH | Within 24 hours |
| Routine scheduled refresh | MEDIUM | During maintenance window |
| Exploratory analysis | LOW | Anytime (non-blocking) |

## Monitoring Statistics Health

### Cluster-Wide Statistics Age Report

```sql
WITH stats_summary AS (
  SELECT
    table_schema,
    table_name,
    created,
    now() - created AS stats_age,
    row_count
  FROM [SHOW STATISTICS FOR TABLE *.*]
  WHERE column_names = '{}'
)
SELECT
  CASE
    WHEN stats_age > INTERVAL '30 days' THEN 'Very stale (>30d)'
    WHEN stats_age > INTERVAL '14 days' THEN 'Stale (14-30d)'
    WHEN stats_age > INTERVAL '7 days' THEN 'Aging (7-14d)'
    ELSE 'Fresh (<7d)'
  END AS health_status,
  count(*) AS table_count,
  SUM(row_count) AS total_rows
FROM stats_summary
GROUP BY health_status
ORDER BY
  CASE health_status
    WHEN 'Very stale (>30d)' THEN 1
    WHEN 'Stale (14-30d)' THEN 2
    WHEN 'Aging (7-14d)' THEN 3
    ELSE 4
  END;
```

**Expected output:**
```
  health_status  | table_count | total_rows
-----------------+-------------+------------
 Fresh (<7d)    |         120 |   45000000
 Aging (7-14d)  |          15 |    2300000
 Stale (14-30d) |           5 |     500000
 Very stale (>30d) |        2 |      10000
```

**Interpretation:**
- **Fresh:** Healthy baseline, most tables should be here
- **Aging:** Monitor, may need manual refresh if workload changes
- **Stale:** Review individual tables, prioritize high-traffic ones
- **Very stale:** Urgent review required

### Drift Trend Analysis

```sql
-- Compare recent statistics history to detect drift trends
WITH stats_history AS (
  SELECT
    table_name,
    row_count,
    created,
    LAG(row_count) OVER (PARTITION BY table_name ORDER BY created) AS prev_row_count,
    LAG(created) OVER (PARTITION BY table_name ORDER BY created) AS prev_created
  FROM [SHOW STATISTICS FOR TABLE database_name.*]
  WHERE column_names = '{}'
)
SELECT
  table_name,
  row_count AS current_rows,
  prev_row_count AS previous_rows,
  created AS current_stats_ts,
  prev_created AS previous_stats_ts,
  created - prev_created AS time_between_refreshes,
  ROUND((row_count - prev_row_count)::NUMERIC / NULLIF(prev_row_count, 0) * 100, 2) AS growth_pct
FROM stats_history
WHERE prev_row_count IS NOT NULL
  AND created > now() - INTERVAL '30 days'  -- Recent history only
ORDER BY ABS(growth_pct) DESC
LIMIT 20;
```

**Use case:** Identify tables with rapid growth rates that may need more frequent refresh.

## Summary Checklist

Use this checklist to establish statistics refresh policies:

- [ ] **Classify workload type:** OLTP, OLAP, batch, real-time ingestion
- [ ] **Categorize table sizes:** Small, medium, large, very large
- [ ] **Set staleness thresholds:** Use matrix recommendations (adjust per workload)
- [ ] **Define drift tolerance:** Default 20-30%, lower for critical tables
- [ ] **Schedule manual refresh:** Post-bulk-load, weekly/monthly for large tables
- [ ] **Monitor automatic collection:** Verify `sql.stats.automatic_collection.enabled = true`
- [ ] **Tune collection threshold:** Adjust `fraction_stale_rows` if needed (default 0.2)
- [ ] **Identify multi-column candidates:** Correlated columns needing composite statistics
- [ ] **Establish maintenance windows:** Large tables (>10M rows) scheduled during low-traffic periods
- [ ] **Implement monitoring:** Cluster-wide health reports, drift trend analysis

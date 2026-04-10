---
name: auditing-table-statistics
description: Audits optimizer table statistics for staleness, missing coverage, and data quality issues using SHOW STATISTICS. Use when diagnosing poor query performance, unexpected plan changes, or after bulk data changes to identify stale statistics requiring refresh via CREATE STATISTICS.
compatibility: Requires SQL access with any privilege on target tables (SELECT, INSERT, UPDATE, DELETE, or admin). Uses SHOW STATISTICS (production-safe, read-only).
metadata:
  author: cockroachdb
  version: "1.0"
---

# Auditing Table Statistics

Audits optimizer table statistics for staleness, missing column coverage, and row count drift to diagnose poor query performance caused by outdated or incomplete statistics. Uses `SHOW STATISTICS` for read-only SQL analysis of table-level and column-level statistics freshness, entirely without requiring DB Console access.

**Complement to profiling-statement-fingerprints:** This skill diagnoses optimizer statistics issues; for identifying historically slow queries, see [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md).

## When to Use This Skill

- Query performance degrades after bulk INSERT, UPDATE, or DELETE operations
- EXPLAIN plans show unexpected full table scans or suboptimal join orders
- Plan instability: same query produces different execution plans over time
- After schema changes: ADD COLUMN, DROP COLUMN, or CREATE INDEX operations
- Tables experience >20-30% row count changes without statistics refresh
- SQL-only diagnostics needed without DB Console access
- Validating automatic statistics collection is working correctly

**For historical query analysis:** Use [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) to identify slow statement patterns.
**For live query triage:** Use [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) for immediate incident response.

## Prerequisites

- SQL connection to CockroachDB cluster
- **Privilege requirement:** Any privilege on target tables (SELECT, INSERT, UPDATE, DELETE, or admin role)
  - Much less restrictive than VIEWACTIVITY: any table access grants statistics visibility for that table
- Automatic statistics collection enabled (default): `sql.stats.automatic_collection.enabled = true`

**Check automatic collection status:**
```sql
SHOW CLUSTER SETTING sql.stats.automatic_collection.enabled;  -- Should return: true
```

**Verify table access:**
```sql
SHOW GRANTS ON TABLE database_name.table_name;
```

## Core Concepts

### What Are Table Statistics?

**Table statistics** provide the optimizer with data distribution information to estimate query costs:

| Statistic Type | Description | Impact on Optimizer |
|----------------|-------------|---------------------|
| **row_count** | Total rows in table | Cardinality estimates for full scans |
| **distinct_count** | Unique values per column | Selectivity estimates for WHERE/JOIN predicates |
| **null_count** | NULL values per column | IS NULL / IS NOT NULL predicate costs |
| **histogram** | Value distribution buckets | Range scan selectivity (e.g., `WHERE age BETWEEN 20 AND 30`) |

**Multi-column statistics** capture correlation between columns (e.g., city + state + zip) for more accurate multi-predicate estimates.

### Statistics Lifecycle

**Automatic collection (default):**
- Triggered when row count changes by ~20% since last statistics collection
- Runs as background job (non-blocking, but consumes resources)
- May be delayed for very large tables (>10M rows)

**Manual collection:**
- Explicit `CREATE STATISTICS` command for immediate refresh
- Required for multi-column statistics (automatic collection only creates single-column stats)
- Recommended after bulk data loads or significant schema changes

### Staleness Indicators

| Indicator | Definition | Recommended Action |
|-----------|------------|-------------------|
| **Age** | Time since last statistics collection | Refresh if >7 days (OLTP) or >30 days (OLAP) |
| **Row count drift** | Percent difference between current and cached row_count | Refresh if >20-30% drift detected |
| **Missing columns** | Columns without statistics | CREATE STATISTICS for frequently queried columns |
| **Missing histograms** | Columns without distribution data | Automatic collection handles; may need manual refresh |

See [references/statistics-thresholds.md](references/statistics-thresholds.md) for workload-specific threshold guidance.

### When Statistics Are Auto-Collected

**Default trigger:** ~20% row count change (controlled by `sql.stats.automatic_collection.fraction_stale_rows`)

**Collection schedule:**
- Small tables (<10K rows): Immediate
- Medium tables (10K-10M rows): Within minutes to hours
- Large tables (>10M rows): May be delayed hours to avoid resource contention

**Check pending jobs:**
```sql
SELECT job_id, description, status, fraction_completed
FROM [SHOW JOBS]
WHERE job_type = 'AUTO CREATE STATS'
  AND status IN ('pending', 'running')
ORDER BY created DESC
LIMIT 20;
```

## Core Diagnostic Queries

### Query 1: Identify Tables with Stale or Missing Statistics

Finds tables with outdated statistics or no statistics at all, ranked by staleness.

```sql
WITH table_stats AS (
  SELECT
    table_catalog,
    table_schema,
    table_name,
    column_names,
    row_count,
    created,
    now() - created AS stats_age
  FROM [SHOW STATISTICS FOR TABLE database_name.*]  -- Replace database_name
  WHERE column_names = '{}'  -- Table-level stats only (empty array)
)
SELECT
  table_schema || '.' || table_name AS full_table_name,
  row_count,
  created AS stats_created_at,
  stats_age,
  CASE
    WHEN created IS NULL THEN 'Missing statistics'
    WHEN stats_age > INTERVAL '30 days' THEN 'Very stale (>30d)'
    WHEN stats_age > INTERVAL '7 days' THEN 'Stale (>7d)'
    ELSE 'Fresh'
  END AS staleness_status
FROM table_stats
WHERE stats_age > INTERVAL '7 days' OR created IS NULL  -- Adjust threshold
ORDER BY stats_age DESC NULLS FIRST
LIMIT 50;
```

**Customization:**
- Replace `database_name.*` with specific schema pattern (e.g., `mydb.public.*`)
- Adjust staleness threshold: `INTERVAL '7 days'` for OLTP, `'30 days'` for OLAP
- Increase `LIMIT` to see more tables

**Key columns:**
- `staleness_status`: Quick classification of statistics freshness
- `stats_age`: Exact time since last collection
- `row_count`: Last known table size

### Query 2: Audit Statistics for Specific Table

Shows all statistics for a single table, including table-level and per-column details.

```sql
SELECT
  column_names,
  row_count,
  distinct_count,
  null_count,
  created,
  now() - created AS stats_age,
  CASE
    WHEN histogram_id IS NOT NULL THEN 'Yes'
    ELSE 'No'
  END AS has_histogram
FROM [SHOW STATISTICS FOR TABLE database_name.schema_name.table_name]
ORDER BY
  CASE WHEN column_names = '{}' THEN 0 ELSE 1 END,  -- Table-level first
  created DESC;
```

**Customization:**
- Replace `database_name.schema_name.table_name` with fully-qualified table name

**Key columns:**
- `column_names`: Empty `{}` = table-level, single element = column-level
- `distinct_count`: Cardinality for selectivity estimates
- `null_count`: NULL value count for IS NULL predicates
- `has_histogram`: Distribution data availability

**Interpretation:**
- First row (column_names = '{}') shows table-level row_count
- Subsequent rows show per-column statistics
- Missing columns indicate no statistics collected yet

### Query 3: Detect Row Count Drift

Compares current table row count against cached statistics to identify significant drift.

```sql
WITH current_count AS (
  SELECT count(*) AS actual_rows
  FROM database_name.schema_name.table_name  -- Replace with target table
),
stats_count AS (
  SELECT row_count, created
  FROM [SHOW STATISTICS FOR TABLE database_name.schema_name.table_name]
  WHERE column_names = '{}'  -- Table-level stats
  ORDER BY created DESC
  LIMIT 1
)
SELECT
  c.actual_rows,
  s.row_count AS stats_rows,
  s.created AS stats_created_at,
  now() - s.created AS stats_age,
  ABS(c.actual_rows - s.row_count) AS drift_absolute,
  ROUND(
    ABS(c.actual_rows - s.row_count)::NUMERIC /
    NULLIF(s.row_count, 0) * 100,
    2
  ) AS drift_pct,
  CASE
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.30 THEN 'High drift (>30%)'
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.20 THEN 'Medium drift (>20%)'
    WHEN ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) > 0.10 THEN 'Low drift (>10%)'
    ELSE 'Minimal drift (<10%)'
  END AS drift_status
FROM current_count c, stats_count s;
```

**Customization:**
- Replace table name in both CTEs
- Adjust drift thresholds (30%, 20%, 10%) based on workload tolerance

**Key columns:**
- `drift_pct`: Percentage difference between current and cached row count
- `drift_status`: Classification for prioritization
- `stats_age`: Time since statistics last refreshed

**Interpretation:**
- **>30% drift**: Urgent refresh recommended, optimizer estimates likely very inaccurate
- **20-30% drift**: Consider refresh if experiencing performance issues
- **10-20% drift**: Monitor for trends, may trigger automatic collection soon
- **<10% drift**: Normal variance, no action needed

### Query 4: Identify Missing Column-Level Statistics

Finds table columns without statistics, focusing on columns frequently used in WHERE/JOIN clauses.

```sql
WITH table_columns AS (
  SELECT column_name
  FROM information_schema.columns
  WHERE table_schema = 'schema_name'  -- Replace
    AND table_name = 'table_name'    -- Replace
    AND is_hidden = 'NO'             -- Exclude internal columns
),
stats_columns AS (
  SELECT UNNEST(column_names) AS column_name
  FROM [SHOW STATISTICS FOR TABLE database_name.schema_name.table_name]
  WHERE column_names != '{}'  -- Exclude table-level stats
)
SELECT
  tc.column_name AS missing_column,
  'No statistics available' AS status
FROM table_columns tc
WHERE tc.column_name NOT IN (SELECT column_name FROM stats_columns)
ORDER BY tc.column_name;
```

**Customization:**
- Replace schema_name, table_name, and database_name with target table

**Interpretation:**
- Columns returned have no optimizer statistics
- Prioritize creating statistics for columns used in:
  - WHERE clause predicates (`WHERE user_id = 123`)
  - JOIN conditions (`JOIN orders ON users.id = orders.user_id`)
  - GROUP BY / ORDER BY expressions

**Action:** Generate CREATE STATISTICS commands (see Query 7)

### Query 5: Histogram Coverage Analysis

Identifies columns with/without histogram data for range query optimization.

```sql
SELECT
  UNNEST(column_names) AS column_name,
  created,
  now() - created AS stats_age,
  CASE
    WHEN histogram_id IS NOT NULL THEN 'Has histogram'
    ELSE 'Missing histogram'
  END AS histogram_status
FROM [SHOW STATISTICS FOR TABLE database_name.schema_name.table_name]
WHERE column_names != '{}'  -- Exclude table-level stats
ORDER BY
  CASE WHEN histogram_id IS NULL THEN 0 ELSE 1 END,  -- Missing first
  created DESC;
```

**Customization:**
- Replace database_name.schema_name.table_name

**Key columns:**
- `histogram_status`: Indicates distribution data availability
- `stats_age`: Time since histogram last updated

**Interpretation:**
- **Has histogram**: Optimizer can estimate range scan selectivity (BETWEEN, >, <)
- **Missing histogram**: Optimizer uses uniform distribution assumption (less accurate)
- Automatic collection creates histograms; missing indicates very new column or disabled collection

### Query 6: Multi-Column Statistics Detection

Identifies existing multi-column (composite) statistics for correlated columns.

```sql
SELECT
  column_names,
  created,
  now() - created AS stats_age,
  row_count,
  ARRAY_LENGTH(column_names, 1) AS column_count
FROM [SHOW STATISTICS FOR TABLE database_name.schema_name.table_name]
WHERE ARRAY_LENGTH(column_names, 1) > 1  -- Multi-column only
ORDER BY created DESC;
```

**Customization:**
- Replace database_name.schema_name.table_name

**Key columns:**
- `column_names`: Array of correlated columns
- `column_count`: Number of columns in composite statistic

**Interpretation:**
- **Present**: Manual multi-column statistics exist (automatic collection only creates single-column)
- **Absent**: May need manual creation for correlated columns (e.g., city + state + zip)
- Common use case: Composite index columns that are queried together

See [references/create-statistics-examples.md](references/create-statistics-examples.md) for multi-column creation patterns.

### Query 7: Generate CREATE STATISTICS Recommendations

Produces ready-to-run CREATE STATISTICS commands for tables with stale or missing statistics.

```sql
WITH stale_tables AS (
  SELECT
    table_schema,
    table_name,
    created,
    now() - created AS stats_age
  FROM [SHOW STATISTICS FOR TABLE database_name.*]
  WHERE column_names = '{}'
    AND (created IS NULL OR now() - created > INTERVAL '7 days')  -- Adjust threshold
)
SELECT
  table_schema || '.' || table_name AS full_table_name,
  stats_age,
  'CREATE STATISTICS __auto__ FROM ' || table_schema || '.' || table_name || ';' AS create_command
FROM stale_tables
ORDER BY stats_age DESC NULLS FIRST
LIMIT 50;
```

**Customization:**
- Replace `database_name.*` with schema pattern
- Adjust `INTERVAL '7 days'` staleness threshold
- Increase `LIMIT` for more recommendations

**Output:**
- `create_command`: Copy-paste ready SQL command
- `__auto__`: Uses automatic column selection (recommended default)

**Execution:**
- Review generated commands before execution
- Run during low-traffic periods for large tables (>10M rows)
- Monitor job progress (see Query 6 for job monitoring)

## Common Workflows

### Workflow 1: Post-Bulk-Load Statistics Audit

**Scenario:** After bulk INSERT/COPY/IMPORT operation, validate statistics are current.

**Steps:**

1. **Identify affected tables:**
   ```sql
   -- List tables modified in last 24 hours
   SELECT DISTINCT table_schema || '.' || table_name AS full_table_name
   FROM [SHOW TABLES]
   WHERE table_schema = 'target_schema';  -- Replace
   ```

2. **Check row count drift (Query 3):**
   Run drift detection query for each affected table.

3. **Generate and execute refresh commands (Query 7):**
   ```sql
   CREATE STATISTICS __auto__ FROM schema_name.table_name;  -- From Query 7 output
   ```

4. **Monitor collection job:**
   ```sql
   SELECT job_id, status, fraction_completed, running_status
   FROM [SHOW JOBS]
   WHERE job_type = 'CREATE STATS'
     AND created > now() - INTERVAL '1 hour'
   ORDER BY created DESC
   LIMIT 10;
   ```

5. **Verify refresh (Query 2):**
   Re-run statistics audit to confirm `created` timestamp updated.

**Expected outcome:** Statistics age <1 hour, drift_pct <5%.

### Workflow 2: Diagnose Unexpected Query Plan Changes

**Scenario:** Query performance suddenly degrades; EXPLAIN shows different plan.

**Steps:**

1. **Identify affected query from [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md):**
   Find query with latency spike or plan hash change.

2. **Extract table references:**
   Parse query text to identify tables in FROM/JOIN clauses.

3. **Audit statistics for each table (Query 2):**
   Check staleness and row count currency.

4. **Compare historical vs current row counts:**
   ```sql
   -- Example: Check if table grew significantly
   SELECT row_count, created
   FROM [SHOW STATISTICS FOR TABLE users]
   WHERE column_names = '{}'
   ORDER BY created DESC
   LIMIT 5;  -- Last 5 collections
   ```

5. **Refresh stale statistics (Query 7):**
   Execute CREATE STATISTICS for tables with high drift.

6. **Validate plan stability:**
   Re-run EXPLAIN to verify plan returns to expected structure.

**Expected outcome:** Plan hash stabilizes, latency returns to baseline after statistics refresh.

### Workflow 3: Routine Statistics Health Check

**Scenario:** Periodic audit to proactively identify statistics issues before performance degrades.

**Steps:**

1. **Run cluster-wide staleness scan (Query 1):**
   ```sql
   -- All databases
   SHOW STATISTICS FOR TABLE *.*;  -- Warning: May be slow on large clusters
   ```

2. **Prioritize critical tables:**
   Focus on high-traffic tables from [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md).

3. **Check automatic collection is enabled:**
   ```sql
   SHOW CLUSTER SETTING sql.stats.automatic_collection.enabled;  -- Should be true
   ```

4. **Review pending auto-collection jobs:**
   ```sql
   SELECT job_id, description, status, fraction_completed
   FROM [SHOW JOBS]
   WHERE job_type = 'AUTO CREATE STATS'
     AND status IN ('pending', 'running')
   ORDER BY created DESC;
   ```

5. **Generate batch refresh script (Query 7):**
   Save output to file for scheduled execution.

6. **Schedule refresh during maintenance window:**
   Execute generated CREATE STATISTICS commands during low-traffic period.

**Frequency:** Weekly for OLTP, monthly for OLAP.

## Safety Considerations

### Production-Safe Operations

**SHOW STATISTICS:**
- **Impact:** Read-only, no cluster impact
- **Safe for production:** Yes, run anytime without restrictions

**CREATE STATISTICS:**
- **Impact:** CPU/IO-intensive, non-blocking table scans
- **Safety:**
  - Does NOT lock table or block writes
  - Consumes resources (CPU, network, disk I/O)
  - May impact query performance during collection on large tables
- **Best practices:**
  - Run during low-traffic periods for tables >10M rows
  - Stagger execution (avoid creating statistics on many tables simultaneously)
  - Monitor job progress and resource utilization

### Resource Consumption

**Small tables (<10K rows):** Negligible impact, safe anytime

**Medium tables (10K-10M rows):** Seconds to minutes, minor impact

**Large tables (>10M rows):** Minutes to hours, plan accordingly:
- Schedule during maintenance windows
- Monitor cluster metrics (CPU, disk I/O) during collection
- Use `SHOW JOBS` to track progress

**Cancellation (if needed):**
```sql
-- Find job ID
SELECT job_id, status, fraction_completed
FROM [SHOW JOBS]
WHERE job_type = 'CREATE STATS' AND status = 'running';

-- Cancel job (non-destructive, existing statistics remain)
CANCEL JOB 123456789012345678;
```

### Batch Collection Best Practices

**Avoid overwhelming cluster:**
- Collect statistics for 3-5 tables concurrently maximum
- Wait for completion before starting next batch
- Monitor cluster health metrics between batches

**Example staggered script:**
```bash
# Collect statistics in batches with delays
for table in table1 table2 table3; do
  cockroach sql -e "CREATE STATISTICS __auto__ FROM $table;" &
done
wait  # Wait for batch to complete

sleep 60  # Delay between batches

for table in table4 table5 table6; do
  cockroach sql -e "CREATE STATISTICS __auto__ FROM $table;" &
done
wait
```

See [references/create-statistics-examples.md](references/create-statistics-examples.md) for detailed batch patterns.

## Troubleshooting

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| **SHOW STATISTICS returns empty** | No statistics ever collected | Run `CREATE STATISTICS __auto__ FROM table_name;` |
| **row_count shows 0 for non-empty table** | Statistics out of sync | Refresh: `CREATE STATISTICS __auto__ FROM table_name;` |
| **Permission denied error** | No privileges on table | Grant any privilege: `GRANT SELECT ON table_name TO user;` |
| **CREATE STATISTICS job stuck** | Large table with high write volume | Check `SHOW JOBS` status; consider `CANCEL JOB` and retry during low-traffic period |
| **Automatic collection not triggering** | Setting disabled or threshold not met | Verify `sql.stats.automatic_collection.enabled = true` and check row count drift |
| **Statistics exist but query plans still poor** | Stale statistics or missing multi-column stats | Refresh existing; create multi-column for correlated columns (see Query 6) |
| **High drift but recent created timestamp** | Extreme write volume between collections | Lower automatic collection threshold or increase manual refresh frequency |

### Defensive Query Patterns

**Handle missing statistics:**
```sql
-- Use COALESCE for NULL created timestamps
SELECT COALESCE(created, '1970-01-01'::TIMESTAMP) AS stats_created_at
FROM [SHOW STATISTICS FOR TABLE table_name]
WHERE column_names = '{}';
```

**Avoid division by zero in drift calculations:**
```sql
-- Use NULLIF to prevent divide-by-zero errors
SELECT
  ABS(actual - stats)::NUMERIC / NULLIF(stats, 0) * 100 AS drift_pct
FROM ...;
```

## Key Considerations

### Automatic vs Manual Collection

**Automatic (default):**
- **Pros:** Zero maintenance, adapts to data changes, covers all single columns
- **Cons:** May lag for very large tables, no multi-column statistics
- **Recommendation:** Keep enabled for baseline coverage

**Manual:**
- **Pros:** Immediate refresh, supports multi-column statistics, controlled timing
- **Cons:** Requires monitoring and operational overhead
- **Recommendation:** Use for critical tables, correlated columns, post-bulk-load scenarios

### Statistics Retention

**Default retention:** Controlled by `sql.stats.persisted_rows.max` (default ~10 million rows across cluster)
- Older statistics are pruned automatically
- Typically 7-30 days of history retained depending on statistics volume

**Historical analysis:**
```sql
-- View statistics history for a table
SELECT column_names, row_count, created
FROM [SHOW STATISTICS FOR TABLE table_name]
WHERE column_names = '{}'
ORDER BY created DESC
LIMIT 10;  -- Last 10 collections
```

### Histogram Limitations

**What histograms optimize:**
- Range queries: `WHERE age BETWEEN 20 AND 30`
- Inequality predicates: `WHERE price > 100`
- ORDER BY selectivity: `ORDER BY created_at LIMIT 10`

**What histograms don't optimize:**
- Exact equality: `WHERE id = 123` (uses distinct_count instead)
- Multi-column predicates: Requires multi-column statistics
- Very sparse columns: Histograms may be ineffective for highly skewed distributions

### Multi-Column Statistics

**When to create:**
- Columns frequently queried together in WHERE clauses
- Composite index columns with correlated values
- Geographic columns (city + state + zip)
- Time-based partitioning columns (year + month)

**Creation:**
```sql
-- Example: Correlated columns
CREATE STATISTICS city_state_stats ON city, state FROM addresses;
```

**Limitation:** Only manual creation (automatic collection does NOT create multi-column statistics)

See [references/create-statistics-examples.md](references/create-statistics-examples.md) for comprehensive patterns.

### Performance Impact Mitigation

**Large table strategies:**
- Schedule during maintenance windows (nights/weekends)
- Use database-specific batching (one database at a time)
- Monitor cluster metrics: CPU, disk I/O, network saturation
- Consider `AS OF SYSTEM TIME` for historical analysis without impacting live traffic

**Resource monitoring during collection:**
```sql
-- Check running statistics jobs
SELECT job_id, description, status, fraction_completed, running_status
FROM [SHOW JOBS]
WHERE job_type IN ('CREATE STATS', 'AUTO CREATE STATS')
  AND status = 'running';
```

### Staleness Threshold Tuning

**OLTP workloads:**
- **Recommended refresh:** 3-7 days
- **Rationale:** Frequent updates, query patterns change rapidly

**OLAP/Analytics workloads:**
- **Recommended refresh:** 14-30 days
- **Rationale:** Batch-oriented, stable query patterns

**Hybrid workloads:**
- Critical tables: 3-7 days
- Archive/historical tables: 30+ days

See [references/statistics-thresholds.md](references/statistics-thresholds.md) for detailed guidance.

### Privilege Requirements

**Required:** Any privilege on table (SELECT, INSERT, UPDATE, DELETE, or admin role)

**Comparison to other diagnostics:**
- **Less restrictive than:** VIEWACTIVITY (required for statement_statistics)
- **More restrictive than:** Public cluster settings

**Grant example:**
```sql
-- Grant SELECT (least privileged) for statistics visibility
GRANT SELECT ON TABLE database_name.table_name TO diagnostics_user;
```

## References

**Official CockroachDB Documentation:**
- [SHOW STATISTICS](https://www.cockroachlabs.com/docs/stable/show-statistics.html) - Complete syntax and output schema
- [CREATE STATISTICS](https://www.cockroachlabs.com/docs/stable/create-statistics.html) - Manual statistics collection guide
- [Cost-Based Optimizer](https://www.cockroachlabs.com/docs/stable/cost-based-optimizer.html) - How optimizer uses statistics
- [Table Statistics](https://www.cockroachlabs.com/docs/stable/cost-based-optimizer.html#table-statistics) - Statistics impact on query planning
- [SHOW JOBS](https://www.cockroachlabs.com/docs/stable/show-jobs.html) - Job monitoring and management

**Related Skills:**
- [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) - Identify slow query patterns
- [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) - Real-time query triage

**Supplementary References:**
- [Statistics Thresholds Guide](references/statistics-thresholds.md) - Workload-specific staleness and drift thresholds
- [CREATE STATISTICS Examples](references/create-statistics-examples.md) - Comprehensive collection patterns and batch strategies

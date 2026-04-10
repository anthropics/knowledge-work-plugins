---
name: analyzing-schema-change-storage-risk
description: Estimates storage requirements for CockroachDB schema change backfills by analyzing per-index range sizes using SHOW RANGES WITH DETAILS and applying the 3× free space rule. Use when planning CREATE INDEX, ADD COLUMN, or ALTER PRIMARY KEY operations on large tables to avoid disk exhaustion during backfill.
compatibility: Requires SQL access with admin role or ZONECONFIG system privilege. DETAILS option is expensive; use only on targeted large tables. CockroachDB requires 3× the largest range size as free storage during backfill operations.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Analyzing Schema Change Storage Risk

Estimates storage requirements for CockroachDB schema change backfills by analyzing per-index range sizes and applying the 3× free space rule. Uses `SHOW RANGES WITH DETAILS` to calculate worst-case disk usage for `CREATE INDEX`, `ADD COLUMN`, and `ALTER PRIMARY KEY` operations, preventing mid-backfill disk exhaustion.

**Complement to range distribution analysis:** This skill focuses on pre-DDL capacity planning; for ongoing range health monitoring, see [analyzing-range-distribution](../analyzing-range-distribution/SKILL.md).

## When to Use This Skill

- Estimate storage needs before CREATE INDEX on large tables (100GB+)
- Validate capacity before ADD COLUMN backfills with computed/default values
- Pre-flight checks for ALTER PRIMARY KEY operations (full table rewrite)
- Avoid mid-backfill disk exhaustion errors causing schema change failures
- Multi-index planning: prioritize index creation by storage impact
- Capacity planning for batch DDL operations
- SQL-only storage estimation without DB Console access

**For range-level monitoring:** Use [analyzing-range-distribution](../analyzing-range-distribution/SKILL.md) to analyze range count, leaseholder placement, and fragmentation patterns.

## Prerequisites

- SQL connection to CockroachDB cluster
- Admin role OR `ZONECONFIG` system privilege
- Understanding of online schema change architecture (backfill process, MVCC)
- Knowledge of current cluster free disk space (check monitoring or `crdb_internal.kv_store_status`)
- Target table must have existing data (empty tables = zero storage risk)

**Check your privileges:**
```sql
SHOW GRANTS ON SYSTEM FOR current_user;  -- Should show admin or ZONECONFIG
```

**Check cluster free disk space:**
```sql
SELECT
  node_id,
  store_id,
  ROUND((capacity - used) / 1073741824.0, 2) AS free_gb,
  ROUND((used::FLOAT / capacity) * 100, 2) AS disk_usage_pct
FROM crdb_internal.kv_store_status
ORDER BY disk_usage_pct DESC;
```

See [permissions reference](references/permissions.md) for RBAC setup (shared with analyzing-range-distribution).

## Core Concepts

### The 3× Storage Rule

**Rule:** CockroachDB requires **3× the largest range size** as free disk space during schema change backfills.

**Why 3×?**
1. **Existing data (1×):** Original table/index data remains during backfill
2. **New backfill data (1×):** New index or column data written during online schema change
3. **MVCC versioning overhead (1×):** Multiple versions during compaction, garbage collection lag

**Critical:** The rule applies to the **largest single range**, not average range size or total table size.

**Example:**
- Table has 100GB total size, 1500 ranges
- Largest range = 80MB
- Required free space = 3 × 80MB = 240MB (per node with replica)

### Schema Change Backfill Process

**Online schema change phases:**
1. **Backfill:** Populate new index/column in background (bulk writes)
2. **Validation:** Verify new index matches existing data
3. **Swap:** Atomically make schema change visible
4. **Cleanup:** Delete old index/column data (GC later)

**Storage peak:** During backfill (phases 1-2), both old and new data exist simultaneously.

**Backfill pause behavior:** CockroachDB pauses backfills if disk usage exceeds `kv.range_split.by_load_enabled` threshold (~85% by default), preventing disk exhaustion but causing schema change delays.

### Per-Index Storage Calculation

**Why per-index?** Each index is backed by separate ranges with different sizes.

**Example table schema:**
```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  customer_id UUID,
  created_at TIMESTAMP,
  total DECIMAL(10,2),
  INDEX idx_customer (customer_id),
  INDEX idx_created (created_at)
);
```

**Storage breakdown:**
- Primary index (`id`): 500GB, largest range 75MB → 225MB required
- `idx_customer`: 150GB, largest range 60MB → 180MB required
- `idx_created`: 200GB, largest range 90MB → **270MB required** (largest)

**Conclusion:** New index creation requires **270MB free space** (worst case from `idx_created`'s largest range).

### SHOW RANGES WITH DETAILS Safety

**CRITICAL WARNING:** The `WITH DETAILS` option computes `span_stats` on-demand, causing:
- **High CPU usage** from statistics computation
- **Memory overhead** proportional to range count
- **Query timeouts** on tables with 1000s of ranges without LIMIT

**Mandatory guardrails:**
1. **LIMIT clause:** Default 50-100 for exploratory analysis
2. **Specific table targeting:** Use `FROM TABLE table_name`, never cluster-wide
3. **Production timing:** Run during maintenance windows or low-traffic periods
4. **Pre-check range count:** Run basic `SHOW RANGES` first to assess table size

See [analyzing-range-distribution safety section](../analyzing-range-distribution/SKILL.md#safety-considerations) for detailed guardrails.

## Core Diagnostic Queries

### Query 1: Total Table Storage (All Indexes)

```sql
-- Estimate total table storage across all indexes
SELECT
  table_name,
  index_name,
  COUNT(*) AS range_count,
  ROUND(SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0, 2) AS total_size_gb,
  ROUND(AVG((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0, 2) AS avg_range_size_mb
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
GROUP BY table_name, index_name
ORDER BY total_size_gb DESC;
```

**Output:**
- `total_size_gb`: Total storage per index
- `avg_range_size_mb`: Average range size (not used for 3× rule, but useful for fragmentation context)

**Interpretation:** High total size (100GB+) indicates CREATE INDEX will have significant storage impact.

**CRITICAL:** Aggregates DETAILS data across all ranges. Use only on targeted tables, never cluster-wide.

---

### Query 2: Largest Range Size per Index (Critical for 3× Rule)

```sql
-- Find largest range per index (determines 3× storage requirement)
SELECT
  table_name,
  index_name,
  MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_range_mb,
  ROUND((MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0) * 3, 2) AS required_free_space_mb
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
GROUP BY table_name, index_name
ORDER BY largest_range_mb DESC;
```

**Output:**
- `largest_range_mb`: Size of largest range in index
- `required_free_space_mb`: 3× the largest range (minimum free space needed)

**Interpretation:**
- `largest_range_mb > 64`: Range exceeds default split threshold (may indicate split lag or custom `range_max_bytes`)
- `required_free_space_mb`: Compare with cluster free space (Query from Prerequisites)

**Use case:** Determine worst-case storage requirement before CREATE INDEX.

**CRITICAL:** Uses DETAILS with aggregation. Limit to specific tables only.

---

### Query 3: Storage Safety Calculation (Decision Logic)

```sql
-- Combined query: compare required storage vs. available capacity
WITH range_requirements AS (
  SELECT
    table_name,
    index_name,
    MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_range_mb,
    ROUND((MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0) * 3, 2) AS required_free_mb_3x,
    ROUND((MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0) * 4, 2) AS required_free_mb_4x
  FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
  GROUP BY table_name, index_name
),
cluster_capacity AS (
  SELECT
    MIN((capacity - used) / 1048576.0) AS min_free_mb  -- Minimum free space across all nodes
  FROM crdb_internal.kv_store_status
)
SELECT
  rr.table_name,
  rr.index_name,
  rr.largest_range_mb,
  rr.required_free_mb_3x AS required_3x,
  rr.required_free_mb_4x AS required_4x_recommended,
  cc.min_free_mb AS cluster_min_free_mb,
  CASE
    WHEN cc.min_free_mb >= rr.required_free_mb_4x THEN 'SAFE (4× margin)'
    WHEN cc.min_free_mb >= rr.required_free_mb_3x THEN 'MARGINAL (3× only, add capacity recommended)'
    ELSE 'UNSAFE (insufficient space, add capacity required)'
  END AS risk_assessment
FROM range_requirements rr
CROSS JOIN cluster_capacity cc
ORDER BY rr.largest_range_mb DESC;
```

**Output:**
- `required_3x`: Minimum free space (3× largest range)
- `required_4x_recommended`: Recommended free space (4× for production safety margin)
- `cluster_min_free_mb`: Minimum free space across all nodes
- `risk_assessment`: SAFE / MARGINAL / UNSAFE

**Decision matrix:**
- **SAFE:** Proceed with schema change
- **MARGINAL:** Proceed with caution, monitor disk usage closely during backfill
- **UNSAFE:** Add capacity before proceeding (or drop unused indexes first)

**CRITICAL:** Uses DETAILS and joins with cluster capacity. Run on targeted tables only.

---

### Query 4: Multi-Index Comparison (Prioritization)

```sql
-- Compare storage requirements across multiple existing indexes
-- Use case: Planning to create index on table with 3+ existing indexes
SELECT
  index_name,
  COUNT(*) AS range_count,
  ROUND(SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0, 2) AS total_size_gb,
  MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_range_mb,
  ROUND((MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0) * 3, 2) AS required_free_mb
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
GROUP BY index_name
ORDER BY required_free_mb DESC;
```

**Use case:** Identify which existing index has largest range (determines worst-case for new index creation).

**Interpretation:**
- New index will likely have similar largest range as largest existing index
- Use worst-case (highest `required_free_mb`) for capacity planning

**Example scenario:**
- Table has 3 indexes: primary (50MB largest), idx_a (70MB largest), idx_b (90MB largest)
- Creating 4th index: assume 90MB largest range → 270MB required free space

**CRITICAL:** Aggregates DETAILS across all indexes. Use only on specific tables.

See [storage-calculations reference](references/storage-calculations.md) for detailed examples and decision trees.

## Storage Calculation Workflows

### Workflow 1: Single-Index Backfill Estimation

**Scenario:** Planning CREATE INDEX on large table (e.g., 200GB table, adding idx_customer).

**Steps:**
1. **Check current free disk space:** Run cluster capacity query (Prerequisites section)
2. **Find largest range in existing indexes:** Run Query 2 on target table
3. **Calculate 3× requirement:** Multiply largest range by 3 (or 4 for production margin)
4. **Compare required vs. available:** Use Query 3 decision logic
5. **Execute or defer:** Proceed if SAFE, add capacity if UNSAFE

**Example walkthrough:**
```sql
-- 1. Check free space (run first)
SELECT MIN((capacity - used) / 1073741824.0) AS min_free_gb
FROM crdb_internal.kv_store_status;
-- Result: 150GB minimum free

-- 2. Find largest range
SELECT MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_mb
FROM [SHOW RANGES FROM TABLE orders WITH DETAILS];
-- Result: 75MB largest range

-- 3. Calculate requirement
-- 3× = 225MB, 4× = 300MB

-- 4. Decision
-- 150GB free >> 300MB required → SAFE, proceed with CREATE INDEX
```

---

### Workflow 2: Multi-Index Backfill Planning

**Scenario:** Planning to create 3 new indexes on same table sequentially.

**Steps:**
1. **Analyze existing indexes:** Run Query 4 to compare storage profiles
2. **Estimate new index sizes:** Assume similar to largest existing index (conservative)
3. **Prioritize by impact:** Create smaller indexes first (faster backfill, less risk)
4. **Monitor between operations:** Check disk usage after each CREATE INDEX before starting next

**Example:**
```sql
-- Analyze existing indexes
SELECT index_name, MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_mb
FROM [SHOW RANGES FROM TABLE products WITH DETAILS]
GROUP BY index_name;

-- Results:
-- primary: 80MB → 240MB required
-- idx_category: 60MB → 180MB required
-- idx_supplier: 90MB → 270MB required (worst case)

-- Plan: Assume new indexes will have 90MB largest range → 270MB each
-- Create indexes sequentially, monitor disk after each
```

---

### Workflow 3: Capacity Validation Before ALTER PRIMARY KEY

**Scenario:** Changing primary key (full table rewrite, highest storage risk).

**Steps:**
1. **Understand scope:** ALTER PRIMARY KEY rewrites entire table (all indexes)
2. **Calculate total storage:** Sum all index sizes (Query 1)
3. **Find worst-case range:** Largest range across all indexes (Query 2)
4. **Apply 3× rule conservatively:** Use 4× multiplier for ALTER PRIMARY KEY operations
5. **Validate capacity:** Ensure 4× largest range available, plus buffer for MVCC overhead

**CRITICAL:** ALTER PRIMARY KEY is highest-risk DDL for storage exhaustion. Always use 4× multiplier.

**Example:**
```sql
-- Total table size
SELECT SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0 AS total_gb
FROM [SHOW RANGES FROM TABLE critical_table WITH DETAILS];
-- Result: 500GB

-- Largest range across all indexes
SELECT MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_mb
FROM [SHOW RANGES FROM TABLE critical_table WITH DETAILS];
-- Result: 100MB

-- Requirement: 4× 100MB = 400MB minimum
-- Recommendation: Add 20% buffer → 480MB recommended free space per node
```

---

## Safety Considerations

### DETAILS Option Performance Impact

**Resource usage:**
- **CPU:** Computes span statistics on-demand (aggregates across KV layer)
- **Memory:** Proportional to range count returned
- **Timeout risk:** Tables with 5000+ ranges may timeout without LIMIT

**Mitigation strategies:**
1. **Pre-check range count:** Run `SELECT COUNT(*) FROM [SHOW RANGES FROM TABLE t]` first
2. **Use LIMIT for exploration:** Start with `LIMIT 100`, remove only if needed
3. **Target specific tables:** Never run cluster-wide `SHOW RANGES WITH DETAILS`
4. **Production timing:** Schedule during maintenance windows for large tables
5. **Incremental analysis:** Analyze per-index if table has many indexes

See [analyzing-range-distribution safety section](../analyzing-range-distribution/SKILL.md#safety-considerations) for complete guardrails.

---

### Production Best Practices

**Margin of safety:**
- **Minimum (3×):** Theoretical minimum, use only in non-production
- **Recommended (4×):** Production standard, accounts for MVCC spikes, GC lag
- **Conservative (5×):** High-stakes tables (financial, compliance), or during high-traffic periods

**Monitoring during backfill:**
```sql
-- Monitor disk usage every 5 minutes during schema change
SELECT
  node_id,
  store_id,
  ROUND((used::FLOAT / capacity) * 100, 2) AS disk_usage_pct
FROM crdb_internal.kv_store_status
ORDER BY disk_usage_pct DESC;
```

**Backfill pause detection:**
```sql
-- Check for paused schema changes
SELECT
  job_id,
  job_type,
  description,
  status,
  fraction_completed
FROM crdb_internal.jobs
WHERE job_type = 'SCHEMA CHANGE' AND status = 'paused';
```

**If paused:** Backfill hit disk threshold. Add capacity or drop unused indexes to free space.

---

### Pre-Execution Checklist

Before running CREATE INDEX / ADD COLUMN / ALTER PRIMARY KEY:

- [ ] Run Query 3 to calculate storage safety (SAFE / MARGINAL / UNSAFE)
- [ ] Verify 4× margin available (not just 3×) for production tables
- [ ] Check for unused indexes to drop (frees space immediately)
- [ ] Schedule during maintenance window or low-traffic period
- [ ] Set up disk usage monitoring alerts (85% threshold)
- [ ] Prepare rollback plan (schema change cancellation steps)
- [ ] Validate table statistics are up-to-date (`SHOW STATISTICS FOR TABLE t`)

**If UNSAFE:** Add capacity first (scale cluster) or drop unused indexes.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Query timeout with DETAILS | Too many ranges, no LIMIT | Add `LIMIT 100`, target specific index |
| Zero `approximate_disk_bytes` | Empty table or statistics lag | Run `CREATE STATISTICS` or wait for auto-stats collection |
| Unexpected high storage values | Includes MVCC versions, old data | Normal; use `live_bytes` for current data estimate |
| Permission denied | Missing ZONECONFIG or admin privilege | Grant ZONECONFIG: `GRANT SYSTEM ZONECONFIG TO user` |
| `min_free_mb` shows negative value | Disk usage > capacity (critical!) | Immediate capacity expansion required |
| Backfill paused mid-operation | Disk usage exceeded threshold | Add capacity, or drop unused indexes to free space |
| Different values between nodes | Non-uniform data distribution | Use MIN(free space) for worst-case planning |
| Largest range > 512MB | Custom `range_max_bytes` or split lag | Investigate zone config; 3× rule still applies |

---

## Key Considerations

- **3× rule applies to largest range, not average:** Always use MAX(range size), not AVG
- **Per-index analysis:** Each index has different range sizes; use worst-case
- **4× for production:** Conservative margin accounts for MVCC spikes, GC lag
- **ALTER PRIMARY KEY = highest risk:** Full table rewrite, use 4-5× multiplier
- **Empty tables have zero risk:** Storage estimation only applies to tables with data
- **DETAILS option is expensive:** Always use LIMIT, target specific tables
- **Backfill pauses automatically:** CockroachDB prevents disk exhaustion by pausing, but delays schema changes
- **Monitor during execution:** Check disk usage every 5-10 minutes during long backfills
- **Statistics accuracy:** `approximate_disk_bytes` includes MVCC overhead; use for conservative estimates

---

## References

**Skill references:**
- [Detailed storage calculations and examples](references/storage-calculations.md)
- [RBAC and privileges setup](references/permissions.md) (shared with analyzing-range-distribution)

**Official CockroachDB Documentation:**
- [Online Schema Changes](https://www.cockroachlabs.com/docs/stable/online-schema-changes.html)
- [SHOW RANGES](https://www.cockroachlabs.com/docs/stable/show-ranges.html)
- [CREATE INDEX](https://www.cockroachlabs.com/docs/stable/create-index.html)
- [ALTER TABLE](https://www.cockroachlabs.com/docs/stable/alter-table.html)
- [Architecture: Storage Layer](https://www.cockroachlabs.com/docs/stable/architecture/storage-layer.html)
- [ZONECONFIG privilege](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

**Related skills:**
- [analyzing-range-distribution](../analyzing-range-distribution/SKILL.md) - For ongoing range health monitoring and leaseholder analysis
- [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) - For query performance analysis
- [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) - For real-time query triage

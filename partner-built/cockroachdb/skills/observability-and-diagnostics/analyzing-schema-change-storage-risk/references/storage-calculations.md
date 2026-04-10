# Storage Calculation Examples for Schema Change Backfills

This reference provides detailed examples, decision trees, and calculation walkthroughs for estimating storage requirements using the 3× rule for CockroachDB schema change operations.

## Table of Contents

1. [The 3× Storage Rule Explained](#the-3-storage-rule-explained)
2. [Example 1: Single Index Creation (Simple)](#example-1-single-index-creation-simple)
3. [Example 2: Multi-Index Table Analysis](#example-2-multi-index-table-analysis)
4. [Example 3: ALTER PRIMARY KEY (High Risk)](#example-3-alter-primary-key-high-risk)
5. [Example 4: ADD COLUMN with Default Value](#example-4-add-column-with-default-value)
6. [Decision Trees](#decision-trees)
7. [Safety Margins: 3× vs 4× vs 5×](#safety-margins-3-vs-4-vs-5)
8. [Common Calculation Mistakes](#common-calculation-mistakes)

---

## The 3× Storage Rule Explained

### Why 3×?

CockroachDB's online schema changes create temporary storage overhead during backfill operations. The 3× multiplier accounts for:

1. **Existing data (1×):** Original table/index data remains accessible during backfill
2. **New backfill data (1×):** New index or column data written in background
3. **MVCC versioning overhead (1×):** Multiple versions exist during compaction, GC lag before old versions deleted

### Key Insight: Largest Range, Not Total Size

**CRITICAL:** The rule applies to the **largest single range**, not average range size or total table size.

**Why?** During backfill, individual ranges split when they approach the split threshold. The largest range determines worst-case storage spike before split occurs.

**Example:**
- Table: 500GB total, 5000 ranges
- Average range size: 100MB
- Largest range: 150MB
- **Required free space: 3 × 150MB = 450MB** (NOT 3 × 100MB)

### Formula

```
Required Free Space = Largest Range Size × Multiplier
```

**Multiplier choices:**
- **3×:** Minimum (theoretical)
- **4×:** Recommended (production standard)
- **5×:** Conservative (high-stakes tables)

---

## Example 1: Single Index Creation (Simple)

### Scenario

**Table:** `users` (300GB, 3 existing indexes)
**Operation:** `CREATE INDEX idx_email ON users(email)`
**Goal:** Estimate storage requirement before execution

---

### Step 1: Check Current Cluster Capacity

```sql
SELECT
  node_id,
  ROUND((capacity - used) / 1073741824.0, 2) AS free_gb,
  ROUND((used::FLOAT / capacity) * 100, 2) AS disk_usage_pct
FROM crdb_internal.kv_store_status
ORDER BY free_gb ASC;  -- Identify node with least free space
```

**Output:**
```
 node_id | free_gb | disk_usage_pct
---------+---------+----------------
    1    |  120.50 |          65.2
    2    |  135.20 |          62.1
    3    |  125.80 |          64.3
```

**Minimum free space:** 120.50 GB (node 1, worst case)

---

### Step 2: Analyze Existing Index Range Sizes

```sql
SELECT
  index_name,
  COUNT(*) AS range_count,
  ROUND(SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0, 2) AS total_gb,
  MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_range_mb
FROM [SHOW RANGES FROM TABLE users WITH DETAILS]
GROUP BY index_name
ORDER BY largest_range_mb DESC;
```

**Output:**
```
 index_name   | range_count | total_gb | largest_range_mb
--------------+-------------+----------+------------------
 primary      |    2500     |  180.00  |       85.5
 idx_username |    1000     |   70.00  |       72.3
 idx_created  |    1200     |   50.00  |       68.1
```

**Largest range across all indexes:** 85.5 MB (primary index)

---

### Step 3: Calculate Storage Requirement

**Assumption:** New `idx_email` will have similar range size distribution to existing indexes (conservative: use largest observed range).

**Calculation:**
```
Largest range: 85.5 MB
3× requirement: 85.5 × 3 = 256.5 MB
4× requirement: 85.5 × 4 = 342 MB (recommended)
```

---

### Step 4: Decision

**Comparison:**
- **Available:** 120.50 GB minimum free space
- **Required (4×):** 342 MB = 0.334 GB

**Risk Assessment:** **SAFE**
- Available >> Required (120.50 GB >> 0.334 GB)
- Proceed with CREATE INDEX

**Command:**
```sql
CREATE INDEX idx_email ON users(email);
```

**Monitoring during backfill:**
```sql
-- Check job progress
SELECT job_id, fraction_completed, status
FROM crdb_internal.jobs
WHERE description LIKE '%idx_email%'
  AND job_type = 'SCHEMA CHANGE';

-- Monitor disk usage every 5 minutes
SELECT node_id, ROUND((used::FLOAT / capacity) * 100, 2) AS pct
FROM crdb_internal.kv_store_status
ORDER BY pct DESC;
```

---

## Example 2: Multi-Index Table Analysis

### Scenario

**Table:** `orders` (500GB, 5 existing indexes)
**Operation:** Plan to create 3 new indexes sequentially
**Goal:** Prioritize index creation by storage impact, validate capacity

---

### Step 1: Analyze All Existing Indexes

```sql
SELECT
  index_name,
  COUNT(*) AS range_count,
  ROUND(SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0, 2) AS total_gb,
  ROUND(AVG((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0, 2) AS avg_range_mb,
  MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_range_mb,
  ROUND((MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0) * 3, 2) AS required_3x_mb,
  ROUND((MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0) * 4, 2) AS required_4x_mb
FROM [SHOW RANGES FROM TABLE orders WITH DETAILS]
GROUP BY index_name
ORDER BY largest_range_mb DESC;
```

**Output:**
```
 index_name      | range_count | total_gb | avg_range_mb | largest_range_mb | required_3x_mb | required_4x_mb
-----------------+-------------+----------+--------------+------------------+----------------+----------------
 idx_created_at  |    3500     |  220.00  |     64.29    |       95.2       |     285.6      |     380.8
 primary         |    3000     |  180.00  |     61.44    |       88.5       |     265.5      |     354.0
 idx_customer_id |    2000     |   80.00  |     40.96    |       75.3       |     225.9      |     301.2
 idx_status      |    1500     |   15.00  |     10.24    |       65.1       |     195.3      |     260.4
 idx_total       |    1000     |    5.00  |      5.12    |       58.8       |     176.4      |     235.2
```

**Worst-case largest range:** 95.2 MB (`idx_created_at`, timestamp-based index with sequential inserts)

---

### Step 2: Estimate New Index Sizes

**Planned new indexes:**
1. `idx_shipping_address` (text column, low cardinality) → Assume similar to `idx_status` (~65 MB)
2. `idx_product_id` (UUID, high cardinality) → Assume similar to `idx_customer_id` (~75 MB)
3. `idx_updated_at` (timestamp, sequential) → Assume similar to `idx_created_at` (~95 MB, worst case)

**Storage requirements (4× margin):**
1. `idx_shipping_address`: 65 MB × 4 = **260 MB**
2. `idx_product_id`: 75 MB × 4 = **300 MB**
3. `idx_updated_at`: 95 MB × 4 = **380 MB**

---

### Step 3: Check Cluster Capacity

```sql
SELECT MIN((capacity - used) / 1073741824.0) AS min_free_gb
FROM crdb_internal.kv_store_status;
```

**Output:**
```
 min_free_gb
-------------
    85.5
```

**Available:** 85.5 GB minimum free space

---

### Step 4: Prioritization Strategy

**Decision:** Create indexes sequentially, smallest to largest (reduces risk, faster validation).

**Order:**
1. **First:** `idx_shipping_address` (260 MB required) → SAFE
2. **Second:** `idx_product_id` (300 MB required) → SAFE
3. **Third:** `idx_updated_at` (380 MB required) → SAFE

**Risk:** All indexes fit comfortably in 85.5 GB available. Proceed sequentially.

**Execution plan:**
```sql
-- 1. Create first index
CREATE INDEX idx_shipping_address ON orders(shipping_address);
-- Monitor: Wait for completion, check disk usage

-- 2. Create second index
CREATE INDEX idx_product_id ON orders(product_id);
-- Monitor: Wait for completion, check disk usage

-- 3. Create third index
CREATE INDEX idx_updated_at ON orders(updated_at);
-- Monitor: Wait for completion, check disk usage
```

**Why sequential?** Parallel CREATE INDEX operations compound storage requirements (e.g., 260 + 300 + 380 = 940 MB simultaneously). Sequential execution limits risk to worst-case single index.

---

## Example 3: ALTER PRIMARY KEY (High Risk)

### Scenario

**Table:** `transactions` (800GB, 4 existing indexes)
**Operation:** `ALTER TABLE transactions ALTER PRIMARY KEY USING COLUMNS (customer_id, created_at)`
**Goal:** Validate capacity for full table rewrite

---

### Step 1: Understand ALTER PRIMARY KEY Scope

**Critical:** ALTER PRIMARY KEY rewrites the **entire table** (all indexes), not just primary index.

**Storage impact:**
- **Old primary index:** Remains until GC (800GB total table size)
- **New primary index:** Full backfill (800GB)
- **All secondary indexes:** Rebuilt to reference new primary key (4 indexes)
- **MVCC overhead:** 2× MVCC versions during compaction

**Worst-case multiplier:** Use **5× largest range** (not 3×) for ALTER PRIMARY KEY.

---

### Step 2: Find Largest Range Across All Indexes

```sql
SELECT
  MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_range_mb_any_index
FROM [SHOW RANGES FROM TABLE transactions WITH DETAILS];
```

**Output:**
```
 largest_range_mb_any_index
----------------------------
           105.8
```

**Largest range:** 105.8 MB (across all indexes)

---

### Step 3: Calculate Storage Requirement (Conservative)

**Calculation:**
```
Largest range: 105.8 MB
5× requirement: 105.8 × 5 = 529 MB per node (conservative for ALTER PRIMARY KEY)
```

**Why 5×?** ALTER PRIMARY KEY has higher MVCC churn due to full table rewrite.

---

### Step 4: Check Cluster Capacity

```sql
SELECT
  node_id,
  ROUND((capacity - used) / 1073741824.0, 2) AS free_gb
FROM crdb_internal.kv_store_status
ORDER BY free_gb ASC;
```

**Output:**
```
 node_id | free_gb
---------+---------
    1    |   45.2
    2    |   52.8
    3    |   48.6
```

**Minimum free space:** 45.2 GB (node 1)

---

### Step 5: Decision

**Comparison:**
- **Available:** 45.2 GB = 46,284 MB
- **Required (5×):** 529 MB

**Risk Assessment:** **SAFE**
- Available >> Required (46,284 MB >> 529 MB)
- Proceed with ALTER PRIMARY KEY, but monitor closely

**Execution:**
```sql
-- 1. Set up monitoring alert (85% disk threshold)
-- 2. Schedule during maintenance window
-- 3. Execute ALTER
ALTER TABLE transactions ALTER PRIMARY KEY USING COLUMNS (customer_id, created_at);

-- 4. Monitor every 5 minutes
SELECT node_id, ROUND((used::FLOAT / capacity) * 100, 2) AS pct
FROM crdb_internal.kv_store_status
ORDER BY pct DESC;
```

**Rollback plan:** If disk usage exceeds 85%, pause backfill:
```sql
-- Cancel schema change job if critical
CANCEL JOB (SELECT job_id FROM crdb_internal.jobs WHERE description LIKE '%transactions%' AND job_type = 'SCHEMA CHANGE');
```

---

## Example 4: ADD COLUMN with Default Value

### Scenario

**Table:** `products` (150GB, 2 existing indexes)
**Operation:** `ALTER TABLE products ADD COLUMN featured BOOL DEFAULT false`
**Goal:** Estimate storage requirement for column backfill

---

### Step 1: Understand ADD COLUMN Storage Impact

**With default value:** Full table backfill required (writes default value to all existing rows).

**Storage impact:**
- **Existing data:** Remains (150GB)
- **New column backfill:** Adds BOOL column to all rows (minimal size, but still backfill overhead)
- **MVCC overhead:** Temporary versions during write

**Note:** BOOL columns are small (1 byte + metadata), so backfill size is minimal. However, MVCC overhead still applies.

---

### Step 2: Find Largest Range

```sql
SELECT
  MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS largest_range_mb
FROM [SHOW RANGES FROM TABLE products WITH DETAILS];
```

**Output:**
```
 largest_range_mb
------------------
       78.3
```

---

### Step 3: Calculate Requirement

**Calculation:**
```
Largest range: 78.3 MB
4× requirement: 78.3 × 4 = 313.2 MB (production standard)
```

**Note:** ADD COLUMN backfill has lower storage overhead than CREATE INDEX (smaller data writes), but use 4× for safety.

---

### Step 4: Check Capacity

```sql
SELECT MIN((capacity - used) / 1073741824.0) AS min_free_gb
FROM crdb_internal.kv_store_status;
```

**Output:**
```
 min_free_gb
-------------
    200.5
```

**Available:** 200.5 GB

---

### Step 5: Decision

**Risk Assessment:** **SAFE**
- Available >> Required (200.5 GB >> 0.313 GB)
- Proceed with ADD COLUMN

**Execution:**
```sql
ALTER TABLE products ADD COLUMN featured BOOL DEFAULT false;
```

**Expected backfill time:** Depends on row count and cluster load. Monitor with:
```sql
SELECT job_id, fraction_completed FROM crdb_internal.jobs WHERE description LIKE '%products%';
```

---

## Decision Trees

### Tree 1: Single Index Creation

```
START: Planning CREATE INDEX on table T
│
├─ Step 1: Check range count
│  ├─ < 1000 ranges → Low complexity
│  └─ > 5000 ranges → High complexity (use LIMIT in queries)
│
├─ Step 2: Find largest range in existing indexes
│  └─ Run: MAX(span_stats->>'approximate_disk_bytes')
│
├─ Step 3: Calculate requirement
│  ├─ Dev/staging: 3× largest range
│  └─ Production: 4× largest range
│
├─ Step 4: Check cluster free space
│  └─ Run: MIN(capacity - used) from kv_store_status
│
└─ Step 5: Decision
   ├─ Free space ≥ 4× → SAFE (proceed)
   ├─ Free space ≥ 3× but < 4× → MARGINAL (proceed with monitoring)
   └─ Free space < 3× → UNSAFE (add capacity or drop unused indexes)
```

---

### Tree 2: Multi-Index Creation

```
START: Planning N new indexes on table T
│
├─ Step 1: Analyze all existing indexes
│  └─ Find worst-case largest range across all indexes
│
├─ Step 2: Estimate each new index
│  └─ Assume similar to worst-case existing index
│
├─ Step 3: Prioritize
│  ├─ Sequential (recommended): Create smallest to largest
│  │  └─ Required capacity: MAX(individual index requirements)
│  └─ Parallel (high risk): Create simultaneously
│      └─ Required capacity: SUM(all index requirements)
│
└─ Step 4: Execute
   ├─ Sequential → Create one, monitor, create next
   └─ Parallel → Monitor continuously, prepare to pause if threshold hit
```

---

### Tree 3: Capacity Expansion Decision

```
START: Required storage > Available storage
│
├─ Option 1: Add cluster capacity
│  ├─ Add nodes (horizontal scaling)
│  └─ Increase disk per node (vertical scaling)
│
├─ Option 2: Free existing space
│  ├─ Drop unused indexes
│  │  └─ Check: SELECT * FROM crdb_internal.index_usage_statistics WHERE total_reads = 0
│  ├─ Reduce GC TTL temporarily (frees MVCC versions faster)
│  │  └─ ALTER TABLE T CONFIGURE ZONE USING gc.ttlseconds = 3600; -- 1 hour (default: 4 hours)
│  └─ Manually trigger GC (force compaction)
│
├─ Option 3: Defer schema change
│  └─ Schedule during off-peak hours when more capacity available
│
└─ Option 4: Execute with risk (NOT RECOMMENDED)
   └─ Monitor continuously, prepare to cancel if threshold hit
```

---

## Safety Margins: 3× vs 4× vs 5×

### When to Use Each Multiplier

| Multiplier | Use Case | Risk Level | Examples |
|------------|----------|------------|----------|
| **3×** | Dev/staging, non-critical tables | Minimum (theoretical) | Test environments, scratch tables |
| **4×** | Production standard | Recommended | Most production workloads |
| **5×** | High-stakes, ALTER PRIMARY KEY | Conservative | Financial tables, compliance data, full table rewrites |

---

### Calculation Comparison Table

**Example:** Largest range = 100 MB

| Multiplier | Required Free Space | Buffer Above Minimum | Use Case |
|------------|---------------------|----------------------|----------|
| 3× | 300 MB | 0 MB (baseline) | Minimum (theory) |
| 4× | 400 MB | 100 MB (33% buffer) | Production standard |
| 5× | 500 MB | 200 MB (66% buffer) | High-stakes operations |

**Recommendation:** Always use **4× for production CREATE INDEX**, **5× for ALTER PRIMARY KEY**.

---

## Common Calculation Mistakes

### Mistake 1: Using Average Instead of Max

**WRONG:**
```sql
-- INCORRECT: Using average range size
SELECT AVG((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS avg_mb
FROM [SHOW RANGES FROM TABLE t WITH DETAILS];
-- Avg: 50 MB → 3× = 150 MB (UNDERESTIMATED)
```

**CORRECT:**
```sql
-- CORRECT: Using largest range size
SELECT MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 AS max_mb
FROM [SHOW RANGES FROM TABLE t WITH DETAILS];
-- Max: 80 MB → 3× = 240 MB (accurate worst case)
```

**Why wrong?** Largest range determines worst-case storage spike before split occurs.

---

### Mistake 2: Applying 3× to Total Table Size

**WRONG:**
```sql
-- INCORRECT: Multiplying total table size
SELECT SUM((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0 * 3 AS wrong_required_gb
FROM [SHOW RANGES FROM TABLE t WITH DETAILS];
-- Total: 500 GB → 3× = 1500 GB (MASSIVELY OVERESTIMATED)
```

**CORRECT:**
```sql
-- CORRECT: Multiplying largest single range
SELECT (MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1073741824.0) * 3 AS correct_required_gb
FROM [SHOW RANGES FROM TABLE t WITH DETAILS];
-- Max range: 0.08 GB → 3× = 0.24 GB (accurate)
```

**Why wrong?** 3× rule applies per-range, not per-table. CockroachDB splits large ranges automatically; total table size is irrelevant.

---

### Mistake 3: Ignoring MVCC Overhead

**WRONG:**
```sql
-- INCORRECT: Using live_bytes only
SELECT MAX((span_stats->>'live_bytes')::BIGINT) / 1048576.0 * 3 AS wrong_mb
FROM [SHOW RANGES FROM TABLE t WITH DETAILS];
-- Live: 60 MB → 3× = 180 MB (UNDERESTIMATED)
```

**CORRECT:**
```sql
-- CORRECT: Using approximate_disk_bytes (includes MVCC)
SELECT MAX((span_stats->>'approximate_disk_bytes')::BIGINT) / 1048576.0 * 3 AS correct_mb
FROM [SHOW RANGES FROM TABLE t WITH DETAILS];
-- Disk: 80 MB → 3× = 240 MB (includes MVCC versions)
```

**Why wrong?** `live_bytes` excludes MVCC versions and old data. Use `approximate_disk_bytes` for realistic estimates.

---

### Mistake 4: Not Checking Per-Node Free Space

**WRONG:**
```sql
-- INCORRECT: Checking total cluster capacity
SELECT SUM(capacity - used) / 1073741824.0 AS total_free_gb
FROM crdb_internal.kv_store_status;
-- Total: 500 GB free across 3 nodes
```

**CORRECT:**
```sql
-- CORRECT: Checking minimum per-node free space
SELECT MIN((capacity - used) / 1073741824.0) AS min_free_gb
FROM crdb_internal.kv_store_status;
-- Min: 120 GB free (worst-case node)
```

**Why wrong?** Replicas distribute across nodes. Worst-case node (minimum free space) determines capacity limit.

---

### Mistake 5: Parallel Index Creation Without Buffer

**WRONG:**
```sql
-- INCORRECT: Creating 3 indexes in parallel without checking combined requirement
-- Index 1: 200 MB, Index 2: 250 MB, Index 3: 300 MB
-- Assumes: 300 MB required (only checking largest)

CREATE INDEX idx_a ON t(col_a);
CREATE INDEX idx_b ON t(col_b);
CREATE INDEX idx_c ON t(col_c);
-- Actual required: 200 + 250 + 300 = 750 MB (UNDERESTIMATED)
```

**CORRECT:**
```sql
-- CORRECT: Sequential creation or account for parallel overhead
-- Option 1: Sequential (safer)
CREATE INDEX idx_a ON t(col_a);  -- Wait for completion
CREATE INDEX idx_b ON t(col_b);  -- Wait for completion
CREATE INDEX idx_c ON t(col_c);  -- Wait for completion
-- Required: 300 MB (worst case at any given time)

-- Option 2: Parallel (if necessary, with buffer)
-- Check: MIN(free space) ≥ 750 MB + 20% buffer = 900 MB
```

**Why wrong?** Parallel backfills compound storage requirements. Sequential execution limits risk to single worst-case index.

---

## Quick Reference: Calculation Checklist

- [ ] Use `MAX(span_stats->>'approximate_disk_bytes')`, NOT average
- [ ] Apply multiplier to largest range, NOT total table size
- [ ] Use `approximate_disk_bytes`, NOT `live_bytes`
- [ ] Check `MIN(free space)` across nodes, NOT total cluster capacity
- [ ] Use 4× for production CREATE INDEX, 5× for ALTER PRIMARY KEY
- [ ] For parallel operations, SUM individual requirements + buffer
- [ ] Validate capacity BEFORE executing DDL
- [ ] Monitor disk usage DURING backfill execution

---

## Related Documentation

- [Main skill documentation](../SKILL.md)
- [Permissions reference](permissions.md)
- [CockroachDB Online Schema Changes](https://www.cockroachlabs.com/docs/stable/online-schema-changes.html)
- [SHOW RANGES documentation](https://www.cockroachlabs.com/docs/stable/show-ranges.html)

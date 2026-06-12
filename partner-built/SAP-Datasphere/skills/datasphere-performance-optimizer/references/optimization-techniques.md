# Performance Optimization Techniques Reference

## Explain Plan Reading Guide

### Basic Structure Example

```
EXPLAIN SELECT d.category, SUM(s.amount) as total
FROM sales s
INNER JOIN product_dim p ON s.product_id = p.id
WHERE s.sale_date >= '2024-01-01'
GROUP BY d.category
```

**Expected Plan:**

```
Plan (cost=100..500 rows=10)
  AGGREGATE (GROUP BY category)
    Input rows: 50,000
    Output rows: 10
    Estimated cost: 450
    Selectivity: 0.0002
    Node Detail: GROUP BY category, SUM(amount)

    JOIN (INNER)
      Input rows: 50,000
      Output rows: 50,000
      Estimated cost: 350
      Join strategy: HASH JOIN
      Build table: product_dim (500 rows)
      Probe table: sales (100,000 rows)

      SCAN sales
        Input rows: 100,000
        Output rows: 50,000
        Estimated cost: 100
        Selectivity: 0.5
        Filter: sale_date >= '2024-01-01'
        Index: sales_date_idx (USED)

      SCAN product_dim
        Input rows: 500
        Output rows: 500
        Estimated cost: 50
        No filter
```

### Interpretation Key

| Metric | Good Value | Bad Value | Implication |
|--------|-----------|-----------|-------------|
| Selectivity | < 0.1 | > 0.5 | Effective filtering removes rows early |
| Index Used | Yes | No | Leveraging indexes for fast access |
| Rows Output | < Rows Input | = Rows Input | Filtering effectiveness |
| Join Strategy | NESTED LOOP (small) or HASH | CARTESIAN | Correct join algorithm |
| Cost Trend | Decreasing | Increasing at each node | Proper plan structure |

## Persistence Decision Matrix

| Factor | Persist | Don't Persist |
|--------|---------|---------------|
| **Consumer Count** | 3+ | 1-2 |
| **Calculation Cost** | High (> 1s) | Low (< 100ms) |
| **Update Frequency** | Stable (daily) | Frequent (hourly+) |
| **Data Freshness** | Can tolerate 1h lag | Requires real-time |
| **Query Concurrency** | High (10+ concurrent) | Low (< 5 concurrent) |
| **Size** | Medium (100MB-10GB) | Very large (> 50GB) |
| **Storage Cost** | Worth reuse benefit | Minimal benefit |

### Persistence Decision Examples

**PERSIST these views:**
- Customer dimension (500MB, stable daily, used in 5+ queries)
- Monthly sales summary (10GB, calculated from 1TB fact, used in 8 dashboards)
- Product hierarchy (100MB, rarely changes, joined in many queries)

**DON'T PERSIST these views:**
- Ad-hoc analysis views (1-time use)
- Real-time operational views (requires latest data)
- Huge aggregations (> 50GB, rarely accessed)
- Frequently recalculated dimensions (underlying data changes hourly)

## Partitioning Strategies by Use Case

### Time-Based Partitioning (Monthly)

**Best For:** Sales, transactions, event logs, time-series data

**Strategy:**
```sql
CREATE TABLE sales_fact (
  sale_id INT,
  amount DECIMAL(10,2),
  sale_date DATE,
  product_id INT
)
PARTITION BY MONTH(sale_date)
```

**Benefits:**
- Natural alignment with business calendars
- Easy to archive old partitions
- Supports typical date-based filters
- Good for time-series analytics

**Query Optimization:**
```sql
-- Partition pruning: only scans 2024-01 partition
SELECT SUM(amount)
FROM sales_fact
WHERE sale_date BETWEEN '2024-01-01' AND '2024-01-31'

-- No pruning: scans all partitions
SELECT SUM(amount)
FROM sales_fact
WHERE EXTRACT(MONTH FROM sale_date) = 1
```

### Range-Based Partitioning (Customer ID)

**Best For:** Large customer tables, hierarchical data, geographic data

**Strategy:**
```sql
CREATE TABLE customers (
  customer_id INT,
  name VARCHAR(100),
  region VARCHAR(50)
)
PARTITION BY RANGE(customer_id) (
  PARTITION p_group_1 VALUES LESS THAN (1000000),
  PARTITION p_group_2 VALUES LESS THAN (2000000),
  PARTITION p_group_3 VALUES LESS THAN (MAXVALUE)
)
```

**Benefits:**
- Distributes large tables evenly
- Supports range-based access patterns
- Enables parallel processing

### Hash-Based Partitioning

**Best For:** Distributing data evenly without natural key, load balancing

**Strategy:**
```sql
CREATE TABLE order_items (
  order_id INT,
  item_id INT,
  product_id INT
)
PARTITION BY HASH(order_id) PARTITIONS 16
```

**Benefits:**
- Automatic even distribution
- No natural partition key needed
- Scalable to any partition count

### List-Based Partitioning (Region)

**Best For:** Categorical data, geographic regions, business units

**Strategy:**
```sql
CREATE TABLE regional_sales (
  region VARCHAR(50),
  amount DECIMAL(10,2)
)
PARTITION BY LIST(region) (
  PARTITION p_west VALUES ('CA', 'WA', 'OR'),
  PARTITION p_midwest VALUES ('IL', 'MI', 'OH'),
  PARTITION p_east VALUES ('NY', 'MA', 'PA')
)
```

**Benefits:**
- Logical alignment with business divisions
- Easy to assign partitions to storage tiers
- Supports region-based compliance requirements

## Memory Management Best Practices

### Memory Calculation Formulas

**Available Memory for Queries:**
```
Available Memory = Total Memory - OS Overhead - Connections - Caching
                = 256GB - 16GB - 8GB - 32GB
                = 200GB
```

**Per-Query Memory Allocation:**
```
Per-Query Limit = Available Memory / Expected Concurrent Queries
                = 200GB / 10
                = 20GB per query
```

**Batch Size Optimization:**
```
Batch Size = Per-Query Memory / (Row Width * Rows Buffered)
           = 20GB / (500 bytes/row * 2 copies in memory)
           = 20,971,520 rows
           ≈ 10M rows or adjust based on testing
```

### Memory Spill Prevention

**Causes of Memory Spill:**
1. Batch size too large for memory
2. Intermediate result sizes grow unexpectedly
3. Join with large build table
4. Multiple concurrent queries exceeding limit
5. Incorrect memory allocation

**Monitoring:**
```sql
SELECT
  task_id,
  memory_peak_mb,
  memory_spill_mb,
  spill_count,
  CASE WHEN memory_spill_mb > 0 THEN 'SPILL DETECTED'
       ELSE 'OK' END as status
FROM task_metrics
WHERE execution_date >= CURRENT_DATE - 7
ORDER BY memory_spill_mb DESC
```

**Resolution:**
1. Reduce batch size (increase memory efficiency)
2. Increase total memory allocation
3. Add indexes to reduce intermediate rows
4. Split large operations into smaller chunks
5. Schedule during lower concurrent load

## Common Anti-Patterns and Fixes

### Anti-Pattern 1: Late Filtering in Joins

**Problem:**
```sql
-- SLOW: Joins full tables, then filters
SELECT *
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.order_date >= '2024-01-01'
```

**Impact:**
- Joins all 100K customers with all 10M orders (1B intermediate rows)
- Filters reduce to 1M rows after join
- Massive memory usage and I/O

**Fix:**
```sql
-- FAST: Filter source before join
SELECT *
FROM (SELECT * FROM orders WHERE order_date >= '2024-01-01') o
INNER JOIN customers c ON o.customer_id = c.id
```

**Result:**
- Filters orders to 1M rows first
- Joins 1M orders with 100K customers (100M rows)
- 1000x memory reduction

### Anti-Pattern 2: Multiple Cascading Aggregations

**Problem:**
```sql
-- SLOW: Each aggregation full scan
SELECT dept, COUNT(*)
FROM (
  SELECT dept, employee_id
  FROM (
    SELECT dept, employee_id
    FROM employees
    GROUP BY dept, employee_id
  )
  GROUP BY dept
)
GROUP BY dept
```

**Fix:**
```sql
-- FAST: Single aggregation
SELECT dept, COUNT(DISTINCT employee_id)
FROM employees
GROUP BY dept
```

### Anti-Pattern 3: Function on Indexed Column

**Problem:**
```sql
-- SLOW: Index not usable
SELECT *
FROM orders
WHERE YEAR(order_date) = 2024
```

**Explain Plan Shows:**
- Full table scan (no index used)
- Function evaluation on every row
- High CPU usage

**Fix:**
```sql
-- FAST: Index usable
SELECT *
FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'
```

**Impact:**
- Index used (order_date_idx)
- Partition pruning (if date-partitioned)
- Orders of magnitude faster

### Anti-Pattern 4: SELECT * with Unused Columns

**Problem:**
```sql
-- SLOW: Fetches all 50 columns
SELECT *
FROM customer_360
WHERE region = 'WEST'
```

**Impact:**
- Fetches columns never used in join/filter
- Larger result sets over network
- More memory required

**Fix:**
```sql
-- FAST: Only needed columns
SELECT customer_id, name, region
FROM customer_360
WHERE region = 'WEST'
```

### Anti-Pattern 5: Missing Index on Foreign Key

**Problem:**
```sql
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id INT,  -- No index!
  amount DECIMAL(10,2)
)
```

**Impact:**
- Joins on customer_id require full table scan
- Every join query slowly crawls through 100M rows
- High memory usage for hash join build

**Fix:**
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

**Impact:**
- Nested loop join uses index
- 100x faster for typical filters

## Performance Benchmarking Approaches

### Baseline Establishment (Week 1)

**Measurements to Capture:**
```
FOR EACH QUERY:
  - Cold execution (cache cleared): 3 runs, take median
  - Warm execution (cache primed): 5 runs, take median
  - Peak memory: from task metrics
  - Rows returned: from logs
  - Data volume scanned: from task metrics
  - CPU time: from task metrics

AGGREGATE:
  - P50, P95, P99 execution time
  - Average rows per query
  - Total data scanned per day
  - Memory utilization pattern
```

### Benchmark Tools Setup

```sql
-- Create benchmark table to track results
CREATE TABLE perf_benchmarks (
  benchmark_date DATE,
  query_name VARCHAR(256),
  execution_time_ms INT,
  memory_peak_mb INT,
  rows_returned INT,
  status VARCHAR(20),
  notes VARCHAR(500)
);

-- Procedure to run benchmark
CREATE PROCEDURE benchmark_query(query_name VARCHAR, query_sql VARCHAR) AS
  DECLARE start_time TIMESTAMP;
  DECLARE end_time TIMESTAMP;
  DECLARE execution_ms INT;
BEGIN
  SET start_time = CURRENT_TIMESTAMP;
  EXECUTE query_sql;
  SET end_time = CURRENT_TIMESTAMP;
  SET execution_ms = EXTRACT(EPOCH FROM (end_time - start_time)) * 1000;
  INSERT INTO perf_benchmarks VALUES (CURRENT_DATE, query_name, execution_ms, ...);
END;
```

### Comparison Methodology (Post-Optimization)

**Compare Against Baseline:**
```
For each metric:
  - Improvement % = (Baseline - New) / Baseline * 100
  - 20% improvement = significant
  - 50%+ improvement = major optimization
  - < 5% = noise, monitor for regression
```

**Statistical Significance:**
- Collect minimum 5 runs in stable conditions
- Use median (not mean) for outlier resistance
- Run for 2+ weeks to catch time-of-day effects
- Monitor for p-value < 0.05 on t-test

### Regression Detection

```sql
-- Daily performance check
SELECT
  query_name,
  AVG(execution_time_ms) as avg_time,
  LAG(AVG(execution_time_ms)) OVER (PARTITION BY query_name ORDER BY benchmark_date) as prev_day_avg,
  ROUND((AVG(execution_time_ms) - LAG(...)) / LAG(...) * 100, 2) as regression_pct
FROM perf_benchmarks
WHERE benchmark_date >= CURRENT_DATE - 7
GROUP BY query_name, benchmark_date
HAVING regression_pct > 10
ORDER BY regression_pct DESC
```

## Storage Tier Recommendations

### Hot Tier (In-Memory)

**Characteristics:**
- Access latency: < 1ms
- Cost: $50-100 per GB/month
- Capacity: Limited to available RAM

**Candidates:**
- Dimension tables (< 1GB)
- Small reference data
- Frequently queried aggregations
- Real-time KPI tables

**Example Allocation:**
```
Customer Dimension:     500 MB
Product Dimension:      200 MB
Date Dimension:         50 MB
Daily Sales Summary:    2 GB
Region Master Data:     100 MB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL HOT:              3 GB
```

### Warm Tier (SSD/NVMe)

**Characteristics:**
- Access latency: 1-10ms
- Cost: $5-20 per GB/month
- Capacity: Typically 50-500 GB

**Candidates:**
- Medium-sized tables (1-50 GB)
- Week's worth of transaction data
- Aggregations queried daily
- Staging tables

**Example Allocation:**
```
Last 4 weeks sales:     30 GB
Last 90 days inventory: 5 GB
Transactional staging:  15 GB
Marketing analytics:    20 GB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL WARM:             70 GB
```

### Cold Tier (Object Store/Archive)

**Characteristics:**
- Access latency: 100ms-1s (may require restore)
- Cost: $1-5 per GB/month
- Capacity: Unlimited

**Candidates:**
- Historical data (> 2 years)
- Infrequently accessed archives
- Compliance/regulatory data
- Backup data

**Example Allocation:**
```
2022 historical sales:  500 GB
2021 archive:           800 GB
Compliance records:     200 GB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL COLD:             1.5 TB
```

### Tiering Policy Implementation

```sql
-- Auto-tier based on age
CREATE POLICY tier_by_age AS
  IF data_age_days < 7 THEN hot_tier
  ELSE IF data_age_days < 90 THEN warm_tier
  ELSE cold_tier;

-- Example: Automatic execution
ALTER TABLE sales_fact SET STORAGE POLICY tier_by_age;
```

### Cost-Benefit Analysis

**Monthly Storage Cost Comparison:**

| Strategy | Hot | Warm | Cold | Total | Notes |
|----------|-----|------|------|-------|-------|
| All Hot | 250 | - | - | $250 | Simple, expensive, limited capacity |
| Hot + Warm | 50 | 350 | - | $160 | Balanced, good performance |
| Hot + Warm + Cold | 50 | 70 | 75 | $130 | Optimal cost, tiering complexity |

**Performance vs. Cost Trade-off:**
- Use tiering when potential savings > 20%
- Avoid over-tiering (management overhead)
- Monitor actual access patterns quarterly
- Adjust tiers based on usage evolution

---
name: Performance Optimizer
description: "Optimize Datasphere performance NOW! Use when views run slow, queries timeout, or data flows lag. Analyze bottlenecks, tune execution plans, optimize persistence, manage storage. Keywords: slow query, performance, bottleneck, timeout, memory, CPU, execution plan, view optimization, partition, index."
---

# Performance Optimizer Skill

## Overview

The Performance Optimizer skill helps you identify and resolve performance issues in SAP Datasphere. Whether your views are running slowly, queries are timing out, or data flows are consuming excessive resources, this skill provides a systematic approach to diagnose and fix performance problems at every layer: views, queries, data flows, and storage.

## When to Use This Skill

Trigger this skill when you encounter:
- Views or queries running slower than expected
- Query timeouts or cancellations
- High memory or CPU consumption
- Data flow execution taking excessive time
- Replication flows with poor delta performance
- Need to optimize storage usage
- Capacity warnings or resource contention alerts
- Performance regression after schema changes
- Need to benchmark performance improvements

## Performance Analysis Approach

### 1. Identify the Bottleneck

Start by pinpointing where performance degradation occurs:

**View Performance Issues:**
- Access the View Analyzer tool in your view's details
- Check execution time trends over the last 7-30 days
- Compare execution times across different consumer queries
- Identify which views are called most frequently
- Note views with long initialization times

**Query Performance Issues:**
- Review query execution statistics in task logs
- Use Explain Plan to understand query execution strategy
- Check statement logs for query duration and resource usage
- Identify queries with full table scans or inefficient joins
- Monitor query frequency and timing patterns

**Data Flow Performance Issues:**
- Check data flow execution logs for step-level timing
- Monitor initial load duration vs. delta load duration
- Review parallelism settings and actual utilization
- Check for data quality issues causing processing overhead
- Analyze memory allocation and spill events

### 2. Measure Current Performance

Establish baseline metrics before optimization:

**Key Metrics to Capture:**
- Query execution time (wall-clock and CPU time)
- Memory usage (peak and average)
- Data volume processed (rows and bytes)
- I/O operations and throughput
- Number of disk accesses vs. in-memory operations
- Index usage patterns
- Cache hit rates
- Parallelism level achieved
- Storage tier distribution

Use the MCP tools to gather metrics:
- `execute_query`: Run diagnostic queries to capture baseline stats
- `analyze_column_distribution`: Understand data skew and selectivity
- `get_table_schema`: Review column types and indexing
- `get_task_status`: Monitor execution metrics

### 3. Optimize

Apply targeted optimizations based on findings (see following sections).

### 4. Validate

Re-measure performance after changes:
- Compare new metrics against baseline
- Verify performance improvement meets targets
- Monitor for 7-14 days to ensure consistency
- Check for negative side effects on other queries
- Document changes for future reference

## View Analyzer

The View Analyzer provides insights into view execution performance and resource consumption.

### Interpreting View Analyzer Results

**Execution Time Breakdown:**
- **Initialization Time**: Time to prepare execution plan and allocate resources. High values indicate complex view logic or many dependent views.
- **Execution Time**: Actual query processing time. Dominated by data retrieval and transformation.
- **Fetch Time**: Time to return results to consumer. Long fetch times indicate large result sets or network latency.

**Resource Consumption:**
- **Peak Memory**: Maximum memory used during execution. Watch for memory spills to disk.
- **CPU Time**: Total CPU cycles consumed. High CPU indicates data processing-heavy operations.
- **I/O Throughput**: Data read from storage. Compare with data returned to find filtering efficiency.

### Identifying Expensive Operations

**High Memory Consumers:**
- Joins with large intermediate result sets
- Aggregations without pre-filtering
- Complex subqueries creating multiple temporary tables
- Non-persisted views with repeated calculations

**CPU-Intensive Operations:**
- Complex calculations and expressions
- Multiple levels of nested aggregations
- String operations on large text fields
- Date/time calculations without optimization

**I/O-Heavy Operations:**
- Full table scans on large tables
- Inefficient join strategies
- Missing indexes on join keys
- Reading unnecessary columns

## Explain Plan Analysis

The Explain Plan shows exactly how Datasphere executes your query, revealing inefficiencies at each step.

### Reading Execution Plans

**Plan Structure:**
1. **Node Type**: SCAN (table access), JOIN, AGGREGATE, SORT, FILTER, etc.
2. **Input Rows**: Rows input to this node
3. **Output Rows**: Rows produced by this node
4. **Selectivity**: Output/Input ratio. Values < 0.1 indicate effective filtering.
5. **Estimated Time**: Predicted execution time
6. **Actual Time**: Measured execution time (if available)

### Spotting Full Table Scans

**Indicators:**
- SCAN node with no index specification
- Input rows equal to table row count
- High selectivity discrepancy (many input rows, few output rows)

**Solutions:**
- Add index on WHERE clause columns
- Add covering index including SELECT columns
- Consider partitioning with partition-aware queries
- Rewrite to improve filter pushdown

### Identifying Join Inefficiencies

**Red Flags:**
- Join producing result set larger than inputs (indicates Cartesian product)
- Very high intermediate row counts before filtering
- Hash joins with small build tables (should use index joins)
- Join order processing large tables first

**Solutions:**
- Reorder joins to process smallest tables first
- Add indexes on join keys
- Apply filters before joins (reduce probe table size)
- Consider materialization of frequently-joined dimensions
- Use broadcast tables for small dimension tables

### Common Explain Plan Anti-Patterns

**Pattern: Multiple Cascading Aggregations**
```
AGGREGATE (GROUP BY col1, col2, col3)
  AGGREGATE (GROUP BY col1, col2)
    AGGREGATE (GROUP BY col1)
      SCAN big_table
```
Issue: Each aggregation processes full dataset
Solution: Combine aggregations or materialize intermediate results

**Pattern: Cartesian Join**
```
JOIN (on false condition)
  SCAN table1 (1M rows)
  SCAN table2 (1M rows)
```
Issue: 1T row intermediate result
Solution: Fix join condition, verify ON clause logic

**Pattern: Late Filtering**
```
FILTER (where price > 100)
  JOIN table1 (1M rows) with table2 (1M rows)
```
Issue: Join processes all rows before filtering
Solution: Move WHERE clause into source tables (pushdown)

## View Optimization Strategies

### Persistence Strategy

**When to Persist:**
- Views consumed by many queries (reuse calculation)
- Complex views with expensive calculations
- Views used in real-time dashboards (reduce latency)
- High-frequency views (cache results between accesses)
- Views with stable underlying data

**When NOT to Persist:**
- Frequently updated source data (maintenance cost)
- Views with specific daily snapshots
- Once-per-execution views
- Views with minimal consumer count

**Persistence Modes:**
- **Runtime**: Results cached in memory during session (no latency, high memory)
- **Disk-Based**: Results written to disk (lower memory, I/O cost)
- **Materialized**: Pre-calculated, updated on schedule (consistent performance, staleness risk)

### Column Pruning

Remove unnecessary columns from views to reduce data volume:

**Strategy:**
1. Audit all consuming queries
2. Identify columns never referenced
3. Remove unused columns from source
4. Test dependent views for impact
5. Document retained columns and purpose

**Benefits:**
- Reduced memory footprint
- Faster data transfer
- Smaller index sizes
- Improved cache effectiveness

### Partition Pruning

Organize data into partitions to reduce scanned volume:

**Partition Key Selection:**
- High-cardinality columns with clear ranges (dates, regions)
- Columns frequently in WHERE clauses
- Columns supporting most common filters
- Avoid partitioning on low-cardinality columns

**Partition Strategy:**
- **Time-Based**: Year, month, day (best for temporal data)
- **Range-Based**: Numeric ranges (best for numeric dimensions)
- **Hash-Based**: Distribute evenly (when no natural partition key)
- **List-Based**: Specific values (geographic regions, business units)

**Partition Pruning in Queries:**
```sql
SELECT * FROM sales
WHERE year = 2024 AND month IN (1,2,3)
-- Partition pruning eliminates months outside this range
```

### Push-Down Optimization

Move filtering and aggregation to earliest possible stage:

**Examples:**
```sql
-- GOOD: Filters pushed to source tables
SELECT dept, COUNT(*)
FROM employees
WHERE hire_date >= '2023-01-01'  -- Pushed down
GROUP BY dept

-- BAD: Filter applied to pre-aggregated result (wrong answer potential)
SELECT dept, COUNT(*) as emp_count
FROM employees
GROUP BY dept
HAVING CAST(MAX(hire_date) AS DATE) >= '2023-01-01'
```

**Benefits:**
- Reduces intermediate result sizes
- Minimizes data movement
- Allows index usage
- Reduces memory pressure

## Query Optimization Techniques

### Index Usage

**Index Types:**
- **B-Tree Index**: Default, efficient for range and equality queries
- **Hash Index**: For equality lookups only, faster than B-Tree
- **Bitmap Index**: For low-cardinality columns, space-efficient
- **Covering Index**: Includes all columns needed (no table access required)

**Index Selection:**
1. Profile query WHERE and JOIN clauses
2. Create indexes on high-selectivity columns
3. Use composite indexes for multi-column conditions
4. Add covering indexes for frequently-run queries
5. Monitor index usage; drop unused indexes

**Query Hints for Index Usage:**
```sql
SELECT /*+ INDEX(orders order_date_idx) */
  order_id, amount
FROM orders
WHERE order_date = '2024-01-15'
```

### Join Order Optimization

**Heuristic: Smallest Table First**
```sql
-- GOOD: Dimension first (smaller)
SELECT *
FROM departments d
  INNER JOIN employees e ON d.dept_id = e.dept_id
WHERE d.region = 'WEST'

-- BAD: Large fact table first
SELECT *
FROM sales_fact f
  INNER JOIN date_dim d ON f.date_id = d.date_id
WHERE d.year = 2024
```

**Broadcast Strategy:**
Use broadcast join for small dimensions (< 100MB):
```sql
SELECT /*+ BROADCAST(dimension) */
  f.amount, d.category
FROM fact_table f
  INNER JOIN small_dimension d ON f.dim_id = d.id
```

### Aggregation Strategies

**Pre-Aggregation Pattern:**
Materialize frequently-aggregated views:
```sql
-- Materialized view updated daily
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT date, product_id, SUM(amount) as total_sales, COUNT(*) as order_count
FROM sales_fact
GROUP BY date, product_id

-- Consumer query now fast
SELECT product_id, SUM(total_sales)
FROM daily_sales_summary
WHERE date >= '2024-01-01'
GROUP BY product_id
```

**Aggregation Push-Down:**
```sql
-- GOOD: Aggregate at source
SELECT dept, SUM(salary)
FROM employees
WHERE status = 'ACTIVE'
GROUP BY dept

-- BAD: Aggregate after joining to dimensions
SELECT e.dept, SUM(e.salary)
FROM employees e
  INNER JOIN departments d ON e.dept_id = d.dept_id
GROUP BY e.dept
```

## Data Flow Performance

### Parallelism Configuration

**Parallelism Settings:**
- **DOP (Degree of Parallelism)**: Number of parallel worker threads
- **Default**: Auto-calculated based on CPU cores and available memory
- **Manual Override**: Set for specific flows with special requirements

**Tuning Approach:**
1. Baseline with default parallelism
2. Monitor CPU utilization (target 70-85%)
3. Increase DOP if CPU < 50% (data not distributed well)
4. Decrease DOP if CPU > 90% (contention, thread overhead)
5. Test with representative data volume

### Batch Sizes

**Batch Size Impact:**
- **Small batches** (1K rows): More overhead, better interactivity
- **Large batches** (100K+ rows): Better throughput, more memory per batch
- **Optimal**: Typically 10K-50K rows depending on row width and memory

**Configuration:**
```
Batch Size = Available Memory / (Row Width * 2)
```

### Memory Allocation

**Memory Distribution:**
- Allocate 60% to data buffers
- 20% to working memory (joins, aggregations)
- 20% to system overhead and safety margin

**Monitoring:**
- Watch for memory spill messages (indicates insufficient allocation)
- Monitor peak memory usage over time
- Check for memory leaks in long-running flows

## Replication Flow Performance

### Initial Load Optimization

**Full Table Replication:**
1. Schedule during low-activity windows
2. Use maximum batch size for the table size
3. Verify target has sufficient staging space
4. Monitor progress via status logs
5. Validate row counts match source

**Selective Replication:**
```sql
-- Replicate only recent data
WHERE created_date >= CURRENT_DATE - 7
```

Benefits: Reduced network traffic, faster completion

### Delta Performance Tuning

**Change Data Capture (CDC) Optimization:**
1. Ensure source system has CDC enabled
2. Configure appropriate change log retention
3. Set delta frequency (hourly, daily) based on volume
4. Monitor delta processing time trends
5. Alert on delta lag exceeding threshold

**Performance Issues and Solutions:**
- **Long delta processing**: Increase parallelism, check for data anomalies
- **High memory usage**: Reduce batch size, increase delta frequency
- **Network bottleneck**: Verify network bandwidth, consider compression
- **Target contention**: Schedule deltas during off-peak, increase parallel writers

## Storage Optimization

### Disk vs. In-Memory Strategy

**In-Memory Advantages:**
- Sub-millisecond query latency
- Efficient for repeated access
- Better for interactive dashboards

**In-Memory Disadvantages:**
- Limited capacity
- Higher cost per GB
- Unsuitable for very large tables

**Disk Advantages:**
- Unlimited capacity
- Cost-effective for archival data
- Suitable for infrequently-accessed tables

**Disk Disadvantages:**
- Higher query latency (100ms+)
- Suitable for batch reporting

**Decision Matrix:**
- High-frequency, small tables → In-Memory
- Large, infrequently-accessed → Disk/Object Store
- Medium-sized, moderate frequency → Hybrid (hot set in-memory)

### Object Store Tiering (HDLF - Hadoop Distributed File System Layer)

**Tier Organization:**
1. **Hot Tier**: Frequently accessed, in-memory or SSD
2. **Warm Tier**: Moderate access, disk-based
3. **Cold Tier**: Archive data, object store (S3/blob)

**Tiering Policy:**
```
Data age < 30 days → Hot tier
Data age 30-90 days → Warm tier
Data age > 90 days → Cold tier
```

**Benefits:**
- Optimal cost-performance balance
- Automatic promotion/demotion
- Transparent to queries
- Improved capacity utilization

## Monitoring and Alerting

### Task Logs

**Key Information:**
- Task execution time (start, end, duration)
- Rows processed (read, written, failed)
- Memory usage (peak, average)
- Data quality metrics (error counts)
- Dependencies (parent/child tasks)

**Analysis:**
- Track execution time trends
- Identify tasks with increasing duration
- Monitor failure rates
- Check for resource contention patterns

### Statement Logs

**Query Metrics:**
- Query text (full SQL)
- Execution time breakdown (parse, optimize, execute)
- Rows returned
- Memory consumed
- CPU time
- Table accesses and I/O

**Usage:**
```sql
SELECT query_text, AVG(execution_time_ms) as avg_time, COUNT(*) as frequency
FROM statement_logs
WHERE timestamp >= CURRENT_DATE - 7
GROUP BY query_text
ORDER BY frequency DESC
```

### Capacity Dashboards

**Metrics to Monitor:**
- Overall CPU utilization
- Memory consumption by tenant/space
- Storage usage by object type
- Network I/O
- Query queue depth
- Active sessions

**Alerting Thresholds:**
- CPU > 80%: Investigate resource contention
- Memory > 85%: Add capacity or optimize
- Storage > 90%: Archive or clean data
- Queue depth > 10: Performance degradation
- Session count increasing: Check for runaway queries

## Using MCP Tools for Performance Analysis

### execute_query
Use to run diagnostic queries and capture explain plans:
```
execute_query(query="EXPLAIN SELECT ...", explain_type="full")
```
Returns execution plan with estimated and actual metrics.

### analyze_column_distribution
Understand data distribution for optimal indexing:
```
analyze_column_distribution(table="sales", column="product_id")
```
Returns histogram of values, identifying skew and cardinality.

### get_table_schema
Review table structure, indexes, and partitioning:
```
get_table_schema(table="orders")
```
Returns columns, data types, indexes, constraints, and statistics.

### get_task_status
Monitor task execution metrics:
```
get_task_status(task_id="replication_flow_01")
```
Returns execution time, rows processed, memory used, and state.

## Performance Optimization Workflow

1. **Identify Issue**: Run diagnostic queries, review task logs
2. **Measure Baseline**: Capture execution time, resource usage, row counts
3. **Analyze Root Cause**: Review Explain Plan, check for anti-patterns
4. **Create Optimization Plan**: Document proposed changes and expected impact
5. **Implement Changes**: Add indexes, modify view logic, adjust persistence
6. **Test Thoroughly**: Validate correctness and measure performance
7. **Monitor Results**: Track metrics for 1-2 weeks post-deployment
8. **Document Learnings**: Record successful optimizations for future reference

## Best Practices

- Always establish baseline metrics before optimization
- Make one change at a time to isolate impact
- Test in non-production environment first
- Monitor for 2+ weeks after changes (catch edge cases)
- Document all optimization decisions and rationale
- Regular review of slow query logs (at least weekly)
- Implement automated alerting on performance regressions
- Consider future growth when sizing indexes and partitions
- Balance optimization effort against business value
- Regularly validate statistics and rebuild indexes

## Reference Materials

See reference files for detailed procedures:
- `references/optimization-techniques.md` - Explain Plan reading guide, persistence decision matrix, partitioning strategies, memory management
- `references/diagnostic-procedures.md` - Advanced diagnostic procedures: PlanViz trace generation/analysis, MDS query diagnosis for SAC live connections, HAR file network analysis, tenant memory/CPU profiling, and extracting underlying SQL from Datasphere views

# CREATE STATISTICS Examples

Comprehensive patterns for manual statistics collection, job monitoring, and batch execution strategies. Covers single-column, multi-column, point-in-time, and advanced scenarios for optimizing CockroachDB query performance.

## Automatic Statistics (Recommended Default)

### Basic Syntax

```sql
CREATE STATISTICS __auto__ FROM table_name;
```

**What it does:**
- Automatically selects all columns for statistics collection
- Creates table-level row count statistics
- Generates per-column distinct_count, null_count, and histograms
- Recommended for most use cases (least operational overhead)

**When to use:**
- Post-bulk-load refresh
- Routine scheduled refresh
- When you don't know which specific columns need statistics
- Tables with stable schema and query patterns

### Example: Refresh Single Table

```sql
-- Refresh statistics for orders table
CREATE STATISTICS __auto__ FROM mydb.public.orders;
```

**Verification:**
```sql
-- Check statistics were created
SELECT column_names, created, row_count
FROM [SHOW STATISTICS FOR TABLE mydb.public.orders]
ORDER BY created DESC
LIMIT 10;
```

### Example: Batch Refresh Multiple Tables

```sql
-- Refresh statistics for multiple tables (execute sequentially)
CREATE STATISTICS __auto__ FROM users;
CREATE STATISTICS __auto__ FROM orders;
CREATE STATISTICS __auto__ FROM products;
```

**Best practice:** For many tables, use staggered execution (see Batch Collection Strategies section).

## Manual Column Selection

### Single Column Syntax

```sql
CREATE STATISTICS stats_name ON column_name FROM table_name;
```

**What it does:**
- Creates statistics for specific column only
- Faster than automatic collection for very wide tables (many columns)
- Useful when only specific columns are queried frequently

**When to use:**
- Narrow statistics refresh (only update critical columns)
- Very wide tables (>50 columns) where full refresh is expensive
- Columns frequently used in WHERE/JOIN but not all columns need statistics

### Example: Refresh Specific Columns

```sql
-- Create statistics for frequently-queried user_id column
CREATE STATISTICS user_id_stats ON user_id FROM orders;

-- Create statistics for order_date (used in range queries)
CREATE STATISTICS order_date_stats ON order_date FROM orders;

-- Create statistics for status column (used in WHERE clauses)
CREATE STATISTICS status_stats ON status FROM orders;
```

**Verification:**
```sql
-- Verify specific column statistics exist
SELECT column_names, created, distinct_count, null_count
FROM [SHOW STATISTICS FOR TABLE orders]
WHERE column_names = '{user_id}' OR column_names = '{order_date}' OR column_names = '{status}'
ORDER BY created DESC;
```

### Example: Refresh After Adding Column

```sql
-- Scenario: Added discount_pct column to orders table
ALTER TABLE orders ADD COLUMN discount_pct DECIMAL(5,2);

-- Populate column with data
UPDATE orders SET discount_pct = 0.10 WHERE order_total > 1000;

-- Create statistics for new column
CREATE STATISTICS discount_pct_stats ON discount_pct FROM orders;
```

**Rationale:** Automatic collection may not trigger immediately; manual refresh ensures optimizer has statistics for new column.

## Multi-Column (Composite) Statistics

### Correlated Columns Syntax

```sql
CREATE STATISTICS stats_name ON column1, column2, column3, ... FROM table_name;
```

**What it does:**
- Captures correlation between multiple columns
- Improves optimizer estimates for queries with multiple predicates on correlated columns
- **Critical:** Automatic collection does NOT create multi-column statistics (manual only)

**When to use:**
- Columns frequently queried together in WHERE clause
- Composite index columns with correlated values
- Geographic hierarchies (city + state + zip)
- Time-based partitioning columns (year + month + day)

### Example: Geographic Columns

```sql
-- Addresses table with correlated geographic columns
CREATE STATISTICS city_state_stats ON city, state FROM addresses;
CREATE STATISTICS city_state_zip_stats ON city, state, zip_code FROM addresses;
```

**Query optimization:**
```sql
-- Before multi-column stats: optimizer assumes independence
-- After multi-column stats: optimizer knows NYC is mostly in NY state
SELECT * FROM addresses
WHERE city = 'New York' AND state = 'NY' AND zip_code LIKE '10%';
```

**Verification:**
```sql
-- Check multi-column statistics exist
SELECT column_names, created, row_count, distinct_count
FROM [SHOW STATISTICS FOR TABLE addresses]
WHERE ARRAY_LENGTH(column_names, 1) > 1  -- Multi-column only
ORDER BY created DESC;
```

### Example: Composite Index Columns

```sql
-- Index on (user_id, created_at) for time-range queries per user
CREATE INDEX orders_user_time_idx ON orders (user_id, created_at);

-- Create multi-column statistics matching index
CREATE STATISTICS user_time_stats ON user_id, created_at FROM orders;
```

**Rationale:** Optimizer can better estimate selectivity for queries like:
```sql
SELECT * FROM orders
WHERE user_id = 12345 AND created_at > '2026-01-01';
```

### Example: Time-Based Partitioning

```sql
-- Table partitioned by year and month
CREATE STATISTICS year_month_stats ON partition_year, partition_month FROM events;
```

**Use case:** Queries filtering on both year and month benefit from accurate correlation estimates.

## Point-in-Time Statistics

### AS OF SYSTEM TIME Syntax

```sql
CREATE STATISTICS stats_name FROM table_name AS OF SYSTEM TIME '-1h';
```

**What it does:**
- Creates statistics based on historical table state
- Uses time-travel query to access past data snapshot
- Does NOT impact live production traffic (reads from committed snapshots)

**When to use:**
- Analyze historical data distribution without impacting current workload
- Compare statistics across different points in time
- Create statistics during high-traffic periods without adding live query load

### Example: Historical Analysis

```sql
-- Create statistics from 24 hours ago
CREATE STATISTICS historical_stats FROM orders AS OF SYSTEM TIME '-24h';
```

**Use case:** Investigate why queries were slow yesterday by analyzing statistics from that time.

### Example: Low-Impact Collection

```sql
-- Create statistics from 1 hour ago during peak traffic
CREATE STATISTICS peak_hour_stats FROM large_table AS OF SYSTEM TIME '-1h';
```

**Rationale:** Reduces resource contention by reading from slightly stale snapshot instead of latest data.

**Limitation:**
- Snapshot must be within garbage collection window (default 25 hours)
- Cannot use `AS OF SYSTEM TIME` older than GC window

**Verify GC window:**
```sql
SHOW CLUSTER SETTING gc.ttlseconds;  -- Default 90000 (25 hours)
```

## Job Monitoring and Management

### Check Statistics Job Status

```sql
-- Find recent CREATE STATISTICS jobs
SELECT
  job_id,
  description,
  status,
  fraction_completed,
  running_status,
  created,
  now() - created AS elapsed_time
FROM [SHOW JOBS]
WHERE job_type IN ('CREATE STATS', 'AUTO CREATE STATS')
  AND created > now() - INTERVAL '24 hours'
ORDER BY created DESC;
```

**Key columns:**
- `status`: 'pending', 'running', 'succeeded', 'failed', 'canceled'
- `fraction_completed`: Progress (0.0 to 1.0)
- `running_status`: Detailed progress message

### Monitor Specific Job

```sql
-- Track progress of specific job by ID
SELECT
  job_id,
  status,
  fraction_completed,
  running_status,
  ROUND(fraction_completed * 100, 2) AS pct_complete,
  now() - created AS elapsed_time
FROM [SHOW JOBS]
WHERE job_id = 123456789012345678;  -- Replace with actual job_id
```

**Polling script:**
```bash
#!/bin/bash
JOB_ID=$1

while true; do
  status=$(cockroach sql --format=csv -e "
    SELECT status, fraction_completed
    FROM [SHOW JOBS]
    WHERE job_id = $JOB_ID;
  " | tail -n1)

  job_status=$(echo $status | cut -d',' -f1)
  progress=$(echo $status | cut -d',' -f2)

  echo "$(date): Job $JOB_ID - Status: $job_status, Progress: $(echo "$progress * 100" | bc)%"

  if [[ "$job_status" == "succeeded" ]]; then
    echo "Job completed successfully"
    exit 0
  elif [[ "$job_status" == "failed" ]] || [[ "$job_status" == "canceled" ]]; then
    echo "Job failed or was canceled"
    exit 1
  fi

  sleep 10
done
```

### Cancel Statistics Job

```sql
-- Find running job
SELECT job_id, description, status, fraction_completed
FROM [SHOW JOBS]
WHERE job_type = 'CREATE STATS'
  AND status = 'running'
ORDER BY created DESC;

-- Cancel job (non-destructive, existing statistics remain)
CANCEL JOB 123456789012345678;  -- Replace with job_id
```

**When to cancel:**
- Job running longer than expected (check `elapsed_time`)
- Need to free up cluster resources immediately
- Incorrect table specified (typo in table name)

**Safety:**
- Canceling a CREATE STATISTICS job does NOT delete existing statistics
- Table remains queryable during and after cancellation
- Can safely re-run CREATE STATISTICS after cancellation

### Verify Job Completion

```sql
-- Confirm statistics were created after job succeeded
SELECT
  column_names,
  created,
  row_count
FROM [SHOW STATISTICS FOR TABLE table_name]
WHERE created > now() - INTERVAL '1 hour'  -- Recent statistics only
ORDER BY created DESC;
```

**Expected result:** New statistics rows with recent `created` timestamps.

## Batch Collection Strategies

### Staggered Execution Pattern

**Problem:** Creating statistics for many tables simultaneously overwhelms cluster resources.

**Solution:** Stagger execution with delays between batches.

```bash
#!/bin/bash
# Batch statistics collection with staggered execution

# Define table list
TABLES=(
  "users"
  "orders"
  "products"
  "inventory"
  "shipments"
  "invoices"
  "payments"
  "reviews"
)

BATCH_SIZE=3
DELAY_SECONDS=60

# Process tables in batches
for ((i=0; i<${#TABLES[@]}; i+=BATCH_SIZE)); do
  batch=("${TABLES[@]:i:BATCH_SIZE}")

  echo "$(date): Starting batch: ${batch[@]}"

  # Execute batch in parallel
  for table in "${batch[@]}"; do
    echo "Creating statistics for $table..."
    cockroach sql -e "CREATE STATISTICS __auto__ FROM $table;" &
  done

  # Wait for batch to complete
  wait

  echo "$(date): Batch completed. Waiting $DELAY_SECONDS seconds..."
  sleep $DELAY_SECONDS
done

echo "$(date): All statistics collection jobs submitted"
```

**Customization:**
- `BATCH_SIZE`: Number of concurrent jobs (default 3, increase cautiously)
- `DELAY_SECONDS`: Delay between batches (default 60, increase for very large tables)

### Priority-Based Collection

**Pattern:** Refresh critical high-traffic tables first, then lower-priority tables.

```bash
#!/bin/bash
# Priority-based statistics refresh

# High-priority tables (critical OLTP tables)
HIGH_PRIORITY=(
  "orders"
  "transactions"
  "user_sessions"
)

# Medium-priority tables
MEDIUM_PRIORITY=(
  "users"
  "products"
  "inventory"
)

# Low-priority tables (analytics, reporting)
LOW_PRIORITY=(
  "audit_logs"
  "archived_orders"
  "reporting_summary"
)

refresh_tables() {
  local priority=$1
  shift
  local tables=("$@")

  echo "$(date): Refreshing $priority priority tables..."

  for table in "${tables[@]}"; do
    echo "  - $table"
    cockroach sql -e "CREATE STATISTICS __auto__ FROM $table;" &
  done

  wait
  echo "$(date): $priority priority complete"
}

# Execute in priority order
refresh_tables "HIGH" "${HIGH_PRIORITY[@]}"
sleep 120  # Longer delay after high-priority

refresh_tables "MEDIUM" "${MEDIUM_PRIORITY[@]}"
sleep 60

refresh_tables "LOW" "${LOW_PRIORITY[@]}"

echo "$(date): All statistics refreshed"
```

### Database-Level Collection

**Pattern:** Refresh all tables in specific database, one database at a time.

```bash
#!/bin/bash
# Refresh statistics for all tables in a database

DATABASE=$1

if [[ -z "$DATABASE" ]]; then
  echo "Usage: $0 <database_name>"
  exit 1
fi

echo "$(date): Fetching table list for database: $DATABASE"

# Get all tables in database
TABLES=$(cockroach sql --format=tsv -e "
  SELECT table_name
  FROM information_schema.tables
  WHERE table_schema = 'public'
    AND table_catalog = '$DATABASE'
    AND is_hidden = 'NO'
  ORDER BY table_name;
")

# Refresh statistics for each table
for table in $TABLES; do
  echo "$(date): Refreshing statistics for $DATABASE.$table"
  cockroach sql -e "CREATE STATISTICS __auto__ FROM $DATABASE.public.$table;" &

  # Wait every 5 tables to avoid overwhelming cluster
  job_count=$(jobs -p | wc -l)
  if [[ $job_count -ge 5 ]]; then
    echo "$(date): Waiting for jobs to complete..."
    wait
    sleep 30
  fi
done

wait
echo "$(date): All statistics refreshed for database: $DATABASE"
```

**Usage:**
```bash
./refresh_database_stats.sh production_db
```

### Progress Tracking Across Multiple Tables

**Pattern:** Track completion status for large batch operations.

```bash
#!/bin/bash
# Batch refresh with progress tracking

TABLES=(
  "table1"
  "table2"
  "table3"
  # ... many more tables
)

TOTAL=${#TABLES[@]}
COMPLETED=0

for table in "${TABLES[@]}"; do
  echo "$(date): Starting statistics collection for $table ($((COMPLETED+1))/$TOTAL)"

  # Submit job and capture job ID
  output=$(cockroach sql --format=tsv -e "CREATE STATISTICS __auto__ FROM $table; SELECT job_id FROM [SHOW JOBS] WHERE job_type = 'CREATE STATS' ORDER BY created DESC LIMIT 1;")
  job_id=$(echo "$output" | tail -n1)

  # Wait for job to complete
  while true; do
    status=$(cockroach sql --format=tsv -e "SELECT status FROM [SHOW JOBS] WHERE job_id = $job_id;" | tail -n1)

    if [[ "$status" == "succeeded" ]]; then
      COMPLETED=$((COMPLETED+1))
      echo "$(date): Completed $table ($COMPLETED/$TOTAL)"
      break
    elif [[ "$status" == "failed" ]]; then
      echo "$(date): FAILED $table - continuing..."
      COMPLETED=$((COMPLETED+1))
      break
    fi

    sleep 5
  done

  # Brief delay between tables
  sleep 10
done

echo "$(date): Batch refresh complete: $COMPLETED/$TOTAL tables processed"
```

## Best Practices Table

Summary of CREATE STATISTICS best practices by scenario:

| Scenario | Recommended Pattern | Key Considerations |
|----------|--------------------|--------------------|
| **Single table refresh** | `CREATE STATISTICS __auto__ FROM table;` | Simplest, automatic column selection |
| **Post-bulk-load** | Automatic per table, immediate execution | Run before downstream queries |
| **High-traffic period** | `AS OF SYSTEM TIME '-1h'` | Reduce live query impact |
| **Wide tables (>50 cols)** | Manual column selection | Faster, focus on queried columns |
| **Correlated columns** | Multi-column statistics | Required for accurate multi-predicate estimates |
| **Many tables (10+)** | Staggered batch execution | Avoid resource contention, 3-5 concurrent max |
| **Very large tables (>1B rows)** | Maintenance window, monitor job | Hours to complete, track progress |
| **Schema changes** | Manual refresh affected columns | Don't wait for automatic collection |
| **Partition maintenance** | Per-partition refresh | `WHERE partition_key >= ...` clause |

## Advanced Patterns

### Conditional Statistics Refresh

**Pattern:** Only refresh if drift exceeds threshold.

```bash
#!/bin/bash
# Conditional refresh based on drift detection

TABLE="orders"
DRIFT_THRESHOLD=20  # 20% drift threshold

# Get current row count
CURRENT_ROWS=$(cockroach sql --format=tsv -e "SELECT count(*) FROM $TABLE;")

# Get statistics row count
STATS_ROWS=$(cockroach sql --format=tsv -e "
  SELECT row_count
  FROM [SHOW STATISTICS FOR TABLE $TABLE]
  WHERE column_names = '{}'
  ORDER BY created DESC
  LIMIT 1;
")

# Calculate drift percentage
DRIFT=$(echo "scale=2; ($CURRENT_ROWS - $STATS_ROWS) / $STATS_ROWS * 100" | bc)
DRIFT_ABS=${DRIFT#-}  # Absolute value

echo "Current rows: $CURRENT_ROWS"
echo "Stats rows: $STATS_ROWS"
echo "Drift: $DRIFT%"

if (( $(echo "$DRIFT_ABS > $DRIFT_THRESHOLD" | bc -l) )); then
  echo "Drift exceeds threshold ($DRIFT_THRESHOLD%). Refreshing statistics..."
  cockroach sql -e "CREATE STATISTICS __auto__ FROM $TABLE;"
else
  echo "Drift within threshold. No refresh needed."
fi
```

### Partition-Aware Refresh

**Pattern:** For range-partitioned tables, refresh only recent partitions.

```sql
-- Scenario: events table partitioned by date
-- Only refresh last 30 days of partitions

CREATE STATISTICS recent_events_stats
FROM events
WHERE event_date >= CURRENT_DATE - INTERVAL '30 days';
```

**Rationale:** Historical partitions rarely change; avoid scanning entire multi-billion-row table.

**Verification:**
```sql
-- Check statistics created with WHERE clause
SELECT column_names, created, row_count
FROM [SHOW STATISTICS FOR TABLE events]
WHERE created > now() - INTERVAL '1 hour'
ORDER BY created DESC;
```

**Note:** CockroachDB does NOT create per-partition statistics automatically; this is a manual optimization.

### Statistics Refresh Validation

**Pattern:** Verify statistics refresh achieved desired outcome (drift reduction).

```sql
-- Before refresh: Check drift
WITH current_count AS (
  SELECT count(*) AS actual_rows FROM table_name
),
stats_count AS (
  SELECT row_count FROM [SHOW STATISTICS FOR TABLE table_name]
  WHERE column_names = '{}'
  ORDER BY created DESC
  LIMIT 1
)
SELECT
  c.actual_rows,
  s.row_count AS stats_rows,
  ABS(c.actual_rows - s.row_count) AS drift_absolute,
  ROUND(ABS(c.actual_rows - s.row_count)::NUMERIC / NULLIF(s.row_count, 0) * 100, 2) AS drift_pct
FROM current_count c, stats_count s;

-- Execute refresh
CREATE STATISTICS __auto__ FROM table_name;

-- After refresh: Verify drift reduced to near-zero
-- (Re-run drift query above)
```

**Expected result:** `drift_pct` should be <1% after successful refresh.

## Troubleshooting Statistics Collection

### Job Fails with Timeout

**Symptom:**
```sql
SELECT status, error FROM [SHOW JOBS] WHERE job_id = 123456789012345678;
-- status: failed
-- error: job timed out
```

**Solutions:**

1. **Retry during low-traffic period:**
   ```sql
   CREATE STATISTICS __auto__ FROM large_table;
   ```

2. **Use AS OF SYSTEM TIME to reduce contention:**
   ```sql
   CREATE STATISTICS __auto__ FROM large_table AS OF SYSTEM TIME '-1h';
   ```

3. **Increase timeout (requires admin):**
   ```sql
   SET CLUSTER SETTING sql.stats.automatic_collection.max_timeout = '2h';  -- Default 30m
   ```

### Job Runs Indefinitely

**Symptom:** Job shows 'running' for hours with minimal progress.

**Diagnosis:**
```sql
-- Check if table has high write volume
SELECT
  table_name,
  (SELECT count(*) FROM table_name) AS current_rows,  -- Replace dynamically
  job.fraction_completed
FROM [SHOW JOBS] job
WHERE job_id = 123456789012345678;
```

**Solutions:**

1. **Cancel and retry during maintenance window:**
   ```sql
   CANCEL JOB 123456789012345678;
   -- Wait for low-traffic period
   CREATE STATISTICS __auto__ FROM table_name;
   ```

2. **Use partition-aware refresh (if applicable):**
   ```sql
   CREATE STATISTICS recent_stats FROM table_name
   WHERE partition_key >= '2026-01-01';
   ```

### Statistics Not Improving Query Performance

**Symptom:** Created statistics, but EXPLAIN still shows poor plan.

**Diagnosis:**

1. **Verify statistics were actually created:**
   ```sql
   SELECT column_names, created
   FROM [SHOW STATISTICS FOR TABLE table_name]
   ORDER BY created DESC
   LIMIT 10;
   ```

2. **Check if query uses columns with statistics:**
   ```sql
   -- Example query
   EXPLAIN SELECT * FROM table_name WHERE column_x = 123;

   -- Verify column_x has statistics
   SELECT column_names, distinct_count
   FROM [SHOW STATISTICS FOR TABLE table_name]
   WHERE column_names = '{column_x}';
   ```

3. **Consider multi-column statistics:**
   ```sql
   -- If query filters on multiple correlated columns
   CREATE STATISTICS multi_col_stats ON column_x, column_y FROM table_name;
   ```

## Summary Checklist

Before executing CREATE STATISTICS in production:

- [ ] **Determine scope:** Single table, batch, or database-wide?
- [ ] **Choose pattern:** Automatic (`__auto__`), manual columns, or multi-column?
- [ ] **Check table size:** <10M rows (anytime), >10M rows (maintenance window)?
- [ ] **Resource planning:** How many concurrent jobs? Stagger execution?
- [ ] **Monitor jobs:** Have `SHOW JOBS` query ready for progress tracking
- [ ] **Cancellation plan:** Know how to cancel job if needed (CANCEL JOB)
- [ ] **Verification:** How will you confirm statistics were created successfully?
- [ ] **Validation:** Will you check drift reduction or query plan improvement?

**Quick reference:**
```sql
-- Most common pattern (recommended)
CREATE STATISTICS __auto__ FROM table_name;

-- Multi-column for correlated columns
CREATE STATISTICS stats_name ON col1, col2 FROM table_name;

-- Low-impact during high-traffic
CREATE STATISTICS __auto__ FROM table_name AS OF SYSTEM TIME '-1h';

-- Monitor job
SELECT job_id, status, fraction_completed
FROM [SHOW JOBS]
WHERE job_type = 'CREATE STATS' AND status = 'running';

-- Cancel if needed
CANCEL JOB <job_id>;
```

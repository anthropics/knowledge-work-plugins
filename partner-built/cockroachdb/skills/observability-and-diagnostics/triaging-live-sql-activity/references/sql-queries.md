# SQL Query Variations and Examples

This reference provides detailed SQL query variations for different triage scenarios. All queries are production-safe and read-only unless explicitly marked as cancellation operations.

## Query Variations by Time Threshold

### 30 Seconds Threshold (Fast OLTP Workloads)

```sql
-- Long-running queries (>30 seconds)
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, node_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE start < now() - INTERVAL '30 seconds'
ORDER BY start
LIMIT 50;
```

### 1 Minute Threshold

```sql
-- Long-running queries (>1 minute)
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, node_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE start < now() - INTERVAL '1 minute'
ORDER BY start
LIMIT 50;
```

### 10 Minutes Threshold

```sql
-- Long-running queries (>10 minutes)
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, node_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE start < now() - INTERVAL '10 minutes'
ORDER BY start
LIMIT 50;
```

### 30 Minutes Threshold (OLAP/Analytics)

```sql
-- Long-running queries (>30 minutes)
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, node_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE start < now() - INTERVAL '30 minutes'
ORDER BY start
LIMIT 50;
```

## Advanced Filtering Patterns

### Regex Pattern for Application Names

```sql
-- Filter by application name pattern
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, application_name, start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE application_name ~ '^payments-.*'  -- Regex pattern
  AND start < now() - INTERVAL '5 minutes'
ORDER BY start
LIMIT 50;
```

### IP Subnet Filtering

```sql
-- Sessions from specific IP subnet
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT session_id, user_name, application_name, client_address,
       active_query_start, substring(active_queries, 1, 200) AS active_queries_preview
FROM s
WHERE client_address LIKE '10.0.1.%'  -- /24 subnet
  OR client_address LIKE '192.168.%'  -- /16 subnet
ORDER BY active_query_start;
```

### Multi-Condition WHERE Clauses

```sql
-- Complex filtering: specific app, user, and duration
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, node_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE application_name IN ('payments-api', 'billing-api')
  AND user_name = 'app_user'
  AND start < now() - INTERVAL '10 minutes'
  AND distributed = true  -- Only distributed queries
ORDER BY start
LIMIT 50;
```

### Exclude Internal Queries

```sql
-- Filter out CockroachDB internal queries
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE application_name != '$ internal'  -- Exclude internal app
  AND user_name != 'node'               -- Exclude node user
  AND start < now() - INTERVAL '5 minutes'
ORDER BY start
LIMIT 50;
```

## Aggregation Queries

### Top N Longest Running Queries

```sql
-- Top 10 longest running queries right now
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
ORDER BY start ASC  -- Oldest first = longest running
LIMIT 10;
```

### Count by Application

```sql
-- Number of active queries per application
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT application_name,
       COUNT(*) AS num_queries,
       AVG(now() - start) AS avg_duration,
       MAX(now() - start) AS max_duration
FROM q
GROUP BY application_name
ORDER BY num_queries DESC;
```

### Count by User

```sql
-- Number of active queries per user
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT user_name,
       COUNT(*) AS num_queries,
       AVG(now() - start) AS avg_duration,
       MAX(now() - start) AS max_duration
FROM q
GROUP BY user_name
ORDER BY num_queries DESC;
```

### Count by Node

```sql
-- Number of active queries per node
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT node_id,
       COUNT(*) AS num_queries,
       AVG(now() - start) AS avg_duration,
       MAX(now() - start) AS max_duration
FROM q
GROUP BY node_id
ORDER BY num_queries DESC;
```

### Average/Max Durations by Application

```sql
-- Average and max query durations per application
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT application_name,
       COUNT(*) AS num_queries,
       AVG(now() - start) AS avg_duration,
       MAX(now() - start) AS max_duration,
       MIN(now() - start) AS min_duration
FROM q
WHERE start < now() - INTERVAL '1 minute'  -- Only queries >1 min
GROUP BY application_name
HAVING COUNT(*) > 5  -- Only apps with >5 active queries
ORDER BY avg_duration DESC;
```

## Transaction-Specific Queries

### High Retry Detection

```sql
-- Transactions with excessive retries (>10)
SELECT id AS txn_id, node_id, session_id, application_name,
       start, now() - start AS running_for,
       num_stmts, num_retries, num_auto_retries,
       substring(txn_string, 1, 200) AS txn_preview
FROM crdb_internal.cluster_transactions
WHERE num_retries > 10
ORDER BY num_retries DESC
LIMIT 50;
```

### Long-Running with Many Statements

```sql
-- Transactions running >5 minutes with >10 statements
SELECT id AS txn_id, node_id, session_id, application_name,
       start, now() - start AS running_for,
       num_stmts, num_retries,
       substring(txn_string, 1, 200) AS txn_preview
FROM crdb_internal.cluster_transactions
WHERE start < now() - INTERVAL '5 minutes'
  AND num_stmts > 10
ORDER BY start
LIMIT 50;
```

### Transactions by Retry Count Histogram

```sql
-- Histogram of transactions by retry count
SELECT
  CASE
    WHEN num_retries = 0 THEN '0 retries'
    WHEN num_retries BETWEEN 1 AND 5 THEN '1-5 retries'
    WHEN num_retries BETWEEN 6 AND 10 THEN '6-10 retries'
    WHEN num_retries > 10 THEN '>10 retries'
  END AS retry_bucket,
  COUNT(*) AS num_transactions
FROM crdb_internal.cluster_transactions
GROUP BY retry_bucket
ORDER BY retry_bucket;
```

### Contention Analysis

```sql
-- Applications with high average retry counts
SELECT application_name,
       COUNT(*) AS num_txns,
       AVG(num_retries) AS avg_retries,
       MAX(num_retries) AS max_retries,
       AVG(num_auto_retries) AS avg_auto_retries
FROM crdb_internal.cluster_transactions
WHERE start < now() - INTERVAL '5 minutes'
GROUP BY application_name
HAVING AVG(num_retries) > 3
ORDER BY avg_retries DESC;
```

## Batch Operations

### Generate Cancel Commands for Long Queries

```sql
-- Generate CANCEL QUERY statements for all queries >10 minutes
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT 'CANCEL QUERY ''' || query_id || ''';' AS cancel_command
FROM q
WHERE start < now() - INTERVAL '10 minutes'
ORDER BY start;
```

**Usage:**
1. Review the generated commands carefully
2. Copy and execute only the specific cancellations you approve
3. Do NOT blindly execute all generated commands

### Generate Cancel Commands for Specific App

```sql
-- Generate CANCEL QUERY statements for specific application
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT 'CANCEL QUERY ''' || query_id || ''';' AS cancel_command,
       user_name, now() - start AS running_for,
       substring(query, 1, 100) AS query_preview
FROM q
WHERE application_name = 'runaway-app'
  AND start < now() - INTERVAL '5 minutes'
ORDER BY start;
```

### Generate Cancel Session Commands

```sql
-- Generate CANCEL SESSION statements for long-idle sessions
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT 'CANCEL SESSION ''' || session_id || ''';' AS cancel_command,
       user_name, application_name, client_address,
       status, now() - session_start AS session_age
FROM s
WHERE status = 'idle'
  AND session_start < now() - INTERVAL '1 hour'
ORDER BY session_start;
```

## Session Analysis

### Sessions by Status

```sql
-- Count of sessions by status
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT status, COUNT(*) AS num_sessions
FROM s
GROUP BY status
ORDER BY num_sessions DESC;
```

### Long-Idle Sessions

```sql
-- Sessions idle for >30 minutes
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT session_id, user_name, application_name, client_address,
       status, session_start, now() - session_start AS session_age,
       substring(last_active_query, 1, 200) AS last_query_preview
FROM s
WHERE status = 'idle'
  AND session_start < now() - INTERVAL '30 minutes'
ORDER BY session_start
LIMIT 50;
```

### Sessions with Multiple Active Queries

```sql
-- Sessions running multiple queries simultaneously
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT session_id, user_name, application_name, client_address,
       active_queries, active_query_start,
       substring(active_queries, 1, 200) AS active_queries_preview
FROM s
WHERE active_queries ~ '.*\;.*'  -- Contains semicolon (multiple queries)
ORDER BY active_query_start;
```

## Full-Text Query Search

### Find Queries Containing Specific Table

```sql
-- Queries accessing specific table
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 500) AS query_preview
FROM q
WHERE query LIKE '%my_table_name%'
ORDER BY start
LIMIT 50;
```

### Find Queries with Specific SQL Pattern

```sql
-- Queries containing specific SQL pattern (e.g., JOIN)
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, user_name, application_name,
       start, now() - start AS running_for,
       substring(query, 1, 500) AS query_preview
FROM q
WHERE query ~ '.*JOIN.*'  -- Regex for JOIN
ORDER BY start
LIMIT 50;
```

## Notes

- All queries include `LIMIT` clauses to prevent overwhelming output
- Adjust time thresholds (`INTERVAL`) based on your workload characteristics
- Use `substring()` to prevent extremely long query text from cluttering output
- For large clusters, consider adding more aggressive filters (node_id, application_name) to reduce result set size
- Batch cancellation queries are for generating commands only - always review before executing

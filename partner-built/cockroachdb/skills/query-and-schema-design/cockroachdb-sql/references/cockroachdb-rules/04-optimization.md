# OPTIMIZATION

## Performance Patterns

### Query Hints
```sql
-- Force index usage
SELECT * FROM orders@orders_user_id_idx WHERE user_id = 1;

-- Force primary key scan
SELECT * FROM orders@primary WHERE id > 1000;

-- Force specific join type
SELECT * FROM orders
INNER HASH JOIN users ON orders.user_id = users.id;

SELECT * FROM orders
INNER MERGE JOIN users ON orders.user_id = users.id;

-- Disable automatic statistics
SET CLUSTER SETTING sql.stats.automatic_collection.enabled = false;

-- Force statistics refresh
CREATE STATISTICS stats_name ON column FROM table;
```

### Range Operations
```sql
-- Split ranges at specific values (admin operation)
ALTER TABLE orders SPLIT AT VALUES (1000), (2000), (3000);

-- Split with expiration
ALTER TABLE events SPLIT AT VALUES ('2024-01-01')
  WITH EXPIRATION '2024-02-01';

-- Unsplit ranges
ALTER TABLE orders UNSPLIT AT VALUES (1000);
ALTER TABLE orders UNSPLIT ALL;

-- Scatter data (redistribute)
ALTER TABLE large_table SCATTER;

-- Scatter with specific range
ALTER TABLE orders SCATTER FROM (1) TO (1000);
```

### Zone Configuration
```sql
-- Configure replication
ALTER TABLE important_data CONFIGURE ZONE USING
  num_replicas = 5,
  constraints = '{"+region=us-east": 2, "+region=us-west": 2}',
  lease_preferences = '[[+region=us-east]]';

-- Configure garbage collection
ALTER TABLE logs CONFIGURE ZONE USING
  gc.ttlseconds = 3600;  -- 1 hour

-- Configure range size
ALTER TABLE large_table CONFIGURE ZONE USING
  range_max_bytes = 134217728,  -- 128MB
  range_min_bytes = 16777216;   -- 16MB
```

### Query Optimization Techniques

#### Partial Indexes
```sql
-- Index only active records
CREATE INDEX idx_active_users ON users (email)
WHERE deleted_at IS NULL;

-- Index recent data
CREATE INDEX idx_recent_events ON events (created_at)
WHERE created_at > '2024-01-01';
```

## Common Anti-Patterns

### DON'T Use These
```sql
-- AUTO_INCREMENT (not supported)
id INT AUTO_INCREMENT  -- ❌ Will fail

-- TRUNCATE with CASCADE on production
TRUNCATE TABLE users CASCADE;  -- ❌ Dangerous

-- Unqualified DELETE
DELETE FROM table;  -- ❌ Add WHERE true if intentional

-- SELECT * in production code
SELECT * FROM large_table;  -- ❌ Specify columns

-- Large OFFSET pagination
SELECT * FROM table LIMIT 20 OFFSET 10000;  -- ❌ Inefficient

-- XA / Prepared Transactions (not fully supported)
PREPARE TRANSACTION 'tx_id';  -- ❌ Can cause stuck transactions and row locks
COMMIT PREPARED 'tx_id';      -- ❌ Not fully supported, undocumented
ROLLBACK PREPARED 'tx_id';    -- ❌ Use outbox pattern for cross-DB writes instead
```

### DO Use These Instead
```sql
-- Safe deletion
DELETE FROM table WHERE condition;  -- ✅
DELETE FROM table WHERE true;  -- ✅ Explicit full delete

-- Specific columns
SELECT id, name, email FROM users;  -- ✅

-- Keyset pagination
SELECT * FROM posts
WHERE (created_at, id) < ($1, $2)
ORDER BY created_at DESC, id DESC
LIMIT 20;  -- ✅

-- For cross-database consistency instead of XA/Prepared Transaction, use the Outbox pattern:
--- 1. Write both the business data and an outbox event in one CockroachDB transaction
BEGIN;
  INSERT INTO orders (id, user_id, total) VALUES ($1, $2, $3);
  INSERT INTO outbox_events (id, aggregate_id, event_type, payload)
    VALUES (gen_random_uuid(), $1, 'order_created', $4::JSONB);
COMMIT; --- ✅

--- 2. Use a changefeed to deliver outbox events to the external system (e.g. Kafka → MongoDB)
CREATE CHANGEFEED FOR TABLE outbox_events
  INTO 'kafka://broker:9092'
  WITH format = 'json', updated, resolved = '10s'; --- ✅

```

## Performance Best Practices

### 1. Index Strategy
- Create indexes for WHERE, JOIN, and ORDER BY columns
- Use hash-sharded indexes for sequential data
- Monitor unused indexes and drop them

### 2. Data Distribution
- Consider hash-sharded indexes for time-series data
- Split ranges manually for known access patterns
- Use zone configs for geo-distribution

### 3. Connection Management
- Use connection pooling
- Set appropriate statement timeout

### 5. Monitoring
```sql
-- Check slow queries
SELECT * FROM crdb_internal.cluster_queries
WHERE start > now() - INTERVAL '5 minutes'
ORDER BY start DESC;

-- Check table statistics
SHOW STATISTICS FOR TABLE table_name;

-- Check index usage
SELECT * FROM crdb_internal.index_usage_statistics
WHERE table_name = 'your_table';

-- Explain query plan
EXPLAIN (VERBOSE) SELECT ...;
EXPLAIN ANALYZE SELECT ...;
```

## Query Plan Analysis

### Understanding EXPLAIN
```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Explain with statistics
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Explain with all options
EXPLAIN (ANALYZE, VERBOSE, TYPES, DISTSQL)
SELECT * FROM users WHERE email = 'test@example.com';

-- Check for full table scans
EXPLAIN SELECT * FROM large_table;
-- Look for "full scan" in output
```

### Common Plan Issues
1. **Full table scans** - Add appropriate indexes
2. **Hash joins on large tables** - Consider merge joins
3. **High network latency** - Use zone configs
4. **Excessive round trips** - Batch operations
5. **Lock contention** - Reduce transaction scope

## Hardware and Deployment

### Resource Recommendations
- **CPU**: 4-8 cores per node minimum
- **Memory**: 8-16 GB per node minimum
- **Storage**: SSDs strongly recommended
- **Network**: Low latency between nodes

### Cluster Sizing
```sql
-- Check cluster capacity
SELECT * FROM crdb_internal.kv_node_status;

-- Check range distribution
SELECT * FROM crdb_internal.ranges;

-- Check replication status
SHOW RANGES FROM TABLE table_name;
```

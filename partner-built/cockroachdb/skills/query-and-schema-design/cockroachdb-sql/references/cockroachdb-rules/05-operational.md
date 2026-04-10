# OPERATIONAL

## Admin Queries

### SHOW Commands
```sql
-- Table information
SHOW TABLES;
SHOW TABLES FROM database;
SHOW CREATE TABLE table_name;
SHOW COLUMNS FROM table_name;

-- Index information
SHOW INDEXES FROM table_name;
SHOW INDEX FROM table_name;

-- Range information
SHOW RANGES FROM TABLE table_name;
SHOW RANGE FOR ROW (1, 'value') FROM table_name;

-- Zone configurations
SHOW ZONE CONFIGURATION FOR TABLE table_name;
SHOW ZONE CONFIGURATION FOR INDEX table_name@index_name;
SHOW ZONE CONFIGURATION FOR PARTITION partition_name;

-- Statistics
SHOW STATISTICS FOR TABLE table_name;
SHOW STATISTICS USING JSON FOR TABLE table_name;

-- Jobs and sessions
SHOW JOBS;
SHOW JOBS FOR SCHEDULES;
SHOW SESSIONS;
SHOW QUERIES;

-- Performance insights
SHOW FULL TABLE SCANS;
SHOW TRACE FOR SESSION;
SHOW TRACE FOR SELECT * FROM table;

-- Cluster settings
SHOW CLUSTER SETTING version;
SHOW ALL CLUSTER SETTINGS;

-- Experimental features
SHOW EXPERIMENTAL_FINGERPRINTS FROM TABLE table_name;
SHOW EXPERIMENTAL_REPLICA LOCALITIES FROM TABLE table_name;
```

### Database Management
```sql
-- Create/Drop database
CREATE DATABASE IF NOT EXISTS mydb;
DROP DATABASE IF EXISTS mydb CASCADE;

-- Change database
USE mydb;
SET database = mydb;

-- Show current database
SELECT current_database();
SHOW database;

-- Database size
SELECT pg_database_size('mydb');
SELECT pg_size_pretty(pg_database_size('mydb'));
```

### User and Role Management
```sql
-- Create users
CREATE USER username WITH PASSWORD 'password';
CREATE USER readonly_user;

-- Create roles
CREATE ROLE admin;
CREATE ROLE readonly;

-- Grant privileges
GRANT ALL ON DATABASE mydb TO admin;
GRANT SELECT ON TABLE users TO readonly;
GRANT USAGE ON SCHEMA public TO username;

-- Grant role membership
GRANT admin TO username;

-- Revoke privileges
REVOKE INSERT ON TABLE users FROM username;
REVOKE admin FROM username;

-- Alter user
ALTER USER username WITH PASSWORD 'newpassword';
ALTER USER username WITH NOCREATEDB;

-- Show grants
SHOW GRANTS ON DATABASE mydb;
SHOW GRANTS ON TABLE users;
SHOW GRANTS FOR username;
```

## EXPLAIN Plans

### Basic Explain
```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Verbose explain (detailed info)
EXPLAIN (VERBOSE) SELECT * FROM orders;

-- Analyze actual execution
EXPLAIN ANALYZE SELECT * FROM large_table;

-- Distribution info
EXPLAIN (DISTSQL) SELECT * FROM distributed_table;

-- Vectorized execution
EXPLAIN (VEC) SELECT * FROM table;

-- All options combined
EXPLAIN (VERBOSE, DISTSQL, VEC, ANALYZE, TYPES)
SELECT * FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';
```

### Reading Explain Output
```sql
-- Look for these warning signs:
-- • "full scan" - Missing index
-- • "hash join" on large tables - Consider merge join
-- • High "time" values - Slow operations
-- • Large "rows" counts - Consider filtering earlier
-- • "distributed" false - Not using distribution

-- Example problem query
EXPLAIN ANALYZE SELECT * FROM large_table WHERE unindexed_column = 'value';
-- Shows: full scan, high time, many rows read
```

## Backup and Restore (Enterprise)

### Backup Operations
```sql
-- Full database backup
BACKUP DATABASE mydb INTO 'nodelocal://1/backup';

-- Multiple databases
BACKUP DATABASE db1, db2 INTO 's3://bucket/backup';

-- Specific tables
BACKUP TABLE users, orders INTO 's3://bucket/backup';

-- Incremental backup (after initial full backup)
BACKUP TABLE users INTO LATEST IN 's3://bucket/backup';

-- Backup with options
BACKUP DATABASE mydb INTO 's3://bucket/backup'
  WITH revision_history,        -- Include revision history
       detached,                 -- Run in background
       encryption_passphrase = 'secret';  -- Encrypt backup

-- Backup as of specific time
BACKUP TABLE users AS OF SYSTEM TIME '-1h' INTO 'path';

-- Scheduled backups
CREATE SCHEDULE daily_backup
  FOR BACKUP DATABASE mydb INTO 's3://bucket/backup'
  RECURRING '@daily'
  WITH SCHEDULE OPTIONS first_run = now();
```

### Restore Operations
```sql
-- Restore entire database
RESTORE DATABASE mydb FROM 's3://bucket/backup';

-- Restore specific tables
RESTORE TABLE users, orders FROM 's3://bucket/backup';

-- Restore with new database name
RESTORE DATABASE mydb FROM 's3://bucket/backup'
  WITH new_db_name = 'mydb_restored';

-- Point-in-time restore (requires revision_history)
RESTORE DATABASE mydb FROM 's3://bucket/backup'
  AS OF SYSTEM TIME '2024-01-01 10:00:00';

-- Restore specific backup from incremental chain
RESTORE DATABASE mydb FROM 's3://bucket/backup'
  AS OF SYSTEM TIME '-2d';

-- Restore with options
RESTORE DATABASE mydb FROM 's3://bucket/backup'
  WITH skip_missing_foreign_keys,
       skip_missing_sequences,
       encryption_passphrase = 'secret';
```

### Backup Management
```sql
-- Show backup contents
SHOW BACKUP FROM 's3://bucket/backup';

-- Show latest backup in location
SHOW BACKUP LATEST IN 's3://bucket/backup';

-- Validate backup integrity
SHOW BACKUP FROM 's3://bucket/backup' WITH check_files;

-- Show backup schedule
SHOW SCHEDULES;
SHOW SCHEDULE 123456;

-- Pause/Resume backup schedule
PAUSE SCHEDULE 123456;
RESUME SCHEDULE 123456;

-- Drop backup schedule
DROP SCHEDULE 123456;
```

## Changefeeds (Enterprise CDC)

### Create Changefeeds
```sql
-- Basic changefeed to Kafka
CREATE CHANGEFEED FOR TABLE users, orders
  INTO 'kafka://broker:9092';

-- Changefeed with Kafka options
CREATE CHANGEFEED FOR TABLE users
  INTO 'kafka://broker:9092'
  WITH format = 'json',
       confluent_schema_registry = 'http://schema-registry:8081',
       updated,                    -- Include previous values
       resolved = '10s',          -- Emit resolved timestamps
       diff,                      -- Show before/after
       envelope = 'wrapped';      -- Wrapped format

-- Changefeed to cloud storage
CREATE CHANGEFEED FOR TABLE orders
  INTO 's3://bucket/changefeed'
  WITH format = 'avro',
       compression = 'gzip',
       file_size = '128MB';

-- Changefeed to webhook
CREATE CHANGEFEED FOR TABLE events
  INTO 'webhook-https://myapp.com/webhook'
  WITH webhook_auth_header = 'Bearer token';

-- Filtered changefeed
CREATE CHANGEFEED FOR TABLE users
  INTO 'kafka://broker:9092'
  WITH schema_change_policy = 'stop',
       initial_scan = 'no',
       on_update = 'ONLY created_at';
```

### Manage Changefeeds
```sql
-- Show changefeed jobs
SHOW CHANGEFEED JOBS;
SELECT * FROM crdb_internal.jobs WHERE job_type = 'CHANGEFEED';

-- Pause changefeed
PAUSE JOB 123456789;

-- Resume changefeed
RESUME JOB 123456789;

-- Cancel changefeed
CANCEL JOB 123456789;

-- Alter changefeed (limited)
-- Must cancel and recreate for most changes
```

## Monitoring and Diagnostics

### Performance Monitoring
```sql
-- Active queries
SELECT query, start, application_name
FROM crdb_internal.cluster_queries
WHERE start > now() - INTERVAL '5 minutes'
ORDER BY start DESC;

-- Slow queries
SELECT query, start, exec_latency
FROM crdb_internal.cluster_queries
WHERE exec_latency > INTERVAL '1 second'
ORDER BY exec_latency DESC;

-- Table sizes
SELECT
  table_name,
  pg_size_pretty(pg_table_size(table_name::regclass)) as size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_table_size(table_name::regclass) DESC;

-- Index usage
SELECT * FROM crdb_internal.index_usage_statistics
WHERE table_name = 'your_table';

-- Connection info
SELECT * FROM crdb_internal.cluster_sessions;
```

### System Tables
```sql
-- Node status
SELECT * FROM crdb_internal.kv_node_status;

-- Range information
SELECT * FROM crdb_internal.ranges;
SELECT * FROM crdb_internal.ranges_no_leases;

-- Jobs history
SELECT * FROM crdb_internal.jobs;
SELECT * FROM system.jobs;

-- Schema changes
SELECT * FROM crdb_internal.schema_changes;

-- Transaction statistics
SELECT * FROM crdb_internal.transaction_statistics;

-- Statement statistics
SELECT * FROM crdb_internal.statement_statistics;
```

### Cluster Health
```sql
-- Check cluster version
SELECT version();
SHOW CLUSTER SETTING version;

-- Check node liveness
SELECT node_id, is_live, updated_at
FROM crdb_internal.kv_node_liveness;

-- Check critical settings
SHOW CLUSTER SETTING kv.range_merge.queue_enabled;
SHOW CLUSTER SETTING kv.range_split.by_load_enabled;
SHOW CLUSTER SETTING admission.kv.enabled;

-- Check replication status
SELECT range_id, lease_holder, replicas
FROM crdb_internal.ranges
WHERE database_name = 'mydb';

-- Check for under-replicated ranges
SELECT * FROM crdb_internal.ranges
WHERE array_length(replicas, 1) < 3;
```

## Maintenance Operations

### Statistics Management
```sql
-- Create table statistics
CREATE STATISTICS stats_name ON column1, column2 FROM table_name;

-- Delete statistics
DELETE FROM system.table_statistics
WHERE name = 'stats_name';

-- Force statistics collection
SET CLUSTER SETTING sql.stats.automatic_collection.enabled = true;
ANALYZE table_name;
```

### Compaction
```sql
-- Manual compaction (use carefully)
ALTER TABLE table_name EXPERIMENTAL_RELOCATE
  SELECT ARRAY[1,2,3], pk FROM table_name;

-- Scatter table (redistribute data)
ALTER TABLE table_name SCATTER;
```

### Schema Changes
```sql
-- Online schema changes (non-blocking)
ALTER TABLE users ADD COLUMN new_field STRING DEFAULT '';

-- Show schema change progress
SHOW JOBS WHEN COMPLETE VALUES (job_id);

-- Cancel schema change
CANCEL JOB job_id;

-- Validate constraints
ALTER TABLE users VALIDATE CONSTRAINT constraint_name;
```
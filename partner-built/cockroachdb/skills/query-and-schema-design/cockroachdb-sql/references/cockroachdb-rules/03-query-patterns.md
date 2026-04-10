# QUERY PATTERNS

## Time Travel Queries (AS OF SYSTEM TIME)

### Historical Data Access
```sql
-- Query data from 1 hour ago
SELECT * FROM orders AS OF SYSTEM TIME '-1h';

-- Query at specific timestamp (the timestamp must be within ttlseconds in the replication zone)
SELECT * FROM users AS OF SYSTEM TIME '2024-01-01T10:00:00';

-- Query with follower reads (read from replicas)
SELECT * FROM products AS OF SYSTEM TIME follower_read_timestamp();

-- Bounded staleness reads
SELECT * FROM inventory
  AS OF SYSTEM TIME with_max_staleness(INTERVAL '10s');

SELECT * FROM inventory
  AS OF SYSTEM TIME with_min_timestamp(now() - INTERVAL '5s');

-- Use in JOINs
SELECT * FROM
  orders AS OF SYSTEM TIME '-1h' o
  JOIN users AS OF SYSTEM TIME '-1h' u ON o.user_id = u.id;

-- Use in backups
BACKUP TABLE users AS OF SYSTEM TIME '-10m' INTO 'path';

-- Use in exports
EXPORT INTO CSV 'path' FROM SELECT * FROM table
  AS OF SYSTEM TIME '-30m';
```

## Window Functions

### Ranking and Numbering
```sql
-- Row numbering
SELECT
  ROW_NUMBER() OVER (ORDER BY created_at DESC) as rn,
  *
FROM posts;

-- Ranking with partitions
SELECT
  user_id,
  score,
  RANK() OVER (PARTITION BY user_id ORDER BY score DESC) as rank,
  DENSE_RANK() OVER (PARTITION BY user_id ORDER BY score DESC) as dense_rank,
  PERCENT_RANK() OVER (ORDER BY score) as percentile
FROM user_scores;

-- NTILE for bucketing
SELECT
  price,
  NTILE(4) OVER (ORDER BY price) as price_quartile
FROM products;
```

### Analytics
```sql
-- Running totals
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
FROM transactions;

-- Moving averages
SELECT
  date,
  value,
  AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day
FROM metrics;

-- Lead/Lag for comparisons
SELECT
  date,
  value,
  LAG(value, 1) OVER (ORDER BY date) as prev_value,
  LEAD(value, 1) OVER (ORDER BY date) as next_value,
  value - LAG(value, 1) OVER (ORDER BY date) as change
FROM metrics;

-- First/Last values
SELECT
  user_id,
  FIRST_VALUE(login_time) OVER (PARTITION BY user_id ORDER BY login_time) as first_login,
  LAST_VALUE(login_time) OVER (PARTITION BY user_id ORDER BY login_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_login
FROM user_sessions;
```

## JSON Operations

### JSON Operators
```sql
data JSONB NOT NULL DEFAULT '{}'::JSONB

-- Extract value (as JSON)
SELECT data->'field' FROM table;

-- Extract value (as text)
SELECT data->>'field' FROM table;

-- Extract nested value by path
SELECT data#>'{address,city}' FROM users;
SELECT data#>>'{address,city}' FROM users;  -- As text

-- Check key existence
SELECT * FROM table WHERE data ? 'key';

-- Check if all keys exist
SELECT * FROM table WHERE data ?& ARRAY['key1', 'key2'];

-- Check if any key exists
SELECT * FROM table WHERE data ?| ARRAY['key1', 'key2'];

-- Containment checks
SELECT * FROM table WHERE data @> '{"status": "active"}';
SELECT * FROM table WHERE '{"status": "active"}' <@ data;
```

### JSON Manipulation
```sql
-- Update JSON
UPDATE table SET data = jsonb_set(data, '{path,to,field}', '"new_value"');

-- Remove field
UPDATE table SET data = data - 'field_to_remove';

-- Remove nested field
UPDATE table SET data = data #- '{path,to,field}';

-- Concatenate JSON
UPDATE table SET data = data || '{"new_field": "value"}';

-- Build JSON
SELECT jsonb_build_object(
  'id', id,
  'name', name,
  'metadata', jsonb_build_array(tag1, tag2, tag3)
) FROM users;
```

### JSON Indexing
```sql
-- General inverted index
CREATE INVERTED INDEX ON table(json_column);

-- Index specific path
CREATE INDEX ON table((json_column->>'specific_field'));

-- Expression index for complex queries
CREATE INDEX ON table((json_column->'user'->>'id'));
```

## Array Operations

### Array Basics
```sql
-- Array column definition
tags STRING[]              -- Array of strings
numbers INT8[]            -- Array of integers
matrix FLOAT8[][]         -- 2D array (limited support)

-- Array literals
INSERT INTO table (tags) VALUES (ARRAY['tag1', 'tag2']);
INSERT INTO table (tags) VALUES ('{tag1,tag2}'::STRING[]);

-- Array operations
SELECT * FROM posts WHERE tags @> ARRAY['cockroachdb'];  -- Contains
SELECT * FROM posts WHERE ARRAY['db'] <@ tags;          -- Contained by
SELECT * FROM posts WHERE tags && ARRAY['sql', 'nosql']; -- Overlap
```

### Array Functions
```sql
-- Array length
SELECT array_length(tags, 1) FROM posts;

-- Unnest arrays
SELECT unnest(tags) as tag FROM posts;

-- Array aggregation
SELECT user_id, array_agg(tag ORDER BY tag) as all_tags
FROM user_tags
GROUP BY user_id;

-- Array position
SELECT array_position(tags, 'sql') FROM posts;

-- Array to string
SELECT array_to_string(tags, ', ') as tag_list FROM posts;

-- String to array
SELECT string_to_array('a,b,c', ',');
```

### Array with ORDINALITY
```sql
-- Add row numbers to array elements
SELECT * FROM unnest(ARRAY['a', 'b', 'c']) WITH ORDINALITY;

SELECT value, row_number
FROM unnest(ARRAY[10, 20, 30]) WITH ORDINALITY
  AS t(value, row_number);

-- Expand JSON array with positions
SELECT row_number, value
FROM jsonb_array_elements_text('["a","b","c"]'::JSONB) WITH ORDINALITY
  AS t(value, row_number);
```

## Common Table Expressions (CTEs)

### Basic CTE
```sql
WITH user_stats AS (
  SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent
  FROM orders
  GROUP BY user_id
)
SELECT u.*, s.order_count, s.total_spent
FROM users u
JOIN user_stats s ON u.id = s.user_id;
```

### Multiple CTEs
```sql
WITH
recent_orders AS (
  SELECT * FROM orders WHERE created_at > now() - INTERVAL '30 days'
),
order_totals AS (
  SELECT user_id, SUM(total) as month_total
  FROM recent_orders
  GROUP BY user_id
),
top_users AS (
  SELECT user_id FROM order_totals WHERE month_total > 1000
)
SELECT u.*
FROM users u
JOIN top_users t ON u.id = t.user_id;
```

### Recursive CTE
```sql
WITH RECURSIVE category_tree AS (
  -- Base case: root categories
  SELECT id, name, parent_id, 0 as level,
         ARRAY[id] as path
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  -- Recursive case: child categories
  SELECT c.id, c.name, c.parent_id, ct.level + 1,
         ct.path || c.id
  FROM categories c
  JOIN category_tree ct ON c.parent_id = ct.id
  WHERE NOT c.id = ANY(ct.path)  -- Prevent cycles
)
SELECT * FROM category_tree ORDER BY level, name;
```

### Materialized CTEs
```sql
-- Force materialization (prevent optimization)
WITH materialized_cte AS MATERIALIZED (
  SELECT expensive_computation() as result
  FROM large_table
)
SELECT * FROM materialized_cte;

-- Not materialized (optimizer can inline)
WITH not_materialized AS NOT MATERIALIZED (
  SELECT * FROM small_table
)
SELECT * FROM not_materialized;
```

## Special Operators

### Text Search
```sql
-- Text search match
SELECT * FROM documents
WHERE to_tsvector('english', content) @@ to_tsquery('database & sql');

-- Create text search index
CREATE INDEX idx_fts ON documents USING GIN(to_tsvector('english', content));

-- Text search with ranking
SELECT *, ts_rank(to_tsvector('english', content), query) as rank
FROM documents,
     to_tsquery('database & sql') query
WHERE to_tsvector('english', content) @@ query
ORDER BY rank DESC;
```

### Spatial/Geometric
```sql
-- Distance between points
SELECT location1 <-> location2 as distance FROM places;

-- Check overlap
SELECT * FROM regions WHERE boundary && $1;

-- Containment
SELECT * FROM locations WHERE point <@ polygon;
SELECT * FROM zones WHERE polygon @> point;
```

### Network Operations
```sql
-- IP address containment
SELECT * FROM connections WHERE ip_address << '192.168.0.0/16';
SELECT * FROM subnets WHERE '192.168.1.100'::INET << subnet;

-- IP contains or equals
SELECT * FROM networks WHERE network >>= '10.0.0.0/24';
```

### Vector Operations (AI/ML)
```sql
-- Cosine similarity (normalized)
SELECT * FROM documents
ORDER BY embedding <=> $1::VECTOR
LIMIT 10;

-- Inner product similarity
SELECT * FROM items
ORDER BY features <#> query_vector
LIMIT 5;

-- L2 (Euclidean) distance
SELECT * FROM vectors
ORDER BY vec <-> $1::VECTOR
LIMIT 10;
```

## System Functions

### CockroachDB-Specific
```sql
-- Generate UUID
SELECT gen_random_uuid();

-- Cluster-wide timestamp
SELECT cluster_logical_timestamp();

-- Unique row ID
SELECT unique_rowid();

-- MVCC timestamp
SELECT crdb_internal_mvcc_timestamp FROM table;

-- Follower read timestamp
SELECT follower_read_timestamp();

-- Pretty size formatting
SELECT pg_size_pretty(pg_database_size('mydb'));
```

### Session Information
```sql
-- Current database
SELECT current_database();

-- Current user
SELECT current_user();

-- Current schema
SELECT current_schema();

-- All current schemas
SELECT current_schemas(true);

-- Session user
SELECT session_user();
```

## Type Casting

### Casting Syntax
```sql
-- PostgreSQL-style (preferred)
expression::type
'2024-01-01'::DATE
'123'::INT8
array_col::STRING[]
'{"key": "value"}'::JSONB

-- SQL standard
CAST(expression AS type)
CAST('2024-01-01' AS DATE)
CAST('123' AS INT8)

-- Triple-colon for forcing precedence
now():::TIMESTAMPTZ
'value':::STRING
```

### Common Conversions
```sql
-- String to numeric
'123'::INT8
'123.45'::DECIMAL

-- Numeric to string
123::STRING
CAST(price AS STRING)

-- Date/time conversions
'2024-01-01'::DATE
'2024-01-01 10:00:00'::TIMESTAMPTZ
now()::DATE  -- Strip time

-- JSON conversions
'{"key": "value"}'::JSONB
row_to_json(table_name)
```

## Common Query Patterns

### Find Recent Items
```sql
-- Basic recent query
SELECT * FROM items
WHERE created_at > now() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 100;

-- With index hint
SELECT * FROM items@items_created_at_idx
WHERE created_at > now() - INTERVAL '7 days';
```

### Existence Checks
```sql
-- Efficient existence check
SELECT EXISTS(
  SELECT 1 FROM users WHERE email = 'test@example.com'
);

-- Count with limit (for "any exist")
SELECT COUNT(*) > 0 as has_records FROM (
  SELECT 1 FROM large_table LIMIT 1
) t;
```

### Get or Create
```sql
-- Insert if not exists, return existing or new
WITH ins AS (
  INSERT INTO users (email, name)
  VALUES ('test@example.com', 'Test')
  ON CONFLICT (email) DO NOTHING
  RETURNING *
)
SELECT * FROM ins
UNION ALL
SELECT * FROM users WHERE email = 'test@example.com'
LIMIT 1;
```

### Pagination

#### Offset Pagination
```sql
-- Simple but inefficient for large offsets
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 40;
```

#### Keyset Pagination
```sql
-- Efficient for large datasets
-- First page
SELECT * FROM posts
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Next pages
SELECT * FROM posts
WHERE (created_at, id) < ('2024-01-01 10:00:00', 'last-id-from-previous-page')
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

### Bulk Operations
```sql
-- Bulk insert with returning
INSERT INTO items (id, name, price) VALUES
  (gen_random_uuid(), 'Item 1', 10.99),
  (gen_random_uuid(), 'Item 2', 20.99),
  (gen_random_uuid(), 'Item 3', 30.99)
RETURNING id;

-- Bulk update with CASE
UPDATE items SET
  price = CASE id
    WHEN '123' THEN 10.99
    WHEN '456' THEN 20.99
    WHEN '789' THEN 30.99
  END,
  updated_at = now()
WHERE id IN ('123', '456', '789');

-- Bulk delete with subquery
DELETE FROM old_records
WHERE id IN (
  SELECT id FROM old_records
  WHERE created_at < '2023-01-01'
  LIMIT 1000
);
```

### Hierarchical Data
```sql
-- Recursive CTE for tree structures
WITH RECURSIVE tree AS (
  SELECT id, parent_id, name, 0 as depth,
         ARRAY[id] as path,
         name as full_path
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  SELECT c.id, c.parent_id, c.name, t.depth + 1,
         t.path || c.id,
         t.full_path || ' > ' || c.name
  FROM categories c
  JOIN tree t ON c.parent_id = t.id
  WHERE NOT c.id = ANY(t.path)  -- Prevent cycles
)
SELECT * FROM tree ORDER BY path;
```

### Deduplication
```sql
-- Remove duplicates keeping newest
DELETE FROM events
WHERE id NOT IN (
  SELECT DISTINCT ON (user_id, event_type)
    id
  FROM events
  ORDER BY user_id, event_type, created_at DESC
);

-- Using window function
WITH duplicates AS (
  SELECT id,
    ROW_NUMBER() OVER (
      PARTITION BY user_id, event_type
      ORDER BY created_at DESC
    ) as rn
  FROM events
)
DELETE FROM events
WHERE id IN (
  SELECT id FROM duplicates WHERE rn > 1
);
```
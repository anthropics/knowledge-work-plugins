# DML OPERATIONS

## INSERT Patterns

### Single and Multi-Row Inserts
```sql
-- Single row insert
INSERT INTO users (email, name) VALUES ('test@example.com', 'Test');

-- Multi-row insert (efficient)
INSERT INTO users (email, name) VALUES
  ('user1@example.com', 'User 1'),
  ('user2@example.com', 'User 2'),
  ('user3@example.com', 'User 3');

-- Insert with RETURNING
INSERT INTO users (email) VALUES ('new@example.com')
  RETURNING id, created_at;

-- Insert with RETURNING NOTHING
INSERT INTO logs (data) VALUES ('log entry') RETURNING NOTHING;

-- Insert from SELECT
INSERT INTO archived_orders
  SELECT * FROM orders WHERE created_at < '2023-01-01';
```

## UPSERT Operations

### Native UPSERT vs INSERT ON CONFLICT
```sql
-- Native UPSERT
UPSERT INTO inventory (product_id, quantity) VALUES (1, 100);

-- INSERT ON CONFLICT for conditional logic
INSERT INTO users (id, email, name) VALUES (1, 'new@example.com', 'New')
  ON CONFLICT (id)
  DO UPDATE SET
    email = EXCLUDED.email,
    name = EXCLUDED.name,
    updated_at = now();

-- ON CONFLICT with WHERE clause
INSERT INTO settings (key, value) VALUES ('theme', 'dark')
  ON CONFLICT (key)
  DO UPDATE SET value = EXCLUDED.value
  WHERE settings.updated_at < EXCLUDED.updated_at;

-- ON CONFLICT DO NOTHING
INSERT INTO users (email) VALUES ('exists@example.com')
  ON CONFLICT (email) DO NOTHING;

-- ON CONFLICT on constraint
INSERT INTO table VALUES (...)
  ON CONFLICT ON CONSTRAINT constraint_name
  DO UPDATE SET ...;
```

## UPDATE Patterns

### Efficient Updates
```sql
-- Basic update with RETURNING
UPDATE users
  SET status = 'active', updated_at = now()
  WHERE id = $1
  RETURNING *;

-- Update with RETURNING NOTHING
UPDATE large_table
  SET flag = true
  WHERE condition
  RETURNING NOTHING;

-- Update with FROM clause
UPDATE orders o
  SET total = s.sum_amount
  FROM (
    SELECT order_id, SUM(amount) as sum_amount
    FROM order_items
    GROUP BY order_id
  ) s
  WHERE o.id = s.order_id;

-- Batch update with LIMIT
UPDATE events
  SET processed = true
  WHERE processed = false
  ORDER BY created_at
  LIMIT 1000;
```

## DELETE Patterns

### Safe Deletions
```sql
-- Delete with RETURNING
DELETE FROM users WHERE id = $1 RETURNING *;

-- Delete with RETURNING NOTHING
DELETE FROM logs WHERE created_at < '2023-01-01' RETURNING NOTHING;

-- Batch delete with LIMIT
DELETE FROM old_records
  WHERE created_at < '2023-01-01'
  LIMIT 1000;

-- Delete with USING clause
DELETE FROM order_items oi
USING orders o
WHERE oi.order_id = o.id
  AND o.status = 'cancelled';
```

## Transaction Control

### Transaction Isolation Levels
```sql
-- Explicit transaction with isolation level
BEGIN ISOLATION LEVEL SERIALIZABLE;  -- Default in CockroachDB
-- or: BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- or: START TRANSACTION;
  INSERT INTO accounts (id, balance) VALUES (1, 1000);
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Set transaction priority
BEGIN PRIORITY HIGH;
  -- Critical operations
COMMIT;

BEGIN PRIORITY LOW;
  -- Background operations
COMMIT;
```

### Savepoints
```sql
-- Savepoints for partial rollback
BEGIN;
  INSERT INTO orders VALUES (...);
  SAVEPOINT before_items;
  INSERT INTO order_items VALUES (...);
  -- If error:
  ROLLBACK TO SAVEPOINT before_items;
  -- Try alternative:
  INSERT INTO order_items VALUES (...);
COMMIT;
```

### Transaction Characteristics
```sql
-- Read-only transactions
BEGIN READ ONLY;
  SELECT * FROM large_table;
COMMIT;

-- Deferrable transactions (for consistency)
BEGIN DEFERRABLE;
  -- Operations that can wait for consistency
COMMIT;

-- Set transaction characteristics
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Prepared Statements

### Basic Prepared Statements
```sql
-- Prepare statement
PREPARE get_user AS
  SELECT * FROM users WHERE id = $1;

-- Execute with parameters
EXECUTE get_user(123);
EXECUTE get_user('550e8400-e29b-41d4-a716-446655440000'::UUID);

-- Deallocate when done
DEALLOCATE get_user;
DEALLOCATE ALL;  -- Remove all prepared statements
```

### Complex Prepared Statements
```sql
-- Prepared statement with multiple parameters
PREPARE insert_user AS
  INSERT INTO users (email, name, role)
  VALUES ($1, $2, $3)
  RETURNING id;

EXECUTE insert_user('user@example.com', 'John Doe', 'admin');

-- Prepared statement for batch operations
PREPARE batch_update AS
  UPDATE products
  SET price = price * $1
  WHERE category = $2;

EXECUTE batch_update(1.1, 'electronics');  -- 10% increase
```

## Bulk Operations

### Efficient Bulk Inserts
```sql
-- Copy from CSV (fastest for large data)
COPY users (id, email, name)
FROM '/path/to/users.csv'
WITH CSV HEADER;

-- Copy to CSV
COPY (SELECT * FROM users WHERE active = true)
TO '/path/to/active_users.csv'
WITH CSV HEADER;

-- Multi-row VALUES for moderate batches
INSERT INTO events (type, data) VALUES
  ('click', '{"page": "home"}'),
  ('view', '{"page": "product"}'),
  -- ... up to 1000 rows
  ('purchase', '{"amount": 99.99}');
```

### Batch Processing Patterns
```sql
-- Process in chunks with LIMIT
WITH batch AS (
  SELECT id FROM large_table
  WHERE processed = false
  LIMIT 1000
  FOR UPDATE
)
UPDATE large_table
SET processed = true
WHERE id IN (SELECT id FROM batch);

-- Incremental processing with cursor
DECLARE process_cursor CURSOR FOR
  SELECT id, data FROM events
  WHERE processed = false
  ORDER BY created_at;

FETCH 100 FROM process_cursor;
-- Process fetched rows
```

## Performance Tips

1. **Add LIMIT** to UPDATE/DELETE for large tables
2. **Use transactions** for related operations
3. **Consider COPY** for bulk imports/exports
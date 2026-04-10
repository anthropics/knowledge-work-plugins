# CockroachDB SQL Examples

## Table Creation Examples

### Example 1: Simple Table Creation (Generation Only)
**Input**: "Create a users table with email and password"

**Output**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email STRING NOT NULL UNIQUE,
  password_hash STRING NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),

  -- Index for login queries
  INDEX idx_email (email)
);
```

### Example 2: Table Creation with Execution
**Input**: "Connect to postgresql://root@localhost:26257/mydb and create a users table with email and password"

**Process**:
1. Extract connection URL from prompt
2. Connect to database
3. Execute CREATE TABLE statement
4. Show confirmation

**Output**:
```
## Connection Method
Using: User-provided URL (postgresql://root@localhost:26257/mydb)

## Executed SQL

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email STRING NOT NULL UNIQUE,
  password_hash STRING NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  INDEX idx_email (email)
);

## Execution Results
✅ Table 'users' created successfully

## Next Steps
- Insert sample data: INSERT INTO users (email, password_hash) VALUES (...)
- Query the table: SELECT * FROM users;
- Add additional indexes if needed
```

## Query Examples

### Example 3: Query Execution via MCP Server
**Input**: "Execute: Show me all users created in the last week"

**Process**:
1. Detect "execute" keyword
2. Check for cockroach-cloud MCP availability
3. Generate and execute query via MCP

**Output**:
```
## Connection Method
Using: cockroach-cloud MCP server

## Executed SQL

SELECT
  id,
  email,
  created_at
FROM users
WHERE created_at > now() - INTERVAL '7 days'
ORDER BY created_at DESC;

## Execution Results
✅ Query executed successfully
Rows returned: 3

| id | email | created_at |
|----|-------|------------|
| a3f...2d1 | user1@example.com | 2024-02-20 10:30:00+00 |
| b7c...4e2 | user2@example.com | 2024-02-19 15:45:00+00 |
| c9a...6f3 | user3@example.com | 2024-02-18 09:15:00+00 |
```

### Example 4: Complex Query with JOINs
**Input**: "Find all orders from the last week with customer details"

**Output**:
```sql
-- Using AS OF SYSTEM TIME for consistent reads
SELECT
  o.id,
  o.total,
  o.created_at,
  c.name,
  c.email
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at > now() - INTERVAL '7 days'
ORDER BY o.created_at DESC;

-- Alternative with follower reads for better performance
SELECT
  o.id,
  o.total,
  o.created_at,
  c.name,
  c.email
FROM orders AS OF SYSTEM TIME follower_read_timestamp() o
JOIN customers AS OF SYSTEM TIME follower_read_timestamp() c
  ON o.customer_id = c.id
WHERE o.created_at > now() - INTERVAL '7 days'
ORDER BY o.created_at DESC;
```

## Multi-Region Examples

### Example 5: Global Configuration Table
**Input**: "Create a configuration table that's replicated everywhere"

**Output**:
```sql
CREATE TABLE config (
  key STRING PRIMARY KEY,
  value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
) LOCALITY GLOBAL;
```

### Example 6: Regional User Table
**Input**: "Create a users table where data stays in user's region"

**Output**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email STRING NOT NULL UNIQUE,
  region STRING NOT NULL,
  profile JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  CONSTRAINT region_check CHECK (region IN ('us-east', 'us-west', 'eu-west'))
) LOCALITY REGIONAL BY ROW AS region;
```

## Performance Optimization Examples

### Example 7: Bulk Insert
**Input**: "Insert 1000 user records efficiently"

**Output**:
```sql
-- Use multi-row INSERT with RETURNING NOTHING for best performance
INSERT INTO users (email, name, created_at) VALUES
  ('user1@example.com', 'User 1', now()),
  ('user2@example.com', 'User 2', now()),
  ('user3@example.com', 'User 3', now()),
  -- ... up to 1000 rows
  ('user1000@example.com', 'User 1000', now())
RETURNING NOTHING;
```

### Example 8: UPSERT Pattern
**Input**: "Update inventory count or insert if doesn't exist"

**Output**:
```sql
-- Native UPSERT (most efficient for blind writes)
UPSERT INTO inventory (product_id, quantity, last_updated)
VALUES (
  '550e8400-e29b-41d4-a716-446655440000',
  100,
  now()
);

-- Alternative with ON CONFLICT for conditional logic
INSERT INTO inventory (product_id, quantity, last_updated)
VALUES ('550e8400-e29b-41d4-a716-446655440000', 100, now())
ON CONFLICT (product_id)
DO UPDATE SET
  quantity = inventory.quantity + EXCLUDED.quantity,
  last_updated = now()
WHERE inventory.last_updated < EXCLUDED.last_updated;
```

## JSON Operations Examples

### Example 9: JSON Column Operations
**Input**: "Query users where metadata contains active status"

**Output**:
```sql
-- Check if JSON contains specific key-value
SELECT * FROM users
WHERE metadata @> '{"status": "active"}';

-- Extract nested JSON field
SELECT
  id,
  email,
  metadata->>'status' as status,
  metadata#>>'{address,city}' as city
FROM users
WHERE metadata ? 'address';

-- Update JSON field
UPDATE users
SET metadata = jsonb_set(
  metadata,
  '{preferences,theme}',
  '"dark"'
)
WHERE id = '550e8400-e29b-41d4-a716-446655440000';
```

## Window Function Examples

### Example 10: Ranking and Analytics
**Input**: "Rank salespeople by quarterly sales"

**Output**:
```sql
SELECT
  salesperson_id,
  quarter,
  total_sales,
  RANK() OVER (PARTITION BY quarter ORDER BY total_sales DESC) as quarter_rank,
  SUM(total_sales) OVER (
    PARTITION BY salesperson_id
    ORDER BY quarter
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) as cumulative_sales
FROM quarterly_sales
ORDER BY quarter, quarter_rank;
```

## Common Issues to Check

1. **Missing PRIMARY KEY**: Always add one, prefer UUID
2. **Wrong timestamp type**: Convert to TIMESTAMPTZ
3. **Using AUTO_INCREMENT**: Replace with UUID or SERIAL
4. **TEXT type usage**: Convert to STRING
5. **JSON type usage**: Convert to JSONB
6. **Missing indexes**: Suggest appropriate indexes
7. **Not using RETURNING NOTHING**: Add for write-only operations
8. **Sequential IDs**: Replace with UUID for better distribution

## Testing Commands

### Quick Schema Verification
```bash
# Show all tables
cockroach sql --execute="SHOW TABLES;"

# Show table structure
cockroach sql --execute="SHOW CREATE TABLE users;"

# Show indexes
cockroach sql --execute="SHOW INDEXES FROM users;"
```

### Performance Testing
```sql
-- Explain query plan
EXPLAIN (VERBOSE) SELECT * FROM users WHERE email = 'test@example.com';

-- Analyze actual execution
EXPLAIN ANALYZE SELECT * FROM large_table WHERE condition;

-- Check for full table scans
SHOW FULL TABLE SCANS;
```
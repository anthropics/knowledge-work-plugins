---
name: designing-application-transactions
description: Guides application developers in designing correct and performant transaction patterns for CockroachDB, covering transaction lifetime, implicit vs explicit transactions, retry handling with exponential backoff, pushing invariants into SQL, selective pessimistic locking, set-based operations, connection pooling, prepared statements, keyset pagination, follower reads, and separating business logic from database logic. Use when building applications on CockroachDB, designing transaction workflows, handling retries, optimizing application-layer database interactions, or configuring connection pools.
compatibility: "CockroachDB >= 22.1. Works with or without a live database connection. With connection, requires appropriate privileges on target tables."
metadata:
  author: cockroachdb
  version: "1.0"
---

# Designing Application Transactions

Guides application developers through the design principles and implementation patterns needed to build correct, performant, and resilient applications on CockroachDB. Covers the full spectrum from transaction scoping and retry logic to connection pooling and observability.

**Complement to SQL skills:** For SQL syntax, schema design, and query optimization, see [cockroachdb-sql](../../query-and-schema-design/cockroachdb-sql/SKILL.md). For benchmarking transaction formulations under contention, see [benchmarking-transaction-patterns](../benchmarking-transaction-patterns/SKILL.md).

## When to Use This Skill

- Designing transaction boundaries for a CockroachDB application
- Implementing client-side retry logic with exponential backoff
- Deciding between implicit and explicit transactions
- Choosing between optimistic and pessimistic concurrency control
- Replacing read-modify-write loops with atomic SQL
- Configuring connection pools (HikariCP, pgbouncer, etc.)
- Implementing keyset pagination instead of OFFSET/LIMIT
- Using follower reads for reporting and analytics queries
- Separating business orchestration from database transactions
- Using prepared statements for performance and security
- Selecting explicit column projections instead of SELECT *
- Testing application behavior under concurrency
- Monitoring application-level database performance

## Prerequisites

- Familiarity with CockroachDB's SERIALIZABLE isolation level
- Understanding of ACID transaction semantics
- Access to application source code for transaction design changes
- SQL connection to a CockroachDB cluster (for testing and validation)

## Steps

### 1. Keep Transactions Short-Lived

Transactions must include only the minimal set of SQL operations needed for one atomic state change. Do not place remote API calls, service-to-service requests, loops, expensive computation, or artificial waits inside a CockroachDB transaction.

Long-lived transactions increase intent lifetime, contention, and retry probability in CockroachDB's distributed, optimistic-concurrency architecture.

**Anti-pattern:**

```java
@Transactional
public void createOrder(Order order) {
    orderRepository.save(order);
    paymentGateway.charge(order); // external call inside TX
}
```

**Correct approach — split the logic:**

```java
@Transactional
public void createOrderRecord(Order order) {
    orderRepository.save(order);
}

// Outside the transaction
paymentGateway.charge(order);
```

**Why it matters:**
- Active intents block concurrent writers, reducing cluster throughput
- Competing transactions are more likely to encounter `40001` retry errors
- External work inside a retried transaction may run twice, causing duplicate side effects
- Long transactions tie up connections and memory, reducing concurrency

### 2. Use Implicit Transactions for Single Statements

CockroachDB automatically wraps each individual SQL statement as a transaction in autocommit mode. For single `INSERT`, `UPDATE`, `DELETE`, or `SELECT` statements, do not wrap in explicit `BEGIN`/`COMMIT`.

**Preferred:**

```sql
INSERT INTO orders (id, status)
VALUES (gen_random_uuid(), 'open');
```

**Avoid:**

```sql
BEGIN;
INSERT INTO orders (id, status)
VALUES (gen_random_uuid(), 'open');
COMMIT;
```

**Benefits:** Simpler code paths, lower latency (fewer round trips), less resource usage, and fewer retry concerns since single-statement transactions are easier for CockroachDB to retry automatically.

### 3. Use Explicit Transactions for Grouped Statements and Handle Retries

When multiple SQL operations must succeed or fail together, use explicit transactions with `BEGIN`/`COMMIT`. Because CockroachDB defaults to SERIALIZABLE isolation, transaction retries are a normal part of correct execution under contention.

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

**Client-side retry loop with exponential backoff:**

```python
import random
import time

def execute_with_retry(conn, txn_logic):
    backoff = 0.1
    while True:
        try:
            with conn.transaction() as txn:
                txn_logic(txn)
            return
        except SerializationFailure:
            time.sleep(backoff + random.uniform(0, 0.1))
            backoff = min(backoff * 2, 2.0)
```

**Advanced retry with the cockroach_restart savepoint protocol:**

```sql
BEGIN;
SAVEPOINT cockroach_restart;
-- transactional work
RELEASE SAVEPOINT cockroach_restart;
COMMIT;
```

**WARNING: Generic savepoints do NOT work as retry mechanisms.** CockroachDB aborts the entire transaction on a `40001` serialization failure. Using `ROLLBACK TO SAVEPOINT` on a regular savepoint cannot recover -- the transaction remains in an aborted state. Only the special `SAVEPOINT cockroach_restart` protocol (where the client catches the error, rolls back to the savepoint, and re-executes the work) is supported. For most applications, a full-transaction retry loop is simpler and recommended.

**SQLSTATE guidance:**

| Code            | Meaning                                 | Action                                                |
|-----------------|-----------------------------------------|-------------------------------------------------------|
| `40001`         | Serialization / retryable               | Retry the entire unit of work with backoff and jitter |
| `40003`         | Ambiguous result / indeterminate commit | Do not blindly replay non-idempotent work             |
| `08xx` / `57xx` | Network or server transient issues      | Retry carefully, account for ambiguous commits        |
| `23xxx`         | Constraint and application errors       | Usually should not be retried                         |

### 4. Mark Read-Only Transactions Where Applicable

Read-only transactions perform retrieval only and make no writes. Marking them as read-only allows CockroachDB to avoid unnecessary write intents, reduce contention with writers, and enable follower or bounded-staleness reads.

```sql
BEGIN;
SET TRANSACTION READ ONLY;
SELECT * FROM customers WHERE region = 'US-East';
COMMIT;
```

### 5. Push Invariants into SQL — Avoid Read-Modify-Write Loops

Do not fetch state into application code, modify it in memory, and write it back. Prefer atomic SQL, constraints, guarded UPDATEs, UPSERT, INSERT ... ON CONFLICT, and CTE-based mutations.

**Anti-pattern:**

```python
balance = db.fetch("SELECT balance FROM accounts WHERE id = 123")
balance += 100
db.execute("UPDATE accounts SET balance = %s WHERE id = 123", (balance,))
```

**Preferred atomic SQL:**

```sql
UPDATE accounts
SET balance = balance + 100
WHERE id = 123;
```

**Guarded write with invariant enforcement:**

```sql
UPDATE customer_daily_limits
SET used_total = used_total + $2
WHERE customer_id = $1
  AND day = current_date
  AND used_total + $2 <= daily_limit;
```

**Atomic CTE pattern:**

```sql
WITH limit_row AS (
  SELECT customer_id, day
  FROM customer_daily_limits
  WHERE customer_id = $1 AND day = current_date
  FOR UPDATE
), spend AS (
  UPDATE customer_daily_limits AS l
  SET remaining_limit = l.remaining_limit - $2,
      used_total = l.used_total + $2
  FROM limit_row
  WHERE l.customer_id = limit_row.customer_id
    AND l.day = limit_row.day
    AND l.remaining_limit >= $2
  RETURNING l.customer_id, l.day
), ins AS (
  INSERT INTO transfers (customer_id, amount, direction, created_at)
  SELECT $1, $2, 'debit', now()
  FROM spend
  RETURNING id AS transfer_id
)
SELECT transfer_id FROM ins;
```

**Key approaches:**
- Use atomic updates: `UPDATE ... SET col = col + 1`
- Use version or timestamp checks in WHERE clauses for optimistic concurrency
- Enforce business rules with `UNIQUE`, `CHECK`, `NOT NULL`, and `FOREIGN KEY` constraints
- Use `UPSERT` or `INSERT ... ON CONFLICT` instead of read-before-write existence checks
- Use CTEs to keep multi-step logic atomic

### 6. Use SELECT ... FOR UPDATE Selectively

CockroachDB defaults to optimistic concurrency, which works well for most workloads. For hot rows or contention-heavy read-before-write paths, `SELECT ... FOR UPDATE` reduces retry churn by making contenders wait instead of race.

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

**Use when:**
- The same rows are updated frequently by many concurrent transactions
- Optimistic retries are causing thrashing
- Consistency before write is required (inventory, financial transfers)

**Counterintuitive contention insight:** Adding more application pods or threads targeting the same hot rows does NOT increase throughput -- it decreases it. With N concurrent writers on the same row, only 1 can commit per round; the other N-1 are aborted with `40001` and must retry. More concurrency on hot data means more wasted work and lower TPS. Solutions: use `SELECT ... FOR UPDATE` to serialize access, use atomic `UPDATE SET balance = balance + amount` to eliminate the read-modify-write cycle, or distribute writes across multiple rows.

**Trade-off:** Overusing pessimistic locks can introduce waiting chains or deadlocks. Reserve for hot paths and contention-heavy workloads.

### 7. Use Set-Based Operations Over Row-by-Row Loops

CockroachDB performs best with set-oriented SQL rather than many small client-driven statements. This reduces round trips, shortens contention windows, and improves throughput.

**Row-by-row anti-pattern:**

```python
for row in rows:
    db.execute(
        "UPDATE accounts SET balance = balance + 10 WHERE id = %s",
        (row.id,)
    )
```

**Set-based preferred:**

```sql
UPDATE accounts
SET balance = balance + 10
WHERE region = 'US-East';
```

**Batch INSERT:**

```sql
INSERT INTO trades (id, symbol, price)
VALUES
  (1, 'AAPL', 180),
  (2, 'GOOG', 125),
  (3, 'AMZN', 140);
```

**Batch UPDATE with UNNEST:**

```sql
WITH incoming AS (
  SELECT *
  FROM UNNEST(
    ARRAY['u1', 'u2', 'u3']::STRING[],
    ARRAY['active', 'inactive', 'active']::STRING[]
  ) AS t(id, new_status)
)
UPDATE users AS u
SET status = incoming.new_status,
    updated_at = now()
FROM incoming
WHERE u.id = incoming.id;
```

**Maintenance batching with LIMIT:**

```sql
DELETE FROM sessions
WHERE expires_at < now()
LIMIT 10000;
```

**JDBC batching (Java):** Use `addBatch`/`executeBatch` instead of per-row `executeUpdate`. This sends all rows in a single network round trip rather than N individual round trips, eliminating idle time that can account for ~50% of transaction latency in chatty workloads.

**Declarative TTL:**

```sql
ALTER TABLE events
SET (ttl_expiration_expression = 'created_at + INTERVAL ''7 DAY''');
```

### 8. Use Follower Reads for Non-Critical Queries

Many analytics, dashboard, and display-oriented queries do not need the absolute latest value. CockroachDB supports follower reads and bounded-staleness reads from follower replicas with lower latency.

**Basic follower read:**

```sql
SELECT * FROM orders
AS OF SYSTEM TIME '-5s';
```

**Bounded staleness:**

```sql
SELECT * FROM inventory
AS OF SYSTEM TIME with_max_staleness(INTERVAL '10s');
```

**Read-write split pattern for heavy reads:** When a workflow reads a large payload (e.g., KYC JSON document) and then updates a status field, split it into three phases: (1) read outside the transaction with `AS OF SYSTEM TIME` for a conflict-free snapshot, (2) process in the application layer, (3) start a short write-only transaction. This avoids holding write intents during the heavy read.

**Use when:** Dashboards, analytics, ETL, display-only reads, or large-payload workflows where the read and write can be separated.

**Avoid when:** The workflow requires the latest transactional state for a subsequent write decision.

### 9. Use Keyset Pagination Instead of OFFSET/LIMIT

As the OFFSET grows, CockroachDB must scan and discard more rows. Keyset pagination uses the last row's ordered key values to jump directly to the next page.

**OFFSET/LIMIT (inefficient at depth):**

```sql
SELECT id, order_date, customer_id
FROM orders
ORDER BY id
LIMIT 100 OFFSET 5000;
```

**Keyset pagination (preferred):**

```sql
SELECT id, order_date, customer_id
FROM orders
WHERE id > 5000
ORDER BY id
LIMIT 100;
```

**Multi-column keyset:**

```sql
SELECT id, created_at, customer_id
FROM orders
WHERE (created_at, id) > ('2025-01-01 00:00:00', 5000)
ORDER BY created_at, id
LIMIT 100;
```

**Trade-off:** Keyset pagination is ideal for next/previous navigation but not for arbitrary "jump to page 73" UX.

### 10. Use Prepared Statements for Performance and Security

Prepared statements reuse query structure and bind new values, improving performance through plan reuse and protecting against SQL injection.

**Unsafe dynamic string concatenation:**

```python
query = f"SELECT * FROM users WHERE username = '{user_input}'"
cursor.execute(query)
```

**Prepared / parameterized execution:**

```python
cursor.execute("SELECT * FROM users WHERE username = %s;", (user_input,))
```

**Plan reuse:**

```sql
PREPARE get_balance AS
SELECT balance FROM accounts WHERE id = $1;

EXECUTE get_balance(1001);
EXECUTE get_balance(2002);
```

### 11. Use Column Projections Instead of SELECT *

Select only the columns you need. `SELECT *` increases network payload, memory usage, CPU cost, and prevents narrower index-only scans.

```sql
-- Avoid
SELECT * FROM users WHERE id = 101;

-- Preferred
SELECT name, email FROM users WHERE id = 101;
```

**Schema evolution impact:** If a later schema change adds `profile_picture BYTEA`, queries using `SELECT *` automatically pull that extra data. Explicit projections avoid this hidden performance regression.

### 12. Design Keys and Indexes to Distribute Load

Sequential or monotonically increasing primary keys create write hotspots. Keys and indexes should distribute reads and writes across ranges evenly.

**Hotspot anti-pattern:**

```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id UUID,
  region STRING
);
```

**Randomized key:**

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID,
  region STRING
);
```

**Hash-sharded index:**

```sql
CREATE INDEX orders_by_id_hash
ON orders (id)
USING HASH SHARDED WITH BUCKET_COUNT = 16;
```

**Composite key for natural distribution:**

```sql
CREATE TABLE sales (
  region_id STRING,
  order_id UUID DEFAULT gen_random_uuid(),
  PRIMARY KEY (region_id, order_id)
);
```

**Enforce explicit PKs cluster-wide:**

```sql
SET CLUSTER SETTING sql.defaults.require_explicit_primary_keys.enabled = true;
```

### 13. Configure Connection Pooling

Opening new database connections is expensive. Pooling reuses live connections to improve performance and prevent overload.

**HikariCP guidance:**

```yaml
maximumPoolSize: (vCPUs * 4) / number_of_pool_instances
minimumIdle: equal to maximumPoolSize
maxLifetime: 30 min (add jitter +/- 5 min)
idleTimeout: 5-10 min typical
keepaliveTime: slightly shorter than infrastructure timeout (~5 min)
connectionTimeout: 10-30 s typical
autoCommit: true unless using explicit transactions only
```

**Example stable configuration:**

```yaml
maximum-pool-size: 12
minimum-idle: 12
max-lifetime: 1800000
idle-timeout: 600000
keepalive-time: 300000
connection-timeout: 10000
auto-commit: true
pool-name: ingestionPool
```

### 14. Separate Business Logic from Database Logic

CockroachDB should manage ACID reads, writes, and schema-level integrity. The application layer should orchestrate workflows, external services, queues, and long-running work.

**Inside the transaction:**
- Reads, writes, constraints, short guarded state transitions

**Outside the transaction:**
- HTTP calls, RPC/service calls, email, payment providers, queue publishing

**Asynchronous workflow pattern:**

```python
def handle_order(order):
    db.execute("INSERT INTO orders (id, status) VALUES (%s, %s)", (order.id, 'PENDING'))
    publish_event('process_order', {'order_id': order.id})
```

### 15. Respect the 16MB Transaction Payload Limit

CockroachDB has a practical limit of ~16MB per transaction payload. This limit applies to the TOTAL data written in a single transaction, not just individual rows.

**Two ways to hit the limit:**
- One large row (e.g., a 15MB JSON document)
- Many moderate rows in one transaction (e.g., 25 INSERTs of 500KB each = 12.5MB)

**Guidelines:**
- Keep individual rows under 1MB
- Keep total transaction payload under 4MB
- Limit transactions to <10 statements
- Chunk large documents into 64-256KB pieces
- Store blobs >1MB in object storage (S3/GCS) with a database reference
- Break multi-statement transactions into smaller batches (commit every 5-10 statements)

**Exceeding the limit causes `split failed while applying backpressure to Put` errors:** large Raft proposals block consensus, range splits stall, and the system applies backpressure.

### 16. Use Session Guardrails

Set session-level guardrails to catch runaway queries and missing WHERE clauses during development and testing:

```sql
SET transaction_rows_read_err = 10000;
SET transaction_rows_written_err = 1000;
```

These cause transactions that exceed the thresholds to fail with an explicit error rather than silently consuming cluster resources.

### 17. Test and Optimize Under Concurrency

Single-user correctness is not sufficient. Test with realistic concurrency to surface retries, hotspots, contention, and workload-specific bottlenecks.

**Quick start:**

```bash
cockroach workload init bank 'postgresql://root@localhost:26257?sslmode=disable'
cockroach workload run bank --concurrency=64 --duration=10m
```

See [monitoring-and-concurrency-testing](references/monitoring-and-concurrency-testing.md) for detailed contention queries, validation checklists, and Prometheus metrics.

### 18. Monitor for Performance and Contention

Actively monitor query latency, contention, retries, and data distribution using `EXPLAIN ANALYZE`, `crdb_internal.transaction_contention_events`, DB Console SQL Activity, and Key Visualizer.

See [monitoring-and-concurrency-testing](references/monitoring-and-concurrency-testing.md) for live contention queries, Prometheus metrics, and external monitoring integration.

## Decision Guide

| Scenario                                    | Recommended Pattern                  |
|---------------------------------------------|--------------------------------------|
| Single SQL statement                        | Implicit transaction (autocommit)    |
| Multiple statements, all-or-nothing         | Explicit transaction with retry loop |
| Read current state before write on hot rows | `SELECT ... FOR UPDATE`              |
| Historical, display, or reporting read      | `AS OF SYSTEM TIME` / follower reads |
| Batch of records in memory                  | `UNNEST` / `VALUES` / batch SQL      |
| Multi-step business rule in one operation   | Single-statement CTE                 |

## Safety Considerations

- Always implement retry logic for `40001` serialization errors
- Make operations idempotent so retries do not cause duplicate side effects (use `INSERT ... ON CONFLICT DO NOTHING`)
- Do not use stale snapshot reads as authoritative preconditions for writes
- Do not run `EXPLAIN ANALYZE` on production queries that modify data
- Be cautious adding indexes to high-traffic tables during peak hours

## References

- [CockroachDB Transactions Documentation](https://www.cockroachlabs.com/docs/stable/transactions)
- [Advanced Client-Side Transaction Retries](https://www.cockroachlabs.com/docs/stable/advanced-client-side-transaction-retries)
- [SQL Performance Best Practices](https://www.cockroachlabs.com/docs/stable/performance-best-practices-overview)
- [Follower Reads and Bounded Staleness](https://www.cockroachlabs.com/docs/stable/follower-reads)
- [Optimize Statement Performance](https://www.cockroachlabs.com/docs/stable/make-queries-fast)
- [Row-Level TTL](https://www.cockroachlabs.com/docs/stable/row-level-ttl)
- [Schema Design and Indexes](https://www.cockroachlabs.com/docs/stable/schema-design-indexes)
- [SQL Injection Prevention](https://www.cockroachlabs.com/docs/stable/sql-injection-prevention)
- [Architecture: Transaction Layer](https://www.cockroachlabs.com/docs/stable/architecture/transaction-layer)
- [JPA Best Practices: Explicit and Implicit Transactions](https://blog.cloudneutral.se/jpa-best-practices-explicit-and-implicit-transactions)
- [Deep Dive into Transaction Retry Failures](https://www.mindfulchase.com/explore/troubleshooting-tips/databases/deep-dive-into-transaction-retry-failures-in-cockroachdb-root-causes-and-fixes.html)
- [Comparing Multi-Statement vs Single-Statement Transactions](https://andrewdeally.medium.com/comparing-multi-statement-vs-single-statement-transactions-for-account-transfers-in-sql-09190b116e64)
- [Set-Based Operations with CockroachDB](https://andrewdeally.medium.com/set-based-operations-with-cockroachdb-c9f371992dc7)
- [Bulk Rewrites with the CockroachDB JDBC Driver](https://blog.cloudneutral.se/cockroachdb-jdbc-driver-part-iii-bulk-rewrites)
- [What is a Database Hotspot?](https://www.cockroachlabs.com/blog/the-hot-content-problem-metadata-storage-for-media-streaming/)
- [CockroachDB Transaction Demo](https://github.com/cockroachdb/cockroach-transaction-demo)
- [CockroachDB Best Practices & Anti-Patterns Demo](https://github.com/viragtripathi/cockroachdb-best-practices-demo) -- 10 runnable Java demos covering retries, batching, PK hotspots, guardrails, chunking, and multi-region
- [CockroachDB JDBC Wrapper](https://github.com/viragtripathi/cockroachdb-jdbc-wrapper) -- automatic retry library for Java/JDBC applications

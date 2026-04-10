# JSON Field Reference

Complete schema documentation for JSONB fields in `crdb_internal.transaction_statistics`. This reference covers the `metadata` and `statistics` columns, which store transaction attributes and performance metrics.

## Overview

`crdb_internal.transaction_statistics` uses JSONB columns for flexible schema evolution. Extract fields using:
- `->` operator: Returns JSON type (for nested access)
- `->>` operator: Returns text type (for values)
- `::TYPE` casting: Convert text to specific types (INT, FLOAT8, BOOL)
- `encode(fingerprint_id, 'hex')`: Convert binary fingerprint to hex string for readability

**Example row structure:**
```sql
SELECT fingerprint_id, metadata, statistics, aggregated_ts
FROM crdb_internal.transaction_statistics
LIMIT 1;
```

## Fingerprint ID Encoding

**fingerprint_id column:** Binary format (bytea) by default; convert to hex for human-readable IDs.

**Hex encoding pattern:**
```sql
encode(fingerprint_id, 'hex') AS txn_fingerprint_id
```

**Decoding for joins:**
```sql
decode('hex_string_value', 'hex')  -- Convert hex back to binary for joins
```

## metadata Column

Transaction attributes and query characteristics (not performance metrics).

| Field Path | Type | Description | Example Extraction |
|------------|------|-------------|-------------------|
| `db` | TEXT | Database name | `metadata->>'db'` |
| `app` | TEXT | Application name from connection string | `metadata->>'app'` |
| `failed` | BOOLEAN | True if this row aggregates failed executions only | `(metadata->>'failed')::BOOL` |
| `implicitTxn` | BOOLEAN | True if transaction is implicit (single statement) | `(metadata->>'implicitTxn')::BOOL` |
| `stmtFingerprintIDs` | JSONB ARRAY | Array of statement fingerprint IDs (hex strings) composing this transaction | `metadata->'stmtFingerprintIDs'` |

### stmtFingerprintIDs Structure

**Purpose:** Maps transaction to constituent statement fingerprints for drill-down analysis.

**Data type:** JSONB array of hex-encoded fingerprint ID strings

**Example value:**
```json
[
  "a1b2c3d4e5f6g7h8",
  "i9j0k1l2m3n4o5p6",
  "q7r8s9t0u1v2w3x4"
]
```

**Extraction patterns:**

**Count statements in transaction:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  jsonb_array_length(metadata->'stmtFingerprintIDs') AS num_statements
FROM crdb_internal.transaction_statistics
WHERE metadata->'stmtFingerprintIDs' IS NOT NULL;
```

**Expand array to rows:**
```sql
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  stmt_fp_id AS stmt_fingerprint_id
FROM crdb_internal.transaction_statistics t
CROSS JOIN LATERAL jsonb_array_elements_text(t.metadata->'stmtFingerprintIDs') AS stmt_fp_id
WHERE t.metadata->'stmtFingerprintIDs' IS NOT NULL;
```

**Join with statement_statistics:**
```sql
-- Cross-reference transaction to statements
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  stmt_fp_id,
  s.metadata->>'query' AS statement_query,
  (s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS stmt_mean_lat
FROM crdb_internal.transaction_statistics t
CROSS JOIN LATERAL jsonb_array_elements_text(t.metadata->'stmtFingerprintIDs') AS stmt_fp_id
LEFT JOIN crdb_internal.statement_statistics s
  ON s.fingerprint_id = decode(stmt_fp_id, 'hex')
  AND s.aggregated_ts = t.aggregated_ts
WHERE t.aggregated_ts > now() - INTERVAL '24 hours'
  AND t.metadata->'stmtFingerprintIDs' IS NOT NULL;
```

**Key notes:**
- Single-statement transactions may have empty or single-element arrays
- Hex encoding matches between transaction_statistics.stmtFingerprintIDs and statement_statistics.fingerprint_id
- Always match on same `aggregated_ts` bucket when joining

### Implicit vs Explicit Transactions

**implicitTxn field:** Distinguishes auto-wrapped single statements from multi-statement transactions.

```sql
-- Analyze implicit vs explicit transaction patterns
SELECT
  (metadata->>'implicitTxn')::BOOL AS is_implicit,
  COUNT(*) AS fingerprint_count,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  AVG((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8) AS avg_commit_lat
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
GROUP BY is_implicit;
```

**Interpretation:**
- `implicitTxn = true`: Single statement auto-wrapped (e.g., standalone `SELECT`)
- `implicitTxn = false`: Multi-statement transaction (e.g., `BEGIN; ... COMMIT;`)

## statistics Column

Nested JSONB object containing two subsections: `statistics` (aggregated) and `execution_statistics` (sampled).

### statistics.statistics (Aggregated Metrics)

**Collected for all executions.** No sampling; represents complete dataset for the time bucket.

| Field Path | Type | Unit | Description | Example Extraction |
|------------|------|------|-------------|-------------------|
| `cnt` | INT | count | Total number of transaction executions | `(statistics->'statistics'->>'cnt')::INT` |
| `maxRetries` | INT | count | Maximum retry count across all executions | `(statistics->'statistics'->>'maxRetries')::INT` |
| `numRows` | OBJECT | count | Rows affected statistics | See subsection below |
| `retryLat` | OBJECT | seconds | Retry latency statistics | See subsection below |
| `commitLat` | OBJECT | seconds | Commit latency statistics (2PC overhead) | See subsection below |
| `svcLat` | OBJECT | seconds | Total service latency | See subsection below |

#### Latency Object Structure

Each latency field (`retryLat`, `commitLat`, `svcLat`) contains:

| Subfield | Type | Description | Example Extraction |
|----------|------|-------------|-------------------|
| `mean` | FLOAT8 | Mean latency in seconds | `(statistics->'statistics'->'commitLat'->>'mean')::FLOAT8` |
| `sqDiff` | FLOAT8 | Sum of squared differences (for variance calculation) | `(statistics->'statistics'->'commitLat'->>'sqDiff')::FLOAT8` |

**Transaction-specific latency fields:**

**retryLat (Retry Latency):**
```sql
(statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_seconds
```
- **Definition:** Time spent retrying due to transaction conflicts/aborts
- **Unit:** Seconds
- **Interpretation:** High retry latency indicates contention; often correlates with high `maxRetries`

**commitLat (Commit Latency):**
```sql
(statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_seconds
```
- **Definition:** Time spent in 2-phase commit protocol (transaction boundary overhead)
- **Unit:** Seconds
- **Interpretation:** High commit latency suggests distributed transaction overhead, cross-region writes, or replication delays

**svcLat (Service Latency):**
```sql
(statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_seconds
```
- **Definition:** Total end-to-end transaction latency (execution + retries + commit)
- **Unit:** Seconds
- **Formula:** Approximately `svcLat ≈ execution_time + retryLat + commitLat`

**Calculate standard deviation:**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat,
  sqrt(
    (statistics->'statistics'->'commitLat'->>'sqDiff')::FLOAT8 /
    NULLIF((statistics->'statistics'->>'cnt')::INT, 0)
  ) AS stddev_commit_lat
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours';
```

#### Rows Object Structure

**numRows field:** Statistics about rows affected by transaction.

| Subfield | Type | Description | Example Extraction |
|----------|------|-------------|-------------------|
| `mean` | FLOAT8 | Mean row count | `(statistics->'statistics'->'numRows'->>'mean')::FLOAT8` |
| `sqDiff` | FLOAT8 | Sum of squared differences | `(statistics->'statistics'->'numRows'->>'sqDiff')::FLOAT8` |

**Example: Average rows affected per transaction**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'numRows'->>'mean')::FLOAT8 AS avg_rows_affected
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
ORDER BY avg_rows_affected DESC
LIMIT 20;
```

### statistics.execution_statistics (Sampled Metrics)

**Collected for ~10% of executions.** Always check `cnt` field to verify sample presence.

| Field Path | Type | Unit | Description | Example Extraction |
|------------|------|------|-------------|-------------------|
| `cnt` | INT | count | Number of sampled executions (always check IS NOT NULL) | `(statistics->'execution_statistics'->>'cnt')::INT` |
| `networkBytes` | OBJECT | bytes | Network bytes sent statistics (distributed SQL overhead) | `(statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8` |
| `maxMemUsage` | OBJECT | bytes | Maximum memory usage statistics | `(statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8` |
| `maxDiskUsage` | OBJECT | bytes | Maximum disk usage (spill) statistics | `(statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8` |
| `contentionTime` | OBJECT | nanoseconds | Lock contention time statistics | `(statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9` |

**Defensive filtering pattern:**
```sql
WHERE (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 > 0
```

#### Sampled Object Structure

Same as aggregated metrics: each field contains `mean` and `sqDiff` subfields.

**Example: Contention analysis**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'execution_statistics'->>'cnt')::INT AS sample_size,
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  ROUND(
    (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9,
    3
  ) AS mean_contention_seconds,
  metadata->>'app' AS application
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 > 0
ORDER BY mean_contention_seconds DESC
LIMIT 20;
```

**Example: Network and memory analysis**
```sql
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 AS mean_network_mb,
  (statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576 AS mean_mem_mb,
  (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1048576 AS mean_disk_mb,
  CASE
    WHEN (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 > 0
    THEN 'SPILLING'
    ELSE 'in-memory'
  END AS memory_status
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
ORDER BY mean_network_mb DESC
LIMIT 20;
```

## Type Casting Patterns

### Safe Casting with NULL Handling

Always use defensive NULL checks and COALESCE for optional fields:

```sql
-- Safe integer extraction
COALESCE((statistics->'statistics'->>'maxRetries')::INT, 0)

-- Safe float extraction with validation
CASE
  WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    AND (statistics->'execution_statistics'->'contentionTime'->>'mean') IS NOT NULL
  THEN (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9
  ELSE NULL
END AS mean_contention_seconds

-- Boolean with default
COALESCE((metadata->>'implicitTxn')::BOOL, false)
```

### Common Type Casting Examples

```sql
-- Text extraction (no casting needed)
metadata->>'db'                                    -- Returns: 'mydb'

-- Hex encoding for fingerprint
encode(fingerprint_id, 'hex')                      -- Returns: 'a1b2c3d4e5f6g7h8'

-- Decode hex for joins
decode('a1b2c3d4e5f6g7h8', 'hex')                  -- Returns: binary bytea

-- Integer extraction
(statistics->'statistics'->>'cnt')::INT            -- Returns: 1000
(statistics->'statistics'->>'maxRetries')::INT     -- Returns: 15

-- Float extraction
(statistics->'statistics'->'commitLat'->>'mean')::FLOAT8  -- Returns: 0.125

-- Boolean extraction
(metadata->>'implicitTxn')::BOOL                   -- Returns: true

-- JSONB array access
metadata->'stmtFingerprintIDs'                     -- Returns: ["abc...", "def..."]
jsonb_array_length(metadata->'stmtFingerprintIDs') -- Returns: 3

-- Nested object extraction (chained ->)
statistics->'statistics'->'retryLat'->>'mean'      -- Extract mean from retryLat object
```

### Unit Conversions

```sql
-- Nanoseconds to seconds (contention)
(statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9

-- Bytes to megabytes
(statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576

-- Bytes to gigabytes
(statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1073741824

-- Latency already in seconds (no conversion)
(statistics->'statistics'->'commitLat'->>'mean')::FLOAT8
```

## Version Compatibility Notes

**Field availability varies by CockroachDB version:**

| Field | Introduced | Notes |
|-------|------------|-------|
| `stmtFingerprintIDs` | v21.2+ | May be NULL or empty for single-statement transactions |
| `retryLat` | v21.1+ | Earlier versions may not track retry latency separately |
| `commitLat` | v21.1+ | Measures 2PC commit overhead |
| `contentionTime` | v20.2+ | Transaction-level contention tracking |

**Compatibility check query:**
```sql
-- Verify field existence before using in production queries
SELECT
  CASE WHEN metadata ? 'stmtFingerprintIDs' THEN 'available' ELSE 'missing' END AS stmt_fp_ids,
  CASE WHEN statistics->'statistics' ? 'retryLat' THEN 'available' ELSE 'missing' END AS retry_lat,
  CASE WHEN statistics->'statistics' ? 'commitLat' THEN 'available' ELSE 'missing' END AS commit_lat
FROM crdb_internal.transaction_statistics
LIMIT 1;
```

## Common Extraction Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid input syntax for type double precision: ""` | Extracting NULL value as FLOAT8 | Add NULL check: `WHERE field IS NOT NULL` |
| `cannot extract element from a scalar` | Using `->` on text field | Use `->>` for final extraction, `->` for nested objects |
| `operator does not exist: text::boolean` | Wrong extraction operator for boolean | Use `->>` then cast: `(metadata->>'implicitTxn')::BOOL` |
| `invalid input syntax for type json` | Malformed JSON or typo in field path | Verify field name spelling; check JSONB structure with `SELECT metadata` |
| Division by zero | NULLIF not used in denominator | Wrap: `NULLIF((statistics->'statistics'->>'cnt')::INT, 0)` |
| `function decode does not exist` | Typo in decode function | Use `decode('hex_string', 'hex')` not `decode()` |

## Complete Example: Multi-Field Extraction

```sql
SELECT
  -- Fingerprint ID
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,

  -- Metadata fields
  metadata->>'db' AS database,
  metadata->>'app' AS application,
  (metadata->>'implicitTxn')::BOOL AS is_implicit,
  jsonb_array_length(metadata->'stmtFingerprintIDs') AS num_statements,

  -- Aggregated statistics
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_sec,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_sec,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_sec,
  (statistics->'statistics'->'numRows'->>'mean')::FLOAT8 AS mean_rows_affected,

  -- Sampled execution statistics (defensive)
  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN (statistics->'execution_statistics'->>'cnt')::INT
    ELSE NULL
  END AS sample_size,

  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN ROUND((statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9, 3)
    ELSE NULL
  END AS mean_contention_sec,

  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN ROUND((statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576, 2)
    ELSE NULL
  END AS mean_network_mb,

  -- Derived metrics
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct_of_service_lat,

  aggregated_ts

FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 5
ORDER BY max_retries DESC
LIMIT 20;
```

## Additional Resources

- **Official schema:** [crdb_internal documentation](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)
- **JSONB operators:** [PostgreSQL JSONB functions](https://www.postgresql.org/docs/current/functions-json.html) (CockroachDB compatible)
- **Metrics interpretation:** See [metrics-and-units.md](metrics-and-units.md)
- **Query examples:** See [sql-query-variations.md](sql-query-variations.md)

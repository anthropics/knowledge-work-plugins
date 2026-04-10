# JSON Field Reference

Complete schema documentation for JSONB fields in `crdb_internal.statement_statistics`. This reference covers the `metadata` and `statistics` columns, which store statement attributes and performance metrics.

## Overview

`crdb_internal.statement_statistics` uses JSONB columns for flexible schema evolution. Extract fields using:
- `->` operator: Returns JSON type (for nested access)
- `->>` operator: Returns text type (for values)
- `::TYPE` casting: Convert text to specific types (INT, FLOAT8, BOOL)

**Example row structure:**
```sql
SELECT fingerprint_id, metadata, statistics, aggregated_ts
FROM crdb_internal.statement_statistics
LIMIT 1;
```

## metadata Column

Statement attributes and query characteristics (not performance metrics).

| Field Path | Type | Description | Example Extraction |
|------------|------|-------------|-------------------|
| `db` | TEXT | Database name | `metadata->>'db'` |
| `query` | TEXT | Full SQL query text (or `<hidden>` with VIEWACTIVITYREDACTED) | `metadata->>'query'` |
| `querySummary` | TEXT | Truncated query preview | `metadata->>'querySummary'` |
| `app` | TEXT | Application name from connection string | `metadata->>'app'` |
| `stmtType` | TEXT | Statement type (e.g., `TypeSelect`, `TypeInsert`, `TypeUpdate`) | `metadata->>'stmtType'` |
| `fullScan` | BOOLEAN | True if query performs full table scan | `(metadata->>'fullScan')::BOOL` |
| `distSQL` | BOOLEAN | True if query uses distributed execution | `(metadata->>'distSQL')::BOOL` |
| `vec` | BOOLEAN | True if query uses vectorized execution engine | `(metadata->>'vec')::BOOL` |
| `implicitTxn` | BOOLEAN | True if query runs in implicit transaction | `(metadata->>'implicitTxn')::BOOL` |
| `failed` | BOOLEAN | True if this row aggregates failed executions only | `(metadata->>'failed')::BOOL` |
| `index_recommendations` | JSONB ARRAY | Array of recommended index creations | `metadata->'index_recommendations'` |

### index_recommendations Structure

JSONB array of index recommendation objects:

```sql
-- Example extraction
SELECT
  fingerprint_id,
  metadata->>'query' AS query,
  jsonb_array_length(metadata->'index_recommendations') AS num_recommendations,
  metadata->'index_recommendations' AS recommendations
FROM crdb_internal.statement_statistics
WHERE metadata->'index_recommendations' IS NOT NULL
  AND jsonb_array_length(metadata->'index_recommendations') > 0;
```

**Recommendation object fields:**
- `type`: Recommendation type (e.g., `index`)
- `SQL`: Suggested `CREATE INDEX` DDL statement

**Example:**
```json
[
  {
    "type": "index",
    "SQL": "CREATE INDEX ON users (email) STORING (name);"
  }
]
```

### Statement Type Values

Common `stmtType` values:

| Value | Description |
|-------|-------------|
| `TypeSelect` | SELECT queries |
| `TypeInsert` | INSERT statements |
| `TypeUpdate` | UPDATE statements |
| `TypeDelete` | DELETE statements |
| `TypeDDL` | Data Definition Language (CREATE, ALTER, DROP) |
| `TypeTCL` | Transaction Control (BEGIN, COMMIT, ROLLBACK) |

## statistics Column

Nested JSONB object containing two subsections: `statistics` (aggregated) and `execution_statistics` (sampled).

### statistics.statistics (Aggregated Metrics)

**Collected for all executions.** No sampling; represents complete dataset for the time bucket.

| Field Path | Type | Unit | Description | Example Extraction |
|------------|------|------|-------------|-------------------|
| `cnt` | INT | count | Total number of executions | `(statistics->'statistics'->>'cnt')::INT` |
| `firstAttemptCnt` | INT | count | First-attempt executions (no retries) | `(statistics->'statistics'->>'firstAttemptCnt')::INT` |
| `maxRetries` | INT | count | Maximum retry count across all executions | `(statistics->'statistics'->>'maxRetries')::INT` |
| `failureCount` | INT | count | Number of failed executions | `(statistics->'statistics'->>'failureCount')::INT` |
| `runLat` | OBJECT | seconds | Runtime latency statistics | See subsection below |
| `parseLat` | OBJECT | seconds | Parse latency statistics | See subsection below |
| `planLat` | OBJECT | seconds | Planning latency statistics | See subsection below |
| `serviceLat` | OBJECT | seconds | Total service latency (parse + plan + run) | See subsection below |
| `rowsRead` | OBJECT | count | Rows read statistics | See subsection below |
| `bytesRead` | OBJECT | bytes | Bytes read statistics | See subsection below |
| `rowsWritten` | OBJECT | count | Rows written statistics (INSERT/UPDATE/DELETE) | See subsection below |

#### Latency Object Structure

Each latency field (`runLat`, `parseLat`, `planLat`, `serviceLat`) contains:

| Subfield | Type | Description | Example Extraction |
|----------|------|-------------|-------------------|
| `mean` | FLOAT8 | Mean latency in seconds | `(statistics->'statistics'->'runLat'->>'mean')::FLOAT8` |
| `sqDiff` | FLOAT8 | Sum of squared differences (for variance calculation) | `(statistics->'statistics'->'runLat'->>'sqDiff')::FLOAT8` |

**Calculate standard deviation:**
```sql
SELECT
  fingerprint_id,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_lat,
  sqrt(
    (statistics->'statistics'->'runLat'->>'sqDiff')::FLOAT8 /
    NULLIF((statistics->'statistics'->>'cnt')::INT, 0)
  ) AS stddev_lat
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours';
```

#### Rows/Bytes Object Structure

Fields like `rowsRead`, `bytesRead`, `rowsWritten` contain:

| Subfield | Type | Description | Example Extraction |
|----------|------|-------------|-------------------|
| `mean` | FLOAT8 | Mean count/size | `(statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8` |
| `sqDiff` | FLOAT8 | Sum of squared differences | `(statistics->'statistics'->'rowsRead'->>'sqDiff')::FLOAT8` |

**Example: Average rows read per execution**
```sql
SELECT
  fingerprint_id,
  (statistics->'statistics'->>'cnt')::INT AS executions,
  (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 AS avg_rows_read
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
ORDER BY avg_rows_read DESC
LIMIT 20;
```

### statistics.execution_statistics (Sampled Metrics)

**Collected for ~10% of executions.** Always check `cnt` field to verify sample presence.

| Field Path | Type | Unit | Description | Example Extraction |
|------------|------|------|-------------|-------------------|
| `cnt` | INT | count | Number of sampled executions (always check IS NOT NULL) | `(statistics->'execution_statistics'->>'cnt')::INT` |
| `networkBytes` | OBJECT | bytes | Network bytes sent statistics | `(statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8` |
| `maxMemUsage` | OBJECT | bytes | Maximum memory usage statistics | `(statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8` |
| `maxDiskUsage` | OBJECT | bytes | Maximum disk usage (spill) statistics | `(statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8` |
| `contentionTime` | OBJECT | nanoseconds | Lock contention time statistics | `(statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9` |
| `cpuSQLNanos` | OBJECT | nanoseconds | CPU time in SQL execution statistics | `(statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9` |
| `admissionWaitTime` | OBJECT | nanoseconds | Admission control queueing time | `(statistics->'execution_statistics'->'admissionWaitTime'->>'mean')::FLOAT8 / 1e9` |

**Defensive filtering pattern:**
```sql
WHERE (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 > 0
```

#### Sampled Object Structure

Same as aggregated metrics: each field contains `mean` and `sqDiff` subfields.

**Example: CPU usage analysis**
```sql
SELECT
  fingerprint_id,
  (statistics->'execution_statistics'->>'cnt')::INT AS sample_size,
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  ROUND(
    (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9,
    3
  ) AS mean_cpu_seconds,
  metadata->>'query' AS query
FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
ORDER BY mean_cpu_seconds DESC
LIMIT 10;
```

## Type Casting Patterns

### Safe Casting with NULL Handling

Always use defensive NULL checks and COALESCE for optional fields:

```sql
-- Safe integer extraction
COALESCE((statistics->'statistics'->>'failureCount')::INT, 0)

-- Safe float extraction with validation
CASE
  WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    AND (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean') IS NOT NULL
  THEN (statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9
  ELSE NULL
END AS mean_cpu_seconds

-- Boolean with default
COALESCE((metadata->>'fullScan')::BOOL, false)
```

### Common Type Casting Examples

```sql
-- Text extraction (no casting needed)
metadata->>'db'                                    -- Returns: 'mydb'

-- Integer extraction
(statistics->'statistics'->>'cnt')::INT            -- Returns: 1000

-- Float extraction
(statistics->'statistics'->'runLat'->>'mean')::FLOAT8  -- Returns: 0.523

-- Boolean extraction
(metadata->>'fullScan')::BOOL                      -- Returns: true

-- JSONB array access
metadata->'index_recommendations'                  -- Returns: [{"type":"index","SQL":"..."}]
jsonb_array_length(metadata->'index_recommendations')  -- Returns: 1

-- Nested object extraction (chained ->)
statistics->'statistics'->'runLat'->>'mean'        -- Extract mean from runLat object
```

### Unit Conversions

```sql
-- Nanoseconds to seconds
(statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9

-- Bytes to megabytes
(statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576

-- Bytes to gigabytes
(statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1073741824

-- Latency already in seconds (no conversion)
(statistics->'statistics'->'runLat'->>'mean')::FLOAT8
```

## Version Compatibility Notes

**Field availability varies by CockroachDB version:**

| Field | Introduced | Notes |
|-------|------------|-------|
| `index_recommendations` | v21.1+ | May be NULL if optimizer has no recommendations |
| `failureCount` | v21.2+ | May not exist in earlier versions; use COALESCE |
| `admissionWaitTime` | v22.1+ | Reflects admission control feature introduction |
| `cpuSQLNanos` | v20.2+ | Replaces older CPU metrics in earlier versions |

**Compatibility check query:**
```sql
-- Verify field existence before using in production queries
SELECT
  CASE WHEN metadata ? 'index_recommendations' THEN 'available' ELSE 'missing' END AS idx_rec,
  CASE WHEN statistics->'statistics' ? 'failureCount' THEN 'available' ELSE 'missing' END AS fail_cnt,
  CASE WHEN statistics->'execution_statistics' ? 'admissionWaitTime' THEN 'available' ELSE 'missing' END AS admission
FROM crdb_internal.statement_statistics
LIMIT 1;
```

## Common Extraction Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid input syntax for type double precision: ""` | Extracting NULL value as FLOAT8 | Add NULL check: `WHERE field IS NOT NULL` |
| `cannot extract element from a scalar` | Using `->` on text field | Use `->>` for final extraction, `->` for nested objects |
| `operator does not exist: text::boolean` | Wrong extraction operator for boolean | Use `->>` then cast: `(metadata->>'fullScan')::BOOL` |
| `invalid input syntax for type json` | Malformed JSON or typo in field path | Verify field name spelling; check JSONB structure with `SELECT metadata` |
| Division by zero | NULLIF not used in denominator | Wrap: `NULLIF((statistics->'statistics'->>'cnt')::INT, 0)` |

## Complete Example: Multi-Field Extraction

```sql
SELECT
  fingerprint_id,

  -- Metadata fields
  metadata->>'db' AS database,
  metadata->>'app' AS application,
  substring(metadata->>'query', 1, 100) AS query_preview,
  (metadata->>'fullScan')::BOOL AS is_full_scan,

  -- Aggregated statistics
  (statistics->'statistics'->>'cnt')::INT AS total_executions,
  (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS mean_run_lat_sec,
  (statistics->'statistics'->'rowsRead'->>'mean')::FLOAT8 AS mean_rows_read,
  COALESCE((statistics->'statistics'->>'failureCount')::INT, 0) AS failures,

  -- Sampled execution statistics (defensive)
  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN (statistics->'execution_statistics'->>'cnt')::INT
    ELSE NULL
  END AS sample_size,

  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN ROUND((statistics->'execution_statistics'->'cpuSQLNanos'->>'mean')::FLOAT8 / 1e9, 3)
    ELSE NULL
  END AS mean_cpu_sec,

  CASE
    WHEN (statistics->'execution_statistics'->>'cnt') IS NOT NULL
    THEN ROUND((statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576, 2)
    ELSE NULL
  END AS mean_mem_mb,

  -- Index recommendations
  CASE
    WHEN metadata->'index_recommendations' IS NOT NULL
      AND jsonb_array_length(metadata->'index_recommendations') > 0
    THEN jsonb_array_length(metadata->'index_recommendations')
    ELSE 0
  END AS num_index_recommendations,

  aggregated_ts

FROM crdb_internal.statement_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 > 0.5
ORDER BY (statistics->'statistics'->'runLat'->>'mean')::FLOAT8 DESC
LIMIT 20;
```

## Additional Resources

- **Official schema:** [crdb_internal documentation](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)
- **JSONB operators:** [PostgreSQL JSONB functions](https://www.postgresql.org/docs/current/functions-json.html) (CockroachDB compatible)
- **Metrics interpretation:** See [metrics-and-units.md](metrics-and-units.md)
- **Query examples:** See [sql-query-variations.md](sql-query-variations.md)

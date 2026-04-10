---
name: profiling-transaction-fingerprints
description: Analyzes transaction fingerprints using aggregated statistics from crdb_internal.transaction_statistics to identify high-retry transactions, contention patterns, and commit latency issues. Provides historical transaction-level analysis to understand which statement combinations are causing retries, contention, or performance degradation. Use when investigating transaction retry storms, analyzing commit latency trends, or understanding statement composition of problematic transactions without DB Console access.
compatibility: Requires SQL access with VIEWACTIVITY or VIEWACTIVITYREDACTED cluster privilege. Uses crdb_internal.transaction_statistics (production-safe). Execution statistics fields are sampled and may be sparse.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Profiling Transaction Fingerprints

Analyzes historical transaction performance patterns using aggregated SQL statistics to identify high-retry transactions, contention patterns, and commit latency issues. Uses `crdb_internal.transaction_statistics` for time-windowed analysis of retry behavior, commit latency, and statement composition - entirely via SQL without requiring DB Console access.

**Complement to profiling-statement-fingerprints:** This skill analyzes transaction-level patterns (groups of statements with retry behavior); for statement-level optimization, see [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md).

**Complement to triaging-live-sql-activity:** This skill analyzes historical transaction patterns; for immediate triage of currently active transactions, see [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md).

## When to Use This Skill

- Identify transactions with high retry counts
- Analyze commit latency trends for transaction fingerprints
- Find transactions with high contention at transaction boundary
- Understand statement composition of problematic transactions
- Investigate transaction retry storms or abort patterns
- SQL-only historical transaction analysis without DB Console access

**For immediate incident response:** Use [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) to triage currently active transactions and cancel runaway work.
**For statement-level optimization:** Use [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) to analyze individual query patterns.

## Prerequisites

- SQL connection to CockroachDB cluster
- `VIEWACTIVITY` or `VIEWACTIVITYREDACTED` cluster privilege for cluster-wide visibility
  - Same privilege requirements as profiling-statement-fingerprints
- Understanding of transaction performance concepts
- Transaction statistics collection enabled (default): `sql.stats.automatic_collection.enabled = true`

**Check transaction stats collection:**
```sql
SHOW CLUSTER SETTING sql.stats.automatic_collection.enabled;
-- Should return: true
```

See [triaging-live-sql-activity permissions reference](../triaging-live-sql-activity/references/permissions.md) for RBAC setup (same privileges).

## Core Concepts

### Transaction Fingerprints vs Live Transactions

**Transaction fingerprint:** Normalized transaction pattern grouping statements with parameterized constants.

**Key differences:**
- **Time scope:** Historical hourly buckets vs real-time current state
- **Granularity:** Aggregated retry/commit stats vs individual transaction instances
- **Relationship:** Transaction = collection of statement fingerprints

### Time-Series Bucketing

**aggregated_ts:** Hourly UTC buckets (e.g., `2026-02-21 14:00:00` = 14:00-14:59 executions)
**Data retention:** Default ~7 days (check `sql.stats.persisted_rows.max`)
**Best practice:** Always filter by time window: `WHERE aggregated_ts > now() - INTERVAL '24 hours'`

### Aggregated vs Sampled Metrics

| Metric Category | JSON Path | Scope | Use Case |
|-----------------|-----------|-------|----------|
| **Aggregated** | `statistics.statistics.*` | All executions | Retries, commit latency, execution counts |
| **Sampled** | `statistics.execution_statistics.*` | Probabilistic sample (~10%) | Contention, network, memory/disk |

**Critical:** Sampled metrics have `cnt` field showing sample size. Always check:
```sql
WHERE (statistics->'execution_statistics'->>'cnt') IS NOT NULL
```

### JSON Field Extraction

CockroachDB stores transaction metadata and statistics as JSONB. Use these operators:

**Operators:**
- `->`: Extract JSON object/value (returns JSON)
- `->>`: Extract as text (returns text)
- `::TYPE`: Cast to specific type
- `encode(fingerprint_id, 'hex')`: Convert binary fingerprint to hex string

**Transaction-specific examples:**
```sql
encode(fingerprint_id, 'hex') AS txn_fingerprint_id                     -- Hex encoding
(statistics->'statistics'->>'maxRetries')::INT                           -- Max retry count
(statistics->'statistics'->'retryLat'->>'mean')::FLOAT8                  -- Retry latency (seconds)
(statistics->'statistics'->'commitLat'->>'mean')::FLOAT8                 -- Commit latency (seconds)
(statistics->'statistics'->'svcLat'->>'mean')::FLOAT8                    -- Service latency (seconds)
metadata->'stmtFingerprintIDs' AS stmt_fingerprint_ids_json             -- Statement composition
```

**Units:**
- Latency fields: **seconds** (FLOAT8)
- CPU/contention: **nanoseconds** (divide by 1e9 for seconds)
- Memory/disk: **bytes** (consider / 1048576 for MB)

See [JSON field reference](references/json-field-reference.md) for complete schema.

### Statement Composition

**metadata.stmtFingerprintIDs:** JSONB array mapping transaction to constituent statements

**Use case:** Understand which statements compose high-retry transactions

**Cross-reference workflow:** Join transaction_statistics with statement_statistics on fingerprint IDs

**Example pattern:**
```sql
-- Extract statement fingerprint IDs from transaction
metadata -> 'stmtFingerprintIDs' AS stmt_ids

-- Use with jsonb_array_elements_text to expand and join
jsonb_array_elements_text(metadata->'stmtFingerprintIDs') AS stmt_fingerprint_id
```

## Core Diagnostic Queries

### Query 1: Top Transactions by Retries and Contention

```sql
-- Identify transactions with high retry counts and contention
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'db' AS database,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'cnt')::INT AS execution_count,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_seconds,
  (statistics->'execution_statistics'->'contentionTime'->>'mean')::FLOAT8 / 1e9 AS mean_contention_seconds,
  aggregated_ts
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
ORDER BY (statistics->'statistics'->>'maxRetries')::INT DESC
LIMIT 20;
```

**Key columns:** `max_retries` shows maximum retry count; `mean_retry_lat_seconds` shows time spent in retries; `mean_contention_seconds` shows lock wait time.

**Interpretation:** High max_retries (>10) indicates transaction conflicts; correlate with contention to identify lock hotspots.

### Query 2: Statement Composition Analysis

```sql
-- Extract statement fingerprints for high-retry transactions
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  t.metadata->>'app' AS application,
  (t.statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  jsonb_array_length(t.metadata->'stmtFingerprintIDs') AS num_statements,
  t.metadata->'stmtFingerprintIDs' AS stmt_fingerprint_ids,
  t.aggregated_ts
FROM crdb_internal.transaction_statistics t
WHERE t.aggregated_ts > now() - INTERVAL '24 hours'
  AND (t.statistics->'statistics'->>'maxRetries')::INT > 10
  AND t.metadata->'stmtFingerprintIDs' IS NOT NULL
ORDER BY max_retries DESC
LIMIT 20;
```

**Key columns:** `num_statements` shows transaction complexity; `stmt_fingerprint_ids` contains statement IDs for cross-reference with statement_statistics.

**Use case:** Understand which statement combinations cause retries; use Query 7 to drill down to specific statements.

### Query 3: High Commit Latency Transactions

```sql
-- Find transactions with slow commit latency
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'db' AS database,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'cnt')::INT AS execution_count,
  (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 AS mean_commit_lat_seconds,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_seconds,
  ROUND(
    ((statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS commit_pct_of_service_lat,
  aggregated_ts
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 > 0.1  -- > 100ms commit latency
ORDER BY (statistics->'statistics'->'commitLat'->>'mean')::FLOAT8 DESC
LIMIT 20;
```

**Key columns:** `mean_commit_lat_seconds` shows 2PC commit time; `commit_pct_of_service_lat` shows what percentage of total latency is commit overhead.

**Interpretation:** High commit percentage (>20%) suggests distributed transaction overhead, replication delays, or cross-region writes.

### Query 4: Retry Rate by Application

```sql
-- Analyze retry patterns by application
SELECT
  metadata->>'app' AS application,
  metadata->>'db' AS database,
  COUNT(*) AS transaction_fingerprint_count,
  SUM((statistics->'statistics'->>'cnt')::INT) AS total_executions,
  AVG((statistics->'statistics'->>'maxRetries')::INT) AS avg_max_retries,
  MAX((statistics->'statistics'->>'maxRetries')::INT) AS overall_max_retries,
  AVG((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8) AS avg_retry_lat_seconds
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
GROUP BY metadata->>'app', metadata->>'db'
ORDER BY avg_max_retries DESC
LIMIT 20;
```

**Use case:** Application-level health scorecard; identify which applications have the most problematic transaction patterns.

**Customization:** Adjust time window to 7 days for trends; filter by specific database.

### Query 5: Transaction Resource Consumption

```sql
-- Find transactions with high resource usage
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'cnt')::INT AS execution_count,
  (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576 AS mean_network_mb,
  (statistics->'execution_statistics'->'maxMemUsage'->>'mean')::FLOAT8 / 1048576 AS mean_mem_mb,
  (statistics->'execution_statistics'->'maxDiskUsage'->>'mean')::FLOAT8 / 1048576 AS mean_disk_mb,
  ROUND(
    ((statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 / 1048576) *
    (statistics->'statistics'->>'cnt')::INT, 2
  ) AS estimated_total_network_mb,
  aggregated_ts
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'execution_statistics'->>'cnt') IS NOT NULL
  AND (statistics->'execution_statistics'->'networkBytes'->>'mean')::FLOAT8 > 0
ORDER BY estimated_total_network_mb DESC
LIMIT 20;
```

**Key columns:** `mean_network_mb` shows distributed transaction overhead; `mean_disk_mb` > 0 indicates memory spill.

**Interpretation:** High network bytes suggest cross-region transactions or inefficient distribution; disk usage indicates memory pressure.

### Query 6: Retry Latency Decomposition

```sql
-- Understand retry latency as percentage of service latency
SELECT
  encode(fingerprint_id, 'hex') AS txn_fingerprint_id,
  metadata->>'app' AS application,
  (statistics->'statistics'->>'cnt')::INT AS execution_count,
  (statistics->'statistics'->>'maxRetries')::INT AS max_retries,
  (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 AS mean_retry_lat_seconds,
  (statistics->'statistics'->'svcLat'->>'mean')::FLOAT8 AS mean_service_lat_seconds,
  ROUND(
    ((statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 /
    NULLIF((statistics->'statistics'->'svcLat'->>'mean')::FLOAT8, 0)) * 100, 2
  ) AS retry_pct_of_service_lat,
  aggregated_ts
FROM crdb_internal.transaction_statistics
WHERE aggregated_ts > now() - INTERVAL '24 hours'
  AND (statistics->'statistics'->>'maxRetries')::INT > 0
  AND (statistics->'statistics'->'retryLat'->>'mean')::FLOAT8 > 0
ORDER BY retry_pct_of_service_lat DESC
LIMIT 20;
```

**Interpretation:** High retry percentage (>30%) means most latency is spent retrying due to contention; optimize transaction boundaries or schema.

### Query 7: Cross-Reference Transaction to Statements

```sql
-- Join transaction statistics with statement statistics to see constituent statements
SELECT
  encode(t.fingerprint_id, 'hex') AS txn_fingerprint_id,
  t.metadata->>'app' AS txn_application,
  (t.statistics->'statistics'->>'maxRetries')::INT AS txn_max_retries,
  stmt_fp_id AS stmt_fingerprint_id,
  s.metadata->>'query' AS statement_query,
  (s.statistics->'statistics'->'runLat'->>'mean')::FLOAT8 AS stmt_mean_run_lat_seconds,
  t.aggregated_ts
FROM crdb_internal.transaction_statistics t
CROSS JOIN LATERAL jsonb_array_elements_text(t.metadata->'stmtFingerprintIDs') AS stmt_fp_id
LEFT JOIN crdb_internal.statement_statistics s
  ON s.fingerprint_id = decode(stmt_fp_id, 'hex')
  AND s.aggregated_ts = t.aggregated_ts
WHERE t.aggregated_ts > now() - INTERVAL '24 hours'
  AND (t.statistics->'statistics'->>'maxRetries')::INT > 10
  AND t.metadata->'stmtFingerprintIDs' IS NOT NULL
ORDER BY txn_max_retries DESC, stmt_mean_run_lat_seconds DESC
LIMIT 50;
```

**Use case:** Drill down from high-retry transactions to specific problematic statements; identify which statement in a transaction is causing retries.

**Note:** Uses `decode(stmt_fp_id, 'hex')` to convert hex string back to binary for join with statement_statistics.

## Common Workflows

### Workflow 1: Retry Storm Investigation

1. **Identify high-retry transactions:** Run Query 1, focus on `max_retries > 20`
2. **Analyze retry patterns by application:** Run Query 4 to identify problematic apps
3. **Examine statement composition:** Run Query 7 to see which statements are in high-retry transactions
4. **Cross-reference live activity:** If ongoing, use triaging-live-sql-activity to check current transaction state
5. **Remediate:** Adjust transaction boundaries, batch operations, optimize statements identified in step 3

### Workflow 2: Commit Latency Analysis

1. **Find slow commit transactions:** Run Query 3, focus on `commit_pct_of_service_lat > 20%`
2. **Check for contention correlation:** Run Query 1 for same transaction fingerprints to see if contention is related
3. **Analyze time patterns:** Group Query 3 by `aggregated_ts` to identify peak periods
4. **Resource investigation:** Run Query 5 to check if network overhead correlates with commit latency
5. **Remediate:** Consider batching operations, partitioning tables, or investigating replication configuration

### Workflow 3: Statement Composition Drill-Down

1. **Identify problematic transactions:** Run Query 1 or Query 3 to find high-retry or slow-commit transactions
2. **Extract statement IDs:** Run Query 2 to see `stmtFingerprintIDs` for target transactions
3. **Join with statement_statistics:** Run Query 7 to see full statement details
4. **Optimize bottleneck statements:** Use profiling-statement-fingerprints skill to analyze and optimize identified statements
5. **Validate retry reduction:** Re-run Query 1 after optimizations to confirm improved retry counts

### Workflow 4: Application Health Scorecard

1. **Generate retry metrics by app:** Run Query 4 to get application-level retry statistics
2. **Correlate with commit latency:** Modify Query 3 to group by application
3. **Resource attribution:** Run Query 5 grouped by application to see resource impact
4. **Trend analysis:** Run queries with 7-day window and compare hourly buckets
5. **Contact application teams:** Provide specific transaction fingerprints with high retries or latency for investigation

## Safety Considerations

**Read-only operations:**
All queries are `SELECT` statements against `crdb_internal.transaction_statistics`, which is production-approved and safe for diagnostic use.

**Performance impact:**

| Consideration | Impact | Mitigation |
|---------------|--------|------------|
| Large table | High transaction diversity = many rows | Always use `WHERE aggregated_ts > now() - INTERVAL '24 hours'` and `LIMIT` |
| JSON parsing | CPU overhead for JSONB extraction | Avoid tight loops; use specific time windows |
| Broad windows | 7-day queries = more rows | Default to 24h; expand only when needed |
| Sampled metrics | NULL handling overhead | Use defensive `WHERE (statistics->'execution_statistics'->>'cnt') IS NOT NULL` |

**Privacy:** Use `VIEWACTIVITYREDACTED` to redact query constants in multi-tenant environments (same as statement profiling).

**Default time window:** 24 hours balances recent data with manageable result sets.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Empty results | No data in window, or stats collection disabled | Check `sql.stats.automatic_collection.enabled = true` |
| `column does not exist` | JSON field typo or version mismatch | Verify field names; check CockroachDB version |
| NULL in sampled metrics | Metric not sampled in bucket | Filter: `WHERE (statistics->'execution_statistics'->>'cnt') IS NOT NULL` |
| `fingerprint_id` not hex | Default binary format | Use `encode(fingerprint_id, 'hex')` for readability |
| Statement join fails | Mismatched aggregated_ts or fingerprint format | Ensure same time bucket and proper type casting with `decode()` |
| Very slow query | Large table, no time filter | Always add time window and LIMIT |
| Empty `stmtFingerprintIDs` | Single-statement transactions or old version | Normal for simple transactions |

## Key Considerations

- **Time windows:** Default to 24h; expand to 7d for trends
- **Sampled metrics:** Not all executions captured; check sample size (`cnt`)
- **JSON field safety:** Use defensive NULL checks; handle type casting errors
- **Privacy:** Use VIEWACTIVITYREDACTED in production
- **Performance:** Always include time filters and LIMIT clauses
- **Complement to statement profiling:** Use together for complete coverage (transaction + statement)
- **Complement to live triage:** Historical patterns vs real-time (use both)
- **Data retention:** Default ~7 days; verify with `sql.stats.persisted_rows.max`
- **Retry semantics:** `maxRetries` is maximum across all executions in bucket, not average
- **Fingerprint encoding:** Use `encode(fingerprint_id, 'hex')` for human-readable IDs

## References

**Skill references:**
- [JSON field schema and extraction](references/json-field-reference.md)
- [Metrics catalog and units](references/metrics-and-units.md)
- [SQL query variations](references/sql-query-variations.md)
- [RBAC and privileges](../triaging-live-sql-activity/references/permissions.md) (shared with triaging-live-sql-activity)

**Official CockroachDB Documentation:**
- [crdb_internal](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)
- [Transactions Page (DB Console)](https://www.cockroachlabs.com/docs/stable/ui-transactions-page.html)
- [Monitor and Analyze Transaction Contention](https://www.cockroachlabs.com/docs/stable/monitor-and-analyze-transaction-contention.html)
- [VIEWACTIVITY privilege](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

**Related skills:**
- [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) - For statement-level optimization
- [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) - For immediate triage of active transactions

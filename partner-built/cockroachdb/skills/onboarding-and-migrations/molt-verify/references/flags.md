# molt verify: Full Flag Reference

## Required

| Flag | Description |
|------|-------------|
| `--source` | Source DB connection string |
| `--target` | Target CockroachDB connection string |

## Connection

| Flag | Default | Description |
|------|---------|-------------|
| `--source-cdb` | - | Oracle CDB connection string (multi-tenant setups) |
| `--allow-tls-mode-disable` | false | Allow insecure connections without TLS |

## Verification Scope

| Flag | Default | Description |
|------|---------|-------------|
| `--rows` | true | Verify row data in addition to schema. Set `false` for schema-only |
| `--table-filter` | - | POSIX regex to include only matching tables |
| `--transformations-file` | - | JSON file with column exclusions and table aliases |
| `--filter-path` | - | JSON file with per-table WHERE clauses (not supported for Oracle) |
| `--case-sensitive` | false | Case-sensitive name comparison |

## Performance & Concurrency

| Flag | Default | Description |
|------|---------|-------------|
| `--concurrency` | 0 (= CPU count) | Number of tables to verify in parallel |
| `--concurrency-per-table` | 1 | Number of PK-range shards per table |
| `--row-batch-size` | 20000 | Rows fetched per shard iteration |
| `--rows-per-second` | 0 (unlimited) | Rate limit per shard (rows/sec) |
| `--verify-statement-timeout` | `1h` | SQL query timeout per statement |

## Logging & Output

| Flag | Default | Description |
|------|---------|-------------|
| `--log-file` | `verify-{datetime}.log` | Log file path or `stdout` |
| `--log-level` | `info` | `debug`, `info`, `warn`, `error` |
| `--metrics-listen-addr` | `localhost:8888` | Prometheus metrics scrape endpoint |

## Automation

| Flag | Default | Description |
|------|---------|-------------|
| `--non-interactive` | false | Skip confirmation prompts (for CI/automation) |
| `--compile-only` | false | Validate flags without connecting to DBs |

## Hidden / Internal

| Flag | Default | Description |
|------|---------|-------------|
| `--show-connection-logging` | false | Log full connection strings (sensitive — avoid in production) |
| `--test-only` | false | Deterministic timing for test output |

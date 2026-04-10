# molt fetch: Full Flag Reference

## Required

| Flag | Description |
|------|-------------|
| `--source` | Source DB connection string |
| `--target` | Target CockroachDB connection string |
| One of: `--bucket-path`, `--direct-copy`, `--local-path` | Intermediate storage |

## Storage

| Flag | Default | Description |
|------|---------|-------------|
| `--bucket-path` | - | Cloud storage URI (`s3://`, `gs://`, `azure://`) |
| `--direct-copy` | false | Skip intermediate storage |
| `--local-path` | - | Local filesystem path |
| `--local-path-listen-addr` | - | HTTP server addr for local path |
| `--local-path-crdb-access-addr` | - | CRDB-visible addr for local HTTP server |
| `--use-implicit-auth` | false | Use IAM/ADC/managed identity |
| `--assume-role` | - | AWS role ARN to assume |
| `--import-region` | - | AWS region for IMPORT statement |

## Data Movement

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | `data-load` | `data-load`, `export-only`, `import-only` |
| `--table-handling` | `none` | `none`, `drop-on-target-and-recreate`, `truncate-if-exists` |
| `--use-copy` | false | Use COPY FROM instead of IMPORT INTO |
| `--compression` | `gzip` | `gzip` or `none` (must be `none` with `--use-copy`) |
| `--dry-run` | false | Test one row without full migration |
| `--compile-only` | false | Validate flags without connecting |

## Filtering

| Flag | Default | Description |
|------|---------|-------------|
| `--table-filter` | - | POSIX regex: include matching tables |
| `--table-exclusion-filter` | - | POSIX regex: exclude matching tables |
| `--schema-filter` | - | Schema filter (PostgreSQL only) |
| `--case-sensitive` | false | Case-sensitive name matching |
| `--filter-path` | - | JSON file with per-table WHERE clauses |

## Performance

| Flag | Default | Description |
|------|---------|-------------|
| `--table-concurrency` | 4 | Tables migrated in parallel |
| `--export-concurrency` | 4 | Export threads per table |
| `--row-batch-size` | 100000 | Rows per SELECT during export |
| `--flush-size` | varies | Bytes before flushing to storage |
| `--flush-rows` | 0 | Rows before flushing (0 = disabled) |
| `--import-batch-size` | 1000 | Files per IMPORT INTO batch |

## Type & Schema

| Flag | Default | Description |
|------|---------|-------------|
| `--type-map-file` | - | JSON file with custom type mappings |
| `--transformations-file` | - | JSON file with column exclusions/aliases |
| `--skip-pk-check` | false | Allow tables without primary keys |
| `--use-stats-based-sharding` | false | Stats-based sharding (PG 11+; run ANALYZE first) |

## Resumption

| Flag | Default | Description |
|------|---------|-------------|
| `--fetch-id` | - | Previous run ID to resume |
| `--continuation-token` | - | Token for specific table resumption |
| `--continuation-file-name` | - | File to resume from within a table |
| `--non-interactive` | false | Skip confirmation prompts |

## Logging & Monitoring

| Flag | Default | Description |
|------|---------|-------------|
| `--log-file` | `fetch-{datetime}.log` | Log file path or `stdout` |
| `--logging` | `info` | `info`, `debug`, `trace` |
| `--use-console-writer` | false | Cleaner output (slightly more latency) |
| `--metrics-listen-addr` | - | `host:port` for Prometheus metrics |
| `--metrics-scrape-interval` | `5s` | Metrics collection interval |
| `--pprof-listen-addr` | - | `host:port` for pprof profiling |

## Connection & Timeouts

| Flag | Default | Description |
|------|---------|-------------|
| `--allow-tls-mode-disable` | false | Allow insecure TLS connections |
| `--export-statement-timeout` | `1h` | Source query timeout |
| `--export-retry-max-attempts` | 3 | Retry attempts for export queries |
| `--export-retry-max-duration` | `5m` | Max duration for export retries |
| `--crdb-pts-refresh-interval` | `10m` | Protected timestamp refresh interval |
| `--crdb-pts-duration` | `24h` | Protected timestamp lifetime |

## PostgreSQL-Specific

| Flag | Default | Description |
|------|---------|-------------|
| `--pglogical-replication-slot-name` | `molt_slot` | Replication slot name |
| `--pglogical-replication-slot-plugin` | `pgoutput` | Plugin for slot |
| `--pglogical-publication-name` | `molt_fetch` | Publication name |
| `--pglogical-publication-and-slot-drop-and-recreate` | false | Drop/recreate if exists |
| `--ignore-replication-check` | false | Skip replication prereq checks |

## Oracle-Specific

| Flag | Default | Description |
|------|---------|-------------|
| `--oracle-application-users` | - | Comma-separated users to filter transactions |
| `--source-cdb` | - | CDB connection for multi-tenant setups |

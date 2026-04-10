---
name: molt-fetch
description: Guide for using molt fetch to migrate data from PostgreSQL, MySQL, Oracle, or MSSQL to CockroachDB. Use when running molt fetch commands, configuring storage backends, handling fetch failures/resumption, or chaining fetch with verify.
compatibility: Requires molt binary. Source DB must be accessible. For Oracle, CGO and Oracle Instant Client required.
metadata:
  author: cockroachdb
  version: "1.0"
---

# molt fetch

Bulk data migration from source databases (PostgreSQL, MySQL, Oracle, MSSQL) to CockroachDB.

## Basic Structure

```bash
molt fetch \
  --source "<source-conn>" \
  --target "<crdb-conn>" \
  --bucket-path "s3://bucket/prefix"   # or --direct-copy or --local-path
  [options]
```

## Storage Backends (pick one)

| Option | When to use |
|--------|-------------|
| `--bucket-path "s3://..."` | AWS S3 (also `gs://` for GCS, `azure://` for Azure) |
| `--direct-copy` | No intermediate storage; fastest for accessible networks |
| `--local-path "/tmp/molt"` + `--local-path-listen-addr "0.0.0.0:9005"` | CRDB must reach the listen addr |

Cloud auth: pass `--use-implicit-auth` for IAM/ADC/managed identity, or set `AWS_ACCESS_KEY_ID`/`GOOGLE_APPLICATION_CREDENTIALS` env vars.

## Table Handling (`--table-handling`)

| Value | Behavior |
|-------|----------|
| `none` (default) | Append to existing tables |
| `drop-on-target-and-recreate` | Drop + recreate from source schema; enables auto schema creation |
| `truncate-if-exists` | Truncate before loading; errors if table missing |

## Import Mode

**IMPORT INTO** (default): Table goes OFFLINE during load. Highest throughput.

**COPY FROM** (`--use-copy`): Table stays ONLINE. Use with `--direct-copy`. Cannot use compression.

```bash
# Zero-downtime load
molt fetch --source "..." --target "..." --direct-copy --use-copy
```

## Key Flags

```bash
# Filtering
--table-filter "customers|orders"      # POSIX regex for tables to include
--table-exclusion-filter "temp_.*"     # exclude pattern
--schema-filter "public"               # PostgreSQL only

# Performance
--table-concurrency 4                  # parallel tables (default: 4)
--export-concurrency 4                 # export threads (default: 4)
--row-batch-size 100000                # rows per SELECT (default: 100k)

# Schema
--type-map-file "types.json"           # custom type mappings
--transformations-file "transforms.json"  # column exclusions, table aliases

# Logging
--log-file "migration.log"             # or "stdout"
--logging debug                        # info (default), debug, trace
--metrics-listen-addr "0.0.0.0:3030"  # Prometheus scrape endpoint
```

## Source-Specific Prerequisites

**MySQL**: GTID mode required (`gtid_mode=ON`, `enforce_gtid_consistency=ON`). `ONLY_FULL_GROUP_BY` must be off. Or use `--ignore-replication-check`.

**Oracle**: Binary must be built with `CGO_ENABLED=1 -tags="cgo source_all"`. Oracle Instant Client in `LD_LIBRARY_PATH`.

**PostgreSQL**: Replication privileges needed, or `--ignore-replication-check`.

## Common Workflows

### 1. Validate before migrating
```bash
molt fetch --dry-run --source "..." --target "..." --bucket-path "s3://..."
# Exports 1 row, imports, verifies, cleans up. Returns immediately.
```

### 2. Full migration with schema creation
```bash
molt fetch \
  --source "postgresql://user:pass@pg:5432/db" \
  --target "postgresql://root@crdb:26257/db" \
  --bucket-path "s3://mybucket/migration" \
  --table-handling drop-on-target-and-recreate \
  --table-filter "customers|orders|payments" \
  --log-file migration.log
```

### 3. Resume after failure
```bash
# List available continuation tokens
molt fetch tokens --fetch-id "abc-123" --target "postgresql://root@crdb:26257/db"

# Resume all failed tables
molt fetch \
  --source "..." --target "..." \
  --bucket-path "s3://mybucket/migration" \
  --fetch-id "abc-123" \
  --non-interactive
```

### 4. Validate flag syntax without connecting
```bash
molt fetch --compile-only --source "..." --target "..." --bucket-path "..."
# Returns JSON: {"status":"ok","message":"arguments parsed successfully"}
```

## Error Recovery

| Error | Cause | Fix |
|-------|-------|-----|
| "GTID-based replication not enabled" | MySQL missing GTID | Enable `gtid_mode=ON` or add `--ignore-replication-check` |
| "Column mismatch" | Schema diverged | Fix target schema manually or use `--type-map-file` |
| Silent IMPORT INTO | CockroachDB import running | `SHOW JOBS` on CRDB to check progress |
| "timestamp in the future" | Docker/Mac clock drift | Sync clocks between hosts |

## Gotchas

- COPY mode: cannot use `--compression gzip`; must use `--compression none` (or omit, default is none with copy)
- Table is **offline** during IMPORT INTO — use `--use-copy` for zero downtime
- Schema changes between runs require starting from scratch
- `--fetch-id` continuation tokens live in the target's exceptions table
- For MySQL, `--ignore-replication-check` skips GTID validation but replication-dependent features won't work
- After fetch, run `molt verify` to confirm data integrity

See [flags reference](references/flags.md) for the full flag list.

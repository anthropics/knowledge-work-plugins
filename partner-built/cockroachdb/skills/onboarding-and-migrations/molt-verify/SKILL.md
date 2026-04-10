---
name: molt-verify
description: Guide for using molt verify to compare source and target databases for schema and row-level consistency after a migration. Use when running verify commands, tuning concurrency/sharding, handling schema mismatches, or validating data integrity post-migration.
compatibility: Requires molt binary. Source and target DBs must be accessible. Oracle requires CGO build.
metadata:
  author: cockroachdb
  version: "1.0"
---

# molt verify

Compares source and target databases for schema (DDL) and row (data) consistency. Run after `molt fetch` to confirm migration integrity.

## Basic Structure

```bash
molt verify \
  --source "<source-conn>" \
  --target "<crdb-conn>" \
  [options]
```

## Verification Phases

**Phase 1 — Schema:** Compares table presence, columns, types, NOT NULL constraints, and primary key structure.

**Phase 2 — Rows** (default, `--rows=true`): Iterates source rows in PK order and compares against target. Reports missing, extraneous, and mismatched rows per shard.

## Modes

| Mode | Command | Use When |
|------|---------|----------|
| Full (default) | `molt verify --source "..." --target "..."` | Post-migration integrity check |
| Schema-only | `molt verify ... --rows=false` | Fast DDL check; no data I/O |
| Compile-only | `molt verify ... --compile-only` | Validate flag syntax without connecting |

## Concurrency & Sharding

```bash
# Default: CPU-count tables in parallel, 1 shard/table, 20k rows/batch
molt verify --source "..." --target "..."

# Large tables: parallelize within a single table
molt verify --source "..." --target "..." \
  --concurrency 1 --concurrency-per-table 8 --row-batch-size 50000

# Rate-limited (minimize production impact)
molt verify --source "..." --target "..." \
  --rows-per-second 1000 --concurrency 2
```

Sharding splits a table's PK range across workers. Supported PK types: INT, FLOAT, DECIMAL, UUID. Falls back to a single full-scan for unsupported types.

## Common Workflows

### 1. Post-migration sanity check
```bash
molt verify \
  --source "postgresql://user:pass@pg:5432/db" \
  --target "postgresql://root@crdb:26257/db"
```

### 2. Schema-only (CI gate)
```bash
molt verify \
  --source "..." --target "..." \
  --rows=false --non-interactive --log-file stdout
```

### 3. Filtered verification (subset of tables)
```bash
molt verify \
  --source "..." --target "..." \
  --table-filter "customers|orders"
```

### 4. Verify with column exclusions
```bash
# transformations.json: {"tables":[{"name":"users","excludedColumns":["temp_col"]}]}
molt verify \
  --source "..." --target "..." \
  --transformations-file transformations.json
```

### 5. Validate flags without connecting
```bash
molt verify --source "..." --target "..." --compile-only
# Returns: {"status":"ok","message":"arguments parsed successfully"}
```

## Source-Specific Prerequisites

**PostgreSQL**: No special requirements. Partition tables (child partitions) are not supported — remove them before verifying.

**MySQL**: Queries current database only. `ONLY_FULL_GROUP_BY` may affect queries; disable if issues arise.

**Oracle**: Binary must be built with `CGO_ENABLED=1 -tags="cgo source_all"`. Oracle Instant Client in `LD_LIBRARY_PATH`. Use `--source-cdb` for multi-tenant (CDB) setups. Selective data verification (`--filter-path`) is not supported.

## Output & Reporting

Each table prints a summary per shard:
```
truth rows seen: 10000, success: 9950, missing: 5, mismatch: 45, extraneous: 0
```

- **missing**: rows present on source but absent on target
- **extraneous**: rows on target with no match on source
- **mismatch**: rows present on both but values differ

Schema issues (missing/extra tables or columns, type mismatches, PK differences) are logged as warnings and do not stop row verification.

Prometheus metrics available at `--metrics-listen-addr` (default `localhost:8888`).

## Error Recovery

| Error | Cause | Fix |
|-------|-------|-----|
| `missing table X on target` | Table not migrated | Rerun fetch or check filters |
| `extraneous table X on target` | Unexpected table | Clean up or adjust `--table-filter` |
| `column type mismatch` | Type conversion issue | Check type mappings or use `--transformations-file` |
| `PRIMARY KEY does not match` | PK structure differs | Inspect schema conversion output |
| `partition table X` | Source has partition tables | Drop/move partitions before verifying |
| `missing a PRIMARY KEY` | No PK on source table | Add PK or use `--rows=false` |
| `TLSModeDisableError` | Insecure connection rejected | Add `--allow-tls-mode-disable` |
| Statement timeout | Query exceeds `--verify-statement-timeout` | Increase timeout or reduce `--row-batch-size` |

## Gotchas

- Schema changes between source and target after migration are not automatically reconciled — fix schema first, then re-run
- `--concurrency` values exceeding 4× CPU count trigger a warning and may degrade performance
- Row verification requires primary keys on both source and target tables; tables without PKs are skipped for row comparison
- `--filter-path` (selective row filters) is not supported for Oracle sources
- Log files contain sensitive query data; avoid `--show-connection-logging` in production logs
- After fetch, always run verify before cutover to confirm data integrity

See [flags reference](references/flags.md) for the full flag list.

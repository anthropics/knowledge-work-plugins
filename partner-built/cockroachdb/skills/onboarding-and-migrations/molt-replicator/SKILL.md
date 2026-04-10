---
name: molt-replicator
description: Guide for using the CockroachDB replicator to continuously replicate changes from PostgreSQL, MySQL, or Oracle to CockroachDB after an initial molt fetch data load. Use when setting up CDC replication, configuring pglogical/mylogical/oraclelogminer, or managing the fetch → replicator cutover workflow.
compatibility: Requires separate replicator binary (not part of molt). Staging CockroachDB database required. Source DB must support logical replication.
metadata:
  author: cockroachdb
  version: "1.0"
---

# molt replicator

Continuous change-data-capture (CDC) replication from source databases to CockroachDB. Run **after** `molt fetch` completes the initial bulk load.

> **Important**: replicator is a **separate binary** from `molt`. It is not invoked by `molt fetch`. The `data-load-and-replication` mode in molt fetch is deprecated — use replicator directly instead.

## Architecture

```
Source DB ──► [replicator] ──► Staging DB (_replicator schema) ──► Target CockroachDB
                  ▲
            Publication/
            Slot/BinLog/
            LogMiner
```

Replicator reads changes from the source, buffers them in a staging schema on the target CRDB cluster, and applies them to the target tables.

## Subcommands by Source

| Source | Command |
|--------|---------|
| PostgreSQL | `replicator pglogical` |
| MySQL | `replicator mylogical` |
| Oracle | `replicator oraclelogminer` |
| Kafka | `replicator kafka` |
| Cloud storage | `replicator objstore` |
| CockroachDB CDC | `replicator start` |

## Full Fetch → Replicator Workflow

### Step 1: Initial bulk load with molt fetch

```bash
molt fetch \
  --source "postgresql://user:pass@source:5432/db" \
  --target "postgresql://root@crdb:26257/db" \
  --bucket-path "s3://mybucket/migration" \
  --table-handling drop-on-target-and-recreate
```

### Step 2: Create publication on source (PostgreSQL)

```sql
-- Run on source PostgreSQL:
CREATE PUBLICATION molt_fetch FOR ALL TABLES;
-- (molt fetch may have already created this; check first)
```

### Step 3: Create staging database on target

```sql
-- Run on target CockroachDB:
CREATE DATABASE _replicator;
```

### Step 4: Test connectivity

```bash
replicator preflight \
  --sourceConn "postgresql://user:pass@source:5432/db" \
  --targetConn "postgresql://root@crdb:26257/db"
```

### Step 5: Start replicator

```bash
replicator pglogical \
  --publicationName "molt_fetch" \
  --sourceConn "postgresql://user:pass@source:5432/db" \
  --stagingConn "postgresql://root@crdb:26257/_replicator" \
  --stagingSchema "_replicator.public" \
  --targetConn "postgresql://root@crdb:26257/db" \
  --targetSchema "public" \
  --metricsAddr "0.0.0.0:8080"
```

### Step 6: Monitor lag

```bash
curl http://localhost:8080/metrics | grep replicator_
# Watch for: mutations applied, unapplied mutations, lag
```

### Step 7: Cutover

1. When lag reaches ~0, redirect app writes to CockroachDB
2. Let replicator drain remaining changes
3. Confirm no new writes on source
4. Stop replicator
5. Decommission source

## Source-Specific Setup

### PostgreSQL (pglogical)

**Source prerequisites:**
- User with `REPLICATION` privilege
- Logical replication enabled (`wal_level = logical`)
- Publication exists (created by `molt fetch` or manually)

```bash
replicator pglogical \
  --publicationName "molt_fetch" \
  --slotName "replicator" \
  --sourceConn "postgresql://..." \
  --stagingConn "postgresql://root@crdb:26257/_replicator" \
  --stagingSchema "_replicator.public" \
  --targetConn "postgresql://root@crdb:26257/db" \
  --targetSchema "public"
```

### MySQL (mylogical)

**Source prerequisites:**
- Binary logging enabled (`binlog_format = ROW`)
- GTID mode on (`gtid_mode=ON`, `enforce_gtid_consistency=ON`)
- User with `REPLICATION CLIENT` privilege

```bash
replicator mylogical \
  --sourceConn "mysql://root:pass@source:3306/db" \
  --stagingConn "postgresql://root@crdb:26257/_replicator" \
  --stagingSchema "_replicator.public" \
  --targetConn "postgresql://root@crdb:26257/db" \
  --targetSchema "public"
```

### Oracle (oraclelogminer)

**Source prerequisites:**
- Archive log mode enabled
- Supplemental logging enabled
- LogMiner permissions granted

```bash
replicator oraclelogminer \
  --sourceConn "oracle://app_user:pass@oracle:1521/db" \
  --stagingConn "postgresql://root@crdb:26257/_replicator" \
  --stagingSchema "_replicator.public" \
  --targetConn "postgresql://root@crdb:26257/db" \
  --targetSchema "public"
```

## Key Flags

```bash
# Performance
--parallelism 16          # concurrent DB transactions (default: 16)
--flushSize 1000          # rows per batch (default: 1000)
--flushPeriod 1s          # flush interval (default: 1s)

# Staging connection pool
--stagingMaxPoolSize 128
--stagingIdleTime 1m
--stagingMaxLifetime 5m

# Target connection pool
--targetMaxPoolSize 128
--targetStatementCacheSize 128

# Retry
--maxRetries 10
--retryInitialBackoff 25ms
--retryMaxBackoff 2s

# Monitoring
--metricsAddr "0.0.0.0:8080"    # Prometheus metrics endpoint
--schemaRefresh 1m               # refresh schema cache (0 = disabled)

# Dead letter queue (failed rows instead of stopping)
--dlqTableName "replicator_dlq"

# Logging
-v                               # debug
-vv                              # trace
--logFormat fluent                # for log aggregators
--logDestination "/var/log/replicator.log"
```

## Gotchas

- Staging schema (`_replicator.public`) is auto-created by replicator, but the **database** (`_replicator`) must exist first
- `--publicationName` and `--slotName` must match what `molt fetch` created (default: `molt_fetch` / `molt_slot`)
- DLQ table grows over time — monitor and purge failed rows periodically
- Replicator holds an open replication slot on the source — this blocks WAL cleanup; monitor source disk usage
- Graceful shutdown respects `--gracePeriod` (default: 30s); don't SIGKILL without it
- No built-in alerting — set up external alerts on the Prometheus metrics endpoint
- Long cutover windows increase replication lag — plan for a maintenance window if needed

See [flags reference](references/flags.md) for the full flag list.

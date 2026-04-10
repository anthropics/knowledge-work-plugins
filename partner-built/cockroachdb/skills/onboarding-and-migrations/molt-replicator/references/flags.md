# molt replicator: Full Flag Reference

## Common Flags (all subcommands)

| Flag | Default | Description |
|------|---------|-------------|
| `--stagingConn` | - | Staging CockroachDB connection string |
| `--stagingSchema` | `_replicator.public` | Schema for replicator metadata tables |
| `--stagingCreateSchema` | false | Auto-create staging schema |
| `--stagingMaxPoolSize` | 128 | Max staging connection pool size |
| `--stagingIdleTime` | `1m` | Idle connection timeout |
| `--stagingMaxLifetime` | `5m` | Max connection lifetime |
| `--targetConn` | - | Target CockroachDB connection string |
| `--targetSchema` | - | Target schema to replicate into |
| `--targetMaxPoolSize` | 128 | Max target connection pool size |
| `--targetStatementCacheSize` | 128 | Prepared statement cache size |
| `--parallelism` | 16 | Concurrent DB transactions |
| `--flushSize` | 1000 | Rows per batch |
| `--flushPeriod` | `1s` | Flush interval |
| `--scanSize` | 10000 | Rows read from staging per pass |
| `--targetApplyQueueSize` | 1000000 | Mutation buffer size |
| `--maxRetries` | 10 | Retry attempts on failure |
| `--retryInitialBackoff` | `25ms` | Initial retry delay |
| `--retryMaxBackoff` | `2s` | Max retry delay |
| `--retryMultiplier` | 2 | Exponential backoff multiplier |
| `--applyTimeout` | `30s` | Max time per update |
| `--taskGracePeriod` | `1m` | Cleanup time on error |
| `--schemaRefresh` | `1m` | Schema cache refresh interval (`0` = disabled) |
| `--metricsAddr` | - | `host:port` for Prometheus metrics |
| `--stageSanityCheckPeriod` | `10m` | Validate staging apply ordering |
| `--stageUnappliedPeriod` | `1m` | Report unapplied mutations |
| `--dlqTableName` | - | Table for failed/unprocessable rows |
| `--gracePeriod` | `30s` | Graceful shutdown time |
| `--logFormat` | `text` | `text` or `fluent` |
| `--logDestination` | stdout | Log file path |
| `-v` | - | Debug logging |
| `-vv` | - | Trace logging |

## pglogical-specific

| Flag | Default | Description |
|------|---------|-------------|
| `--sourceConn` | - | Source PostgreSQL connection |
| `--publicationName` | - | Publication name on source (must match molt fetch) |
| `--slotName` | `replicator` | Replication slot on source |

## mylogical-specific

| Flag | Default | Description |
|------|---------|-------------|
| `--sourceConn` | - | Source MySQL connection |

## oraclelogminer-specific

| Flag | Default | Description |
|------|---------|-------------|
| `--sourceConn` | - | Source Oracle connection |

## Utility Subcommands

| Command | Description |
|---------|-------------|
| `replicator preflight` | Test source/target connectivity |
| `replicator version` | Show version and build info |
| `replicator make-jwt` | Generate JWT for auth |
| `replicator workload` | Run test workload against target |
| `replicator fakeworkload` | Generate synthetic test data |

# Production-Recommended Cluster Settings

## Tier Key

| Abbreviation | Tier |
|---|---|
| SH | Self-Hosted |
| ADV | CockroachDB Advanced (Dedicated) |
| BYOC | Bring Your Own Cloud |
| STD | CockroachDB Standard |
| All | All tiers |

## Recommended Settings

| Setting | Recommended Value | Default | Why | Tier Applicability |
|---|---|---|---|---|
| `kv.rangefeed.enabled` | `true` | `false` | Required for changefeeds, CDC, and schema change processing. Must be enabled before creating any changefeed. | SH / ADV / BYOC / STD |
| `sql.stats.automatic_collection.enabled` | `true` | `true` | Critical for the cost-based optimizer to generate efficient query plans. Disabling this causes the optimizer to fall back to heuristics, leading to poor plan selection and degraded query performance. | All |
| `server.time_until_store_dead` | `5m0s` | `5m0s` | Controls how long a node must be unreachable before the cluster considers it dead and begins up-replicating data. Lower values trigger faster recovery but risk false positives during transient network issues. Higher values delay recovery. The default is appropriate for most production deployments. | SH |
| `admission.enabled` | `true` | `true` | Enables admission control for overload protection. Prevents cascading failures under heavy load by throttling work at the admission layer rather than allowing unbounded resource consumption. | SH / ADV / BYOC |
| `gc.ttlseconds` | `25h` (`90000`) | `90000` (25h) | Controls MVCC garbage collection. Determines how long revisions of a key are preserved. Must be set high enough to support changefeed backfills and `AS OF SYSTEM TIME` queries. Lowering it reclaims storage faster but may break changefeeds that fall behind. | All |
| `sql.defaults.idle_in_transaction_session_timeout` | Non-zero, e.g. `300s` | `0s` (disabled) | Prevents idle transactions from holding locks, leases, and memory indefinitely. Sessions exceeding this timeout are automatically terminated. Essential for preventing transaction leak issues in connection-pooled environments. | All |
| `sql.defaults.statement_timeout` | Workload-dependent, e.g. `30s` | `0s` (disabled) | Prevents runaway queries from consuming unbounded resources. Value should be set based on expected query latency for the workload. Individual sessions can override with `SET statement_timeout`. | All |
| `kv.snapshot_rebalance.max_rate` | `32 MiB` | `32 MiB` | Controls the rate at which range snapshots are sent during rebalancing operations. Higher values speed up rebalancing but increase network and disk I/O pressure. Increase cautiously on fast networks with SSD storage. | SH |
| `kv.snapshot_recovery.max_rate` | `32 MiB` | `32 MiB` | Controls the rate at which range snapshots are sent during node recovery after a failure. Higher values speed up recovery but increase load on surviving nodes. Consider increasing temporarily during recovery of a large dataset. | SH |
| `diagnostics.reporting.enabled` | Organizational preference | `true` | Controls whether anonymized diagnostic data is sent to Cockroach Labs. Useful for product improvement and proactive support but may be disabled for compliance reasons in air-gapped or restricted environments. | SH |
| `cluster.preserve_downgrade_option` | Empty string unless mid-upgrade | Empty string | Controls upgrade finalization. Set to the current cluster version before starting a rolling upgrade to prevent automatic finalization. Clear it (set to empty) only after verifying all nodes are running the new version and the cluster is healthy. Never change during an active upgrade unless intentionally rolling back. | SH |

## Notes

- **Changing `gc.ttlseconds`**: This is a zone configuration, not a cluster setting. Use `ALTER ZONE` to modify it per table, database, or cluster-wide. Lowering it too aggressively while changefeeds are running can cause changefeed failures requiring a full restart.
- **Timeout settings**: The `sql.defaults.*` timeout settings establish defaults for new sessions. Existing sessions are not affected. Application code can override these per-session using `SET` statements.
- **Admission control**: Disabling `admission.enabled` in production is strongly discouraged. It removes the cluster's primary defense against overload-induced cascading failures.
- **`cluster.preserve_downgrade_option`**: This is the single most important setting during upgrades. See the performing-rolling-upgrades skill for the full upgrade procedure.

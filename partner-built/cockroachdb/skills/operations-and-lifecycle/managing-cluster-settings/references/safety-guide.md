# Cluster Settings Safety Guide

## Risk Assessment by Setting Category

### Low Risk

These settings can generally be changed without service impact. They are safe to modify during normal operations.

| Category | Examples | Impact of Misconfiguration |
|---|---|---|
| Telemetry and diagnostics | `diagnostics.reporting.enabled`, `sql.defaults.cost_scans_with_default_col_size` | No impact on data integrity or availability. May affect support experience or optimizer behavior slightly. |
| Logging and tracing | `sql.log.slow_query.latency_threshold`, `sql.trace.txn.enable_threshold` | Over-logging may increase disk I/O and storage consumption. Under-logging may reduce observability. |
| SQL defaults (with session overrides) | `sql.defaults.distsql`, `sql.defaults.vectorize` | Individual sessions can override. Cluster-wide default affects only new sessions without explicit SET. |

### Medium Risk

These settings affect performance or operational behavior. Test changes in staging first. Changes are reversible but may cause transient disruptions.

| Category | Examples | Impact of Misconfiguration |
|---|---|---|
| Timeout settings | `sql.defaults.idle_in_transaction_session_timeout`, `sql.defaults.statement_timeout` | Too low: kills legitimate long-running queries. Too high: allows resource-consuming transactions to persist. |
| Snapshot rates | `kv.snapshot_rebalance.max_rate`, `kv.snapshot_recovery.max_rate` | Too high: saturates network and disk I/O. Too low: slows rebalancing and recovery significantly. |
| GC settings | `gc.ttlseconds` (zone config) | Too low: breaks changefeeds, prevents historical reads. Too high: increases storage consumption from retained MVCC revisions. |
| Statistics | `sql.stats.automatic_collection.enabled`, `sql.stats.automatic_collection.min_stale_rows` | Disabling causes optimizer plan degradation over time. Over-aggressive collection increases CPU usage. |

### High Risk

These settings affect cluster availability, data safety, or upgrade integrity. Incorrect values can cause outages or data issues. Change only with full understanding and a rollback plan.

| Category | Examples | Impact of Misconfiguration |
|---|---|---|
| Admission control | `admission.enabled` | Disabling removes overload protection. Cluster may cascade-fail under heavy load. |
| Dead node detection | `server.time_until_store_dead` | Too low: healthy nodes are marked dead during transient partitions, causing unnecessary data movement. Too high: delays recovery after actual failures. |
| Upgrade finalization | `cluster.preserve_downgrade_option` | Clearing prematurely finalizes an upgrade that may need to be rolled back. Setting it after finalization has no effect. |
| Replication | `CONFIGURE ZONE ... num_replicas` | Under-replication risks data loss. Over-replication wastes storage. |
| Rangefeed | `kv.rangefeed.enabled` | Disabling while changefeeds are running causes all changefeeds to fail immediately. |

## Rollback Procedures

### For Cluster Settings (SET CLUSTER SETTING)

Cluster settings can be reverted immediately via SQL:

```sql
-- Revert to default
RESET CLUSTER SETTING <setting_name>;

-- Or set to a specific previous value
SET CLUSTER SETTING <setting_name> = '<previous_value>';
```

**Before changing any setting**, record the current value:

```sql
SHOW CLUSTER SETTING <setting_name>;
```

### For Zone Configurations

```sql
-- Revert a table's zone config to inherit from database/cluster default
ALTER TABLE <table_name> CONFIGURE ZONE DISCARD;

-- Revert a database's zone config
ALTER DATABASE <db_name> CONFIGURE ZONE DISCARD;

-- Revert cluster default (reset to system defaults)
ALTER RANGE default CONFIGURE ZONE USING gc.ttlseconds = 90000, num_replicas = 3;
```

### For Node-Level Flags

Node-level flags require a restart to change. Rollback procedure:

1. Drain the node.
2. Stop the process.
3. Revert the start flags to previous values.
4. Restart the node.

Keep a record (e.g., version-controlled systemd unit file or Kubernetes manifest) of all node-level flags.

## Never Change During an Active Upgrade

The following settings must not be modified while a rolling upgrade is in progress (nodes running mixed versions):

| Setting | Why |
|---|---|
| `cluster.preserve_downgrade_option` | Only clear this after ALL nodes are running the new version and cluster health is confirmed. Setting it mid-upgrade is acceptable (it blocks finalization). Clearing it mid-upgrade is dangerous. |
| `admission.enabled` | Upgrades change internal data structures. Removing overload protection during this period increases the risk of cascading failure. |
| `kv.rangefeed.enabled` | Disabling this during an upgrade will break changefeeds and may interfere with internal schema change processing. |
| `server.time_until_store_dead` | During an upgrade, nodes restart and are temporarily unavailable. Lowering this threshold may cause the cluster to unnecessarily redistribute data for nodes that are simply restarting. |
| `gc.ttlseconds` | The upgrade process may rely on historical data access. Do not reduce this during an upgrade. |

**General rule**: During a rolling upgrade, change only the settings required by the upgrade procedure itself. Defer all other setting changes until the upgrade is finalized and the cluster is stable.

## Session Variables vs Cluster Settings

### When to Use Session Variables

Use `SET <variable>` (session-level) when:

- The change applies to a single application or workload.
- Different workloads sharing the cluster need different values.
- You want to test a change before applying it cluster-wide.
- The application manages its own session configuration.

```sql
-- Session-level: affects only this session
SET statement_timeout = '10s';
SET idle_in_transaction_session_timeout = '60s';
SET distsql = 'always';
```

### When to Use Cluster Settings

Use `SET CLUSTER SETTING <setting>` when:

- The change should be the default for all sessions.
- No application explicitly sets the session variable.
- The setting has no session variable equivalent (e.g., `kv.rangefeed.enabled`).
- You want a safety net for sessions that forget to configure themselves.

```sql
-- Cluster-level: affects all new sessions
SET CLUSTER SETTING sql.defaults.statement_timeout = '30s';
SET CLUSTER SETTING sql.defaults.idle_in_transaction_session_timeout = '300s';
```

### Precedence

Session variables always override their corresponding cluster default:

```
Session SET > Cluster SET CLUSTER SETTING sql.defaults.* > Built-in Default
```

If a session explicitly runs `SET statement_timeout = '60s'`, the cluster setting `sql.defaults.statement_timeout` has no effect for that session.

### Recommendation

Set cluster defaults as a safety baseline, and allow applications to override per-session as needed. This ensures that all sessions have reasonable limits even if the application neglects to configure them.

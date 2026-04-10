# Cloud-Restricted Cluster Settings

On CockroachDB Cloud, certain cluster settings are restricted because the underlying infrastructure, security, and upgrade lifecycle are managed by Cockroach Labs. The level of restriction varies by tier.

## Tier Access Hierarchy

```
Self-Hosted  >  Advanced/BYOC  >  Standard  >  Basic
(full access)   (most settings)   (limited)    (minimal)
```

- **Self-Hosted**: Full access to all cluster settings and node-level flags.
- **Advanced / BYOC**: Access to most application-relevant settings. Infrastructure and security settings are managed by Cockroach Labs.
- **Standard**: Access to a curated subset of settings relevant to workload tuning.
- **Basic**: Minimal access. Most settings are fully managed.

## Restricted Setting Categories

### Infrastructure Settings (Managed by Cockroach Labs)

These settings control storage, replication, and node behavior. They are tuned by Cockroach Labs SRE teams based on the cluster's provisioned resources and tier.

| Setting | Why Restricted |
|---|---|
| `kv.snapshot_rebalance.max_rate` | Rebalancing rate is managed to prevent resource contention on shared or provisioned infrastructure. |
| `kv.snapshot_recovery.max_rate` | Recovery rate is managed to ensure consistent performance during node replacement. |
| `server.time_until_store_dead` | Dead node detection and replacement is automated by the Cloud control plane. |
| `kv.range_split.by_load_enabled` | Load-based splitting is managed as part of infrastructure auto-tuning. |
| `kv.range_merge.queue_enabled` | Range merging is managed alongside splitting for optimal range sizes. |
| `--cache` | Node memory allocation is provisioned based on selected machine type. |
| `--max-sql-memory` | Node memory allocation is provisioned based on selected machine type. |
| `--store` | Storage is provisioned and managed by the Cloud platform. |
| `--locality` | Locality topology is configured automatically based on selected regions and zones. |

### Security Settings (Managed by Cockroach Labs)

These settings control authentication, encryption, and network security. On Cloud, these are managed through the Cloud Console or API, not via SQL.

| Setting | Why Restricted |
|---|---|
| `server.user_login.password_encryption` | Encryption method is enforced by the platform (scram-sha-256). |
| `server.host_based_authentication.configuration` | Network-level access is managed via Cloud Console IP allowlisting. |
| `server.auth_log.sql_connections.enabled` | Audit logging is configured at the platform level. |
| `server.auth_log.sql_sessions.enabled` | Audit logging is configured at the platform level. |
| Certificate management (all `--certs-dir` related) | TLS certificates are fully managed, automatically rotated, and never exposed to users. |
| `cluster.organization` | Set automatically based on the Cloud organization. |
| `enterprise.license` | Enterprise license is managed automatically by the Cloud platform. |

### Upgrade Settings (Managed via Cloud Console)

Upgrade lifecycle is orchestrated through the Cloud Console, not via cluster settings.

| Setting | Why Restricted |
|---|---|
| `cluster.preserve_downgrade_option` | Upgrades are initiated and finalized through the Cloud Console. Users may have the option to delay finalization in some tiers but cannot set this setting directly. |
| `version` | Version upgrades are managed through the Cloud Console upgrade workflow. |
| `diagnostics.reporting.enabled` | Telemetry is required for Cloud SLA monitoring and proactive support. |

## What You CAN Change on Cloud

Even on managed tiers, you typically retain control over workload-tuning settings:

| Setting | Available On |
|---|---|
| `sql.defaults.idle_in_transaction_session_timeout` | Standard, Advanced, BYOC |
| `sql.defaults.statement_timeout` | Standard, Advanced, BYOC |
| `sql.stats.automatic_collection.enabled` | Standard, Advanced, BYOC |
| `kv.rangefeed.enabled` | Standard, Advanced, BYOC |
| `sql.defaults.distsql` | Advanced, BYOC |
| `sql.defaults.default_int_size` | Advanced, BYOC |
| `sql.defaults.serial_normalization` | Advanced, BYOC |
| `gc.ttlseconds` (zone config) | Standard, Advanced, BYOC |
| `sql.log.slow_query.latency_threshold` | Advanced, BYOC |

## Checking Available Settings

To see which settings you can modify on your Cloud cluster, run:

```sql
SHOW CLUSTER SETTINGS;
```

Settings that are restricted will either not appear in the output or will return a permission error when you attempt to change them with `SET CLUSTER SETTING`.

## Requesting Changes to Restricted Settings

If you need a restricted setting changed on a Cloud cluster:

1. **Advanced / BYOC**: File a support ticket with Cockroach Labs. Many infrastructure settings can be adjusted by the SRE team on request with justification.
2. **Standard**: Some restricted settings may be adjustable via support request. Others are fixed for the tier.
3. **Basic**: Most settings are fixed and cannot be changed even via support.

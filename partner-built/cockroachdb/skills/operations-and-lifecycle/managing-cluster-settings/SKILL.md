---
name: managing-cluster-settings
description: Reviews, audits, and modifies CockroachDB cluster settings. Self-Hosted has full control over all settings and start flags. Advanced/BYOC can modify most SQL-level settings but infrastructure settings are managed by CRL. Standard has limited settings access — session variables are the primary tuning mechanism. Basic has minimal settings — use session variables and Cloud Console. Use when auditing configuration, tuning performance, or troubleshooting settings-related issues.
compatibility: Self-Hosted has full control with admin role. Advanced/BYOC can modify most settings. Standard has limited SET CLUSTER SETTING access. Basic has minimal access. All tiers support SHOW CLUSTER SETTING for visible settings.
metadata:
  author: cockroachdb
  version: "2.0"
---

# Managing Cluster Settings

Reviews, audits, and modifies CockroachDB cluster settings. Before providing procedures, this skill gathers context to determine which settings are available and which modification approach to recommend for the operator's tier.

## When to Use This Skill

- Auditing cluster configuration for production readiness
- Identifying settings that deviate from defaults
- Tuning performance, replication, or admission control
- Verifying settings after an upgrade or incident
- Understanding which settings are modifiable on your tier
- Managing enterprise license installation and renewal (Self-Hosted)

**For version management:** Use [upgrading-cluster-version](../upgrading-cluster-version/SKILL.md) — do not change settings during an upgrade.
**For health checks:** Use [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md).

---

## Step 1: Gather Context

### Required Context

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Deployment tier?** | Self-Hosted, Advanced, BYOC, Standard, Basic | Determines which settings are viewable and modifiable |
| **Goal?** | Audit/review, Tune performance, Fix specific issue, Post-upgrade verification | Directs which queries and procedures to use |

### Additional Context (by tier)

**If Self-Hosted:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **SQL access level?** | admin, MODIFYCLUSTERSETTING, VIEWCLUSTERSETTING | Determines available operations |
| **Specific setting or area?** | e.g., "timeout", "replication", "gc" | Narrows search to relevant settings |
| **Currently mid-upgrade?** | Yes, No | Settings must NOT be changed during rolling upgrades |

**If Advanced or BYOC:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **SQL access level?** | admin, limited | Determines available operations |
| **Specific setting or area?** | e.g., "timeout", "rangefeed" | Narrows search |

**If Standard or Basic:** No additional context needed — settings access is limited. Session variables are the primary tuning mechanism.

### Context-Driven Routing

| Tier | Settings Access | Go To |
|------|----------------|-------|
| Self-Hosted | Full | [Self-Hosted Settings](#self-hosted-settings) |
| Advanced / BYOC | Most (some restricted) | [Advanced / BYOC Settings](#advanced--byoc-settings) |
| Standard | Limited | [Standard Settings](#standard-settings) |
| Basic | Minimal | [Basic Settings](#basic-settings) |

---

## Audit Queries (All Tiers)

These read-only queries work on Self-Hosted and Advanced/BYOC. Standard and Basic may have restricted visibility — see tier-specific sections below.

### Non-Default Settings

```sql
SELECT variable, value, setting_type, description
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE value != default_value ORDER BY variable;
```

### Production-Critical Settings

```sql
SELECT variable, value FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable IN (
  'kv.rangefeed.enabled', 'sql.stats.automatic_collection.enabled',
  'server.time_until_store_dead', 'admission.kv.enabled',
  'gc.ttlseconds', 'cluster.preserve_downgrade_option',
  'sql.defaults.idle_in_transaction_session_timeout'
) ORDER BY variable;
```

### Search by Keyword

```sql
SELECT variable, value, description FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable LIKE '%<keyword>%' OR description LIKE '%<keyword>%'
ORDER BY variable;
```

See [sql-queries reference](references/sql-queries.md) for additional audit queries.
See [recommended-values reference](references/recommended-values.md) for production-recommended settings.

---

## Self-Hosted Settings

**Applies when:** Tier = Self-Hosted

Full control over all cluster settings and node-level start flags.

### Modify a Setting

```sql
SHOW CLUSTER SETTING <name>;          -- Document current value first
SET CLUSTER SETTING <name> = <value>; -- Apply
SHOW CLUSTER SETTING <name>;          -- Verify
```

### Reset to Default

```sql
RESET CLUSTER SETTING <name>;
```

### Node-Level Settings (require node restart)

Node-level settings are `cockroach start` flags and cannot be changed at runtime. To change: drain the node, stop the process, update flags, restart. See [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md).

See [node-level-settings reference](references/node-level-settings.md) for the complete list of start flags.

### License Management

CockroachDB Self-Hosted requires an enterprise license for features like backup/restore, changefeeds, encryption at rest, and multi-region capabilities. The license is stored as a cluster setting.

**Check current license:**
```sql
SHOW CLUSTER SETTING cluster.organization;
SHOW CLUSTER SETTING enterprise.license;
```

**Install or renew a license:**
```sql
SET CLUSTER SETTING cluster.organization = '<organization-name>';
SET CLUSTER SETTING enterprise.license = '<license-key>';
```

**Verify license is active:**
```sql
SELECT * FROM [SHOW CLUSTER SETTING enterprise.license];
```

**License expiry:** Expired licenses do not cause data loss or cluster unavailability. Enterprise features (backups, CDC, EAR) stop working until renewed. Core features remain available. Monitor license expiry proactively.

**CockroachDB Core (free):** If running without an enterprise license, no license management is needed. Core features are always available.

---

## Advanced / BYOC Settings

**Applies when:** Tier = Advanced or BYOC

Most SQL-level cluster settings are modifiable. Infrastructure-level settings are managed by Cockroach Labs.

### Modifiable (common examples)

```sql
SET CLUSTER SETTING sql.defaults.idle_in_transaction_session_timeout = '300s';
SET CLUSTER SETTING sql.defaults.statement_timeout = '30s';
SET CLUSTER SETTING kv.rangefeed.enabled = true;
-- gc.ttlseconds is a zone configuration parameter, not a cluster setting
ALTER RANGE default CONFIGURE ZONE USING gc.ttlseconds = 86400;
```

### Restricted (managed by CRL)

Settings managed by Cockroach Labs that cannot be modified:
- `server.time_until_store_dead`
- `kv.snapshot_rebalance.max_rate`
- `cluster.preserve_downgrade_option` (use Cloud Console for upgrades)
- Node-level flags (`--cache`, `--max-sql-memory`) — managed by CRL

If a modification is rejected, the error will indicate the setting is managed by CockroachDB Cloud. Use Cloud Console or contact support.

**License:** Enterprise license is managed automatically by Cockroach Labs on Advanced/BYOC. No customer action needed.

See [cloud-restricted-settings reference](references/cloud-restricted-settings.md) for the full list.

---

## Standard Settings

**Applies when:** Tier = Standard

Standard is a multi-tenant managed service. Most cluster settings are not modifiable because changes could affect other tenants. Use **session variables** as the primary tuning mechanism.

### Session Variables (recommended approach)

```sql
-- Per-session
SET statement_timeout = '30s';

-- Default for all sessions (preferred over sql.defaults.*)
ALTER ROLE ALL SET statement_timeout = '30s';
ALTER ROLE ALL SET idle_in_transaction_session_timeout = '300s';
```

### What You Can Configure

- Session-level timeouts and defaults via `SET` and `ALTER ROLE`
- SQL-level behavior through session variables

### What Is Managed by CRL

- All infrastructure settings (replication, admission control, storage)
- Compute and networking — configured via Cloud Console

**Note:** `SHOW ALL CLUSTER SETTINGS` may return a limited set of settings on Standard.

---

## Basic Settings

**Applies when:** Tier = Basic

Basic is a serverless offering with minimal settings access. Infrastructure is fully managed and auto-scales. Use session variables for SQL-level tuning.

### Session Variables

```sql
SET statement_timeout = '30s';
ALTER ROLE ALL SET statement_timeout = '30s';
```

### Cloud Console Configuration

- Spending limits
- IP allowlists
- Region selection

All other configuration is managed by Cockroach Labs. If more control over settings is needed, consider upgrading to Standard or Advanced.

---

## Safety Considerations

**Read-only queries are safe on all tiers.**

**Before modifying any setting:**
1. Document the current value (for rollback)
2. Verify you are NOT mid-upgrade
3. Understand the impact (check `description` field)
4. Change one setting at a time
5. Monitor for 15-30 minutes before making additional changes

**Risk levels:**
- **Low:** `sql.defaults.statement_timeout`, `diagnostics.reporting.enabled`
- **Medium:** `gc.ttlseconds`, `kv.snapshot_rebalance.max_rate`
- **High:** `cluster.preserve_downgrade_option`, `admission.kv.enabled`

**Critical:** Never change settings during a rolling upgrade. Cluster settings affect ALL workloads on the cluster — prefer session variables for narrower scope when possible.

See [safety-guide reference](references/safety-guide.md) for detailed risk assessments per setting.

## Troubleshooting

| Issue | Tier | Fix |
|-------|------|-----|
| "permission denied" on SET | SH/ADV/BYOC | Grant MODIFYCLUSTERSETTING or use admin role |
| "managed by Cloud" error | ADV/BYOC | Setting restricted on this tier; use Cloud Console or contact support |
| Setting not visible | STD/BAS | Expected — limited settings visibility on multi-tenant/serverless tiers |
| No visible effect | SH/ADV/BYOC | Check for session variable override; verify with SHOW |
| Setting reverted after upgrade | SH | Re-apply; document in operational runbook |
| Enterprise features stopped working | SH | License expired; renew with SET CLUSTER SETTING enterprise.license |
| "enterprise license required" error | SH | Install license or use core-only alternative |

## References

**Skill references:**
- [SQL audit queries](references/sql-queries.md)
- [Recommended production values](references/recommended-values.md)
- [Node-level settings (start flags)](references/node-level-settings.md)
- [Cloud-restricted settings](references/cloud-restricted-settings.md)
- [Safety guide](references/safety-guide.md)

**Related skills:**
- [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md)
- [upgrading-cluster-version](../upgrading-cluster-version/SKILL.md)

**Official CockroachDB Documentation:**
- [Cluster Settings](https://www.cockroachlabs.com/docs/stable/cluster-settings)
- [SET CLUSTER SETTING](https://www.cockroachlabs.com/docs/stable/set-cluster-setting)
- [Production Checklist](https://www.cockroachlabs.com/docs/stable/recommended-production-settings)

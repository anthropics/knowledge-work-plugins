---
name: upgrading-cluster-version
description: Guides CockroachDB version upgrades with tier-appropriate procedures. Self-Hosted covers manual rolling binary replacement with finalization control. Advanced/BYOC covers Console-initiated major upgrades, maintenance windows for patches, and release channel selection. Standard and Basic upgrades are fully automatic with no customer action required. Use when planning, executing, or monitoring a version upgrade.
compatibility: Self-Hosted requires CLI and SQL access with admin role. Advanced/BYOC requires Cloud Console with Cluster Admin role. Standard/Basic upgrades are automatic — SQL access needed only for post-upgrade verification.
metadata:
  author: cockroachdb
  version: "2.0"
---

# Upgrading Cluster Version

Guides CockroachDB version upgrades end-to-end. Before providing procedures, this skill gathers deployment context to deliver only the steps relevant to the operator's tier.

## When to Use This Skill

- Planning or executing a version upgrade (Self-Hosted)
- Initiating a major version upgrade via Cloud Console (Advanced, BYOC)
- Configuring how patches are applied (Advanced, BYOC)
- Verifying upgrade completion (all tiers)
- Deciding whether to finalize or roll back (Self-Hosted)

**For pre-upgrade health check:** Use [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md).
**For node drain during Self-Hosted upgrade:** Use [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md).
**For maintenance window configuration:** Use [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md).

---

## Step 1: Gather Context

### Required Context

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Deployment tier?** | Self-Hosted, Advanced, BYOC, Standard, Basic | Completely different upgrade procedures per tier |
| **Current version?** | e.g., v24.2.5 | Validates upgrade path and compatibility |

### Additional Context (by tier)

**If Self-Hosted:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Upgrade type?** | Major (e.g., 24.2→24.3), Patch (e.g., 24.2.5→24.2.8) | Major requires finalization; patches do not |
| **Target version?** | e.g., v24.3.1 | Confirms version is available and sequential |
| **Deployment platform?** | Bare metal, VMs, Kubernetes (Operator/Helm/manual) | Changes binary replacement and restart procedure |
| **Process manager?** | systemd, manual, container orchestrator | Changes stop/start commands |
| **Node count?** | Number | Affects upgrade sequencing |

**If Advanced or BYOC:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Upgrade type?** | Major version, Patch | Major requires Console initiation; patches use maintenance windows |
| **Cloud provider?** (BYOC only) | AWS, GCP, Azure | For infrastructure-level monitoring during upgrade |
| **Release channel?** | Regular, Innovation | Innovation gives latest features, shorter support window |

**If Standard or Basic:** No additional context needed — upgrades are fully automatic.

### Context-Driven Routing

| Tier | Go To |
|------|-------|
| Self-Hosted | [Self-Hosted Upgrade](#self-hosted-upgrade) |
| Advanced | [Advanced Upgrade](#advanced-upgrade) |
| BYOC | [BYOC Upgrade](#byoc-upgrade) |
| Standard | [Standard Upgrade](#standard-upgrade) |
| Basic | [Basic Upgrade](#basic-upgrade) |

---

## Self-Hosted Upgrade

**Applies when:** Tier = Self-Hosted

### Major vs Patch

| Aspect | Major (e.g., 24.2→24.3) | Patch (e.g., 24.2.5→24.2.8) |
|--------|--------------------------|------------------------------|
| Finalization required | Yes | No |
| Rollback possible | Before finalization | Always (binary swap) |
| Auto-finalization | Enabled by default (disable recommended) | N/A |

### Pre-Upgrade Validation

```sql
-- All nodes live
SELECT n.node_id, n.build_tag, n.is_live
FROM crdb_internal.gossip_nodes n ORDER BY n.node_id;

-- No bulk operations running
WITH j AS (SHOW JOBS)
SELECT job_id, job_type, status, now() - created AS running_for FROM j
WHERE status IN ('running', 'paused')
  AND job_type IN ('SCHEMA CHANGE', 'BACKUP', 'RESTORE', 'IMPORT', 'NEW SCHEMA CHANGE');

-- No pending finalization from a previous upgrade
SHOW CLUSTER SETTING cluster.preserve_downgrade_option;

-- Ranges fully replicated
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;
```

### Disable Auto-Finalization (Major Version — Recommended)

```sql
SET CLUSTER SETTING cluster.preserve_downgrade_option = '<current_version>';
-- Example: SET CLUSTER SETTING cluster.preserve_downgrade_option = '24.2';
```

### Rolling Node Upgrade (repeat for each node)

**If process manager = systemd:**
```bash
cockroach node drain --self --certs-dir=<certs-dir> --host=<node-address>
sudo systemctl stop cockroachdb
cp /path/to/new/cockroach /usr/local/bin/cockroach
cockroach version  # verify new binary
sudo systemctl start cockroachdb
```

**If Kubernetes (Operator):**
```bash
kubectl patch crdbcluster <name> --type merge -p '{"spec":{"cockroachDBVersion":"<new-version>"}}'
# Operator handles rolling restart automatically
```

**If Kubernetes (Helm):**
```bash
helm upgrade cockroachdb cockroachdb/cockroachdb --set image.tag=<new-version>
```

**If Kubernetes (manual StatefulSet):**
```bash
kubectl set image statefulset/cockroachdb cockroachdb=cockroachdb/cockroach:<new-version>
```

**Verify each node before proceeding to the next:**
```sql
SELECT node_id, build_tag, is_live
FROM crdb_internal.gossip_nodes
WHERE node_id = <upgraded-node-id>;
```

### Monitor Progress

```sql
SELECT n.node_id, n.build_tag AS version,
  CASE WHEN n.build_tag = (SELECT MAX(build_tag) FROM crdb_internal.gossip_nodes)
       THEN 'UPGRADED' ELSE 'PENDING' END AS status
FROM crdb_internal.gossip_nodes n ORDER BY n.node_id;
```

### Finalize (Major Version Only — Irreversible)

```sql
SELECT COUNT(DISTINCT build_tag) FROM crdb_internal.gossip_nodes;  -- Must be 1
RESET CLUSTER SETTING cluster.preserve_downgrade_option;
SHOW CLUSTER SETTING version;  -- Monitor until updated
```

### Roll Back (Before Finalization Only)

Verify `cluster.preserve_downgrade_option` still returns the old version, then replace each node's binary with the previous version and restart. After all nodes are back:
```sql
RESET CLUSTER SETTING cluster.preserve_downgrade_option;
```

---

## Advanced Upgrade

**Applies when:** Tier = Advanced

Advanced clusters are managed by Cockroach Labs. You initiate major upgrades; patches are applied automatically.

### Major Version Upgrade

1. **Cloud Console → Cluster → Settings → Upgrade**
2. Select target version
3. CRL performs rolling upgrade across nodes automatically
4. Monitor progress in Cloud Console
5. Finalize via Cloud Console when testing is complete

**SQL verification during upgrade:**
```sql
SELECT build_tag AS version, COUNT(*) FROM crdb_internal.gossip_nodes GROUP BY 1;
```

### Patch Upgrades

Patches are applied automatically during the configured maintenance window. See [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md) for maintenance window configuration and patch deferral.

### Release Channel

- **Regular:** Stability-focused, longer support windows
- **Innovation:** Latest features, shorter support, can be skipped

Configure via Cloud Console → Cluster → Settings → Upgrades.

### Upgrade Before End of Support

You are responsible for initiating major upgrades before the current version reaches End of Support (EOS). Failure to upgrade before EOS may affect SLA guarantees.

### Cloud API

```bash
# Check current version
curl -s -H "Authorization: Bearer $COCKROACH_API_KEY" \
  "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>" | jq '.cockroach_version'
```

---

## BYOC Upgrade

**Applies when:** Tier = BYOC

BYOC upgrade procedures are the same as Advanced. Follow all [Advanced Upgrade](#advanced-upgrade) steps.

### Cloud Provider Monitoring During Upgrade

Since BYOC clusters run in your cloud account, you can observe the rolling upgrade in your infrastructure:

**If AWS:** EC2 console shows instance restarts; CloudWatch metrics show brief dips during node cycling.

**If GCP:** Compute Engine console shows VM restarts; Cloud Monitoring shows instance-level events.

**If Azure:** Azure portal shows VM restarts; Azure Monitor captures instance events.

### Additional BYOC Considerations

- Verify PrivateLink/PSC/VPC Peering connections remain healthy during the upgrade
- Reserved instances and committed use discounts are unaffected (instance types don't change)

---

## Standard Upgrade

**Applies when:** Tier = Standard

Standard is a multi-tenant managed service. There are no nodes or infrastructure for you to manage. All upgrades — both major versions and patches — are applied automatically by Cockroach Labs.

- Only Regular releases (no Innovation channel)
- No maintenance window configuration
- No deferral capability
- No downtime during upgrades

### After an Upgrade

1. Monitor Cloud Console for upgrade notifications
2. Review release notes for behavior changes
3. Verify application compatibility:
   ```sql
   SELECT version();
   ```

---

## Basic Upgrade

**Applies when:** Tier = Basic

Basic is a serverless offering. All upgrades are fully managed and transparent. The serverless architecture is designed for zero-downtime upgrades with no customer action required.

### After an Upgrade

1. Review release notes for behavior changes
2. Verify version if needed: `SELECT version();`

---

## Safety Considerations

| Operation | Tier | Reversible? |
|-----------|------|-------------|
| Set preserve_downgrade_option | SH | Yes |
| Replace node binary | SH | Yes (swap back before finalization) |
| Finalize upgrade | SH | **No — irreversible** |
| Initiate Cloud Console upgrade | ADV/BYOC | Contact support to discuss |
| Automatic upgrade | STD/BAS | N/A (managed by CRL) |

**Critical:**
- Never skip major versions (SH) — upgrades must be sequential
- Never finalize before testing (SH) — finalization is irreversible
- Never change cluster settings during an upgrade (SH, ADV, BYOC)

## Troubleshooting

| Issue | Tier | Fix |
|-------|------|-----|
| Cannot set preserve_downgrade_option | SH | Value must match output of `SHOW CLUSTER SETTING version` |
| Finalization stuck | SH | Decommission dead nodes; ensure all live nodes are upgraded |
| Auto-finalization triggered early | SH | Cannot undo; test application on new version |
| Upgrade not available in Console | ADV/BYOC | Check release schedule; contact support |
| Behavior change after automatic upgrade | STD/BAS | Review release notes; contact support |

## References

**Related skills:**
- [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md) — Pre/post-upgrade health
- [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md) — Node drain (SH) and maintenance windows (ADV/BYOC)
- [managing-cluster-settings](../managing-cluster-settings/SKILL.md) — preserve_downgrade_option

**Official CockroachDB Documentation:**
- [Upgrade Self-Hosted](https://www.cockroachlabs.com/docs/stable/upgrade-cockroach-version)
- [Upgrade Cloud Cluster](https://www.cockroachlabs.com/docs/cockroachcloud/upgrade-cockroach-version)
- [Cloud Upgrade Policy](https://www.cockroachlabs.com/docs/cockroachcloud/upgrade-policy)
- [Upgrade on Kubernetes](https://www.cockroachlabs.com/docs/stable/upgrade-cockroachdb-kubernetes)

---
name: performing-cluster-maintenance
description: Manages planned cluster maintenance across all tiers. Self-Hosted covers node drain procedures for OS patching, hardware changes, and configuration updates. Advanced/BYOC covers maintenance window configuration, patch scheduling, deferral policies, and monitoring during CRL-managed maintenance. Standard and Basic maintenance is fully managed with no customer action. Use when planning maintenance, configuring maintenance windows, or preparing applications for maintenance events.
compatibility: Self-Hosted requires CLI access and SQL access. Advanced/BYOC requires Cloud Console with Cluster Admin role. Standard and Basic maintenance is fully managed.
metadata:
  author: cockroachdb
  version: "2.0"
---

# Performing Cluster Maintenance

Manages planned cluster maintenance across all deployment tiers. For Self-Hosted, this means draining and restarting individual nodes. For Advanced/BYOC, this means configuring and managing maintenance windows for CRL-applied patches. For Standard and Basic, maintenance is fully managed with no customer action required.

## When to Use This Skill

- Planning OS patching, hardware changes, or configuration updates (Self-Hosted)
- Configuring or modifying a maintenance window (Advanced, BYOC)
- Setting patch deferral policies (Advanced, BYOC)
- Monitoring during a CRL-managed maintenance event (Advanced, BYOC)
- Running pre-maintenance validation checks (Self-Hosted, Advanced, BYOC)
- Understanding how maintenance affects your application (all tiers)
- Preparing applications for maintenance events (all tiers)

**For permanent node removal:** Use [managing-cluster-capacity](../managing-cluster-capacity/SKILL.md).
**For pre-maintenance health check:** Use [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md).
**For version upgrades:** Use [upgrading-cluster-version](../upgrading-cluster-version/SKILL.md).

---

## Step 1: Gather Context

### Required Context

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Deployment tier?** | Self-Hosted, Advanced, BYOC, Standard, Basic | Determines maintenance procedure |
| **Goal?** | Plan maintenance, Configure maintenance window, Defer a patch, Monitor during maintenance, Prepare application | Routes to the right procedure |

### Additional Context (by tier)

**If Self-Hosted:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Maintenance type?** | OS patching, Hardware change, Binary upgrade, Config change, Planned restart | Affects sequencing and post-maintenance steps |
| **Deployment platform?** | Bare metal, VMs, Kubernetes (Operator/Helm/manual) | Changes drain and restart commands |
| **Process manager?** | systemd, manual, container orchestrator | Changes stop/start commands |
| **Target node ID?** | Node ID | Required for drain command |
| **Long-running queries expected?** | Yes (increase drain timeout), No (default timeout) | Determines drain-wait parameter |

**If Advanced or BYOC:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Maintenance window configured?** | Yes (what schedule), No | Determines if window needs setup |
| **Patch pending?** | Yes, No, Don't know | Determines urgency |
| **Cloud provider?** (BYOC only) | AWS, GCP, Azure | For infrastructure-level monitoring |

**If Standard or Basic:** No context needed — maintenance is fully managed.

### Context-Driven Routing

| Tier | Go To |
|------|-------|
| Self-Hosted | [Self-Hosted Node Maintenance](#self-hosted-node-maintenance) |
| Advanced | [Advanced Maintenance Management](#advanced-maintenance-management) |
| BYOC | [BYOC Maintenance Management](#byoc-maintenance-management) |
| Standard | [Standard Maintenance](#standard-maintenance) |
| Basic | [Basic Maintenance](#basic-maintenance) |

---

## Self-Hosted Node Maintenance

**Applies when:** Tier = Self-Hosted

Self-Hosted operators manage all maintenance directly. The core operation is draining a node to safely move leases and connections before stopping it.

### Pre-Maintenance Checks

Run all checks before any maintenance operation. **Stop if any check fails.**

```sql
-- Check 1: All nodes live (STOP if any node is not live)
SELECT n.node_id, n.is_live
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id) ORDER BY n.node_id;

-- Check 2: No other nodes currently draining (STOP if any draining)
SELECT node_id FROM crdb_internal.gossip_liveness WHERE draining = true;

-- Check 3: Ranges fully replicated (STOP if under-replicated ranges exist)
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;

-- Check 4: No disruptive jobs running (WAIT or pause before proceeding)
WITH j AS (SHOW JOBS)
SELECT job_id, job_type, status, now() - created AS running_for FROM j
WHERE status IN ('running', 'paused')
  AND job_type IN ('SCHEMA CHANGE', 'BACKUP', 'RESTORE', 'IMPORT', 'NEW SCHEMA CHANGE');

-- Check 5: Not mid-upgrade (STOP if versions differ)
SELECT DISTINCT build_tag FROM crdb_internal.gossip_nodes;

-- Check 6: Storage utilization safe (WARNING if any node > 70%)
SELECT node_id,
  ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

**Stop conditions:** Do not proceed with maintenance if any node is not live, ranges are under-replicated, another node is draining, or a rolling upgrade is in progress. Wait for running jobs to complete or pause them.

See [maintenance-prechecks reference](references/maintenance-prechecks.md) for a consolidated precheck script.

### Execute Drain

**If platform = bare metal or VMs:**
```bash
cockroach node drain --self --certs-dir=<certs-dir> --host=<node-address>
```

**If long-running queries expected:**
```bash
cockroach node drain --self --certs-dir=<certs-dir> --host=<node-address> --drain-wait=60s
```

**If platform = Kubernetes:**
```bash
# Operator handles drain automatically during pod eviction
kubectl delete pod <pod-name>
# Or for rolling restart:
kubectl rollout restart statefulset cockroachdb
```

### Stop, Maintain, Restart

**If process manager = systemd:**
```bash
sudo systemctl stop cockroachdb
# ... perform maintenance ...
sudo systemctl start cockroachdb
```

**If process manager = manual:**
```bash
kill -TERM $(pgrep -f 'cockroach start')
# ... perform maintenance ...
cockroach start --certs-dir=<certs-dir> --store=<path> --join=<addresses> --background
```

Never use `kill -9` unless the process is unresponsive to SIGTERM.

### Post-Restart Verification

```sql
SELECT node_id, is_live FROM crdb_internal.gossip_nodes WHERE node_id = <node_id>;
-- is_live = true

SELECT node_id, lease_count FROM crdb_internal.kv_store_status WHERE node_id = <node_id>;
-- lease_count should increase over minutes as leases rebalance
```

See [drain-details reference](references/drain-details.md) for drain phases, timeout configuration, and advanced monitoring.

### Storage Maintenance

Periodic storage maintenance for Self-Hosted clusters:

**Ballast file verification:**
```bash
ls -lh <store-path>/auxiliary/EMERGENCY_BALLAST
# If missing, create: cockroach debug ballast <store-path>/auxiliary/EMERGENCY_BALLAST --size=1GiB
```

**Disk utilization check:**
```sql
SELECT node_id,
  ROUND(capacity / 1073741824.0, 2) AS total_gb,
  ROUND(available / 1073741824.0, 2) AS available_gb,
  ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

Nodes above 70% utilization should be addressed before maintenance — draining a node temporarily increases load on remaining nodes.

---

## Advanced Maintenance Management

**Applies when:** Tier = Advanced

Advanced clusters are managed by Cockroach Labs. CRL applies patches and performs infrastructure maintenance during the configured maintenance window. You do not drain or restart nodes — CRL handles this using rolling restarts.

### Configure a Maintenance Window

1. **Cloud Console → Cluster → Settings → Maintenance**
2. Set a weekly 6-hour window
   - Choose day of week (e.g., Sunday)
   - Choose start time in UTC (e.g., 02:00 UTC)
   - Window duration is 6 hours

If no window is configured, CRL applies patches at a time of their choosing.

### View Current Maintenance Window

**Cloud Console → Cluster → Settings → Maintenance** shows the current schedule.

**Cloud API:**
```bash
curl -s -H "Authorization: Bearer $COCKROACH_API_KEY" \
  "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>" | jq '.maintenance_window'
```

### Defer Patches

If a pending patch needs to be delayed (e.g., for testing):

1. **Cloud Console → Cluster → Settings → Upgrades**
2. Select deferral period: **30, 60, or 90 days**

Deferred patches still apply at the end of the deferral period. Deferral only delays — it does not skip.

### What Happens During Maintenance

1. CRL applies the patch using rolling restarts — one node at a time
2. Each node is drained (connections and leases moved), updated, and restarted
3. Cluster remains available throughout (multi-node clusters)
4. Performance may be slightly degraded during the window due to temporarily reduced capacity

**Single-node clusters** experience downtime during maintenance. Consider scaling to 3+ nodes for production workloads.

### Monitor During Maintenance

**Cloud Console:**
- Cluster Overview shows node status during rolling restarts
- Metrics page shows temporary dips in QPS and capacity
- Alerts may fire for transient node unavailability

**SQL (during maintenance):**
```sql
-- Check which nodes are currently live
SELECT node_id, build_tag, is_live
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id) ORDER BY node_id;
```

### Best Practices

- Schedule during your lowest-traffic period
- Monitor P99 latency during and after the window
- Test patches in a staging cluster before production
- Use deferral to align with your testing and release cadence
- Configure alerting to notify during maintenance windows
- Ensure applications implement connection retry with exponential backoff

---

## BYOC Maintenance Management

**Applies when:** Tier = BYOC

BYOC maintenance follows the same CRL-managed process as Advanced. Follow all [Advanced Maintenance Management](#advanced-maintenance-management) steps for maintenance window configuration, patch deferral, and monitoring.

### Cloud Provider Visibility

Since BYOC clusters run in your cloud account, you can directly observe maintenance operations:

**If AWS:**
- EC2 console shows instance restarts during rolling patches
- CloudWatch metrics show brief dips during node cycling
- Set up CloudWatch Alarms for instance state changes

**If GCP:**
- Compute Engine console shows VM restarts
- Cloud Monitoring shows instance-level events
- Configure alerting policies for instance uptime

**If Azure:**
- Azure portal shows VM cycling
- Azure Monitor captures instance restart events
- Set up Azure Alerts for VM availability

### BYOC Infrastructure Maintenance

For infrastructure changes in your cloud account that CRL does not manage (VPC, security groups, IAM, DNS):

- **Coordinate with CRL** before making changes that could affect the cluster
- **Do not modify** CRL-managed resources (instances, disks, network interfaces)
- Test infrastructure changes in a staging BYOC cluster first
- Changes to networking (PrivateLink, PSC, VPC Peering) may require CRL coordination

---

## Standard Maintenance

**Applies when:** Tier = Standard

Standard is a multi-tenant managed service. There are no nodes, no maintenance windows to configure, and no patches to defer. Cockroach Labs manages all maintenance transparently.

### What to Expect

- Patches are applied during low-traffic periods chosen by CRL
- No downtime during maintenance
- No customer notification required for routine patches
- Major version upgrades are also automatic

### Application Preparation

- Implement connection retry logic with exponential backoff
- Handle brief latency variations gracefully
- Monitor Cloud Console for any service notifications

---

## Basic Maintenance

**Applies when:** Tier = Basic

Basic is a serverless offering. All maintenance is fully managed by Cockroach Labs. The serverless architecture is designed for zero-downtime maintenance.

### What to Expect

- All patches and upgrades are transparent
- No customer action required
- No maintenance notifications needed

### Application Preparation

- Implement connection retry logic (recommended for all production applications)
- Be aware that idle clusters may scale to zero — first reconnection after inactivity may have higher latency (this is not maintenance-related)

---

## Safety Considerations

**Read-only monitoring queries are safe on all tiers.**

**Self-Hosted node maintenance:**
- Only drain one node at a time
- Drain cannot be canceled once started
- Applications must have connection retry logic
- Load balancer detects drained node via `/health?ready=1` returning error
- Never SIGKILL unless process is unresponsive to SIGTERM

**Advanced/BYOC maintenance windows:**
- Single-node clusters experience downtime during maintenance
- Deferring patches too long delays security fixes — evaluate CVE impact
- Do not modify CRL-managed infrastructure during a maintenance window

**Standard/Basic:** No maintenance risk for customers — fully managed by CRL.

See [safety-guide reference](references/safety-guide.md) for detailed risk matrix.

## Troubleshooting

| Issue | Tier | Fix |
|-------|------|-----|
| Drain very slow | SH | Check `SHOW CLUSTER STATEMENTS` for stuck queries |
| Drain hangs | SH | Check logs; SIGTERM if unresponsive |
| Node won't rejoin after restart | SH | Verify --join flag; check network connectivity |
| Leases not returning to node | SH | Wait 5-10 min; monitor lease_count |
| Clients not reconnecting | SH | Verify load balancer health check is passing |
| Maintenance window missed | ADV/BYOC | Contact support |
| Unexpected maintenance outside window | ADV/BYOC | Emergency patches may be applied outside windows; check Cloud Console notifications |
| Latency during maintenance | ADV/BYOC | Expected — temporarily reduced capacity; monitor and verify recovery after window |

## References

**Skill references:**
- [Drain phases and timeouts](references/drain-details.md)
- [Maintenance prechecks](references/maintenance-prechecks.md)
- [Safety guide](references/safety-guide.md)

**Related skills:**
- [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md)
- [managing-cluster-capacity](../managing-cluster-capacity/SKILL.md)
- [upgrading-cluster-version](../upgrading-cluster-version/SKILL.md)

**Official CockroachDB Documentation:**
- [Node Shutdown](https://www.cockroachlabs.com/docs/stable/node-shutdown)
- [cockroach node drain](https://www.cockroachlabs.com/docs/stable/cockroach-node.html)
- [Manage Advanced Cluster](https://www.cockroachlabs.com/docs/cockroachcloud/advanced-cluster-management)
- [Cloud Upgrade Policy](https://www.cockroachlabs.com/docs/cockroachcloud/upgrade-policy)

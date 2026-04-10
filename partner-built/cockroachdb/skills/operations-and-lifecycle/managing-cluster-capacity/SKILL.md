---
name: managing-cluster-capacity
description: Manages CockroachDB cluster capacity across all tiers. Self-Hosted covers node decommissioning for permanent removal and adding nodes for expansion. Advanced/BYOC covers scaling node count and machine size via Cloud Console, API, or Terraform. Standard covers adjusting provisioned compute (vCPUs). Basic auto-scales — guidance covers spending limits and cost management. Use when scaling capacity up or down, permanently removing nodes, or managing costs.
compatibility: Self-Hosted requires CLI access and admin role. Advanced/BYOC requires Cloud Console with Cluster Admin role. Standard requires Cloud Console. Basic has no capacity management — spending limits only.
metadata:
  author: cockroachdb
  version: "2.0"
---

# Managing Cluster Capacity

Manages cluster capacity across all CockroachDB deployment tiers. What "capacity" means varies by tier — Self-Hosted manages individual nodes, Advanced/BYOC manage node count and machine size, Standard manages provisioned vCPUs, and Basic auto-scales with cost controls.

## When to Use This Skill

- Permanently removing a node from a cluster (Self-Hosted)
- Adding nodes to increase capacity (Self-Hosted)
- Scaling cluster node count or machine size (Advanced, BYOC)
- Adjusting provisioned compute (Standard)
- Managing costs on a serverless cluster (Basic)
- Replacing hardware or migrating infrastructure (Self-Hosted, BYOC)
- Replacing a failed or dead node (Self-Hosted)
- Managing storage utilization and disk pressure (Self-Hosted)

**For temporary maintenance (not capacity changes):** Use [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md).
**For pre-operation health check:** Use [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md).

---

## Step 1: Gather Context

### Required Context

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Deployment tier?** | Self-Hosted, Advanced, BYOC, Standard, Basic | Different capacity model per tier |
| **Direction?** | Scale up (add capacity), Scale down (reduce capacity) | Determines procedure |

### Additional Context (by tier)

**If Self-Hosted (scaling down):**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **How many nodes to remove?** | 1, multiple | Multi-node decommission should be done simultaneously |
| **Target node IDs?** | Node IDs from `cockroach node status` | Required for CLI commands |
| **Is the node alive or dead?** | Alive, Dead | Dead nodes use a different procedure |
| **Deployment platform?** | Bare metal, VMs, Kubernetes | Changes CLI and cleanup steps |
| **Current replication factor?** | 3, 5, custom | Must have enough nodes remaining |
| **Current node count?** | Number | Validates remaining capacity |
| **Storage utilization?** | Low (<60%), Medium (60-80%), High (>80%) | Determines urgency and whether storage maintenance is needed |

**If Advanced or BYOC:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Scale method?** | Cloud Console, API, Terraform | Determines procedure |
| **Current and target configuration?** | e.g., 5 nodes → 3 nodes, or 4 vCPU → 8 vCPU | Validates constraints |
| **Cloud provider?** (BYOC only) | AWS, GCP, Azure | Affects infrastructure verification |

**If Standard:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Current provisioned vCPUs?** | Number | Context for scaling decision |
| **Target vCPUs?** | Number | Validates workload will fit |

**If Basic:** Gather cost management goals — Basic auto-scales with no manual capacity control.

### Context-Driven Routing

| Tier | Go To |
|------|-------|
| Self-Hosted | [Self-Hosted Capacity Management](#self-hosted-capacity-management) |
| Advanced | [Advanced Scaling](#advanced-scaling) |
| BYOC | [BYOC Scaling](#byoc-scaling) |
| Standard | [Standard Compute Management](#standard-compute-management) |
| Basic | [Basic Cost Management](#basic-cost-management) |

---

## Self-Hosted Capacity Management

**Applies when:** Tier = Self-Hosted

### Scaling Down: Decommission Nodes

#### Pre-Decommission Validation

```sql
-- All nodes live
SELECT n.node_id, n.is_live, n.build_tag
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id) ORDER BY n.node_id;

-- Ranges fully replicated
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;

-- Remaining capacity check
SELECT node_id, store_id,
  ROUND(capacity / 1073741824.0, 2) AS total_gb,
  ROUND(available / 1073741824.0, 2) AS available_gb,
  ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;

-- Replication factor
SHOW ZONE CONFIGURATION FOR RANGE default;
```

Remaining nodes must stay < 60% utilization after absorbing data. Node count after decommission must be >= replication factor.

#### If Node Is Alive: Drain Then Decommission

```bash
# Step 1: Drain
cockroach node drain <node_id> --certs-dir=<certs-dir> --host=<any-live-node>

# Step 2: Decommission (single node)
cockroach node decommission <node_id> --certs-dir=<certs-dir> --host=<any-live-node>

# Step 2: Decommission (multiple nodes — more efficient, do simultaneously)
cockroach node decommission <id_1> <id_2> <id_3> --certs-dir=<certs-dir> --host=<any-live-node>
```

#### If Node Is Dead: Replace Failed Node

When a node has been dead longer than `server.time_until_store_dead` (default 5m), CockroachDB automatically re-replicates its data to surviving nodes. Use this procedure to clean up the dead node and optionally add a replacement.

**Step 1: Confirm the node is dead and data is safe**

```sql
-- Confirm node is dead
SELECT node_id, is_live FROM crdb_internal.gossip_nodes WHERE node_id = <dead_node_id>;

-- Verify all ranges are fully replicated (no under-replicated after re-replication)
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;

-- Check remaining capacity can handle the load
SELECT node_id, ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

If under-replicated ranges exist, wait for re-replication to complete before proceeding.

**Step 2: Decommission the dead node (metadata cleanup)**

```bash
cockroach node decommission <dead_node_id> --certs-dir=<certs-dir> --host=<any-live-node>
```

**Step 3: Add a replacement node (recommended)**

If remaining nodes are above 60% utilization, provision a replacement node using the [Scaling Up: Add Nodes](#scaling-up-add-nodes) procedure.

**Multiple dead nodes:** Decommission all dead nodes simultaneously:
```bash
cockroach node decommission <id_1> <id_2> --certs-dir=<certs-dir> --host=<any-live-node>
```

See [replacing-failed-nodes reference](references/replacing-failed-nodes.md) for detailed failure scenarios and recovery procedures.

#### Monitor Decommission Progress

```bash
cockroach node status --decommission --certs-dir=<certs-dir> --host=<any-live-node>
```

Wait for `gossiped_replicas = 0` and `membership = 'decommissioned'`. Then stop the process on the decommissioned node.

#### Cancel a Decommission

```bash
cockroach node recommission <node_id> --certs-dir=<certs-dir> --host=<any-live-node>
```

Only works while still in `decommissioning` state.

### Scaling Up: Add Nodes

1. Provision new hardware/VM with same specs as existing nodes
2. Install same CockroachDB version (`cockroach version` to confirm)
3. Start node with `--join` pointing to existing cluster nodes
4. Verify join:
   ```sql
   SELECT node_id, address, is_live FROM crdb_internal.gossip_nodes n
   JOIN crdb_internal.gossip_liveness l USING (node_id) ORDER BY node_id;
   ```
5. Data rebalances automatically — monitor with:
   ```sql
   SELECT node_id, range_count, lease_count
   FROM crdb_internal.kv_store_status ORDER BY node_id;
   ```

### Post-Scaling Verification

```sql
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;

SELECT node_id, range_count, lease_count,
  ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

---

## Advanced Scaling

**Applies when:** Tier = Advanced

Advanced clusters are managed by Cockroach Labs. Capacity is adjusted by changing node count or machine size.

### Via Cloud Console

1. **Cluster → Capacity**
2. Adjust node count or machine type (vCPUs per node)
3. CRL handles all node operations (drain, decommission, provisioning) safely
4. Monitor progress in Cloud Console

### Via Cloud API

```bash
# Scale node count
curl -X PATCH -H "Authorization: Bearer $COCKROACH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"config": {"num_nodes": <new_count>}}' \
  "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>"
```

### Via Terraform

```hcl
resource "cockroach_cluster" "example" {
  dedicated {
    num_virtual_cpus = 8     # vCPUs per node
    storage_gib      = 150
    num_nodes        = 5     # total nodes
  }
}
```

### Pre-Scaling Check

```sql
-- Ensure no disruptive jobs are running before scaling down
WITH j AS (SHOW JOBS)
SELECT job_type, status, COUNT(*) FROM j WHERE status = 'running' GROUP BY 1, 2;
```

### Constraints

- **Minimum:** 3 nodes x 4 vCPUs (12 vCPUs total)
- **Scale down:** Data must fit on remaining nodes; zone configs must be satisfiable
- **Scale up:** Additional nodes available within your plan limits

---

## BYOC Scaling

**Applies when:** Tier = BYOC

Follow all [Advanced Scaling](#advanced-scaling) steps. BYOC scaling is managed through the same Cloud Console/API/Terraform interfaces.

### Cloud Provider Verification (after scaling down)

**If AWS:**
```bash
aws ec2 describe-instances --filters "Name=tag:cockroach-cluster,Values=<cluster-name>" \
  --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name}'
```

**If GCP:**
```bash
gcloud compute instances list --filter="labels.cockroach-cluster=<cluster-name>"
```

**If Azure:**
```bash
az vm list --resource-group <rg> --query "[?tags.cockroachCluster=='<name>']"
```

### Additional BYOC Considerations

- Verify security groups/firewall rules after scaling
- Update reserved instance or committed use discount allocations
- Verify network connectivity (PrivateLink/PSC/VPC Peering) is unaffected
- Check cloud billing reflects the new instance count

---

## Standard Compute Management

**Applies when:** Tier = Standard

Standard is a multi-tenant managed service. There are no individual nodes. Capacity is managed by adjusting provisioned compute (vCPUs).

### Adjust Provisioned vCPUs

1. **Cloud Console → Cluster → Capacity**
2. Increase or decrease provisioned vCPUs
3. Change takes effect without downtime

### Before Scaling Down

- Review CPU utilization in Cloud Console — ensure workload fits within reduced compute
- Storage is usage-based and unaffected by compute changes

### After Scaling

Monitor P99 latency and QPS in Cloud Console for 24-48 hours. If latency increases after scaling down, scale compute back up.

---

## Basic Cost Management

**Applies when:** Tier = Basic

Basic is a serverless offering that auto-scales. There are no nodes or provisioned compute to manage. Capacity scales automatically based on demand. Cost is managed through spending controls.

### Manage Spending

- **Set spending limits:** Cloud Console → Cluster → Settings → configure monthly spending cap
- **Review usage:** Cloud Console shows Request Unit (RU) consumption over time
- **Optimize queries:** Reduce RU consumption through query tuning and indexing
- **Archive data:** Delete unused tables or databases to reduce storage costs

### When to Consider Upgrading

If you need explicit control over compute capacity (guaranteed vCPUs), consider upgrading to Standard. If you need dedicated infrastructure, consider Advanced.

---

## Safety Considerations

| Operation | Tier | Reversible? |
|-----------|------|-------------|
| `cockroach node decommission` | SH | Recommission only before completion |
| Stop decommissioned node | SH | No (must rejoin as new node) |
| Add node to cluster | SH | Yes (decommission to remove) |
| Scale via Console/API | ADV/BYOC | Contact support to reverse |
| Adjust provisioned vCPUs | STD | Yes (scale back) |
| Set spending limit | BAS | Yes (adjust anytime) |

**Critical (Self-Hosted):**
- Never decommission below the replication factor
- Always drain before decommission (for live nodes)
- Decommission multiple nodes simultaneously (not sequentially)
- Verify remaining capacity can absorb the data
- For dead nodes: wait for re-replication to complete before decommissioning
- Monitor storage utilization — nodes above 80% risk performance degradation

## Troubleshooting

| Issue | Tier | Fix |
|-------|------|-----|
| Decommission hangs | SH | Check zone config constraints; investigate stalled ranges |
| Recommission fails | SH | Node already fully decommissioned; must rejoin as new |
| New node not rebalancing | SH | Wait for automatic rebalancing; check `range_count` |
| Scale-down rejected | ADV/BYOC | Below minimum or data won't fit |
| Latency spike after reduction | STD | Scale provisioned vCPUs back up |
| Cloud instances not cleaned up | BYOC | Contact support; verify in cloud console |
| Dead node not re-replicating | SH | Check `server.time_until_store_dead`; verify surviving nodes have capacity |
| Storage utilization high after scale-down | SH | Add replacement node or increase disk size |

## References

**Skill references:**
- [Replacing failed nodes](references/replacing-failed-nodes.md)
- [Storage management](references/storage-management.md)

**Related skills:**
- [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md) — Pre/post health checks
- [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md) — Drain procedure (SH)
- [upgrading-cluster-version](../upgrading-cluster-version/SKILL.md) — Upgrades and lifecycle

**Official CockroachDB Documentation:**
- [cockroach node decommission](https://www.cockroachlabs.com/docs/stable/cockroach-node.html)
- [Node Shutdown](https://www.cockroachlabs.com/docs/stable/node-shutdown)
- [Manage Advanced Cluster](https://www.cockroachlabs.com/docs/cockroachcloud/advanced-cluster-management)
- [Manage Standard Cluster](https://www.cockroachlabs.com/docs/cockroachcloud/cluster-management)
- [Cloud API](https://www.cockroachlabs.com/docs/cockroachcloud/cloud-api)

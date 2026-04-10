# Replacing Failed Nodes

Detailed procedures for replacing failed or dead CockroachDB nodes in Self-Hosted deployments.

## Failure Scenarios

### Single Node Failure (Cluster Remains Healthy)

The most common scenario. CockroachDB automatically re-replicates data from the failed node after `server.time_until_store_dead` (default 5 minutes).

**Timeline:**
1. Node goes down → leases transfer to other nodes (seconds)
2. After 5 minutes → CockroachDB marks node as dead
3. Re-replication begins → replicas move to surviving nodes
4. Re-replication completes → all ranges fully replicated again

**Monitoring re-replication:**
```sql
-- Track under-replicated ranges (should decrease to 0)
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;
```

### Multiple Simultaneous Node Failures

If fewer than a majority of replicas for any range are lost, CockroachDB can recover. With replication factor 3, losing 2 of 3 replicas for any range causes data unavailability.

**Assessment:**
```sql
-- Check if any ranges lost quorum
SELECT range_id, array_length(replicas, 1) AS replica_count
FROM crdb_internal.ranges_no_leases
WHERE array_length(replicas, 1) < 2
LIMIT 10;
```

If ranges lost quorum, see [cockroach debug recover](https://www.cockroachlabs.com/docs/stable/cockroach-debug-recover) for unsafe recovery procedures.

### Node with Corrupted Store

If a node's store is corrupted but the node process is running:

1. Drain the node: `cockroach node drain --self`
2. Stop the process
3. Decommission the node from another node
4. Provision a new node with a fresh store
5. Join the new node to the cluster

## Replacement Procedure

### Step 1: Assess Impact

```sql
-- Current cluster state
SELECT n.node_id, n.is_live, n.build_tag
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id) ORDER BY n.node_id;

-- Utilization on remaining nodes
SELECT node_id,
  ROUND(capacity / 1073741824.0, 2) AS total_gb,
  ROUND(available / 1073741824.0, 2) AS available_gb,
  ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

### Step 2: Wait for Re-Replication

Do not rush. Wait for under-replicated ranges to reach 0. Monitor via DB Console or:

```sql
SELECT COUNT(*) AS under_replicated
FROM crdb_internal.ranges_no_leases
WHERE array_length(replicas, 1) < 3;
```

### Step 3: Decommission Dead Node

```bash
cockroach node decommission <dead_node_id> --certs-dir=<certs-dir> --host=<any-live-node>
```

### Step 4: Provision Replacement

1. Provision new hardware/VM with **same or better specs** as the failed node
2. Install the **same CockroachDB version** as the cluster
3. Use the same `--store` path, `--certs-dir`, and `--join` flags
4. Start the node — it will join automatically and begin receiving data

### Step 5: Verify

```sql
-- New node is live
SELECT node_id, is_live FROM crdb_internal.gossip_nodes ORDER BY node_id;

-- Ranges rebalancing to new node
SELECT node_id, range_count, lease_count
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

## Kubernetes-Specific Recovery

**Operator:** The operator automatically replaces failed pods. If a PV is lost:
```bash
kubectl delete pvc datadir-cockroachdb-<ordinal>
kubectl delete pod cockroachdb-<ordinal>
# Operator recreates both
```

**StatefulSet (manual):** Delete the PVC and pod for the failed node. The StatefulSet controller recreates the pod, and a new PV is provisioned.

## When to Escalate

- Multiple nodes failed simultaneously and ranges lost quorum
- Re-replication stalled for more than 1 hour
- Remaining nodes above 80% storage utilization after absorbing data
- Node repeatedly crashes after restart (check logs for store corruption)

# Maintenance Prechecks

Consolidated pre-maintenance validation for CockroachDB Self-Hosted clusters. Run all checks before any maintenance operation (drain, restart, upgrade, decommission).

## Quick Precheck Script

Run this single query block to get a pass/fail assessment:

```sql
-- === MAINTENANCE PRECHECK REPORT ===

-- 1. Node Health
SELECT 'NODE_HEALTH' AS check,
  CASE WHEN COUNT(*) FILTER (WHERE NOT n.is_live) = 0 THEN 'PASS'
       ELSE 'FAIL: ' || COUNT(*) FILTER (WHERE NOT n.is_live) || ' nodes not live' END AS result
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id);

-- 2. No Draining Nodes
SELECT 'NO_DRAINING' AS check,
  CASE WHEN COUNT(*) = 0 THEN 'PASS'
       ELSE 'FAIL: ' || COUNT(*) || ' nodes draining' END AS result
FROM crdb_internal.gossip_liveness WHERE draining = true;

-- 3. Replication Health
SELECT 'REPLICATION' AS check,
  CASE WHEN COUNT(*) FILTER (WHERE array_length(replicas, 1) < 3) = 0 THEN 'PASS'
       ELSE 'FAIL: ' || COUNT(*) FILTER (WHERE array_length(replicas, 1) < 3) || ' under-replicated ranges' END AS result
FROM crdb_internal.ranges_no_leases;

-- 4. No Disruptive Jobs
WITH j AS (SHOW JOBS)
SELECT 'NO_DISRUPTIVE_JOBS' AS check,
  CASE WHEN COUNT(*) = 0 THEN 'PASS'
       ELSE 'WARN: ' || COUNT(*) || ' jobs running (' || string_agg(DISTINCT job_type, ', ') || ')' END AS result
FROM j
WHERE status = 'running'
  AND job_type IN ('SCHEMA CHANGE', 'BACKUP', 'RESTORE', 'IMPORT', 'NEW SCHEMA CHANGE');

-- 5. Consistent Versions (not mid-upgrade)
SELECT 'VERSION_CONSISTENT' AS check,
  CASE WHEN COUNT(DISTINCT build_tag) = 1 THEN 'PASS'
       ELSE 'FAIL: ' || COUNT(DISTINCT build_tag) || ' different versions running' END AS result
FROM crdb_internal.gossip_nodes;

-- 6. Storage Utilization
SELECT 'STORAGE' AS check,
  CASE WHEN MAX(1 - available::FLOAT / capacity::FLOAT) < 0.7 THEN 'PASS'
       WHEN MAX(1 - available::FLOAT / capacity::FLOAT) < 0.8 THEN 'WARN: node(s) above 70% utilization'
       ELSE 'FAIL: node(s) above 80% utilization' END AS result
FROM crdb_internal.kv_store_status;
```

## Check Details

### Check 1: Node Health
**What:** All nodes must be live and reachable.
**Why:** Draining a node while another is down risks data unavailability (reduces fault tolerance).
**If FAIL:** Investigate the dead node before proceeding. Use `cockroach node status` for details.

### Check 2: No Draining Nodes
**What:** No other nodes should be in a draining state.
**Why:** Only one node should be drained at a time to maintain quorum.
**If FAIL:** Wait for the current drain to complete before starting maintenance on another node.

### Check 3: Replication Health
**What:** All ranges must have the expected number of replicas (typically 3).
**Why:** Under-replicated ranges mean the cluster is already operating with reduced fault tolerance.
**If FAIL:** Wait for re-replication to complete. Check DB Console for stuck ranges.

### Check 4: No Disruptive Jobs
**What:** No schema changes, backups, restores, or imports should be actively running.
**Why:** These operations are sensitive to node unavailability and may fail or retry expensively.
**If WARN:** Either wait for jobs to complete or pause them with `PAUSE JOB <job_id>`.

### Check 5: Consistent Versions
**What:** All nodes should be running the same CockroachDB version.
**Why:** Multiple versions indicate a rolling upgrade is in progress. Do not perform maintenance during an upgrade.
**If FAIL:** Complete the upgrade first before performing other maintenance.

### Check 6: Storage Utilization
**What:** No node should be above 70% disk utilization before maintenance.
**Why:** Draining a node shifts its load to other nodes, temporarily increasing their utilization.
**If WARN (70-80%):** Proceed with caution; monitor remaining nodes during drain.
**If FAIL (>80%):** Add capacity before maintenance. A drained node's workload may push remaining nodes above safe thresholds.

## Post-Maintenance Verification

After maintenance is complete and the node is restarted:

```sql
-- Node is live
SELECT node_id, is_live FROM crdb_internal.gossip_nodes WHERE node_id = <node_id>;

-- Leases returning (check after 5-10 minutes)
SELECT node_id, lease_count FROM crdb_internal.kv_store_status WHERE node_id = <node_id>;

-- All ranges fully replicated
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;
```

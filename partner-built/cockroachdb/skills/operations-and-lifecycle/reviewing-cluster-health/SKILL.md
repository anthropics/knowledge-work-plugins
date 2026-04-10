---
name: reviewing-cluster-health
description: Performs a comprehensive health check of a CockroachDB cluster. Gathers deployment context first, then provides tier-appropriate diagnostics. Self-Hosted uses SQL against node-level system tables and CLI. Advanced/BYOC use Cloud Console and SQL with node visibility. Standard monitors provisioned compute and workload via Cloud Console. Basic monitors Request Unit consumption and connectivity. Use for daily checks, pre-maintenance validation, post-incident verification, or production readiness assessment.
compatibility: Self-Hosted requires SQL access with admin or VIEWCLUSTERMETADATA privilege. Advanced/BYOC require Cloud Console and SQL connectivity. Standard requires Cloud Console and SQL. Basic requires Cloud Console.
metadata:
  author: cockroachdb
  version: "2.0"
---

# Reviewing Cluster Health

Performs a comprehensive health check of a CockroachDB cluster. Before running diagnostics, this skill gathers deployment context to provide the right queries and tools for the operator's tier.

## When to Use This Skill

- Daily or shift-start operational health checks
- Before starting maintenance (Self-Hosted, Advanced, BYOC)
- After incidents to confirm recovery
- Verifying production readiness
- Monitoring capacity and performance

**For live query issues:** Use [triaging-live-sql-activity](../../observability-and-diagnostics/triaging-live-sql-activity/SKILL.md).
**For background jobs:** Use [monitoring-background-jobs](../../observability-and-diagnostics/monitoring-background-jobs/SKILL.md).
**For range analysis:** Use [analyzing-range-distribution](../../observability-and-diagnostics/analyzing-range-distribution/SKILL.md).

---

## Step 1: Gather Context

### Required Context

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Deployment tier?** | Self-Hosted, Advanced, BYOC, Standard, Basic | Determines available diagnostics and operator responsibilities |
| **Reason for health check?** | Daily check, Pre-maintenance, Post-incident, Pre-upgrade | Prioritizes which dimensions to check first |

### Additional Context (by tier)

**If Self-Hosted:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Access available?** | SQL + CLI, SQL only | Determines which tools can be used |
| **Cloud provider?** | AWS, GCP, Azure, On-Premises | Affects infrastructure-level checks |
| **Kubernetes deployment?** | Yes (Operator, Helm, manual), No | Changes CLI commands and monitoring |
| **Node count and regions?** | e.g., 9 nodes, 3 regions | Sets expectations for query results |

**If Advanced or BYOC:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Cloud provider?** (BYOC only) | AWS, GCP, Azure | For infrastructure-level monitoring in your cloud account |

**If Standard:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Current provisioned vCPUs?** | Number | Context for compute utilization assessment |

**If Basic:** No additional context needed.

### Context-Driven Routing

| Tier | Go To |
|------|-------|
| Self-Hosted | [Self-Hosted Health Check](#self-hosted-health-check) |
| Advanced | [Advanced Health Check](#advanced-health-check) |
| BYOC | [BYOC Health Check](#byoc-health-check) |
| Standard | [Standard Health Check](#standard-health-check) |
| Basic | [Basic Health Check](#basic-health-check) |

---

## Self-Hosted Health Check

**Applies when:** Tier = Self-Hosted

### Query 1: Node Liveness

```sql
SELECT
  n.node_id, n.address, n.build_tag AS version, n.locality,
  n.is_live, l.epoch,
  CASE WHEN n.is_live THEN 'HEALTHY'
       WHEN n.is_live IS NULL THEN 'UNKNOWN'
       ELSE 'DOWN' END AS health_status
FROM crdb_internal.gossip_nodes n
LEFT JOIN crdb_internal.gossip_liveness l ON n.node_id = l.node_id
ORDER BY n.node_id;
```

- Any `is_live = false` (from `gossip_nodes`) requires immediate investigation
- High `epoch` suggests repeated restarts (node flapping)

**If CLI is available:**
```bash
cockroach node status --certs-dir=<certs-dir> --host=<node-address>
```

### Query 2: Version Consistency

```sql
SELECT build_tag AS version, COUNT(*) AS node_count,
  array_agg(node_id ORDER BY node_id) AS node_ids
FROM crdb_internal.gossip_nodes GROUP BY build_tag;
```

- Single row = healthy. Two rows = acceptable during rolling upgrade. Three+ = investigate.

### Query 3: Storage Capacity

```sql
SELECT node_id, store_id,
  ROUND(capacity / 1073741824.0, 2) AS total_gb,
  ROUND(available / 1073741824.0, 2) AS available_gb,
  ROUND((1 - (available::FLOAT / capacity::FLOAT)) * 100, 2) AS utilization_pct,
  CASE WHEN (available::FLOAT / capacity::FLOAT) < 0.10 THEN 'CRITICAL'
       WHEN (available::FLOAT / capacity::FLOAT) < 0.30 THEN 'WARNING'
       ELSE 'OK' END AS capacity_status,
  range_count, lease_count
FROM crdb_internal.kv_store_status ORDER BY utilization_pct DESC;
```

### Query 4: Range Health

```sql
SELECT
  CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
       WHEN array_length(replicas, 1) = 2 THEN 'under_replicated'
       WHEN array_length(replicas, 1) = 1 THEN 'critically_under_replicated'
       ELSE 'unknown' END AS replication_status,
  COUNT(*) AS range_count
FROM crdb_internal.ranges_no_leases GROUP BY 1 ORDER BY 1;
```

### Query 5: Certificate Expiration

```sql
SELECT node_id,
  to_timestamp((metrics->>'security.certificate.expiration.ca')::FLOAT)::TIMESTAMPTZ AS ca_expires,
  to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ AS node_cert_expires,
  CASE WHEN to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ
            < now() + INTERVAL '90 days' THEN 'EXPIRING_SOON'
       ELSE 'OK' END AS cert_status
FROM crdb_internal.kv_node_status ORDER BY node_cert_expires;
```

### Query 6: Critical Settings

```sql
SELECT variable, value FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable IN (
  'kv.rangefeed.enabled', 'sql.stats.automatic_collection.enabled',
  'server.time_until_store_dead', 'admission.kv.enabled',
  'cluster.preserve_downgrade_option', 'gc.ttlseconds'
) ORDER BY variable;
```

### Query 7: Consolidated Summary

```sql
SELECT 'live_nodes' AS metric, COUNT(*)::TEXT AS value
FROM crdb_internal.gossip_nodes WHERE is_live = true
UNION ALL SELECT 'dead_nodes', COUNT(*)::TEXT
FROM crdb_internal.gossip_nodes WHERE is_live = false
UNION ALL SELECT 'distinct_versions', COUNT(DISTINCT build_tag)::TEXT
FROM crdb_internal.gossip_nodes
UNION ALL SELECT 'total_ranges', COUNT(*)::TEXT
FROM crdb_internal.ranges_no_leases
UNION ALL SELECT 'min_store_available_pct',
  ROUND(MIN(available::FLOAT / capacity::FLOAT) * 100, 2)::TEXT
FROM crdb_internal.kv_store_status
UNION ALL SELECT 'cluster_version', value
FROM [SHOW CLUSTER SETTING version];
```

**If reason = Pre-maintenance**, also check for running jobs:
```sql
WITH j AS (SHOW JOBS)
SELECT job_type, COUNT(*) FROM j WHERE status = 'running' GROUP BY job_type;
```

### Query 8: Production Readiness Assessment

Use when verifying a cluster is ready for production workloads or during periodic operational reviews.

```sql
-- Node count and replication (minimum 3 nodes for production)
SELECT COUNT(*) AS total_nodes,
  COUNT(*) FILTER (WHERE n.is_live) AS live_nodes,
  COUNT(DISTINCT n.locality) AS distinct_localities
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id);

-- Critical production settings check
SELECT variable, value,
  CASE
    WHEN variable = 'kv.rangefeed.enabled' AND value = 'true' THEN 'OK'
    WHEN variable = 'kv.rangefeed.enabled' AND value = 'false' THEN 'WARN: should be true for CDC'
    WHEN variable = 'sql.stats.automatic_collection.enabled' AND value = 'true' THEN 'OK'
    WHEN variable = 'sql.stats.automatic_collection.enabled' AND value = 'false' THEN 'WARN: should be true'
    WHEN variable = 'admission.kv.enabled' AND value = 'true' THEN 'OK'
    WHEN variable = 'admission.kv.enabled' AND value = 'false' THEN 'WARN: recommended for production'
    WHEN variable = 'cluster.preserve_downgrade_option' AND value != '' THEN 'INFO: finalization pending'
    ELSE 'OK'
  END AS assessment
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable IN (
  'kv.rangefeed.enabled', 'sql.stats.automatic_collection.enabled',
  'admission.kv.enabled', 'cluster.preserve_downgrade_option',
  'server.time_until_store_dead', 'gc.ttlseconds'
) ORDER BY variable;

-- Enterprise license status (Self-Hosted only)
SELECT value AS organization FROM [SHOW CLUSTER SETTING cluster.organization];
```

See [production-readiness reference](references/production-readiness.md) for the full production readiness checklist.

---

## Advanced Health Check

**Applies when:** Tier = Advanced

Advanced clusters are dedicated single-tenant clusters managed by Cockroach Labs. You have node-level visibility via both Cloud Console and SQL.

### Cloud Console Checks

1. **Cluster Overview** — verify all nodes are live, check node count
2. **Metrics** — CPU utilization, QPS, P99 latency, storage utilization
3. **Alerts** — check for active alerts

### SQL Checks

```sql
-- Node liveness (nodes are visible on Advanced)
SELECT n.node_id, n.build_tag, n.is_live
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id) ORDER BY n.node_id;

-- Version consistency
SELECT build_tag AS version, COUNT(*) FROM crdb_internal.gossip_nodes GROUP BY 1;

-- Range health
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;

-- Recent failed jobs
WITH j AS (SHOW JOBS)
SELECT job_type, status, COUNT(*) FROM j
WHERE status IN ('running', 'failed') AND created > now() - INTERVAL '24 hours'
GROUP BY job_type, status;
```

### Cloud API

```bash
curl -s -H "Authorization: Bearer $COCKROACH_API_KEY" \
  "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>" | jq '.state, .cockroach_version'
```

---

## BYOC Health Check

**Applies when:** Tier = BYOC

BYOC clusters are dedicated and run in your cloud account. You have the same CockroachDB visibility as Advanced, plus direct access to the underlying infrastructure.

### CockroachDB Health

Run all [Advanced Health Check](#advanced-health-check) steps.

### Cloud Provider Infrastructure Checks

**If AWS:**
```bash
aws ec2 describe-instance-status --filters "Name=tag:cockroach-cluster,Values=<cluster-name>"
```

**If GCP:**
```bash
gcloud compute instances list --filter="labels.cockroach-cluster=<cluster-name>"
```

**If Azure:**
```bash
az vm list --resource-group <rg> --query "[?tags.cockroachCluster=='<cluster-name>']"
```

### Additional BYOC Checks

- Verify VPC/network connectivity (PrivateLink, PSC, VPC Peering)
- Check IAM roles — CRL service account permissions still valid
- Review cloud provider monitoring for infrastructure-level anomalies

---

## Standard Health Check

**Applies when:** Tier = Standard

Standard is a multi-tenant managed service. There are no individual nodes to monitor — Cockroach Labs manages all infrastructure, replication, and capacity. Health checking focuses on your workload performance and provisioned compute.

### Cloud Console Checks

1. **Cluster Overview** — verify cluster state is `RUNNING`
2. **SQL Activity** — statement and transaction latency, error rates
3. **Storage** — current usage
4. **Compute** — provisioned vCPU utilization

### SQL Checks

```sql
-- Verify connectivity
SELECT 1;

-- Current version
SELECT version();

-- Recent failed jobs
WITH j AS (SHOW JOBS)
SELECT job_type, status, description FROM j
WHERE status = 'failed' AND created > now() - INTERVAL '24 hours';
```

### What to Monitor

- **P99 SQL latency** — track via Cloud Console Metrics
- **Error rates** — check for spikes in statement errors
- **Storage growth** — plan based on usage trends
- **Compute utilization** — increase provisioned vCPUs if utilization is consistently high

**Note:** Node-level system tables (`crdb_internal.gossip_nodes`, `kv_store_status`, etc.) are not available on Standard. Use Cloud Console for all infrastructure health monitoring.

---

## Basic Health Check

**Applies when:** Tier = Basic

Basic is a serverless offering that auto-scales. There are no nodes or provisioned compute to monitor. Cockroach Labs manages all infrastructure. Health checking focuses on connectivity, consumption, and spending.

### Cloud Console Checks

1. **Cluster Overview** — verify state is `RUNNING`
2. **Request Units** — consumption rate and remaining budget
3. **Storage** — current usage (10 GiB included free)
4. **Spending Limits** — verify limits are configured to avoid unexpected charges

### SQL Checks

```sql
-- Verify connectivity
SELECT 1;

-- Current version
SELECT version();

-- Recent failed jobs
WITH j AS (SHOW JOBS)
SELECT job_type, status, description FROM j
WHERE status = 'failed' AND created > now() - INTERVAL '24 hours';
```

### What to Monitor

- **Request Unit (RU) consumption** — track via Cloud Console to stay within spending limits
- **Storage usage** — monitor growth relative to the 10 GiB free tier
- **Query efficiency** — optimize queries that consume excessive RUs
- **Cold start latency** — Basic clusters may scale to zero during inactivity; first connection after idle may have higher latency

---

## Safety Considerations

All queries in this skill are read-only. No data is modified.

- **Self-Hosted:** `crdb_internal.ranges_no_leases` can be slow on large clusters — consider using `LIMIT`
- **Advanced/BYOC:** Some system tables may have restricted access depending on SQL user role
- **Standard/Basic:** Node-level system tables are not available — this is expected, not an error

## Troubleshooting

| Issue | Tier | Fix |
|-------|------|-----|
| `crdb_internal.kv_node_status` empty | SH | Grant admin or VIEWCLUSTERMETADATA |
| `crdb_internal` table not found | STD/BAS | Expected — use Cloud Console |
| Node missing from gossip_nodes | SH | Check node process; verify --join address |
| Cloud Console shows degraded | ADV/BYOC | Check Cloud status page; contact support |
| High RU consumption | BAS | Profile queries; set spending limits |
| Cloud API returns 401 | ADV/BYOC | Regenerate API key |
| High latency on first connection | BAS | Expected cold start after idle period |

## References

**Skill references:**
- [Production readiness checklist](references/production-readiness.md)

**Related skills:**
- [upgrading-cluster-version](../upgrading-cluster-version/SKILL.md)
- [managing-cluster-capacity](../managing-cluster-capacity/SKILL.md)
- [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md)
- [monitoring-background-jobs](../../observability-and-diagnostics/monitoring-background-jobs/SKILL.md)

**Official CockroachDB Documentation:**
- [Monitoring and Alerting](https://www.cockroachlabs.com/docs/stable/monitoring-and-alerting)
- [crdb_internal](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)
- [Production Checklist](https://www.cockroachlabs.com/docs/stable/recommended-production-settings)
- [Cloud Console Monitoring](https://www.cockroachlabs.com/docs/cockroachcloud/cluster-overview-page)
- [Export Metrics (Advanced)](https://www.cockroachlabs.com/docs/cockroachcloud/export-metrics)

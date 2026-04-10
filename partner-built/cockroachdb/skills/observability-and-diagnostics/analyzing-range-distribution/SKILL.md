---
name: analyzing-range-distribution
description: Analyzes CockroachDB range distribution across tables and indexes using SHOW RANGES to identify range count, size patterns, leaseholder placement, and replication health. Use when investigating hotspots, uneven data distribution, range fragmentation, or validating zone configuration effects without DB Console access.
compatibility: Requires SQL access with admin role or ZONECONFIG system privilege. DETAILS option has high cost; use targeted queries with LIMIT. Production-safe for basic usage.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Analyzing Range Distribution

Analyzes CockroachDB range distribution, leaseholder placement, and zone configuration compliance using `SHOW RANGES` and `SHOW ZONE CONFIGURATIONS` commands. Identifies range count anomalies, size imbalances, leaseholder hotspots, and replication issues - entirely via SQL without requiring DB Console access.

**Complement to profiling skills:** This skill analyzes range-level data distribution; for query performance patterns, see [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md). For schema change storage planning, see [analyzing-schema-change-storage-risk](../analyzing-schema-change-storage-risk/SKILL.md).

## When to Use This Skill

- Identify tables/indexes with excessive range counts indicating fragmentation
- Detect range size imbalances or uneven data distribution across nodes
- Investigate leaseholder concentration causing read hotspots
- Validate zone configuration effects on range placement and replica distribution
- Diagnose range-level replication issues (under-replicated or unavailable ranges)
- Analyze range split patterns from high write volume
- SQL-only range analysis without DB Console access

**For schema change planning:** Use [analyzing-schema-change-storage-risk](../analyzing-schema-change-storage-risk/SKILL.md) to estimate storage requirements before CREATE INDEX or ADD COLUMN operations.

## Prerequisites

- SQL connection to CockroachDB cluster
- Admin role OR `ZONECONFIG` system privilege
- Understanding of CockroachDB range architecture (64MB default max size)
- Knowledge of cluster topology (node IDs, regions, availability zones)

**Check your privileges:**
```sql
SHOW GRANTS ON SYSTEM FOR current_user;  -- Should show admin or ZONECONFIG
```

See [permissions reference](references/permissions.md) for RBAC setup.

## Core Concepts

### Ranges: Units of Data Distribution

**Range:** Contiguous key space segment (default 64MB max size, configurable via zone config `range_max_bytes`)
**Raft group:** Each range replicated across nodes (default 3 replicas)
**Leaseholder:** Single replica handling reads and coordinating writes for a range

**Critical:** Ranges split automatically at 64MB by default, but can fragment further due to load-based splitting during high write traffic.

### Leaseholders and Hotspots

**Leaseholder concentration:** Single node holding disproportionate leaseholders = read hotspot
**Load-based splitting:** CockroachDB splits ranges experiencing high QPS, increasing range count
**Hotspot symptoms:** High CPU on single node, slow reads on specific table/index

### Range Fragmentation

**Fragmentation:** Excessive range splits creating many small ranges (overhead from Raft coordination)
**Causes:** High write throughput, sequential inserts (timestamp-based primary keys), load-based splitting
**Symptoms:** High range count relative to data size, increased latency from Raft overhead

**Fragmentation metric:** Ranges per GB (healthy: 1-15, fragmented: 50+)

### Zone Configurations

**Zone config:** Replication and placement policies for databases, tables, or indexes
**Replication factor:** Number of replicas per range (default: 3)
**Constraints:** Node placement rules (region, availability zone, node attributes)

**Use case:** Validate intended zone config matches actual range placement.

### SHOW RANGES DETAILS Option

**CRITICAL SAFETY WARNING:** The `WITH DETAILS` option computes `span_stats` (range size, key counts) on-demand, causing:
- **High CPU usage** from statistics computation
- **Memory overhead** proportional to range count
- **Query timeouts** on large tables without LIMIT

**Best practice:** Always use `LIMIT` with `DETAILS`, target specific tables/indexes, avoid cluster-wide scans.

## Core Diagnostic Queries

### Query 1: Range Count by Table (Production-Safe)

```sql
SELECT
  table_name,
  index_name,
  COUNT(*) AS range_count
FROM [SHOW RANGES FROM TABLE your_table_name]
GROUP BY table_name, index_name
ORDER BY range_count DESC;
```

**Interpretation:** High range count (1000s) on small tables indicates fragmentation. Cross-reference with table size.

**Safety:** No `DETAILS` option = production-safe, minimal overhead.

### Query 2: Range Size Analysis (Targeted DETAILS)

```sql
SELECT
  range_id,
  start_key,
  end_key,
  (span_stats->>'approximate_disk_bytes')::INT / 1048576 AS size_mb,
  lease_holder,
  replicas
FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
ORDER BY (span_stats->>'approximate_disk_bytes')::INT DESC
LIMIT 50;
```

**Interpretation:** Large ranges (>64MB) indicate split lag; many small ranges (<10MB) indicate fragmentation.

**CRITICAL:** Always include `LIMIT` and target specific tables. Never run `SHOW RANGES WITH DETAILS` on entire database.

### Query 3: Leaseholder Distribution (Hotspot Detection)

```sql
SELECT
  lease_holder,
  COUNT(*) AS leaseholder_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM [SHOW RANGES FROM TABLE your_table_name]
GROUP BY lease_holder
ORDER BY leaseholder_count DESC;
```

**Interpretation:** >40% leaseholders on single node in balanced cluster = hotspot. Check if table has zone constraints favoring specific nodes.

**Remediation:** Use `ALTER TABLE ... CONFIGURE ZONE USING lease_preferences` to spread leaseholders.

### Query 4: Range Replication Health Check

```sql
SELECT
  range_id,
  start_key,
  replicas,
  array_length(replicas, 1) AS replica_count,
  voting_replicas,
  array_length(voting_replicas, 1) AS voting_replica_count,
  lease_holder
FROM [SHOW RANGES FROM TABLE your_table_name]
WHERE array_length(replicas, 1) < 3  -- Under-replicated
ORDER BY range_id
LIMIT 100;
```

**Interpretation:** `replica_count < 3` = under-replicated (data loss risk). Check for node failures, decommissioning operations, or zone config mismatches.

**Safety:** No `DETAILS` = production-safe.

### Query 5: Zone Configuration Audit

```sql
SHOW ZONE CONFIGURATIONS;
```

**Output columns:**
- `target`: Database, table, or index
- `raw_config_sql`: Zone config SQL (replication factor, constraints)

**Use case:** Validate intended replication factor and placement constraints match expected design.

**Cross-reference:** Compare zone configs with Query 3 (leaseholder distribution) and Query 4 (replica health) to validate actual placement.

### Query 6: Fragmentation Analysis (Ranges per GB)

```sql
WITH range_counts AS (
  SELECT
    table_name,
    index_name,
    COUNT(*) AS range_count
  FROM [SHOW RANGES FROM TABLE your_table_name]
  GROUP BY table_name, index_name
),
table_sizes AS (
  SELECT
    table_name,
    SUM((span_stats->>'approximate_disk_bytes')::INT) / 1073741824.0 AS size_gb
  FROM [SHOW RANGES FROM TABLE your_table_name WITH DETAILS]
  GROUP BY table_name
)
SELECT
  rc.table_name,
  rc.index_name,
  rc.range_count,
  ts.size_gb,
  ROUND(rc.range_count / NULLIF(ts.size_gb, 0), 2) AS ranges_per_gb
FROM range_counts rc
JOIN table_sizes ts ON rc.table_name = ts.table_name
ORDER BY ranges_per_gb DESC;
```

**Interpretation:**
- **Healthy:** 1-15 ranges/GB
- **Moderate fragmentation:** 16-50 ranges/GB
- **Severe fragmentation:** 50+ ranges/GB

**CRITICAL:** This query uses `DETAILS` - only run on targeted tables with known size, never cluster-wide.

**Remediation:** Increase `range_max_bytes` via zone config (with caution), or accept fragmentation if caused by necessary load-based splitting.

See [sql-queries reference](references/sql-queries.md) for complete query variations and guardrails.

## Common Workflows

### Workflow 1: Hotspot Investigation

**Scenario:** Single node experiencing high CPU, slow reads on specific table.

**Steps:**
1. **Identify leaseholder concentration:** Run Query 3 on suspected table
2. **Validate zone config:** Run Query 5 to check lease_preferences
3. **Check for load-based splits:** Run Query 1 to detect recent range fragmentation (symptom of hotspot)
4. **Remediate:** Configure lease preferences to spread reads, or partition table if hotspot is on sequential key range

**Example:**
```sql
-- Check leaseholder distribution
SELECT lease_holder, COUNT(*) FROM [SHOW RANGES FROM TABLE hot_table] GROUP BY lease_holder;

-- Validate zone config
SHOW ZONE CONFIGURATION FOR TABLE hot_table;

-- Spread leaseholders if concentrated
ALTER TABLE hot_table CONFIGURE ZONE USING lease_preferences = '[[+region=us-west]]';
```

### Workflow 2: Zone Config Validation

**Scenario:** After configuring multi-region setup, validate ranges are placed according to constraints.

**Steps:**
1. **Review intended configs:** Run Query 5 (SHOW ZONE CONFIGURATIONS)
2. **Check actual replica placement:** Run Query 4 on critical tables, inspect `replicas` array for node IDs
3. **Map node IDs to regions:** Cross-reference with `SHOW REGIONS` or `crdb_internal.gossip_nodes`
4. **Identify mismatches:** Ranges not matching constraints indicate rebalancing in progress or misconfiguration

**Example:**
```sql
-- Show zone config
SHOW ZONE CONFIGURATION FOR TABLE multi_region_table;

-- Check replica placement
SELECT range_id, replicas FROM [SHOW RANGES FROM TABLE multi_region_table] LIMIT 20;

-- Map node IDs to regions
SELECT node_id, locality FROM crdb_internal.gossip_nodes;
```

### Workflow 3: Fragmentation Diagnosis

**Scenario:** Table with high range count relative to size, experiencing latency.

**Steps:**
1. **Calculate ranges per GB:** Run Query 6 (targeted to specific table)
2. **Check for load-based splits:** Review write patterns (sequential inserts, high QPS periods)
3. **Determine if expected:** Fragmentation may be intentional for load distribution
4. **Remediate if excessive:** Increase `range_max_bytes` (with caution - larger ranges = slower splits), or investigate reducing write hotspots

**CRITICAL:** Never increase `range_max_bytes` above 512MB without understanding impact on split/rebalance performance.

## Safety Considerations

### DETAILS Option Cost

**Resource impact:**
- **CPU:** Computes span statistics on-demand for each range
- **Memory:** Proportional to range count returned
- **Timeout risk:** High on tables with 1000s of ranges without LIMIT

**Mitigation strategies:**
1. **Always use LIMIT:** Cap at 50-100 ranges for exploratory analysis
2. **Target specific tables:** Use `FROM TABLE table_name`, never cluster-wide `SHOW RANGES WITH DETAILS`
3. **Use basic queries first:** Run Query 1 (no DETAILS) to assess range count before using DETAILS
4. **Production timing:** Run during maintenance windows or low-traffic periods

### Privilege Safety

**Admin role:** Full cluster access, use with caution in production
**ZONECONFIG privilege:** Limited to viewing ranges and zone configs, safer for read-only analysis

**Best practice:** Grant `ZONECONFIG` instead of admin for range analysis operators.

See [permissions reference](references/permissions.md) for granting minimal privileges.

### Production Impact

**Read-only operations:** All queries are `SELECT` or `SHOW` statements with no writes.

**Performance considerations:**

| Query Type | Impact | Safe for Production? |
|------------|--------|---------------------|
| Basic SHOW RANGES | Minimal CPU, metadata-only | Yes |
| SHOW RANGES WITH DETAILS (targeted, LIMIT 50) | Moderate CPU spike | Yes (low-traffic window) |
| SHOW RANGES WITH DETAILS (no LIMIT) | High CPU, timeout risk | **NO - NEVER USE** |
| SHOW ZONE CONFIGURATIONS | Minimal, metadata-only | Yes |

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Permission denied | Missing admin or ZONECONFIG privilege | Grant ZONECONFIG: `GRANT SYSTEM ZONECONFIG TO user` |
| Query timeout with DETAILS | Too many ranges without LIMIT | Add `LIMIT 50`, target specific table |
| Empty span_stats column | Missing DETAILS keyword | Add `WITH DETAILS` to SHOW RANGES |
| Unexpected high range count | Load-based splitting or fragmentation | Run Query 6 to calculate ranges/GB, review write patterns |
| Leaseholder = 0 or NULL | Range in transition during rebalancing | Normal during cluster changes, retry query |
| Under-replicated ranges | Node failure, decommission, zone mismatch | Check node status, validate zone config constraints |
| SHOW ZONE CONFIGURATIONS shows no custom configs | Using default cluster-wide config | Normal if no table/database-level overrides set |

## Key Considerations

- **DETAILS option:** Expensive operation - always use with LIMIT and targeted scope
- **Fragmentation is sometimes intentional:** Load-based splitting improves concurrency
- **Leaseholder concentration:** Check zone configs (lease_preferences) before assuming hotspot
- **Range size target:** Default 64MB max (not 512MB as in older versions)
- **Replication lag:** Range placement may not immediately reflect zone config changes (rebalancing takes time)
- **Cross-reference queries:** Combine range analysis with zone configs for complete picture
- **Node mapping:** Use `crdb_internal.gossip_nodes` to map node IDs to regions/zones

## References

**Skill references:**
- [SQL query variations and guardrails](references/sql-queries.md)
- [RBAC and privileges setup](references/permissions.md)

**Official CockroachDB Documentation:**
- [SHOW RANGES](https://www.cockroachlabs.com/docs/stable/show-ranges.html)
- [SHOW ZONE CONFIGURATIONS](https://www.cockroachlabs.com/docs/stable/show-zone-configurations.html)
- [Architecture: Distribution Layer](https://www.cockroachlabs.com/docs/stable/architecture/distribution-layer.html)
- [Configure Replication Zones](https://www.cockroachlabs.com/docs/stable/configure-replication-zones.html)
- [ZONECONFIG privilege](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

**Related skills:**
- [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) - For query performance analysis
- [triaging-live-sql-activity](../triaging-live-sql-activity/SKILL.md) - For real-time query triage
- [analyzing-schema-change-storage-risk](../analyzing-schema-change-storage-risk/SKILL.md) - For estimating storage requirements before DDL operations

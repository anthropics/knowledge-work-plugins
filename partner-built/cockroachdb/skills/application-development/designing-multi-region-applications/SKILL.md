---
name: designing-multi-region-applications
description: Guides developers in selecting and implementing multi-region patterns for CockroachDB applications, covering active-passive vs active-active architectures, REGIONAL BY ROW, GLOBAL tables, manual geo-partitioning with lease preferences, and live demo setup with validation queries. Use when designing multi-region database topologies, choosing between REGIONAL BY ROW and manual partitioning, building multi-region demos, or optimizing cross-region latency.
compatibility: "CockroachDB >= 22.1 with multi-region licensed features. Requires a multi-region cluster or cockroach demo with locality flags."
metadata:
  author: cockroachdb
  version: "1.0"
---

# Designing Multi-Region Applications

Guides developers through selecting the right multi-region pattern for their CockroachDB application and implementing it with proper validation. Covers the decision model for choosing between regular regional tables, `REGIONAL BY ROW`, `GLOBAL` tables, and manual geo-partitioning, plus a hands-on demo framework for comparing approaches.

**Complement to other skills:** For transaction design patterns, see [designing-application-transactions](../designing-application-transactions/SKILL.md). For SQL syntax and schema design, see [cockroachdb-sql](../../query-and-schema-design/cockroachdb-sql/SKILL.md).

## When to Use This Skill

- Deciding how to model multi-region read/write behavior in CockroachDB
- Choosing between active-active and active-passive architectures
- Evaluating `REGIONAL BY ROW` vs manual geo-partitioning
- Understanding `GLOBAL` table behavior and trade-offs
- Designing for local reads and writes in multiple regions
- Building or presenting a multi-region demo or workshop
- Validating leaseholder placement and zone configurations
- Optimizing cross-region transaction latency

**Do not use this skill** when the question is only about SQL syntax, indexing, or generic schema design with no multi-region decision involved.

## Prerequisites

- Understanding of CockroachDB range architecture and leaseholder concepts
- Multi-region cluster or `cockroach demo` with locality flags for testing
- Knowledge of application write patterns (single-region vs multi-region)

## Pattern Selection

### Step 1: Identify the Application Write Model

Ask first: **is there one write home, or many?**

- If the application has **one primary region for read/write**, start with a primary-region / regular regional-table model or a manually configured active-passive design.
- If the application needs **low-latency read/write in multiple regions**, evaluate manual geo-partitioning or `REGIONAL BY ROW`.
- If the table is mostly **reference data** that should read fast everywhere and the write path is not the main focus, consider `GLOBAL` tables.

### Step 2: Choose the Pattern

#### A. Regular Regional Tables (Active-Passive)

**Use when:**
- The application has one primary region for RW
- Remote regions are secondary or read-mostly
- Simplicity matters more than region-local writes everywhere

**Characteristics:**
- All leaseholders stay in the active region
- Replicas in other regions provide resiliency and single-region-failure survival
- Indicative latency: ~20ms writes, ~2-5ms reads (local region)

**Recommendation:** Prefer the higher-level multi-region abstractions first unless the user explicitly needs manual control over partitions, voters, and lease preferences.

#### B. Manual Geo-Partitioning with Region-Specific Leaseholders

**Use when:**
- The application is active-active
- The data model is region-keyed
- The team wants explicit operational control
- Understanding internal mechanics (partitions, voters, lease preferences) is important

**Characteristics:**
- Region-specific leaseholder pattern keeps writes around ~20ms and reads around ~2-5ms
- The application must enforce reads and writes for a key in the same region
- More DDL and operational burden
- Best for teaching internals

**Example DDL:**

```sql
CREATE TABLE accounts_manual (
  account_id STRING(40),
  owner_id   STRING(40) NOT NULL,
  status     STRING(20) NOT NULL,
  region     STRING(10) NOT NULL,
  CONSTRAINT accounts_manual_pkey PRIMARY KEY (region, account_id)
);

ALTER INDEX accounts_manual_pkey
  PARTITION BY LIST (region) (
    PARTITION na_ne VALUES IN ('NA-NE'),
    PARTITION na_mw VALUES IN ('NA-MW'),
    PARTITION na_nw VALUES IN ('NA-NW')
  );

ALTER PARTITION na_ne OF INDEX accounts_manual_pkey
  CONFIGURE ZONE USING
    num_replicas      = 5,
    num_voters        = 5,
    voter_constraints = '{+region=NA-NE: 2, +region=NA-MW: 2, +region=NA-NW: 1}',
    lease_preferences = '[[+region=NA-NE]]';
```

#### C. REGIONAL BY ROW

**Use when:**
- The workload is active-active
- Each row naturally belongs to a region
- The team wants local RW in multiple regions without hand-managing partition zone configs
- The goal is the developer-facing multi-region abstraction

**Characteristics:**
- All configured regions are possible home/leaseholder regions
- Indicative latency: ~20ms writes, ~2-5ms reads (local region)
- Less manual configuration than geo-partitioning
- Default recommendation for region-affine application data

**Example DDL:**

```sql
CREATE DATABASE IF NOT EXISTS example_service_rbr;
ALTER DATABASE example_service_rbr PRIMARY REGION 'NA-NE';
ALTER DATABASE example_service_rbr ADD REGION 'NA-NW';
ALTER DATABASE example_service_rbr ADD REGION 'NA-MW';
ALTER DATABASE example_service_rbr SURVIVE REGION FAILURE;

USE example_service_rbr;

CREATE TABLE accounts_rbr (
  account_id STRING(40),
  owner_id   STRING(40) NOT NULL,
  status     STRING(20) NOT NULL,
  region     crdb_internal_region
    NOT NULL
    DEFAULT gateway_region()::crdb_internal_region,
  CONSTRAINT accounts_rbr_pkey PRIMARY KEY (region, account_id)
) LOCALITY REGIONAL BY ROW AS region;
```

**Local allocation pattern:**

```sql
WITH candidate AS (
  SELECT id, resource_code
  FROM resource_pool
  WHERE allocated_at IS NULL
    AND region = gateway_region()::crdb_internal_region
  ORDER BY random()
  LIMIT 1
  FOR UPDATE
)
UPDATE resource_pool
SET allocated_at = now()
WHERE id = (SELECT id FROM candidate);
```

#### D. GLOBAL Tables

**Use when:**
- The table is global/reference-style data
- The workload is primarily about broad read locality rather than region-owned writes

**Important constraint:** `GLOBAL` tables optimize for fast reads everywhere. Do not position them as an "RW everywhere" pattern without verifying product-specific behavior in the official documentation.

#### E. Survival Goals

Choose the survival goal based on the trade-off between write latency and durability:

```sql
-- Survive any single zone failure (default, 3+ zones required):
ALTER DATABASE mydb SURVIVE ZONE FAILURE;

-- Survive an entire region going down (3+ regions required):
ALTER DATABASE mydb SURVIVE REGION FAILURE;
```

| Goal                   | Requirement | Write Latency                   | Data Safety              |
|------------------------|-------------|---------------------------------|--------------------------|
| SURVIVE ZONE FAILURE   | 3+ zones    | Low (local consensus)           | Survives 1 zone outage   |
| SURVIVE REGION FAILURE | 3+ regions  | Higher (cross-region consensus) | Survives 1 region outage |

`SURVIVE REGION FAILURE` adds write latency because Raft consensus must span regions, but guarantees zero data loss even if an entire cloud region goes offline.

### Pattern Comparison

| Aspect             | Regular Regional           | Manual Geo-Partition                    | REGIONAL BY ROW               | GLOBAL                    |
|--------------------|----------------------------|-----------------------------------------|-------------------------------|---------------------------|
| Write model        | Single primary region      | Active-active, region-keyed             | Active-active, row-affine     | Write from primary region |
| Read locality      | Local to primary           | Local to partition                      | Local to row region           | All regions               |
| Operational burden | Low                        | High                                    | Medium                        | Low                       |
| Configuration      | Minimal                    | Explicit partitions, zones, lease prefs | Database-level abstractions   | Table-level declaration   |
| Best for           | Simple primary-region apps | Full control over mechanics             | Developer-facing multi-region | Reference data            |

## Live Demo Setup

For workshops and technical walkthroughs, use a 9-node local demo cluster to make multi-region locality observable.

### Cluster Setup

```bash
cockroach demo \
  --nodes 9 \
  --no-example-database \
  --insecure \
  --demo-locality=\
region=NA-NE,zone=NA-NE-1:\
region=NA-NE,zone=NA-NE-2:\
region=NA-NE,zone=NA-NE-3:\
region=NA-MW,zone=NA-MW-1:\
region=NA-MW,zone=NA-MW-2:\
region=NA-MW,zone=NA-MW-3:\
region=NA-NW,zone=NA-NW-1:\
region=NA-NW,zone=NA-NW-2:\
region=NA-NW,zone=NA-NW-3
```

### Demo Flow

**Recommended presentation order:**

1. Start with the manual geo-partitioning path
2. Show explicit partitioning and zone configuration
3. Run validation queries and confirm lease homing
4. Switch to REGIONAL BY ROW
5. Run RBR validations
6. Compare operational surface area

### Validation Queries

**Manual partitioning validation:**

```sql
SHOW RANGES FROM INDEX accounts_manual_pkey WITH DETAILS;
```

Check that:
- All expected partition values are present
- Lease holder locality matches partition region
- Mismatches return FAIL, otherwise PASS

**RBR validation:**

```sql
SHOW RANGES FROM TABLE accounts_rbr WITH DETAILS;
```

Check that:
- Leaseholder locality coverage includes the expected regions
- There are no unexpected lease regions

### Demo Talking Points

**Manual path:**
- Precise control over partitions, voters, replicas, and lease preferences
- More DDL and operational burden
- Best for teaching internals and understanding what the database does under the hood

**RBR path:**
- Keeps application intent front and center
- Less manual configuration
- Easier to explain for app teams
- Still grounded in the same topology

## Cross-Region Latency Guidance

Transaction latency increases when the client is remote from the relevant leaseholder/quorum path.

| Client Location            | Local RW Latency | Cross-Region RW Latency |
|----------------------------|------------------|-------------------------|
| Same region as leaseholder | ~10-20ms         | —                       |
| Different region           | —                | ~50-150ms+              |

**Guidance:**
- Place latency-sensitive services close to their primary data locality
- Use follower reads for non-critical display/reporting queries
- Use multi-region table locality and zone configuration intentionally
- Do not assume "distributed" means "same latency everywhere"

## Output Expectations

A strong answer using this skill should include:

1. The recommended pattern
2. Why it fits the workload
3. What the application must do (routing, row affinity, primary-region assumptions)
4. What CockroachDB manages automatically vs manually
5. Expected latency shape or locality behavior
6. A warning when the user is asking for something the chosen pattern does not optimize for

## Guardrails

- Do not claim that regular primary-region tables provide symmetric low-latency writes from all regions
- Do not claim that `GLOBAL` is the answer for all-region low-latency writes without supporting documentation
- When comparing manual geo-partitioning vs `REGIONAL BY ROW`, explicitly call out control vs simplicity
- When the user wants to understand internal mechanics, bias toward explaining the manual model first
- When the user wants the best default application pattern, bias toward `REGIONAL BY ROW` for region-affine data
- Keep region names and locality labels consistent across all SQL
- Do not mix manual and abstraction approaches in the same explanation unless explicitly comparing them
- Always include validation, not just DDL

## Multi-Region Migration Checklist

For teams migrating from single-region PostgreSQL/Oracle to multi-region CockroachDB:

1. Deploy nodes with `--locality=region=<region>,zone=<zone>`
2. Set primary region: `ALTER DATABASE <db> PRIMARY REGION '<region>'`
3. Add regions: `ALTER DATABASE <db> ADD REGION '<region>'` (for each)
4. Set survival goal: `ALTER DATABASE <db> SURVIVE ZONE|REGION FAILURE`
5. Classify tables: GLOBAL (reference data), REGIONAL BY ROW (row-affine), REGIONAL BY TABLE (default)
6. Set localities: `ALTER TABLE <t> SET LOCALITY <locality>`
7. Monitor leaseholder distribution in DB Console
8. Test failover: kill a zone/region and verify survival goal holds

## Safety Considerations

- Multi-region configuration changes affect data placement across the cluster
- Test multi-region configurations on demo or staging clusters before production
- Validate leaseholder placement after configuration changes
- Allow time for range rebalancing after topology changes

## References

- [CockroachDB Multi-Region Overview](https://www.cockroachlabs.com/docs/stable/multiregion-overview)
- [REGIONAL BY ROW Tables](https://www.cockroachlabs.com/docs/stable/regional-tables)
- [GLOBAL Tables](https://www.cockroachlabs.com/docs/stable/global-tables)
- [Follower Reads Documentation](https://www.cockroachlabs.com/docs/stable/follower-reads)
- [CockroachDB Transactions](https://www.cockroachlabs.com/docs/stable/transactions)
- [Performance Best Practices](https://www.cockroachlabs.com/docs/stable/performance-best-practices-overview)
- [Cross-Regional Latency Impact on Transactions](https://andrewdeally.medium.com/cross-regional-latency-impact-on-transactions-with-cockroachdb-a38e0dcb82f9)
- [Query Parallelism with CockroachDB](https://andrewdeally.medium.com/when-and-how-to-use-query-parallelism-with-cockroachdb-df92fbe92845)
- [CockroachDB Best Practices & Anti-Patterns Demo](https://github.com/viragtripathi/cockroachdb-best-practices-demo) -- Demo 10 covers multi-region patterns with runnable examples

# Production Deployment Checklist

Pre-go-live checklist for CockroachDB Self-Hosted deployments. Complete all items before directing production traffic to the cluster.

## Infrastructure

- [ ] **3+ nodes** deployed across separate failure domains (zones or racks)
- [ ] **Non-burstable CPU** instances (no AWS t-series, GCP e2-micro/small)
- [ ] **SSD storage** (NVMe preferred, no HDDs)
- [ ] **Memory configured**: `--cache=.25 --max-sql-memory=.25` (or equivalent for your RAM)
- [ ] **Locality flags** set on all nodes (`--locality=region=...,zone=...`)
- [ ] **Clock synchronization** verified (chrony/NTP, within 500ms)
- [ ] **Ballast files** created on each node (`cockroach debug ballast`)
- [ ] **systemd** (or process manager) configured for auto-restart on failure
- [ ] **File descriptor limit** set to 65536+ (`LimitNOFILE` in systemd)

## Networking

- [ ] **Load balancer** configured with health check on `/health?ready=1`
- [ ] **Firewall rules** allow port 26257 (SQL) between nodes and from application
- [ ] **Firewall rules** allow port 8080 (DB Console) from admin networks only
- [ ] **DNS** or service discovery configured for client connections
- [ ] **Inter-node latency** verified < 10ms within a region

## Security

- [ ] **TLS certificates** generated and deployed (no `--insecure`)
- [ ] **CA key** stored securely (not on cluster nodes)
- [ ] **Certificate expiry** > 1 year (set calendar reminder for renewal)
- [ ] **Root password** set or root client cert created
- [ ] **SQL users** created with appropriate roles (not using root for applications)
- [ ] **Enterprise license** installed (if using enterprise features)

### Verify Certificates

```sql
SELECT node_id,
  to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ AS node_cert_expires,
  to_timestamp((metrics->>'security.certificate.expiration.ca')::FLOAT)::TIMESTAMPTZ AS ca_cert_expires
FROM crdb_internal.kv_node_status ORDER BY node_id;
```

## Cluster Settings

- [ ] `kv.rangefeed.enabled = true`
- [ ] `sql.stats.automatic_collection.enabled = true`
- [ ] `admission.kv.enabled = true`
- [ ] `sql.defaults.idle_in_transaction_session_timeout = '300s'`
- [ ] `sql.defaults.statement_timeout = '30s'`
- [ ] `diagnostics.reporting.enabled` — set based on your policy

### Verify Settings

```sql
SELECT variable, value FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable IN (
  'kv.rangefeed.enabled',
  'sql.stats.automatic_collection.enabled',
  'admission.kv.enabled',
  'sql.defaults.idle_in_transaction_session_timeout',
  'sql.defaults.statement_timeout',
  'server.time_until_store_dead'
) ORDER BY variable;
```

## Application Readiness

- [ ] **Connection pooling** configured (PgBouncer, HikariCP, pgx pool, etc.)
- [ ] **Connection retry logic** with exponential backoff
- [ ] **Transaction retry logic** for serialization errors (SQLSTATE 40001)
- [ ] **Application uses `application_name`** in connection string for debugging
- [ ] **Connection string** uses load balancer address (not individual nodes)
- [ ] **Schema has primary keys** on all tables
- [ ] **Indexes** created for common query patterns

### Verify Schema

```sql
-- Tables without primary keys (bad for performance)
SELECT table_catalog AS database, table_schema AS schema, table_name
FROM information_schema.tables t
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('crdb_internal', 'information_schema', 'pg_catalog', 'pg_extension')
  AND NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints tc
    WHERE tc.table_name = t.table_name
      AND tc.table_schema = t.table_schema
      AND tc.constraint_type = 'PRIMARY KEY'
  );
```

## Monitoring and Alerting

- [ ] **DB Console** accessible and bookmarked (port 8080)
- [ ] **Prometheus** scraping `/_status/vars` from all nodes
- [ ] **Alerts configured** for:
  - Node down
  - Storage utilization > 70%
  - Certificate expiring within 90 days
  - Under-replicated ranges
  - P99 latency exceeding SLO
  - Failed jobs
- [ ] **Log aggregation** configured (cockroach logs → your logging platform)
- [ ] **Backup schedule** configured and tested

### Verify Monitoring

```sql
-- Confirm all nodes reachable
SELECT node_id, address FROM crdb_internal.gossip_nodes ORDER BY node_id;

-- Confirm ranges healthy
SELECT CASE WHEN array_length(replicas, 1) >= 3 THEN 'fully_replicated'
            ELSE 'under_replicated' END AS status, COUNT(*)
FROM crdb_internal.ranges_no_leases GROUP BY 1;
```

## Operational Readiness

- [ ] **Runbook** documented for common operations (node restart, drain, decommission)
- [ ] **On-call rotation** established
- [ ] **Upgrade plan** documented (which version, when, who)
- [ ] **Backup restoration** tested (restore to a test cluster)
- [ ] **Failover tested** (kill a node, verify cluster remains available)

## Final Verification

Run this consolidated query to verify production readiness:

```sql
SELECT 'node_count' AS check,
  CASE WHEN COUNT(*) >= 3 THEN 'PASS (' || COUNT(*) || ' nodes)'
       ELSE 'FAIL: need 3+ nodes' END AS result
FROM crdb_internal.gossip_nodes WHERE is_live = true
UNION ALL
SELECT 'all_nodes_same_version',
  CASE WHEN COUNT(DISTINCT build_tag) = 1
       THEN 'PASS (' || MIN(build_tag) || ')'
       ELSE 'FAIL: ' || COUNT(DISTINCT build_tag) || ' versions' END
FROM crdb_internal.gossip_nodes
UNION ALL
SELECT 'storage_healthy',
  CASE WHEN MIN(available::FLOAT / capacity::FLOAT) > 0.40 THEN 'PASS'
       ELSE 'FAIL: node above 60% utilization' END
FROM crdb_internal.kv_store_status
UNION ALL
SELECT 'ranges_healthy',
  CASE WHEN COUNT(*) FILTER (WHERE array_length(replicas, 1) < 3) = 0 THEN 'PASS'
       ELSE 'FAIL: under-replicated ranges' END
FROM crdb_internal.ranges_no_leases
UNION ALL
SELECT 'certs_valid',
  CASE WHEN MIN(to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ)
            > now() + INTERVAL '90 days' THEN 'PASS'
       ELSE 'WARN: cert expiring within 90 days' END
FROM crdb_internal.kv_node_status;
```

# Production Readiness Checklist

Comprehensive checklist for verifying a CockroachDB Self-Hosted cluster is ready for production workloads. Also useful for periodic operational reviews.

## Infrastructure Readiness

### Hardware Requirements

| Component | Minimum (Dev/Test) | Recommended (Production) |
|-----------|-------------------|--------------------------|
| Nodes | 3 | 3+ (odd numbers preferred) |
| CPU per node | 4 vCPUs (non-burstable) | 8+ vCPUs (non-burstable) |
| RAM per node | 16 GB | 32+ GB |
| Storage per node | 150 GB SSD | 500+ GB NVMe SSD |
| Network | 1 Gbps | 10 Gbps |

**Critical:** Never use burstable instances (AWS t-series, GCP e2-micro/small) for production. CPU throttling causes latency spikes and instability.

### Memory Configuration

CockroachDB memory formula: `(2 * --max-sql-memory) + --cache <= 75-80% of total RAM`

Default: `--cache=128MiB`, `--max-sql-memory=128MiB` (too low for production).

Recommended: `--cache=.25` (25% of RAM), `--max-sql-memory=.25` (25% of RAM).

```sql
-- Verify memory settings
SHOW CLUSTER SETTING sql.distsql.temp_storage.workmem;
```

### Clock Synchronization

CockroachDB requires clocks synchronized within 500ms (default `--max-offset`). Use NTP or chrony.

```bash
# Check clock offset
cockroach debug time-series --host=<node-address> --certs-dir=<certs-dir>
```

### Disk Verification

```sql
-- Storage capacity and utilization
SELECT node_id,
  ROUND(capacity / 1073741824.0, 2) AS total_gb,
  ROUND(available / 1073741824.0, 2) AS available_gb,
  ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

- All nodes should have SSDs (check IOPS if using cloud volumes)
- Utilization should be below 60% to allow for growth and rebalancing
- Ballast file should exist: `ls <store-path>/auxiliary/EMERGENCY_BALLAST`

## Cluster Settings Readiness

```sql
-- Production-critical settings assessment
SELECT variable, value, default_value,
  CASE WHEN value != default_value THEN 'CUSTOMIZED' ELSE 'DEFAULT' END AS status
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable IN (
  'kv.rangefeed.enabled',
  'sql.stats.automatic_collection.enabled',
  'server.time_until_store_dead',
  'admission.kv.enabled',
  'gc.ttlseconds',
  'sql.defaults.idle_in_transaction_session_timeout',
  'sql.defaults.statement_timeout',
  'diagnostics.reporting.enabled',
  'cluster.preserve_downgrade_option'
) ORDER BY variable;
```

### Recommended Production Settings

| Setting | Recommended | Why |
|---------|------------|-----|
| `kv.rangefeed.enabled` | `true` | Required for CDC and schema changes |
| `sql.stats.automatic_collection.enabled` | `true` | Query optimizer depends on statistics |
| `admission.kv.enabled` | `true` | Prevents overload under stress |
| `sql.defaults.idle_in_transaction_session_timeout` | `300s` | Prevents idle transactions from holding locks |
| `sql.defaults.statement_timeout` | `30s` | Prevents runaway queries |

## Security Readiness

### TLS Certificates

```sql
-- Certificate expiration check
SELECT node_id,
  to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ AS node_cert_expires,
  to_timestamp((metrics->>'security.certificate.expiration.ca')::FLOAT)::TIMESTAMPTZ AS ca_cert_expires,
  CASE WHEN to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ
            < now() + INTERVAL '90 days' THEN 'RENEW SOON'
       ELSE 'OK' END AS status
FROM crdb_internal.kv_node_status ORDER BY node_cert_expires;
```

### Enterprise License

```sql
-- License status (Self-Hosted only)
SELECT value FROM [SHOW CLUSTER SETTING cluster.organization];
SELECT value FROM [SHOW CLUSTER SETTING enterprise.license];
```

If using enterprise features (backup, CDC, encryption at rest, multi-region), a valid enterprise license is required.

## Application Readiness

### Connection Configuration

- [ ] Connection pooling configured (recommended: PgBouncer or application-level pool)
- [ ] Connection retry logic with exponential backoff implemented
- [ ] Transaction retry logic implemented (CockroachDB uses optimistic concurrency)
- [ ] Load balancer configured with health check on `/health?ready=1`
- [ ] Connection string uses `application_name` for debugging

### Schema Readiness

```sql
-- Tables without primary keys (performance concern)
SELECT table_catalog, table_schema, table_name
FROM information_schema.tables t
WHERE table_type = 'BASE TABLE'
  AND NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints tc
    WHERE tc.table_name = t.table_name
      AND tc.constraint_type = 'PRIMARY KEY'
  );
```

## Monitoring Readiness

- [ ] Prometheus metrics endpoint configured (`/_status/vars`)
- [ ] Alerting configured for: node down, certificate expiry, storage utilization, replication lag
- [ ] DB Console accessible and bookmarked
- [ ] Log aggregation configured (stdout/stderr → your logging platform)
- [ ] Backup schedule configured and verified

### Monitoring Verification

```sql
-- Verify DB Console is accessible
SELECT node_id, address FROM crdb_internal.gossip_nodes ORDER BY node_id;
-- DB Console runs on the same address, default port 8080
```

## Summary Assessment Query

Run this consolidated query for a quick production readiness score:

```sql
SELECT 'node_count' AS check,
  CASE WHEN COUNT(*) >= 3 THEN 'PASS' ELSE 'FAIL: need 3+ nodes' END AS result
FROM crdb_internal.gossip_nodes WHERE is_live = true
UNION ALL
SELECT 'all_nodes_live',
  CASE WHEN COUNT(*) FILTER (WHERE NOT is_live) = 0 THEN 'PASS'
       ELSE 'FAIL: ' || COUNT(*) FILTER (WHERE NOT is_live) || ' dead nodes' END
FROM crdb_internal.gossip_nodes
UNION ALL
SELECT 'single_version',
  CASE WHEN COUNT(DISTINCT build_tag) = 1 THEN 'PASS'
       ELSE 'WARN: ' || COUNT(DISTINCT build_tag) || ' versions' END
FROM crdb_internal.gossip_nodes
UNION ALL
SELECT 'storage_healthy',
  CASE WHEN MIN(available::FLOAT / capacity::FLOAT) > 0.40 THEN 'PASS'
       WHEN MIN(available::FLOAT / capacity::FLOAT) > 0.20 THEN 'WARN: node above 80% utilization'
       ELSE 'FAIL: node above 80% utilization' END
FROM crdb_internal.kv_store_status
UNION ALL
SELECT 'replication_healthy',
  CASE WHEN COUNT(*) FILTER (WHERE array_length(replicas, 1) < 3) = 0 THEN 'PASS'
       ELSE 'FAIL: ' || COUNT(*) FILTER (WHERE array_length(replicas, 1) < 3) || ' under-replicated ranges' END
FROM crdb_internal.ranges_no_leases
UNION ALL
SELECT 'certs_valid',
  CASE WHEN MIN(to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ) > now() + INTERVAL '90 days' THEN 'PASS'
       WHEN MIN(to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ) > now() THEN 'WARN: cert expiring within 90 days'
       ELSE 'FAIL: cert expired' END
FROM crdb_internal.kv_node_status;
```

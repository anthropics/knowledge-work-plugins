# Storage Management

Storage monitoring and management for CockroachDB Self-Hosted deployments.

## Storage Monitoring Queries

### Current Utilization

```sql
SELECT node_id, store_id,
  ROUND(capacity / 1073741824.0, 2) AS total_gb,
  ROUND(used / 1073741824.0, 2) AS used_gb,
  ROUND(available / 1073741824.0, 2) AS available_gb,
  ROUND((1 - available::FLOAT / capacity::FLOAT) * 100, 2) AS utilization_pct
FROM crdb_internal.kv_store_status ORDER BY node_id;
```

### Storage Utilization Thresholds

| Utilization | Status | Action |
|-------------|--------|--------|
| < 60% | Healthy | No action needed |
| 60-70% | Watch | Plan capacity addition |
| 70-80% | Warning | Add nodes or increase disk size |
| > 80% | Critical | Immediate capacity addition required |
| > 90% | Emergency | Risk of writes being rejected |

CockroachDB uses a ballast file (default 1% of disk or 1GB, whichever is smaller) as emergency reserve. At extreme utilization, the node may refuse writes.

## Ballast Files

Ballast files reserve emergency disk space. If a node runs out of disk, the ballast file can be deleted to free space for recovery.

**Check ballast:**
```bash
ls -lh <store-path>/auxiliary/EMERGENCY_BALLAST
```

**Create or resize ballast:**
```bash
cockroach debug ballast <store-path>/auxiliary/EMERGENCY_BALLAST --size=1GiB
```

**Recommended:** 1GB or 1% of disk, whichever is larger, for production clusters.

## GC TTL and Storage

The `gc.ttlseconds` setting (default 90000 = 25 hours) controls how long MVCC revisions are retained. Lowering this reduces storage but limits backup and AS OF SYSTEM TIME query windows.

```sql
-- Check current GC TTL
SHOW ZONE CONFIGURATION FOR RANGE default;

-- Reduce GC TTL to save storage (minimum recommended: 14400 = 4 hours)
ALTER RANGE default CONFIGURE ZONE USING gc.ttlseconds = 14400;

-- Check per-zone GC TTL overrides
SHOW ZONE CONFIGURATIONS;
```

## Large Table Management

```sql
-- Largest tables by size
SELECT t.name AS table_name,
       count(r.range_id) AS range_count,
       sum(r.range_size) AS total_bytes
FROM crdb_internal.tables t
JOIN crdb_internal.ranges r ON r.table_id = t.table_id
WHERE t.database_name = current_database()
GROUP BY t.name
ORDER BY total_bytes DESC NULLS LAST
LIMIT 20;

-- Range distribution per table
SELECT table_name, range_count
FROM [SHOW RANGES FROM DATABASE <database>]
ORDER BY range_count DESC;
```

## Disk Recommendations

| Aspect | Recommendation |
|--------|---------------|
| Type | NVMe SSD or equivalent (no HDDs, no network-attached unless SSD-backed) |
| IOPS | Minimum 500 IOPS per node; 3000+ for write-heavy workloads |
| Throughput | Minimum 100 MB/s sequential |
| Filesystem | ext4 or XFS |
| Mount options | `noatime,nobarrier` (if UPS-backed) |
| Multiple stores | Supported but single large SSD is simpler |

## Cloud Provider Disk Types

| Provider | Recommended | Acceptable | Avoid |
|----------|------------|------------|-------|
| AWS | gp3 (3000+ IOPS), io2 | gp2 | st1, sc1 |
| GCP | pd-ssd | pd-balanced | pd-standard |
| Azure | Premium SSD v2, Ultra | Premium SSD | Standard HDD/SSD |

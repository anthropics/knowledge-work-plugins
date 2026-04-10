# Monitoring and Concurrency Testing Reference

Detailed guidance for testing application behavior under concurrency and monitoring CockroachDB for performance and contention issues.

## Testing Under Concurrency

Single-user correctness is not sufficient. Test with realistic concurrency to surface retries, hotspots, contention, and workload-specific bottlenecks.

### Workload Simulation

```bash
cockroach workload init bank 'postgresql://root@localhost:26257?sslmode=disable'
cockroach workload run bank --concurrency=64 --duration=10m
```

### Python Multithreading Simulation

```python
import threading
from myapp import execute_transaction

threads = []
for _ in range(50):
    t = threading.Thread(target=execute_transaction)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

### Contention Inspection

```sql
SELECT *
FROM crdb_internal.transaction_contention_events
ORDER BY contention_duration DESC
LIMIT 10;
```

### Minimum Validation Checklist

- Run concurrent workload tests
- Inspect `crdb_internal.transaction_contention_events`
- Review DB Console SQL Activity Statements view
- Use `EXPLAIN` and `EXPLAIN ANALYZE` on critical queries
- Verify retry logic and idempotency in the application path

**When to test:** Before launching high-volume workloads, after schema or key redesigns, when adding regions, and during release load testing.

## Monitoring for Performance and Contention

Actively monitor query latency, contention, retries, and data distribution. Regular inspection detects early warning signs such as full table scans, long-running transactions, lock waits, and hot ranges.

### Explain Plans

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 'abc123';
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 'abc123';
```

### Live Contention Query

```sql
WITH waits AS (
  SELECT
    lh.database_name, lh.schema_name, lh.table_name, lh.index_name,
    lh.lock_key_pretty, lh.lock_key,
    lh.txn_id AS blocking_txn_id,
    lw.txn_id AS waiting_txn_id
  FROM crdb_internal.cluster_locks AS lh
  JOIN crdb_internal.cluster_locks AS lw
    ON lh.lock_key = lw.lock_key
  WHERE lh.granted = true
    AND lw.granted = false
)
SELECT
  w.database_name, w.schema_name, w.table_name, w.index_name,
  w.lock_key_pretty,
  w.blocking_txn_id,
  qh.query AS blocking_sql,
  w.waiting_txn_id,
  qw.query AS waiting_sql
FROM waits AS w
LEFT JOIN crdb_internal.cluster_queries AS qh
  ON qh.txn_id = w.blocking_txn_id
LEFT JOIN crdb_internal.cluster_queries AS qw
  ON qw.txn_id = w.waiting_txn_id
ORDER BY w.table_name, w.index_name, w.lock_key_pretty;
```

### Key Visualizer

Use the DB Console heatmap to identify hot ranges, index skew, and uneven distribution.

### Key Prometheus Metrics

- `sql.transactions.retries` — retry frequency
- `sql.transactions.duration` — transaction duration distribution
- `sql.distsql.flows.total` — distributed SQL flow count
- `kv.range.write_bytes_per_second` — write throughput per range
- `kv.range.requests.slow.latch` — slow latch acquisitions indicating contention

### External Monitoring Integration

Integrate with Prometheus and Grafana to build dashboards tracking the metrics above. Set alerts on retry rate spikes, p99 latency increases, and hot range detection.

## References

- [Performance Tuning Guide](https://www.cockroachlabs.com/docs/stable/performance-best-practices-overview)
- [Make Queries Fast](https://www.cockroachlabs.com/docs/stable/make-queries-fast)
- [Troubleshooting CockroachDB Performance](https://www.mindfulchase.com/explore/troubleshooting-tips/databases/troubleshooting-cockroachdb-performance-in-enterprise-deployments.html)

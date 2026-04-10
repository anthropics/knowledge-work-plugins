# Detailed Drain Mechanics

## Drain Phases

When a node drain is initiated (via `cockroach node drain` or `SIGTERM`), the node progresses through the following phases in order:

### Phase 1: Unready

The node marks itself as "not ready" for new connections. This signals load balancers and connection pools to stop routing new traffic to the node.

- The node's health endpoint (`/health?ready=1`) begins returning a non-200 status code.
- Load balancers with health checks will remove the node from their rotation.
- **Duration**: Controlled by `server.shutdown.drain_wait`.
- **Purpose**: Provides a window for load balancers to detect the node is draining and stop sending new connections before active connections are interrupted.

### Phase 2: Lease Transfer

The node transfers all range leases it holds to other nodes. Leases are the mechanism that determines which node serves reads and coordinates writes for a given range of data.

- Each lease is transferred individually to a suitable replica on another node.
- The transfer target is chosen based on locality, load, and replica availability.
- **Duration**: Controlled by `server.shutdown.lease_transfer_iteration.timeout` per iteration. The node makes multiple passes until all leases are transferred or the timeout expires.
- **Purpose**: Ensures no range leadership is lost, preventing temporary unavailability for reads/writes on those ranges.

### Phase 3: Connection Drain

The node stops accepting new SQL connections and begins draining existing connections.

- New SQL connection attempts are rejected.
- Existing connections with no active queries are closed.
- Connections with active queries are allowed to continue until they complete or the timeout expires.
- **Duration**: Controlled by `server.shutdown.query_wait`.
- **Purpose**: Provides a grace period for in-flight queries to finish without interruption.

### Phase 4: Query Completion

Final phase where remaining queries are given time to complete.

- Queries still running when this phase ends are forcefully canceled.
- After all queries are canceled, all remaining connections are closed.
- The node process can then safely exit.

---

## Timeout Settings

| Setting | Default | Description |
|---|---|---|
| `server.shutdown.drain_wait` | `0s` | Time to wait after marking the node as unready before proceeding with lease transfers. Set this to at least the health check interval of your load balancer (e.g., `15s` or `30s`) so the LB has time to stop routing traffic. |
| `server.shutdown.query_wait` | `10s` | Time to wait for active queries to complete during connection drain. Queries exceeding this are canceled. Set based on your longest expected legitimate query. This value is used twice: once during connection drain and once during query completion. |
| `server.shutdown.lease_transfer_iteration.timeout` | `5s` | Timeout for each iteration of lease transfers. The drain process makes multiple iterations. If leases remain after all iterations, the node proceeds with shutdown anyway. |

### Total Drain Time

The total maximum drain time is approximately:

```
drain_wait + (lease_transfer_iterations * lease_transfer_iteration.timeout) + (2 * query_wait)
```

The `query_wait` is applied twice: once during the connection drain phase (to let active queries finish) and once during the final query completion phase.

### Recommended Production Values

```sql
-- Allow load balancer health checks to detect drain
SET CLUSTER SETTING server.shutdown.drain_wait = '15s';

-- Allow queries up to 30 seconds to complete
SET CLUSTER SETTING server.shutdown.query_wait = '30s';

-- Allow up to 5 seconds per lease transfer iteration
SET CLUSTER SETTING server.shutdown.lease_transfer_iteration.timeout = '5s';
```

For workloads with long-running queries, increase `query_wait`:

```sql
SET CLUSTER SETTING server.shutdown.query_wait = '120s';
```

---

## Monitoring During Drain

### Connection Count

Monitor active connections on the draining node to track drain progress:

```sql
-- Count active sessions on a specific node
SELECT count(*) AS active_sessions
FROM [SHOW SESSIONS]
WHERE node_id = <draining_node_id>;

-- Detailed view of active sessions
SELECT
  session_id,
  node_id,
  user_name,
  client_address,
  application_name,
  active_queries,
  last_active_query,
  status
FROM [SHOW SESSIONS]
WHERE node_id = <draining_node_id>
ORDER BY status, last_active_query;
```

### Lease Count

Monitor lease count on the draining node:

```sql
-- Count leases held by the draining node
SELECT count(*) AS lease_count
FROM crdb_internal.ranges
WHERE lease_holder = <draining_node_id>;

-- Track lease migration progress (run repeatedly)
SELECT
  lease_holder,
  count(*) AS ranges
FROM crdb_internal.ranges
GROUP BY lease_holder
ORDER BY lease_holder;
```

### Drain Progress Output

The `cockroach node drain` command outputs progress information:

```bash
cockroach node drain <node_id> --certs-dir=/path/to/certs --host=<any-other-node>:26257
```

Example output:

```
node is draining... remaining: 512
node is draining... remaining: 256
node is draining... remaining: 64
node is draining... remaining: 8
node is draining... remaining: 0 (complete)
ok
```

The "remaining" count represents the number of range leases still held by the draining node.

---

## What Happens to In-Flight Queries

| Query State | Behavior |
|---|---|
| Query not yet started | Rejected. Client receives a connection error. |
| Query actively executing | Allowed to continue until `query_wait` expires. If still running after timeout, the query is canceled and the client receives an error. |
| Query in a transaction (not idle) | Allowed to continue until `query_wait` expires. Transaction is rolled back if canceled. |
| Idle in transaction | Connection is closed. Transaction is rolled back. |
| Query completed, results being sent | Allowed to complete result delivery. |

**Client impact**: When a query is forcefully canceled, the client receives an error such as `server is shutting down` or `query execution canceled due to node shutdown`. Applications should be designed to retry on these errors.

**Transaction safety**: Canceled transactions are always rolled back. There is no risk of partial commits. CockroachDB's transaction model ensures atomicity even during node shutdown.

---

## Drain vs SIGTERM vs SIGKILL Comparison

| Signal / Command | Graceful | Lease Transfer | Query Drain | Connection Drain | Recovery Required |
|---|---|---|---|---|---|
| `cockroach node drain` | Yes | Yes, full | Yes, respects `query_wait` | Yes, respects `drain_wait` | No |
| `SIGTERM` | Yes | Yes, full | Yes, respects `query_wait` | Yes, respects `drain_wait` | No |
| `SIGINT` (Ctrl+C) | Yes | Yes, full | Yes, respects `query_wait` | Yes, respects `drain_wait` | No |
| `SIGQUIT` | Partial | Abbreviated | Abbreviated | Abbreviated | Possible |
| `SIGKILL` (kill -9) | No | No | No | No | Yes, Raft recovery |
| Process crash (OOM, etc.) | No | No | No | No | Yes, Raft recovery |

### Detailed Behavior

- **`cockroach node drain` + process stop**: The recommended approach. Drain first, then stop the process. Gives maximum control and visibility into drain progress.

  ```bash
  # Step 1: Drain
  cockroach node drain <node_id> --certs-dir=/path/to/certs --host=<other-node>:26257

  # Step 2: Stop the process
  kill <pid>
  # or
  systemctl stop cockroachdb
  ```

- **`SIGTERM`**: CockroachDB handles SIGTERM by initiating the same drain procedure internally. Equivalent to drain + stop in a single operation, but you cannot observe drain progress externally.

- **`SIGKILL` (kill -9)**: The process is terminated immediately by the OS. No cleanup occurs. The remaining nodes will detect the dead node after `server.time_until_store_dead` and begin up-replicating data. In-flight transactions on the killed node are resolved via Raft consensus on other replicas. No data is lost (assuming replication factor >= 3) but there is a period of degraded performance during recovery.

---

## Advanced Drain Monitoring Queries

### Active Sessions on Target Node with Query Details

```sql
SELECT
  session_id,
  user_name,
  client_address,
  application_name,
  active_queries,
  num_txns_executed,
  CASE
    WHEN status = 'ACTIVE' THEN 'Running query'
    WHEN status = 'IDLE' THEN 'Connected, no query'
    WHEN status = 'IDLE IN TRANSACTION' THEN 'In open transaction'
    ELSE status
  END AS session_status,
  (now() - session_start)::STRING AS session_duration
FROM [SHOW SESSIONS]
WHERE node_id = <draining_node_id>
ORDER BY
  CASE status
    WHEN 'ACTIVE' THEN 0
    WHEN 'IDLE IN TRANSACTION' THEN 1
    ELSE 2
  END,
  session_start;
```

### Lease Count Tracking Over Time

Run this repeatedly (e.g., every 5 seconds) to monitor lease migration progress:

```sql
SELECT
  now()::STRING AS check_time,
  count(*) AS total_leases,
  count(*) FILTER (WHERE lease_holder = <draining_node_id>) AS draining_node_leases,
  count(*) FILTER (WHERE lease_holder != <draining_node_id>) AS other_node_leases
FROM crdb_internal.ranges;
```

### Identify Long-Running Queries Blocking Drain

```sql
SELECT
  query_id,
  node_id,
  user_name,
  application_name,
  query,
  phase,
  (now() - start)::STRING AS duration
FROM [SHOW QUERIES]
WHERE node_id = <draining_node_id>
ORDER BY start ASC;
```

### Pre-Drain Health Check

Run before initiating drain to understand what to expect:

```sql
SELECT
  node_id,
  count(*) AS lease_count,
  (SELECT count(*) FROM [SHOW SESSIONS] WHERE node_id = n.node_id) AS session_count
FROM crdb_internal.ranges AS r
JOIN crdb_internal.gossip_nodes AS n ON r.lease_holder = n.node_id
WHERE n.node_id = <target_node_id>
GROUP BY node_id;
```

### Post-Drain Verification

After drain completes, verify the node has no remaining responsibilities:

```sql
-- Confirm zero leases
SELECT count(*) AS remaining_leases
FROM crdb_internal.ranges
WHERE lease_holder = <drained_node_id>;

-- Confirm zero sessions
SELECT count(*) AS remaining_sessions
FROM [SHOW SESSIONS]
WHERE node_id = <drained_node_id>;

-- Check node status
SELECT
  n.node_id,
  n.address,
  n.is_live,
  l.decommissioning,
  l.membership
FROM crdb_internal.gossip_nodes n
JOIN crdb_internal.gossip_liveness l USING (node_id)
WHERE n.node_id = <drained_node_id>;
```

# Node-Level Settings (cockroach start Flags)

Node-level settings are configured via `cockroach start` flags and require a node restart to change. They cannot be modified at runtime via SQL.

## Memory Allocation Formula

The critical constraint for memory-related flags is:

```
(2 * --max-sql-memory) + --cache <= 80% of total RAM
```

The remaining 20% is reserved for the operating system, Go runtime overhead, CGo allocations, and other non-managed memory usage. Violating this formula risks OOM kills under load.

**Example for a 64 GB node:**

```
80% of 64 GB = 51.2 GB
--cache = 16 GB
--max-sql-memory = 16 GB
(2 * 16 GB) + 16 GB = 48 GB < 51.2 GB  (OK)
```

## Flag Reference

| Flag | Purpose | Recommended Production Value | Requires Restart |
|---|---|---|---|
| `--cache` | Size of the in-memory storage engine (Pebble) block cache. Caches frequently-read data blocks to reduce disk reads. | 25-35% of total RAM (e.g., `16GiB` on a 64 GB node). Can also specify as a fraction: `0.25`. | Yes |
| `--max-sql-memory` | Maximum memory allocated for SQL query execution, including sorts, hash joins, and result buffering. | 25% of total RAM (e.g., `16GiB` on a 64 GB node). Can also specify as a fraction: `0.25`. | Yes |
| `--max-offset` | Maximum allowed clock offset between nodes. Nodes exceeding this offset are rejected from the cluster. | `500ms` (default). Only increase if running on infrastructure with poor clock synchronization. Must be identical across all nodes. | Yes |
| `--locality` | Describes the node's location in a hierarchical topology. Used for data placement, lease preferences, and survival goals. | `--locality=region=us-east-1,zone=us-east-1a` (match your cloud provider topology). Must follow the same key hierarchy across all nodes. | Yes |
| `--store` | Path to the on-disk storage directory and optional store attributes. | `--store=path=/data/cockroach,attrs=ssd`. Use a dedicated volume (not the OS disk). For multiple stores: specify `--store` multiple times. | Yes |
| `--log-dir` | Directory for log file output. Defaults to the first store's `logs` subdirectory. | A dedicated partition or volume separate from the store, e.g., `--log-dir=/var/log/cockroach`. Prevents log growth from consuming store disk space. | Yes |
| `--join` | Comma-separated list of host:port addresses for existing nodes to join the cluster. | List 3-5 nodes (ideally the initial seed nodes). Example: `--join=node1:26257,node2:26257,node3:26257`. All nodes should use the same join list. | Yes |
| `--listen-addr` | Address and port for intra-cluster (node-to-node) RPC communication. | `--listen-addr=:26257` to bind to all interfaces on the default port, or a specific interface address for security. | Yes |
| `--sql-addr` | Address and port for SQL client connections. Defaults to `--listen-addr` if not set. | `--sql-addr=:26257` (same as listen-addr by default). Use a separate port (e.g., `:26258`) if you want to isolate SQL traffic from RPC traffic on different network interfaces. | Yes |
| `--http-addr` | Address and port for the DB Console (Admin UI) HTTP endpoint. | `--http-addr=:8080`. Restrict to internal networks or use a reverse proxy for external access. Do not expose directly to the public internet. | Yes |

## Additional Considerations

### Store Configuration

Multiple stores per node are supported but generally not recommended in cloud environments where you can scale horizontally instead:

```bash
cockroach start \
  --store=path=/mnt/ssd1,attrs=ssd \
  --store=path=/mnt/ssd2,attrs=ssd \
  ...
```

### Locality Best Practices

Consistent locality key hierarchies are critical for correct data placement:

```bash
# Correct - all nodes use the same key hierarchy
--locality=region=us-east-1,zone=us-east-1a
--locality=region=us-west-2,zone=us-west-2b

# Incorrect - inconsistent keys cause placement issues
--locality=region=us-east-1,zone=us-east-1a
--locality=datacenter=us-west-2,rack=2b
```

### Clock Synchronization

The `--max-offset` value must be the same on all nodes. CockroachDB will refuse to start a node if its clock offset from other nodes exceeds this value. Ensure NTP or a similar time synchronization service is running on all nodes. On cloud VMs, the cloud provider's time sync service (e.g., Amazon Time Sync, Google NTP) is generally sufficient.

### Applying Changes

Since all node-level settings require a restart, follow the drain-then-restart procedure:

1. Drain the node (`cockroach node drain`).
2. Stop the process.
3. Update the start flags.
4. Restart the node.

See the draining-nodes-for-maintenance skill for the full drain procedure.

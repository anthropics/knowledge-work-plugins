# Safety Guide: Draining Nodes for Maintenance

## Risk Matrix

| Operation | Risk Level | Reversible? | Impact |
|-----------|-----------|-------------|--------|
| Pre-drain SQL queries | None | N/A | Read-only diagnostics |
| `cockroach node drain` | Medium | No (drain cannot be canceled once started) | Moves leases and connections off node |
| `systemctl stop cockroachdb` | Medium | Yes (restart) | Node becomes unavailable |
| `kill -TERM` (SIGTERM) | Medium | Yes (restart) | Graceful shutdown |
| `kill -9` (SIGKILL) | High | Yes (restart) | Ungraceful shutdown; may cause brief unavailability |
| `kubectl delete pod` | Low | Yes (pod recreated) | Operator handles drain automatically |
| Configure maintenance window (ADV/BYOC) | Low | Yes (reconfigure) | Changes patch schedule |
| Defer patches (ADV/BYOC) | Low | Yes (remove deferral) | Delays security fixes |

## Self-Hosted Safety Rules

### Before Draining

1. **Only drain one node at a time** — draining multiple nodes simultaneously risks under-replication and data unavailability
2. **Verify no other nodes are draining** — check `crdb_internal.gossip_liveness` for `draining = true`
3. **All ranges must be fully replicated** — never drain a node when ranges are already under-replicated
4. **No bulk jobs in progress** — backups, restores, imports, and schema changes should complete first

### During Drain

- Drain **cannot be canceled** once initiated — the node will complete the drain process
- Existing connections are closed after in-flight queries complete
- New SQL connections are rejected immediately
- Leases transfer to other nodes (may take seconds to minutes)
- Load balancers detect the drained node via `/health?ready=1` returning an error

### Stop and Restart

- **Always use SIGTERM** — never SIGKILL unless the process is unresponsive after 60+ seconds
- SIGTERM triggers a graceful shutdown sequence
- SIGKILL causes immediate termination — replicas become unavailable until other nodes detect the failure
- After restart, monitor lease rebalancing (may take 5-10 minutes)

### Application Requirements

- Applications **must** have connection retry logic with exponential backoff
- Connection pools should handle `connection refused` and `server is shutting down` errors
- Load balancer health check should use `/health?ready=1` endpoint

## Advanced/BYOC Safety Rules

### Maintenance Windows

- **Single-node clusters experience downtime** during maintenance windows
- Multi-node clusters remain available with reduced capacity
- Performance may be slightly degraded during rolling restarts
- Schedule during lowest-traffic periods

### Patch Deferral

- Deferring patches delays security fixes — evaluate CVE impact before deferring
- Maximum deferral: 90 days
- Deferred patches still apply at end of deferral period

## Standard/Basic Safety

- Maintenance is fully managed — no customer action needed
- Applications should implement connection retry for brief latency variations
- No risk of customer-caused maintenance issues

## Common Mistakes

| Mistake | Consequence | Prevention |
|---------|------------|------------|
| Draining multiple nodes simultaneously | Under-replicated ranges, potential unavailability | Always drain one at a time; verify pre-drain |
| Using SIGKILL for routine maintenance | Abrupt disconnection, brief range unavailability | Use SIGTERM; only SIGKILL if unresponsive |
| Not updating load balancer | Traffic still sent to drained node | Use `/health?ready=1` health check |
| Draining during under-replication | Data unavailability risk | Check range health before draining |
| Changing cluster settings during maintenance | Unpredictable behavior | Complete maintenance before adjusting settings |
| Forgetting to restart after maintenance | Reduced cluster capacity | Verify node rejoin in gossip_liveness |

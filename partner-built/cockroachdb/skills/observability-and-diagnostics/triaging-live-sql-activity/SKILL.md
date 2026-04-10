---
name: triaging-live-sql-activity
description: Diagnoses live CockroachDB cluster performance issues by identifying long-running queries, busy sessions, and active transactions using SQL-only interfaces. Use when users report cluster slowness, high CPU, or need to find runaway queries and their source applications without DB Console access.
compatibility: Requires SQL access with VIEWACTIVITY or VIEWACTIVITYREDACTED cluster privilege for cluster-wide visibility.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Triaging Live SQL Activity

Diagnoses live cluster performance issues by identifying currently active long-running queries, busy sessions, and active transactions. Uses SQL-only interfaces (SHOW statements and `crdb_internal` views) to provide immediate triage without requiring DB Console, HTTP endpoints, or Prometheus access.

## When to Use This Skill

- Users report "the cluster is slow right now"
- High CPU or memory usage on cluster nodes
- Need to identify runaway queries or stuck transactions
- Want to find which applications/users are consuming resources
- Require immediate triage without DB Console access
- Need to generate SQL to cancel problematic sessions/queries

**For historical performance analysis:** Use [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) to analyze query patterns over time, identify slow fingerprints, and investigate trends without needing live queries.
**For transaction-level analysis:** Use [profiling-transaction-fingerprints](../profiling-transaction-fingerprints/SKILL.md) to analyze historical transaction retry patterns, commit latency trends, and statement composition.
**For background job monitoring:** Use [monitoring-background-jobs](../monitoring-background-jobs/SKILL.md) to monitor schema changes, backups, and automatic jobs that don't appear in SHOW CLUSTER STATEMENTS.

## Prerequisites

**Required SQL access:**
- Connection to any CockroachDB node
- For cluster-wide visibility: `VIEWACTIVITY` or `VIEWACTIVITYREDACTED` privilege
  - `VIEWACTIVITYREDACTED`: Redacts constants in other users' queries (recommended for privacy)
  - `VIEWACTIVITY`: Shows full query text for all users
  - Without these: Only see your own sessions/queries
- Basic understanding of SQL query execution
- (Optional) `CANCELQUERY` / `CANCELSESSION` privileges for cancellation operations

**Check your privileges:**
```sql
SHOW GRANTS ON ROLE <username>;
```

See [permissions reference](references/permissions.md) for detailed RBAC setup.

## Core Diagnostic Approach

CockroachDB provides SQL-only interfaces for live activity triage:

| Interface | Purpose | Cluster-wide? |
|-----------|---------|---------------|
| `SHOW CLUSTER STATEMENTS` | Currently executing queries | Yes (with VIEWACTIVITY) |
| `SHOW CLUSTER SESSIONS` | Active client sessions | Yes (with VIEWACTIVITY) |
| `crdb_internal.cluster_transactions` | In-progress transactions | Yes (with VIEWACTIVITY) |

**Triage workflow:**
1. Identify long-running queries (> 5-10 minutes)
2. Correlate to sessions and applications
3. Check transaction retry counts (high retries = contention)
4. Drill down by app/user/client
5. (Optional) Cancel runaway work

**Safety:** All diagnostic queries are read-only. Cancellation is opt-in with explicit warnings.

## Core Diagnostic Queries

### Long-Running Queries

Identify queries running longer than a specified threshold:

```sql
-- Queries running longer than 5 minutes
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT
  query_id,
  node_id,
  session_id,
  user_name,
  client_address,
  application_name,
  start,
  now() - start AS running_for,
  substring(query, 1, 200) AS query_preview,
  distributed,
  phase
FROM q
WHERE start < now() - INTERVAL '5 minutes'
ORDER BY start
LIMIT 50;
```

**Key columns:**
- `running_for`: How long the query has been executing
- `query_preview`: First 200 characters (protects against massive queries)
- `phase`: execution phase (preparing, executing, etc.)
- `distributed`: whether query spans multiple nodes

**Customizable thresholds:**
- Change `INTERVAL '5 minutes'` to `'10 minutes'`, `'30 seconds'`, etc.
- Adjust `LIMIT` based on cluster size and expected load

### Active Sessions

Find sessions with long-running active queries:

```sql
-- Sessions with active queries running > 5 minutes
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT
  node_id,
  session_id,
  user_name,
  client_address,
  application_name,
  status,
  active_query_start,
  now() - active_query_start AS active_query_for,
  substring(active_queries, 1, 200) AS active_queries_preview,
  substring(last_active_query, 1, 200) AS last_query_preview
FROM s
WHERE active_query_start IS NOT NULL
  AND active_query_start < now() - INTERVAL '5 minutes'
ORDER BY active_query_start
LIMIT 50;
```

**Key columns:**
- `active_query_for`: Duration of current active query
- `application_name`: Source application for drill-down
- `client_address`: Client IP/hostname for troubleshooting
- `status`: Session state (Idle, Active, etc.)

### Active Transactions

Identify long-running transactions (potential blockers):

```sql
-- Transactions running > 5 minutes
SELECT
  id AS txn_id,
  node_id,
  session_id,
  application_name,
  start,
  now() - start AS running_for,
  num_stmts,
  num_retries,
  num_auto_retries,
  substring(txn_string, 1, 200) AS txn_string_preview
FROM crdb_internal.cluster_transactions
WHERE start < now() - INTERVAL '5 minutes'
ORDER BY start
LIMIT 50;
```

**Key columns:**
- `num_retries` / `num_auto_retries`: High retry counts indicate contention
- `num_stmts`: Number of statements in transaction (large = potentially problematic)
- `txn_string`: Transaction fingerprint

**Production safety note:** `crdb_internal.cluster_transactions` is production-approved and safe for triage.

## Drill-Down by Application, User, or Client

Once you identify suspicious activity, drill down by filtering:

### Filter by Application

```sql
-- All activity from specific application
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, user_name, start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE application_name = 'payments-api'
ORDER BY start;
```

### Filter by User

```sql
-- All activity from specific user
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT session_id, application_name, client_address,
       active_query_start, substring(active_queries, 1, 200) AS active_queries_preview
FROM s
WHERE user_name = 'app_user'
  AND active_query_start IS NOT NULL
ORDER BY active_query_start;
```

### Filter by Client Address

```sql
-- All sessions from specific client IP
WITH s AS (SHOW CLUSTER SESSIONS)
SELECT session_id, user_name, application_name,
       status, substring(active_queries, 1, 200) AS active_queries_preview
FROM s
WHERE client_address LIKE '10.0.1.%'
ORDER BY active_query_start;
```

### Combined Filters

```sql
-- Long queries from specific app and user
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, node_id, start, now() - start AS running_for,
       substring(query, 1, 200) AS query_preview
FROM q
WHERE application_name = 'payments-api'
  AND user_name = 'app_user'
  AND start < now() - INTERVAL '10 minutes'
ORDER BY start;
```

## Safety Considerations

**Read-only operations:**
All diagnostic queries (`SHOW` statements, `crdb_internal.cluster_transactions`) are read-only and safe to run in production.

**Cancellation operations (opt-in):**

**CAUTION: Canceling queries/sessions terminates user work**

Only proceed if:
- You've confirmed the query/session is runaway or stuck
- You have authorization to interrupt user workloads
- You've notified stakeholders if appropriate
- You have `CANCELQUERY` or `CANCELSESSION` privileges

## Canceling Runaway Work (Opt-In)

### Cancel a Specific Query

```sql
-- 1. Identify the query_id from triage queries above
-- 2. Cancel it
CANCEL QUERY '<query_id>';
```

**Example:**
```sql
CANCEL QUERY '15f9e0e91f072f0f0000000000000001';
```

### Cancel an Entire Session

```sql
-- 1. Identify the session_id from triage queries above
-- 2. Cancel all queries in that session
CANCEL SESSION '<session_id>';
```

**Example:**
```sql
CANCEL SESSION '15f9e0e91f072f0f';
```

**Verification:**
After canceling, re-run the triage queries to confirm the query/session is gone.

**Required privileges:**
- `CANCELQUERY` system privilege to cancel queries
- `CANCELSESSION` system privilege to cancel sessions
- Admin role has both by default

See [permissions reference](references/permissions.md) for granting these privileges.

## Common Triage Workflows

### Workflow 1: "Cluster is slow" investigation

**Scenario:** Users report general slowness.

1. **Check for long-running queries:**
   ```sql
   -- Run the "Long-Running Queries" diagnostic
   -- Look for queries running > 5-10 minutes
   ```

2. **Identify source applications:**
   ```sql
   -- Group by application to find culprits
   WITH q AS (SHOW CLUSTER STATEMENTS)
   SELECT application_name, COUNT(*) AS num_queries,
          AVG(now() - start) AS avg_duration
   FROM q
   WHERE start < now() - INTERVAL '5 minutes'
   GROUP BY application_name
   ORDER BY num_queries DESC;
   ```

3. **Drill down into specific app:**
   ```sql
   -- Filter by top application from step 2
   -- Use "Filter by Application" query
   ```

4. **Decide on action:**
   - Contact app team to investigate query patterns
   - Cancel specific runaway queries if critical
   - Check for schema/index issues if queries are legitimate

### Workflow 2: Find high-retry transactions

**Scenario:** Suspect contention issues.

1. **Check for high retry counts:**
   ```sql
   SELECT application_name, AVG(num_retries) AS avg_retries,
          MAX(num_retries) AS max_retries, COUNT(*) AS num_txns
   FROM crdb_internal.cluster_transactions
   WHERE start < now() - INTERVAL '5 minutes'
   GROUP BY application_name
   HAVING AVG(num_retries) > 5
   ORDER BY avg_retries DESC;
   ```

2. **Investigate specific transactions:**
   ```sql
   -- Find transactions with >10 retries
   SELECT id, application_name, num_retries, num_stmts,
          substring(txn_string, 1, 200) AS txn_preview
   FROM crdb_internal.cluster_transactions
   WHERE num_retries > 10
   ORDER BY num_retries DESC;
   ```

3. **Next steps:**
   - Review transaction patterns for contention
   - Check for lock conflicts or hotspots
   - Consider schema changes to reduce contention

### Workflow 3: Identify resource hogs by user

**Scenario:** Need to attribute load to specific users.

1. **Count active queries per user:**
   ```sql
   WITH q AS (SHOW CLUSTER STATEMENTS)
   SELECT user_name, COUNT(*) AS num_active_queries,
          AVG(now() - start) AS avg_duration
   FROM q
   GROUP BY user_name
   ORDER BY num_active_queries DESC;
   ```

2. **Drill down to specific user's activity:**
   ```sql
   -- Use "Filter by User" query
   ```

3. **Take action:**
   - Contact user if unexpected load
   - Review user's query patterns
   - Cancel if clearly runaway

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `SHOW CLUSTER STATEMENTS` returns empty | No active queries, or insufficient privileges | Grant `VIEWACTIVITY` or `VIEWACTIVITYREDACTED`; verify cluster has active load |
| Query text shows `<hidden>` | Using `VIEWACTIVITYREDACTED` privilege | This is expected for privacy; use `VIEWACTIVITY` if full text needed |
| Can't cancel query: "permission denied" | Missing `CANCELQUERY` privilege | Grant `CANCELQUERY` system privilege to your user |
| `crdb_internal.cluster_transactions` slow | High transaction volume on cluster | Add filters (application_name, time threshold) to reduce result set |
| "relation does not exist" error | Typo in table name or old CockroachDB version | Verify you're using production-approved tables; check CockroachDB version compatibility |
| Triage queries themselves are slow | Cluster under extreme load | Use more aggressive filters (shorter time window, specific apps); consider canceling obvious runaway work first |

## Key Considerations

- **Privacy:** Use `VIEWACTIVITYREDACTED` instead of `VIEWACTIVITY` to protect sensitive query constants in multi-tenant environments
- **Performance impact:** Triage queries are read-only and lightweight, but avoid running them in tight loops during extreme load
- **LIMIT clause:** Always include `LIMIT` to prevent overwhelming output on large clusters
- **Time thresholds:** Adjust `INTERVAL` based on your workload (5 minutes is a reasonable default, but fast OLTP may need 30 seconds)
- **Cancellation is disruptive:** Only cancel queries/sessions after confirming they're problematic; coordinate with application teams when possible
- **Not for historical analysis:** These queries show current state only; for trends over time, use DB Console or Prometheus metrics
- **Production-approved sources:** Only use `SHOW CLUSTER STATEMENTS`, `SHOW CLUSTER SESSIONS`, and `crdb_internal.cluster_transactions` for production triage

## References

**Skill references:**
- [SQL query variations and examples](references/sql-queries.md)
- [RBAC and privilege setup](references/permissions.md)

**Related skills:**
- [profiling-statement-fingerprints](../profiling-statement-fingerprints/SKILL.md) - For historical performance pattern analysis and trend identification
- [profiling-transaction-fingerprints](../profiling-transaction-fingerprints/SKILL.md) - For historical transaction-level analysis including retry storms and commit latency

**Official CockroachDB Documentation:**
- [SHOW STATEMENTS](https://www.cockroachlabs.com/docs/stable/show-statements.html)
- [SHOW SESSIONS](https://www.cockroachlabs.com/docs/stable/show-sessions.html)
- [CANCEL QUERY](https://www.cockroachlabs.com/docs/stable/cancel-query.html)
- [CANCEL SESSION](https://www.cockroachlabs.com/docs/stable/cancel-session.html)
- [crdb_internal](https://www.cockroachlabs.com/docs/stable/crdb-internal.html)
- [VIEWACTIVITY privilege](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

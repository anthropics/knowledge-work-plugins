# SQL Queries for Audit Logging Configuration

This reference provides SQL queries for configuring, verifying, and managing audit logging on CockroachDB clusters.

## Checking Current Configuration

### All Audit-Related Settings

```sql
-- All cluster settings related to auditing
SELECT variable, value, description
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable LIKE '%audit%'
   OR variable LIKE '%slow_query%'
ORDER BY variable;
```

### Individual Setting Checks

```sql
-- User audit logging configuration
SHOW CLUSTER SETTING sql.log.user_audit;

-- Admin audit logging
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;

-- Slow query logging threshold
SHOW CLUSTER SETTING sql.log.slow_query.latency_threshold;
```

## Enabling Audit Logging

### Admin Audit Logging

```sql
-- Enable admin audit logging (captures all admin SQL statements)
SET CLUSTER SETTING sql.log.admin_audit.enabled = true;
```

### Role-Based Audit Logging

```sql
-- Audit all statements from a specific role
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL';

-- Audit multiple roles
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL
security_admin ALL
app_service_account READ';

-- Audit modes:
--   ALL   - All statements (SELECT, INSERT, UPDATE, DELETE, DDL)
--   READ  - SELECT statements only
--   WRITE - INSERT, UPDATE, DELETE statements only
--   NONE  - Disable auditing for this role (useful to exclude a role)
```

### Slow Query Logging

```sql
-- Log queries exceeding 1 second
SET CLUSTER SETTING sql.log.slow_query.latency_threshold = '1s';

-- Log queries exceeding 5 seconds
SET CLUSTER SETTING sql.log.slow_query.latency_threshold = '5s';

-- Log ALL queries (very high overhead — investigation only)
SET CLUSTER SETTING sql.log.slow_query.latency_threshold = '0';
```

## Creating Audit Roles

### Sensitive Data Access Role

```sql
-- Create a role for users who access sensitive tables
CREATE ROLE sensitive_data_reader;

-- Grant access to sensitive tables
GRANT SELECT ON TABLE customers TO sensitive_data_reader;
GRANT SELECT ON TABLE payments TO sensitive_data_reader;
GRANT SELECT ON TABLE user_pii TO sensitive_data_reader;

-- Assign users to the role
GRANT sensitive_data_reader TO app_user, analyst_user;

-- Enable auditing for this role
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL';
```

### Admin Operations Role

```sql
-- Create a role for users who perform admin operations
CREATE ROLE security_admin;

-- Grant admin-like privileges
GRANT SYSTEM MODIFYCLUSTERSETTING TO security_admin;

-- Assign users
GRANT security_admin TO ops_user;

-- Audit both roles
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL
security_admin ALL';
```

## Disabling Audit Logging

```sql
-- Disable user audit logging
SET CLUSTER SETTING sql.log.user_audit = '';

-- Disable admin audit logging
SET CLUSTER SETTING sql.log.admin_audit.enabled = false;

-- Reset slow query threshold to default
RESET CLUSTER SETTING sql.log.slow_query.latency_threshold;
```

## Verification Queries

### Verify Settings Are Active

```sql
-- Confirm all audit settings
SHOW CLUSTER SETTING sql.log.user_audit;
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;
SHOW CLUSTER SETTING sql.log.slow_query.latency_threshold;
```

### Generate Test Audit Events

```sql
-- Execute statements to test audit capture
CREATE TABLE audit_test (id INT PRIMARY KEY, data STRING);
INSERT INTO audit_test VALUES (1, 'test');
SELECT * FROM audit_test;
DROP TABLE audit_test;
```

After running these statements, check your log export destination to verify the events were captured.

## Notes

- Audit logs are written to CockroachDB log files, not queryable via SQL
- On CockroachDB Cloud, configure log export to deliver logs to your cloud provider's logging service
- Role-based audit logging requires CockroachDB 22.2+
- Changes to audit settings take effect immediately — no restart required
- Audit logging captures the SQL text, user, timestamp, and execution status

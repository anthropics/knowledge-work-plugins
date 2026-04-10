---
name: configuring-audit-logging
description: Configures SQL audit logging on CockroachDB clusters to capture security-relevant events including authentication, privilege changes, and sensitive data access. Use when enabling audit logging for compliance, setting up role-based audit policies, or verifying audit configuration.
compatibility: Requires admin role for cluster setting changes. Role-based audit logging available on CockroachDB 22.2+.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Configuring Audit Logging

Configures SQL audit logging on CockroachDB clusters to capture security-relevant events such as authentication attempts, privilege changes, DDL operations, and sensitive data access. Supports both cluster-wide audit settings and role-based audit policies for targeted logging.

## When to Use This Skill

- Enabling audit logging to meet SOC 2, HIPAA, or PCI DSS compliance requirements
- Setting up role-based audit policies for specific users or roles
- Verifying that audit logging is properly configured and capturing events
- Responding to a security audit finding about missing audit trails
- Investigating security incidents by reviewing audit log configuration

## Prerequisites

- **SQL access** with admin role (required to modify cluster settings)
- **CockroachDB version:** 22.2+ for role-based audit logging
- **Log export** configured for persistent audit trail (CockroachDB Cloud exports logs to your cloud provider)
- **Storage planning:** Audit logging increases log volume; plan for additional storage

**Check your access:**
```sql
-- Verify admin role
SELECT member FROM [SHOW GRANTS ON ROLE admin] WHERE member = current_user();

-- Check CockroachDB version
SELECT version();
```

## Steps

### 1. Check Current Audit Configuration

```sql
-- User audit logging configuration
SHOW CLUSTER SETTING sql.log.user_audit;

-- Admin audit logging
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;

-- All audit-related settings
SELECT variable, value
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable LIKE '%audit%'
ORDER BY variable;
```

See [SQL queries reference](references/sql-queries.md) for additional audit-related queries.

### 2. Enable Admin Audit Logging

Admin audit logging captures all SQL statements executed by users with the admin role.

```sql
-- Enable admin audit logging
SET CLUSTER SETTING sql.log.admin_audit.enabled = true;
```

**What is captured:**
- All SQL statements executed by admin users
- DDL operations (CREATE, ALTER, DROP)
- Grant and revoke operations
- Cluster setting changes

### 3. Configure Role-Based Audit Logging

Role-based audit logging allows targeted logging for specific roles. This is more efficient than cluster-wide logging.

```sql
-- Enable audit logging for a specific role
-- Format: <role_name> <audit_mode>
-- Audit modes: ALL (all statements), READ (reads only), WRITE (writes only), NONE (disable)
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL';
```

**Multiple roles:**
```sql
-- Audit multiple roles (newline-separated)
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL
security_admin ALL
app_service_account READ';
```

**Create purpose-specific audit roles:**
```sql
-- Create a role for users accessing sensitive data
CREATE ROLE sensitive_data_reader;
GRANT SELECT ON TABLE customers, payments, pii_table TO sensitive_data_reader;

-- Assign users to the audited role
GRANT sensitive_data_reader TO app_user;

-- Enable audit logging for this role
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL';
```

### 4. Configure Slow Query Logging (Supplemental)

Slow query logging captures queries exceeding a latency threshold, which can indicate unauthorized scans or data exfiltration attempts.

```sql
-- Log queries taking longer than 1 second
SET CLUSTER SETTING sql.log.slow_query.latency_threshold = '1s';

-- Log all queries (high overhead — use only for investigation)
-- SET CLUSTER SETTING sql.log.slow_query.latency_threshold = '0';
```

### 5. Verify Audit Logging

```sql
-- Confirm settings are active
SHOW CLUSTER SETTING sql.log.user_audit;
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;

-- Execute a test statement to generate an audit event
SELECT 1;
```

**Verify log delivery:**
On CockroachDB Cloud, audit logs are exported to your configured log sink (cloud provider logging service). Check your log export destination to verify events are being captured.

```bash
# On CockroachDB Cloud, check log export configuration
ccloud cluster info <cluster-name> -o json
# Look for log_export_config section
```

## Safety Considerations

**Performance impact:** Audit logging increases CPU and I/O overhead. The impact depends on the audit scope:

| Audit Scope | Performance Impact | Recommendation |
|-------------|-------------------|----------------|
| Admin audit only | Minimal | Safe for all environments |
| Role-based audit (targeted roles) | Low to moderate | Recommended for production |
| Cluster-wide all-statement logging | High | Use only during investigations |
| Slow query logging (threshold > 0) | Minimal | Safe for all environments |
| Slow query logging (threshold = 0) | Very high | Never use in production |

**Storage impact:** Audit logs increase log volume. Plan for:
- Admin audit: ~1-5% increase in log volume
- Role-based audit: Proportional to query volume of audited roles
- All-statement logging: 10x+ increase in log volume

**Recommendations:**
- Start with admin audit logging (minimal overhead, high value)
- Add role-based auditing for sensitive data access roles
- Avoid cluster-wide all-statement logging in production
- Configure log rotation and retention policies

## Rollback

```sql
-- Disable user audit logging
SET CLUSTER SETTING sql.log.user_audit = '';

-- Disable admin audit logging
SET CLUSTER SETTING sql.log.admin_audit.enabled = false;

-- Reset slow query threshold to default
RESET CLUSTER SETTING sql.log.slow_query.latency_threshold;
```

## References

**Skill references:**
- [SQL queries for audit logging](references/sql-queries.md)

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit
- [hardening-user-privileges](../hardening-user-privileges/SKILL.md) — Create purpose-specific roles for targeted auditing

**Official CockroachDB Documentation:**
- [SQL Audit Logging](https://www.cockroachlabs.com/docs/stable/sql-audit-logging.html)
- [Role-Based Audit Logging](https://www.cockroachlabs.com/docs/stable/role-based-audit-logging.html)
- [Cluster Settings](https://www.cockroachlabs.com/docs/stable/cluster-settings.html)
- [Log Export (CockroachDB Cloud)](https://www.cockroachlabs.com/docs/cockroachcloud/export-logs.html)

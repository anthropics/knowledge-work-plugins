# SQL Queries for Security Auditing

This reference provides SQL queries used during security posture assessments. All queries are read-only (SELECT and SHOW statements only).

## User and Role Queries

### List All Users with Role Membership

```sql
-- All users and their role memberships
SELECT
  username,
  options,
  member_of
FROM [SHOW USERS]
ORDER BY username;
```

### Count Admin Role Members

```sql
-- Count users with admin role
SELECT COUNT(*) AS admin_count
FROM [SHOW GRANTS ON ROLE admin];
```

### List Admin Users with Details

```sql
-- Detailed admin user listing
SELECT
  member AS admin_user,
  is_admin
FROM [SHOW GRANTS ON ROLE admin]
WHERE is_admin = true
ORDER BY member;
```

### Find Users Without Role Membership

```sql
-- Users not assigned to any custom role (potential orphaned accounts)
SELECT username
FROM [SHOW USERS]
WHERE 'NOLOGIN' != ALL(options)
  AND array_length(member_of, 1) IS NULL
ORDER BY username;
```

## Privilege Queries

### PUBLIC Role Privileges

```sql
-- Non-default privileges granted to PUBLIC (current database context)
-- Note: SHOW GRANTS FOR public is scoped to the current database.
-- Run from each application database for full coverage.
SELECT
  database_name,
  schema_name,
  object_name,
  object_type,
  privilege_type
FROM [SHOW GRANTS FOR public]
WHERE privilege_type NOT IN ('USAGE')
  AND schema_name = 'public'
ORDER BY database_name, object_name;
```

### Database-Level Grants

```sql
-- All grants on a specific database
SELECT
  grantee,
  privilege_type,
  is_grantable
FROM [SHOW GRANTS ON DATABASE <database_name>]
ORDER BY grantee, privilege_type;
```

### System Privileges

```sql
-- System-level privileges for all users
SELECT
  grantee,
  privilege_type
FROM [SHOW SYSTEM GRANTS]
ORDER BY grantee, privilege_type;
```

### Users with Sensitive Privileges

```sql
-- Users with potentially dangerous system privileges
SELECT
  grantee,
  privilege_type
FROM [SHOW SYSTEM GRANTS]
WHERE privilege_type IN (
  'MODIFYCLUSTERSETTING',
  'CANCELQUERY',
  'CANCELSESSION',
  'VIEWACTIVITY',
  'CREATEDB',
  'CREATELOGIN'
)
ORDER BY privilege_type, grantee;
```

## Audit Logging Queries

### Check All Audit-Related Cluster Settings

```sql
-- User audit logging configuration
SHOW CLUSTER SETTING sql.log.user_audit;

-- Admin audit logging
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;

-- Slow query log threshold (related to audit visibility)
SHOW CLUSTER SETTING sql.log.slow_query.latency_threshold;
```

### Verify Audit Log Is Capturing Events

```sql
-- Check recent audit log entries (if audit logging is enabled)
-- Note: Audit logs are written to CockroachDB log files, not queryable via SQL
-- Use ccloud or log export to verify log delivery
```

## Password Policy Queries

### Check Password Policy Settings

```sql
-- Minimum password length
SHOW CLUSTER SETTING server.user_login.min_password_length;

-- Password hash cost (bcrypt rounds)
SHOW CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt;

-- Login attempt throttling
SHOW CLUSTER SETTING server.user_login.password.min_delay;
SHOW CLUSTER SETTING server.user_login.password.max_delay;
```

## SSO and Authentication Queries

### Check Cluster SSO (Database SSO) Settings

```sql
-- OIDC authentication enabled
SHOW CLUSTER SETTING server.oidc_authentication.enabled;

-- OIDC provider URL
SHOW CLUSTER SETTING server.oidc_authentication.provider_url;

-- OIDC client ID (verify configured)
SHOW CLUSTER SETTING server.oidc_authentication.client_id;

-- Identity mapping configuration
SHOW CLUSTER SETTING server.identity_map.configuration;
```

### Check Authentication Methods

```sql
-- HBA (Host-Based Authentication) configuration
SHOW CLUSTER SETTING server.host_based_authentication.configuration;
```

## Encryption Queries

### Check Encryption Settings

```sql
-- Enterprise encryption type
SHOW CLUSTER SETTING enterprise.encryption.type;
```

## Cluster Configuration Queries

### Cluster Version and Settings

```sql
-- CockroachDB version
SELECT version();

-- Cluster ID
SELECT crdb_internal.cluster_id();

-- All cluster settings related to security
SELECT
  variable,
  value,
  description
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable LIKE '%audit%'
   OR variable LIKE '%auth%'
   OR variable LIKE '%password%'
   OR variable LIKE '%login%'
   OR variable LIKE '%encrypt%'
   OR variable LIKE '%tls%'
   OR variable LIKE '%identity%'
   OR variable LIKE '%oidc%'
ORDER BY variable;
```

## Notes

- All queries use `SELECT` or `SHOW` statements and are read-only
- Replace `<database_name>` with the actual database name when running database-specific queries
- Some queries require admin or `VIEWACTIVITY` privilege for full visibility
- Queries that return no results may indicate the feature is not configured (not necessarily an error)

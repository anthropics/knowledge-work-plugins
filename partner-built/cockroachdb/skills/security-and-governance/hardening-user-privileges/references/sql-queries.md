# SQL Queries for Privilege Hardening

This reference provides SQL queries for auditing and managing user privileges on CockroachDB clusters.

## User and Role Auditing

### List All Users and Roles

```sql
-- All users and their role memberships
SELECT
  username,
  options,
  member_of
FROM [SHOW USERS]
ORDER BY username;
```

### List Admin Users

```sql
-- All users with admin role
SELECT member AS admin_user, is_admin
FROM [SHOW GRANTS ON ROLE admin]
WHERE is_admin = true
ORDER BY member;
```

### Count Admin Users

```sql
-- Count of admin users
SELECT COUNT(*) AS admin_count
FROM [SHOW GRANTS ON ROLE admin];
```

### Find Users Without Custom Roles

```sql
-- Users not assigned to any custom role (potential orphaned accounts)
SELECT username
FROM [SHOW USERS]
WHERE 'NOLOGIN' != ALL(options)
  AND array_length(member_of, 1) IS NULL
ORDER BY username;
```

### Find Roles Without Members

```sql
-- Roles with no members (potential unused roles)
SELECT username AS role_name
FROM [SHOW USERS]
WHERE 'NOLOGIN' = ANY(options)
ORDER BY role_name;
-- Compare with SHOW GRANTS ON ROLE <role_name> to find empty roles
```

## Privilege Auditing

### PUBLIC Role Privileges

```sql
-- All non-default privileges granted to PUBLIC
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

### System-Level Privileges

```sql
-- All system privileges granted to users
SELECT grantee, privilege_type
FROM [SHOW SYSTEM GRANTS]
ORDER BY grantee, privilege_type;
```

### Sensitive System Privileges

```sql
-- Users with potentially dangerous privileges
SELECT grantee, privilege_type
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

### Database-Level Privileges

```sql
-- All grants on a specific database
SELECT grantee, privilege_type, is_grantable
FROM [SHOW GRANTS ON DATABASE <database_name>]
ORDER BY grantee, privilege_type;
```

### Table-Level Privileges

```sql
-- All grants on a specific table
SELECT grantee, privilege_type, is_grantable
FROM [SHOW GRANTS ON TABLE <table_name>]
ORDER BY grantee, privilege_type;
```

### User-Specific Privileges

```sql
-- All privileges for a specific user
SHOW GRANTS FOR <username>;
```

## Creating Purpose-Specific Roles

### Read-Only Analyst Role

```sql
CREATE ROLE analyst_reader;
GRANT SELECT ON DATABASE <app_db> TO analyst_reader;
GRANT analyst_reader TO <analyst_user>;
```

### Application Service Role

```sql
CREATE ROLE app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON DATABASE <app_db> TO app_service;
GRANT app_service TO <service_account>;
```

### Schema Management Role

```sql
CREATE ROLE schema_manager;
GRANT CREATE ON DATABASE <app_db> TO schema_manager;
GRANT schema_manager TO <migration_user>;
```

### Monitoring Role

```sql
CREATE ROLE monitoring;
GRANT SYSTEM VIEWACTIVITYREDACTED TO monitoring;
GRANT monitoring TO <monitoring_user>;
```

### Operations Triage Role

```sql
CREATE ROLE ops_triage;
GRANT SYSTEM VIEWACTIVITYREDACTED, CANCELQUERY TO ops_triage;
GRANT ops_triage TO <oncall_user>;
```

## Revoking Privileges

### Revoke Admin

```sql
-- Revoke admin from a specific user
REVOKE admin FROM <username>;

-- Verify admin was revoked
SELECT member FROM [SHOW GRANTS ON ROLE admin] WHERE member = '<username>';
-- Should return empty
```

### Revoke PUBLIC Grants

```sql
-- Revoke SELECT from PUBLIC on a database
REVOKE SELECT ON DATABASE <database_name> FROM public;

-- Revoke all data privileges from PUBLIC on a table
REVOKE ALL ON TABLE <table_name> FROM public;
```

### Revoke System Privileges

```sql
-- Revoke specific system privileges
REVOKE SYSTEM MODIFYCLUSTERSETTING FROM <username>;
REVOKE SYSTEM CREATEDB FROM <username>;
REVOKE SYSTEM VIEWACTIVITY FROM <username>;
```

## Pre-Change Snapshots

Before making privilege changes, capture current state for rollback:

```sql
-- Snapshot all grants for a user
SELECT * FROM [SHOW GRANTS FOR <username>];

-- Snapshot PUBLIC grants
SELECT * FROM [SHOW GRANTS FOR public];

-- Snapshot system grants
SELECT * FROM [SHOW SYSTEM GRANTS];

-- Snapshot admin members
SELECT * FROM [SHOW GRANTS ON ROLE admin];
```

## Notes

- All audit queries are read-only (SELECT and SHOW only)
- Privilege changes (GRANT, REVOKE) take effect immediately
- Always test privilege changes in staging before production
- Keep at least one admin user at all times
- The `root` user always has admin and cannot be modified
- Replace `<database_name>`, `<table_name>`, `<username>` with actual values

---
name: hardening-user-privileges
description: Hardens CockroachDB user privileges by auditing and tightening role-based access control, reducing admin grants, restricting PUBLIC role permissions, and applying least-privilege principles. Use when reducing excessive privileges, cleaning up admin access, or implementing RBAC best practices.
compatibility: Requires admin role to modify grants and role membership.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Hardening User Privileges

Audits and tightens CockroachDB role-based access control (RBAC) by identifying over-privileged users, reducing admin grants, restricting PUBLIC role permissions, creating purpose-specific roles, and applying least-privilege principles.

## When to Use This Skill

- Reducing the number of users with admin role
- Removing excessive PUBLIC role privileges (SELECT, INSERT, UPDATE, DELETE)
- Creating purpose-specific roles to replace broad admin grants
- Responding to a security audit finding about excessive privileges
- Implementing RBAC best practices for a production cluster
- Onboarding a cluster to a least-privilege access model

## Prerequisites

- **SQL access** with admin role (required to modify grants and role membership)
- **User inventory:** Understanding of which users/applications need which level of access
- **Application testing plan:** Revoking grants can break applications that depend on them

**Check your access:**
```sql
SELECT member FROM [SHOW GRANTS ON ROLE admin] WHERE member = current_user();
```

## Steps

### 1. Audit Current Users and Roles

```sql
-- List all users and their role memberships
SELECT
  username,
  options,
  member_of
FROM [SHOW USERS]
ORDER BY username;

-- Count admin role members
SELECT COUNT(*) AS admin_count
FROM [SHOW GRANTS ON ROLE admin];

-- List all admin users
SELECT member AS admin_user
FROM [SHOW GRANTS ON ROLE admin]
WHERE is_admin = true
ORDER BY member;
```

See [SQL queries reference](references/sql-queries.md) for additional audit queries.

### 2. Identify Over-Privileged Users

**Admin role review:**
```sql
-- Admin users — each should have a documented reason for admin access
SELECT member AS admin_user
FROM [SHOW GRANTS ON ROLE admin]
WHERE is_admin = true
ORDER BY member;
```

Evaluate each admin user:
- **Keep admin:** Cluster operators, DBAs, automation accounts that genuinely need full access
- **Downgrade:** Developers, analysts, application service accounts that only need specific permissions

**PUBLIC role review:**
```sql
-- Check what PUBLIC can do (these apply to ALL users)
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

**System privilege review:**
```sql
-- Users with sensitive system privileges
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

### 3. Create Purpose-Specific Roles

Replace broad admin grants with targeted roles:

```sql
-- Read-only role for analysts
CREATE ROLE analyst_reader;
GRANT SELECT ON DATABASE <app_db> TO analyst_reader;

-- Application service role (read + write, no DDL)
CREATE ROLE app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON DATABASE <app_db> TO app_service;

-- Schema management role (DDL only)
CREATE ROLE schema_manager;
GRANT CREATE ON DATABASE <app_db> TO schema_manager;

-- Monitoring role (read-only system visibility)
CREATE ROLE monitoring;
GRANT SYSTEM VIEWACTIVITYREDACTED TO monitoring;

-- Operations role (triage + cancel, no data access)
CREATE ROLE ops_triage;
GRANT SYSTEM VIEWACTIVITYREDACTED, CANCELQUERY TO ops_triage;
```

### 4. Reassign Users to Purpose-Specific Roles

```sql
-- Assign users to their appropriate roles
GRANT analyst_reader TO analyst_user;
GRANT app_service TO payment_service, order_service;
GRANT schema_manager TO migration_user;
GRANT monitoring TO monitoring_user;
GRANT ops_triage TO oncall_sre;
```

### 5. Revoke Excessive Grants

**Revoke admin from users who no longer need it:**
```sql
-- Revoke admin from specific users
REVOKE admin FROM analyst_user;
REVOKE admin FROM payment_service;
REVOKE admin FROM monitoring_user;
```

**Revoke PUBLIC role data grants:**
```sql
-- Revoke SELECT from PUBLIC on application databases
REVOKE SELECT ON DATABASE <app_db> FROM public;

-- Revoke all data privileges from PUBLIC on specific tables
REVOKE ALL ON TABLE <sensitive_table> FROM public;
```

**Revoke unnecessary system privileges:**
```sql
-- Revoke system privileges from users who don't need them
REVOKE SYSTEM MODIFYCLUSTERSETTING FROM <username>;
REVOKE SYSTEM CREATEDB FROM <username>;
```

### 6. Verify Changes

```sql
-- Confirm admin count is reduced
SELECT COUNT(*) AS admin_count FROM [SHOW GRANTS ON ROLE admin];

-- Confirm PUBLIC privileges are minimal
SELECT database_name, privilege_type
FROM [SHOW GRANTS FOR public]
WHERE privilege_type NOT IN ('USAGE');

-- Verify specific user's effective privileges
SHOW GRANTS FOR <username>;
```

**Application testing:** After revoking grants, verify that all applications still function correctly. Test:
- Read operations (SELECT)
- Write operations (INSERT, UPDATE, DELETE)
- Schema operations (CREATE, ALTER, DROP) — only for schema management accounts
- Connection and authentication

## Safety Considerations

**Revoking grants can break applications.** Applications that depend on admin, PUBLIC, or specific grants will fail with permission errors if those grants are revoked.

**Mitigation steps:**
1. **Audit before revoking:** Document which users/apps depend on which grants
2. **Create replacement roles first:** Assign purpose-specific roles before revoking admin
3. **Test in staging:** Revoke grants in a staging environment first and test all application flows
4. **Revoke incrementally:** Revoke one user/grant at a time and test
5. **Monitor for errors:** Watch application logs for permission-denied errors after changes

**Do not revoke admin from:**
- The last remaining admin user (you'll lose the ability to manage the cluster)
- Automation accounts that manage schema migrations (unless you've created a schema_manager role)
- The `root` user (built-in, cannot be revoked)

## Rollback

If an application breaks after revoking a grant:

```sql
-- Re-grant admin (emergency)
GRANT admin TO <username>;

-- Re-grant specific privileges
GRANT SELECT, INSERT, UPDATE ON DATABASE <app_db> TO <username>;

-- Re-grant PUBLIC privileges
GRANT SELECT ON DATABASE <app_db> TO public;
```

**Best practice:** Keep a record of all grants before revoking so you can restore them if needed:
```sql
-- Snapshot current grants before changes
SELECT * FROM [SHOW GRANTS FOR <username>];
SELECT * FROM [SHOW GRANTS FOR public];
SELECT * FROM [SHOW SYSTEM GRANTS];
```

## References

**Skill references:**
- [SQL queries for privilege hardening](references/sql-queries.md)

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit
- [configuring-audit-logging](../configuring-audit-logging/SKILL.md) — Set up audit logging for privilege-sensitive operations

**Official CockroachDB Documentation:**
- [Authorization Overview](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html)
- [GRANT](https://www.cockroachlabs.com/docs/stable/grant.html)
- [REVOKE](https://www.cockroachlabs.com/docs/stable/revoke.html)
- [CREATE ROLE](https://www.cockroachlabs.com/docs/stable/create-role.html)
- [SHOW GRANTS](https://www.cockroachlabs.com/docs/stable/show-grants.html)
- [System Privileges](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

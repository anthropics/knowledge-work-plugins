# RBAC and Privilege Setup

This reference provides detailed information about CockroachDB privileges required for SQL activity triage, including how to grant them and security best practices.

## Privilege Comparison

### VIEWACTIVITY vs VIEWACTIVITYREDACTED

| Privilege | Query Text Visibility | Use Case | Privacy Level |
|-----------|----------------------|----------|---------------|
| `VIEWACTIVITY` | Full query text for all users | Dev/staging, single-tenant environments | Low - exposes all query constants |
| `VIEWACTIVITYREDACTED` | Redacted constants in other users' queries | Production, multi-tenant environments | High - protects sensitive data |
| None (default) | Only your own queries | Limited triage capability | Highest - no visibility into other users |

**Redaction example:**
- With `VIEWACTIVITY`: `SELECT * FROM users WHERE email = 'user@example.com'`
- With `VIEWACTIVITYREDACTED`: `SELECT * FROM users WHERE email = '_'`

### Cancellation Privileges

| Privilege | Scope | Use Case |
|-----------|-------|----------|
| `CANCELQUERY` | Cancel individual queries | Terminate specific runaway queries |
| `CANCELSESSION` | Cancel entire sessions (all queries in session) | Terminate problematic client connections |

### Admin Role Defaults

The `admin` role has all privileges by default:
- `VIEWACTIVITY`
- `CANCELQUERY`
- `CANCELSESSION`
- All other system privileges

## Checking Current Privileges

### Check Your Own Privileges

```sql
-- Show all system privileges for your current user
SHOW GRANTS ON ROLE <your_username>;
```

**Example output:**
```
database_name | schema_name | object_name | object_type | grantee  | privilege_type       | is_grantable
--------------+-------------+-------------+-------------+----------+---------------------+--------------
NULL          | NULL        | NULL        | system      | myuser   | VIEWACTIVITYREDACTED | false
NULL          | NULL        | NULL        | system      | myuser   | CANCELQUERY          | false
```

### Check Another User's Privileges (Admin Only)

```sql
-- Show privileges for another user
SHOW GRANTS ON ROLE <other_username>;
```

### Check Role Membership

```sql
-- Show all roles you belong to
SHOW GRANTS ON ROLE <your_username>;

-- Show members of a specific role
SHOW GRANTS ON ROLE admin;
```

## Granting Privileges

**Prerequisite:** You must be an `admin` user to grant system privileges.

### Grant VIEWACTIVITYREDACTED (Recommended for Production)

```sql
-- Grant cluster-wide activity visibility with redaction
GRANT SYSTEM VIEWACTIVITYREDACTED TO <username>;
```

**Use when:**
- User needs to triage cluster-wide performance issues
- Privacy/security requires protecting query constants
- Multi-tenant or production environments

### Grant VIEWACTIVITY (Full Query Text)

```sql
-- Grant cluster-wide activity visibility without redaction
GRANT SYSTEM VIEWACTIVITY TO <username>;
```

**Use when:**
- User needs full query text for debugging
- Single-tenant or development environments
- Privacy is not a concern

**Warning:** This exposes potentially sensitive data (passwords, emails, PII) in query constants.

### Grant CANCELQUERY

```sql
-- Grant ability to cancel individual queries
GRANT SYSTEM CANCELQUERY TO <username>;
```

**Use when:**
- User is authorized to terminate runaway queries
- DBA or on-call SRE role

### Grant CANCELSESSION

```sql
-- Grant ability to cancel entire sessions
GRANT SYSTEM CANCELSESSION TO <username>;
```

**Use when:**
- User is authorized to terminate client connections
- DBA or on-call SRE role

### Grant Multiple Privileges at Once

```sql
-- Grant full triage and cancellation privileges
GRANT SYSTEM VIEWACTIVITYREDACTED, CANCELQUERY, CANCELSESSION TO <username>;
```

## Revoking Privileges

### Revoke Specific Privilege

```sql
-- Revoke activity viewing privilege
REVOKE SYSTEM VIEWACTIVITYREDACTED FROM <username>;

-- Revoke cancellation privilege
REVOKE SYSTEM CANCELQUERY FROM <username>;
```

### Revoke Multiple Privileges

```sql
-- Revoke all triage-related privileges
REVOKE SYSTEM VIEWACTIVITYREDACTED, CANCELQUERY, CANCELSESSION FROM <username>;
```

## Role-Based Access Control (RBAC)

Instead of granting privileges to individual users, use roles for easier management:

### Create a Triage Role

```sql
-- Create a role for triage operations
CREATE ROLE triage_operator;

-- Grant triage privileges to the role
GRANT SYSTEM VIEWACTIVITYREDACTED, CANCELQUERY TO triage_operator;

-- Assign users to the role
GRANT triage_operator TO alice, bob, charlie;
```

### Create a Read-Only Triage Role

```sql
-- Create a role for read-only triage (no cancellation)
CREATE ROLE triage_viewer;

-- Grant only viewing privilege
GRANT SYSTEM VIEWACTIVITYREDACTED TO triage_viewer;

-- Assign users to the role
GRANT triage_viewer TO viewer_user;
```

### Example: Multi-Tier Access Model

```sql
-- Tier 1: View only (redacted)
CREATE ROLE triage_viewer;
GRANT SYSTEM VIEWACTIVITYREDACTED TO triage_viewer;
GRANT triage_viewer TO tier1_user;

-- Tier 2: View + Cancel Queries
CREATE ROLE triage_operator;
GRANT SYSTEM VIEWACTIVITYREDACTED, CANCELQUERY TO triage_operator;
GRANT triage_operator TO tier2_user;

-- Tier 3: Full triage + Cancel Sessions (DBA)
CREATE ROLE triage_admin;
GRANT SYSTEM VIEWACTIVITY, CANCELQUERY, CANCELSESSION TO triage_admin;
GRANT triage_admin TO dba_user;
```

## Least Privilege Examples

### On-Call SRE (Read-Only Triage)

```sql
-- Grant minimal privileges for read-only triage
GRANT SYSTEM VIEWACTIVITYREDACTED TO oncall_sre;
```

**Rationale:**
- Can diagnose issues without terminating workloads
- Protects against accidental cancellations
- Maintains privacy with redaction

### Database Administrator (Full Triage)

```sql
-- Grant full triage and intervention privileges
GRANT SYSTEM VIEWACTIVITY, CANCELQUERY, CANCELSESSION TO dba_user;
```

**Rationale:**
- Needs full query text for deep debugging
- Authorized to terminate problematic workloads
- Trusted with sensitive data

### Application Team Lead (Limited Scope)

**Challenge:** CockroachDB doesn't support application-scoped privileges.

**Workaround:**
1. Grant `VIEWACTIVITYREDACTED` for cluster-wide visibility
2. Train users to filter by their `application_name` in queries
3. Use audit logging to monitor cancellation operations

```sql
-- Grant view-only access
GRANT SYSTEM VIEWACTIVITYREDACTED TO app_team_lead;

-- User manually filters in queries:
-- WHERE application_name = 'my-app'
```

## Security Best Practices

### 1. Use VIEWACTIVITYREDACTED by Default

Unless you have a specific need for full query text, always use `VIEWACTIVITYREDACTED` to protect sensitive data.

```sql
-- Recommended
GRANT SYSTEM VIEWACTIVITYREDACTED TO triage_user;

-- Avoid unless necessary
GRANT SYSTEM VIEWACTIVITY TO triage_user;
```

### 2. Separate View and Cancel Privileges

Not everyone who can diagnose issues should be able to cancel work. Use separate roles:

```sql
-- Most users: view only
GRANT SYSTEM VIEWACTIVITYREDACTED TO triage_viewer;

-- Senior users: view + cancel
GRANT SYSTEM VIEWACTIVITYREDACTED, CANCELQUERY TO triage_operator;
```

### 3. Enable Audit Logging

Track who cancels queries and sessions for accountability:

```sql
-- Enable audit logging for cancellation events
SET CLUSTER SETTING sql.log.admin_audit.enabled = true;
```

**Logged events include:**
- `CANCEL QUERY` operations
- `CANCEL SESSION` operations
- User who issued the command
- Timestamp

### 4. Rotate Privileges Regularly

Review and revoke privileges for users who no longer need them:

```sql
-- Quarterly privilege audit
SHOW GRANTS ON ROLE ALL;

-- Revoke from inactive users
REVOKE SYSTEM VIEWACTIVITYREDACTED FROM inactive_user;
```

### 5. Use Roles Instead of Direct Grants

Manage privileges via roles for easier auditing and updates:

```sql
-- Good: Use roles
CREATE ROLE triage_operator;
GRANT SYSTEM VIEWACTIVITYREDACTED TO triage_operator;
GRANT triage_operator TO alice;

-- Avoid: Direct grants to many users
GRANT SYSTEM VIEWACTIVITYREDACTED TO alice;
GRANT SYSTEM VIEWACTIVITYREDACTED TO bob;
GRANT SYSTEM VIEWACTIVITYREDACTED TO charlie;
```

### 6. Document Privilege Grants

Maintain documentation of who has what privileges and why:

```sql
-- Add comments to roles
COMMENT ON ROLE triage_operator IS 'Read-only triage access for on-call team';
```

## Common Privilege Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Can't see other users' queries | `SHOW CLUSTER STATEMENTS` only shows your own queries | Grant `VIEWACTIVITY` or `VIEWACTIVITYREDACTED` |
| Query text shows `<hidden>` | Constants redacted in query output | This is expected with `VIEWACTIVITYREDACTED`; use `VIEWACTIVITY` if needed |
| "permission denied" when canceling | Error when running `CANCEL QUERY` | Grant `CANCELQUERY` privilege |
| Can't cancel session | Error when running `CANCEL SESSION` | Grant `CANCELSESSION` privilege |
| Privilege grant fails | "permission denied" when granting privileges | Only `admin` users can grant system privileges |

## Verifying Privilege Effects

### Test VIEWACTIVITYREDACTED

```sql
-- 1. Grant privilege
GRANT SYSTEM VIEWACTIVITYREDACTED TO test_user;

-- 2. As test_user, run triage query
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id, user_name, substring(query, 1, 200) AS query_preview
FROM q
LIMIT 10;

-- 3. Verify you see other users' queries with redacted constants
```

### Test CANCELQUERY

```sql
-- 1. Grant privilege
GRANT SYSTEM CANCELQUERY TO test_user;

-- 2. Identify a query to cancel
WITH q AS (SHOW CLUSTER STATEMENTS)
SELECT query_id FROM q LIMIT 1;

-- 3. As test_user, attempt to cancel
CANCEL QUERY '<query_id_from_step_2>';

-- 4. Verify no "permission denied" error
```

## References

**Official CockroachDB Documentation:**
- [Authorization Overview](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html)
- [GRANT (System Privilege)](https://www.cockroachlabs.com/docs/stable/grant.html)
- [REVOKE (System Privilege)](https://www.cockroachlabs.com/docs/stable/revoke.html)
- [SHOW GRANTS](https://www.cockroachlabs.com/docs/stable/show-grants.html)
- [CREATE ROLE](https://www.cockroachlabs.com/docs/stable/create-role.html)

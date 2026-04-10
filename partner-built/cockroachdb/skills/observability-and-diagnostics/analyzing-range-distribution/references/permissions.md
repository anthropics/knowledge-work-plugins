# Permissions and RBAC for Range Analysis

This reference covers privilege requirements for `SHOW RANGES`, `SHOW RANGES WITH DETAILS`, and `SHOW ZONE CONFIGURATIONS` commands used in range distribution analysis and schema change storage planning.

## Required Privileges

### Command Privilege Matrix

| Command | Minimum Privilege | Alternative | Scope |
|---------|------------------|-------------|-------|
| `SHOW RANGES` | `ZONECONFIG` system privilege | `admin` role | Cluster-wide or specific table |
| `SHOW RANGES WITH DETAILS` | `ZONECONFIG` system privilege | `admin` role | Cluster-wide or specific table |
| `SHOW ZONE CONFIGURATIONS` | `ZONECONFIG` system privilege | `admin` role | Cluster-wide |

**Recommended approach:** Grant `ZONECONFIG` system privilege instead of `admin` role for read-only range analysis operators.

---

## Privilege Comparison

### Admin Role vs ZONECONFIG Privilege

| Capability | Admin Role | ZONECONFIG Privilege |
|------------|-----------|---------------------|
| `SHOW RANGES` | Yes | Yes |
| `SHOW RANGES WITH DETAILS` | Yes | Yes |
| `SHOW ZONE CONFIGURATIONS` | Yes | Yes |
| `ALTER ... CONFIGURE ZONE` | Yes | **No** (read-only) |
| `DROP TABLE`, `ALTER TABLE` | Yes | **No** |
| Grant/revoke privileges | Yes | **No** |
| View all user data | Yes | **No** (only range metadata) |

**Security best practice:** Use `ZONECONFIG` for range analysis roles. Reserve `admin` for operators who need write access.

---

## Granting ZONECONFIG Privilege

### Grant to Individual User

```sql
-- Grant ZONECONFIG system privilege to a user
GRANT SYSTEM ZONECONFIG TO range_analyst;
```

**Effect:** User `range_analyst` can run all range analysis queries but cannot modify zone configurations or data.

---

### Grant to Role (Multi-User)

```sql
-- Create a role for range analysts
CREATE ROLE range_analysts;

-- Grant ZONECONFIG to the role
GRANT SYSTEM ZONECONFIG TO range_analysts;

-- Add users to the role
GRANT range_analysts TO alice, bob, charlie;
```

**Effect:** All users in `range_analysts` role inherit ZONECONFIG privilege.

**Use case:** Onboarding multiple DBAs or support engineers for read-only observability access.

---

### Verify Privilege Grant

```sql
-- Check system privileges for a user
SHOW GRANTS ON SYSTEM FOR range_analyst;
```

**Expected output:**
```
  grantee      | privilege_type | is_grantable
---------------+----------------+--------------
 range_analyst | ZONECONFIG     |    false
```

---

## Revoking ZONECONFIG Privilege

### Revoke from User

```sql
-- Revoke ZONECONFIG privilege
REVOKE SYSTEM ZONECONFIG FROM range_analyst;
```

---

### Revoke from Role

```sql
-- Revoke privilege from role (affects all role members)
REVOKE SYSTEM ZONECONFIG FROM range_analysts;
```

---

## Checking Current User Privileges

### Check Your Own Privileges

```sql
-- View privileges for the current session user
SHOW GRANTS ON SYSTEM FOR current_user;
```

**Use case:** Confirm you have necessary privileges before running range analysis queries.

---

### Check If You Have Admin Role

```sql
-- Check if current user is an admin
SELECT crdb_internal.is_admin();
```

**Output:**
- `true`: You are an admin (can run all queries)
- `false`: Check for ZONECONFIG privilege separately

---

## Privilege Troubleshooting

### Common Error Messages

#### Error: "user does not have ZONECONFIG privilege"

**Full error:**
```
ERROR: user range_analyst does not have ZONECONFIG privilege
SQLSTATE: 42501
```

**Cause:** User lacks both `admin` role and `ZONECONFIG` system privilege.

**Fix:**
```sql
-- Option 1: Grant ZONECONFIG (recommended)
GRANT SYSTEM ZONECONFIG TO range_analyst;

-- Option 2: Grant admin role (use with caution)
GRANT admin TO range_analyst;
```

---

#### Error: "permission denied to show zone configuration"

**Full error:**
```
ERROR: permission denied to show zone configuration for TABLE your_table_name
SQLSTATE: 42501
```

**Cause:** User lacks privilege to view zone configurations.

**Fix:**
```sql
-- Grant ZONECONFIG privilege
GRANT SYSTEM ZONECONFIG TO range_analyst;
```

---

### Privilege Escalation (When Admin Access Needed)

**Scenario:** Range analyst needs to modify zone configurations after identifying hotspots.

**Approaches:**

**Option 1: Temporary Admin Grant (Less Secure)**
```sql
-- Grant admin temporarily
GRANT admin TO range_analyst;

-- User performs zone config changes
-- ALTER TABLE hot_table CONFIGURE ZONE USING lease_preferences = '[[+region=us-west]]';

-- Revoke admin after task completion
REVOKE admin FROM range_analyst;
```

**Option 2: Request Admin Intervention (Recommended)**
- Range analyst documents findings (leaseholder concentration, fragmentation metrics)
- Escalates to admin with specific zone config change recommendations
- Admin reviews and applies changes
- Maintains separation of duties (read vs. write access)

---

## Security Best Practices

### Principle of Least Privilege

**For range analysis operators:**
- Grant `ZONECONFIG` system privilege (not `admin` role)
- Allows full observability access without write permissions
- Limits blast radius if credentials compromised

**For schema change planners:**
- Same principle: `ZONECONFIG` for read-only storage estimation
- Escalate to `admin` only when executing DDL (CREATE INDEX, ADD COLUMN)

---

### Multi-Tenant Considerations

**Private data visibility:**
- `SHOW RANGES WITH DETAILS` exposes start/end keys (may reveal primary key values)
- Keys are hex-encoded but can be decoded if sensitive data used in primary keys

**Mitigation:**
- Use role-based access (grant to specific users/roles)
- Audit `SHOW RANGES WITH DETAILS` usage in compliance-sensitive environments
- Consider separate databases for multi-tenant isolation (each tenant = separate DB)

---

### Audit Logging

**Enable audit logging for ZONECONFIG privilege usage:**

```sql
-- Enable audit logging for admin/privilege changes (cluster setting)
SET CLUSTER SETTING server.auth_log.sql_sessions.enabled = true;
```

**Audit log location:** Check `cockroach-sql-audit.log` for `GRANT`/`REVOKE` statements.

**Use case:** Track who has been granted range analysis privileges and when.

---

## Privilege Workflow Examples

### Example 1: Onboarding Range Analyst

```sql
-- 1. Create user
CREATE USER alice WITH PASSWORD 'secure_password';

-- 2. Grant ZONECONFIG system privilege
GRANT SYSTEM ZONECONFIG TO alice;

-- 3. Verify grant
SHOW GRANTS ON SYSTEM FOR alice;

-- 4. User confirms access
-- Run as alice:
-- SELECT crdb_internal.is_admin();  -- Returns false
-- SHOW RANGES FROM TABLE users LIMIT 10;  -- Works
```

---

### Example 2: Read-Only Range Analysis Role

```sql
-- 1. Create role for range analysts team
CREATE ROLE range_analysts;

-- 2. Grant ZONECONFIG to role
GRANT SYSTEM ZONECONFIG TO range_analysts;

-- 3. Add team members
GRANT range_analysts TO alice, bob, charlie;

-- 4. Later: Remove user from role
REVOKE range_analysts FROM bob;
```

---

### Example 3: Temporary Admin for Zone Config Change

```sql
-- 1. Range analyst (alice) identifies hotspot via SHOW RANGES
-- 2. Escalates to admin with recommendation:
--    "Table 'orders' has 80% leaseholders on node 1. Recommend lease_preferences = [[+region=us-west]]"

-- 3. Admin (root) reviews and applies change:
ALTER TABLE orders CONFIGURE ZONE USING lease_preferences = '[[+region=us-west]]';

-- 4. Admin notifies alice to re-run SHOW RANGES to validate change
-- alice runs: SELECT lease_holder, COUNT(*) FROM [SHOW RANGES FROM TABLE orders] GROUP BY lease_holder;
```

---

## Privilege Summary Table

### Quick Reference: Who Can Run What

| User Type | SHOW RANGES | SHOW RANGES WITH DETAILS | SHOW ZONE CONFIGURATIONS | ALTER ZONE |
|-----------|-------------|--------------------------|-------------------------|------------|
| **Admin role** | Yes | Yes | Yes | Yes |
| **ZONECONFIG privilege** | Yes | Yes | Yes | **No** |
| **Regular user** | **No** | **No** | **No** | **No** |

---

## Related Documentation

- [Main skill: analyzing-range-distribution](../SKILL.md)
- [Main skill: analyzing-schema-change-storage-risk](../../analyzing-schema-change-storage-risk/SKILL.md)
- [CockroachDB Authorization Reference](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html)
- [GRANT (Privileges)](https://www.cockroachlabs.com/docs/stable/grant.html)
- [SHOW GRANTS](https://www.cockroachlabs.com/docs/stable/show-grants.html)
- [System Privileges](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html#supported-privileges)

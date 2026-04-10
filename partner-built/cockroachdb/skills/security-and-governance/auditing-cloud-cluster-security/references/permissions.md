# RBAC and Privileges for Security Auditing

This reference details the privileges required to run security audit queries and how to grant minimal access for audit operations.

## Required Privileges

### For Full Security Audit

| Privilege | Purpose | Required? |
|-----------|---------|-----------|
| `admin` role | Full cluster visibility, all settings, all grants | Recommended |
| `VIEWACTIVITY` | View all active sessions and queries | Alternative to admin |
| `VIEWACTIVITYREDACTED` | View sessions with redacted constants | Minimum for session visibility |

### For Specific Audit Checks

| Audit Check | Minimum Privilege | Notes |
|-------------|------------------|-------|
| User/role listing | Any authenticated user | `SHOW USERS` is available to all |
| Admin role membership | Any authenticated user | `SHOW GRANTS ON ROLE admin` is available to all |
| PUBLIC grants | Any authenticated user | `SHOW GRANTS FOR public` is available to all |
| Cluster settings | `admin` or `MODIFYCLUSTERSETTING` | `SHOW CLUSTER SETTING` requires elevated access |
| System grants | `admin` | `SHOW SYSTEM GRANTS` requires admin |
| Database grants | Database-level privilege | Can view grants on databases you have access to |

### For ccloud CLI

| Operation | Required Cloud Console Role |
|-----------|---------------------------|
| `ccloud cluster list` | Org Member (minimum) |
| `ccloud cluster describe` | Cluster Reader (minimum) |
| `ccloud cluster networking allowlist list` | Cluster Reader |
| `ccloud auth describe-sso` | Org Admin |
| `ccloud auth describe-scim` | Org Admin |

## Granting Audit Privileges

### Option 1: Create a Dedicated Audit Role (Recommended)

```sql
-- Create a security audit role with read-only access
CREATE ROLE security_auditor;

-- Grant the minimum privileges for a full audit
GRANT SYSTEM VIEWACTIVITYREDACTED TO security_auditor;

-- Assign the role to audit users
GRANT security_auditor TO <audit_username>;
```

**Limitation:** Some cluster setting queries require admin. The auditor will get partial results for those checks, which the audit report will note.

### Option 2: Use Admin Role (Full Visibility)

```sql
-- Grant admin for complete audit coverage
GRANT admin TO <audit_username>;
```

**Warning:** Admin grants full cluster control. Only use for trusted audit operators and consider revoking after the audit.

### Option 3: Temporary Admin Grant

```sql
-- Grant admin temporarily for the audit
GRANT admin TO <audit_username>;

-- After audit is complete, revoke
REVOKE admin FROM <audit_username>;
```

## Checking Current Privileges

```sql
-- Check your own privileges
SHOW GRANTS ON ROLE <your_username>;

-- Check system-level privileges
SHOW SYSTEM GRANTS;

-- Check if you have admin
SELECT member FROM [SHOW GRANTS ON ROLE admin] WHERE member = current_user();
```

## Security Best Practices for Audit Access

1. **Use dedicated audit accounts** — Do not use personal admin accounts for audits
2. **Time-bound access** — Grant admin temporarily and revoke after the audit
3. **Use VIEWACTIVITYREDACTED** — Protects sensitive data in query constants
4. **Audit the auditor** — Enable admin audit logging before granting audit access
5. **Document access grants** — Track who has audit privileges and why

```sql
-- Enable admin audit logging before granting audit access
SET CLUSTER SETTING sql.log.admin_audit.enabled = true;

-- Then grant temporary audit access
GRANT admin TO audit_user;
```

## References

**Official CockroachDB Documentation:**
- [Authorization Overview](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html)
- [GRANT (System Privilege)](https://www.cockroachlabs.com/docs/stable/grant.html)
- [SHOW GRANTS](https://www.cockroachlabs.com/docs/stable/show-grants.html)
- [Cloud Console Roles](https://www.cockroachlabs.com/docs/cockroachcloud/authorization.html)

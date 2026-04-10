---
name: enforcing-password-policies
description: Configures and enforces password policies on CockroachDB clusters including minimum length, complexity requirements, and hash cost settings. Use when strengthening authentication requirements, setting up password policies for a new cluster, or meeting compliance password standards.
compatibility: Requires admin role for cluster setting changes.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Enforcing Password Policies

Configures and enforces password policies on CockroachDB clusters by setting minimum password length, bcrypt hash cost, and login throttling. Ensures password strength meets organizational and compliance requirements.

## When to Use This Skill

- Strengthening password requirements to meet compliance standards (SOC 2, HIPAA, NIST 800-63B)
- Setting up password policies for a new production cluster
- Responding to a security audit finding about weak password policies
- Increasing bcrypt hash cost to improve resistance against brute-force attacks
- Configuring login throttling to mitigate credential stuffing

## Prerequisites

- **SQL access** with admin role (required to modify cluster settings)
- **Understanding of impact:** Password policy changes affect new passwords only, not existing passwords

**Check your access:**
```sql
SELECT member FROM [SHOW GRANTS ON ROLE admin] WHERE member = current_user();
```

## Steps

### 1. Check Current Password Policy Settings

```sql
-- Minimum password length
SHOW CLUSTER SETTING server.user_login.min_password_length;

-- Password hash cost (bcrypt rounds)
SHOW CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt;

-- Login attempt throttling
SHOW CLUSTER SETTING server.user_login.password.min_delay;
SHOW CLUSTER SETTING server.user_login.password.max_delay;
```

See [SQL queries reference](references/sql-queries.md) for additional password-related queries.

### 2. Set Minimum Password Length

```sql
-- Set minimum password length to 12 characters (recommended)
SET CLUSTER SETTING server.user_login.min_password_length = 12;
```

**Recommended minimums by compliance framework:**

| Framework | Minimum Length | Recommendation |
|-----------|---------------|----------------|
| NIST 800-63B | 8 characters | 12+ recommended |
| SOC 2 | 8 characters | 12+ recommended |
| HIPAA | 8 characters | 12+ recommended |
| PCI DSS | 7 characters | 12+ recommended |
| Internal best practice | — | 14+ for admin accounts |

### 3. Configure Hash Cost

The bcrypt hash cost controls how computationally expensive password hashing is. Higher values make brute-force attacks slower but increase CPU during authentication.

```sql
-- Set bcrypt hash cost (default: 10, recommended: 12)
SET CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt = 12;
```

**Hash cost guidance:**

| Cost | Time per Hash (approx.) | Recommendation |
|------|------------------------|----------------|
| 10 | ~100ms | Default, acceptable for most |
| 12 | ~400ms | Recommended for production |
| 14 | ~1.5s | High security, slower logins |

**Trade-off:** Higher cost means slower password verification, which affects login latency. Cost 12 is a good balance.

### 4. Configure Login Throttling

Login throttling introduces delays after failed authentication attempts to slow down brute-force attacks.

```sql
-- Minimum delay after failed login attempt
SET CLUSTER SETTING server.user_login.password.min_delay = '0.5s';

-- Maximum delay after repeated failures
SET CLUSTER SETTING server.user_login.password.max_delay = '10s';
```

The delay increases exponentially between `min_delay` and `max_delay` with each consecutive failed attempt.

### 5. Verify Enforcement

```sql
-- Confirm settings
SHOW CLUSTER SETTING server.user_login.min_password_length;
SHOW CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt;
SHOW CLUSTER SETTING server.user_login.password.min_delay;
SHOW CLUSTER SETTING server.user_login.password.max_delay;
```

**Test enforcement:**
```sql
-- This should fail if min_password_length is 12
CREATE USER test_weak_password WITH PASSWORD 'short';
-- Expected: ERROR: password too short

-- This should succeed
CREATE USER test_strong_password WITH PASSWORD 'a-secure-password-123';
DROP USER test_strong_password;
```

### 6. Address Existing Users with Weak Passwords

Password policy changes only apply to new passwords. Existing users retain their old passwords until they change them.

**Options for enforcing password rotation:**
1. **Communicate the policy change** and ask users to update their passwords
2. **Expire existing passwords** by requiring a password change on next login (if supported by your application layer)
3. **Reset passwords administratively** for critical accounts:

```sql
-- Reset a user's password (forces them to use a new, policy-compliant password)
ALTER USER <username> WITH PASSWORD '<new-strong-password>';
```

### 7. Manage Password Changes and Rotation

#### User Self-Service Password Changes

SQL users can change their own passwords:

```sql
-- User changes their own password
ALTER USER current_user() WITH PASSWORD '<new-password>';
```

**Note:** Non-admin users can change their own passwords by default. If users report they cannot change their password, verify they are connected as the correct user and that there are no HBA rules blocking password-based authentication.

#### Administrative Password Reset

```sql
-- Admin resets another user's password
ALTER USER <username> WITH PASSWORD '<new-strong-password>';

-- Verify the user exists before resetting
SELECT username FROM [SHOW USERS] WHERE username = '<username>';
```

#### Cloud Console vs SQL Passwords

CockroachDB Cloud has two separate password domains:
- **Cloud Console password** — Managed via Cloud Console UI or SSO. Reset via the Cloud Console login page "Forgot password" flow.
- **SQL user password** — Managed via SQL `ALTER USER`. Independent of the Cloud Console password.

Changing one does not affect the other. Users must manage both if they use both access methods.

#### Password Rotation Best Practices

- Rotate service account passwords on a regular schedule (e.g., every 90 days)
- Use certificate-based authentication for service accounts to avoid password rotation entirely
- Coordinate password rotation with application deployment cycles to avoid downtime
- After changing a password, verify the application can connect with the new credentials before decommissioning the old password

### 8. Troubleshoot Common Password Errors

#### "password too short"

The password does not meet the `min_password_length` setting.

```sql
-- Check the current minimum
SHOW CLUSTER SETTING server.user_login.min_password_length;
```

Fix: Use a longer password that meets or exceeds the minimum length.

#### "bcrypt password hash too long"

The password exceeds the bcrypt input limit of 72 bytes. This can occur with very long passwords or multi-byte Unicode characters.

```sql
-- Workaround: use a shorter password (under 72 bytes)
ALTER USER <username> WITH PASSWORD '<shorter-password>';
```

This is a bcrypt limitation, not a CockroachDB-specific issue.

#### Authentication failures after password change

If users report authentication failures immediately after changing their password:

1. Verify the password was set correctly (no copy-paste whitespace)
2. Check for connection pool caching of old credentials — restart the connection pool
3. Verify the HBA configuration allows password authentication:
   ```sql
   SHOW CLUSTER SETTING server.host_based_authentication.configuration;
   ```
4. Check login throttling delays if there were failed attempts:
   ```sql
   SHOW CLUSTER SETTING server.user_login.password.min_delay;
   SHOW CLUSTER SETTING server.user_login.password.max_delay;
   ```

## Safety Considerations

- **New passwords only:** Changing `min_password_length` does not invalidate existing passwords. Users with short passwords can still log in until they change their password.
- **Hash cost latency:** Increasing `crdb_bcrypt` cost increases login time. Test with realistic connection pools before setting cost above 12.
- **Throttling impact:** Login throttling delays affect all users after failed attempts, including legitimate users who mistype their password.
- **Service accounts:** Ensure service accounts use strong passwords or certificate-based authentication (certificates bypass password policy).

## Rollback

```sql
-- Reset minimum password length to default (1 = no minimum)
SET CLUSTER SETTING server.user_login.min_password_length = 1;

-- Reset hash cost to default
RESET CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt;

-- Reset login throttling to defaults
RESET CLUSTER SETTING server.user_login.password.min_delay;
RESET CLUSTER SETTING server.user_login.password.max_delay;
```

## References

**Skill references:**
- [SQL queries for password policies](references/sql-queries.md)

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit
- [configuring-sso-and-scim](../configuring-sso-and-scim/SKILL.md) — Use SSO to eliminate password-based authentication
- [managing-tls-certificates](../managing-tls-certificates/SKILL.md) — Use certificate-based authentication instead of passwords

**Official CockroachDB Documentation:**
- [Cluster Settings Reference](https://www.cockroachlabs.com/docs/stable/cluster-settings.html)
- [CREATE USER](https://www.cockroachlabs.com/docs/stable/create-user.html)
- [ALTER USER](https://www.cockroachlabs.com/docs/stable/alter-user.html)
- [Security Overview](https://www.cockroachlabs.com/docs/stable/security-reference/security-overview.html)
- [Authentication](https://www.cockroachlabs.com/docs/stable/authentication.html)

# SQL Queries for Password Policy Management

This reference provides SQL queries for configuring, verifying, and managing password policies on CockroachDB clusters.

## Checking Current Settings

### All Password-Related Settings

```sql
-- All cluster settings related to passwords and login
SELECT variable, value, description
FROM [SHOW ALL CLUSTER SETTINGS]
WHERE variable LIKE '%password%'
   OR variable LIKE '%login%'
ORDER BY variable;
```

### Individual Settings

```sql
-- Minimum password length
SHOW CLUSTER SETTING server.user_login.min_password_length;

-- Password hash cost (bcrypt rounds)
SHOW CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt;

-- Login throttling: minimum delay after failed attempt
SHOW CLUSTER SETTING server.user_login.password.min_delay;

-- Login throttling: maximum delay after repeated failures
SHOW CLUSTER SETTING server.user_login.password.max_delay;
```

## Configuring Password Policies

### Minimum Password Length

```sql
-- Set minimum length to 12 characters (recommended)
SET CLUSTER SETTING server.user_login.min_password_length = 12;

-- Set minimum length to 14 characters (high security)
SET CLUSTER SETTING server.user_login.min_password_length = 14;

-- Disable minimum length (not recommended)
SET CLUSTER SETTING server.user_login.min_password_length = 1;
```

### Hash Cost (bcrypt)

```sql
-- Set hash cost to 12 (recommended for production)
SET CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt = 12;

-- Set hash cost to 14 (high security, slower logins)
SET CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt = 14;

-- Reset to default (10)
RESET CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt;
```

### Login Throttling

```sql
-- Configure login throttling
SET CLUSTER SETTING server.user_login.password.min_delay = '0.5s';
SET CLUSTER SETTING server.user_login.password.max_delay = '10s';

-- Reset to defaults
RESET CLUSTER SETTING server.user_login.password.min_delay;
RESET CLUSTER SETTING server.user_login.password.max_delay;
```

## Testing Password Policy

### Test Minimum Length Enforcement

```sql
-- Should fail with "password too short" if min_password_length > 5
CREATE USER pw_test_user WITH PASSWORD 'short';

-- Should succeed with a compliant password
CREATE USER pw_test_user WITH PASSWORD 'a-secure-password-that-meets-policy';

-- Clean up
DROP USER IF EXISTS pw_test_user;
```

### Test Hash Cost Impact

```sql
-- Time a password change to measure hash cost impact
-- Higher cost = longer time to hash
ALTER USER <test_user> WITH PASSWORD 'new-password-for-timing-test';
```

## User Password Management

### Reset a User's Password

```sql
-- Set a new password for a user
ALTER USER <username> WITH PASSWORD '<new-strong-password>';
```

### List All Users (to identify password rotation candidates)

```sql
-- All non-role users who may have passwords
SELECT username
FROM [SHOW USERS]
WHERE 'NOLOGIN' != ALL(options)
ORDER BY username;
```

## Resetting to Defaults

```sql
-- Reset all password-related settings to defaults
SET CLUSTER SETTING server.user_login.min_password_length = 1;
RESET CLUSTER SETTING server.user_login.password_hashes.default_cost.crdb_bcrypt;
RESET CLUSTER SETTING server.user_login.password.min_delay;
RESET CLUSTER SETTING server.user_login.password.max_delay;
```

## Notes

- Password policy changes affect new passwords only — existing passwords remain valid
- Hash cost changes apply to the next password set/change, not retroactively
- Login throttling applies per-user, not globally
- Service accounts using certificate authentication bypass password policies
- CockroachDB does not currently support password complexity rules (uppercase, special chars) — only minimum length

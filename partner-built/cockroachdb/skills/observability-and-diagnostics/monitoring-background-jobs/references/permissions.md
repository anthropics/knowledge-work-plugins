# RBAC and Privilege Setup

This reference provides detailed information about CockroachDB privileges required for background job monitoring, including how to grant them and security best practices.

## Privilege Comparison

### VIEWJOB vs CONTROLJOB vs None

| Privilege | Type | Job Visibility | Control Operations | Use Case |
|-----------|------|----------------|-------------------|----------|
| `VIEWJOB` | System privilege | All jobs cluster-wide | No | Read-only monitoring and diagnosis |
| `CONTROLJOB` | Role option | All jobs cluster-wide | Yes (PAUSE/RESUME/CANCEL) | Operational job management |
| None (default) | N/A | Only your own jobs | No | Limited self-service access |

**Key differences from VIEWACTIVITY:**
- `VIEWJOB` is for job monitoring (background operations)
- `VIEWACTIVITY` is for statement monitoring (user queries)
- Both are system privileges, but serve different observability needs
- Jobs and statements are tracked separately in CockroachDB

### VIEWJOB Privilege

**Scope:** Read-only access to all cluster jobs via:
- `SHOW JOBS` (all user-initiated and automatic jobs)
- `SHOW AUTOMATIC JOBS` (automatic jobs only)
- `crdb_internal.jobs` table
- `crdb_internal.system_jobs` table

**Operations allowed:**
- View job status, progress, errors
- Monitor running, failed, paused jobs
- Analyze job history

**Operations NOT allowed:**
- `PAUSE JOB` (requires CONTROLJOB)
- `RESUME JOB` (requires CONTROLJOB)
- `CANCEL JOB` (requires CONTROLJOB)

### CONTROLJOB Role Option

**CRITICAL: CONTROLJOB is a role option, not a system privilege**

**Scope:** Full job visibility AND control operations:
- All `VIEWJOB` capabilities
- `PAUSE JOB <job_id>` - Pause running jobs
- `RESUME JOB <job_id>` - Resume paused jobs
- `CANCEL JOB <job_id>` - Cancel jobs (terminal operation)

**Grant syntax (different from system privileges):**
```sql
-- Correct: Use ALTER ROLE WITH
ALTER ROLE <username> WITH CONTROLJOB;

-- WRONG: Cannot use GRANT SYSTEM for CONTROLJOB
-- GRANT SYSTEM CONTROLJOB TO <username>;  -- This will FAIL
```

**Revoke syntax:**
```sql
-- Revoke CONTROLJOB role option
ALTER ROLE <username> WITH NOCONTROLJOB;
```

### Admin Role Defaults

The `admin` role has CONTROLJOB by default:
- Full job visibility (VIEWJOB implicit)
- Full job control (PAUSE/RESUME/CANCEL)
- No additional grants needed

## Checking Current Privileges

### Check Your Own Privileges

**For VIEWJOB (system privilege):**
```sql
-- Show all system privileges for your current user
SHOW GRANTS ON ROLE <your_username>;
```

**Example output:**
```
database_name | schema_name | object_name | object_type | grantee  | privilege_type | is_grantable
--------------+-------------+-------------+-------------+----------+----------------+--------------
NULL          | NULL        | NULL        | system      | myuser   | VIEWJOB        | false
```

**For CONTROLJOB (role option):**
```sql
-- Show user details including role options
SHOW USERS;
```

**Example output:**
```
username | options    | member_of
---------+------------+-----------
myuser   | CONTROLJOB | {}
admin    | CONTROLJOB | {}
```

### Check Another User's Privileges (Admin Only)

```sql
-- Check system privileges
SHOW GRANTS ON ROLE <other_username>;

-- Check role options
SHOW USERS;  -- Look for CONTROLJOB in options column
```

### Verify Effective Permissions

**Test VIEWJOB:**
```sql
-- Should return all cluster jobs (not just your own)
SHOW JOBS;
```

If you only see your own jobs, you don't have VIEWJOB privilege.

**Test CONTROLJOB:**
```sql
-- Attempt to pause a job (requires CONTROLJOB)
PAUSE JOB <some_job_id>;
```

If you get "permission denied", you don't have CONTROLJOB role option.

## Granting Privileges

**Prerequisite:** You must be an `admin` user to grant privileges and role options.

### Grant VIEWJOB (Read-Only Monitoring)

```sql
-- Grant cluster-wide job visibility (read-only)
GRANT SYSTEM VIEWJOB TO <username>;
```

**Use when:**
- User needs to monitor job health and status
- Read-only access is sufficient (no job control needed)
- Separation of duties: monitoring vs operational control
- On-call engineers need visibility without intervention rights

### Grant CONTROLJOB (Full Job Control)

```sql
-- Grant job control capabilities (includes VIEWJOB functionality)
ALTER ROLE <username> WITH CONTROLJOB;
```

**IMPORTANT:** This is `ALTER ROLE ... WITH`, NOT `GRANT SYSTEM`.

**Use when:**
- User is authorized to pause/resume/cancel jobs
- DBA or senior SRE role
- Operational troubleshooting requires job intervention
- User understands job cancellation implications

**Note:** CONTROLJOB implicitly provides job visibility, so VIEWJOB is not required separately.

### Grant Both Explicitly (Not Recommended)

```sql
-- VIEWJOB for read-only monitoring
GRANT SYSTEM VIEWJOB TO <username>;

-- CONTROLJOB for job control (already includes visibility)
ALTER ROLE <username> WITH CONTROLJOB;
```

**Recommendation:** If granting CONTROLJOB, you don't need to grant VIEWJOB separately.

## Revoking Privileges

### Revoke VIEWJOB

```sql
-- Revoke job viewing privilege
REVOKE SYSTEM VIEWJOB FROM <username>;
```

### Revoke CONTROLJOB

```sql
-- Revoke job control privilege (use NOCONTROLJOB)
ALTER ROLE <username> WITH NOCONTROLJOB;
```

**Note:** Different syntax from revoking system privileges.

## Role-Based Access Control (RBAC)

Instead of granting privileges to individual users, use roles for easier management.

### Create a Job Monitoring Role (Read-Only)

```sql
-- Create a role for read-only job monitoring
CREATE ROLE job_monitor;

-- Grant VIEWJOB privilege to the role
GRANT SYSTEM VIEWJOB TO job_monitor;

-- Assign users to the role
GRANT job_monitor TO alice, bob, charlie;
```

**Users in this role can:**
- View all cluster jobs
- Monitor job status and errors
- Run diagnostic queries

**Users in this role CANNOT:**
- Pause, resume, or cancel jobs

### Create a Job Operator Role (Full Control)

```sql
-- Create a role for job operations
CREATE ROLE job_operator;

-- Grant VIEWJOB to the role
GRANT SYSTEM VIEWJOB TO job_operator;

-- Grant CONTROLJOB to users individually (role options can't be granted to roles)
-- You must grant CONTROLJOB directly to each user:
ALTER ROLE alice WITH CONTROLJOB;
ALTER ROLE bob WITH CONTROLJOB;

-- Assign users to the role for VIEWJOB
GRANT job_operator TO alice, bob;
```

**Important limitation:** CONTROLJOB is a role option and cannot be assigned to roles. You must grant it directly to individual users via `ALTER ROLE ... WITH CONTROLJOB`.

### Example: Multi-Tier Access Model

```sql
-- Tier 1: Read-only job monitoring
CREATE ROLE job_viewer;
GRANT SYSTEM VIEWJOB TO job_viewer;
GRANT job_viewer TO tier1_user;

-- Tier 2: Full job control (DBA)
-- Grant VIEWJOB via role
CREATE ROLE job_admin;
GRANT SYSTEM VIEWJOB TO job_admin;
GRANT job_admin TO dba_user;

-- Grant CONTROLJOB directly to DBA user
ALTER ROLE dba_user WITH CONTROLJOB;
```

## Least Privilege Examples

### On-Call SRE (Read-Only)

```sql
-- Grant minimal privileges for read-only job monitoring
GRANT SYSTEM VIEWJOB TO oncall_sre;
```

**Rationale:**
- Can diagnose job issues without terminating operations
- Protects against accidental job cancellations
- Sufficient for most monitoring and triage tasks

### Database Administrator (Full Control)

```sql
-- Grant full job monitoring and control
GRANT SYSTEM VIEWJOB TO dba_user;
ALTER ROLE dba_user WITH CONTROLJOB;
```

**Rationale:**
- Needs full job visibility for troubleshooting
- Authorized to pause/resume/cancel jobs during incidents
- Understands implications of job control operations

### Application Developer (No Access)

**Default:** No special privileges needed for developers unless they need to monitor their own jobs.

Developers can:
- View their own jobs (no VIEWJOB needed)
- Cancel their own jobs (no CONTROLJOB needed)

Developers CANNOT:
- View other users' jobs
- Cancel other users' jobs

## Security Best Practices

### 1. Separate Read and Control Privileges

Not everyone who can monitor jobs should be able to control them:

```sql
-- Most users: view only
GRANT SYSTEM VIEWJOB TO monitoring_team;

-- Senior users: view + control
GRANT SYSTEM VIEWJOB TO senior_dba;
ALTER ROLE senior_dba WITH CONTROLJOB;
```

### 2. Use VIEWJOB by Default

Start with read-only access and escalate only when needed:

```sql
-- Default for new monitoring users
GRANT SYSTEM VIEWJOB TO new_oncall_user;

-- Escalate only after training and authorization
-- ALTER ROLE new_oncall_user WITH CONTROLJOB;
```

### 3. Enable Audit Logging

Track who controls jobs for accountability:

```sql
-- Enable audit logging for job control operations
SET CLUSTER SETTING sql.log.admin_audit.enabled = true;
```

**Logged events include:**
- `PAUSE JOB` operations
- `RESUME JOB` operations
- `CANCEL JOB` operations
- User who issued the command
- Timestamp and affected job ID

### 4. Document CONTROLJOB Grants

Maintain documentation of who has CONTROLJOB and why:

```sql
-- Add comments to users with special privileges
COMMENT ON ROLE senior_dba IS 'Has CONTROLJOB for incident response';
```

### 5. Rotate Privileges Regularly

Review and revoke privileges for users who no longer need them:

```sql
-- Quarterly privilege audit
SHOW GRANTS ON ROLE ALL;
SHOW USERS;  -- Check CONTROLJOB role options

-- Revoke from inactive users
REVOKE SYSTEM VIEWJOB FROM inactive_user;
ALTER ROLE inactive_user WITH NOCONTROLJOB;
```

### 6. Use Roles Instead of Direct Grants

Manage privileges via roles for easier auditing and updates:

```sql
-- Good: Use roles for VIEWJOB
CREATE ROLE job_monitor;
GRANT SYSTEM VIEWJOB TO job_monitor;
GRANT job_monitor TO alice;

-- Avoid: Direct grants to many users
GRANT SYSTEM VIEWJOB TO alice;
GRANT SYSTEM VIEWJOB TO bob;
GRANT SYSTEM VIEWJOB TO charlie;
```

**Note:** CONTROLJOB must be granted directly to users (can't be assigned to roles).

### 7. Understand Job Control Risks

Before granting CONTROLJOB, ensure users understand:

| Job Type | Cancel Risk | Impact |
|----------|-------------|--------|
| SCHEMA CHANGE | High | May leave schema in inconsistent state |
| BACKUP | Low | Can safely retry backup |
| RESTORE | High | May leave database partially restored |
| AUTO CREATE STATS | Low | Will automatically retry later |
| CHANGEFEED | Medium | May lose CDC events if not replayed |

Train users to prefer PAUSE over CANCEL when possible.

## Common Privilege Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Can't see other users' jobs | `SHOW JOBS` only shows your own jobs | Grant `VIEWJOB` system privilege |
| "permission denied" when pausing job | Error when running `PAUSE JOB` | Grant CONTROLJOB role option: `ALTER ROLE <user> WITH CONTROLJOB` |
| "permission denied" when resuming job | Error when running `RESUME JOB` | Grant CONTROLJOB role option |
| "permission denied" when canceling job | Error when running `CANCEL JOB` | Grant CONTROLJOB role option |
| Privilege grant fails | "permission denied" when granting VIEWJOB | Only `admin` users can grant system privileges |
| GRANT SYSTEM CONTROLJOB fails | Syntax error or command not recognized | Use `ALTER ROLE <user> WITH CONTROLJOB` instead |
| Can't view automatic jobs | `SHOW AUTOMATIC JOBS` returns limited results | Grant `VIEWJOB` system privilege |

## Verifying Privilege Effects

### Test VIEWJOB

```sql
-- 1. Grant privilege
GRANT SYSTEM VIEWJOB TO test_user;

-- 2. As test_user, run job query
SHOW JOBS;

-- 3. Verify you see other users' jobs (not just your own)
-- Check for job_id values from other users
```

### Test CONTROLJOB

```sql
-- 1. Grant privilege
ALTER ROLE test_user WITH CONTROLJOB;

-- 2. Identify a test job to pause (use your own job to be safe)
WITH j AS (SHOW JOBS)
SELECT job_id FROM j WHERE status = 'running' LIMIT 1;

-- 3. As test_user, attempt to pause
PAUSE JOB <job_id_from_step_2>;

-- 4. Verify no "permission denied" error

-- 5. Resume the job
RESUME JOB <job_id_from_step_2>;
```

## Privilege Comparison with Other Monitoring Skills

| Skill | Read Privilege | Control Privilege |
|-------|----------------|-------------------|
| monitoring-background-jobs | `VIEWJOB` (system privilege) | `CONTROLJOB` (role option) |
| triaging-live-sql-activity | `VIEWACTIVITY` or `VIEWACTIVITYREDACTED` (system privilege) | `CANCELQUERY`, `CANCELSESSION` (system privileges) |
| profiling-statement-fingerprints | `VIEWACTIVITY` or `VIEWACTIVITYREDACTED` (system privilege) | N/A (read-only) |

**Key takeaway:** Job monitoring uses a different privilege model (VIEWJOB + CONTROLJOB role option) than query monitoring (VIEWACTIVITY + CANCELQUERY/CANCELSESSION).

## References

**Official CockroachDB Documentation:**
- [Authorization Overview](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html)
- [GRANT (System Privilege)](https://www.cockroachlabs.com/docs/stable/grant.html)
- [REVOKE (System Privilege)](https://www.cockroachlabs.com/docs/stable/revoke.html)
- [ALTER ROLE](https://www.cockroachlabs.com/docs/stable/alter-role.html)
- [SHOW GRANTS](https://www.cockroachlabs.com/docs/stable/show-grants.html)
- [SHOW USERS](https://www.cockroachlabs.com/docs/stable/show-users.html)
- [CREATE ROLE](https://www.cockroachlabs.com/docs/stable/create-role.html)

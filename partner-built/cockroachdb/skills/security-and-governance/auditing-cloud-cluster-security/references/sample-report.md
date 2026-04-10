# Sample Security Audit Report

This is a sample report generated from an audit of a CockroachDB Cloud development cluster with intentionally insecure configuration. It demonstrates the expected output format, finding categories, severity adjustments, and remediation links.

Use this as a template when producing audit reports. Replace all values with actual findings from the target cluster.

---

# Security Audit Report — example-dev-cluster

**Date:** 2026-02-23
**Cluster ID:** xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
**Plan:** Basic
**CockroachDB Version:** v25.4.5
**Cloud Provider:** AWS
**Regions:** us-east-1
**Deployment:** CockroachDB Cloud
**Environment:** development
**Compliance:** (none specified)
**Data Sensitivity:** internal business data

## Summary

| Status | Count |
|--------|-------|
| PASS   | 1     |
| WARN   | 1     |
| FAIL   | 7     |
| INFO   | 3     |

## Findings

### Network Security

**[WARN] IP allowlist includes 0.0.0.0/0 (open to all traffic)** *(downgraded from FAIL — development cluster)*

The cluster's IP allowlist contains `0.0.0.0/0` ("Default - Allow all"), which permits SQL connections from any IPv4 address. This is the default for new clusters but should be replaced with specific CIDR ranges before production use.

Current allowlist:
| CIDR | Name | SQL | UI |
|------|------|-----|-----|
| 0.0.0.0/0 | Default - Allow all | Yes | No |

**Remediation:** [configuring-ip-allowlists](../../configuring-ip-allowlists/SKILL.md)
- "Explain how to fix this" — The skill walks through listing current entries, identifying authorized CIDR ranges, adding specific entries, and removing `0.0.0.0/0`
- "Help me fix this now" — Interactively add your office/VPN CIDRs and remove the open entry

### Authentication & SSO

**[FAIL] Cloud Console SSO: Not configured**

SSO is not configured for the CockroachDB Cloud organization. Users authenticate with passwords. Check the Cloud Console UI (Organization Settings > Authentication) to verify.

**Remediation:** [configuring-sso-and-scim](../../configuring-sso-and-scim/SKILL.md) — Part 1: Cloud Console SSO

---

**[FAIL] Database SSO (Cluster SSO): Disabled**

```
server.oidc_authentication.enabled = false
```

SQL authentication uses passwords only. Cluster SSO via OIDC is not enabled.

**Remediation:** [configuring-sso-and-scim](../../configuring-sso-and-scim/SKILL.md) — Part 2: Database SSO

---

**[FAIL] SCIM 2.0 provisioning: Not configured**

SCIM automated user provisioning is not enabled. User lifecycle (creation, deactivation) must be managed manually. Check the Cloud Console UI (Organization Settings > Authentication > SCIM) to verify.

**Remediation:** [configuring-sso-and-scim](../../configuring-sso-and-scim/SKILL.md) — Part 3: SCIM 2.0

---

**[FAIL] Auto user provisioning: Not configured**

```
server.identity_map.configuration = '' (empty)
```

SQL users are not automatically provisioned from IdP identities. Users must be created manually via `CREATE USER` or `ccloud cluster user create`.

**Remediation:** [configuring-sso-and-scim](../../configuring-sso-and-scim/SKILL.md) — Part 4: Auto User Provisioning

### Authorization

**[FAIL] Admin user count: 8 users with admin role**

| Admin User | Member Of |
|------------|-----------|
| cluster_admin | {admin} |
| root | {admin} |
| test_admin_1 | {admin} |
| test_admin_2 | {admin} |
| test_admin_3 | {admin} |
| test_admin_4 | {admin} |
| test_admin_5 | {admin} |
| test_admin_6 | {admin} |

8 users have the admin role. The threshold for FAIL is 6+. Only 1-2 admin users are recommended for production clusters. Each admin user should have a documented justification.

**Remediation:** [hardening-user-privileges](../../hardening-user-privileges/SKILL.md)
- Create purpose-specific roles (analyst_reader, app_service, ops_triage)
- Reassign users to appropriate roles
- Revoke admin from users who don't need full cluster control

---

**[FAIL] PUBLIC role has SELECT on application tables**

The PUBLIC role has SELECT granted on `test_db.public.test_table`. This means any authenticated user can read this table regardless of their role assignments.

| Database | Schema | Object | Type | Privilege |
|----------|--------|--------|------|-----------|
| test_db | public | test_table | table | SELECT |

Note: `SHOW GRANTS FOR public` is scoped to the current database. The audit checked `defaultdb` and `test_db`. The `defaultdb` PUBLIC grants on `crdb_internal`, `information_schema`, and `pg_catalog` system tables are default and expected.

**Remediation:** [hardening-user-privileges](../../hardening-user-privileges/SKILL.md)
```sql
-- Revoke PUBLIC SELECT on application tables
REVOKE SELECT ON TABLE test_db.public.test_table FROM public;
```

### Encryption

**[INFO] CMEK: Basic plan — upgrade required**

This cluster is on the Basic plan. Customer-Managed Encryption Keys (CMEK) require the Advanced plan with the Advanced Security Add-on. Data at rest is encrypted using CockroachDB-managed keys.

To enable CMEK:
1. Upgrade to the Advanced plan
2. Enable the Advanced Security Add-on
3. Follow [enabling-cmek-encryption](../../enabling-cmek-encryption/SKILL.md)

---

**[PASS] TLS: Enforced on all connections**

CockroachDB Cloud enforces TLS on all SQL and UI connections by default. No action needed.

### Audit Logging

**[FAIL] Audit logging is disabled**

```
sql.log.user_audit = '' (empty — disabled)
sql.log.admin_audit.enabled = false
```

Neither user audit logging nor admin audit logging is enabled. No SQL activity is being recorded for security review.

**Remediation:** [configuring-audit-logging](../../configuring-audit-logging/SKILL.md)
```sql
-- Minimum recommended: enable admin audit logging
SET CLUSTER SETTING sql.log.admin_audit.enabled = true;

-- Recommended: add role-based audit logging for sensitive data access
SET CLUSTER SETTING sql.log.user_audit = 'sensitive_data_reader ALL';
```

### Password Policy

**[FAIL] Minimum password length is 1 (effectively no minimum)**

```
server.user_login.min_password_length = 1
```

The minimum password length is set to 1, which effectively disables password length enforcement. NIST 800-63B and SOC 2 recommend a minimum of 8 characters; 12+ is best practice.

**Remediation:** [enforcing-password-policies](../../enforcing-password-policies/SKILL.md)
```sql
-- Set minimum password length to 12 (recommended)
SET CLUSTER SETTING server.user_login.min_password_length = 12;
```

### Backup & Recovery

**[INFO] Managed backups: Auto-enabled**

CockroachDB Cloud automatically manages backups for all clusters. No user configuration is required. Backup frequency and retention are managed by the platform.

### Cluster Configuration

**[INFO] Cluster details**

| Property | Value |
|----------|-------|
| Name | example-dev-cluster |
| Plan | Basic |
| Cloud Provider | AWS |
| Region | us-east-1 |
| CockroachDB Version | v25.4.5 |
| Network Visibility | PUBLIC |
| Delete Protection | DISABLED |
| State | CREATED |

## Remediation Summary

Ordered by priority (highest risk first):

| # | Finding | Severity | Remediation Skill | Quick Fix |
|---|---------|----------|-------------------|-----------|
| 1 | IP allowlist 0.0.0.0/0 | WARN | [configuring-ip-allowlists](../../configuring-ip-allowlists/SKILL.md) | Add specific CIDRs, remove 0.0.0.0/0 |
| 2 | 8 admin users | FAIL | [hardening-user-privileges](../../hardening-user-privileges/SKILL.md) | Create roles, revoke admin |
| 3 | PUBLIC has SELECT | FAIL | [hardening-user-privileges](../../hardening-user-privileges/SKILL.md) | `REVOKE SELECT ... FROM public` |
| 4 | Audit logging disabled | FAIL | [configuring-audit-logging](../../configuring-audit-logging/SKILL.md) | Enable admin + role-based audit |
| 5 | Password min length = 1 | FAIL | [enforcing-password-policies](../../enforcing-password-policies/SKILL.md) | Set min length to 12 |
| 6 | SSO not configured | FAIL | [configuring-sso-and-scim](../../configuring-sso-and-scim/SKILL.md) | Configure SAML/OIDC SSO |
| 7 | SCIM not enabled | FAIL | [configuring-sso-and-scim](../../configuring-sso-and-scim/SKILL.md) | Enable SCIM endpoint |
| 8 | Database SSO disabled | FAIL | [configuring-sso-and-scim](../../configuring-sso-and-scim/SKILL.md) | Enable Cluster SSO |
| 9 | CMEK not available | INFO | [enabling-cmek-encryption](../../enabling-cmek-encryption/SKILL.md) | Upgrade to Advanced plan |

## How to Use This Report

For each FAIL finding above, you have two options:

1. **"Explain how to fix this"** — Open the linked remediation skill and read the steps. The skill provides full context, prerequisites, safety considerations, and rollback instructions.

2. **"Help me fix this now"** — Ask Claude to walk through the remediation interactively. For example:
   - "Help me fix the IP allowlist using the configuring-ip-allowlists skill"
   - "Help me reduce the admin user count using the hardening-user-privileges skill"
   - "Help me enable audit logging using the configuring-audit-logging skill"

After remediating findings, re-run the audit to verify all checks now show PASS.

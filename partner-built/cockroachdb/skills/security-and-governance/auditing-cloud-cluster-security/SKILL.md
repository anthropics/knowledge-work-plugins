---
name: auditing-cloud-cluster-security
description: Audits the security posture of a CockroachDB cluster (Cloud or self-hosted) across network, authentication, authorization, encryption, audit logging, and backup dimensions. Use when assessing cluster security readiness, preparing for compliance reviews, or investigating security configuration gaps.
compatibility: Requires ccloud CLI authenticated via `ccloud auth login` and SQL access via cockroach sql with admin or VIEWACTIVITY privilege.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Auditing Cloud Cluster Security

Assesses the security posture of a CockroachDB Cloud cluster by examining network access controls, authentication and SSO configuration, user authorization, encryption, audit logging, and backup status. Produces a structured PASS/WARN/FAIL report with remediation links for each finding. Supports both CockroachDB Cloud and self-hosted clusters — checks that don't apply to the deployment model are marked N/A.

**Read-only audit:** All operations are read-only. No cluster state is modified during the assessment.

## When to Use This Skill

- Preparing for SOC 2, HIPAA, or other compliance reviews
- Conducting periodic security posture assessments
- Onboarding a new production cluster and validating security baseline
- Investigating security configuration gaps after an incident
- Reviewing cluster security before a major release or customer onboarding

## Prerequisites

**Tools:**

| Tool | Cloud | Self-Hosted | Purpose |
|------|-------|-------------|---------|
| `ccloud` CLI | Required | N/A | Cluster metadata, network config, CMEK |
| `cockroach sql` | Required | Required | SQL security checks |
| `openssl` (v3+) | Recommended | Recommended | TLS/PQC cipher probing (`-starttls postgres`) |
| `sslyze` | Optional | Optional | Comprehensive TLS enumeration (`--starttls postgres`) |

**Credentials:**

| Credential | Cloud | Self-Hosted |
|---|---|---|
| `ccloud auth login` session | Required | N/A |
| SQL connection string | Required (from `ccloud cluster sql --url`) | Required (user provides) |
| DB username/password | Required (admin or VIEWACTIVITY) | Required (admin or VIEWACTIVITY) |
| TLS certificates directory | N/A (managed) | Required for cert expiry checks |
| CA certificate file | N/A | Required for `openssl` TLS probing |

See [permissions reference](references/permissions.md) for detailed privilege requirements.

## Security Audit Dimensions

| Dimension | Tool | Checks |
|-----------|------|--------|
| Network Security | ccloud | IP allowlists, private endpoints |
| Authentication & SSO | ccloud + sql | Cloud Console SSO, Database SSO (Cluster SSO), SCIM 2.0 provisioning, auto user provisioning |
| Authorization | sql | Users, roles, admin grants, PUBLIC privileges |
| Encryption | ccloud + sql | CMEK status, TLS settings |
| Audit Logging | sql | Audit log config, session logging |
| Backup & Recovery | ccloud + sql | Managed backup status, self-managed backup schedules |
| Cryptographic Posture | sql + openssl + sslyze | TLS version, PQC hybrid cipher support, encryption key size |
| Cluster Context | ccloud + user input | Deployment model, environment, compliance, data sensitivity |
| Cluster Configuration | ccloud | Version, plan, regions |

## Assessment Workflow

### Step 0: Verify Prerequisites

Run the following checks to determine which tools are available. The audit proceeds regardless — missing tools degrade specific checks rather than blocking the audit.

**Cloud clusters:**
```bash
# Verify ccloud authentication
ccloud auth whoami

# Verify cluster access
ccloud cluster list -o json
```

**Both deployment models:**
```bash
# Verify SQL connectivity
cockroach sql --url "<connection-string>" -e "SELECT current_user();"

# Check openssl version (v3+ recommended for PQC probes)
openssl version

# Check sslyze availability
which sslyze && sslyze --version
```

**Report tool availability before proceeding:**

| Tool | Status | Impact if Missing |
|------|--------|-------------------|
| `ccloud` | Available / Missing | Network, CMEK, and managed backup checks skipped (Cloud only) |
| `cockroach sql` | Available / Missing | **All SQL-based checks skipped** — audit severely limited |
| `openssl` (v3+) | Available / Missing | TLS cipher and PQC probing degraded |
| `sslyze` | Available / Missing | Comprehensive TLS enumeration unavailable; falls back to `openssl` |

If `cockroach sql` is unavailable, warn the user that the audit will be limited to `ccloud`-only checks and recommend resolving connectivity before continuing. For missing optional tools (`openssl`, `sslyze`), note which checks will produce incomplete results and proceed.

### Step 1: Gather Cluster Metadata and Confirm Audit Context

**Cloud clusters:**
```bash
# List clusters and identify target
ccloud cluster list -o json

# Get cluster details (use cluster name or ID)
ccloud cluster info <cluster-name> -o json
```

**Self-hosted clusters:**
```bash
# Gather metadata via SQL and cockroach CLI
cockroach node status --certs-dir=<certs-dir> --host=<host>
cockroach sql --url "<connection-string>" -e "SELECT version();"
```

Record: cluster ID, plan type (Basic/Standard/Advanced or self-hosted), cloud provider, regions, CockroachDB version. See [ccloud commands reference](references/ccloud-commands.md) for Cloud CLI syntax.

**Confirm audit context:** Present auto-detected metadata (cluster name, version, provider, regions, plan) and ask the user to confirm and provide:

1. **Deployment model:** CockroachDB Cloud / self-hosted
2. **Environment:** production / staging / development / sandbox
3. **Compliance frameworks:** SOC 2, HIPAA, PCI DSS, ISO 27001, GDPR, or none
4. **Data sensitivity:** PII/PHI, financial/payment, internal business, public/non-sensitive

**Defaults** (if user confirms without changes): Cloud, production, no compliance, internal business data. Deployment model determines check applicability (below). Environment and compliance calibrate severity (see Severity Adjustments).

### Check Applicability by Deployment Model

| Check | Cloud | Self-Hosted |
|-------|-------|-------------|
| IP allowlists (ccloud) | Yes (all tiers) | N/A — managed externally via firewall/VPC |
| Ingress Private Endpoints (ccloud) | Yes (Standard+, Advanced) | N/A |
| Egress Private Endpoints (ccloud) | Yes (Advanced) | N/A |
| HBA configuration (SQL) | Yes | Yes — primary network-level auth control |
| Cloud Console SSO | Yes | N/A |
| SCIM 2.0 | Yes | N/A |
| Database SSO (OIDC) | Yes | Yes |
| Database SSO (LDAP/AD) | Yes | Yes |
| Users & Roles (SQL) | Yes | Yes |
| Privileges (SQL) | Yes | Yes |
| CMEK (ccloud) | Yes | N/A — check Enterprise Encryption instead |
| Enterprise Encryption | N/A | Yes — verify encryption-at-rest via store config |
| TLS | Always PASS (enforced) | Check — verify certs, expiry, config |
| TLS 1.3 / PQC / Key Size | Yes (INFO) | Yes (INFO) |
| Audit Logging (SQL) | Yes | Yes |
| Managed Backups (ccloud) | Yes (automatic) | N/A |
| Self-Managed Backups (SQL) | Optional (if managed backups present) | Yes — verify backup schedules exist and are running |

Skip N/A checks for the detected deployment model and mark them as `[N/A]` in the report rather than PASS/FAIL.

### Step 2: Assess Network Security

**Cloud clusters:** Check all three layers based on cluster tier:

```bash
# IP allowlists (all tiers)
ccloud cluster networking allowlist list <cluster-id> -o json

# Ingress private endpoints (Standard+, Advanced) — via Cloud Console or API
# Cloud Console: Networking > Private endpoint tab
# API: GET /api/v1/clusters/{cluster_id}/networking/private-endpoint-connections

# Egress private endpoints (Advanced only) — via Cloud Console or API
# Cloud Console: Networking > Egress tab
# API: GET /api/v1/clusters/{cluster_id}/networking/egress-endpoints
```

```sql
-- HBA configuration (all tiers)
SHOW CLUSTER SETTING server.host_based_authentication.configuration;
```

**Evaluate (Cloud):**
- **FAIL** if `0.0.0.0/0` is in the IP allowlist (open to all traffic)
- **WARN** if allowlist contains broad CIDR ranges (e.g., `/8` or `/16`)
- **WARN** if no private endpoints configured on Advanced plan
- **INFO** if private endpoints not available on current tier
- **PASS** if allowlist contains only specific, narrow CIDR ranges or private endpoints are configured

**Self-hosted clusters:** Check HBA configuration as the primary network-level auth control:

```sql
SHOW CLUSTER SETTING server.host_based_authentication.configuration;
```

**Evaluate (self-hosted):**
- **WARN** if HBA configuration is empty or default — network security may be managed externally (firewalls, security groups, VPCs), so this is WARN not FAIL
- **PASS** if HBA rules restrict connections by IP, subnet, or auth method

### Step 3: Check SSO and SCIM Configuration

> For self-hosted clusters, skip Cloud Console SSO and SCIM checks (N/A). Database SSO checks still apply — check OIDC and/or LDAP/AD configuration.

**Cloud Console SSO** (Cloud Console UI > Organization Settings > Authentication — not via ccloud CLI):
- **FAIL** if SSO is not configured
- **PASS** if SAML or OIDC SSO is enabled and enforced

**Database SSO (Cluster SSO) — OIDC:**
```sql
-- Check if Cluster SSO is enabled for SQL authentication
SHOW CLUSTER SETTING server.oidc_authentication.enabled;
SHOW CLUSTER SETTING server.oidc_authentication.provider_url;
```
- **FAIL** if `server.oidc_authentication.enabled` is `false`
- **PASS** if enabled with a valid provider URL

**Database SSO — LDAP/AD (Cloud and self-hosted):**
```sql
-- Check if LDAP authentication is configured via HBA
SHOW CLUSTER SETTING server.host_based_authentication.configuration;
-- Look for ldap auth method entries in the HBA configuration
```
- **PASS** if HBA contains entries with `ldap` auth method
- **INFO** if LDAP is not configured (OIDC may be used instead)

**SCIM 2.0** (Cloud Console UI > Organization Settings > Authentication > SCIM):
- **FAIL** if SCIM endpoint is not enabled; **PASS** if enabled and connected to an IdP

**Auto user provisioning on Database:**
```sql
-- Check if SQL users are automatically provisioned from SSO identities
SHOW CLUSTER SETTING server.identity_map.configuration;
```
- **FAIL** if identity mapping is not configured
- **PASS** if identity mapping routes IdP identities to SQL users

### Step 4: Audit Users and Roles

```sql
-- List all users and their roles
SELECT
  username,
  options,
  member_of
FROM [SHOW USERS]
ORDER BY username;
```

See [SQL queries reference](references/sql-queries.md) for additional role audit queries.

### Step 5: Check Privileges

```sql
-- Count admin role members
SELECT COUNT(*) AS admin_count
FROM [SHOW GRANTS ON ROLE admin];

-- Check PUBLIC role privileges on the current database
-- Note: SHOW GRANTS FOR public is scoped to the current database.
-- Run this query from each application database to get full coverage.
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

**Important:** `SHOW GRANTS FOR public` is scoped to the current database. Run `SHOW DATABASES;` and repeat the query from each database for full coverage.

**Evaluate:**
- **FAIL** if more than 5 users have admin role
- **FAIL** if PUBLIC has SELECT, INSERT, UPDATE, or DELETE on application tables
- **WARN** if admin count is between 3 and 5
- **PASS** if admin count is 1-2 and PUBLIC has minimal grants

### Step 6: Verify Encryption

**CMEK status (Cloud clusters):**
```bash
# Check CMEK configuration (Advanced plan with Advanced Security Add-on)
ccloud cluster info <cluster-name> -o json
# Look for cmek_config in the output
```

**Evaluate by plan type (Cloud):**
- **Standard plan:** INFO — "Upgrade to Advanced plan with Advanced Security Add-on to enable CMEK"
- **Advanced plan without Advanced Security Add-on:** INFO — "Add Advanced Security Add-on to enable CMEK"
- **Advanced plan with Advanced Security Add-on, CMEK not enabled:** FAIL — CMEK not enabled despite plan supporting it
- **Advanced plan with Advanced Security Add-on, CMEK enabled:** PASS

**Enterprise Encryption (self-hosted — skip CMEK, check this instead):**
```bash
# Enterprise Encryption is configured via --enterprise-encryption flag at node startup
cockroach node status --certs-dir=<certs-dir> --host=<host> --format=records
```
```sql
SHOW CLUSTER SETTING enterprise.encryption.type;
```
- **FAIL** if not enabled and cluster stores sensitive data
- **WARN** if encryption status cannot be determined
- **PASS** if enabled with AES-256

**TLS (Cloud):** Always PASS — enforced on all connections.

**TLS (self-hosted):** Verify certificate validity and expiry (NOT auto-PASS):
```bash
cockroach cert list --certs-dir=<certs-dir>
openssl x509 -in <certs-dir>/node.crt -noout -enddate
```
- **FAIL** if any certificate expires within 30 days
- **WARN** if any certificate expires within 90 days
- **PASS** if all certificates valid with 90+ days remaining

**Remediation (self-hosted):** [managing-tls-certificates](../managing-tls-certificates/SKILL.md)

**Cryptographic posture (both Cloud and self-hosted — informational only):**
```bash
# Primary: sslyze with STARTTLS postgres (if available)
sslyze <host>:26257 --starttls postgres

# Supplementary: openssl with STARTTLS postgres
openssl s_client -connect <host>:26257 -starttls postgres -showcerts -tlsextdebug 2>&1

# PQC probe: offer ML-KEM hybrid, check if server accepts
openssl s_client -connect <host>:26257 -starttls postgres -groups X25519MLKEM768:x25519 2>&1
```
- **INFO** — TLS version (should be TLS 1.3; note if TLS 1.2 only)
- **INFO** — PQC hybrid cipher support (e.g., X25519MLKEM768) — emerging, not yet a FAIL condition
- **INFO** — Encryption key size (check for AES-256; note if AES-128)

> **Note:** CockroachDB uses PostgreSQL wire protocol, so `openssl s_client` requires `-starttls postgres` to negotiate TLS correctly. Without this flag, the connection will fail. `sslyze` similarly requires `--starttls postgres`.

### Step 7: Check Audit Logging

```sql
-- Check audit log configuration
SHOW CLUSTER SETTING sql.log.user_audit;

-- Check admin audit logging
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;
```

**Evaluate:**
- **FAIL** if `sql.log.user_audit` is empty and `sql.log.admin_audit.enabled` is `false`
- **WARN** if only admin audit is enabled but user audit is not configured
- **PASS** if both user and admin audit logging are configured

### Step 8: Assess Backup Status

**Cloud clusters:** Managed backups are automatic — always PASS. Optionally check for self-managed schedules:
```bash
ccloud cluster info <cluster-name> -o json  # Look for backup_config
```
```sql
SHOW SCHEDULES;  -- Check for additional self-managed backup schedules
```

**Self-hosted clusters:** No managed backups — verify self-managed backup schedules:
```sql
SHOW SCHEDULES;
SELECT id, label, schedule_status, next_run, created
FROM [SHOW SCHEDULES]
WHERE label ILIKE '%backup%' OR command @> '{"backup":{}}';
```
- **FAIL** if no backup schedules exist
- **WARN** if schedules exist but show errors or haven't run recently
- **PASS** if schedules are active and running

**Remediation (self-hosted):**
```sql
CREATE SCHEDULE 'nightly-full-backup'
  FOR BACKUP INTO 'gs://bucket/backups'
  RECURRING '@daily'
  WITH SCHEDULE OPTIONS first_run = 'now';
```

## Pass/Warn/Fail Criteria

| Check | PASS | WARN | FAIL |
|-------|------|------|------|
| IP Allowlist | Specific CIDRs only | Broad ranges (/8, /16) | `0.0.0.0/0` present |
| Cloud Console SSO | SSO enabled + enforced | SSO enabled, not enforced | Not configured |
| Database SSO | Cluster SSO enabled | — | Not configured |
| SCIM 2.0 | SCIM enabled + connected | — | Not enabled |
| DB Auto User Provisioning | Identity mapping configured | — | Not configured |
| Admin Users | 1-2 admins | 3-5 admins | 6+ admins |
| PUBLIC Privileges | No data grants | USAGE-only grants | SELECT/INSERT/UPDATE/DELETE |
| CMEK (Standard) | N/A | — | — (INFO: upgrade path) |
| CMEK (Advanced + Security Add-on) | CMEK enabled | — | Not enabled |
| Enterprise Encryption (self-hosted) | AES-256 enabled | Cannot determine | Not enabled (sensitive data) |
| TLS (self-hosted) | Certs valid 90+ days | Certs expire in 30-90 days | Certs expire within 30 days |
| TLS 1.3 / PQC / Key Size | — | — | — (INFO only) |
| HBA (self-hosted) | Restrictive rules | Empty/default | — |
| Audit Logging | User + admin audit on | Admin audit only | Disabled |
| Password Policy | min length >= 12 | min length 8-11 | min length < 8 |
| Backups (Cloud) | N/A | — | — (INFO: managed) |
| Backups (self-hosted) | Schedules active | Schedules have errors | No schedules exist |

## Severity Adjustments by Environment

Severity is calibrated for production by default. Non-production environments downgrade some findings. Compliance requirements override downgrades.

| Check | Production | Staging | Development | Sandbox |
|-------|-----------|---------|-------------|---------|
| IP allowlist `0.0.0.0/0` (Cloud) | FAIL | FAIL | WARN | WARN |
| No private endpoints on Advanced (Cloud) | WARN | WARN | INFO | INFO |
| Empty HBA conf (self-hosted) | WARN | WARN | INFO | INFO |
| SSO not configured | FAIL | FAIL | INFO | INFO |
| SCIM not enabled | FAIL | FAIL | INFO | INFO |
| Database SSO disabled | FAIL | FAIL | INFO | INFO |
| Admin count 6+ | FAIL | FAIL | WARN | WARN |
| CMEK not enabled (Cloud) | FAIL | FAIL | WARN | WARN |
| Enterprise Encryption not enabled (self-hosted) | FAIL | FAIL | WARN | WARN |
| Audit logging disabled | FAIL | FAIL | WARN | INFO |
| No backup schedules (self-hosted) | FAIL | FAIL | WARN | INFO |

**Compliance overrides** — these checks cannot be downgraded when a compliance framework is specified (compliance takes precedence over environment):

| Framework | Non-Downgradable Checks |
|-----------|------------------------|
| SOC 2 | SSO, audit logging, admin users, password policy |
| HIPAA | SSO, CMEK/Enterprise Encryption, audit logging, encryption, password policy, backups |
| PCI DSS | IP allowlist/HBA, CMEK/Enterprise Encryption, audit logging, admin users, password policy, backups |
| ISO 27001 | SSO, audit logging, admin users |
| GDPR | Audit logging, encryption |

**Annotations:** `*(downgraded from FAIL — development cluster)*` or `*(PCI DSS compliance — cannot downgrade)*`

## Report Format

Save each audit report to `reports/security-audit-<cluster-name>-<YYYY-MM-DD>-<sequence>.md` (gitignored, local-only). The `reports/` directory is not committed to version control — it serves as a local log for historical comparison and remediation tracking.

Generate a markdown report with the following structure:

```
# Security Audit Report — <Cluster Name>

**Date:** YYYY-MM-DD
**Cluster ID:** <cluster-id>
**Plan:** Standard | Advanced | Self-hosted
**CockroachDB Version:** vXX.X.X
**Regions:** us-east-1, us-west-2
**Deployment:** CockroachDB Cloud | Self-hosted
**Environment:** production | staging | development | sandbox
**Compliance:** SOC 2, PCI DSS | (none specified)
**Data Sensitivity:** PII/PHI | financial | internal | public

## Summary

| Status | Count |
|--------|-------|
| PASS   | X     |
| WARN   | X     |
| FAIL   | X     |
| INFO   | X     |
| N/A    | X     |

## Findings

### Network Security
- [PASS|WARN|FAIL|N/A] IP allowlist: <details>
- [PASS|WARN|INFO|N/A] Private endpoints: <details>
- [PASS|WARN|N/A] HBA configuration: <details>

### Authentication & SSO
- [PASS|FAIL|N/A] Cloud Console SSO: <details>
- [PASS|FAIL] Database SSO (OIDC): <details>
- [PASS|INFO] Database SSO (LDAP/AD): <details>
- [PASS|FAIL|N/A] SCIM 2.0 provisioning: <details>
- [PASS|FAIL] Auto user provisioning: <details>

### Authorization
- [PASS|WARN|FAIL] Admin user count: X users with admin role
- [PASS|FAIL] PUBLIC role privileges: <details>

### Encryption
- [PASS|FAIL|INFO|N/A] CMEK: <details>
- [PASS|FAIL|WARN|N/A] Enterprise Encryption: <details>
- [PASS|FAIL|N/A] TLS: <details>
- [INFO] Cryptographic posture: TLS version, PQC support, key size

### Audit Logging
- [PASS|WARN|FAIL] Audit log configuration: <details>

### Backup & Recovery
- [PASS|INFO|N/A] Managed backups: <details>
- [PASS|WARN|FAIL|N/A] Self-managed backups: <details>

### Cluster Configuration
- [INFO] Version: vXX.X.X
- [INFO] Plan: Standard | Advanced | Self-hosted
- [INFO] Regions: <list>
```

**Status markers:** `[PASS]`, `[WARN]`, `[FAIL]`, `[INFO]`, `[N/A]`. Use `[N/A]` for checks that don't apply to the deployment model. Append severity adjustment annotations when applicable (see Severity Adjustments).

## Remediation

For each finding, the corresponding remediation skill can be used independently:

| Finding | Remediation Skill |
|---------|------------------|
| Open IP allowlist | [configuring-ip-allowlists](../configuring-ip-allowlists/SKILL.md) |
| SSO not configured / SCIM not enabled | [configuring-sso-and-scim](../configuring-sso-and-scim/SKILL.md) |
| CMEK not enabled | [enabling-cmek-encryption](../enabling-cmek-encryption/SKILL.md) |
| Audit logging disabled | [configuring-audit-logging](../configuring-audit-logging/SKILL.md) |
| Excessive admin privileges | [hardening-user-privileges](../hardening-user-privileges/SKILL.md) |
| Weak password policy | [enforcing-password-policies](../enforcing-password-policies/SKILL.md) |
| TLS/certificate issues | [managing-tls-certificates](../managing-tls-certificates/SKILL.md) |
| No private connectivity | [configuring-private-connectivity](../configuring-private-connectivity/SKILL.md) |
| Log export not configured | [configuring-log-export](../configuring-log-export/SKILL.md) |
| Compliance gaps | [preparing-compliance-documentation](../preparing-compliance-documentation/SKILL.md) |

For each FAIL finding, offer: **"Explain how to fix this"** (step-by-step guidance) or **"Help me fix this now"** (interactive remediation).

## Safety Considerations

- **All operations are read-only.** No cluster settings, users, roles, or network configurations are modified during the audit.
- **SQL queries use SHOW and SELECT only.** No DDL or DML statements are executed.
- **ccloud commands are read-only.** Only `list`, `info`, and `auth` subcommands are used.
- **No secrets are logged.** Connection strings and tokens are not included in the report output.
- **Privilege check:** The audit may produce incomplete results if the executing user lacks admin or VIEWACTIVITY privilege. The report notes any permission gaps.

## References

**Skill references:**
- [Sample audit report](references/sample-report.md) — Example report with findings and remediation links
- [SQL queries for security auditing](references/sql-queries.md)
- [ccloud CLI commands](references/ccloud-commands.md)
- [RBAC and privileges setup](references/permissions.md)

**Remediation skills:**
- [configuring-ip-allowlists](../configuring-ip-allowlists/SKILL.md) — Network access hardening
- [enabling-cmek-encryption](../enabling-cmek-encryption/SKILL.md) — Customer-managed encryption keys
- [configuring-audit-logging](../configuring-audit-logging/SKILL.md) — SQL audit logging
- [hardening-user-privileges](../hardening-user-privileges/SKILL.md) — RBAC tightening
- [enforcing-password-policies](../enforcing-password-policies/SKILL.md) — Password strength enforcement
- [configuring-sso-and-scim](../configuring-sso-and-scim/SKILL.md) — SSO and SCIM provisioning
- [managing-tls-certificates](../managing-tls-certificates/SKILL.md) — TLS certificate management
- [configuring-private-connectivity](../configuring-private-connectivity/SKILL.md) — Private endpoints and VPC peering
- [configuring-log-export](../configuring-log-export/SKILL.md) — Log and metric export
- [preparing-compliance-documentation](../preparing-compliance-documentation/SKILL.md) — Compliance readiness and documentation

**Official CockroachDB Documentation:**
- [CockroachDB Cloud Security Overview](https://www.cockroachlabs.com/docs/cockroachcloud/security-overview.html)
- [Managing IP Allowlists](https://www.cockroachlabs.com/docs/cockroachcloud/network-authorization.html)
- [Cloud Console SSO](https://www.cockroachlabs.com/docs/cockroachcloud/cloud-org-sso.html)
- [Cluster SSO (Database SSO)](https://www.cockroachlabs.com/docs/stable/sso-sql.html)
- [SCIM Provisioning](https://www.cockroachlabs.com/docs/cockroachcloud/configure-scim-provisioning)
- [CMEK Overview](https://www.cockroachlabs.com/docs/cockroachcloud/cmek.html)
- [Audit Logging](https://www.cockroachlabs.com/docs/stable/sql-audit-logging.html)
- [Security Reference: Authorization](https://www.cockroachlabs.com/docs/stable/security-reference/authorization.html)

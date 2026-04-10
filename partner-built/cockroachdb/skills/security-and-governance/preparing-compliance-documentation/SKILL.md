---
name: preparing-compliance-documentation
description: Guides preparation of compliance documentation for CockroachDB Cloud deployments, covering SOC 2, PCI DSS, ISO 27001, HIPAA, and GDPR certifications. Use when responding to compliance questionnaires, preparing for audits, locating certification documents, or assessing cluster configuration for compliance readiness.
compatibility: Applicable to all CockroachDB Cloud plans. Some compliance features require Advanced plan with security add-ons.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Preparing Compliance Documentation

Guides the preparation of compliance documentation for CockroachDB Cloud deployments by identifying available certifications, mapping security features to compliance controls, and providing a configuration checklist for compliance readiness. Covers SOC 2 Type II, PCI DSS, ISO 27001, HIPAA, and GDPR.

## When to Use This Skill

- Responding to customer security questionnaires about CockroachDB Cloud
- Preparing for SOC 2, PCI DSS, or HIPAA compliance audits
- Locating CockroachDB Cloud certification documents (SOC 2 reports, PCI AOC, ISO certificates)
- Assessing whether a cluster's configuration meets a specific compliance framework
- Understanding which compliance features are available on each CockroachDB Cloud plan

## Prerequisites

- **CockroachDB Cloud account** — Any plan
- **Cloud Console access** — For downloading compliance documents
- **Understanding of your compliance requirements** — Which frameworks apply to your organization

## Steps

### 1. Identify Available Certifications

CockroachDB Cloud maintains the following certifications and attestations:

| Certification | Type | Scope | Where to Find |
|--------------|------|-------|---------------|
| SOC 2 Type II | Attestation report | Cloud infrastructure and operations | Trust Center or request via support |
| PCI DSS | Certificate of Compliance (AOC) | Payment data processing | Trust Center or request via support |
| ISO 27001 | Certification | Information security management | Trust Center or request via support |
| HIPAA | BAA eligibility | Protected health information | Contact sales for BAA execution |
| GDPR | Compliance | EU personal data protection | DPA available on request |

**CockroachDB Cloud Trust Center:** The Trust Center is the primary location for downloading compliance documents. Access it via the Cloud Console or request documents through a support ticket.

### 2. Map Compliance Controls to CockroachDB Features

See [compliance matrix reference](references/compliance-matrix.md) for a detailed mapping of compliance controls to CockroachDB features.

#### SOC 2 — Key Controls

| Control Area | CockroachDB Feature | Configuration Required |
|-------------|---------------------|----------------------|
| Access Control | RBAC, SSO, SCIM | Configure roles, enable SSO |
| Encryption | TLS (always on), CMEK | Enable CMEK on Advanced plan |
| Audit Logging | SQL audit logging, log export | Enable audit logging + log export |
| Network Security | IP allowlists, private endpoints | Configure network restrictions |
| Availability | Multi-region, managed backups | Built-in on all plans |
| Change Management | Cluster versioning, Terraform | Use IaC for cluster management |

#### PCI DSS — Key Requirements

| Requirement | CockroachDB Feature | Notes |
|------------|---------------------|-------|
| Req 1: Network Security | IP allowlists, private endpoints | Restrict access to cardholder data environment |
| Req 3: Protect Stored Data | Encryption at rest (default), CMEK | CMEK provides key control |
| Req 4: Encrypt Transmission | TLS (always on) | Enforced by default |
| Req 7: Restrict Access | RBAC, least privilege | Use hardening-user-privileges skill |
| Req 8: Identify Users | SQL users, SSO, MFA | Enable SSO with MFA at IdP |
| Req 10: Track Access | Audit logging, log export | Enable and export audit logs |

#### HIPAA — Key Safeguards

| Safeguard | CockroachDB Feature | Notes |
|-----------|---------------------|-------|
| Access Control | RBAC, SSO | Implement least privilege |
| Audit Controls | Audit logging, log export | Export to SIEM |
| Integrity | Checksums, replication | Built-in data integrity |
| Transmission Security | TLS (always on) | Enforced by default |
| Encryption | Encryption at rest, CMEK | CMEK for key control |

**HIPAA requirement:** A Business Associate Agreement (BAA) must be executed with Cockroach Labs before storing PHI. Contact your account team to execute a BAA.

### 3. Assess Cluster Configuration for Compliance

Use this checklist to evaluate whether a cluster meets common compliance requirements:

#### Baseline (All Frameworks)

```sql
-- Check password policy
SHOW CLUSTER SETTING server.user_login.min_password_length;
-- Should be >= 12

-- Check admin user count
SELECT COUNT(*) AS admin_count FROM [SHOW GRANTS ON ROLE admin];
-- Should be minimized (1-3)

-- Check audit logging
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;
SHOW CLUSTER SETTING sql.log.user_audit;
-- Should be enabled

-- Check PUBLIC role privileges
SELECT database_name, privilege_type
FROM [SHOW GRANTS FOR public]
WHERE privilege_type NOT IN ('USAGE')
  AND schema_name = 'public';
-- Should return no rows for application databases
```

```bash
# Check network security
ccloud cluster networking allowlist list <cluster-id> -o json
# Should NOT contain 0.0.0.0/0

# Check SSO configuration (Cloud Console)
# Verify in Cloud Console > Organization Settings > Authentication

# Check CMEK (Advanced plan)
ccloud cluster info <cluster-name> -o json
# Check for cmek_config

# Check log export (Advanced plan)
# Look for log_export_config in cluster info output
```

#### Advanced Compliance (SOC 2 + PCI DSS + HIPAA)

| Check | Command/Location | Expected State |
|-------|------------------|----------------|
| SSO enabled | Cloud Console | Enabled and enforced |
| SCIM provisioning | Cloud Console | Enabled |
| CMEK enabled | `ccloud cluster info` | Enabled with valid key |
| Audit logging | SQL: `SHOW CLUSTER SETTING sql.log.admin_audit.enabled` | `true` |
| Log export | `ccloud cluster info` | Configured and ENABLED |
| IP allowlist | `ccloud cluster networking allowlist list` | No 0.0.0.0/0 |
| Private endpoints | Cloud Console: Networking > Private endpoint | Configured (recommended) |
| Password policy | SQL: min_password_length | >= 12 |
| Admin count | SQL: admin role grants | <= 3 |
| PUBLIC privileges | SQL: SHOW GRANTS FOR public | Minimal |

### 4. Respond to Security Questionnaires

When responding to customer or auditor questionnaires, reference these standard answers:

**Encryption at rest:**
- CockroachDB Cloud encrypts all data at rest using AES-256
- CMEK is available on Advanced plan with Advanced Security Add-on for customer-controlled keys
- Key management follows cloud provider best practices (AWS KMS, GCP Cloud KMS, Azure Key Vault)

**Encryption in transit:**
- TLS 1.2+ is enforced on all connections — cannot be disabled
- Client certificate authentication (mTLS) is supported

**Data residency:**
- Clusters can be deployed in specific regions to meet data residency requirements
- Multi-region clusters keep data within specified regions

**Backup and recovery:**
- Managed backups are automatic on all plans
- RPO and RTO depend on plan type and configuration
- Backups are encrypted and stored in the same cloud provider

**Incident response:**
- Cockroach Labs maintains a documented incident response plan
- Details are available in the SOC 2 Type II report

### 5. Prepare for Compliance Audits

**Before the audit:**
1. Run the [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) skill to identify gaps
2. Remediate any FAIL findings using the linked remediation skills
3. Download current compliance documents from the Trust Center
4. Document your CockroachDB Cloud configuration with screenshots or Terraform state

**During the audit:**
1. Provide the SOC 2 Type II report to demonstrate CockroachDB Cloud's controls
2. Show your cluster configuration (security audit report) to demonstrate your controls
3. Demonstrate audit log export and review capability
4. Show RBAC configuration and access control policies

**Compliance documents to have ready:**
- SOC 2 Type II report (from Trust Center)
- PCI AOC (if processing payment data)
- ISO 27001 certificate (if required)
- BAA (if storing PHI — executed with Cockroach Labs)
- DPA (if processing EU personal data)
- Your security audit report (from auditing-cloud-cluster-security skill)

## Safety Considerations

- **This skill is read-only.** No cluster configuration is modified.
- **Compliance documents may be confidential.** Handle SOC 2 reports and PCI AOCs according to your organization's information classification policy.
- **Compliance is shared responsibility.** CockroachDB Cloud provides the platform controls; your organization is responsible for configuring and using them correctly.

## References

**Skill references:**
- [Compliance control matrix](references/compliance-matrix.md)

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Automated security posture assessment
- [configuring-audit-logging](../configuring-audit-logging/SKILL.md) — Enable audit logging for compliance
- [enabling-cmek-encryption](../enabling-cmek-encryption/SKILL.md) — Enable customer-managed encryption keys
- [configuring-sso-and-scim](../configuring-sso-and-scim/SKILL.md) — Enable SSO and automated provisioning
- [hardening-user-privileges](../hardening-user-privileges/SKILL.md) — Implement least-privilege access
- [enforcing-password-policies](../enforcing-password-policies/SKILL.md) — Configure password requirements
- [configuring-ip-allowlists](../configuring-ip-allowlists/SKILL.md) — Network access control
- [configuring-private-connectivity](../configuring-private-connectivity/SKILL.md) — Private network endpoints
- [configuring-log-export](../configuring-log-export/SKILL.md) — Export logs for compliance retention

**Official CockroachDB Documentation:**
- [CockroachDB Cloud Security Overview](https://www.cockroachlabs.com/docs/cockroachcloud/security-overview.html)
- [Compliance](https://www.cockroachlabs.com/docs/cockroachcloud/compliance.html)
- [SOC 2 Compliance](https://www.cockroachlabs.com/docs/cockroachcloud/compliance)

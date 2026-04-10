# Compliance Control Matrix

This reference maps compliance framework controls to CockroachDB Cloud features and configuration requirements.

## Feature Availability by Plan

| Feature | Basic | Standard | Advanced | Advanced + Security Add-on |
|---------|-------|----------|----------|---------------------------|
| TLS encryption (in transit) | Yes | Yes | Yes | Yes |
| Encryption at rest (platform-managed) | Yes | Yes | Yes | Yes |
| IP allowlists | Yes | Yes | Yes | Yes |
| SQL users and RBAC | Yes | Yes | Yes | Yes |
| Password policies | Yes | Yes | Yes | Yes |
| Managed backups | Yes | Yes | Yes | Yes |
| Cloud Console SSO | No | Yes | Yes | Yes |
| Database SSO (Cluster SSO) | No | Yes | Yes | Yes |
| SCIM 2.0 | No | No | Yes | Yes |
| Private endpoints | No | Yes | Yes | Yes |
| VPC peering | No | No | Yes | Yes |
| SQL audit logging | Yes | Yes | Yes | Yes |
| Log export | No | No | Yes | Yes |
| Metric export | No | No | Yes | Yes |
| CMEK | No | No | No | Yes |
| Egress perimeter controls | No | No | Yes | Yes |

## SOC 2 Type II — Control Mapping

### Trust Service Criteria: Security

| Control | TSC Reference | CockroachDB Feature | Minimum Plan |
|---------|--------------|---------------------|--------------|
| Logical access controls | CC6.1 | RBAC, SQL users, roles | Basic |
| Authentication mechanisms | CC6.1 | Password policies, SSO, MFA (via IdP) | Standard (SSO) |
| Network access restrictions | CC6.1 | IP allowlists, private endpoints | Basic (allowlists), Standard (endpoints) |
| Encryption in transit | CC6.1 | TLS 1.2+ (always on) | Basic |
| Encryption at rest | CC6.1 | AES-256 (default), CMEK | Basic (default), Advanced + Security (CMEK) |
| Audit logging | CC7.2 | SQL audit logging, admin audit | Basic |
| Log monitoring | CC7.2 | Log export to SIEM | Advanced |
| Vulnerability management | CC7.1 | Managed patching by Cockroach Labs | Basic |
| Incident response | CC7.3 | Cockroach Labs IR plan (in SOC 2 report) | Basic |
| Backup and recovery | CC7.5 | Managed backups | Basic |

### Trust Service Criteria: Availability

| Control | TSC Reference | CockroachDB Feature | Minimum Plan |
|---------|--------------|---------------------|--------------|
| System redundancy | A1.2 | Multi-node, multi-AZ deployment | Basic |
| Disaster recovery | A1.2 | Managed backups, multi-region | Basic |
| Capacity planning | A1.1 | Auto-scaling, metrics | Basic |

### Trust Service Criteria: Confidentiality

| Control | TSC Reference | CockroachDB Feature | Minimum Plan |
|---------|--------------|---------------------|--------------|
| Data classification | C1.1 | RBAC, schema-level grants | Basic |
| Encryption of confidential data | C1.2 | Encryption at rest + in transit | Basic |
| Key management | C1.2 | CMEK for customer-controlled keys | Advanced + Security |
| Secure disposal | C1.2 | Automatic cleanup on cluster deletion | Basic |

## PCI DSS v4.0 — Requirement Mapping

| Requirement | Description | CockroachDB Feature | Minimum Plan |
|------------|-------------|---------------------|--------------|
| 1 | Install and maintain network security controls | IP allowlists, private endpoints, firewall rules | Basic |
| 2 | Apply secure configurations | Cluster settings hardening, password policies | Basic |
| 3 | Protect stored account data | Encryption at rest, CMEK | Basic (default), Advanced + Security (CMEK) |
| 4 | Protect cardholder data with strong cryptography during transmission | TLS 1.2+ (enforced) | Basic |
| 5 | Protect all systems from malicious software | Managed infrastructure by Cockroach Labs | Basic |
| 6 | Develop and maintain secure systems | Managed patching, version upgrades | Basic |
| 7 | Restrict access to system components by business need | RBAC, least privilege, role-based audit | Basic |
| 8 | Identify users and authenticate access | SQL users, SSO, MFA (via IdP), password policies | Standard (SSO) |
| 9 | Restrict physical access | Cloud provider physical security (AWS/GCP/Azure SOC 2) | Basic |
| 10 | Log and monitor all access | SQL audit logging, admin audit, log export | Basic (logging), Advanced (export) |
| 11 | Test security of systems regularly | Penetration testing (customer responsibility) | N/A |
| 12 | Support information security with policies | Cockroach Labs security policies (in SOC 2) | Basic |

## HIPAA — Safeguard Mapping

| Safeguard | HIPAA Reference | CockroachDB Feature | Minimum Plan |
|-----------|----------------|---------------------|--------------|
| Access control | 164.312(a)(1) | RBAC, unique user IDs, emergency access | Basic |
| Audit controls | 164.312(b) | SQL audit logging, log export | Basic (logging), Advanced (export) |
| Integrity controls | 164.312(c)(1) | Checksums, replication, MVCC | Basic |
| Person or entity authentication | 164.312(d) | Password policies, SSO, certificates | Basic |
| Transmission security | 164.312(e)(1) | TLS 1.2+ (enforced) | Basic |
| Encryption at rest | 164.312(a)(2)(iv) | AES-256, CMEK | Basic |
| Backup and disaster recovery | 164.308(a)(7) | Managed backups | Basic |
| BAA required | 164.502(e) | Available from Cockroach Labs | N/A |

**HIPAA note:** A Business Associate Agreement (BAA) must be executed with Cockroach Labs before storing Protected Health Information (PHI) in CockroachDB Cloud. Contact your Cockroach Labs account team.

## ISO 27001 — Control Mapping

| Control | ISO Reference | CockroachDB Feature | Minimum Plan |
|---------|--------------|---------------------|--------------|
| Access control policy | A.9.1 | RBAC, role hierarchy | Basic |
| User access management | A.9.2 | SQL users, SSO, SCIM | Basic (users), Advanced (SCIM) |
| Cryptographic controls | A.10.1 | TLS, encryption at rest, CMEK | Basic |
| Network security | A.13.1 | IP allowlists, private endpoints | Basic |
| Logging and monitoring | A.12.4 | Audit logging, log export, metrics | Basic (logging), Advanced (export) |
| Information transfer | A.13.2 | TLS (enforced) | Basic |
| Backup | A.12.3 | Managed backups | Basic |

## GDPR — Compliance Considerations

| GDPR Article | Requirement | CockroachDB Feature | Notes |
|-------------|-------------|---------------------|-------|
| Art. 5 | Data processing principles | RBAC, audit logging | Customer responsibility to implement |
| Art. 17 | Right to erasure | SQL DELETE, DROP | Customer implements via SQL |
| Art. 25 | Data protection by design | Encryption, access control | Built-in |
| Art. 28 | Data processing agreement | DPA available | Request from Cockroach Labs |
| Art. 32 | Security of processing | Encryption, access control, backups | Built-in |
| Art. 33 | Breach notification | Cockroach Labs IR plan | Cockroach Labs responsibility for platform |
| Art. 44-49 | International transfers | Region-specific deployments | Deploy in EU regions for EU data |

**Data residency:** CockroachDB Cloud supports deployment in specific regions (EU, US, APAC). Multi-region configurations can be restricted to regions within a single jurisdiction to meet data residency requirements.

## Compliance Readiness Checklist

### Minimum Viable Compliance (All Frameworks)

- [ ] Password minimum length >= 12
- [ ] Admin users <= 3
- [ ] PUBLIC role has no data privileges
- [ ] IP allowlist does not contain 0.0.0.0/0
- [ ] SQL audit logging enabled (admin audit at minimum)

### Enhanced Compliance (SOC 2 + PCI DSS)

All of the above, plus:
- [ ] SSO enabled and enforced
- [ ] SCIM provisioning enabled (if Enterprise plan)
- [ ] Role-based audit logging for sensitive data access
- [ ] Private endpoints configured (eliminates public internet exposure)

### Maximum Compliance (HIPAA + PCI DSS Level 1)

All of the above, plus:
- [ ] CMEK enabled (Advanced plan with Security Add-on)
- [ ] Log export configured (to SIEM or CloudWatch)
- [ ] Metric export configured (to monitoring platform)
- [ ] BAA executed (HIPAA only)
- [ ] DPA executed (GDPR only)
- [ ] Egress perimeter controls configured
- [ ] All data access via private endpoints only

## Notes

- Compliance is a shared responsibility between Cockroach Labs and the customer
- CockroachDB Cloud SOC 2 Type II reports are refreshed annually
- PCI DSS compliance scope depends on how the database is used in the cardholder data environment
- HIPAA compliance requires a BAA before storing PHI
- Feature availability may change — check the CockroachDB Cloud pricing page for current plan features

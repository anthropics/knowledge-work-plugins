---
name: managing-certificates-and-encryption
description: Manages TLS certificate and encryption key lifecycle across all tiers. Self-Hosted covers certificate expiry monitoring, node/CA/client cert rotation, and Kubernetes cert management. Advanced/BYOC covers managed TLS (no action) and CMEK (Customer-Managed Encryption Key) rotation in your KMS. Standard and Basic have fully managed TLS and encryption with no customer action. CMEK is only available on Advanced. Use when monitoring cert health, performing rotation, managing CMEK, or responding to key compromise.
compatibility: Self-Hosted requires SQL admin access and filesystem access for cert rotation. Advanced/BYOC requires Cloud Console for CMEK management. Standard and Basic certificates and encryption are fully managed.
metadata:
  author: cockroachdb
  version: "2.0"
---

# Managing Certificates and Encryption

Manages TLS certificate and encryption key lifecycle across all deployment tiers. Before providing procedures, this skill gathers context to determine whether the operator manages certificates directly (Self-Hosted), manages CMEK encryption keys (Advanced/BYOC), or has fully managed encryption (Standard/Basic).

## When to Use This Skill

- Monitoring certificate expiration (Self-Hosted)
- Performing scheduled certificate rotation (Self-Hosted)
- Managing CMEK encryption keys (Advanced/BYOC)
- Responding to key compromise (Self-Hosted, CMEK)
- Auditing encryption posture for compliance (all tiers)
- Adding DNS names or IPs to node certificates (Self-Hosted)

**For daily health checks:** Use [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md).

---

## Step 1: Gather Context

### Required Context

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Deployment tier?** | Self-Hosted, Advanced, BYOC, Standard, Basic | Determines encryption management responsibility |
| **Reason?** | Routine monitoring, Scheduled rotation, Key compromise, Compliance audit, Add SAN entries | Determines urgency and procedure |

### Additional Context (by tier)

**If Self-Hosted:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Certificate type?** | CA, Node, Client, UI | Different rotation procedures per type |
| **Deployment platform?** | Bare metal/VMs, Kubernetes (Operator/Helm/manual) | Changes rotation tooling |
| **Certificate tooling?** | cockroach cert, openssl, HashiCorp Vault, cert-manager | Determines generation commands |
| **Is the CA being rotated?** | Yes, No | CA rotation requires combined CA approach |

**If Advanced or BYOC:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Is this about CMEK?** | Yes, No | CMEK is the customer's encryption responsibility; TLS is managed by CRL |
| **Cloud provider?** | AWS, GCP, Azure | Determines KMS service and CLI commands |
| **CMEK currently enabled?** | Yes, No | CMEK must be enabled at cluster creation |

**If Standard or Basic:** No context needed — TLS and encryption are fully managed. CMEK is not available on these tiers.

### Context-Driven Routing

| Tier + Scenario | Go To |
|-----------------|-------|
| Self-Hosted | [Self-Hosted Certificate Management](#self-hosted-certificate-management) |
| Advanced/BYOC + CMEK | [CMEK Key Management](#cmek-key-management) |
| Advanced/BYOC + TLS question | [Cloud TLS (Managed)](#cloud-tls-managed) |
| Standard | [Fully Managed Encryption](#fully-managed-encryption) |
| Basic | [Fully Managed Encryption](#fully-managed-encryption) |

---

## Self-Hosted Certificate Management

**Applies when:** Tier = Self-Hosted

### Monitor Certificate Expiry

```sql
SELECT node_id,
  to_timestamp((metrics->>'security.certificate.expiration.ca')::FLOAT)::TIMESTAMPTZ AS ca_expires,
  to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ AS node_cert_expires,
  CASE WHEN to_timestamp((metrics->>'security.certificate.expiration.node')::FLOAT)::TIMESTAMPTZ
            < now() + INTERVAL '90 days' THEN 'EXPIRING_SOON' ELSE 'OK' END AS status
FROM crdb_internal.kv_node_status ORDER BY node_cert_expires;
```

Alert thresholds: CA < 1 year = plan rotation. Node < 90 days = schedule rotation. Node < 30 days = rotate immediately.

### Rotate Node Certificates (Same CA)

```bash
cockroach cert create-node <hostname> <ip> <lb-hostname> <lb-ip> localhost 127.0.0.1 \
  --certs-dir=<certs-dir> --ca-key=<ca-key-path> --overwrite
```

Deploy to node, set `chmod 0600` on key file. CockroachDB auto-detects new certs — no restart required.

See [rotation-procedures reference](references/rotation-procedures.md) for detailed steps and verification.

### Rotate CA Certificate

CA rotation requires a combined certificate (new + old) for seamless trust transition:

1. Generate new CA key and certificate
2. Create combined CA file: `cat new-ca.crt old-ca.crt > ca.crt`
3. Deploy combined CA to all nodes
4. Re-issue node and client certificates signed by the new CA
5. After all entities use new-CA-signed certs, remove old CA from combined file

See [rotation-procedures reference](references/rotation-procedures.md) for the full CA rotation procedure.

### Kubernetes Certificate Management

- **CockroachDB Operator:** Self-signer rotates automatically. Configure via `tls.certs.selfSigner.rotateCerts`.
- **cert-manager:** Auto-renews. Pods may need restart to pick up new certs.

See [kubernetes-certs reference](references/kubernetes-certs.md) for detailed Kubernetes procedures.

---

## CMEK Key Management

**Applies when:** Tier = Advanced or BYOC, CMEK enabled

### What Is CMEK

Customer-Managed Encryption Keys wrap CockroachDB's data-at-rest encryption with a key stored in your cloud provider's KMS. CockroachDB Cloud never has access to the CMEK itself.

CMEK requires an Advanced cluster with advanced security features enabled at cluster creation. It cannot be enabled retroactively. **CMEK is not available on Standard or Basic.**

### Check CMEK Status

```bash
curl -s -H "Authorization: Bearer $COCKROACH_API_KEY" \
  "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/cmek" | jq '.'
```

Or: Cloud Console → Cluster → Security → Encryption.

### Rotate CMEK Key

Rotate the key in your cloud provider's KMS. CockroachDB Cloud automatically uses the new key version. No cluster downtime.

See [cmek-procedures reference](references/cmek-procedures.md) for provider-specific KMS rotation commands (AWS KMS, GCP Cloud KMS, Azure Key Vault) and IAM audit procedures.

### Emergency: Revoke CMEK Key

Revoking the CMEK key makes cluster data **permanently inaccessible** unless the key is restored within your KMS provider's grace period.

**Only use as an emergency kill switch.** This may be irreversible.

---

## Cloud TLS (Managed)

**Applies when:** Tier = Advanced or BYOC, question is about TLS (not CMEK)

TLS certificates are fully managed by Cockroach Labs on Advanced and BYOC:
- Provisioning, rotation, and renewal are automatic
- No customer action needed
- Certificate health is monitored by CRL

**Client certificates:** You manage your own client-side certificates for application connections. These are standard PostgreSQL client certificates.

---

## Fully Managed Encryption

**Applies when:** Tier = Standard or Basic

TLS certificates and data-at-rest encryption are fully managed by Cockroach Labs.
- No certificate visibility or rotation responsibility
- Encryption in transit is always enabled
- Encryption at rest is always enabled
- CMEK is not available on these tiers

**If CMEK is required:** Upgrade to Advanced.

---

## Safety Considerations

**Read-only monitoring queries are safe on all tiers.**

**Self-Hosted certificate operations:**
- Always backup existing certificates before rotation
- Use combined CA approach — never abruptly replace the CA
- Verify SAN entries include ALL hostnames, IPs, and load balancer addresses
- CA key must be stored separately from node certificates
- File permissions: key files must be mode 0600, owned by cockroach process user

**CMEK operations (Advanced/BYOC):**
- CMEK key revocation renders data permanently inaccessible
- Verify IAM permissions before and after KMS key rotation
- Test CMEK rotation in a staging cluster first

See [safety-guide reference](references/safety-guide.md) for detailed risk matrix.

## Troubleshooting

| Issue | Tier | Fix |
|-------|------|-----|
| Cert metric NULL | SH | Verify cluster is in secure mode |
| New cert not detected | SH | Check file permissions (0600, correct owner) |
| "unknown authority" error | SH | Deploy combined CA (new + old) |
| Connection failures after rotation | SH | Check SAN entries cover all hostnames/IPs |
| CMEK access denied | ADV/BYOC | Verify KMS key policy and IAM permissions |
| Cannot enable CMEK | ADV/BYOC | CMEK must be enabled at cluster creation |

## References

**Skill references:**
- [Certificate rotation procedures](references/rotation-procedures.md)
- [Kubernetes certificate management](references/kubernetes-certs.md)
- [CMEK procedures by cloud provider](references/cmek-procedures.md)
- [Safety guide](references/safety-guide.md)

**Related skills:**
- [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md)
- [managing-cluster-settings](../managing-cluster-settings/SKILL.md)

**Official CockroachDB Documentation:**
- [Rotate Security Certificates](https://www.cockroachlabs.com/docs/stable/rotate-certificates)
- [cockroach cert](https://www.cockroachlabs.com/docs/stable/cockroach-cert)
- [TLS and PKI Reference](https://www.cockroachlabs.com/docs/stable/security-reference/transport-layer-security)
- [Manage CMEK](https://www.cockroachlabs.com/docs/cockroachcloud/managing-cmek)

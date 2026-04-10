# Safety Guide: Rotating Security Certificates

## Risk Matrix

| Operation | Risk Level | Reversible? | Impact |
|-----------|-----------|-------------|--------|
| Certificate expiry monitoring (SQL) | None | N/A | Read-only diagnostics |
| Rotate node certificate (same CA) | Low | Yes (restore backup) | No restart needed; auto-detected |
| Rotate client certificate | Low | Yes (restore backup) | Applications must be updated |
| Rotate CA certificate (combined approach) | High | Partial (requires planning) | Multi-step; affects all trust |
| CMEK key rotation in KMS | Low | Yes (previous version retained) | Automatic; no cluster downtime |
| CMEK key revocation | Critical | No (data permanently inaccessible) | Emergency only |
| CMEK key deletion | Critical | No (irreversible after retention period) | Never do without explicit authorization |

## Self-Hosted Certificate Safety

### General Rules

1. **Always backup existing certificates before rotation** — copy `certs-dir` contents to a secure backup location
2. **Never abruptly replace the CA** — always use the combined CA approach (new + old CA in a single file)
3. **Test in staging first** — validate the rotation procedure on a non-production cluster
4. **One certificate type at a time** — don't rotate CA, node, and client certs simultaneously

### Node Certificate Rotation

- CockroachDB auto-detects new node certificates — **no restart required**
- File permissions must be `0600` for key files, owned by the cockroach process user
- SAN entries must include **all** hostnames, IPs, and load balancer addresses
- Missing SAN entries cause `x509: certificate is valid for X, not Y` errors
- Verify rotation via SQL before moving to the next node

### CA Certificate Rotation

This is the highest-risk certificate operation. The combined CA approach prevents trust disruption:

1. Generate new CA key and certificate
2. Create combined CA file: `cat new-ca.crt old-ca.crt > ca.crt`
3. Deploy combined CA to **all** nodes
4. Generate new node certificates signed by new CA
5. Deploy new node certificates to all nodes
6. Generate new client certificates signed by new CA
7. Deploy new client certificates to all applications
8. After all entities use new-CA-signed certs, remove old CA from combined file

**Critical timing:** Steps 2-3 must complete before steps 4-7 begin. The combined CA ensures both old and new certificates are trusted during the transition.

**Failure scenario:** If you replace the CA without the combined approach:
- All existing node-to-node connections fail immediately
- All client connections fail immediately
- Cluster becomes unavailable until certificates are fixed

### Client Certificate Rotation

- Client certificates are deployed to applications, not CockroachDB nodes
- Coordinate rotation with application teams
- Applications need restart or connection pool refresh to pick up new certificates
- Old and new client certificates can coexist if signed by the same (or combined) CA

### File Permission Reference

| File | Required Permission | Owner |
|------|-------------------|-------|
| `ca.crt` | `0644` (readable) | cockroach user |
| `node.crt` | `0644` (readable) | cockroach user |
| `node.key` | `0600` (owner only) | cockroach user |
| `client.*.crt` | `0644` (readable) | application user |
| `client.*.key` | `0600` (owner only) | application user |

### CA Key Storage

- CA private key (`ca.key`) must be stored **separately** from node certificates
- Never deploy `ca.key` to CockroachDB nodes
- Use a secure vault or offline storage for the CA key
- If CA key is compromised, all certificates must be rotated immediately

## CMEK Safety

### Key Rotation

- KMS key rotation is safe — previous key versions are retained automatically
- CockroachDB Cloud uses the new key version for new writes
- Existing data remains accessible via previous key versions
- No cluster downtime during rotation

### Key Revocation (Emergency Only)

**CMEK key revocation makes cluster data permanently inaccessible** unless the key is restored in KMS within the cloud provider's grace period.

- AWS KMS: 7-30 day waiting period before deletion (configurable)
- GCP Cloud KMS: Key versions can be restored if not yet destroyed
- Azure Key Vault: Soft-delete retention period (7-90 days)

**Only revoke CMEK as an emergency kill switch** when data must be rendered immediately inaccessible (e.g., security breach, regulatory requirement).

### IAM Verification

Before and after CMEK key rotation, verify:
- CockroachDB Cloud service account retains `encrypt` and `decrypt` permissions
- Key policy has not been modified during rotation
- Cross-region key access (if applicable) remains configured

## Common Mistakes

| Mistake | Consequence | Prevention |
|---------|------------|------------|
| Replacing CA without combined approach | Cluster-wide connection failure | Always use combined CA (new + old) |
| Wrong file permissions on key files | CockroachDB refuses to start | Set `0600` on all `.key` files |
| Missing SAN entries | TLS handshake failures | Include all hostnames, IPs, LB addresses |
| Deploying CA key to nodes | Security risk — CA key exposure | Store CA key offline or in vault |
| Revoking CMEK without understanding impact | Permanent data loss | Only revoke in verified emergencies |
| Rotating certs during maintenance window | Compounded risk | Separate cert rotation from other maintenance |
| Not backing up certs before rotation | Cannot rollback on failure | Always backup `certs-dir` first |

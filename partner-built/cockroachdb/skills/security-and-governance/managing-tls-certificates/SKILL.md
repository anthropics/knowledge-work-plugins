---
name: managing-tls-certificates
description: Manages TLS certificates for CockroachDB clusters including CA certificate configuration, client certificate authentication, certificate rotation, and troubleshooting SSL/TLS connection errors. Use when setting up client certificate auth, resolving SSL connection failures, rotating certificates, or configuring mTLS for CDC changefeeds.
compatibility: Requires ccloud CLI for Cloud clusters. Requires admin access and cockroach cert CLI for self-hosted clusters.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Managing TLS Certificates

Manages TLS certificates for CockroachDB clusters, covering CA certificate downloads, client certificate authentication setup, certificate rotation, and troubleshooting common SSL/TLS connection errors. Addresses both CockroachDB Cloud (always-on TLS) and self-hosted certificate lifecycle management.

## When to Use This Skill

- Troubleshooting SSL/TLS connection errors from application clients (DBeaver, TypeORM, psql, Go, Python, Java)
- Setting up client certificate authentication on CockroachDB Cloud
- Uploading a custom Client CA to a Cloud cluster
- Rotating or renewing certificates (Cloud or self-hosted)
- Configuring mTLS for CDC changefeeds to Kafka
- Downloading or locating the CA certificate for a Cloud cluster

## Prerequisites

**CockroachDB Cloud:**
- **ccloud CLI** authenticated (`ccloud auth login`)
- **Cloud Console access** for CA certificate download
- **Cluster Admin role** for client CA configuration

**Self-hosted:**
- **cockroach cert** CLI available
- **Admin access** to cluster nodes
- **OpenSSL** for certificate inspection and generation

**Verify access:**
```bash
# Cloud
ccloud auth whoami
ccloud cluster list

# Self-hosted — check existing certificates
cockroach cert list --certs-dir=<certs-directory>
```

## Configuration Decisions

Before proceeding, determine the user's deployment model. Ask which option applies, then follow only the relevant sections below.

**Decision 1 — Deployment model:**
- **CockroachDB Cloud:** TLS is always on and the cluster CA is managed by Cockroach Labs. Follow Part 1 for CA download, client certificate auth, and Cloud certificate rotation.
- **Self-hosted:** Full manual certificate lifecycle management (CA, node, and client certificates). Follow Part 2 for certificate creation, rotation, and management.

Parts 3 (Troubleshooting) and 4 (mTLS for CDC) apply to both deployment models.

## Steps

### Part 1: CockroachDB Cloud TLS

> Follow this part if the user selected **CockroachDB Cloud** in Decision 1.

CockroachDB Cloud enforces TLS on all connections. The cluster CA certificate is managed by Cockroach Labs.

#### 1.1 Download the CA Certificate

The CA certificate is required by clients to verify the cluster's identity.

```bash
# Download via ccloud CLI
ccloud cluster cert <cluster-id>

# Or download from the Cloud Console:
# Cluster > Connect > Download CA Cert
```

The CA certificate is also available at: `https://cockroachlabs.cloud/clusters/<cluster-id>/cert`

**Common CA cert locations after download:**
- macOS: `~/.postgresql/root.crt`
- Linux: `~/.postgresql/root.crt` or `/etc/cockroach-certs/ca.crt`
- Windows: `%APPDATA%\postgresql\root.crt`

#### 1.2 Configure Client Certificate Authentication

Client certificate auth provides mutual TLS (mTLS) — the client proves its identity via certificate instead of a password.

**Step 1: Upload a Client CA to the cluster**

The Client CA signs your client certificates. This is separate from the cluster's CA.

```bash
# Upload a Client CA certificate via ccloud CLI
ccloud cluster cert set-client-ca <cluster-id> --cert-file <client-ca.crt>
```

**Step 2: Create a client certificate signed by your Client CA**

```bash
# Generate a client key and certificate signing request
openssl genrsa -out client.<username>.key 2048
openssl req -new -key client.<username>.key \
  -out client.<username>.csr \
  -subj "/CN=<username>"

# Sign the CSR with your Client CA
openssl x509 -req -in client.<username>.csr \
  -CA client-ca.crt -CAkey client-ca.key \
  -CAcreateserial \
  -out client.<username>.crt \
  -days 365
```

**Step 3: Connect using the client certificate**

```bash
cockroach sql \
  --url "postgresql://<username>@<cluster-host>:26257/defaultdb?sslmode=verify-full&sslrootcert=<ca.crt>&sslcert=client.<username>.crt&sslkey=client.<username>.key"
```

See [connection examples reference](references/connection-examples.md) for client-specific connection strings.

#### 1.3 Certificate Rotation (Cloud)

Client certificates should be rotated before expiry. The cluster CA certificate is managed by Cockroach Labs and rotated automatically.

**Client certificate rotation:**
1. Generate a new client certificate signed by the same Client CA (or a new Client CA)
2. Deploy the new certificate to application clients
3. Verify connections work with the new certificate
4. Remove the old certificate from application clients

**Client CA rotation:**
1. Generate a new Client CA
2. Upload the new Client CA to the cluster (supports multiple CAs during transition)
3. Issue new client certificates signed by the new CA
4. Deploy new client certificates to all applications
5. Remove the old Client CA after all clients have migrated

### Part 2: Self-Hosted Certificate Management

> Follow this part if the user selected **Self-hosted** in Decision 1.

Self-hosted CockroachDB requires manual certificate lifecycle management for the CA, node, and client certificates.

#### 2.1 Initialize the Certificate Authority

```bash
# Create the CA certificate and key
cockroach cert create-ca \
  --certs-dir=certs \
  --ca-key=my-safe-directory/ca.key
```

#### 2.2 Create Node Certificates

```bash
# Create a node certificate for each node
cockroach cert create-node \
  <node-hostname> \
  <node-ip> \
  localhost \
  127.0.0.1 \
  --certs-dir=certs \
  --ca-key=my-safe-directory/ca.key
```

#### 2.3 Create Client Certificates

```bash
# Create a client certificate for root user
cockroach cert create-client root \
  --certs-dir=certs \
  --ca-key=my-safe-directory/ca.key

# Create a client certificate for an application user
cockroach cert create-client <username> \
  --certs-dir=certs \
  --ca-key=my-safe-directory/ca.key
```

#### 2.4 Certificate Rotation (Self-Hosted)

```bash
# Check certificate expiry
cockroach cert list --certs-dir=certs

# Or with OpenSSL
openssl x509 -in certs/node.crt -noout -enddate
```

**Rotation process:**
1. Generate new certificates using the existing CA (or rotate the CA first)
2. Copy new certificates to each node
3. Reload certificates (SIGHUP — no downtime required):
   ```bash
   kill -SIGHUP $(pgrep cockroach)
   ```
4. Verify nodes are serving the new certificates

### Part 3: Troubleshooting SSL/TLS Errors

See [troubleshooting reference](references/troubleshooting.md) for a comprehensive error guide.

#### Common Errors and Quick Fixes

**"x509: certificate signed by unknown authority"**
- Client does not trust the cluster's CA certificate
- Fix: Download the correct CA certificate and set `sslrootcert` in the connection string

**"SSL SYSCALL error: EOF detected"**
- Connection terminated unexpectedly during TLS handshake
- Fix: Check network connectivity, firewall rules, and that the correct port (26257) is used

**"tls: bad certificate"**
- Client certificate rejected by the server
- Fix: Verify the client certificate is signed by a CA the cluster trusts (Client CA must be uploaded)

**"certificate has expired"**
- Client or server certificate has passed its expiry date
- Fix: Rotate the expired certificate (see rotation steps above)

#### Diagnostic Commands

```bash
# Inspect a certificate
openssl x509 -in cert.crt -text -noout

# Verify certificate chain
openssl verify -CAfile ca.crt client.crt

# Test TLS connection to cluster
openssl s_client -connect <host>:26257 -CAfile ca.crt

# Check certificate expiry date
openssl x509 -in cert.crt -noout -enddate
```

### Part 4: mTLS for CDC Changefeeds to Kafka

CockroachDB CDC changefeeds can use mTLS to authenticate to Kafka brokers.

```sql
-- Create a changefeed with mTLS authentication to Kafka
CREATE CHANGEFEED FOR TABLE orders
  INTO 'kafka://<kafka-broker>:9093?tls_enabled=true&ca_cert=<base64-ca>&client_cert=<base64-cert>&client_key=<base64-key>'
  WITH updated, resolved;
```

**Preparing certificates for changefeed URI:**
```bash
# Base64 encode certificates for use in changefeed URI
cat ca.crt | base64 -w 0    # Linux
cat ca.crt | base64          # macOS

cat client.crt | base64 -w 0
cat client.key | base64 -w 0
```

## Safety Considerations

| Impact Type | Severity | Recommendation |
|-------------|----------|----------------|
| Client CA upload | Low | Does not affect existing connections; only adds a new trust root |
| Client CA removal | High | Invalidates all client certificates signed by that CA |
| Certificate expiry | High | Monitor expiry dates; rotate before expiration |
| Wrong CA certificate | Medium | Clients will fail to connect; correctable by updating the CA cert |

**Do not:**
- Delete the CA private key — it is required for signing new certificates
- Upload an expired CA certificate
- Remove a Client CA while clients still depend on it
- Disable TLS on production clusters (CockroachDB Cloud does not allow this)

## Rollback

**Cloud — Client CA issues:**
1. If a new Client CA was uploaded incorrectly, upload the correct CA
2. If client certificates are rejected, revert to password authentication temporarily
3. Contact CockroachDB support if the cluster CA needs intervention

**Self-hosted — Certificate issues:**
1. Restore previous certificates from backup
2. Reload certificates: `kill -SIGHUP $(pgrep cockroach)`
3. If CA was rotated, ensure all nodes and clients have the new CA

## References

**Skill references:**
- [Client connection examples](references/connection-examples.md) — Connection strings for common clients
- [TLS troubleshooting guide](references/troubleshooting.md) — Common SSL/TLS errors and fixes

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit
- [configuring-sso-and-scim](../configuring-sso-and-scim/SKILL.md) — SSO as an alternative to certificate-based auth

**Official CockroachDB Documentation:**
- [Transport Layer Security (TLS)](https://www.cockroachlabs.com/docs/stable/security-reference/transport-layer-security.html)
- [Authentication](https://www.cockroachlabs.com/docs/stable/authentication.html)
- [Client Connection Parameters](https://www.cockroachlabs.com/docs/stable/connection-parameters.html)
- [cockroach cert Commands](https://www.cockroachlabs.com/docs/stable/cockroach-cert.html)
- [Rotate Security Certificates](https://www.cockroachlabs.com/docs/stable/rotate-certificates.html)
- [Cloud Certificate Management](https://www.cockroachlabs.com/docs/cockroachcloud/authentication.html)
- [CDC Kafka Sink](https://www.cockroachlabs.com/docs/stable/changefeed-sinks.html#kafka)

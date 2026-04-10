# Certificate Rotation Procedures

## Prerequisites

- `cockroach` binary available on the machine performing certificate generation.
- Access to the CA key (for signing new certificates).
- Ability to distribute files to all nodes (via SSH, configuration management, etc.).
- File permissions: certificate files must be `0600` (or `0644` for public certs) and owned by the CockroachDB process user.

## Important: CockroachDB Auto-Detects New Certificates

CockroachDB monitors the `certs` directory and automatically reloads certificates when files change. **No node restart is required** for certificate rotation in most cases. The reload happens within a few seconds of file modification.

Exceptions that require a restart:
- Changing the `--certs-dir` flag itself.
- Changing from insecure mode to secure mode.

---

## Procedure 1: Node Certificate Rotation (Same CA)

Use this procedure when the CA certificate is still valid and you only need to rotate node certificates (e.g., approaching expiration or key rotation policy).

### Step 1: Generate New Node Certificate

```bash
cockroach cert create-node \
  <node-hostname> \
  <node-ip> \
  localhost \
  127.0.0.1 \
  <load-balancer-hostname> \
  --certs-dir=/path/to/certs \
  --ca-key=/path/to/ca.key \
  --overwrite
```

Include all DNS names and IP addresses the node may be accessed by. The `--overwrite` flag replaces the existing `node.crt` and `node.key` files.

**Example for a 3-node cluster:**

```bash
# Node 1
cockroach cert create-node \
  crdb-node1.example.com \
  10.0.1.10 \
  localhost \
  127.0.0.1 \
  crdb-lb.example.com \
  --certs-dir=./certs-node1 \
  --ca-key=./ca.key \
  --overwrite

# Node 2
cockroach cert create-node \
  crdb-node2.example.com \
  10.0.1.11 \
  localhost \
  127.0.0.1 \
  crdb-lb.example.com \
  --certs-dir=./certs-node2 \
  --ca-key=./ca.key \
  --overwrite

# Node 3
cockroach cert create-node \
  crdb-node3.example.com \
  10.0.1.12 \
  localhost \
  127.0.0.1 \
  crdb-lb.example.com \
  --certs-dir=./certs-node3 \
  --ca-key=./ca.key \
  --overwrite
```

### Step 2: Deploy to Each Node

```bash
# Copy new cert and key to the node
scp ./certs-node1/node.crt cockroach@crdb-node1:/path/to/certs/node.crt
scp ./certs-node1/node.key cockroach@crdb-node1:/path/to/certs/node.key

# Fix permissions on the node
ssh cockroach@crdb-node1 "chmod 0600 /path/to/certs/node.key && chmod 0644 /path/to/certs/node.crt"
```

### Step 3: Verify via SQL

CockroachDB auto-reloads the certificates. Verify the new certificate is active:

```sql
-- Check certificate expiry via node metrics (v25.4+)
SELECT node_id,
       metrics->>'security.certificate.expiration.ca' AS ca_expiry_epoch,
       metrics->>'security.certificate.expiration.node' AS node_expiry_epoch
FROM crdb_internal.kv_node_status
ORDER BY node_id;
```

Also verify externally using `openssl`:

```bash
openssl s_client -connect crdb-node1.example.com:26257 -showcerts < /dev/null 2>/dev/null \
  | openssl x509 -noout -dates -serial
```

---

## Procedure 2: CA Certificate Rotation (Combined CA Approach)

Use this procedure when the CA certificate itself needs to be rotated (approaching expiration, CA key compromise, or policy-mandated rotation). This is a multi-step process to maintain trust continuity.

### Step 1: Generate New CA Certificate

```bash
cockroach cert create-ca \
  --certs-dir=./new-ca \
  --ca-key=./new-ca/ca.key \
  --lifetime=3650d
```

This creates a new CA in the `./new-ca` directory. The original CA files remain untouched.

### Step 2: Create Combined CA Certificate File

Concatenate the old and new CA certificates into a single file. This allows nodes to trust certificates signed by either CA during the transition period.

```bash
cat ./old-ca/ca.crt ./new-ca/ca.crt > ./combined-ca.crt
```

### Step 3: Deploy Combined CA to All Nodes

Replace `ca.crt` on every node with the combined file:

```bash
for node in crdb-node1 crdb-node2 crdb-node3; do
  scp ./combined-ca.crt cockroach@${node}:/path/to/certs/ca.crt
  ssh cockroach@${node} "chmod 0644 /path/to/certs/ca.crt"
done
```

CockroachDB auto-reloads the CA certificate. All nodes now trust both the old and new CA.

### Step 4: Wait for CA Propagation

Wait for all nodes to reload the combined CA. Verify by checking the logs or querying:

```sql
-- In v25.4+, cert details (including issuer) are available via metrics in crdb_internal.kv_node_status.
-- Use openssl to inspect issuer details directly from cert files or via s_client.
SELECT node_id,
       metrics->>'security.certificate.expiration.ca' AS ca_expiry_epoch,
       metrics->>'security.certificate.expiration.node' AS node_expiry_epoch
FROM crdb_internal.kv_node_status
ORDER BY node_id;
```

Allow at least 1-2 minutes for propagation across all nodes.

### Step 5: Rotate Node Certificates (Signed by New CA)

Generate new node certificates using the **new** CA key:

```bash
cockroach cert create-node \
  <node-hostname> \
  <node-ip> \
  localhost \
  127.0.0.1 \
  <load-balancer-hostname> \
  --certs-dir=./new-certs-node1 \
  --ca-key=./new-ca/ca.key \
  --overwrite
```

Deploy to each node following the same process as Procedure 1, Steps 2-3.

### Step 6: Rotate Client Certificates (Signed by New CA)

Generate new client certificates using the **new** CA key:

```bash
cockroach cert create-client \
  root \
  --certs-dir=./new-client-certs \
  --ca-key=./new-ca/ca.key \
  --overwrite

cockroach cert create-client \
  app_user \
  --certs-dir=./new-client-certs \
  --ca-key=./new-ca/ca.key \
  --overwrite
```

Deploy new client certificates to all applications.

### Step 7: Remove Old CA (After Full Transition)

Once all node and client certificates have been rotated to the new CA, and sufficient time has passed to confirm everything works:

```bash
# Replace combined CA with new CA only
for node in crdb-node1 crdb-node2 crdb-node3; do
  scp ./new-ca/ca.crt cockroach@${node}:/path/to/certs/ca.crt
  ssh cockroach@${node} "chmod 0644 /path/to/certs/ca.crt"
done
```

**Warning**: Only perform this step after confirming that no certificates signed by the old CA are still in use. Any client or node still presenting an old-CA-signed certificate will fail authentication after this step.

### Step 8: Securely Store and Retire Old CA Key

```bash
# Archive the old CA key securely (e.g., to a vault or offline storage)
# Then remove from the working system
rm ./old-ca/ca.key
```

---

## Procedure 3: Client Certificate Rotation

### Step 1: Generate New Client Certificate

```bash
cockroach cert create-client \
  <username> \
  --certs-dir=./client-certs \
  --ca-key=/path/to/ca.key \
  --overwrite
```

**Example:**

```bash
cockroach cert create-client \
  app_user \
  --certs-dir=./client-certs \
  --ca-key=./ca.key \
  --lifetime=365d \
  --overwrite
```

### Step 2: Deploy to Application

The deployment method depends on the application architecture:

```bash
# Direct file deployment
scp ./client-certs/client.app_user.crt app-server:/path/to/certs/
scp ./client-certs/client.app_user.key app-server:/path/to/certs/

# Fix permissions
ssh app-server "chmod 0600 /path/to/certs/client.app_user.key"
```

For applications using connection strings:

```
postgresql://app_user@crdb-lb.example.com:26257/mydb?sslmode=verify-full&sslcert=/path/to/certs/client.app_user.crt&sslkey=/path/to/certs/client.app_user.key&sslrootcert=/path/to/certs/ca.crt
```

### Step 3: Verify Client Certificate

```bash
# Verify the certificate details
openssl x509 -in ./client-certs/client.app_user.crt -noout -text

# Test connectivity with the new certificate
cockroach sql \
  --certs-dir=./client-certs \
  --host=crdb-lb.example.com \
  --user=app_user \
  -e "SELECT 1;"
```

---

## File Permission Reference

| File | Recommended Permission | Owner |
|---|---|---|
| `ca.crt` | `0644` | CockroachDB process user |
| `ca.key` | `0600` | Restricted (ideally offline) |
| `node.crt` | `0644` | CockroachDB process user |
| `node.key` | `0600` | CockroachDB process user |
| `client.<user>.crt` | `0644` | Application process user |
| `client.<user>.key` | `0600` | Application process user |

**Note**: The CA key (`ca.key`) should not be stored on CockroachDB nodes in production. It should be kept in a secure, offline location (e.g., hardware security module or vault) and only brought online during certificate generation.

---

## Verification Checklist

After any certificate rotation, verify:

1. All nodes are communicating (no RPC errors in logs).
2. SQL connections succeed from all clients.
3. DB Console (Admin UI) loads without certificate warnings.
4. Certificate expiration dates are as expected (query `crdb_internal.kv_node_status` metrics).
5. No authentication errors in the CockroachDB log files.
6. Monitoring and alerting systems can still connect.

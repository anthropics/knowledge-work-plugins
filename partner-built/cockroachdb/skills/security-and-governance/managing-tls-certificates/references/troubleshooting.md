# TLS Troubleshooting Guide

This reference provides solutions for common SSL/TLS connection errors encountered with CockroachDB.

## Certificate Verification Errors

### "x509: certificate signed by unknown authority"

**Cause:** The client does not have the correct CA certificate, so it cannot verify the server's TLS certificate.

**Fix:**
1. Download the correct CA certificate for your cluster
2. Set the `sslrootcert` parameter in your connection string to point to the CA cert file
3. Verify the CA cert matches: `openssl verify -CAfile ca.crt server.crt`

**Cloud-specific:** Download the CA cert from Cloud Console (Cluster > Connect > Download CA Cert) or via `ccloud cluster cert <cluster-id>`.

### "x509: certificate has expired or is not yet valid"

**Cause:** A certificate in the chain (CA, node, or client) has expired or has a start date in the future.

**Fix:**
1. Check expiry: `openssl x509 -in cert.crt -noout -dates`
2. Rotate the expired certificate (see rotation steps in SKILL.md)
3. For self-hosted: regenerate using `cockroach cert create-node` or `create-client`
4. For Cloud: client certificates need to be reissued; the cluster CA is managed by Cockroach Labs

### "x509: certificate is valid for X, not Y"

**Cause:** The hostname in the connection string does not match any Subject Alternative Name (SAN) in the server certificate.

**Fix:**
1. Use the correct hostname as shown in the Cloud Console or cluster configuration
2. Inspect the certificate SANs: `openssl x509 -in node.crt -noout -text | grep -A1 "Subject Alternative Name"`
3. If using a load balancer or proxy, ensure it presents the correct certificate
4. Use `sslmode=verify-ca` instead of `verify-full` as a workaround (less secure)

## Connection Errors

### "SSL SYSCALL error: EOF detected"

**Cause:** The connection was terminated during or after the TLS handshake. This is a network-level issue, not a certificate issue.

**Common causes:**
- Firewall blocking port 26257
- Load balancer timeout or idle connection drop
- Network connectivity issues
- IP allowlist rejecting the connection (Cloud)

**Fix:**
1. Verify network connectivity: `nc -zv <host> 26257`
2. Check firewall rules allow port 26257
3. For Cloud: verify your IP is in the allowlist
4. Check load balancer health and timeout settings
5. Set connection pool keepalive to prevent idle disconnects

### "connection refused" or "connection timed out"

**Cause:** The client cannot reach the CockroachDB server at all.

**Fix:**
1. Verify the hostname and port are correct
2. Check DNS resolution: `nslookup <host>` or `dig <host>`
3. For Cloud: check IP allowlist includes your source IP
4. For self-hosted: verify the node is running and listening on the expected interface

### "no pg_hba.conf entry for host"

**Cause:** The server's HBA (Host-Based Authentication) configuration does not allow the connection method from the client's IP.

**Fix:**
1. Check HBA configuration: `SHOW CLUSTER SETTING server.host_based_authentication.configuration;`
2. Ensure there is an entry allowing `cert` or `cert-password` for certificate auth
3. For password auth, ensure there is a `password` entry

## Client Certificate Errors

### "tls: bad certificate"

**Cause:** The server rejected the client certificate. The certificate may not be signed by a trusted Client CA, or the certificate may be malformed.

**Fix:**
1. Verify the client cert is signed by a CA the cluster trusts
2. For Cloud: verify the Client CA has been uploaded via `ccloud cluster cert set-client-ca`
3. Check the certificate chain: `openssl verify -CAfile client-ca.crt client.<user>.crt`
4. Ensure the CN (Common Name) in the client cert matches the SQL username

### "tls: private key does not match public key"

**Cause:** The client key file does not correspond to the client certificate file.

**Fix:**
1. Verify the key matches the cert:
   ```bash
   openssl x509 -in client.crt -noout -modulus | md5sum
   openssl rsa -in client.key -noout -modulus | md5sum
   # Both hashes should match
   ```
2. Regenerate the client certificate and key pair if they don't match

### "permission denied" on key file

**Cause:** The client key file has overly permissive permissions.

**Fix:**
```bash
chmod 0600 client.<user>.key
```

PostgreSQL drivers require the key file to be readable only by the owner.

### "could not load private key file: unsupported key type"

**Cause:** Java JDBC requires the client key in PKCS#8 DER format, but the key is in PEM format.

**Fix:**
```bash
openssl pkcs8 -topk8 -inform PEM -outform DER \
  -in client.<user>.key -out client.<user>.key.pk8 -nocrypt
```

Use the `.pk8` file in your JDBC connection string.

## CockroachDB Cloud-Specific Issues

### "certificates issued by Client CA attached to cluster being rejected"

**Cause:** The uploaded Client CA may not match the CA that signed the client certificates, or the upload may not have completed successfully.

**Fix:**
1. Verify the Client CA was uploaded successfully: check Cloud Console or ccloud CLI
2. Ensure the client certificates are signed by the uploaded Client CA (not a different CA)
3. Re-upload the Client CA if needed: `ccloud cluster cert set-client-ca <cluster-id> --cert-file client-ca.crt`

### "Terraform apply caused SSL certificate to change"

**Cause:** Certain Terraform operations (like cluster recreation or major updates) may cause the cluster CA certificate to be reissued.

**Fix:**
1. Re-download the CA certificate after Terraform applies
2. Distribute the new CA certificate to all clients
3. Consider pinning the CA cert in Terraform outputs for automation

## Diagnostic Commands

### Inspect a Certificate

```bash
# Full certificate details
openssl x509 -in cert.crt -text -noout

# Just the subject and issuer
openssl x509 -in cert.crt -noout -subject -issuer

# Expiry date only
openssl x509 -in cert.crt -noout -enddate

# Subject Alternative Names
openssl x509 -in cert.crt -noout -text | grep -A1 "Subject Alternative Name"
```

### Verify Certificate Chain

```bash
# Verify a certificate against its CA
openssl verify -CAfile ca.crt cert.crt

# Verify with intermediate certificates
openssl verify -CAfile ca.crt -untrusted intermediate.crt cert.crt
```

### Test TLS Connection

```bash
# Connect and show server certificate
openssl s_client -connect <host>:26257 -CAfile ca.crt

# Show the full certificate chain
openssl s_client -connect <host>:26257 -CAfile ca.crt -showcerts

# Test with client certificate
openssl s_client -connect <host>:26257 \
  -CAfile ca.crt \
  -cert client.<user>.crt \
  -key client.<user>.key
```

### List CockroachDB Certificates (Self-Hosted)

```bash
# List all certificates in the certs directory
cockroach cert list --certs-dir=certs
```

## Notes

- CockroachDB Cloud enforces TLS — `sslmode=disable` always fails
- Self-hosted CockroachDB defaults to requiring TLS but can be configured with `--accept-sql-without-tls` (not recommended for production)
- Certificate rotation via SIGHUP does not cause downtime on self-hosted clusters
- The default certificate lifetime for `cockroach cert` is 10 years for CA, 5 years for node/client
- Always monitor certificate expiry dates in production environments

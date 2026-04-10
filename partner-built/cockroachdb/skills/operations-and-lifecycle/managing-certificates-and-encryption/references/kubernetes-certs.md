# Certificate Management in Kubernetes

## Overview

Certificate management in Kubernetes CockroachDB deployments depends on the deployment method. There are three primary approaches:

1. **CockroachDB Kubernetes Operator** with built-in self-signer
2. **cert-manager** (Jetstack) integration
3. **Manual** certificate management (similar to bare metal)

---

## Approach 1: CockroachDB Kubernetes Operator Self-Signer

The CockroachDB Kubernetes Operator includes a built-in certificate manager that handles certificate generation, rotation, and renewal automatically.

### Configuration

The self-signer is configured in the CrdbCluster custom resource:

```yaml
apiVersion: crdb.cockroachlabs.com/v1alpha1
kind: CrdbCluster
metadata:
  name: cockroachdb
spec:
  nodes: 3
  tlsEnabled: true
  # Certificate configuration
  additionalArgs:
    - "--locality=region=us-east-1"
  # Self-signer settings are controlled via operator flags
```

### Operator Certificate Settings

The operator manages certificates with the following configurable parameters (set as operator deployment flags):

| Parameter | Description | Default |
|---|---|---|
| `--feature-gates=AutoRotateCerts=true` | Enable automatic certificate rotation | `true` (recent operator versions) |
| CA certificate duration | Lifetime of the generated CA certificate | 365 days (configurable via operator flags) |
| Node certificate duration | Lifetime of node certificates | 365 days |
| Minimum certificate duration before renewal | Threshold that triggers renewal | Typically 30 days before expiry |

### Checking Certificate Expiration

The operator annotates pods with certificate expiration information:

```bash
# Check certificate expiration annotation on pods
kubectl get pods -l app.kubernetes.io/name=cockroachdb \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.crdb\.io/certexpiration}{"\n"}{end}'
```

Example output:

```
cockroachdb-0    2027-02-23T12:00:00Z
cockroachdb-1    2027-02-23T12:00:00Z
cockroachdb-2    2027-02-23T12:00:00Z
```

### Triggering Manual Rotation

If you need to force a certificate rotation before the automatic threshold:

```bash
# Delete the certificate secrets to trigger regeneration
kubectl delete secret cockroachdb-node
kubectl delete secret cockroachdb-root

# The operator will detect the missing secrets and regenerate them
# Monitor operator logs for rotation progress
kubectl logs deployment/cockroach-operator -f
```

### Verifying Rotation

```bash
# Check operator logs for rotation events
kubectl logs deployment/cockroach-operator | grep -i cert

# Verify new secrets were created
kubectl get secrets cockroachdb-node cockroachdb-root -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.creationTimestamp}{"\n"}{end}'

# Check certificate content
kubectl get secret cockroachdb-node -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -dates
```

---

## Approach 2: cert-manager Integration

[cert-manager](https://cert-manager.io/) provides automated certificate lifecycle management using Kubernetes-native resources.

### Certificate Resource Configuration

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: cockroachdb-ca-issuer
  namespace: cockroachdb
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: cockroachdb-ca
  namespace: cockroachdb
spec:
  isCA: true
  commonName: Cockroach CA
  secretName: cockroachdb-ca-secret
  duration: 8760h    # 365 days
  renewBefore: 720h  # 30 days before expiry
  privateKey:
    algorithm: RSA
    size: 4096
  issuerRef:
    name: cockroachdb-ca-issuer
    kind: Issuer
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: cockroachdb-issuer
  namespace: cockroachdb
spec:
  ca:
    secretName: cockroachdb-ca-secret
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: cockroachdb-node
  namespace: cockroachdb
spec:
  secretName: cockroachdb-node-secret
  duration: 8760h     # 365 days
  renewBefore: 720h   # 30 days before expiry
  privateKey:
    algorithm: RSA
    size: 2048
  usages:
    - server auth
    - client auth
  dnsNames:
    - "localhost"
    - "cockroachdb-public"
    - "cockroachdb-public.cockroachdb"
    - "cockroachdb-public.cockroachdb.svc.cluster.local"
    - "*.cockroachdb"
    - "*.cockroachdb.cockroachdb"
    - "*.cockroachdb.cockroachdb.svc.cluster.local"
  ipAddresses:
    - "127.0.0.1"
  issuerRef:
    name: cockroachdb-issuer
    kind: Issuer
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: cockroachdb-root-client
  namespace: cockroachdb
spec:
  secretName: cockroachdb-root-secret
  duration: 8760h
  renewBefore: 720h
  privateKey:
    algorithm: RSA
    size: 2048
  usages:
    - client auth
  commonName: root
  issuerRef:
    name: cockroachdb-issuer
    kind: Issuer
```

### Key Parameters

| Parameter | Description | Recommended Value |
|---|---|---|
| `duration` | Total certificate lifetime | `8760h` (365 days) or per organizational policy |
| `renewBefore` | Time before expiry to trigger renewal | `720h` (30 days) minimum |
| `privateKey.algorithm` | Key algorithm | `RSA` for broadest compatibility |
| `privateKey.size` | Key size | `4096` for CA, `2048` for node/client |

### Pod Restart Requirement

**Important**: cert-manager updates the Kubernetes Secret when it renews a certificate, but CockroachDB pods do not automatically pick up the new certificate from the mounted Secret volume. You must restart pods to load renewed certificates.

Options for handling this:

```bash
# Option 1: Rolling restart after cert-manager renews
kubectl rollout restart statefulset cockroachdb -n cockroachdb

# Option 2: Use a sidecar or init container that watches for secret changes
# and copies updated certs to the CockroachDB certs directory

# Option 3: Use stakater/Reloader to auto-restart on secret changes
# (Install Reloader and add annotation to StatefulSet)
```

Using [Reloader](https://github.com/stakater/Reloader) for automatic restarts:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cockroachdb
  annotations:
    secret.reloader.stakater.com/reload: "cockroachdb-node-secret,cockroachdb-ca-secret"
```

### Checking cert-manager Certificate Status

```bash
# Check certificate status
kubectl get certificates -n cockroachdb

# Detailed certificate status
kubectl describe certificate cockroachdb-node -n cockroachdb

# Check renewal status
kubectl get certificaterequests -n cockroachdb

# Check certificate expiry from the secret
kubectl get secret cockroachdb-node-secret -n cockroachdb \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -dates

# cert-manager events
kubectl get events -n cockroachdb --field-selector reason=Issuing
```

---

## Approach 3: Manual Certificate Management

Manual certificate management in Kubernetes follows the same process as bare metal (see `rotation-procedures.md`) but uses `kubectl` for file distribution instead of `scp`.

### Distributing Certificates via kubectl

```bash
# Create or update the Kubernetes secret with new certificates
kubectl create secret generic cockroachdb-node-secret \
  --from-file=ca.crt=./certs/ca.crt \
  --from-file=tls.crt=./certs/node.crt \
  --from-file=tls.key=./certs/node.key \
  --namespace=cockroachdb \
  --dry-run=client -o yaml | kubectl apply -f -

# Create or update client certificate secret
kubectl create secret generic cockroachdb-root-secret \
  --from-file=ca.crt=./certs/ca.crt \
  --from-file=tls.crt=./certs/client.root.crt \
  --from-file=tls.key=./certs/client.root.key \
  --namespace=cockroachdb \
  --dry-run=client -o yaml | kubectl apply -f -
```

### Copying Files Directly to Pods

If certificates are mounted via `emptyDir` or a writable volume:

```bash
# Copy to each pod
for i in 0 1 2; do
  kubectl cp ./certs/node.crt cockroachdb/cockroachdb-${i}:/cockroach/cockroach-certs/node.crt
  kubectl cp ./certs/node.key cockroachdb/cockroachdb-${i}:/cockroach/cockroach-certs/node.key
  kubectl cp ./certs/ca.crt cockroachdb/cockroachdb-${i}:/cockroach/cockroach-certs/ca.crt
done
```

**Note**: Files copied via `kubectl cp` do not persist across pod restarts. This method is only suitable for temporary operations. For persistent certificate management, use Kubernetes Secrets.

---

## Certificate Expiry Monitoring

### Prometheus Alerts

If using the CockroachDB Prometheus metrics endpoint, set up alerts for certificate expiry:

```yaml
groups:
  - name: cockroachdb-cert-alerts
    rules:
      - alert: CockroachDBCertExpiringSoon
        expr: (security_certificate_expiration_ca - time()) / 86400 < 30
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "CockroachDB CA certificate expiring in less than 30 days"
      - alert: CockroachDBNodeCertExpiringSoon
        expr: (security_certificate_expiration_node - time()) / 86400 < 14
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "CockroachDB node certificate expiring in less than 14 days"
```

### kubectl-Based Expiry Check Script

```bash
#!/bin/bash
# Check certificate expiry for all CockroachDB pods

NAMESPACE="cockroachdb"
WARNING_DAYS=30

echo "Checking CockroachDB certificate expiry..."
echo "============================================"

for pod in $(kubectl get pods -n ${NAMESPACE} -l app.kubernetes.io/name=cockroachdb -o name); do
  pod_name=$(basename ${pod})
  echo ""
  echo "Pod: ${pod_name}"

  # Check node certificate
  expiry=$(kubectl exec -n ${NAMESPACE} ${pod_name} -- \
    openssl x509 -in /cockroach/cockroach-certs/node.crt -noout -enddate 2>/dev/null \
    | cut -d= -f2)

  if [ -n "${expiry}" ]; then
    expiry_epoch=$(date -d "${expiry}" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "${expiry}" +%s 2>/dev/null)
    now_epoch=$(date +%s)
    days_left=$(( (expiry_epoch - now_epoch) / 86400 ))

    if [ ${days_left} -lt ${WARNING_DAYS} ]; then
      echo "  WARNING: Node cert expires in ${days_left} days (${expiry})"
    else
      echo "  OK: Node cert expires in ${days_left} days (${expiry})"
    fi
  else
    echo "  ERROR: Could not read node certificate"
  fi
done
```

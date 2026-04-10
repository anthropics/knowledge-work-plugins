---
name: provisioning-cluster-for-production
description: Guides initial CockroachDB cluster provisioning and production deployment. Self-Hosted covers cockroach start/init, Kubernetes deployment (Operator, Helm), hardware sizing, and production configuration. Advanced/BYOC covers Cloud Console, API, and Terraform provisioning with production settings. Standard covers cluster creation and provisioned compute selection. Basic covers cluster creation and spending limits. Use when creating a new cluster, preparing for production go-live, or validating deployment configuration.
compatibility: Self-Hosted requires CLI access and infrastructure provisioning. Advanced/BYOC requires Cloud Console with Org Admin role. Standard requires Cloud Console. Basic requires Cloud Console.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Provisioning Cluster for Production

Guides CockroachDB cluster creation and production deployment configuration. Before providing procedures, this skill gathers context to deliver tier-appropriate provisioning steps and production hardening guidance.

## When to Use This Skill

- Creating a new CockroachDB cluster
- Preparing a development/staging cluster for production go-live
- Validating hardware and configuration for production readiness
- Choosing the right deployment tier and sizing

**For post-deployment health checks:** Use [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md).
**For ongoing settings management:** Use [managing-cluster-settings](../managing-cluster-settings/SKILL.md).
**For capacity changes after deployment:** Use [managing-cluster-capacity](../managing-cluster-capacity/SKILL.md).

---

## Step 1: Gather Context

### Required Context

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Deployment tier?** | Self-Hosted, Advanced, BYOC, Standard, Basic | Completely different provisioning procedures |
| **Environment?** | Production, Staging, Development | Determines hardware sizing and configuration rigor |

### Additional Context (by tier)

**If Self-Hosted:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Platform?** | Bare metal, VMs (AWS/GCP/Azure), Kubernetes | Changes installation and start commands |
| **If Kubernetes?** | Operator (recommended), Helm, Manual StatefulSet | Determines deployment method |
| **Node count?** | 3 (minimum), 5, 9+ | Affects topology and replication |
| **Multi-region?** | Yes (how many regions), No | Requires locality flags and topology planning |
| **Expected workload?** | OLTP, mixed OLTP/analytics, write-heavy | Affects hardware sizing |
| **Security requirements?** | TLS required, encryption at rest, CMEK | Determines certificate and encryption setup |

**If Advanced or BYOC:**

| Question | Options | Why It Matters |
|----------|---------|----------------|
| **Provisioning method?** | Cloud Console, Cloud API, Terraform | Determines procedure |
| **Cloud provider?** | AWS, GCP, Azure | Affects region selection and networking |
| **Node count and size?** | e.g., 3 nodes x 8 vCPUs | Determines initial capacity |

**If Standard:** Gather expected workload size (vCPUs) and storage estimate.

**If Basic:** Gather expected usage pattern and monthly budget.

### Context-Driven Routing

| Tier | Go To |
|------|-------|
| Self-Hosted | [Self-Hosted Provisioning](#self-hosted-provisioning) |
| Advanced | [Advanced Provisioning](#advanced-provisioning) |
| BYOC | [BYOC Provisioning](#byoc-provisioning) |
| Standard | [Standard Provisioning](#standard-provisioning) |
| Basic | [Basic Provisioning](#basic-provisioning) |

---

## Self-Hosted Provisioning

**Applies when:** Tier = Self-Hosted

### Hardware Sizing

| Component | Minimum | Production Recommended |
|-----------|---------|----------------------|
| Nodes | 3 | 3+ (odd number per failure domain) |
| CPU | 4 vCPUs (non-burstable) | 8+ vCPUs |
| RAM | 16 GB | 32+ GB |
| Storage | 150 GB SSD | 500+ GB NVMe SSD |
| Network | 1 Gbps | 10 Gbps |

**Memory formula:** `--cache + --max-sql-memory <= 75% of total RAM`
Recommended: `--cache=.25 --max-sql-memory=.25`

**Never use:** burstable instances, HDDs, network-attached HDD, shared CPU.

See [hardware-and-infrastructure reference](references/hardware-and-infrastructure.md) for cloud instance recommendations.

### Deploy on VMs / Bare Metal

**Step 1: Install CockroachDB on each node**
```bash
curl https://binaries.cockroachdb.com/cockroach-v<version>.linux-amd64.tgz | tar -xz
cp cockroach-v<version>.linux-amd64/cockroach /usr/local/bin/
```

**Step 2: Generate certificates**
```bash
cockroach cert create-ca --certs-dir=certs --ca-key=my-safe-directory/ca.key
cockroach cert create-node <node-hostname> <node-ip> localhost 127.0.0.1 \
  --certs-dir=certs --ca-key=my-safe-directory/ca.key
cockroach cert create-client root --certs-dir=certs --ca-key=my-safe-directory/ca.key
```

**Step 3: Start nodes (repeat on each node)**
```bash
cockroach start \
  --certs-dir=certs \
  --store=path=<store-path> \
  --listen-addr=<node-address>:26257 \
  --http-addr=<node-address>:8080 \
  --join=<node1-address>,<node2-address>,<node3-address> \
  --locality=region=<region>,zone=<zone> \
  --cache=.25 \
  --max-sql-memory=.25 \
  --background
```

**Step 4: Initialize cluster (once, from any node)**
```bash
cockroach init --certs-dir=certs --host=<any-node-address>
```

**Step 5: Verify**
```sql
SELECT node_id, address, locality, build_tag, is_live
FROM crdb_internal.gossip_nodes ORDER BY node_id;
```

### Deploy on Kubernetes

**Operator (recommended):**
```bash
kubectl apply -f https://raw.githubusercontent.com/cockroachdb/cockroach-operator/master/install/crds.yaml
kubectl apply -f https://raw.githubusercontent.com/cockroachdb/cockroach-operator/master/install/operator.yaml
# Apply CrdbCluster manifest with node count, resources, and storage
```

**Helm:**
```bash
helm repo add cockroachdb https://charts.cockroachdb.com/
helm install cockroachdb cockroachdb/cockroachdb \
  --set statefulset.replicas=3 \
  --set storage.persistentVolume.size=100Gi
```

### Production Configuration (Self-Hosted)

After cluster is running, apply production settings:

```sql
-- Enable critical features
SET CLUSTER SETTING kv.rangefeed.enabled = true;
SET CLUSTER SETTING sql.stats.automatic_collection.enabled = true;
SET CLUSTER SETTING admission.kv.enabled = true;

-- Set timeouts
SET CLUSTER SETTING sql.defaults.idle_in_transaction_session_timeout = '300s';
SET CLUSTER SETTING sql.defaults.statement_timeout = '30s';

-- Install enterprise license (if applicable)
SET CLUSTER SETTING cluster.organization = '<org-name>';
SET CLUSTER SETTING enterprise.license = '<license-key>';
```

**Create ballast files on each node:**
```bash
cockroach debug ballast <store-path>/auxiliary/EMERGENCY_BALLAST --size=1GiB
```

**Configure load balancer:** Point to all nodes with health check on `/health?ready=1`.

See [production-deployment-checklist reference](references/production-deployment-checklist.md) for the full go-live checklist.

---

## Advanced Provisioning

**Applies when:** Tier = Advanced

### Via Cloud Console

1. **cockroachlabs.cloud → Create Cluster**
2. Select **Advanced** plan
3. Choose cloud provider (AWS, GCP, Azure)
4. Select region(s)
5. Configure node count (minimum 3) and machine size (vCPUs per node)
6. Configure storage
7. Review and create

### Via Cloud API

```bash
curl -X POST -H "Authorization: Bearer $COCKROACH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<cluster-name>",
    "provider": "AWS",
    "spec": {
      "dedicated": {
        "region_nodes": {"us-east-1": 3},
        "machine_type": "m6i.xlarge",
        "storage_gib": 150
      }
    }
  }' \
  "https://cockroachlabs.cloud/api/v1/clusters"
```

### Via Terraform

```hcl
resource "cockroach_cluster" "production" {
  name           = "production"
  cloud_provider = "AWS"

  dedicated {
    num_virtual_cpus = 8
    storage_gib      = 150
    num_nodes        = 3
  }

  regions = [{
    name = "us-east-1"
  }]
}
```

### Post-Provisioning

- Configure IP allowlists or VPC Peering/PrivateLink
- Create SQL users and databases
- Set maintenance window (see [performing-cluster-maintenance](../performing-cluster-maintenance/SKILL.md))
- Configure metrics export to Datadog/Prometheus if needed

---

## BYOC Provisioning

**Applies when:** Tier = BYOC

Follow [Advanced Provisioning](#advanced-provisioning) steps — BYOC uses the same Cloud Console, API, and Terraform interfaces.

**Additional BYOC steps:**
- Ensure your cloud account meets CRL prerequisites (service account, VPC, IAM roles)
- Configure PrivateLink/PSC for private connectivity
- Verify CRL service account permissions

---

## Standard Provisioning

**Applies when:** Tier = Standard

1. **cockroachlabs.cloud → Create Cluster**
2. Select **Standard** plan
3. Choose cloud provider and region
4. Set provisioned compute (vCPUs) based on expected workload
5. Create

**Post-provisioning:**
- Create SQL users and databases
- Configure IP allowlists
- Set session-level defaults:
  ```sql
  ALTER ROLE ALL SET statement_timeout = '30s';
  ALTER ROLE ALL SET idle_in_transaction_session_timeout = '300s';
  ```

---

## Basic Provisioning

**Applies when:** Tier = Basic

1. **cockroachlabs.cloud → Create Cluster**
2. Select **Basic** plan
3. Choose cloud provider and region
4. Create (auto-scales, no sizing needed)

**Post-provisioning:**
- Set spending limits (Cloud Console → Cluster → Settings)
- Create SQL users and databases
- Configure IP allowlists

---

## Safety Considerations

| Operation | Tier | Risk |
|-----------|------|------|
| `cockroach init` | SH | Safe — only runs once; subsequent calls are no-ops |
| Certificate generation | SH | Store CA key securely — loss means no new certs |
| Cloud cluster creation | ADV/BYOC/STD/BAS | Safe — can be deleted if misconfigured |
| Production settings changes | SH | See [managing-cluster-settings](../managing-cluster-settings/SKILL.md) |

**Critical (Self-Hosted):**
- Never use `--insecure` in production — always use TLS
- Never use burstable instances for production workloads
- Always set `--locality` flags for multi-node clusters
- Always configure `--cache` and `--max-sql-memory` (defaults are too low)
- Always create ballast files before going to production

## Troubleshooting

| Issue | Tier | Fix |
|-------|------|-----|
| `cockroach init` fails | SH | Check all nodes are started and reachable on port 26257 |
| Node won't join cluster | SH | Verify `--join` addresses; check firewall rules for ports 26257, 8080 |
| "clock offset" error | SH | Sync clocks with NTP; check `--max-offset` setting |
| TLS handshake failure | SH | Verify certs match; check CA is the same across all nodes |
| Cloud cluster stuck in "Creating" | ADV/BYOC | Wait 15 min; contact support if no progress |
| Cannot connect after creation | ALL | Check IP allowlist; verify connection string; try with root user |

## References

**Skill references:**
- [Hardware and infrastructure](references/hardware-and-infrastructure.md)
- [Production deployment checklist](references/production-deployment-checklist.md)

**Related skills:**
- [reviewing-cluster-health](../reviewing-cluster-health/SKILL.md) — Post-deployment health check
- [managing-cluster-settings](../managing-cluster-settings/SKILL.md) — Production settings
- [managing-certificates-and-encryption](../managing-certificates-and-encryption/SKILL.md) — TLS setup
- [managing-cluster-capacity](../managing-cluster-capacity/SKILL.md) — Scaling after deployment

**Official CockroachDB Documentation:**
- [Install CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb)
- [Start a Cluster](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster)
- [Deploy on Kubernetes](https://www.cockroachlabs.com/docs/stable/deploy-cockroachdb-with-kubernetes)
- [Production Checklist](https://www.cockroachlabs.com/docs/stable/recommended-production-settings)
- [Create an Advanced Cluster](https://www.cockroachlabs.com/docs/cockroachcloud/create-an-advanced-cluster)
- [Cloud API](https://www.cockroachlabs.com/docs/cockroachcloud/cloud-api)

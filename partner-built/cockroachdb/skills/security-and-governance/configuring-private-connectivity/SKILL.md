---
name: configuring-private-connectivity
description: Configures private network connectivity for CockroachDB Cloud clusters including AWS PrivateLink, GCP Private Service Connect, Azure Private Link, egress private endpoints, and VPC peering. Use when setting up private endpoints to eliminate public internet exposure, configuring egress to external services like Kafka, or establishing VPC peering.
compatibility: Requires CockroachDB Cloud Advanced or Standard plan. Private endpoints require cloud provider configuration (AWS, GCP, or Azure). VPC peering requires Advanced plan.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Configuring Private Connectivity

Configures private network connectivity for CockroachDB Cloud clusters to eliminate public internet exposure for database traffic. Covers ingress private endpoints (AWS PrivateLink, GCP Private Service Connect, Azure Private Link), egress private endpoints for outbound connections to external services, and VPC peering.

## When to Use This Skill

- Setting up private endpoints to eliminate public internet exposure for database connections
- Configuring egress private endpoints for CDC changefeeds to Confluent Kafka or other external services
- Establishing VPC peering between a CockroachDB Cloud cluster and application VPCs
- Troubleshooting DNS resolution issues with private endpoints
- Resolving "stuck pending" or connection failure errors with private endpoints
- Automating private connectivity setup with Terraform

## Prerequisites

- **CockroachDB Cloud cluster** — Standard or Advanced plan (VPC peering requires Advanced)
- **ccloud CLI** authenticated with Cluster Admin role
- **Cloud provider access:**
  - **AWS:** IAM permissions to create VPC endpoints, modify DNS, and manage security groups
  - **GCP:** Permissions to create Private Service Connect endpoints and DNS records
  - **Azure:** Permissions to create private endpoints and manage DNS zones
- **Cluster ID and cloud provider details** from `ccloud cluster info`

**Verify access:**
```bash
ccloud auth whoami
ccloud cluster info <cluster-name> -o json
```

See [ccloud commands reference](references/ccloud-commands.md) for full command syntax.

## Configuration Decisions

Before proceeding, determine which connectivity types and cloud provider apply to the user's environment. Ask which options are relevant, then follow only the corresponding sections below.

**Decision 1 — Connectivity type(s) needed:**
- **Ingress private endpoints:** Applications connect to CockroachDB over a private network path (AWS PrivateLink, GCP Private Service Connect, Azure Private Link). Most common use case.
- **Egress private endpoints:** CockroachDB connects outbound to external services (e.g., Confluent Kafka for CDC) over a private path.
- **VPC peering:** Direct network connection between the application VPC and the CockroachDB Cloud VPC. Requires Advanced plan.
- **Combination:** Multiple connectivity types can be configured together.

**Decision 2 — Cloud provider:**
- **AWS:** Use AWS PrivateLink for ingress, AWS VPC peering for peering.
- **GCP:** Use GCP Private Service Connect for ingress, GCP VPC peering for peering.
- **Azure:** Use Azure Private Link for ingress. VPC peering is not available for Azure.

## Steps

### Part 1: Ingress Private Endpoints

> Follow this part only if the user selected **Ingress private endpoints** in Decision 1. Follow only the subsection (1.2, 1.3, or 1.4) matching the user's cloud provider from Decision 2.

Private endpoints allow applications in your VPC to connect to CockroachDB Cloud without traversing the public internet.

#### 1.1 Get the Private Endpoint Service

Get the private endpoint service information from the **Cloud Console** or **Cloud API**:

**Cloud Console:** Navigate to your cluster's **Networking > Private endpoint** tab. The service name/ID is displayed.

**Cloud API:**
```bash
curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-services" \
  -H "Authorization: Bearer <api-key>"
```

This returns the cloud provider service name/ID needed to create the endpoint in your cloud account.

#### 1.2 Create the Private Endpoint (AWS PrivateLink)

```bash
# In your AWS account, create a VPC endpoint
aws ec2 create-vpc-endpoint \
  --vpc-id <your-vpc-id> \
  --service-name <service-name-from-ccloud> \
  --vpc-endpoint-type Interface \
  --subnet-ids <subnet-id-1> <subnet-id-2> \
  --security-group-ids <security-group-id>
```

**Security group requirements:**
- Allow inbound TCP port 26257 from your application subnets
- Allow outbound to the VPC endpoint

#### 1.3 Create the Private Endpoint (GCP Private Service Connect)

```bash
# Reserve an internal IP address
gcloud compute addresses create cockroachdb-psc \
  --region=<region> \
  --subnet=<subnet> \
  --addresses=<internal-ip>

# Create the Private Service Connect endpoint
gcloud compute forwarding-rules create cockroachdb-psc \
  --region=<region> \
  --network=<network> \
  --address=cockroachdb-psc \
  --target-service-attachment=<service-attachment-from-ccloud>
```

#### 1.4 Create the Private Endpoint (Azure Private Link)

```bash
# Create a private endpoint in your Azure subscription
az network private-endpoint create \
  --name cockroachdb-pe \
  --resource-group <resource-group> \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-connection-resource-id <service-id-from-ccloud> \
  --connection-name cockroachdb-connection
```

#### 1.5 Register the Endpoint in CockroachDB Cloud

Register the private endpoint via the **Cloud Console** or **Cloud API**:

**Cloud Console:** Navigate to your cluster's **Networking > Private endpoint** tab, click **Add a private endpoint**, and enter the cloud provider endpoint ID.

**Cloud API:**
```bash
# Register the private endpoint connection with the cluster
curl -X POST "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"endpoint_id": "<cloud-provider-endpoint-id>"}'
```

**Terraform:**
```hcl
resource "cockroach_private_endpoint_connection" "connection" {
  cluster_id  = cockroach_cluster.cluster.id
  endpoint_id = "<cloud-provider-endpoint-id>"
}
```

Wait for the connection status to become `AVAILABLE` — check in the Cloud Console or via API:
```bash
curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections" \
  -H "Authorization: Bearer <api-key>"
```

#### 1.6 Configure DNS

Private endpoints require DNS configuration so clients resolve the cluster hostname to the private endpoint IP instead of the public IP.

**AWS:** Create a Route 53 private hosted zone with the cluster hostname pointing to the VPC endpoint DNS name.

**GCP:** Create a Cloud DNS private zone with an A record pointing to the reserved internal IP.

**Azure:** Create a private DNS zone with an A record pointing to the private endpoint IP.

See [cloud provider setup reference](references/cloud-provider-setup.md) for detailed DNS configuration steps.

### Part 2: Egress Private Endpoints

> Skip this part if the user did not select **Egress private endpoints** in Decision 1.

Egress private endpoints allow CockroachDB Cloud to connect to external services (e.g., Confluent Kafka for CDC) over a private network path.

#### 2.1 Create an Egress Private Endpoint

Create an egress endpoint via the **Cloud Console** or **Cloud API**:

**Cloud Console:** Navigate to your cluster's **Networking > Egress** tab, click **Add egress endpoint**, and specify the external service.

**Cloud API:**
```bash
# Create an egress endpoint to an external service
curl -X POST "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/egress-endpoints" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"service_name": "<external-service-name>", "cloud_provider": "<AWS|GCP|AZURE>"}'
```

**Common egress targets:**
- Confluent Cloud Kafka (most common use case)
- Amazon MSK
- Self-managed Kafka on PrivateLink
- Other SaaS services with PrivateLink support

#### 2.2 Accept the Endpoint Connection

The external service owner must accept the pending connection request. For Confluent Cloud:

1. Log into Confluent Cloud Console
2. Navigate to **Networking > Private Link Access**
3. Accept the pending connection from the CockroachDB Cloud account

#### 2.3 Verify Egress Endpoint Status

Check egress endpoint status via the Cloud Console (**Networking > Egress** tab) or Cloud API:
```bash
curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/egress-endpoints" \
  -H "Authorization: Bearer <api-key>"
```

**Troubleshooting "stuck pending":**
- Verify the external service has accepted the connection
- Check that the external service is in the same cloud provider region
- Contact the external service admin to accept the pending connection

#### 2.4 Use the Egress Endpoint in CDC Changefeeds

```sql
-- Create a changefeed using the egress endpoint
CREATE CHANGEFEED FOR TABLE orders
  INTO 'kafka://<private-kafka-endpoint>:9092?topic_prefix=crdb_'
  WITH updated, resolved;
```

### Part 3: VPC Peering

> Skip this part if the user did not select **VPC peering** in Decision 1. Follow only the commands matching the user's cloud provider (AWS or GCP) from Decision 2. Azure does not support VPC peering.

VPC peering creates a direct network connection between your VPC and the CockroachDB Cloud VPC.

#### 3.1 Initiate VPC Peering

```bash
# AWS
ccloud cluster networking peering create <cluster-id> \
  --peer-account-id <aws-account-id> \
  --peer-vpc-id <vpc-id> \
  --peer-vpc-region <region> \
  --peer-cidr <cidr-block>

# GCP
ccloud cluster networking peering create <cluster-id> \
  --peer-project-id <gcp-project-id> \
  --peer-network <network-name>
```

#### 3.2 Accept the Peering Request

**AWS:** Accept the peering request in the VPC Console:
```bash
aws ec2 accept-vpc-peering-connection \
  --vpc-peering-connection-id <peering-id>
```

**GCP:** Peering is established automatically if the peer network configuration is correct.

#### 3.3 Configure Route Tables

After peering is established, update route tables to route traffic to the CockroachDB Cloud CIDR through the peering connection.

```bash
# AWS — add a route to the CockroachDB Cloud CIDR
aws ec2 create-route \
  --route-table-id <route-table-id> \
  --destination-cidr-block <cockroachdb-cidr> \
  --vpc-peering-connection-id <peering-id>
```

#### 3.4 Verify VPC Peering

```bash
# Check peering status
ccloud cluster networking peering list <cluster-id> -o json
```

Test connectivity from your VPC:
```bash
# From an instance in your peered VPC
cockroach sql --url "<connection-string>" -e "SELECT 1;"
```

## Safety Considerations

| Impact Type | Severity | Recommendation |
|-------------|----------|----------------|
| Private endpoint creation | Low | Does not affect existing connections; additive change |
| DNS configuration change | Medium | Incorrect DNS can break existing connections |
| IP allowlist interaction | Medium | Private endpoints bypass IP allowlists; review security implications |
| VPC peering CIDR overlap | High | Overlapping CIDRs will prevent peering; plan IP space carefully |
| Egress endpoint creation | Low | Does not affect cluster operation |

**Do not:**
- Delete a private endpoint that has active connections without migrating traffic first
- Configure overlapping CIDR ranges between peered VPCs
- Remove DNS records for private endpoints while clients are connected
- Assume private endpoints replace all other security controls (authentication and authorization still apply)

**When to prefer private endpoints over IP allowlists:**
- When the IP allowlist entry limit is insufficient for your number of source IPs
- When you need to eliminate public internet exposure entirely
- When compliance requirements mandate private network paths

## Rollback

**Remove a private endpoint:**
```bash
# Delete the endpoint connection in CockroachDB Cloud (via Cloud API)
curl -X DELETE "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections/<endpoint-id>" \
  -H "Authorization: Bearer <api-key>"

# Or remove via Cloud Console: Networking > Private endpoint > Delete

# Then delete the endpoint in your cloud provider
# AWS
aws ec2 delete-vpc-endpoints --vpc-endpoint-ids <endpoint-id>
```

**Remove VPC peering:**
```bash
ccloud cluster networking peering delete <cluster-id> --peering-id <peering-id>
```

After removing private connectivity, ensure the IP allowlist is configured to allow connections from the public internet if needed.

## References

**Skill references:**
- [ccloud networking commands](references/ccloud-commands.md)
- [Cloud provider setup steps](references/cloud-provider-setup.md)

**Related skills:**
- [configuring-ip-allowlists](../configuring-ip-allowlists/SKILL.md) — IP-based network access control
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit

**Official CockroachDB Documentation:**
- [Network Authorization](https://www.cockroachlabs.com/docs/cockroachcloud/network-authorization.html)
- [AWS PrivateLink](https://www.cockroachlabs.com/docs/cockroachcloud/aws-privatelink.html)
- [GCP Private Service Connect](https://www.cockroachlabs.com/docs/cockroachcloud/connect-to-an-advanced-cluster)
- [Azure Private Link](https://www.cockroachlabs.com/docs/cockroachcloud/network-authorization)
- [VPC Peering](https://www.cockroachlabs.com/docs/cockroachcloud/network-authorization.html#vpc-peering)
- [Egress Perimeter Controls](https://www.cockroachlabs.com/docs/cockroachcloud/egress-perimeter-controls.html)

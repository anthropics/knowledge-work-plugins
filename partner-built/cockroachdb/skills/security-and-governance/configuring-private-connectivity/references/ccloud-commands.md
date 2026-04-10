# CLI and API Commands for Private Connectivity

This reference provides commands for managing private endpoints, VPC peering, and egress endpoints on CockroachDB Cloud clusters.

> **Note:** The `ccloud` CLI currently only supports IP allowlist management under `networking`. Private endpoint and egress endpoint operations are performed via the **Cloud Console**, **Cloud API**, or **Terraform**. VPC peering commands shown below may require a newer version of `ccloud`.

## Private Endpoint Services (Cloud API)

### List Private Endpoint Services

```bash
# List available private endpoint services for a cluster
curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-services" \
  -H "Authorization: Bearer <api-key>"
```

**Key fields to inspect:**
- `cloud_provider` — AWS, GCP, or Azure
- `service_name` — The cloud provider service name/ID to use when creating the endpoint
- `region` — The region where the service is available
- `status` — Should be AVAILABLE

## Private Endpoint Connections — Ingress (Cloud API / Console / Terraform)

### List Private Endpoint Connections

**Cloud Console:** Navigate to your cluster's **Networking > Private endpoint** tab.

**Cloud API:**
```bash
curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections" \
  -H "Authorization: Bearer <api-key>"
```

**Key fields to inspect:**
- `endpoint_id` — The cloud provider endpoint ID
- `status` — PENDING, AVAILABLE, REJECTED, or DELETED
- `region` — Region of the endpoint

### Create a Private Endpoint Connection

**Cloud Console:** Networking > Private endpoint > Add a private endpoint.

**Cloud API:**
```bash
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

### Delete a Private Endpoint Connection

**Cloud Console:** Networking > Private endpoint > select endpoint > Delete.

**Cloud API:**
```bash
curl -X DELETE "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections/<endpoint-id>" \
  -H "Authorization: Bearer <api-key>"
```

## Egress Private Endpoints (Cloud API / Console)

### List Egress Endpoints

**Cloud Console:** Navigate to your cluster's **Networking > Egress** tab.

**Cloud API:**
```bash
curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/egress-endpoints" \
  -H "Authorization: Bearer <api-key>"
```

**Key fields to inspect:**
- `id` — The egress endpoint ID
- `service_name` — The external service being connected to
- `status` — PENDING, AVAILABLE, REJECTED, or FAILED
- `endpoint_type` — The type of private connectivity

### Create an Egress Endpoint

**Cloud Console:** Networking > Egress > Add egress endpoint.

**Cloud API:**
```bash
curl -X POST "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/egress-endpoints" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"service_name": "<external-service-name>", "cloud_provider": "<AWS|GCP|AZURE>"}'
```

### Delete an Egress Endpoint

**Cloud Console:** Networking > Egress > select endpoint > Delete.

**Cloud API:**
```bash
curl -X DELETE "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/egress-endpoints/<endpoint-id>" \
  -H "Authorization: Bearer <api-key>"
```

## VPC Peering (ccloud CLI)

> VPC peering commands may require a specific version of `ccloud`. Run `ccloud version` to check. If unavailable, use the Cloud Console or Cloud API.

### List VPC Peering Connections

```bash
# List all VPC peering connections for a cluster
ccloud cluster networking peering list <cluster-id> -o json
```

**Key fields to inspect:**
- `id` — The peering connection ID
- `status` — PENDING, ACTIVE, FAILED, or DELETED
- `peer_vpc_id` or `peer_network` — The peered VPC/network
- `peer_cidr` — The CIDR block of the peered network

### Create VPC Peering (AWS)

```bash
ccloud cluster networking peering create <cluster-id> \
  --peer-account-id <aws-account-id> \
  --peer-vpc-id <vpc-id> \
  --peer-vpc-region <region> \
  --peer-cidr <cidr-block>
```

### Create VPC Peering (GCP)

```bash
ccloud cluster networking peering create <cluster-id> \
  --peer-project-id <gcp-project-id> \
  --peer-network <network-name>
```

### Delete VPC Peering

```bash
ccloud cluster networking peering delete <cluster-id> \
  --peering-id <peering-id>
```

## IP Allowlist (ccloud CLI)

Private endpoints bypass the IP allowlist, but the allowlist still applies to public connections.

```bash
# List current allowlist (for comparison with private endpoint setup)
ccloud cluster networking allowlist list <cluster-name> -o json
```

## Notes

- Private endpoint connections require the cloud provider endpoint to be created first
- Egress endpoints require the external service to accept the connection
- VPC peering requires non-overlapping CIDR ranges between the CockroachDB Cloud VPC and the peer VPC
- Private endpoint changes can take several minutes to propagate
- For Terraform examples, see [cloud provider setup reference](cloud-provider-setup.md)

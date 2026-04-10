# Cloud Provider Setup for Private Connectivity

This reference provides cloud provider-specific setup steps for private endpoints, DNS configuration, and VPC peering with CockroachDB Cloud.

## AWS PrivateLink Setup

### Step 1: Create a VPC Endpoint

```bash
# Get the service name from the Cloud Console (Networking > Private endpoint)
# or via Cloud API:
# curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-services" \
#   -H "Authorization: Bearer <api-key>"
# Note the "service_name" value (e.g., com.amazonaws.vpce.us-east-1.vpce-svc-xxxx)

# Create the VPC endpoint
aws ec2 create-vpc-endpoint \
  --vpc-id <your-vpc-id> \
  --service-name <service-name> \
  --vpc-endpoint-type Interface \
  --subnet-ids <subnet-1> <subnet-2> <subnet-3> \
  --security-group-ids <sg-id>
```

### Step 2: Configure Security Group

The security group attached to the VPC endpoint must allow:

| Direction | Protocol | Port | Source/Destination |
|-----------|----------|------|--------------------|
| Inbound | TCP | 26257 | Application subnets CIDR |
| Outbound | All | All | 0.0.0.0/0 |

### Step 3: Configure DNS (Route 53)

```bash
# Create a private hosted zone for the cluster hostname
aws route53 create-hosted-zone \
  --name <cluster-hostname> \
  --vpc VPCRegion=<region>,VPCId=<vpc-id> \
  --caller-reference <unique-string> \
  --hosted-zone-config PrivateZone=true

# Create a CNAME record pointing to the VPC endpoint DNS name
aws route53 change-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "<cluster-hostname>",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "<vpc-endpoint-dns-name>"}]
      }
    }]
  }'
```

### Step 4: Register with CockroachDB Cloud

Register the endpoint via Cloud Console (**Networking > Private endpoint > Add**) or Cloud API:
```bash
curl -X POST "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"endpoint_id": "<vpce-xxxx>"}'
```

Or via Terraform:
```hcl
resource "cockroach_private_endpoint_connection" "main" {
  cluster_id  = "<cluster-id>"
  endpoint_id = aws_vpc_endpoint.cockroachdb.id
}
```

## GCP Private Service Connect Setup

### Step 1: Reserve an Internal IP Address

```bash
gcloud compute addresses create cockroachdb-psc-ip \
  --region=<region> \
  --subnet=<subnet-name> \
  --addresses=<internal-ip>
```

### Step 2: Create the Forwarding Rule

```bash
# Get the service attachment from the Cloud Console (Networking > Private endpoint)
# or via Cloud API:
# curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-services" \
#   -H "Authorization: Bearer <api-key>"
# Note the "service_name" value (the service attachment URI)

gcloud compute forwarding-rules create cockroachdb-psc \
  --region=<region> \
  --network=<network-name> \
  --address=cockroachdb-psc-ip \
  --target-service-attachment=<service-attachment-uri> \
  --load-balancing-scheme=""
```

### Step 3: Configure DNS (Cloud DNS)

```bash
# Create a private DNS zone
gcloud dns managed-zones create cockroachdb-private \
  --dns-name="<cluster-hostname>." \
  --description="CockroachDB Private DNS" \
  --visibility=private \
  --networks=<network-name>

# Add an A record pointing to the reserved internal IP
gcloud dns record-sets create "<cluster-hostname>." \
  --zone=cockroachdb-private \
  --type=A \
  --ttl=300 \
  --rrdatas=<internal-ip>
```

### Step 4: Register with CockroachDB Cloud

Register via Cloud Console (**Networking > Private endpoint > Add**) or Cloud API:
```bash
curl -X POST "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"endpoint_id": "<forwarding-rule-uri>"}'
```

## Azure Private Link Setup

### Step 1: Create a Private Endpoint

```bash
# Get the service ID from Cloud Console (Networking > Private endpoint)
# or via Cloud API:
# curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-services" \
#   -H "Authorization: Bearer <api-key>"

az network private-endpoint create \
  --name cockroachdb-pe \
  --resource-group <resource-group> \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-connection-resource-id <service-id> \
  --connection-name cockroachdb-connection \
  --location <region>
```

### Step 2: Configure DNS (Azure Private DNS Zone)

```bash
# Create a private DNS zone
az network private-dns zone create \
  --resource-group <resource-group> \
  --name <cluster-hostname>

# Link the DNS zone to your VNet
az network private-dns link vnet create \
  --resource-group <resource-group> \
  --zone-name <cluster-hostname> \
  --name cockroachdb-dns-link \
  --virtual-network <vnet-name> \
  --registration-enabled false

# Create an A record
az network private-dns record-set a add-record \
  --resource-group <resource-group> \
  --zone-name <cluster-hostname> \
  --record-set-name "@" \
  --ipv4-address <private-endpoint-ip>
```

### Step 3: Register with CockroachDB Cloud

Register via Cloud Console (**Networking > Private endpoint > Add**) or Cloud API:
```bash
curl -X POST "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"endpoint_id": "<azure-endpoint-id>"}'
```

## Egress Private Endpoints to Confluent Cloud Kafka

This is the most common egress use case — connecting CockroachDB CDC changefeeds to Confluent Cloud Kafka over PrivateLink.

### AWS

1. Create an egress endpoint via Cloud Console (**Networking > Egress > Add**) or Cloud API:
   ```bash
   curl -X POST "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/egress-endpoints" \
     -H "Authorization: Bearer <api-key>" \
     -H "Content-Type: application/json" \
     -d '{"service_name": "<confluent-privatelink-service-name>", "cloud_provider": "AWS"}'
   ```

2. In Confluent Cloud Console:
   - Navigate to **Networking > Private Link Access**
   - Accept the pending connection from the CockroachDB Cloud AWS account

3. Verify the egress endpoint status is AVAILABLE in Cloud Console (**Networking > Egress** tab) or via API:
   ```bash
   curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/egress-endpoints" \
     -H "Authorization: Bearer <api-key>"
   ```

4. Create a changefeed using the private Kafka endpoint:
   ```sql
   CREATE CHANGEFEED FOR TABLE orders
     INTO 'kafka://<confluent-private-endpoint>:9092?topic_prefix=crdb_'
     WITH updated, resolved;
   ```

### GCP

Follow the same pattern using GCP Private Service Connect instead of AWS PrivateLink. The Confluent Cloud service attachment is different for each cloud provider.

## VPC Peering Route Table Setup

### AWS

After VPC peering is active, add routes to your route tables:

```bash
# Get the CockroachDB Cloud VPC CIDR from the peering details
ccloud cluster networking peering list <cluster-id> -o json

# Add a route in your route table
aws ec2 create-route \
  --route-table-id <rtb-xxxx> \
  --destination-cidr-block <cockroachdb-cidr> \
  --vpc-peering-connection-id <pcx-xxxx>
```

Repeat for each route table associated with subnets that need access to CockroachDB.

### GCP

GCP VPC peering automatically exchanges routes. Verify with:

```bash
gcloud compute routes list --filter="network=<network-name>"
```

## Terraform Examples

### AWS PrivateLink with Terraform

```hcl
resource "aws_vpc_endpoint" "cockroachdb" {
  vpc_id             = aws_vpc.main.id
  service_name       = "<service-name-from-ccloud>"
  vpc_endpoint_type  = "Interface"
  subnet_ids         = [aws_subnet.private_a.id, aws_subnet.private_b.id]
  security_group_ids = [aws_security_group.cockroachdb_endpoint.id]
}

resource "cockroach_private_endpoint_connection" "main" {
  cluster_id  = "<cluster-id>"
  endpoint_id = aws_vpc_endpoint.cockroachdb.id
}
```

### GCP Private Service Connect with Terraform

```hcl
resource "google_compute_address" "cockroachdb_psc" {
  name         = "cockroachdb-psc"
  region       = "<region>"
  subnetwork   = google_compute_subnetwork.main.id
  address_type = "INTERNAL"
}

resource "google_compute_forwarding_rule" "cockroachdb_psc" {
  name                  = "cockroachdb-psc"
  region                = "<region>"
  network               = google_compute_network.main.id
  ip_address            = google_compute_address.cockroachdb_psc.id
  target                = "<service-attachment-from-ccloud>"
  load_balancing_scheme = ""
}
```

## Troubleshooting

### DNS Resolution Issues

```bash
# Verify DNS resolves to private IP (not public)
nslookup <cluster-hostname>
dig <cluster-hostname>

# If resolving to public IP:
# 1. Check private DNS zone is linked to your VPC/VNet
# 2. Check the DNS record points to the correct endpoint IP
# 3. Verify DNS is being served from the private zone (not public)
```

### Connection Timeout After Private Endpoint Setup

1. Verify security group allows port 26257
2. Check the endpoint is in the same AZ as your application
3. Verify the endpoint status is AVAILABLE (not PENDING)
4. Test network connectivity: `nc -zv <private-endpoint-ip> 26257`

## Notes

- Private endpoints provide the highest level of network isolation
- DNS configuration is critical — incorrect DNS will route traffic over the public internet
- VPC peering and private endpoints can coexist on the same cluster
- Egress endpoint changes may take 5-10 minutes to propagate
- Terraform `cockroach` provider is required for CockroachDB Cloud resources

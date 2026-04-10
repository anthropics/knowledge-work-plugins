# Cloud Provider IAM Setup for Log Export

This reference provides cloud provider-specific IAM and permission setup for CockroachDB Cloud log and metric export.

## AWS CloudWatch — IAM Role Setup

### Log Export IAM Role

CockroachDB Cloud needs a cross-account IAM role to write logs to your CloudWatch log group.

#### Step 1: Create the IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:<region>:<your-account-id>:log-group:cockroachdb-*",
        "arn:aws:logs:<region>:<your-account-id>:log-group:cockroachdb-*:*"
      ]
    }
  ]
}
```

#### Step 2: Create the IAM Role with Trust Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "<cockroachdb-cloud-account-arn>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<cluster-id>"
        }
      }
    }
  ]
}
```

The CockroachDB Cloud account ARN is provided in the log export setup instructions in the Cloud Console.

#### Step 3: Create the Role

```bash
# Create the IAM policy
aws iam create-policy \
  --policy-name CockroachDBLogExport \
  --policy-document file://log-export-policy.json

# Create the IAM role with trust policy
aws iam create-role \
  --role-name CockroachDBLogExport \
  --assume-role-policy-document file://trust-policy.json

# Attach the policy to the role
aws iam attach-role-policy \
  --role-name CockroachDBLogExport \
  --policy-arn arn:aws:iam::<your-account-id>:policy/CockroachDBLogExport
```

### Metric Export IAM Role

For CloudWatch metric export, the IAM role needs additional permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "cloudwatch:namespace": "CockroachDB"
        }
      }
    }
  ]
}
```

The same trust policy as log export can be used. You can attach both policies to a single IAM role.

## GCP Cloud Logging — Service Account Setup

### Step 1: Enable Required APIs

```bash
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
```

### Step 2: Grant Permissions

The CockroachDB Cloud service account needs the `Logs Writer` role:

```bash
# Get the CockroachDB Cloud service account email from cluster info
ccloud cluster info <cluster-name> -o json
# Look for the service account email in the output

# Grant Logs Writer role
gcloud projects add-iam-policy-binding <gcp-project-id> \
  --member="serviceAccount:<cockroachdb-service-account-email>" \
  --role="roles/logging.logWriter"
```

For metric export, also grant:
```bash
gcloud projects add-iam-policy-binding <gcp-project-id> \
  --member="serviceAccount:<cockroachdb-service-account-email>" \
  --role="roles/monitoring.metricWriter"
```

## Datadog — API Key Setup

### Step 1: Create a Datadog API Key

1. Log into Datadog
2. Navigate to **Organization Settings > API Keys**
3. Create a new API key named "CockroachDB Cloud"
4. Copy the API key value

### Step 2: Identify Your Datadog Site

| Datadog URL | Site Value |
|-------------|-----------|
| app.datadoghq.com | `datadoghq.com` |
| app.datadoghq.eu | `datadoghq.eu` |
| us3.datadoghq.com | `us3.datadoghq.com` |
| us5.datadoghq.com | `us5.datadoghq.com` |
| app.ddog-gov.com | `ddog-gov.com` |

## Cost Estimation

### CloudWatch Logs

| Component | Price (us-east-1) | Notes |
|-----------|-------------------|-------|
| Log ingestion | $0.50/GB | All log data sent to CloudWatch |
| Log storage | $0.03/GB/month | After retention period, automatically deleted |
| Log queries | $0.005/GB scanned | CloudWatch Logs Insights queries |

**Estimating log volume:**
- A low-traffic cluster generates ~500 MB/day of logs
- A high-traffic cluster with audit logging can generate 5-10 GB/day per node
- Admin audit logging adds ~1-5% to log volume
- Role-based audit logging adds proportionally to audited query volume

### CloudWatch Metrics

| Component | Price | Notes |
|-----------|-------|-------|
| Custom metrics | $0.30/metric/month (first 10k) | Each CockroachDB metric is a custom metric |
| API requests | $0.01/1000 PutMetricData calls | Metrics are pushed at regular intervals |

## Troubleshooting

### Log Export Shows ENABLED but No Logs Appear

1. Check the IAM role permissions are correct
2. Verify the log group name matches the configured export target
3. Allow 5-10 minutes for initial log delivery
4. Check CloudTrail for `AssumeRole` failures (AWS)
5. Check the CockroachDB Cloud cluster is running and generating logs

### "Internal error" When Enabling Log Export

1. Verify the IAM role ARN is correct (no typos)
2. Verify the trust policy allows the CockroachDB Cloud account
3. Verify the external ID matches the cluster ID
4. Check that the log group exists in the specified region

### Terraform Race Condition

When creating a cluster with log export and CMEK in the same Terraform configuration:

```hcl
# Add explicit dependency to avoid race condition
resource "cockroach_log_export_config" "main" {
  depends_on = [cockroach_cluster.main]
  # ... config
}
```

Or split into two `terraform apply` runs: first create the cluster, then add log export.

## Notes

- Log export is a Cloud Advanced plan feature only
- Logs are exported in near real-time (seconds to minutes of delay)
- Disabling log export does not delete existing logs in the destination
- Re-enabling log export does not backfill historical logs
- Each cluster can have one log export configuration at a time
- Metric export can target both CloudWatch and Datadog simultaneously

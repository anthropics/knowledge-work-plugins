---
name: configuring-log-export
description: Configures log and metric export for CockroachDB Cloud clusters to external monitoring services including AWS CloudWatch, GCP Cloud Logging, and Datadog. Use when setting up log export for audit compliance, configuring metric export for monitoring, or troubleshooting log delivery issues.
compatibility: Requires CockroachDB Cloud Advanced plan. Requires ccloud CLI with Cluster Admin role and cloud provider IAM configuration.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Configuring Log Export

Configures log and metric export for CockroachDB Cloud clusters to deliver cluster logs, audit logs, and performance metrics to external monitoring services. Supports AWS CloudWatch, GCP Cloud Logging, and third-party integrations like Datadog.

## When to Use This Skill

- Setting up log export to AWS CloudWatch or GCP Cloud Logging
- Configuring metric export to CloudWatch or Datadog
- Verifying that SQL audit logs are being exported to an external sink
- Troubleshooting log export errors or missing logs
- Estimating CloudWatch or logging service costs for CockroachDB log volume
- Configuring log export via Terraform

## Prerequisites

- **CockroachDB Cloud Advanced plan** — Log export is not available on Basic or Standard plans
- **ccloud CLI** authenticated with Cluster Admin role
- **Cloud provider setup:**
  - **AWS:** CloudWatch Logs group created, IAM role granting CockroachDB Cloud cross-account access
  - **GCP:** Cloud Logging API enabled, service account with Logs Writer role
- **Cluster ID:** Available from `ccloud cluster list`

**Verify access:**
```bash
ccloud auth whoami
ccloud cluster info <cluster-name> -o json
# Look for "plan": "ADVANCED"
```

## Configuration Decisions

Before proceeding, determine which export destinations apply to the user's environment. Ask which options are relevant, then follow only the corresponding sections below.

**Decision 1 — Log export destination:**
- **AWS CloudWatch:** Use when the cluster runs on AWS and logs should go to CloudWatch Logs. Requires IAM cross-account role setup.
- **GCP Cloud Logging:** Use when the cluster runs on GCP. Requires a service account with Logs Writer role.

**Decision 2 — Metric export destination:**
- **CloudWatch:** Use when metrics should go to AWS CloudWatch. Requires IAM role with `cloudwatch:PutMetricData` permission.
- **Datadog:** Use when metrics should go to Datadog. Requires a Datadog API key and site.
- **Skip:** No metric export needed at this time.

## Steps

### 1. Check Current Log Export Configuration

```bash
# Check if log export is currently configured
ccloud cluster info <cluster-name> -o json
# Look for "log_export_config" in the output
```

### 2. Set Up Log Export to AWS CloudWatch

> Follow this section only if the user selected **AWS CloudWatch** in Decision 1. Skip to Step 3 if using GCP Cloud Logging.

#### 2.1 Create a CloudWatch Log Group

```bash
# Create a log group in AWS (if it doesn't exist)
aws logs create-log-group \
  --log-group-name cockroachdb-<cluster-name> \
  --region <aws-region>

# Set retention policy (recommended)
aws logs put-retention-policy \
  --log-group-name cockroachdb-<cluster-name> \
  --retention-in-days 90 \
  --region <aws-region>
```

#### 2.2 Create an IAM Role for CockroachDB Cloud

See [cloud provider setup reference](references/cloud-provider-setup.md) for the complete IAM role policy.

The IAM role must:
- Trust the CockroachDB Cloud AWS account as an allowed principal
- Grant `logs:CreateLogStream`, `logs:PutLogEvents`, `logs:DescribeLogGroups`, `logs:DescribeLogStreams` permissions
- Be scoped to the specific log group

#### 2.3 Enable Log Export

```bash
# Enable log export to CloudWatch
ccloud cluster log-export create <cluster-id> \
  --log-group-name cockroachdb-<cluster-name> \
  --auth-principal <iam-role-arn> \
  --type AWS_CLOUDWATCH \
  --region <aws-region>
```

### 3. Set Up Log Export to GCP Cloud Logging

> Follow this section only if the user selected **GCP Cloud Logging** in Decision 1. Skip if using AWS CloudWatch.

#### 3.1 Enable Cloud Logging API

```bash
gcloud services enable logging.googleapis.com
```

#### 3.2 Grant CockroachDB Cloud Service Account Access

```bash
# Get the CockroachDB Cloud service account from ccloud cluster info
# Grant Logs Writer role
gcloud projects add-iam-policy-binding <gcp-project-id> \
  --member="serviceAccount:<cockroachdb-service-account>" \
  --role="roles/logging.logWriter"
```

#### 3.3 Enable Log Export

```bash
ccloud cluster log-export create <cluster-id> \
  --auth-principal <gcp-project-id> \
  --type GCP_CLOUD_LOGGING
```

### 4. Configure Metric Export

> Skip this section if the user selected **Skip** in Decision 2. Follow only the relevant subsection (4.1 or 4.2) based on the selected metric export destination.

Metric export sends CockroachDB performance metrics to CloudWatch or Datadog.

#### 4.1 Metric Export to CloudWatch

```bash
ccloud cluster metric-export create cloudwatch <cluster-id> \
  --role-arn <iam-role-arn> \
  --target-region <aws-region>
```

The IAM role for metric export needs `cloudwatch:PutMetricData` permission.

#### 4.2 Metric Export to Datadog

```bash
ccloud cluster metric-export create datadog <cluster-id> \
  --api-key <datadog-api-key> \
  --site <datadog-site>
```

**Datadog site values:** `datadoghq.com` (US), `datadoghq.eu` (EU), `us3.datadoghq.com` (US3), `us5.datadoghq.com` (US5)

### 5. Verify Log and Metric Export

```bash
# Check log export status
ccloud cluster log-export list <cluster-id> -o json
# Status should be ENABLED

# Check metric export status
ccloud cluster metric-export list <cluster-id> -o json
```

**Verify log delivery in CloudWatch:**
```bash
# Check for recent log streams
aws logs describe-log-streams \
  --log-group-name cockroachdb-<cluster-name> \
  --order-by LastEventTime \
  --descending \
  --limit 5 \
  --region <aws-region>

# Tail recent log events
aws logs tail cockroachdb-<cluster-name> \
  --since 1h \
  --region <aws-region>
```

**Verify audit logs are being exported:**

Audit logs are included in the log export if SQL audit logging is enabled on the cluster. To confirm:

```sql
-- Check audit logging is enabled
SHOW CLUSTER SETTING sql.log.admin_audit.enabled;
SHOW CLUSTER SETTING sql.log.user_audit;
```

If audit logging is enabled but audit events are not appearing in CloudWatch, check:
1. Log export status is ENABLED
2. The IAM role has correct permissions
3. Log group name matches the configured export target
4. Allow 5-10 minutes for initial log delivery

### 6. Configure Log Export via Terraform

```hcl
resource "cockroach_log_export_config" "main" {
  id         = cockroach_cluster.main.id
  auth_principal = "<iam-role-arn>"
  log_name       = "cockroachdb-${cockroach_cluster.main.name}"
  type           = "AWS_CLOUDWATCH"
  region         = "<aws-region>"
}

resource "cockroach_metric_export_cloudwatch_config" "main" {
  id         = cockroach_cluster.main.id
  role_arn       = "<iam-role-arn>"
  target_region  = "<aws-region>"
}
```

**Known Terraform issue:** Creating a cluster with log export and CMEK in the same `terraform apply` can cause a race condition. Apply the cluster first, then add log export and CMEK configurations in a subsequent apply.

## Safety Considerations

| Impact Type | Severity | Recommendation |
|-------------|----------|----------------|
| Log export enabling | Low | No impact on cluster operation |
| Log export disabling | Low | Stops log delivery but does not affect cluster |
| IAM misconfiguration | Medium | Log export will fail silently; monitor for delivery gaps |
| Cost impact | Medium | High-volume clusters can generate significant CloudWatch/logging costs |
| Terraform race condition | Medium | Apply cluster creation before log/CMEK config |

**Cost planning:**
- CockroachDB Cloud can generate 1-10 GB of logs per day per node depending on query volume and audit settings
- CloudWatch Logs pricing: ~$0.50/GB ingestion + $0.03/GB storage/month (varies by region)
- Enable log retention policies to control storage costs
- Audit logging significantly increases log volume — plan accordingly

**Do not:**
- Delete the CloudWatch log group while log export is active (will cause delivery errors)
- Revoke IAM permissions without disabling log export first
- Enable cluster-wide SQL audit logging without considering the log volume increase

## Rollback

```bash
# Disable log export
ccloud cluster log-export delete <cluster-id>

# Disable metric export
ccloud cluster metric-export delete cloudwatch <cluster-id>
ccloud cluster metric-export delete datadog <cluster-id>
```

Log export can be re-enabled at any time with the same or different configuration. Historical logs are not re-sent — only new logs are exported after re-enabling.

## References

**Skill references:**
- [Cloud provider IAM setup](references/cloud-provider-setup.md)

**Related skills:**
- [configuring-audit-logging](../configuring-audit-logging/SKILL.md) — Enable SQL audit logging (must be enabled for audit logs to appear in export)
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit

**Official CockroachDB Documentation:**
- [Export Logs From a CockroachDB Cloud Cluster](https://www.cockroachlabs.com/docs/cockroachcloud/export-logs.html)
- [Export Metrics From a CockroachDB Cloud Cluster](https://www.cockroachlabs.com/docs/cockroachcloud/export-metrics.html)
- [Cloud API — Log Export](https://www.cockroachlabs.com/docs/cockroachcloud/cloud-api.html)

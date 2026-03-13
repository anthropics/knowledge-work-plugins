---
name: "SAP Datasphere CLI Automator"
description: "Automate Datasphere administration with CLI commands! Use this skill when you need to bulk-provision users, create spaces programmatically, manage connections at scale, rotate certificates, or integrate Datasphere into CI/CD pipelines. Ideal for DevOps teams, system administrators, and enterprises managing hundreds of users or multi-system landscapes through Infrastructure-as-Code."
---

# SAP Datasphere CLI Automator

## Overview

The SAP Datasphere CLI (Command-Line Interface) is the power user's gateway to programmatic administration and automation. While the Datasphere UI excels at interactive tasks, the CLI is your tool of choice when you need to:

- **Bulk Operations**: Provision hundreds or thousands of users, create multiple spaces, configure connections across landscapes
- **Infrastructure-as-Code**: Version control your Datasphere configuration in Git, deploy changes through pipelines
- **Scheduled Automation**: Trigger administrative tasks on schedules via cron, Task Chains, or cloud schedulers
- **CI/CD Integration**: Embed Datasphere provisioning into your DevOps pipeline (GitHub Actions, Azure DevOps, Jenkins)
- **Headless Environments**: Automate when no UI access is available or when running in containerized systems

### CLI vs GUI: When to Use Each

| Scenario | CLI | GUI |
|----------|-----|-----|
| Creating 500 users with attributes | ✓ | ✗ |
| Exploring data model visually | ✗ | ✓ |
| One-time user creation | Possible | ✓ |
| Batch certificate rotation | ✓ | ✗ |
| Setting up connection for testing | ✗ | ✓ |
| Deploying 10 connections across 5 systems | ✓ | ✗ |
| Configuring space capacity | ✓ | ✓ |
| Validating connection credentials | ✓ | ✓ |

## Authentication and Setup

Before using the CLI, configure authentication to your Datasphere instance.

### Service Key Authentication (Recommended for Automation)

Service keys are non-human identities ideal for automation, CI/CD, and scheduled tasks.

1. **Create a Service Key in Datasphere**:
   - Navigate to **System > Administration > Security**
   - Create a new service key with appropriate scope
   - Download the key file (JSON format containing client ID, secret, URL)

2. **Configure CLI with Service Key**:
   ```bash
   datasphere config init \
     --client-id "your-client-id" \
     --client-secret "your-client-secret" \
     --instance-url "https://your-datasphere-instance.com" \
     --auth-method service-key
   ```

3. **Store in Environment Variables** (for CI/CD pipelines):
   ```bash
   export DATASPHERE_CLIENT_ID="your-client-id"
   export DATASPHERE_CLIENT_SECRET="your-client-secret"
   export DATASPHERE_INSTANCE_URL="https://your-datasphere-instance.com"
   ```

### OAuth Token Authentication (Interactive Use)

For personal workstations with interactive CLI use:

```bash
datasphere config init --auth-method oauth
# Opens browser for authentication
```

### Verify Configuration

```bash
datasphere config validate
# Output: Configuration valid. Connected to datasphere.acme.com
```

## Space Management via CLI

Spaces are the foundational containers in Datasphere. Manage them programmatically for consistent environments.

### Creating a Single Space

```bash
datasphere spaces create \
  --name "SALES_ANALYTICS" \
  --description "Sales and Revenue Analytics Space" \
  --ram-allocation 100 \
  --disk-allocation 500 \
  --priority standard
```

### Space Definition JSON (for bulk operations)

Create a `spaces.json` file for reusable space configurations:

```json
{
  "spaces": [
    {
      "name": "SALES_ANALYTICS",
      "description": "Sales and Revenue Analytics",
      "configuration": {
        "memory": {
          "allocated_gb": 100,
          "reserved_gb": 50
        },
        "disk": {
          "allocated_gb": 500
        },
        "priority": "standard",
        "network": {
          "enable_public_access": false,
          "data_isolation_level": "tenant"
        }
      },
      "owner": "sales-admin@company.com",
      "tags": ["production", "analytics"]
    },
    {
      "name": "FINANCE_REPORTING",
      "description": "Finance and Accounting Reporting",
      "configuration": {
        "memory": {
          "allocated_gb": 150,
          "reserved_gb": 75
        },
        "disk": {
          "allocated_gb": 1000
        },
        "priority": "high",
        "network": {
          "enable_public_access": false,
          "data_isolation_level": "tenant"
        }
      },
      "owner": "finance-admin@company.com",
      "tags": ["production", "finance"]
    }
  ]
}
```

### Bulk Space Creation

```bash
datasphere spaces create-bulk --file spaces.json --validate --dry-run
# Review output before committing

datasphere spaces create-bulk --file spaces.json --confirm
```

### Pre-allocating Resources

Control memory, disk, and processing priority during creation:

```bash
datasphere spaces create \
  --name "HIGH_PERFORMANCE_SPACE" \
  --ram-allocation 200 \
  --disk-allocation 2000 \
  --priority high \
  --reserved-memory 100 \
  --network-isolation strict
```

**Resource Allocation Guide**:
- **RAM**: Minimum 50 GB for development, 100+ GB for production analytics
- **Disk**: 5x your expected data volume
- **Priority**: `low` (shared), `standard` (default), `high` (guaranteed resources)

### Space Cloning

Duplicate an existing space configuration as a template:

```bash
datasphere spaces clone \
  --source "PROD_TEMPLATE" \
  --target "NEW_ENVIRONMENT" \
  --copy-connections true \
  --copy-users false
```

### Space Configuration Updates

Modify existing space settings:

```bash
datasphere spaces update SALES_ANALYTICS \
  --new-ram-allocation 150 \
  --new-disk-allocation 750 \
  --new-description "Updated: Sales and Revenue Analytics (upgraded)"
```

## User Management via CLI

Efficiently provision and manage users at scale.

### Batch User Onboarding

Create a `users.json` file:

```json
{
  "users": [
    {
      "email": "alice.johnson@company.com",
      "first_name": "Alice",
      "last_name": "Johnson",
      "roles": [
        {
          "role": "datasphere.admin",
          "scope": "global"
        }
      ],
      "space_assignments": [
        {
          "space_name": "SALES_ANALYTICS",
          "role": "space_admin"
        }
      ],
      "attributes": {
        "department": "Sales",
        "cost_center": "CC-1001",
        "manager": "bob.smith@company.com"
      },
      "status": "active"
    },
    {
      "email": "charlie.brown@company.com",
      "first_name": "Charlie",
      "last_name": "Brown",
      "roles": [
        {
          "role": "datasphere.analyst",
          "scope": "global"
        }
      ],
      "space_assignments": [
        {
          "space_name": "SALES_ANALYTICS",
          "role": "viewer"
        },
        {
          "space_name": "FINANCE_REPORTING",
          "role": "editor"
        }
      ],
      "attributes": {
        "department": "Finance",
        "cost_center": "CC-2001",
        "manager": "alice.johnson@company.com"
      },
      "status": "active"
    }
  ]
}
```

### Execute Bulk User Provisioning

```bash
datasphere users create-bulk \
  --file users.json \
  --validate \
  --dry-run
# Review output

datasphere users create-bulk \
  --file users.json \
  --send-invitations true \
  --confirm
```

**Output**: Lists success/failure per user, generates report with invitation links.

### Assigning Scoped Roles Programmatically

Scoped Roles attach users to specific spaces with granular permissions:

```bash
datasphere users assign-role \
  --email "alice.johnson@company.com" \
  --role "datasphere.space_admin" \
  --space "SALES_ANALYTICS" \
  --effective-date "2024-02-01"
```

**Available Scoped Roles**:
- `datasphere.space_admin` — Full space administration
- `datasphere.space_editor` — Create and modify objects
- `datasphere.space_viewer` — Read-only access

### User Attribute Management

Store custom metadata on users for governance and integration:

```bash
datasphere users set-attribute \
  --email "alice.johnson@company.com" \
  --attribute "department" \
  --value "Sales" \
  --attribute "cost_center" \
  --value "CC-1001"
```

Bulk update attributes:

```bash
datasphere users batch-attributes \
  --file user_attributes.json
```

Where `user_attributes.json` contains:

```json
{
  "updates": [
    {
      "email": "alice.johnson@company.com",
      "attributes": {
        "department": "Sales",
        "cost_center": "CC-1001",
        "manager": "bob.smith@company.com"
      }
    }
  ]
}
```

### User Deprovisioning Workflows

**Soft Deprovisioning** (disable access without deleting):

```bash
datasphere users disable \
  --email "alice.johnson@company.com" \
  --reason "Employee departure" \
  --effective-date "2024-03-15"
```

**Hard Deprovisioning** (permanent deletion):

```bash
datasphere users delete \
  --email "alice.johnson@company.com" \
  --transfer-owned-objects-to "admin@company.com" \
  --confirm
```

## Connection Management via CLI

Datasphere connections link to source and target systems. Manage them at scale via JSON templates.

### Creating Connections from JSON Templates

Create a `connections.json` file:

```json
{
  "connections": [
    {
      "name": "PROD_SAP_S4",
      "type": "sap_s4hana",
      "description": "Production SAP S/4HANA System",
      "technical_user": "DATASPHERE_USER",
      "connection_details": {
        "host": "s4h-prod.company.com",
        "port": 50013,
        "client": "100",
        "use_ssl": true,
        "tls_version": "1.2"
      },
      "authentication": {
        "method": "basic",
        "username_variable": "SAP_USER",
        "password_variable": "SAP_PASS"
      },
      "test_table": "MARA",
      "retry_policy": {
        "max_attempts": 3,
        "backoff_seconds": 5
      },
      "owner": "integration-admin@company.com"
    },
    {
      "name": "SNOWFLAKE_WAREHOUSE",
      "type": "snowflake",
      "description": "Snowflake Data Warehouse",
      "connection_details": {
        "account_identifier": "xy12345.us-east-1",
        "warehouse": "COMPUTE_WH",
        "database": "DATASPHERE_DB",
        "schema": "STAGING"
      },
      "authentication": {
        "method": "oauth",
        "client_id_variable": "SF_CLIENT_ID",
        "client_secret_variable": "SF_CLIENT_SECRET",
        "token_endpoint": "https://xy12345.us-east-1.snowflakecomputing.com/oauth/authorize"
      },
      "test_query": "SELECT 1",
      "owner": "data-team@company.com"
    }
  ]
}
```

### Bulk Connection Setup

```bash
datasphere connections create-bulk \
  --file connections.json \
  --validate-credentials \
  --dry-run
# Verify output

datasphere connections create-bulk \
  --file connections.json \
  --confirm
```

### Connection Validation and Testing

Verify connectivity before deployment:

```bash
datasphere connections test \
  --name "PROD_SAP_S4" \
  --verbose
# Output: Connection test successful. Response time: 145ms
```

Batch test multiple connections:

```bash
datasphere connections test-batch \
  --file connections.json \
  --generate-report test_results.html
```

## Certificate Management

Manage TLS server certificates for secure connections to external systems.

### Certificate Lifecycle Operations

**List Current Certificates**:

```bash
datasphere configuration certificates list \
  --show-expiry \
  --sort-by "expiry_date"
```

**Upload New Certificate**:

```bash
datasphere configuration certificates upload \
  --name "PROD_SAP_S4_CERT" \
  --certificate-file "/path/to/certificate.pem" \
  --key-file "/path/to/private.key" \
  --description "Production S/4HANA TLS Certificate"
```

**Certificate Rotation Workflow**:

```bash
# 1. Upload new certificate
datasphere configuration certificates upload \
  --name "PROD_SAP_S4_CERT_NEW" \
  --certificate-file "/path/to/new_cert.pem" \
  --key-file "/path/to/new_key.pem" \
  --scheduled-activation "2024-02-15T00:00:00Z"

# 2. Activate new certificate (automatic at scheduled time or manual)
datasphere configuration certificates activate \
  --name "PROD_SAP_S4_CERT_NEW"

# 3. Deactivate old certificate
datasphere configuration certificates deactivate \
  --name "PROD_SAP_S4_CERT"

# 4. Clean up (optional, after verification period)
datasphere configuration certificates delete \
  --name "PROD_SAP_S4_CERT" \
  --force
```

### Expiry Monitoring and Alerting

Create an automated monitoring script:

```bash
#!/bin/bash
# cert_expiry_check.sh - Monitor certificate expiry

ALERT_DAYS=30
RECIPIENTS="security-team@company.com"

datasphere configuration certificates list --json > certs.json

python3 << 'EOF'
import json
from datetime import datetime, timedelta

with open('certs.json') as f:
    certs = json.load(f)

alert_threshold = datetime.utcnow() + timedelta(days=ALERT_DAYS)

for cert in certs['certificates']:
    expiry = datetime.fromisoformat(cert['expiry_date'])
    if expiry < alert_threshold:
        print(f"ALERT: {cert['name']} expires on {cert['expiry_date']}")
EOF
```

Schedule in cron:

```bash
# Run daily at 6 AM
0 6 * * * /opt/datasphere/cert_expiry_check.sh | mail -s "Datasphere Certificate Expiry Alert" security-team@company.com
```

## Task Automation Patterns

### Scheduling CLI Commands via Cron

Execute administrative tasks on a schedule:

```bash
# Daily space quota report
0 2 * * * datasphere spaces report --format json > /var/reports/space_quota_$(date +\%Y\%m\%d).json

# Weekly user access review
0 3 * * 0 datasphere users list --inactive-days 30 > /var/reports/inactive_users.txt

# Monthly certificate expiry check
0 4 1 * * /opt/datasphere/cert_expiry_check.sh
```

### CI/CD Integration for Datasphere

#### GitHub Actions Example

Create `.github/workflows/datasphere-deploy.yml`:

```yaml
name: Deploy Datasphere Configuration

on:
  push:
    branches: [main]
    paths: ['datasphere/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Datasphere CLI
        run: |
          curl -sL https://datasphere-cli.company.com/install.sh | bash
          datasphere --version

      - name: Configure CLI
        env:
          DATASPHERE_CLIENT_ID: ${{ secrets.DATASPHERE_CLIENT_ID }}
          DATASPHERE_CLIENT_SECRET: ${{ secrets.DATASPHERE_CLIENT_SECRET }}
          DATASPHERE_INSTANCE_URL: ${{ secrets.DATASPHERE_INSTANCE_URL }}
        run: datasphere config init --auth-method service-key

      - name: Validate Configuration
        run: |
          datasphere spaces create-bulk --file datasphere/spaces.json --validate --dry-run
          datasphere users create-bulk --file datasphere/users.json --validate --dry-run
          datasphere connections create-bulk --file datasphere/connections.json --validate --dry-run

      - name: Deploy Changes
        run: |
          datasphere spaces create-bulk --file datasphere/spaces.json --confirm
          datasphere users create-bulk --file datasphere/users.json --send-invitations true --confirm
          datasphere connections create-bulk --file datasphere/connections.json --confirm

      - name: Run Post-Deployment Tests
        run: |
          datasphere connections test-batch --file datasphere/connections.json --generate-report deployment_test.html

      - name: Archive Reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: deployment-reports
          path: deployment_test.html
```

#### Azure DevOps Pipeline Example

Create `datasphere-pipeline.yml`:

```yaml
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - datasphere/*

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Validate
  jobs:
  - job: ValidateConfiguration
    steps:
    - task: Bash@3
      inputs:
        targetType: 'inline'
        script: |
          curl -sL https://datasphere-cli.company.com/install.sh | bash
          export DATASPHERE_CLIENT_ID=$(DATASPHERE_CLIENT_ID)
          export DATASPHERE_CLIENT_SECRET=$(DATASPHERE_CLIENT_SECRET)
          export DATASPHERE_INSTANCE_URL=$(DATASPHERE_INSTANCE_URL)
          datasphere config init --auth-method service-key
          datasphere spaces create-bulk --file datasphere/spaces.json --validate --dry-run
          datasphere users create-bulk --file datasphere/users.json --validate --dry-run

- stage: Deploy
  condition: succeeded()
  jobs:
  - deployment: DeployDatasphere
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: Bash@3
            inputs:
              targetType: 'inline'
              script: |
                datasphere spaces create-bulk --file datasphere/spaces.json --confirm
                datasphere users create-bulk --file datasphere/users.json --send-invitations true --confirm
                datasphere connections create-bulk --file datasphere/connections.json --confirm
```

### Infrastructure-as-Code Patterns

Version all Datasphere configuration in Git:

```
datasphere-config/
├── spaces/
│   ├── sales.json
│   ├── finance.json
│   └── marketing.json
├── users/
│   ├── bulk_onboarding.json
│   └── role_assignments.json
├── connections/
│   ├── sap_systems.json
│   └── data_warehouses.json
├── certificates/
│   └── certificates.json
└── deploy.sh
```

`deploy.sh` orchestrates all deployments:

```bash
#!/bin/bash
set -e

echo "Deploying Datasphere Configuration..."

# Validate all configurations
echo "Validating spaces..."
datasphere spaces create-bulk --file spaces/*.json --validate --dry-run

echo "Validating users..."
datasphere users create-bulk --file users/*.json --validate --dry-run

echo "Validating connections..."
datasphere connections create-bulk --file connections/*.json --validate --dry-run

# Deploy
echo "Deploying spaces..."
datasphere spaces create-bulk --file spaces/*.json --confirm

echo "Deploying users..."
datasphere users create-bulk --file users/*.json --send-invitations true --confirm

echo "Deploying connections..."
datasphere connections create-bulk --file connections/*.json --confirm

echo "Deployment complete!"
```

## Error Handling and Logging in CLI Operations

### Enable Verbose Logging

```bash
datasphere --log-level debug spaces create-bulk --file spaces.json
# Output includes detailed request/response logs
```

### Capture Structured Output

```bash
datasphere spaces create-bulk --file spaces.json --output json > deployment_log.json
# Parse with jq for post-processing
jq '.results[] | select(.status == "FAILED")' deployment_log.json
```

### Common CLI Error Codes

| Code | Error | Resolution |
|------|-------|-----------|
| 401 | Authentication failed | Verify service key credentials and expiry |
| 403 | Permission denied | Check role assignments and space membership |
| 409 | Conflict (object exists) | Use `--force-overwrite` or change name |
| 422 | Invalid configuration | Validate JSON schema and retry |
| 503 | Service unavailable | Retry with exponential backoff |

### Retry Logic in Scripts

```bash
#!/bin/bash
retry_with_backoff() {
  local max_attempts=5
  local attempt=1
  local delay=2

  while [ $attempt -le $max_attempts ]; do
    if "$@"; then
      return 0
    fi

    if [ $attempt -lt $max_attempts ]; then
      echo "Attempt $attempt failed. Retrying in ${delay}s..."
      sleep $delay
      delay=$((delay * 2))
    fi

    attempt=$((attempt + 1))
  done

  return 1
}

retry_with_backoff datasphere spaces create-bulk --file spaces.json --confirm
```

---

## MCP Tools Reference

This skill leverages these MCP (Model Context Protocol) tools for enhanced automation:

- **`list_spaces`** — List all spaces with metadata
- **`get_space_info`** — Retrieve detailed space configuration
- **`list_database_users`** — Query user records from Datasphere database
- **`create_database_user`** — Create users programmatically (advanced)
- **`test_connection`** — Validate connection before deployment

Use these tools in conjunction with CLI commands for end-to-end automation workflows.

---

## Next Steps

1. **Set up service key authentication** for your Datasphere instance
2. **Create JSON templates** for your spaces, users, and connections
3. **Validate configurations** with `--dry-run` before committing
4. **Integrate with your CI/CD pipeline** (GitHub Actions or Azure DevOps)
5. **Monitor and alert** on certificate expiry and user provisioning

See the **references/cli-reference.md** for complete command syntax, JSON schemas, and troubleshooting guides.

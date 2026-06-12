# SAP Datasphere CLI Complete Reference

## Table of Contents
1. [Configuration Commands](#configuration-commands)
2. [Space Management Commands](#space-management-commands)
3. [User Management Commands](#user-management-commands)
4. [Connection Management Commands](#connection-management-commands)
5. [Certificate Management Commands](#certificate-management-commands)
6. [JSON Schema Reference](#json-schema-reference)
7. [Bulk Operation Templates](#bulk-operation-templates)
8. [CI/CD Pipeline Examples](#cicd-pipeline-examples)
9. [Certificate Rotation Runbook](#certificate-rotation-runbook)
10. [Error Codes and Troubleshooting](#error-codes-and-troubleshooting)

---

## Configuration Commands

### Initialize Configuration

```bash
datasphere config init \
  --client-id <CLIENT_ID> \
  --client-secret <CLIENT_SECRET> \
  --instance-url <INSTANCE_URL> \
  --auth-method [service-key|oauth|basic]
```

**Options**:
- `--client-id` — Service key client ID
- `--client-secret` — Service key secret
- `--instance-url` — Datasphere instance URL (e.g., https://ds.company.com)
- `--auth-method` — Authentication method (service-key recommended for automation)

**Example**:
```bash
datasphere config init \
  --client-id "sb-cli-user-001" \
  --client-secret "xXkJbK9...L2mN" \
  --instance-url "https://datasphere.acme.com" \
  --auth-method service-key
```

### Validate Configuration

```bash
datasphere config validate [--verbose]
```

**Output**:
```
Configuration valid.
Connected to: https://datasphere.acme.com
Authenticated as: sb-cli-user-001
Timeout: 30s
```

### List Configuration

```bash
datasphere config list
```

### Set Configuration Options

```bash
datasphere config set \
  --key <KEY> \
  --value <VALUE>
```

**Common Keys**:
- `timeout` — Request timeout in seconds (default: 30)
- `retry-attempts` — Max retry attempts (default: 3)
- `log-level` — Log level (debug|info|warn|error)
- `output-format` — Default output format (json|table|csv)

---

## Space Management Commands

### Create Space

```bash
datasphere spaces create \
  --name <SPACE_NAME> \
  [--description <DESC>] \
  [--ram-allocation <GB>] \
  [--disk-allocation <GB>] \
  [--priority <PRIORITY>] \
  [--reserved-memory <GB>] \
  [--owner <EMAIL>] \
  [--tags <TAG1,TAG2,...>] \
  [--public-access true|false]
```

**Parameters**:
- `--name` — Space name (alphanumeric, max 128 chars)
- `--description` — Space description (optional)
- `--ram-allocation` — RAM in GB (min: 50, recommended: 100+)
- `--disk-allocation` — Disk in GB (min: 100, recommended: 5x data volume)
- `--priority` — `low` | `standard` | `high`
- `--reserved-memory` — Reserved RAM in GB (must be <= ram-allocation)
- `--owner` — Space owner email
- `--tags` — Comma-separated tags for organization
- `--public-access` — Enable/disable public access (true|false)

**Example**:
```bash
datasphere spaces create \
  --name "SALES_ANALYTICS" \
  --description "Sales and Revenue Analytics" \
  --ram-allocation 100 \
  --disk-allocation 500 \
  --priority standard \
  --owner "sales-admin@acme.com" \
  --tags "production,analytics"
```

### Bulk Create Spaces

```bash
datasphere spaces create-bulk \
  --file <PATH_TO_JSON> \
  [--validate] \
  [--dry-run] \
  [--confirm]
```

**Flags**:
- `--validate` — Validate JSON schema without creating
- `--dry-run` — Show what would be created
- `--confirm` — Confirm and create spaces

**Example**:
```bash
datasphere spaces create-bulk \
  --file spaces.json \
  --validate \
  --dry-run
```

### List Spaces

```bash
datasphere spaces list \
  [--filter <FILTER>] \
  [--sort-by <FIELD>] \
  [--output <FORMAT>]
```

**Output Formats**: json, table, csv

**Example**:
```bash
datasphere spaces list --output json | jq '.spaces[] | select(.status == "ACTIVE")'
```

### Get Space Details

```bash
datasphere spaces get <SPACE_NAME> \
  [--include-members] \
  [--include-objects]
```

**Example**:
```bash
datasphere spaces get SALES_ANALYTICS --include-members
```

### Clone Space

```bash
datasphere spaces clone \
  --source <SOURCE_SPACE> \
  --target <TARGET_SPACE> \
  [--copy-connections true|false] \
  [--copy-users true|false] \
  [--copy-objects true|false]
```

**Example**:
```bash
datasphere spaces clone \
  --source "PROD_TEMPLATE" \
  --target "DEV_ENVIRONMENT" \
  --copy-connections true \
  --copy-users false
```

### Update Space

```bash
datasphere spaces update <SPACE_NAME> \
  [--new-ram-allocation <GB>] \
  [--new-disk-allocation <GB>] \
  [--new-description <DESC>] \
  [--new-priority <PRIORITY>] \
  [--new-owner <EMAIL>] \
  [--new-tags <TAG1,TAG2,...>]
```

**Example**:
```bash
datasphere spaces update SALES_ANALYTICS \
  --new-ram-allocation 150 \
  --new-disk-allocation 750 \
  --new-priority high
```

### Delete Space

```bash
datasphere spaces delete <SPACE_NAME> \
  [--backup-path <PATH>] \
  [--force]
```

**Example**:
```bash
datasphere spaces delete TEMP_SPACE \
  --backup-path /backups/temp_space_backup.json \
  --force
```

### Space Quota Report

```bash
datasphere spaces report \
  [--metric <METRIC>] \
  [--format <FORMAT>] \
  [--output-file <PATH>]
```

**Metrics**: cpu|memory|disk|concurrent-users

**Example**:
```bash
datasphere spaces report --metric memory --format json > space_usage.json
```

---

## User Management Commands

### Create User

```bash
datasphere users create \
  --email <EMAIL> \
  --first-name <FIRST> \
  --last-name <LAST> \
  [--roles <ROLE1,ROLE2,...>] \
  [--spaces <SPACE1:ROLE1,SPACE2:ROLE2,...>] \
  [--attributes <KEY1:VALUE1,KEY2:VALUE2,...>] \
  [--send-invitation true|false]
```

**Parameters**:
- `--email` — User email address (unique)
- `--first-name` — First name
- `--last-name` — Last name
- `--roles` — Comma-separated global roles
- `--spaces` — Space assignments with roles (format: SPACE_NAME:ROLE)
- `--attributes` — Custom attributes for organization
- `--send-invitation` — Send invitation email

**Available Roles**:
- `datasphere.admin` — Full system administration
- `datasphere.analyst` — Analytics and modeling
- `datasphere.viewer` — Read-only access

**Example**:
```bash
datasphere users create \
  --email "alice.johnson@acme.com" \
  --first-name "Alice" \
  --last-name "Johnson" \
  --roles "datasphere.analyst" \
  --spaces "SALES_ANALYTICS:editor,FINANCE_REPORTING:viewer" \
  --attributes "department:Sales,cost_center:CC-1001" \
  --send-invitation true
```

### Bulk Create Users

```bash
datasphere users create-bulk \
  --file <PATH_TO_JSON> \
  [--validate] \
  [--dry-run] \
  [--send-invitations true|false] \
  [--confirm]
```

**Example**:
```bash
datasphere users create-bulk \
  --file users.json \
  --validate \
  --dry-run
```

### List Users

```bash
datasphere users list \
  [--filter <FILTER>] \
  [--inactive-days <DAYS>] \
  [--sort-by <FIELD>] \
  [--output <FORMAT>]
```

**Filters**: active|inactive|disabled|pending

**Example**:
```bash
datasphere users list --inactive-days 90 --output csv > inactive_users.csv
```

### Get User Details

```bash
datasphere users get <EMAIL> \
  [--include-roles] \
  [--include-space-assignments]
```

### Assign Role

```bash
datasphere users assign-role \
  --email <EMAIL> \
  --role <ROLE> \
  [--space <SPACE_NAME>] \
  [--effective-date <ISO_DATE>]
```

**Example**:
```bash
datasphere users assign-role \
  --email "alice.johnson@acme.com" \
  --role "datasphere.space_admin" \
  --space "SALES_ANALYTICS"
```

### Remove Role

```bash
datasphere users remove-role \
  --email <EMAIL> \
  --role <ROLE> \
  [--space <SPACE_NAME>]
```

### Set User Attributes

```bash
datasphere users set-attribute \
  --email <EMAIL> \
  --attribute <KEY> \
  --value <VALUE> \
  [--attribute <KEY2> --value <VALUE2>]
```

**Example**:
```bash
datasphere users set-attribute \
  --email "alice.johnson@acme.com" \
  --attribute "department" \
  --value "Sales" \
  --attribute "cost_center" \
  --value "CC-1001"
```

### Batch Update User Attributes

```bash
datasphere users batch-attributes \
  --file <PATH_TO_JSON>
```

**File Format**:
```json
{
  "updates": [
    {
      "email": "alice.johnson@acme.com",
      "attributes": {
        "department": "Sales",
        "manager": "bob.smith@acme.com"
      }
    }
  ]
}
```

### Disable User

```bash
datasphere users disable \
  --email <EMAIL> \
  [--reason <REASON>] \
  [--effective-date <ISO_DATE>]
```

**Example**:
```bash
datasphere users disable \
  --email "alice.johnson@acme.com" \
  --reason "Employee departure" \
  --effective-date "2024-03-15"
```

### Delete User

```bash
datasphere users delete \
  --email <EMAIL> \
  [--transfer-owned-objects-to <EMAIL>] \
  [--force]
```

**Important**: Deletes user and reassigns owned objects.

**Example**:
```bash
datasphere users delete \
  --email "alice.johnson@acme.com" \
  --transfer-owned-objects-to "bob.smith@acme.com" \
  --force
```

---

## Connection Management Commands

### Create Connection

```bash
datasphere connections create \
  --name <NAME> \
  --type <TYPE> \
  [--description <DESC>] \
  [--connection-file <PATH_TO_JSON>]
```

**Connection Types**: sap_s4hana, sap_bw, snowflake, postgresql, oracle, mysql, kafka, etc.

**Example**:
```bash
datasphere connections create \
  --name "PROD_SAP_S4" \
  --type "sap_s4hana" \
  --connection-file s4h_connection.json
```

### Bulk Create Connections

```bash
datasphere connections create-bulk \
  --file <PATH_TO_JSON> \
  [--validate-credentials] \
  [--dry-run] \
  [--confirm]
```

**Example**:
```bash
datasphere connections create-bulk \
  --file connections.json \
  --validate-credentials \
  --dry-run
```

### List Connections

```bash
datasphere connections list \
  [--filter <FILTER>] \
  [--type <TYPE>] \
  [--output <FORMAT>]
```

**Filters**: active|inactive|test-failed|expiring

### Get Connection Details

```bash
datasphere connections get <CONNECTION_NAME> \
  [--include-test-results]
```

### Test Connection

```bash
datasphere connections test \
  --name <CONNECTION_NAME> \
  [--verbose] \
  [--test-query <SQL>]
```

**Example**:
```bash
datasphere connections test \
  --name "PROD_SAP_S4" \
  --verbose
```

### Batch Test Connections

```bash
datasphere connections test-batch \
  --file <PATH_TO_JSON> \
  [--generate-report <PATH>] \
  [--timeout <SECONDS>]
```

### Update Connection

```bash
datasphere connections update \
  --name <CONNECTION_NAME> \
  --connection-file <PATH_TO_JSON>
```

### Delete Connection

```bash
datasphere connections delete \
  --name <CONNECTION_NAME> \
  [--force]
```

---

## Certificate Management Commands

### List Certificates

```bash
datasphere configuration certificates list \
  [--show-expiry] \
  [--sort-by <FIELD>] \
  [--output <FORMAT>]
```

**Fields for Sort**: name|created|expiry|status

**Example**:
```bash
datasphere configuration certificates list \
  --show-expiry \
  --sort-by expiry \
  --output table
```

### Upload Certificate

```bash
datasphere configuration certificates upload \
  --name <NAME> \
  --certificate-file <PATH> \
  --key-file <PATH> \
  [--description <DESC>] \
  [--scheduled-activation <ISO_DATETIME>]
```

**File Format**: PEM (Privacy Enhanced Mail)

**Example**:
```bash
datasphere configuration certificates upload \
  --name "PROD_SAP_S4_CERT" \
  --certificate-file "/secure/cert.pem" \
  --key-file "/secure/key.pem" \
  --description "Production SAP S/4HANA Certificate" \
  --scheduled-activation "2024-03-01T00:00:00Z"
```

### Activate Certificate

```bash
datasphere configuration certificates activate \
  --name <NAME>
```

### Deactivate Certificate

```bash
datasphere configuration certificates deactivate \
  --name <NAME>
```

### Delete Certificate

```bash
datasphere configuration certificates delete \
  --name <NAME> \
  [--force]
```

### Get Certificate Details

```bash
datasphere configuration certificates get <NAME>
```

---

## JSON Schema Reference

### Space Definition Schema

```json
{
  "spaces": [
    {
      "name": "string (required, alphanumeric max 128)",
      "description": "string (optional)",
      "configuration": {
        "memory": {
          "allocated_gb": "integer (min: 50, max: 10000)",
          "reserved_gb": "integer (optional, <= allocated_gb)"
        },
        "disk": {
          "allocated_gb": "integer (min: 100, max: 100000)"
        },
        "priority": "string (low|standard|high)",
        "network": {
          "enable_public_access": "boolean",
          "data_isolation_level": "string (tenant|shared|isolated)"
        }
      },
      "owner": "string (email, required)",
      "tags": "array of strings (optional)",
      "labels": {
        "custom_key": "custom_value"
      }
    }
  ]
}
```

### User Provisioning Schema

```json
{
  "users": [
    {
      "email": "string (required, unique)",
      "first_name": "string (required)",
      "last_name": "string (required)",
      "roles": [
        {
          "role": "string (datasphere.admin|datasphere.analyst|datasphere.viewer)",
          "scope": "string (global|space)",
          "effective_date": "string (ISO 8601, optional)"
        }
      ],
      "space_assignments": [
        {
          "space_name": "string (required)",
          "role": "string (space_admin|editor|viewer)",
          "effective_date": "string (ISO 8601, optional)"
        }
      ],
      "attributes": {
        "department": "string (optional)",
        "cost_center": "string (optional)",
        "manager": "string (email, optional)",
        "custom_field": "string (optional)"
      },
      "status": "string (active|inactive|pending)"
    }
  ]
}
```

### Connection Definition Schema

```json
{
  "connections": [
    {
      "name": "string (required)",
      "type": "string (required: sap_s4hana|snowflake|postgresql|etc)",
      "description": "string (optional)",
      "technical_user": "string (optional)",
      "connection_details": {
        "host": "string",
        "port": "integer",
        "client": "string (for SAP systems)",
        "use_ssl": "boolean",
        "tls_version": "string (1.2|1.3)",
        "timeout_seconds": "integer (default: 30)"
      },
      "authentication": {
        "method": "string (basic|oauth|certificate|kerberos)",
        "username": "string (or use variable)",
        "username_variable": "string (env var name)",
        "password_variable": "string (env var name)",
        "client_id_variable": "string (for OAuth)",
        "client_secret_variable": "string (for OAuth)",
        "token_endpoint": "string (for OAuth)"
      },
      "test_table": "string (optional, for validation)",
      "test_query": "string (optional, for validation)",
      "retry_policy": {
        "max_attempts": "integer (default: 3)",
        "backoff_seconds": "integer (default: 5)",
        "backoff_multiplier": "float (default: 2.0)"
      },
      "owner": "string (email)",
      "tags": "array of strings (optional)"
    }
  ]
}
```

---

## Bulk Operation Templates

### Template 1: 50-User Onboarding

```json
{
  "users": [
    {
      "email": "user001@acme.com",
      "first_name": "John",
      "last_name": "Doe",
      "roles": [{"role": "datasphere.analyst", "scope": "global"}],
      "space_assignments": [
        {"space_name": "SALES_ANALYTICS", "role": "editor"},
        {"space_name": "FINANCE_REPORTING", "role": "viewer"}
      ],
      "attributes": {
        "department": "Sales",
        "cost_center": "CC-1001",
        "manager": "admin@acme.com"
      },
      "status": "active"
    },
    {
      "email": "user002@acme.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "roles": [{"role": "datasphere.analyst", "scope": "global"}],
      "space_assignments": [
        {"space_name": "FINANCE_REPORTING", "role": "editor"}
      ],
      "attributes": {
        "department": "Finance",
        "cost_center": "CC-2001",
        "manager": "admin@acme.com"
      },
      "status": "active"
    }
  ]
}
```

### Template 2: 5-Space Environment Setup

```json
{
  "spaces": [
    {
      "name": "INBOUND_LAYER",
      "description": "Raw data ingestion from source systems",
      "configuration": {
        "memory": {"allocated_gb": 80, "reserved_gb": 40},
        "disk": {"allocated_gb": 2000},
        "priority": "standard"
      },
      "owner": "data-admin@acme.com",
      "tags": ["lsa_plus", "inbound"]
    },
    {
      "name": "HARMONIZATION_LAYER",
      "description": "Data cleansing and standardization",
      "configuration": {
        "memory": {"allocated_gb": 100, "reserved_gb": 50},
        "disk": {"allocated_gb": 2500},
        "priority": "standard"
      },
      "owner": "data-admin@acme.com",
      "tags": ["lsa_plus", "harmonization"]
    },
    {
      "name": "REPORTING_LAYER",
      "description": "Analytics and reporting views",
      "configuration": {
        "memory": {"allocated_gb": 150, "reserved_gb": 75},
        "disk": {"allocated_gb": 3000},
        "priority": "high"
      },
      "owner": "analytics-admin@acme.com",
      "tags": ["lsa_plus", "reporting"]
    }
  ]
}
```

### Template 3: Multi-System Connection Setup

```json
{
  "connections": [
    {
      "name": "SAP_S4H_PROD",
      "type": "sap_s4hana",
      "description": "Production SAP S/4HANA",
      "connection_details": {
        "host": "s4h-prod.acme.com",
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
      "owner": "integration-admin@acme.com"
    },
    {
      "name": "SAP_BW_PROD",
      "type": "sap_bw",
      "description": "Production SAP BW",
      "connection_details": {
        "host": "bw-prod.acme.com",
        "port": 50013,
        "client": "100",
        "use_ssl": true
      },
      "authentication": {
        "method": "basic",
        "username_variable": "BW_USER",
        "password_variable": "BW_PASS"
      },
      "owner": "integration-admin@acme.com"
    },
    {
      "name": "SNOWFLAKE_PROD",
      "type": "snowflake",
      "description": "Production Snowflake Warehouse",
      "connection_details": {
        "account_identifier": "xy12345.us-east-1",
        "warehouse": "COMPUTE_WH",
        "database": "PROD_DB",
        "schema": "STAGING"
      },
      "authentication": {
        "method": "oauth",
        "client_id_variable": "SF_CLIENT_ID",
        "client_secret_variable": "SF_CLIENT_SECRET"
      },
      "test_query": "SELECT 1",
      "owner": "data-team@acme.com"
    }
  ]
}
```

---

## CI/CD Pipeline Examples

### GitHub Actions: Full Datasphere Deployment

```yaml
name: Deploy Datasphere Config

on:
  push:
    branches: [main]
    paths: ['datasphere/**']
  pull_request:
    branches: [main]
    paths: ['datasphere/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Datasphere CLI
        run: |
          curl -sL https://releases.datasphere.company.com/cli/install.sh | bash
          datasphere --version

      - name: Configure CLI
        env:
          DATASPHERE_CLIENT_ID: ${{ secrets.DATASPHERE_CLIENT_ID }}
          DATASPHERE_CLIENT_SECRET: ${{ secrets.DATASPHERE_CLIENT_SECRET }}
          DATASPHERE_INSTANCE_URL: ${{ secrets.DATASPHERE_INSTANCE_URL }}
        run: datasphere config init --auth-method service-key

      - name: Validate Spaces Configuration
        run: datasphere spaces create-bulk --file datasphere/spaces.json --validate --dry-run

      - name: Validate Users Configuration
        run: datasphere users create-bulk --file datasphere/users.json --validate --dry-run

      - name: Validate Connections Configuration
        run: datasphere connections create-bulk --file datasphere/connections.json --validate --dry-run

      - name: Test Connections (Dry Run)
        run: datasphere connections test-batch --file datasphere/connections.json --timeout 60

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Install Datasphere CLI
        run: |
          curl -sL https://releases.datasphere.company.com/cli/install.sh | bash

      - name: Configure CLI
        env:
          DATASPHERE_CLIENT_ID: ${{ secrets.DATASPHERE_CLIENT_ID }}
          DATASPHERE_CLIENT_SECRET: ${{ secrets.DATASPHERE_CLIENT_SECRET }}
          DATASPHERE_INSTANCE_URL: ${{ secrets.DATASPHERE_INSTANCE_URL }}
        run: datasphere config init --auth-method service-key

      - name: Deploy Spaces
        run: datasphere spaces create-bulk --file datasphere/spaces.json --confirm

      - name: Deploy Connections
        run: datasphere connections create-bulk --file datasphere/connections.json --confirm

      - name: Deploy Users
        run: datasphere users create-bulk --file datasphere/users.json --send-invitations true --confirm

      - name: Post-Deployment Tests
        run: |
          datasphere connections test-batch --file datasphere/connections.json \
            --generate-report deployment_report.html

      - name: Upload Deployment Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: deployment-report
          path: deployment_report.html
          retention-days: 30

      - name: Slack Notification
        if: always()
        uses: slackapi/slack-github-action@v1.24.0
        with:
          payload: |
            {
              "text": "Datasphere Deployment: ${{ job.status }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Datasphere Config Deployment*\nStatus: ${{ job.status }}\nCommit: <${{ github.server_url }}/${{ github.repository }}/commit/${{ github.sha }}|${{ github.sha }}>"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Certificate Rotation Runbook

### Pre-Rotation Checklist

- [ ] Obtain new TLS certificate and private key (PEM format)
- [ ] Verify certificate validity dates and CN/SANs
- [ ] Confirm backup of current certificate
- [ ] Schedule maintenance window (off-peak)
- [ ] Notify stakeholders of potential brief service interruption

### Rotation Steps

**1. Validate New Certificate**

```bash
# Check certificate details
openssl x509 -in /path/to/new_cert.pem -text -noout

# Verify certificate chain
openssl verify -CAfile /path/to/ca_bundle.pem /path/to/new_cert.pem

# Verify key matches certificate
openssl x509 -noout -modulus -in /path/to/new_cert.pem | openssl md5
openssl rsa -noout -modulus -in /path/to/key.pem | openssl md5
# Both commands should return same MD5 hash
```

**2. Backup Current Certificate**

```bash
datasphere configuration certificates list --show-expiry > cert_backup_$(date +%Y%m%d).json
```

**3. Upload New Certificate**

```bash
datasphere configuration certificates upload \
  --name "PROD_SAP_S4_CERT_NEW" \
  --certificate-file "/secure/new_cert.pem" \
  --key-file "/secure/new_key.pem" \
  --description "New Production SAP S/4HANA Certificate (Rotation on 2024-03-01)" \
  --scheduled-activation "2024-03-01T02:00:00Z"
```

**4. Verify Upload**

```bash
datasphere configuration certificates get PROD_SAP_S4_CERT_NEW
# Verify: Status = PENDING_ACTIVATION, Expiry date correct
```

**5. During Maintenance Window - Activate New Certificate**

```bash
datasphere configuration certificates activate --name "PROD_SAP_S4_CERT_NEW"
```

**6. Verify Connections After Rotation**

```bash
datasphere connections test-batch --file connections.json --timeout 60 --generate-report rotation_test.html
```

**7. Deactivate Old Certificate (after 24-hour observation)**

```bash
datasphere configuration certificates deactivate --name "PROD_SAP_S4_CERT"
```

**8. Archive Old Certificate (after 30-day retention period)**

```bash
datasphere configuration certificates delete \
  --name "PROD_SAP_S4_CERT" \
  --force
```

### Rollback Procedure (If Issues Occur)

```bash
# 1. Revert to old certificate
datasphere configuration certificates activate --name "PROD_SAP_S4_CERT"

# 2. Deactivate new certificate
datasphere configuration certificates deactivate --name "PROD_SAP_S4_CERT_NEW"

# 3. Verify connections
datasphere connections test-batch --file connections.json

# 4. Notify stakeholders
```

---

## Error Codes and Troubleshooting

### Authentication Errors

| Code | Error | Cause | Resolution |
|------|-------|-------|-----------|
| 401 | Unauthorized | Invalid credentials or expired token | Refresh service key, verify client ID/secret |
| 403 | Forbidden | Insufficient permissions | Check service key roles and scopes |
| 405 | Method Not Allowed | Wrong HTTP method (CLI bug) | Update CLI to latest version |

### Space Management Errors

| Code | Error | Cause | Resolution |
|------|-------|-------|-----------|
| 409 | Space already exists | Name conflict | Use different space name or `--force-overwrite` |
| 422 | Invalid space name | Name contains invalid characters | Use alphanumeric + underscore only |
| 507 | Insufficient space quota | Organization limit exceeded | Contact SAP support for quota increase |
| 400 | Invalid memory allocation | Below minimum (50 GB) | Increase memory allocation |

### User Management Errors

| Code | Error | Cause | Resolution |
|------|-------|-------|-----------|
| 409 | User already exists | Email already in system | Check existing users or use different email |
| 422 | Invalid email format | Email not properly formatted | Verify email syntax |
| 400 | Invalid role | Role doesn't exist | Check available roles: datasphere.admin|analyst|viewer |
| 404 | Space not found | Space doesn't exist | Verify space name and create space first |

### Connection Errors

| Code | Error | Cause | Resolution |
|------|-------|-------|-----------|
| 400 | Invalid connection type | Unsupported system type | Check supported types: sap_s4hana, snowflake, etc |
| 422 | Invalid connection details | Missing required fields | Verify all required fields in JSON |
| 503 | Connection test failed | Target system unreachable | Verify host, port, network connectivity |
| 401 | Authentication failed | Invalid credentials | Verify username/password or OAuth token |
| 408 | Timeout | Response too slow | Increase timeout or check target system performance |

### Certificate Errors

| Code | Error | Cause | Resolution |
|------|-------|-------|-----------|
| 400 | Invalid certificate | Certificate format or content issue | Verify PEM format, expiry date, key validity |
| 409 | Certificate already exists | Name conflicts | Use unique certificate name |
| 422 | Certificate expired | Certificate no longer valid | Provide valid, non-expired certificate |
| 410 | Cannot deactivate active cert | Cert in use by connections | Activate replacement cert first |

### Common Troubleshooting Steps

**1. Enable Debug Logging**

```bash
datasphere --log-level debug [COMMAND]
# Output shows detailed request/response for debugging
```

**2. Validate Configuration JSON**

```bash
# Use jq to validate JSON syntax
jq . spaces.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Validate against schema
datasphere [spaces|users|connections] create-bulk --file [FILE] --validate
```

**3. Check CLI Version**

```bash
datasphere --version
# Update if outdated
curl -sL https://releases.datasphere.company.com/cli/install.sh | bash
```

**4. Verify Connectivity**

```bash
# Test Datasphere instance accessibility
curl -I https://datasphere.acme.com/health
# Should return HTTP 200 OK

# Verify service key authentication
datasphere config validate
```

**5. Review Server Logs**

Request logs from Datasphere instance administrator:
- `/var/log/datasphere/cli-requests.log`
- `/var/log/datasphere/admin.log`
- Include request ID from error output

---

## Additional Resources

- **Official CLI Documentation**: https://help.sap.com/datasphere/cli
- **API Reference**: https://api.datasphere.company.com/docs
- **Support Portal**: https://support.sap.com/datasphere
- **Community**: https://community.sap.com/datasphere

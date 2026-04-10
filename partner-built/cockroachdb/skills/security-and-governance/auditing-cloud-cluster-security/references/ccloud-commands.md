# ccloud CLI Commands for Security Auditing

This reference provides `ccloud` CLI commands used during security posture assessments. All commands are read-only operations.

## Authentication

### Verify Authentication

```bash
# Check current authentication status
ccloud auth whoami
```

### Login (If Not Authenticated)

```bash
# Interactive login (opens browser)
ccloud auth login
```

## Cluster Information

### List All Clusters

```bash
# List clusters in the organization
ccloud cluster list -o json
```

### Get Cluster Info

```bash
# Get detailed cluster info including plan type, regions, version
# Accepts cluster name or ID
ccloud cluster info <cluster-name> -o json
```

**Key fields to inspect:**
- `plan` — Basic, Standard, or Advanced
- `cockroach_version` — CockroachDB version
- `regions` — Deployed regions
- `state` — Cluster state (CREATED, READY, etc.)

## Network Security

### List IP Allowlist Entries

```bash
# List all IP allowlist entries
ccloud cluster networking allowlist list <cluster-id> -o json
```

**Key fields to inspect:**
- `cidr_ip` / `cidr_mask` — The allowed IP range
- `name` — Description of the entry
- `sql` — Whether SQL access is allowed
- `ui` — Whether DB Console access is allowed

**Red flags:**
- `0.0.0.0/0` — Open to all IPv4 addresses
- `/8` or `/16` ranges — Overly broad network access

### List Private Endpoint Connections

Private endpoint connections are managed via the **Cloud Console** or **Cloud API** (not the `ccloud` CLI).

**Cloud Console:** Navigate to your cluster's **Networking > Private endpoint** tab.

**Cloud API:**
```bash
curl "https://cockroachlabs.cloud/api/v1/clusters/<cluster-id>/networking/private-endpoint-connections" \
  -H "Authorization: Bearer <api-key>"
```

## SSO and SCIM

Cloud Console SSO and SCIM 2.0 are configured via the **Cloud Console UI** (Organization Settings > Authentication). The `ccloud` CLI does not currently expose SSO or SCIM configuration commands.

**To check SSO status:**
1. Log into the CockroachDB Cloud Console
2. Navigate to Organization Settings > Authentication
3. Check if SSO (SAML/OIDC) is enabled and whether it is enforced

**To check SCIM status:**
1. Log into the CockroachDB Cloud Console
2. Navigate to Organization Settings > Authentication > SCIM
3. Check if the SCIM endpoint is enabled and connected to an IdP

**Database SSO (Cluster SSO)** is checked via SQL — see the SQL queries reference.

## Encryption (CMEK)

### Check CMEK Status

```bash
# CMEK configuration is part of cluster info output
ccloud cluster info <cluster-name> -o json
# Look for cmek_config section
```

**Key fields to inspect:**
- `cmek_config.status` — CMEK status (enabled/disabled)
- `cmek_config.key_spec` — KMS key details

**Note:** CMEK requires Advanced plan with Advanced Security Add-on.

## Backup Configuration

### Check Managed Backup Status

```bash
# Backup configuration is part of cluster info output
ccloud cluster info <cluster-name> -o json
# Look for backup_config section
```

**Key fields to inspect:**
- `backup_config.frequency` — Backup frequency
- `backup_config.retention` — Backup retention period

**Note:** CockroachDB Cloud automatically manages backups for all clusters. This is informational only.

## SQL User Management

### List SQL Users

```bash
# List SQL users for a cluster
ccloud cluster user list <cluster-name>
```

### Create SQL User

```bash
# Create a SQL user with password
ccloud cluster user create <cluster-name> <username> -p '<password>'
```

### Connect via SQL

```bash
# Open interactive SQL shell
ccloud cluster sql <cluster-name> -u <username> -p '<password>'

# Get connection URL (for use with cockroach sql)
ccloud cluster sql <cluster-name> -u <username> -p '<password>' --connection-url
```

## Output Formatting

All commands support `-o json` for machine-readable output:

```bash
# JSON output (recommended for automation)
ccloud cluster list -o json

# Table output (default, human-readable)
ccloud cluster list
```

## Notes

- All audit commands are read-only (`list`, `info`, `whoami`)
- No commands modify cluster state, network configuration, or user access
- JSON output (`-o json`) is recommended for structured parsing during audits
- SSO and SCIM configuration must be checked via the Cloud Console UI
- Cluster networking commands accept cluster ID; other commands accept cluster name or ID

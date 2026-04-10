---
name: configuring-ip-allowlists
description: Configures and hardens IP allowlists for CockroachDB Cloud clusters to restrict network access to authorized CIDR ranges. Use when tightening network security, removing overly permissive allowlist entries like 0.0.0.0/0, or setting up allowlists for a new cluster.
compatibility: Requires ccloud CLI with Cluster Admin or Cluster Operator role.
metadata:
  author: cockroachdb
  version: "1.0"
---

# Configuring IP Allowlists

Configures and hardens IP allowlists on CockroachDB Cloud clusters to restrict SQL and DB Console access to authorized CIDR ranges. Identifies overly permissive entries (such as `0.0.0.0/0`) and replaces them with specific, narrow ranges.

## When to Use This Skill

- Removing `0.0.0.0/0` (open to all) from the IP allowlist
- Restricting network access after initial cluster setup
- Adding office, VPN, or CI/CD CIDR ranges to the allowlist
- Reviewing and tightening existing allowlist entries
- Responding to a security audit finding about overly broad network access

## Prerequisites

- **ccloud CLI** installed and authenticated (`ccloud auth login`)
- **Cloud Console role:** Cluster Admin or Cluster Operator
- **Known CIDR ranges:** Office IPs, VPN egress IPs, CI/CD runner IPs, or other authorized sources
- **Cluster ID:** Available from `ccloud cluster list`

**Verify access:**
```bash
ccloud auth whoami
ccloud cluster list
```

## Steps

### 1. List Current Allowlist Entries

```bash
# List all IP allowlist entries for the cluster
ccloud cluster networking allowlist list <cluster-id> -o json
```

Review each entry. Flag any of these as overly permissive:
- `0.0.0.0/0` — Open to all IPv4 addresses
- `/8` ranges — 16 million+ addresses
- `/16` ranges — 65,000+ addresses
- Unknown or undocumented entries

See [ccloud commands reference](references/ccloud-commands.md) for full command syntax.

### 2. Understand Allowlist Limits

CockroachDB Cloud clusters have a maximum number of IP allowlist entries per cluster. If you need more entries than the limit allows:

- **Consolidate entries:** Use broader CIDR ranges where security permits (e.g., combine several `/32` entries into a `/24`)
- **Use private endpoints:** Switch to [private endpoints](../configuring-private-connectivity/SKILL.md) instead of allowlists for VPC-based access — private endpoints bypass the allowlist entirely
- **Request a limit increase:** Contact CockroachDB Cloud support if consolidation and private endpoints are not sufficient

### 3. Identify Required CIDR Ranges

Before modifying the allowlist, document all legitimate access sources:

| Source | CIDR | SQL Access | UI Access |
|--------|------|------------|-----------|
| Office network | `203.0.113.0/24` | Yes | Yes |
| VPN egress | `198.51.100.0/24` | Yes | Yes |
| CI/CD runners | `192.0.2.0/28` | Yes | No |
| Monitoring | `10.0.1.5/32` | Yes | No |

### 4. Add Specific CIDR Entries

```bash
# Add a specific CIDR range (CIDR is a positional argument)
ccloud cluster networking allowlist create <cluster-name> <cidr> \
  --sql \
  --ui \
  --name "<description>"
```

**Examples:**
```bash
# Office network — SQL and UI access
ccloud cluster networking allowlist create <cluster-name> 203.0.113.0/24 \
  --sql \
  --ui \
  --name "Office network"

# CI/CD runners — SQL only
ccloud cluster networking allowlist create <cluster-name> 192.0.2.0/28 \
  --sql \
  --name "CI/CD runners"

# Single IP — /32 for maximum specificity
ccloud cluster networking allowlist create <cluster-name> 198.51.100.42/32 \
  --sql \
  --ui \
  --name "Developer workstation"
```

### 5. Remove Overly Permissive Entries

```bash
# Delete the 0.0.0.0/0 entry (or other overly broad entries)
ccloud cluster networking allowlist delete <cluster-name> 0.0.0.0/0
```

**Important:** Only remove `0.0.0.0/0` after confirming your specific CIDR entries are in place and tested.

### 6. Verify the Updated Allowlist

```bash
# Confirm the final allowlist
ccloud cluster networking allowlist list <cluster-id> -o json
```

Test connectivity from each authorized source:
```bash
# Test SQL connection from an allowed IP
cockroach sql --url "<connection-string>" -e "SELECT 1;"

# Test from a non-allowed IP (should fail)
# Attempt connection from an IP not in the allowlist — expect connection refused
```

## Safety Considerations

**Risk: Locking yourself out.** Removing `0.0.0.0/0` before adding your current IP will immediately block your access.

**Mitigation steps:**
1. **Identify your current IP** before making changes: `curl -s https://checkip.amazonaws.com`
2. **Add your IP first** as a `/32` entry before removing broad ranges
3. **Test connectivity** after adding specific entries but before removing `0.0.0.0/0`
4. **Keep Cloud Console access** — the Cloud Console UI can modify allowlists even if SQL access is blocked

**Order of operations:**
1. Add all specific CIDR entries
2. Verify SQL connectivity from each allowed source
3. Remove `0.0.0.0/0` only after verifying all needed entries are in place
4. Test again to confirm access still works

## Rollback

If you lose access after removing a broad entry:

1. **Cloud Console:** Log into the CockroachDB Cloud Console (web UI) — this does not use the IP allowlist
2. **Re-add your IP:** Add your current IP as a `/32` or re-add `0.0.0.0/0` temporarily
3. **Investigate:** Determine which CIDR was missing and add it

```bash
# Emergency: re-add 0.0.0.0/0 via ccloud (if you still have ccloud access)
ccloud cluster networking allowlist create <cluster-name> 0.0.0.0/0 \
  --sql \
  --ui \
  --name "Emergency - temporary open access"
```

## References

**Skill references:**
- [ccloud commands for IP allowlists](references/ccloud-commands.md)

**Related skills:**
- [auditing-cloud-cluster-security](../auditing-cloud-cluster-security/SKILL.md) — Run a full security posture audit
- [configuring-private-connectivity](../configuring-private-connectivity/SKILL.md) — Private endpoints as an alternative to IP allowlists

**Official CockroachDB Documentation:**
- [Network Authorization](https://www.cockroachlabs.com/docs/cockroachcloud/network-authorization.html)
- [Private Clusters](https://www.cockroachlabs.com/docs/cockroachcloud/private-clusters.html)
- [ccloud CLI Reference](https://www.cockroachlabs.com/docs/cockroachcloud/ccloud-get-started.html)

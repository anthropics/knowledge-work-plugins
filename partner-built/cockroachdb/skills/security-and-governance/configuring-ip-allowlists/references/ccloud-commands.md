# ccloud Commands for IP Allowlist Management

This reference provides the full set of `ccloud` CLI commands for managing IP allowlists on CockroachDB Cloud clusters.

## Listing Allowlist Entries

```bash
# List all IP allowlist entries (JSON output)
ccloud cluster networking allowlist list <cluster-name> -o json

# List in table format (human-readable)
ccloud cluster networking allowlist list <cluster-name>
```

**Output fields:**
- `cidr_ip` — IP address portion of the CIDR
- `cidr_mask` — Subnet mask length
- `name` — Description of the entry
- `sql` — Whether SQL connections are allowed
- `ui` — Whether DB Console access is allowed

## Creating Allowlist Entries

```bash
# Add a CIDR range with SQL and UI access
# Note: CIDR is a positional argument, not a flag
ccloud cluster networking allowlist create <cluster-name> <ip>/<mask> \
  --sql \
  --ui \
  --name "<description>"

# Add a CIDR range with SQL access only
ccloud cluster networking allowlist create <cluster-name> <ip>/<mask> \
  --sql \
  --name "<description>"

# Add a CIDR range with UI access only
ccloud cluster networking allowlist create <cluster-name> <ip>/<mask> \
  --ui \
  --name "<description>"
```

**CIDR examples:**
- `203.0.113.42/32` — Single IP address
- `203.0.113.0/24` — 256 addresses (typical office subnet)
- `10.0.0.0/16` — 65,536 addresses (VPN range)
- `0.0.0.0/0` — All IPv4 addresses (not recommended)

## Deleting Allowlist Entries

```bash
# Delete a specific allowlist entry by CIDR
# Note: CIDR is a positional argument, not a flag
ccloud cluster networking allowlist delete <cluster-name> <ip>/<mask>
```

**Warning:** Deleting an entry immediately blocks connections from that CIDR range.

## Common Patterns

### Replace 0.0.0.0/0 with Specific Ranges

```bash
# Step 1: Add specific ranges
ccloud cluster networking allowlist create <cluster-name> 203.0.113.0/24 \
  --sql --ui --name "Office"

ccloud cluster networking allowlist create <cluster-name> 198.51.100.0/24 \
  --sql --ui --name "VPN"

# Step 2: Verify connectivity from allowed ranges
# (test SQL connection from office/VPN)

# Step 3: Remove 0.0.0.0/0
ccloud cluster networking allowlist delete <cluster-name> 0.0.0.0/0

# Step 4: Verify final state
ccloud cluster networking allowlist list <cluster-name> -o json
```

### Add Single Developer IP

```bash
# Find your current IP
curl -s https://checkip.amazonaws.com

# Add as /32 (single IP)
ccloud cluster networking allowlist create <cluster-name> \
  "$(curl -s https://checkip.amazonaws.com)/32" \
  --sql --ui --name "Developer - $(whoami)"
```

## Notes

- Changes take effect immediately — there is no propagation delay
- The Cloud Console web UI is not affected by IP allowlists (always accessible)
- Private endpoint connections bypass IP allowlists entirely
- Duplicate CIDR entries are rejected
- You can use either the cluster name or cluster UUID with these commands

# Fastly NGWAF Security

Configure Next-Gen Web Application Firewall protection.

## Enabling / Disabling NGWAF on a Service

There are two separate concepts:
1. **Workspace mode** (`block`, `log`, `off`) — controls what the WAF does with traffic it inspects.
2. **Service enablement** — whether NGWAF is active on a specific Fastly service at all.

To fully **enable** NGWAF on a service, you need both a workspace AND the product enabled on the service. To fully **disable** NGWAF on a service (stop all inspection), use the product disablement API — just setting the workspace mode to `log` or `off` is not the same as disabling.

**When the user says "enable/disable WAF"**: Ask whether they want to change the workspace blocking mode (`block`/`log`/`off`) or fully enable/disable the NGWAF product on the service. These are different operations with different impact. If the workspace already exists and is linked, changing the mode is usually what they want. If NGWAF has never been set up on the service, full enablement is needed.

### Enable NGWAF on a service

```bash
# 1. Find the service ID
fastly service list --json | jq -r '.[] | select(.Name=="my-service") | .ServiceID'

# 2. Find or create a workspace
fastly ngwaf workspace list --json
fastly ngwaf workspace create --name=my-waf --description="WAF for my-service" --blockingMode=block

# 3. Enable NGWAF product on the service (links the workspace)
#    The CLI does not have a dedicated command for this — use the products API:
curl -X PUT -H "Fastly-Key: $(fastly auth token)" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id":"WORKSPACE_ID"}' \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/SERVICE_ID"

# 4. Verify enablement
curl -H "Fastly-Key: $(fastly auth token)" \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/SERVICE_ID"
```

### Disable NGWAF on a service

```bash
# Fully disable — removes NGWAF from the service (stops all inspection)
curl -X DELETE -H "Fastly-Key: $(fastly auth token)" \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/SERVICE_ID"
# Returns 204 No Content on success

# Alternative: keep NGWAF enabled but stop blocking (observe-only mode)
fastly ngwaf workspace update --workspace-id WORKSPACE_ID --blockingMode log
```

**IMPORTANT**: Prefer `$(fastly auth token)` to get the currently active API token for curl commands. It only writes to non-terminal stdout, so use it in a pipe or shell substitution. If you specifically need a stored token by name, use `$(fastly auth show TOKEN_NAME --reveal --quiet | awk '/^Token:/ {print $2}')`. NEVER run `fastly auth show --reveal` directly — it prints the full token value into the conversation, exposing credentials.

## Workspaces

Workspaces contain NGWAF configurations for a service.

**IMPORTANT — subcommand names**: NGWAF workspace uses `get`, NOT `describe`. There is NO `describe` subcommand. The correct command is `fastly ngwaf workspace get --workspace-id ID`. Do not guess subcommand names — refer to the examples below.

### Workspace Modes (--blockingMode values)

| Mode    | Behavior                                            |
| ------- | --------------------------------------------------- |
| `block` | Actively blocks malicious requests                  |
| `log`   | Inspects and logs but does not block (observe-only) |
| `off`   | Disables WAF processing in the workspace            |

```bash
# List workspaces
fastly ngwaf workspace list

# Create workspace (--description and --blockingMode are required)
fastly ngwaf workspace create \
  --name=NAME \
  --description=DESCRIPTION \
  --blockingMode=block

# Optional create flags: --attackThresholds, --clientIPHeaders,
# --defaultBlockingCode, --defaultRedirectURL, --ipAnonimization, --json

# Get workspace details
fastly ngwaf workspace get --workspace-id WORKSPACE_ID

# Update workspace (same optional flags as create)
fastly ngwaf workspace update --workspace-id WORKSPACE_ID --name updated-name

# Change blocking mode
fastly ngwaf workspace update --workspace-id WORKSPACE_ID --blockingMode log

# Delete workspace
fastly ngwaf workspace delete --workspace-id WORKSPACE_ID
```

## IP Lists

Manage lists of IP addresses for allow/block rules. The `--workspace-id` flag falls back to the `FASTLY_WORKSPACE_ID` environment variable.

### Workspace-Level IP Lists

```bash
# List IP lists
fastly ngwaf workspace ip-list list [--workspace-id] [--json]

# Create IP list (--entries accepts comma-separated values or a file path)
fastly ngwaf workspace ip-list create \
  --entries=ENTRIES \
  --name=NAME \
  [--workspace-id] [--description] [--json]

# Get IP list
fastly ngwaf workspace ip-list get --list-id=LIST-ID [--workspace-id] [--json]

# Update IP list
fastly ngwaf workspace ip-list update \
  --list-id=LIST-ID \
  [--workspace-id] [--description] [--entries] [--json]

# Delete IP list
fastly ngwaf workspace ip-list delete --list-id=LIST-ID [--workspace-id] [--json]
```

### Account-Level IP Lists

```bash
fastly ngwaf ip-list create --entries=ENTRIES --name=NAME [--description] [--json]
fastly ngwaf ip-list delete --list-id=LIST-ID [--json]
fastly ngwaf ip-list get --list-id=LIST-ID [--json]
fastly ngwaf ip-list list [--json]
fastly ngwaf ip-list update --list-id=LIST-ID [--description] [--entries] [--json]
```

## Country Lists

Block or allow traffic from specific countries.

```bash
# List country lists
fastly ngwaf workspace country-list list [--workspace-id] [--json]

# Create country list
fastly ngwaf workspace country-list create \
  --entries=ENTRIES \
  --name=NAME \
  [--workspace-id] [--description] [--json]

# Get country list
fastly ngwaf workspace country-list get --list-id=LIST-ID [--workspace-id] [--json]

# Update country list
fastly ngwaf workspace country-list update \
  --list-id=LIST-ID \
  [--workspace-id] [--description] [--entries] [--json]

# Delete country list
fastly ngwaf workspace country-list delete --list-id=LIST-ID [--workspace-id] [--json]
```

## Signal Lists

Group related signals for easier management.

```bash
# List signal lists
fastly ngwaf workspace signal-list list [--workspace-id] [--json]

# Create signal list
fastly ngwaf workspace signal-list create \
  --entries=ENTRIES \
  --name=NAME \
  [--workspace-id] [--description] [--json]

# Get signal list
fastly ngwaf workspace signal-list get --list-id=LIST-ID [--workspace-id] [--json]

# Update signal list
fastly ngwaf workspace signal-list update \
  --list-id=LIST-ID \
  [--workspace-id] [--description] [--entries] [--json]

# Delete signal list
fastly ngwaf workspace signal-list delete --list-id=LIST-ID [--workspace-id] [--json]
```

## Custom Signals

Create custom detection signals. The `--workspace-id` flag is required (or falls back to `FASTLY_WORKSPACE_ID`).

### Workspace-Level Custom Signals

```bash
# List custom signals
fastly ngwaf workspace customsignal list --workspace-id=WORKSPACE-ID [--json]

# Create custom signal
fastly ngwaf workspace customsignal create \
  --name=NAME \
  --workspace-id=WORKSPACE-ID \
  [--description] [--json]

# Get custom signal
fastly ngwaf workspace customsignal get \
  --signal-id=SIGNAL-ID \
  --workspace-id=WORKSPACE-ID \
  [--json]

# Update custom signal (--description is required)
fastly ngwaf workspace customsignal update \
  --signal-id=SIGNAL-ID \
  --description=DESCRIPTION \
  --workspace-id=WORKSPACE-ID \
  [--json]

# Delete custom signal
fastly ngwaf workspace customsignal delete \
  --signal-id=SIGNAL-ID \
  --workspace-id=WORKSPACE-ID \
  [--json]
```

## String Lists

Match against lists of strings (paths, user agents, etc.).

```bash
# List string lists
fastly ngwaf workspace string-list list [--workspace-id] [--json]

# Create string list
fastly ngwaf workspace string-list create \
  --entries=ENTRIES \
  --name=NAME \
  [--workspace-id] [--description] [--json]

# Get string list
fastly ngwaf workspace string-list get --list-id=LIST-ID [--workspace-id] [--json]

# Update string list
fastly ngwaf workspace string-list update \
  --list-id=LIST-ID \
  [--workspace-id] [--description] [--entries] [--json]

# Delete string list
fastly ngwaf workspace string-list delete --list-id=LIST-ID [--workspace-id] [--json]
```

## Wildcard Lists

Pattern matching with wildcards.

```bash
# List wildcard lists
fastly ngwaf workspace wildcard-list list [--workspace-id] [--json]

# Create wildcard list
fastly ngwaf workspace wildcard-list create \
  --entries=ENTRIES \
  --name=NAME \
  [--workspace-id] [--description] [--json]

# Get wildcard list
fastly ngwaf workspace wildcard-list get --list-id=LIST-ID [--workspace-id] [--json]

# Update wildcard list
fastly ngwaf workspace wildcard-list update \
  --list-id=LIST-ID \
  [--workspace-id] [--description] [--entries] [--json]

# Delete wildcard list
fastly ngwaf workspace wildcard-list delete --list-id=LIST-ID [--workspace-id] [--json]
```

## Thresholds

Configure rate limiting and threshold-based blocking.

```bash
# List thresholds
fastly ngwaf workspace threshold list [--workspace-id] [--json]

# Create threshold
fastly ngwaf workspace threshold create \
  --action=ACTION \
  --do-not-notify=BOOL \
  --duration=DURATION \
  --enabled=BOOL \
  --interval=INTERVAL \
  --limit=LIMIT \
  --name=NAME \
  --signal=SIGNAL \
  [--workspace-id] [--json]

# --action: block or log
# --do-not-notify: true or false
# --duration: seconds (default 86400)
# --enabled: true or false
# --interval: seconds (default 3600)
# --limit: 1-10000 (default 10)
# --name: 3-50 characters
# --signal: signal name

# Get threshold
fastly ngwaf workspace threshold get --threshold-id=THRESHOLD-ID [--workspace-id] [--json]

# Update threshold
fastly ngwaf workspace threshold update \
  --threshold-id=THRESHOLD-ID \
  [--workspace-id] [--action] [--do-not-notify] [--duration] \
  [--enabled] [--interval] [--limit] [--signal] [--json]

# Delete threshold
fastly ngwaf workspace threshold delete --threshold-id=THRESHOLD-ID [--workspace-id] [--json]
```

## Virtual Patches

Temporary security patches for vulnerabilities.

```bash
# List virtual patches
fastly ngwaf workspace virtualpatch list --workspace-id=WORKSPACE-ID [--json]

# Get virtual patch details
fastly ngwaf workspace virtualpatch retrieve \
  --virtual-patch-id=ID \
  --workspace-id=WORKSPACE-ID \
  [--json]

# Update virtual patch
fastly ngwaf workspace virtualpatch update \
  --virtual-patch-id=ID \
  --workspace-id=WORKSPACE-ID \
  [--enabled] [--mode] [--json]
```

## Redactions

Configure data redaction in logs.

```bash
# List redactions
fastly ngwaf workspace redaction list [--workspace-id] [--limit] [--json]

# Create redaction
fastly ngwaf workspace redaction create \
  --field=FIELD \
  --type=TYPE \
  [--workspace-id] [--json]

# Retrieve redaction
fastly ngwaf workspace redaction retrieve --redaction-id=REDACTION-ID [--workspace-id] [--json]

# Update redaction
fastly ngwaf workspace redaction update \
  --redaction-id=REDACTION-ID \
  [--workspace-id] [--field] [--type] [--json]

# Delete redaction
fastly ngwaf workspace redaction delete --redaction-id=REDACTION-ID [--workspace-id] [--json]
```

## Rules

Workspace-level request rules.

```bash
# List rules
fastly ngwaf workspace rule list [--workspace-id] [--action] [--enabled] [--json]

# Create rule
fastly ngwaf workspace rule create --path=PATH [--workspace-id] [--json]

# Get rule
fastly ngwaf workspace rule get --rule-id=RULE-ID [--workspace-id] [--json]

# Update rule
fastly ngwaf workspace rule update --rule-id=RULE-ID --path=PATH [--workspace-id] [--json]

# Delete rule
fastly ngwaf workspace rule delete --rule-id=RULE-ID [--workspace-id] [--json]
```

## Alerts

Configure alerting integrations.

### Supported Alert Destinations

- Datadog
- Jira
- Mailing List (`mailinglist`)
- Microsoft Teams (`microsoftteams`)
- Opsgenie
- PagerDuty
- Slack
- Webhook

### Slack Alert Example

```bash
# List Slack alerts
fastly ngwaf workspace alert slack list [--workspace-id] [--json]

# Create Slack alert
fastly ngwaf workspace alert slack create \
  --webhook=WEBHOOK \
  [--workspace-id] [--description] [--json]

# Get alert
fastly ngwaf workspace alert slack get --alert-id=ALERT-ID [--workspace-id] [--json]

# Update alert
fastly ngwaf workspace alert slack update \
  --alert-id=ALERT-ID \
  --webhook=WEBHOOK \
  [--workspace-id] [--json]

# Delete alert
fastly ngwaf workspace alert slack delete --alert-id=ALERT-ID [--workspace-id] [--json]
```

### Webhook Alert Example

```bash
# Create webhook alert
fastly ngwaf workspace alert webhook create \
  --webhook=WEBHOOK \
  [--workspace-id] [--description] [--json]

# List webhook alerts
fastly ngwaf workspace alert webhook list [--workspace-id] [--json]

# Get webhook alert
fastly ngwaf workspace alert webhook get --alert-id=ALERT-ID [--workspace-id] [--json]

# Update webhook alert
fastly ngwaf workspace alert webhook update \
  --alert-id=ALERT-ID \
  --webhook=WEBHOOK \
  [--workspace-id] [--json]

# Delete webhook alert
fastly ngwaf workspace alert webhook delete --alert-id=ALERT-ID [--workspace-id] [--json]

# Get signing key for webhook verification
fastly ngwaf workspace alert webhook get-signing-key --alert-id=ALERT-ID [--workspace-id] [--json]

# Rotate signing key
fastly ngwaf workspace alert webhook rotate-signing-key --alert-id=ALERT-ID [--workspace-id] [--json]
```

## Account-Level Lists, Signals, and Rules

All workspace-level list types, custom signals, and rules also exist at the account level. These commands follow the same patterns as their workspace counterparts but without `--workspace-id`.

```bash
# Account-level country lists
fastly ngwaf country-list create/delete/get/list/update

# Account-level custom signals
fastly ngwaf customsignal create/delete/get/list/update

# Account-level IP lists
fastly ngwaf ip-list create/delete/get/list/update

# Account-level rules
fastly ngwaf rule create/delete/get/list/update

# Account-level signal lists
fastly ngwaf signal-list create/delete/get/list/update

# Account-level string lists
fastly ngwaf string-list create/delete/get/list/update

# Account-level wildcard lists
fastly ngwaf wildcard-list create/delete/get/list/update
```

## Common Workflows

### Setup Basic WAF Protection

```bash
# 1. Create workspace (use 'block' not 'blocking')
fastly ngwaf workspace create \
  --name=my-service-waf \
  --description="Production WAF" \
  --blockingMode=block

# 2. Enable NGWAF on the service (links workspace to service)
curl -X PUT -H "Fastly-Key: $(fastly auth token)" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id":"WORKSPACE_ID","traffic_ramp":"100"}' \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/SERVICE_ID"

# 3. Create IP blocklist
fastly ngwaf workspace ip-list create \
  --entries="192.0.2.1,198.51.100.0/24" \
  --name=blocklist \
  [--workspace-id]

# 4. Configure alert
fastly ngwaf workspace alert slack create \
  --webhook="https://hooks.slack.com/..." \
  [--workspace-id]
```

### Configure Geo-Blocking

```bash
# Create country blocklist
fastly ngwaf workspace country-list create \
  --entries=RU,CN,KP \
  --name=blocked-countries \
  [--workspace-id]
```

## Common Mistakes

- **`describe` does not exist**: Use `fastly ngwaf workspace get`, not `describe`. No NGWAF subcommand uses `describe`.
- **Wrong API URL for enablement**: The correct path is `/enabled-products/v1/ngwaf/services/{service_id}`, NOT `/enabled-products/v1/services/{service_id}`. The `/ngwaf/` segment is required.
- **Don't run `--help` for commands documented here**: This reference already contains the correct flags and syntax. Running `--help` wastes turns. Only use `--help` for commands NOT covered in this document.
- **Don't search the repo for service IDs**: For operational tasks (enable/disable WAF, change settings), use `fastly service list --json` or `fastly service describe --service-name NAME` to find service IDs. The repo may not contain them.

## Dangerous Operations

Ask the user for explicit confirmation before running these commands:

- **Disabling NGWAF on a service** (`DELETE /enabled-products/v1/ngwaf/services/{id}`) - Stops all WAF inspection
- **Changing blockingMode to `off` or `log`** - Stops blocking attacks (log still inspects but won't block)
- `fastly ngwaf workspace delete` - Deletes WAF workspace and all its rules
- `fastly ngwaf ip-list delete` - Removes an IP blocklist/allowlist
- `fastly ngwaf workspace country-list delete` - Removes country-based blocking
- `fastly ngwaf workspace threshold delete` - Removes rate limiting protection

Disabling or weakening security rules may expose the service to attacks.

## Propagation Delays

NGWAF configuration changes typically propagate within 1-2 minutes:
- Rule updates: 1-2 minutes
- IP list changes: 1-2 minutes
- Threshold/rate limit changes: 1-2 minutes

When updating security rules in response to active attacks, account for this propagation delay. Verify rule effectiveness by monitoring blocked requests in the NGWAF dashboard or alerts after the propagation period.

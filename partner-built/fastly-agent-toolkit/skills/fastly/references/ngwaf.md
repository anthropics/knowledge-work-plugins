# Fastly Next-Gen WAF (NGWAF)

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/ngwaf

## Key Concepts

**Signal Sciences integration**: NGWAF can be accessed via the Fastly control panel or the legacy Signal Sciences control panel (`dashboard.signalsciences.net`). The legacy Signal Sciences API (`docs.fastly.com/signalsciences/api/`) is separate from the Fastly NGWAF API documented here. Customers with access to the Fastly control panel use the `/ngwaf/v1/` endpoints.

**Signal-based detection model**: Every request inspected by NGWAF gets tagged with zero or more signals (e.g., `SQLI`, `XSS`). Rules then match on these signals to decide actions. Signals have a `detector_scope` which can be `system`, `account`, `workspace`, or `unknown`; custom signals use the `site.*` prefix.

**Three deployment types**: NGWAF supports edge WAF deployment (runs in the Fastly edge `edge_waf_request_inspection` phase, after VCL/Compute processing), on-prem WAF deployment (module and agent on your web servers, or agent in reverse proxy mode), and cloud WAF deployment (on Fastly's cloud-hosted infrastructure). Edge deployment is the recommended approach for Fastly CDN customers. Feature availability varies by deployment type.

**Workspace model**: Workspaces (also known as sites) are user-defined sets of rules and settings. A workspace contains rules, events, requests, and configuration. Custom signals are account-level, not workspace-level. One workspace can be linked to multiple Fastly services via the enablement API. Account-level rules can target all workspaces (`"*"`) or specific workspace IDs.

**Traffic ramp**: When enabling NGWAF on a service, the `traffic_ramp` configuration controls what percentage of traffic is inspected (e.g., `"20"`).

## Enablement

Enable, disable, and configure NGWAF on individual services. Requires a `workspace_id` linking the service to an NGWAF workspace.

**Important distinction**: Enablement (this section) controls whether NGWAF is active on a service at all. Workspace mode (`block`/`log`/`off`) controls what NGWAF does with inspected traffic. To fully disable WAF on a service, use the `DELETE` endpoint below — changing workspace mode to `log` or `off` is NOT the same as disabling.

| Action                | Method   | Endpoint                                                         |
| --------------------- | -------- | ---------------------------------------------------------------- |
| Enable                | `PUT`    | `/enabled-products/v1/ngwaf/services/{service_id}`               |
| Disable (full remove) | `DELETE` | `/enabled-products/v1/ngwaf/services/{service_id}`               |
| Get status            | `GET`    | `/enabled-products/v1/ngwaf/services/{service_id}`               |
| Get configuration     | `GET`    | `/enabled-products/v1/ngwaf/services/{service_id}/configuration` |
| Update configuration  | `PATCH`  | `/enabled-products/v1/ngwaf/services/{service_id}/configuration` |
| List enabled services | `GET`    | `/enabled-products/v1/ngwaf/services`                            |

```bash
# Enable NGWAF on a service (links to a workspace)
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id":"7JFbo4RNA0OKdFWC04r6B3"}' \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/$SERVICE_ID"

# Check enablement status
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/$SERVICE_ID"

# Disable NGWAF on a service (stops all inspection, returns 204)
curl -X DELETE -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/$SERVICE_ID"

# Update configuration (e.g., change traffic ramp percentage)
curl -X PATCH -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"traffic_ramp":"20"}' \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/$SERVICE_ID/configuration"
```

Enable request body requires `workspace_id` (required) and optionally `traffic_ramp` (percentage of traffic to inspect). Disable returns `204 No Content`.

## Workspaces

Each workspace has a mode, attack signal thresholds, and a default blocking response code. Workspaces are also known as sites.

**Valid workspace modes** (exactly three values):
- `block` — actively blocks malicious requests
- `log` — inspects and logs but does not block (observe-only)
- `off` — disables WAF processing in the workspace

No other mode values exist. Do not try `monitor`, `disabled`, `detection`, etc.

**CLI note**: When using the Fastly CLI, the subcommand to retrieve a workspace is `get` (e.g., `fastly ngwaf workspace get`). There is NO `describe` subcommand for NGWAF resources.

| Action           | Method   | Endpoint                                          |
| ---------------- | -------- | ------------------------------------------------- |
| List workspaces  | `GET`    | `/ngwaf/v1/workspaces`                            |
| Create workspace | `POST`   | `/ngwaf/v1/workspaces`                            |
| Get workspace    | `GET`    | `/ngwaf/v1/workspaces/{workspace_id}`             |
| Edit workspace   | `PATCH`  | `/ngwaf/v1/workspaces/{workspace_id}`             |
| Delete workspace | `DELETE` | `/ngwaf/v1/workspaces/{workspace_id}`             |
| Get top attacks  | `GET`    | `/ngwaf/v1/workspaces/{workspace_id}/top-attacks` |

```bash
# List all workspaces
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/ngwaf/v1/workspaces?limit=100"
```

Workspace modes: `off`, `log`, `block`. The `attack_signal_thresholds` object controls how many attack signals per IP trigger flagging (`one_minute`, `ten_minutes`, `one_hour`, or `immediate`). The `default_blocking_response_code` accepts `301`, `302`, or `400-599`.

## Rules

Rules allow, block, rate-limit, or tag requests based on conditions. Two scopes: **account-level** rules (apply across workspaces) and **workspace-level** rules (apply to one workspace). Four rule types: `request`, `signal`, `rate_limit`, `templated_signal`.

### Account-Level Rules

| Action              | Method   | Endpoint                    |
| ------------------- | -------- | --------------------------- |
| List account rules  | `GET`    | `/ngwaf/v1/rules`           |
| Create account rule | `POST`   | `/ngwaf/v1/rules`           |
| Get account rule    | `GET`    | `/ngwaf/v1/rules/{rule_id}` |
| Edit account rule   | `PATCH`  | `/ngwaf/v1/rules/{rule_id}` |
| Delete account rule | `DELETE` | `/ngwaf/v1/rules/{rule_id}` |

### Workspace-Level Rules

| Action                | Method   | Endpoint                                              |
| --------------------- | -------- | ----------------------------------------------------- |
| List workspace rules  | `GET`    | `/ngwaf/v1/workspaces/{workspace_id}/rules`           |
| Create workspace rule | `POST`   | `/ngwaf/v1/workspaces/{workspace_id}/rules`           |
| Get workspace rule    | `GET`    | `/ngwaf/v1/workspaces/{workspace_id}/rules/{rule_id}` |
| Edit workspace rule   | `PATCH`  | `/ngwaf/v1/workspaces/{workspace_id}/rules/{rule_id}` |
| Delete workspace rule | `DELETE` | `/ngwaf/v1/workspaces/{workspace_id}/rules/{rule_id}` |

Rule actions include: `block`, `allow`, `add_signal`, `exclude_signal`, `block_signal`, `browser_challenge`, `dynamic_challenge`, `verify_token`, `deception`, `log_request`. Condition fields include `ip`, `path`, `method`, `domain`, `country`, `user_agent`, `ja3_fingerprint`, `response_code`, and multival fields like `request_header`, `signal`, `query_parameter`.

## Custom Signals

Custom signals are user-defined tags that can be applied to requests via rules. They exist at the account level.

| Action               | Method   | Endpoint                        |
| -------------------- | -------- | ------------------------------- |
| List custom signals  | `GET`    | `/ngwaf/v1/signals`             |
| Create custom signal | `POST`   | `/ngwaf/v1/signals`             |
| Get custom signal    | `GET`    | `/ngwaf/v1/signals/{signal_id}` |
| Edit custom signal   | `PATCH`  | `/ngwaf/v1/signals/{signal_id}` |
| Delete custom signal | `DELETE` | `/ngwaf/v1/signals/{signal_id}` |

Custom signal names generate a `reference_id` automatically: the name is lowercased, spaces become dashes, and it is prefixed with `site.` (e.g., name `foo signal` becomes `site.foo-signal`).

## Events and Requests

Events are actions NGWAF takes due to threshold-based blocking, templated rules, or site alerts. Requests are individual HTTP requests tagged with signals.

### Events

| Action              | Method  | Endpoint                                                       |
| ------------------- | ------- | -------------------------------------------------------------- |
| List events         | `GET`   | `/ngwaf/v1/workspaces/{workspace_id}/events`                   |
| Get event           | `GET`   | `/ngwaf/v1/workspaces/{workspace_id}/events/{event_id}`        |
| Expire event        | `PATCH` | `/ngwaf/v1/workspaces/{workspace_id}/events/{event_id}`        |
| Remove flag from IP | `POST`  | `/ngwaf/v1/workspaces/{workspace_id}/events/{event_id}/expire` |

List events requires a `from` parameter (RFC 3339 datetime). Filter by `signal`, `ip`, or `status` (`active`/`expired`).

```bash
# List recent events in a workspace
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/ngwaf/v1/workspaces/$WORKSPACE_ID/events?from=2025-01-01T00:00:00Z&limit=100"
```

### Requests

| Action                | Method | Endpoint                                                           |
| --------------------- | ------ | ------------------------------------------------------------------ |
| Search requests       | `GET`  | `/ngwaf/v1/workspaces/{workspace_id}/requests`                     |
| Get request           | `GET`  | `/ngwaf/v1/workspaces/{workspace_id}/requests/{request_id}`        |
| Report false positive | `POST` | `/ngwaf/v1/workspaces/{workspace_id}/requests/{request_id}/report` |

The `q` parameter accepts a search query syntax (e.g., `"/a/path sqli from:-7h"`). Supports CSV export via `export=true` with `Accept: text/csv` header. Each request includes detected `signals` with `id`, `location`, `value`, `detector`, and `detector_scope`.

## Additional APIs

| Area             | Key Endpoints                                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Lists            | `/ngwaf/v1/lists` (account-level), `/ngwaf/v1/workspaces/{workspaceId}/lists` (workspace-level) -- lists for use in rule conditions |
| Virtual Patches  | `/ngwaf/v1/workspaces/{workspace_id}/virtual-patches` -- virtual patches for a workspace                                            |
| Redactions       | `/ngwaf/v1/workspaces/{workspace_id}/redactions` -- control which fields are redacted in request logs                               |
| Workspace Alerts | `/ngwaf/v1/workspaces/{workspace_id}/alerts` -- configure alert notifications                                                       |
| Timeseries       | `/ngwaf/v1/workspaces/{workspace_id}/timeseries` -- time-bucketed signal and request metrics                                        |
| Reports          | `/ngwaf/v1/reports/signals` -- signals report data                                                                                  |

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                         | URL                                                                                                |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| NGWAF product overview, prerequisites, billing | `https://docs.fastly.com/products/ngwaf`                                                           |
| Setup guides, configuration, deployment modes  | `https://www.fastly.com/documentation/guides/next-gen-waf`                                         |
| API reference, endpoint schemas, examples      | `https://www.fastly.com/documentation/reference/api/ngwaf`                                         |
| Edge WAF deployment setup                      | `https://www.fastly.com/documentation/guides/next-gen-waf/setup-and-configuration/edge-deployment` |
| Cloud WAF deployment setup                     | `https://www.fastly.com/documentation/guides/next-gen-waf/setup-and-configuration/cloud-waf`       |
| Rule types, conditions, actions                | `https://www.fastly.com/documentation/guides/next-gen-waf/rules`                                   |
| Signal monitoring and custom signals           | `https://www.fastly.com/documentation/guides/next-gen-waf/monitoring`                              |
| Attack signals overview                        | `https://www.fastly.com/documentation/guides/next-gen-waf/signals`                                 |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

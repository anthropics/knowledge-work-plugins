# Fastly DDoS Protection

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/ddos-protection

## Enablement

| Action       | Method   | Endpoint                                                                   |
| ------------ | -------- | -------------------------------------------------------------------------- |
| Enable       | `PUT`    | `/enabled-products/v1/ddos_protection/services/{service_id}`               |
| Disable      | `DELETE` | `/enabled-products/v1/ddos_protection/services/{service_id}`               |
| Get status   | `GET`    | `/enabled-products/v1/ddos_protection/services/{service_id}`               |
| Get config   | `GET`    | `/enabled-products/v1/ddos_protection/services/{service_id}/configuration` |
| Set config   | `PATCH`  | `/enabled-products/v1/ddos_protection/services/{service_id}/configuration` |
| List enabled | `GET`    | `/enabled-products/v1/ddos_protection/services`                            |

Modes: `log` (observe only, default), `block` (mitigate), `off`

```bash
# Enable in blocking mode
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" -d '{"mode":"block"}' \
  "https://api.fastly.com/enabled-products/v1/ddos_protection/services/{service_id}"

# Switch to logging mode
curl -X PATCH -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" -d '{"mode":"log"}' \
  "https://api.fastly.com/enabled-products/v1/ddos_protection/services/{service_id}/configuration"

# Disable
curl -X DELETE -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/enabled-products/v1/ddos_protection/services/{service_id}"
```

## Events API

| Action        | Method  | Endpoint                                                              |
| ------------- | ------- | --------------------------------------------------------------------- |
| List events   | `GET`   | `/ddos-protection/v1/events`                                          |
| Get event     | `GET`   | `/ddos-protection/v1/events/{event_id}`                               |
| List rules    | `GET`   | `/ddos-protection/v1/events/{event_id}/rules`                         |
| Get rule      | `GET`   | `/ddos-protection/v1/rules/{rule_id}`                                 |
| Update rule   | `PATCH` | `/ddos-protection/v1/rules/{rule_id}`                                 |
| Traffic stats | `GET`   | `/ddos-protection/v1/events/{event_id}/rules/{rule_id}/traffic-stats` |

List params: `cursor`, `limit`, `service_id`, `from`, `to` (RFC 3339)
Rules params: `include=traffic_stats` for inline stats

```bash
# Check active attacks (ended_at is null)
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/ddos-protection/v1/events?limit=10" | \
  jq '.data[] | select(.ended_at == null)'

# Get rules with traffic breakdown
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/ddos-protection/v1/events/{event_id}/rules?include=traffic_stats"

# Switch rule to log-only
curl -X PATCH -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" -d '{"action":"log"}' \
  "https://api.fastly.com/ddos-protection/v1/rules/{rule_id}"
```

Rule actions: `default` (follow service mode), `block`, `log`, `off`

## How It Works

**Adaptive Threat Engine** baselines traffic throughput and attributes (L3/L4 headers, TLS, L7) to fingerprint attack traffic and distinguish it from normal traffic.

- Billing: attack traffic free

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                               | URL                                                                                                       |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Prerequisites, limitations, billing                  | `https://docs.fastly.com/products/fastly-ddos-protection`                                                 |
| Enabling/disabling, protection modes, UI walkthrough | `https://www.fastly.com/documentation/guides/security/ddos-protection/about-ddos-protection`              |
| Dashboard, events page, rule management controls     | `https://www.fastly.com/documentation/guides/security/ddos-protection/about-the-ddos-protection-controls` |
| API endpoints, request/response schemas              | `https://www.fastly.com/documentation/reference/api/products/ddos_protection`                             |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

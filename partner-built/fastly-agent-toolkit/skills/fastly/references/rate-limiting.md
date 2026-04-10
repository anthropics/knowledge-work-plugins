# Fastly Rate Limiting

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/vcl-services/rate-limiter

## Key Concepts

- **Three separate systems.** ERL, VCL ratecounters, and NGWAF Advanced Rate Limiting have different prerequisites, configuration methods, and enforcement models. Agents frequently conflate them -- see the comparison table below.
- **Penalty box (ERL and VCL only).** Once a client exceeds the rate limit, they are placed in a penalty box for the configured duration. Future requests from that client are actioned (blocked or logged) for the penalty duration. NGWAF Advanced Rate Limiting uses signal-based thresholds instead.
- **Client key composition (ERL).** ERL accepts an array of VCL variables to generate a composite counter key (e.g., `req.http.Fastly-Client-IP`, `req.http.User-Agent`, or custom headers like `req.http.API-Key`).
- **URI scoping via Dictionary (ERL).** ERL allows you to specify paths to protect using a Dictionary where keys are URI paths (relative, no trailing `/`, no query strings or regex).
- **Versioned configuration (ERL).** ERL rate limiters are attached to a service version. Creating or modifying them requires a new version and activation.
- **Anti-abuse vs resource rate limiting.** Fastly's ratecounters are designed for anti-abuse (fast counting, approximate, no global sync). For precise resource-rate limiting (e.g., 1000 API calls/hour), use real-time log streaming to an external system that maintains globally synchronized counts.
- **VCL `check_rate()` syntax.** `ratelimit.check_rate(entry, ratecounter, delta, window, limit, penaltybox, ttl)` — `entry` is the client key (any string), `window` is `1`/`10`/`60` seconds, `limit` is RPS threshold, `ttl` is penalty duration. Use `check_rates()` for dual sustained+burst limits. Guard with `fastly.ff.visits_this_service == 0` to count only edge requests (avoid double-counting at shield).
- **Rate counter precision.** Counts are estimated, not precise. Shorter windows detect faster but are less accurate. Bucket boundaries are fixed (aligned to :00/:10/:20 within each minute), not sliding.

## Three Distinct Rate Limiting Systems

Agents frequently conflate these. They have different prerequisites, configuration methods, and capabilities.

| System                           | Config Method          | Subscription Required            | Window/Bucket Sizes  |
| -------------------------------- | ---------------------- | -------------------------------- | -------------------- |
| **Edge Rate Limiting (ERL)**     | REST API               | NGWAF (Signal Sciences)          | 1s, 10s, 60s fixed   |
| **VCL Rate Limiting**            | VCL declarations       | None (must be enabled by Fastly) | 1s, 10s, 60s windows |
| **NGWAF Advanced Rate Limiting** | Signal Sciences UI/API | NGWAF                            | Configurable         |

### Decision Framework

- **Use ERL** when you want API-managed rate limiting policies, need per-client-key enforcement at the edge, and already have an NGWAF subscription.
- **Use VCL ratecounters** when you need rate limiting without an NGWAF subscription, want full VCL-level control, or need custom logic beyond what ERL supports. See VCL function reference in the Documentation section. Compute has analogous rate limiting APIs.
- **Use NGWAF Advanced Rate Limiting** when you need signal-based rules, complex request inspection, or already manage security through the Signal Sciences platform. See `ngwaf.md` for workspace rules and rate-limited sources APIs.

## Edge Rate Limiting (ERL) API

Requires NGWAF subscription (Signal Sciences Cloud WAF or Next-Gen WAF) and a paid account with a contract for full-site delivery.

| Action              | Method   | Endpoint                                                   |
| ------------------- | -------- | ---------------------------------------------------------- |
| List rate limiters  | `GET`    | `/service/{service_id}/version/{version_id}/rate-limiters` |
| Create rate limiter | `POST`   | `/service/{service_id}/version/{version_id}/rate-limiters` |
| Get rate limiter    | `GET`    | `/rate-limiters/{rate_limiter_id}`                         |
| Update rate limiter | `PUT`    | `/rate-limiters/{rate_limiter_id}`                         |
| Delete rate limiter | `DELETE` | `/rate-limiters/{rate_limiter_id}`                         |

### ERL Configuration Fields

| Field                  | Type    | Description                                                                                        |
| ---------------------- | ------- | -------------------------------------------------------------------------------------------------- |
| `name`                 | string  | Human-readable name (1-255 chars)                                                                  |
| `http_methods`         | array   | Methods to limit: HEAD, OPTIONS, GET, POST, PUT, PATCH, DELETE, TRACE                              |
| `rps_limit`            | integer | Requests per second threshold (10-10000)                                                           |
| `window_size`          | enum    | Seconds the RPS limit must be exceeded: `1`, `10`, or `60`                                         |
| `client_key`           | array   | VCL variables for client identification (e.g., `req.http.Fastly-Client-IP`)                        |
| `penalty_box_duration` | integer | Minutes the limiter stays active after violation (1-60)                                            |
| `action`               | enum    | `response` (custom status), `response_object` (named VCL response object), `log_only`              |
| `response`             | object  | Custom response: `status` (100-999), `content_type`, `content`. Required when action is `response` |
| `response_object_name` | string  | Name of existing response object. Required when action is `response_object`                        |
| `uri_dictionary_name`  | string  | Dictionary name containing URI keys to scope limiting. If null, all URIs are limited               |
| `logger_type`          | string  | Logging endpoint type for `log_only` action (e.g., `s3`, `splunk`, `datadog`, `https`)             |

```bash
# Create a rate limiter (POST form-encoded)
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=api-rate-limit&http_methods[]=POST&http_methods[]=PUT&http_methods[]=PATCH&http_methods[]=DELETE&rps_limit=100&window_size=10&client_key[]=req.http.Fastly-Client-IP&penalty_box_duration=30&action=response&response[status]=429&response[content_type]=application/json&response[content]=%7B%22error%22%3A%22Too%20many%20requests%22%7D" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/rate-limiters"

# List all rate limiters for a service version
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/rate-limiters"

# Get a specific rate limiter
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/rate-limiters/{rate_limiter_id}"

# Update a rate limiter (change RPS limit and window)
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "rps_limit=500&window_size=60" \
  "https://api.fastly.com/rate-limiters/{rate_limiter_id}"

# Delete a rate limiter
curl -X DELETE -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/rate-limiters/{rate_limiter_id}"
```

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                               | URL                                                                           |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| Product page, prerequisites, billing | `https://docs.fastly.com/products/edge-rate-limiting`                         |
| Rate limiting conceptual overview    | `https://www.fastly.com/documentation/guides/concepts/rate-limiting`          |
| Security guide for rate limiting     | `https://www.fastly.com/documentation/guides/security/rate-limiting/`         |
| ERL API reference                    | `https://www.fastly.com/documentation/reference/api/security/rate-limiter`    |
| VCL ratecounter declaration          | `https://www.fastly.com/documentation/reference/vcl/declarations/ratecounter` |
| VCL penaltybox declaration           | `https://www.fastly.com/documentation/reference/vcl/declarations/penaltybox`  |
| VCL rate limiting example            | `https://www.fastly.com/documentation/solutions/examples/rate-limit-requests` |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

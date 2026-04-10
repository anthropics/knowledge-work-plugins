# Fastly Load Balancing

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/load-balancing

## Key Concepts

**Backends vs Pools.** Backends are versioned origin server definitions -- any change requires cloning the service version, editing, and activating. Pools are dynamic origin groups: the pool definition itself is versioned, but the servers within a pool can be added, removed, or disabled at any time without a new version activation. Dynamic server pools are Limited Availability; consider custom directors or automatic load balancing as alternatives.

**Director types.** Directors group backends for load balancing. The `type` field controls selection:
- `1` (random): Weighted random selection. Each backend's `weight` determines its share of traffic.
- `3` (hash): Consistent hashing. Requests with the same hash key go to the same backend (useful for cache locality).
- `4` (client): Client-based selection.

**Quorum.** Minimum percentage of healthy servers (0-100) required before the director or pool is considered "up." Default is 75. When the healthy percentage drops below quorum, the entire group is treated as down. Fastly will then attempt to serve stale content or return a 503.

**Shield + backend interaction.** When origin shielding is enabled, edge POPs forward cache misses to a designated shield POP rather than directly to the origin. The shield POP then selects the backend. Both directors and pools support a `shield` field to configure this. Backend-level `shield` and director/pool-level `shield` serve different roles -- backend `shield` designates the shield POP for that specific backend, while director/pool `shield` applies to the group.

**Health check mechanism.** Fastly sends periodic HTTP requests (configurable method, path, host, headers) to each origin. The `threshold` and `window` fields define a sliding window: if `threshold` out of the last `window` checks succeed, the origin is healthy. The `initial` field sets how many probes are assumed healthy when a new config is loaded, preventing origins from being marked down during deployment. Set `initial` equal to `threshold` to avoid 503s on first deployment.

**Health check amortization.** Each Fastly site handles health checks independently and shares results within the site. Actual health check volume is: `[1/check_interval] × [~150 sites] × [services using this backend] × [IPs returned by DNS]`. To reduce volume, set the same `share_key` across services that use the same backend (defaults to service ID -- set to customer ID to share across all your services). If a backend hostname resolves to multiple IPs, a separate health check is sent to each one (up to 16 IPs by default).

**Partial health.** If a backend resolves to multiple IP addresses and some are sick, the backend is still considered healthy. Fastly routes traffic to the healthy IPs and considers the backend healthy within any director it belongs to.

**DNS caching tied to health checks.** Fastly honors DNS TTL for backend hostnames but only renews DNS results when performing a health check. Live traffic always uses cached DNS results. If DNS lookup fails, stale DNS data is used briefly; continued failure clears the IPs and marks the backend sick.

**Shielding double-execution.** Services using shielding will in many cases execute edge code twice: once at the edge POP and once at the shield POP. Use `req.backend.is_origin` to conditionally modify requests only when going to origin, and `fastly.ff.visits_this_service` to modify responses only at the edge. Use `Fastly-Client-IP` header instead of `client.ip` for true client IP (shield requests report the source POP's IP as `client.ip`).

**Placeholder backend technique for directors + shielding.** Custom directors override Fastly's shield routing when assigned via `req.backend`. Workaround: create a placeholder backend (e.g., address `127.0.0.1`) with shielding enabled, set `false` conditions on real backends, then swap the placeholder for the director in `vcl_miss`/`vcl_pass` when `req.backend == F_shielding_placeholder`.

## Backends

Versioned origin servers. Changes require a new service version and activation.

| Action         | Method   | Endpoint                                                            |
| -------------- | -------- | ------------------------------------------------------------------- |
| List backends  | `GET`    | `/service/{service_id}/version/{version_id}/backend`                |
| Create backend | `POST`   | `/service/{service_id}/version/{version_id}/backend`                |
| Get backend    | `GET`    | `/service/{service_id}/version/{version_id}/backend/{backend_name}` |
| Update backend | `PUT`    | `/service/{service_id}/version/{version_id}/backend/{backend_name}` |
| Delete backend | `DELETE` | `/service/{service_id}/version/{version_id}/backend/{backend_name}` |

Key fields: `address` (hostname/IP), `name`, `port`, `use_ssl`, `ssl_cert_hostname`, `ssl_sni_hostname`, `shield`, `healthcheck`, `weight`, `auto_loadbalance`, `connect_timeout`, `first_byte_timeout`, `between_bytes_timeout`, `max_conn`, `override_host`, `request_condition`.

**SSL hostname rule**: `ssl_cert_hostname` and `ssl_sni_hostname` must match the origin's TLS certificate (its SANs), NOT the `override_host` value. When `override_host` differs from `address`, always set `ssl_cert_hostname` and `ssl_sni_hostname` to the `address` hostname. Omitting them or setting them to the `override_host` value causes 503 "hostname doesn't match against certificate".

**Pre-flight check**: Before creating any backend, verify the origin's TLS SANs to determine the correct `ssl_cert_hostname`/`ssl_sni_hostname`: `echo | openssl s_client -connect ORIGIN:443 -servername ORIGIN 2>/dev/null | openssl x509 -noout -text | grep -A1 "Subject Alternative Name"`. Also verify the origin responds to the intended Host header: `curl -sI -H "Host: DESIRED_HOST" https://ORIGIN_ADDRESS/`.

```bash
# Create a backend (same host for address and override_host)
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=my-origin&address=origin.example.com&port=443&use_ssl=1&ssl_cert_hostname=origin.example.com&ssl_sni_hostname=origin.example.com" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/backend"

# Create a backend (different host header from origin address)
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=my-origin&address=origin.example.com&port=443&use_ssl=1&override_host=cdn.example.com&ssl_cert_hostname=origin.example.com&ssl_sni_hostname=origin.example.com" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/backend"
```

## Directors

Load balancer groups that distribute traffic across multiple backends. Versioned.

| Action          | Method   | Endpoint                                                              |
| --------------- | -------- | --------------------------------------------------------------------- |
| List directors  | `GET`    | `/service/{service_id}/version/{version_id}/director`                 |
| Create director | `POST`   | `/service/{service_id}/version/{version_id}/director`                 |
| Get director    | `GET`    | `/service/{service_id}/version/{version_id}/director/{director_name}` |
| Update director | `PUT`    | `/service/{service_id}/version/{version_id}/director/{director_name}` |
| Delete director | `DELETE` | `/service/{service_id}/version/{version_id}/director/{director_name}` |

Key fields: `name`, `type` (1=random, 3=hash, 4=client), `quorum` (0-100, default 75), `retries` (default 5), `shield`, `capacity`.

```bash
# Create a director with round-robin-style random balancing
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=my-director&type=1&quorum=75&retries=3" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/director"
```

## Director-Backend Mapping

Associates backends with directors. A backend can belong to multiple directors, but a director holds only one reference to a specific backend.

| Action              | Method   | Endpoint                                                                                     |
| ------------------- | -------- | -------------------------------------------------------------------------------------------- |
| Get relationship    | `GET`    | `/service/{service_id}/version/{version_id}/director/{director_name}/backend/{backend_name}` |
| Create relationship | `POST`   | `/service/{service_id}/version/{version_id}/director/{director_name}/backend/{backend_name}` |
| Delete relationship | `DELETE` | `/service/{service_id}/version/{version_id}/director/{director_name}/backend/{backend_name}` |

```bash
# Associate a backend with a director
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/director/my-director/backend/my-origin"
```

## Pools

Dynamic server pools. The pool definition is versioned, but servers within the pool are NOT versioned -- servers can be added/removed without activating a new service version.

| Action      | Method   | Endpoint                                                      |
| ----------- | -------- | ------------------------------------------------------------- |
| List pools  | `GET`    | `/service/{service_id}/version/{version_id}/pool`             |
| Create pool | `POST`   | `/service/{service_id}/version/{version_id}/pool`             |
| Get pool    | `GET`    | `/service/{service_id}/version/{version_id}/pool/{pool_name}` |
| Update pool | `PUT`    | `/service/{service_id}/version/{version_id}/pool/{pool_name}` |
| Delete pool | `DELETE` | `/service/{service_id}/version/{version_id}/pool/{pool_name}` |

Key fields: `name`, `type` (random, hash, client), `quorum` (0-100, default 75), `shield`, `healthcheck`, `max_conn_default` (default 200), `connect_timeout`, `first_byte_timeout`, `between_bytes_timeout`, `override_host`, `use_tls`, `tls_cert_hostname`, `tls_sni_hostname`, `tls_check_cert`.

## Servers

Servers within a pool. **NOT versioned** -- add, remove, or disable servers without a new service version activation.

| Action        | Method   | Endpoint                                                  |
| ------------- | -------- | --------------------------------------------------------- |
| List servers  | `GET`    | `/service/{service_id}/pool/{pool_id}/servers`            |
| Add server    | `POST`   | `/service/{service_id}/pool/{pool_id}/server`             |
| Get server    | `GET`    | `/service/{service_id}/pool/{pool_id}/server/{server_id}` |
| Update server | `PUT`    | `/service/{service_id}/pool/{pool_id}/server/{server_id}` |
| Delete server | `DELETE` | `/service/{service_id}/pool/{pool_id}/server/{server_id}` |

Key fields: `address` (hostname/IP, required), `port` (default 80), `weight` (1-100, default 100), `max_conn` (0 inherits from pool's `max_conn_default`), `disabled` (boolean), `override_host`.

Note: Server endpoints use `pool_id` (alphanumeric ID), not `pool_name`.

## Health Checks

HTTP health checks sent to origins. Versioned. Can be shared across backends and pools via the `healthcheck` field.

| Action              | Method   | Endpoint                                                                    |
| ------------------- | -------- | --------------------------------------------------------------------------- |
| List health checks  | `GET`    | `/service/{service_id}/version/{version_id}/healthcheck`                    |
| Create health check | `POST`   | `/service/{service_id}/version/{version_id}/healthcheck`                    |
| Get health check    | `GET`    | `/service/{service_id}/version/{version_id}/healthcheck/{healthcheck_name}` |
| Update health check | `PUT`    | `/service/{service_id}/version/{version_id}/healthcheck/{healthcheck_name}` |
| Delete health check | `DELETE` | `/service/{service_id}/version/{version_id}/healthcheck/{healthcheck_name}` |

Key fields: `name`, `host`, `path`, `method`, `expected_response` (status code), `check_interval` (ms, 1000-3600000), `threshold` (successes needed), `window` (recent checks to keep), `timeout` (ms), `initial` (probes assumed OK on config load), `http_version`, `headers` (array of custom headers).

```bash
# Create a health check
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=my-healthcheck&host=origin.example.com&path=/health&method=HEAD&expected_response=200&check_interval=15000&threshold=3&window=5&timeout=5000" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/healthcheck"
```

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                          | URL                                                                                            |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Backends API reference                          | `https://www.fastly.com/documentation/reference/api/load-balancing/backend`                    |
| Directors API reference                         | `https://www.fastly.com/documentation/reference/api/load-balancing/directors/director`         |
| Pools API reference                             | `https://www.fastly.com/documentation/reference/api/load-balancing/pools/pool`                 |
| Health checks API reference                     | `https://www.fastly.com/documentation/reference/api/load-balancing/healthcheck`                |
| Load balancing concepts                         | `https://www.fastly.com/documentation/guides/concepts/load-balancing`                          |
| Health check concepts                           | `https://www.fastly.com/documentation/guides/concepts/healthcheck`                             |
| Failover concepts                               | `https://www.fastly.com/documentation/guides/concepts/failover`                                |
| Shielding concepts, double-execution, debugging | `https://www.fastly.com/documentation/guides/concepts/shielding`                               |
| Shielding setup via web interface               | `https://www.fastly.com/documentation/guides/getting-started/hosts/shielding`                  |
| Health check setup via web interface            | `https://www.fastly.com/documentation/guides/getting-started/hosts/working-with-health-checks` |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

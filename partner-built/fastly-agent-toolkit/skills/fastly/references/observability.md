# Fastly Observability

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/observability

## Key Concepts

**Real-time vs historical timing.** Real-time endpoints (`rt.fastly.com`) provide per-second data with an `AggregateDelay`. Historical endpoints (`api.fastly.com/stats`) support `minute`, `hour`, and `day` resolution. Minute data is usually available within 2-15 minutes; hourly within 15 minutes of the hour; daily around 2am UTC the following day.

**120-second real-time window.** The `/ts/h` endpoints return data for the 120 seconds preceding the latest available timestamp. Use `/ts/{timestamp}` with the returned `Timestamp` for continuous polling beyond this window.

**Metric aggregation.** `bandwidth` is a computed total of multiple byte fields. `hit_ratio` is the ratio of cache hits to cache misses (between 0 and 1). `origin_offload` measures the fraction of bytes served from cache. These derived fields are provided by the API, not computed client-side.

**Domain Inspector, Origin Inspector, and Log Explorer & Insights require enablement.** These are optional upgrades that must be enabled per service before their endpoints return data.

## Enablement

Product slugs: `domain_inspector`, `origin_inspector`, `log_explorer_insights`. See `products.md` for the universal enablement pattern.

## Historical Stats

Query cached statistics grouped by service, aggregated across services, or filtered by field. Supports `day`, `hour`, and `minute` resolution via the `by` parameter. Filter by `region`, `datacenter`, or `services`.

| Action                          | Method | Endpoint                                    |
| ------------------------------- | ------ | ------------------------------------------- |
| Get stats (all services)        | `GET`  | `/stats`                                    |
| Get single field (all services) | `GET`  | `/stats/field/{field}`                      |
| Get aggregated stats            | `GET`  | `/stats/aggregate`                          |
| Get stats for a service         | `GET`  | `/stats/service/{service_id}`               |
| Get single field for a service  | `GET`  | `/stats/service/{service_id}/field/{field}` |
| Get usage by region             | `GET`  | `/stats/usage`                              |
| Get usage by service            | `GET`  | `/stats/usage_by_service`                   |
| Get month-to-date usage         | `GET`  | `/stats/usage_by_month`                     |
| Get region codes                | `GET`  | `/stats/regions`                            |
| Get service stats summary       | `GET`  | `/service/{service_id}/stats/summary`       |

```bash
# Get historical stats for a service, last 7 days, daily resolution
curl -s -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/stats/service/$SERVICE_ID?from=7+days+ago&by=day"

# Get a single field across all services
curl -s -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/stats/field/hit_ratio?from=1+day+ago&by=hour"
```

## Real-Time Stats

Per-second stats for a single service. Hosted on `rt.fastly.com` (not `api.fastly.com`). Pass `0` as timestamp for the latest complete second. Use the returned `Timestamp` value as the next request's timestamp for seamless polling.

| Action                  | Method | Endpoint                                                                  |
| ----------------------- | ------ | ------------------------------------------------------------------------- |
| Get data from timestamp | `GET`  | `https://rt.fastly.com/v1/channel/{service_id}/ts/{timestamp_in_seconds}` |
| Get last 120 seconds    | `GET`  | `https://rt.fastly.com/v1/channel/{service_id}/ts/h`                      |
| Get last N entries      | `GET`  | `https://rt.fastly.com/v1/channel/{service_id}/ts/h/limit/{max_entries}`  |

```bash
# Subscribe to real-time stats (get latest second, then poll with returned Timestamp)
curl -s -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://rt.fastly.com/v1/channel/$SERVICE_ID/ts/0"
```

## Metrics Platform

Time-series TTFB (time-to-first-byte) percentile metrics at edge, origin, and shield. Uses RFC 8339 timestamps and path-based granularity (`minutely`, `hourly`, `daily`). Supports `group_by`, `region`, `datacenter`, and cursor pagination.

Metric set: `ttfb` -- metrics include `ttfb_edge_p50_us`, `ttfb_origin_p95_us`, `ttfb_shield_p99_us`, etc.

| Action                    | Method | Endpoint                                                |
| ------------------------- | ------ | ------------------------------------------------------- |
| Get metrics for a service | `GET`  | `/metrics/platform/services/{service_id}/{granularity}` |

## Domain Inspector

Per-domain edge metrics (requests, bytes, status codes, hit ratio, origin offload). **Must be enabled per service via the enablement API.** Uses `start`/`end` (ISO 8601) and `downsample` (`minute`, `hour`, `day`). Can `group_by` domain, region, or datacenter. Absolute times in historical API are UTC.

| Action                                   | Method | Endpoint                                                                 |
| ---------------------------------------- | ------ | ------------------------------------------------------------------------ |
| Get historical domain data               | `GET`  | `/metrics/domains/services/{service_id}`                                 |
| Get real-time domain data from timestamp | `GET`  | `https://rt.fastly.com/v1/domains/{service_id}/ts/{start_timestamp}`     |
| Get real-time domain data (last 120s)    | `GET`  | `https://rt.fastly.com/v1/domains/{service_id}/ts/h`                     |
| Get real-time domain data (limited)      | `GET`  | `https://rt.fastly.com/v1/domains/{service_id}/ts/h/limit/{max_entries}` |

## Origin Inspector

Per-origin metrics (responses, bytes, status codes, latency buckets). **Must be enabled per service via the enablement API.** Can `group_by` host, region, or datacenter. Includes latency histogram buckets (0-1ms through 60000ms+). Absolute times in historical API are UTC.

| Action                                   | Method | Endpoint                                                                 |
| ---------------------------------------- | ------ | ------------------------------------------------------------------------ |
| Get historical origin data               | `GET`  | `/metrics/origins/services/{service_id}`                                 |
| Get real-time origin data from timestamp | `GET`  | `https://rt.fastly.com/v1/origins/{service_id}/ts/{start_timestamp}`     |
| Get real-time origin data (last 120s)    | `GET`  | `https://rt.fastly.com/v1/origins/{service_id}/ts/h`                     |
| Get real-time origin data (limited)      | `GET`  | `https://rt.fastly.com/v1/origins/{service_id}/ts/h/limit/{max_entries}` |

## Alerts

Metric-based alert definitions that trigger notifications via integrations. Sources: `origins`, `domains`, or `stats`. Evaluation strategies: `above_threshold`, `all_above_threshold`, `below_threshold`, `percent_absolute`, `percent_decrease`, `percent_increase`. Periods: `2m`, `3m`, `5m`, `15m`, `30m`.

| Action                  | Method   | Endpoint                              |
| ----------------------- | -------- | ------------------------------------- |
| List alert definitions  | `GET`    | `/alerts/definitions`                 |
| Create alert definition | `POST`   | `/alerts/definitions`                 |
| Get alert definition    | `GET`    | `/alerts/definitions/{definition_id}` |
| Update alert definition | `PUT`    | `/alerts/definitions/{definition_id}` |
| Delete alert definition | `DELETE` | `/alerts/definitions/{definition_id}` |
| List alert history      | `GET`    | `/alerts/history`                     |

```bash
# List all alert definitions
curl -s -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/alerts/definitions"
```

## Log Explorer

Query sampled log records for a service. Requires `service_id`, `start`, and `end` (RFC 3339). Supports field-based filters with operators (`=`, `ends-with`, `in`, `not_in`, `gt`, `gte`, `lt`, `lte`). Filterable fields: `domain`, `request_path`, `fastly_pop`, `response_time`, `response_status`, `fastly_is_shield`, `fastly_is_edge`, `client_os_name`, `client_device_type`, `client_browser_name`, `fastly_is_cache_hit`.

| Action               | Method | Endpoint                      |
| -------------------- | ------ | ----------------------------- |
| Retrieve log records | `GET`  | `/observability/log-explorer` |

```bash
# Query log records for a service
curl -s -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/observability/log-explorer?service_id=$SERVICE_ID&start=2024-01-01T00:00:00Z&end=2024-01-02T00:00:00Z&limit=10"
```

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header). Pages contain lists of available metrics and stats respectively.

| Source                             | URL                                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| Historical stats API reference     | `https://www.fastly.com/documentation/reference/api/metrics-stats/historical-stats`  |
| Real-time stats API reference      | `https://www.fastly.com/documentation/reference/api/metrics-stats/realtime`          |
| Domain Inspector API reference     | `https://www.fastly.com/documentation/reference/api/metrics-stats/domain-inspector`  |
| Origin Inspector API reference     | `https://www.fastly.com/documentation/reference/api/metrics-stats/origin-inspector`  |
| Observability guides               | `https://www.fastly.com/documentation/guides/observability`                          |
| Alert configuration and management | `https://www.fastly.com/documentation/guides/observability/alerts`                   |
| Observability dashboards setup     | `https://www.fastly.com/documentation/guides/observability/observability-dashboards` |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

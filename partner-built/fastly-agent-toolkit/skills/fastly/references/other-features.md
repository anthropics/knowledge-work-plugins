# Fastly Other Features

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api

## Fanout / Real-Time Publishing

Publish messages to Fanout channels for WebSocket, SSE, and long-poll delivery. GRIP-compatible (`https://api.fastly.com/service/{service_id}` as GRIP URL). Requires a trailing slash on the endpoint. Auth may use `Authorization: Bearer {token}` instead of `Fastly-Key`.

| Action           | Method | Endpoint                         |
| ---------------- | ------ | -------------------------------- |
| Publish messages | `POST` | `/service/{service_id}/publish/` |

Body contains `items` array; each item has `channel` and `formats` (`ws-message`, `http-stream`, `http-response`).

```bash
# Publish a WebSocket message to a Fanout channel
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"channel":"mychannel","formats":{"ws-message":{"content":"hello world"}}}]}' \
  "https://api.fastly.com/service/$SERVICE_ID/publish/"
```

## Public IP List

Get Fastly's IPv4 and IPv6 ranges for firewall allowlisting. No authentication required. Subscribe to [Fastly status](https://fastlystatus.com/) for IP address change announcements.

| Action                 | Method | Endpoint          |
| ---------------------- | ------ | ----------------- |
| List Fastly public IPs | `GET`  | `/public-ip-list` |

```bash
# Get Fastly's public IP ranges (no auth required)
curl -s "https://api.fastly.com/public-ip-list" | jq .
```

Returns `addresses` (IPv4) and `ipv6_addresses` (IPv6) arrays.

## POPs

List all Fastly Points of Presence with location, region, coordinates, and shield eligibility.

| Action        | Method | Endpoint       |
| ------------- | ------ | -------------- |
| List all POPs | `GET`  | `/datacenters` |

```bash
# List all Fastly POPs
curl -s -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/datacenters" | jq '.[].code'
```

Each POP includes `code` (three-letter), `name`, `region`, `coordinates`, `shield` (shield code if eligible), and billing/stats regions.

## HTTP/3

Enable or disable HTTP/3 (QUIC) support on a per-service, per-version basis.

| Action            | Method   | Endpoint                                           |
| ----------------- | -------- | -------------------------------------------------- |
| Get HTTP/3 status | `GET`    | `/service/{service_id}/version/{version_id}/http3` |
| Enable HTTP/3     | `POST`   | `/service/{service_id}/version/{version_id}/http3` |
| Disable HTTP/3    | `DELETE` | `/service/{service_id}/version/{version_id}/http3` |

```bash
# Enable HTTP/3 for a service version
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'feature_revision=1' \
  "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/http3"
```

## Image Optimizer

Configure default Image Optimizer settings for a service version. Individual requests can override via URL query parameters.

| Action             | Method  | Endpoint                                                                      |
| ------------------ | ------- | ----------------------------------------------------------------------------- |
| Get IO defaults    | `GET`   | `/service/{service_id}/version/{version_id}/image_optimizer_default_settings` |
| Update IO defaults | `PATCH` | `/service/{service_id}/version/{version_id}/image_optimizer_default_settings` |

Settings: `resize_filter` (lanczos3/lanczos2/bicubic/bilinear/nearest), `webp` (bool), `webp_quality` (1-100), `jpeg_type` (auto/baseline/progressive), `jpeg_quality` (1-100), `upscale` (bool), `allow_video` (bool, GIF-to-MP4).

## Sudo

Request elevated permissions for sensitive operations (e.g., creating automation tokens). Re-authenticates with username/password; sudo expires after `expiry_time` (default 5 minutes).

| Action              | Method | Endpoint |
| ------------------- | ------ | -------- |
| Request sudo access | `POST` | `/sudo`  |

Body: `{"username": "...", "password": "..."}`. Optional `expiry_time` field.

## Audit Events

Query account activity and audit trail. Filter by event type, service, user, token, or date range. Supports pagination and sorting.

| Action      | Method | Endpoint             |
| ----------- | ------ | -------------------- |
| List events | `GET`  | `/events`            |
| Get event   | `GET`  | `/events/{event_id}` |

Query params: `filter[event_type]`, `filter[service_id]`, `filter[user_id]`, `filter[created_at][gte]`, `filter[created_at][lte]`, `page[number]`, `page[size]`, `sort`.

## Notifications

Manage notification integrations for alerts. Supported types: mailinglist, microsoftteams, newrelic, pagerduty, slack, webhook.

| Action                         | Method   | Endpoint                                                        |
| ------------------------------ | -------- | --------------------------------------------------------------- |
| List integration types         | `GET`    | `/notifications/integration-types`                              |
| Search integrations            | `GET`    | `/notifications/integrations`                                   |
| Create integration             | `POST`   | `/notifications/integrations`                                   |
| Get integration                | `GET`    | `/notifications/integrations/{integration_id}`                  |
| Update integration             | `PATCH`  | `/notifications/integrations/{integration_id}`                  |
| Delete integration             | `DELETE` | `/notifications/integrations/{integration_id}`                  |
| Get webhook signing key        | `GET`    | `/notifications/integrations/{integration_id}/signingKey`       |
| Rotate webhook signing key     | `POST`   | `/notifications/integrations/{integration_id}/rotateSigningKey` |
| Send mailing list confirmation | `POST`   | `/notifications/mailinglist-confirmations`                      |

Create body: `{"name": "...", "type": "slack", "config": {"webhook": "https://hooks.slack.com/..."}}`.

## Starred Services

Star or unstar services for quick access. Uses JSON:API format with user and service relationships.

| Action      | Method   | Endpoint           |
| ----------- | -------- | ------------------ |
| List stars  | `GET`    | `/stars`           |
| Create star | `POST`   | `/stars`           |
| Get star    | `GET`    | `/stars/{star_id}` |
| Delete star | `DELETE` | `/stars/{star_id}` |

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                           | URL                                                                                          |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| Fanout concept                   | `https://www.fastly.com/documentation/guides/concepts/real-time-messaging/fanout`            |
| WebSocket tunneling concept      | `https://www.fastly.com/documentation/guides/concepts/real-time-messaging/websockets-tunnel` |
| Image Optimizer product          | `https://docs.fastly.com/products/image-optimizer`                                           |
| Public IP list API               | `https://www.fastly.com/documentation/reference/api/utils/public-ip-list`                    |
| POP locations and network map    | `https://www.fastly.com/documentation/guides/concepts/pop`                                   |
| Geolocation and device detection | `https://www.fastly.com/documentation/guides/concepts/geolocation`                           |
| Streaming miss concept           | `https://www.fastly.com/documentation/guides/concepts/real-time-messaging/streaming-miss`    |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

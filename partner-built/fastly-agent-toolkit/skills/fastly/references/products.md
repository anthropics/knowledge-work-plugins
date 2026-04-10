# Fastly Product Enablement

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/products

## Key Concepts

- **Products are enabled per-service** unless noted as account-level in the catalog. Account-level products (AI Accelerator, Domain Research, Object Storage) omit the `/services/{service_id}` path segment entirely.
- **Some products require prerequisites**: Bot Management requires purchase of the Next-Gen WAF.
- **Configuration endpoints are separate from enablement**: Only `ddos_protection` and `ngwaf` currently expose `/configuration` endpoints. All other products are simple on/off toggles.
- **Product slugs use underscores**, matching the API spec filenames (e.g., `bot_management`, not `bot-management`). The slug is also returned as `product.id` in API responses.

## Universal Enablement Pattern

All Fastly products follow the same API pattern. Replace `{product_id}` with the slug from the Product Catalog below.

**Per-service products** (most products):

| Action       | Method   | Endpoint                                                  |
| ------------ | -------- | --------------------------------------------------------- |
| Enable       | `PUT`    | `/enabled-products/v1/{product_id}/services/{service_id}` |
| Disable      | `DELETE` | `/enabled-products/v1/{product_id}/services/{service_id}` |
| Get status   | `GET`    | `/enabled-products/v1/{product_id}/services/{service_id}` |
| List enabled | `GET`    | `/enabled-products/v1/{product_id}/services`              |

**Account-level products** (no service_id):

| Action     | Method   | Endpoint                            |
| ---------- | -------- | ----------------------------------- |
| Enable     | `PUT`    | `/enabled-products/v1/{product_id}` |
| Disable    | `DELETE` | `/enabled-products/v1/{product_id}` |
| Get status | `GET`    | `/enabled-products/v1/{product_id}` |

**Configuration endpoints** (only some products support these):

| Action        | Method  | Endpoint                                                                |
| ------------- | ------- | ----------------------------------------------------------------------- |
| Get config    | `GET`   | `/enabled-products/v1/{product_id}/services/{service_id}/configuration` |
| Update config | `PATCH` | `/enabled-products/v1/{product_id}/services/{service_id}/configuration` |

```bash
# Enable a product on a service (e.g., brotli_compression)
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/enabled-products/v1/brotli_compression/services/$SERVICE_ID"

# Check enablement status
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/enabled-products/v1/brotli_compression/services/$SERVICE_ID"

# Get DDoS Protection configuration (products with configuration only)
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/enabled-products/v1/ddos_protection/services/$SERVICE_ID/configuration"
```

Response (enable/status):
```json
{
  "product": { "id": "brotli_compression", "object": "product" },
  "service": { "id": "{service_id}", "object": "service" },
  "_links": {
    "self": "https://api.fastly.com/enabled-products/v1/brotli_compression/services/{service_id}",
    "service": "https://api.fastly.com/service/{service_id}"
  }
}
```

Disable returns `204 No Content` on success.

## Product Catalog

| Product                 | Slug (`product_id`)     | Scope   | Has Configuration                     | Notes                             |
| ----------------------- | ----------------------- | ------- | ------------------------------------- | --------------------------------- |
| AI Accelerator          | `ai_accelerator`        | Account | No                                    | Beta                              |
| API Discovery           | `api_discovery`         | Service | No                                    |                                   |
| Bot Management          | `bot_management`        | Service | No                                    | Requires NGWAF subscription       |
| Brotli Compression      | `brotli_compression`    | Service | No                                    |                                   |
| DDoS Protection         | `ddos_protection`       | Service | Yes -- `mode`: off/log/block          | Defaults to `log` mode            |
| Domain Inspector        | `domain_inspector`      | Service | No                                    |                                   |
| Domain Research         | `domain_research`       | Account | No                                    |                                   |
| Fanout                  | `fanout`                | Service | No                                    | Publish-subscribe message broker  |
| Image Optimizer         | `image_optimizer`       | Service | No                                    |                                   |
| Log Explorer & Insights | `log_explorer_insights` | Service | No                                    |                                   |
| Next-Gen WAF (NGWAF)    | `ngwaf`                 | Service | Yes -- `workspace_id`, `traffic_ramp` | Requires `workspace_id` on enable |
| Object Storage          | `object_storage`        | Account | No                                    |                                   |
| Origin Inspector        | `origin_inspector`      | Service | No                                    |                                   |
| WebSockets              | `websockets`            | Service | No                                    |                                   |

### Products with Configuration

**DDoS Protection** -- Enable accepts an optional `mode` in the request body (`off`, `log`, or `block`). Defaults to `log` if omitted. Use the `/configuration` endpoint to change mode after enablement.

**NGWAF** -- Enable requires a `workspace_id` in the request body to link a workspace. Optionally accepts `traffic_ramp` (percentage of traffic to inspect). Use the `/configuration` endpoint to update these after enablement.

```bash
# Enable NGWAF with a workspace
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id": "your-workspace-id", "traffic_ramp": "100"}' \
  "https://api.fastly.com/enabled-products/v1/ngwaf/services/$SERVICE_ID"

# Update DDoS Protection mode to block
curl -X PATCH -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mode": "block"}' \
  "https://api.fastly.com/enabled-products/v1/ddos_protection/services/$SERVICE_ID/configuration"
```

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                | URL                                                           |
| ------------------------------------- | ------------------------------------------------------------- |
| Products API reference (all products) | `https://www.fastly.com/documentation/reference/api/products` |
| Products overview                     | `https://docs.fastly.com/products`                            |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

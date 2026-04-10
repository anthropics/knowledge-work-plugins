# Fastly API Security

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/security

## Key Concepts

- **API Discovery** automatically catalogs API endpoints observed in traffic flowing through the service. It identifies HTTP methods, domains, and paths without requiring an API specification.
- **Operations** represent discovered or manually created API paths with method, domain, path, and metadata. They can be organized with tags and annotated with descriptions.
- **Discovered operations** have a status lifecycle: `DISCOVERED`, `SAVED` (added to inventory), or `IGNORED`.
- **Tags** group operations for organization (e.g., by environment or team). Operations can have multiple tags; tags track how many operations reference them.
- The API Discovery product must be **enabled on the service first** before the operations endpoints will return data.

## Enablement

Product slug: `api_discovery`. Must be enabled per service before the operations endpoints return data. No product-specific configuration. See `products.md` for the universal enablement pattern.

## API Operations

| Action           | Method   | Endpoint                                                           |
| ---------------- | -------- | ------------------------------------------------------------------ |
| List discovered  | `GET`    | `/api-security/v1/services/{service_id}/discovered-operations`     |
| List operations  | `GET`    | `/api-security/v1/services/{service_id}/operations`                |
| Create operation | `POST`   | `/api-security/v1/services/{service_id}/operations`                |
| Get operation    | `GET`    | `/api-security/v1/services/{service_id}/operations/{operation_id}` |
| Update operation | `PATCH`  | `/api-security/v1/services/{service_id}/operations/{operation_id}` |
| Delete operation | `DELETE` | `/api-security/v1/services/{service_id}/operations/{operation_id}` |
| List tags        | `GET`    | `/api-security/v1/services/{service_id}/tags`                      |
| Create tag       | `POST`   | `/api-security/v1/services/{service_id}/tags`                      |
| Get tag          | `GET`    | `/api-security/v1/services/{service_id}/tags/{tag_id}`             |
| Update tag       | `PATCH`  | `/api-security/v1/services/{service_id}/tags/{tag_id}`             |
| Delete tag       | `DELETE` | `/api-security/v1/services/{service_id}/tags/{tag_id}`             |

Query parameters for list endpoints: `limit` (1-1000, default 100), `page` (0-based). Discovered operations accept `status` filter (`DISCOVERED`, `SAVED`, `IGNORED`). Operations accept `tag_id` filter.

```bash
# List discovered operations for a service
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/api-security/v1/services/{service_id}/discovered-operations"
```

Operations have fields: `id`, `method`, `domain`, `path`, `description`, `tag_ids`, `created_at`, `updated_at`, `last_seen_at`. Discovered operations have: `method`, `domain`, `path`, `status`, `updated_at`, `last_seen_at`.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                    | URL                                                                 |
| ----------------------------------------- | ------------------------------------------------------------------- |
| API Security reference                    | `https://www.fastly.com/documentation/reference/api/security`       |
| API Discovery setup, inventory management | `https://www.fastly.com/documentation/guides/security/api-security` |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

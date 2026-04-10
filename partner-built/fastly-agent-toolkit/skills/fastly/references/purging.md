# Fastly Cache Purging

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/purging

## Key Concepts

**Surrogate keys** are tags attached to cached objects by setting the `Surrogate-Key` response header at your origin. Multiple space-separated keys can be assigned to a single object, and one key can span many objects. This enables fine-grained purge control (e.g., purge all images for a product without purging the product page itself).

**Origin sets the keys, the purge API references them:**
- Origin response header: `Surrogate-Key: product-123 category-shoes image` (space-separated)
- Purge API request body: `{"surrogate_keys": ["product-123"]}` (JSON array)

## Purge Types

Three purge types, each with a different endpoint and auth model:

| Action                    | Method  | Endpoint                                      | Notes                              |
| ------------------------- | ------- | --------------------------------------------- | ---------------------------------- |
| Single URL purge (direct) | `PURGE` | `{content_url}`                               | Unauthenticated by default         |
| Single URL purge (API)    | `POST`  | `/purge/{cached_url}`                         | Authenticated via Fastly-Key       |
| Surrogate key purge       | `POST`  | `/service/{service_id}/purge/{surrogate_key}` | Purges all objects tagged with key |
| Batch surrogate key purge | `POST`  | `/service/{service_id}/purge`                 | Up to 256 keys per request         |
| Purge all                 | `POST`  | `/service/{service_id}/purge_all`             | Invalidates entire service cache   |

## Soft vs Hard Purge

Soft and hard purge are orthogonal to the purge type. Any single URL, surrogate key, or batch surrogate key purge can be soft or hard. **Purge-all is always hard and cannot be soft.**

- **Hard purge** (default): Object becomes immediately inaccessible. New requests go to origin as cache misses.
- **Soft purge**: Marks object as stale instead of deleting it. Enables conditional revalidation (`If-Modified-Since`, `If-None-Match`) and protects origin from traffic spikes after purge.

To make any purge soft, add this header to the request:

```http
Fastly-Soft-Purge: 1
```

## Single URL Purge

Two methods:

**Direct PURGE** -- send HTTP `PURGE` to the content URL itself. Unauthenticated by default. To require token auth, set `req.http.Fastly-Purge-Requires-Auth = "1"` in `vcl_recv`. In VCL services, the `PURGE` method is transformed to `FASTLYPURGE` before VCL processing. In Compute services, `PURGE` requests must be explicitly forwarded to a backend to reach the cache layer.

**API purge** -- `POST` to `https://api.fastly.com/purge/{hostname}/{path}` with `Fastly-Key` header. Always authenticated.

```bash
# Direct PURGE (unauthenticated by default)
curl -X PURGE http://www.example.com/images/logo.png

# API purge (authenticated)
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/purge/www.example.com/images/logo.png"

# Soft purge via API
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Fastly-Soft-Purge: 1" \
  "https://api.fastly.com/purge/www.example.com/images/logo.png"
```

## Surrogate Key Purge

Purge all objects tagged with a specific surrogate key. Uses `api.fastly.com`.

```bash
# Hard purge by surrogate key
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/{service_id}/purge/product-123"

# Soft purge by surrogate key
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Fastly-Soft-Purge: 1" \
  "https://api.fastly.com/service/{service_id}/purge/product-123"
```

### Batch Surrogate Key Purge

Purge multiple keys in one request. Maximum **256 keys** per batch.

Two ways to specify keys -- JSON body or header:

```bash
# Option 1: JSON body with surrogate_keys array
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"surrogate_keys":["key_1","key_2","key_3"]}' \
  "https://api.fastly.com/service/{service_id}/purge"

# Option 2: Space-separated keys in Surrogate-Key header
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Surrogate-Key: key_1 key_2 key_3" \
  "https://api.fastly.com/service/{service_id}/purge"
```

Response maps each key to a purge ID:

```json
{"key_1": "108-1391560174-974124", "key_2": "108-1391560174-974125", "key_3": "108-1391560174-974126"}
```

## Purge All

Instantly invalidates all cached content for a service. **Always a hard purge.**

```bash
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/{service_id}/purge_all"
```

Purge-all takes up to 2 minutes to complete. With shielding enabled, edge and shield POPs may be purged in the wrong order, causing stale content to be re-cached. This can be mitigated by comparing `req.vcl.generation` (VCL) or `FASTLY_CACHE_GENERATION` (Compute) between edge and shield. See `https://www.fastly.com/documentation/solutions/examples/prevent-race-conditions-with-purge-all-and-shielding`.

## Content Edge Check

Verify purge propagation across POPs. Rate limited to 200 requests/hour.

```bash
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/content/edge_check?url=https://www.example.com/path/to/object"
```

Returns per-POP hash, request/response details, response time, server, and POP identifier. Hash of `error-timeout-$pop` means the content took too long to download; `warning-too-large-$pop` means the response was too large.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                            | URL                                                                                                  |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Purging concepts, best practices, limitations     | `https://www.fastly.com/documentation/guides/concepts/cache/purging`                                 |
| Working with surrogate keys                       | `https://www.fastly.com/documentation/guides/full-site-delivery/purging/working-with-surrogate-keys` |
| Purging guides and tutorials                      | `https://www.fastly.com/documentation/guides/full-site-delivery/purging`                             |
| API endpoints, request/response schemas           | `https://www.fastly.com/documentation/reference/api/purging`                                         |
| Soft purge guide, stale-while-revalidate behavior | `https://www.fastly.com/documentation/guides/full-site-delivery/purging/soft-purges`                 |
| Purging a single URL via UI, API, CLI             | `https://www.fastly.com/documentation/guides/full-site-delivery/purging/purging-a-url`               |
| Purge-all guide, timing, caveats                  | `https://www.fastly.com/documentation/guides/full-site-delivery/purging/purging-all-content`         |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

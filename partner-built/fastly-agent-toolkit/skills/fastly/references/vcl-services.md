# Fastly VCL Services

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/vcl-services

## Key Concepts

**Snippets vs Custom VCL.** Snippets are blocks of VCL logic inserted into the generated VCL at locations determined by their `type`. Custom VCL is a full VCL configuration file used to customize the entire configuration for a service.

**Dynamic vs Versioned Snippets.** Versioned snippets are associated with a service version. Dynamic snippets (`dynamic: "1"`) can be updated via `/service/{service_id}/snippet/{id}` without activating a new version.

**Edge Dictionaries.** Dictionaries are attached to a version but their items are updated independently without version activation. Dictionaries must be created/deleted on a draft version, but items are managed via the non-versioned item endpoints.

**Condition Types.** `REQUEST` conditions are available everywhere and may only reference VCL variables accessible throughout the VCL flow. `CACHE` conditions are available in `vcl_fetch` and may access VCL variables in the `beresp` namespace. `RESPONSE` conditions are available in `vcl_deliver` and may access VCL variables in the `resp` namespace. `PREFETCH` conditions are available in `vcl_miss` and `vcl_pass` and may access VCL variables in the `bereq` namespace.

**Stale content states.** Cached objects transition through three stale states after TTL expires: **stale-while-revalidate (SWR)** serves stale content immediately while asynchronously revalidating with origin; **stale-if-error (SIE)** serves stale content when the backend is sick (auto) or when VCL returns `deliver_stale` from `vcl_fetch`, `vcl_error`, or `vcl_miss`; **expired** means the object can no longer be served stale. Use `stale.exists` to check for usable stale content. `Surrogate-Control` overrides `Cache-Control` for Fastly's cache and is automatically stripped before delivery to clients. Compute services do not support `stale-if-error`.

**Request collapsing.** When multiple requests arrive for the same uncached object, Fastly queues them on a "waiting list" and sends a single fetch to origin. Cacheable responses satisfy all queued requests. Uncacheable responses dequeue requests consecutively (potential bottleneck). `return(pass)` in `vcl_fetch` on a cacheable response creates a **hit-for-pass** marker (default 2-minute TTL, minimum 2 minutes, maximum 1 hour) that disables collapsing for future requests. To skip collapsing entirely, use `return(pass)` in `vcl_recv` or set `req.hash_ignore_busy = true`. Clustering and shielding create up to four collapsing opportunities.

**Streaming miss.** Enable with `beresp.do_stream` to begin writing partial responses to cache as soon as headers arrive. New requests for the same URL during download join the in-progress response instead of triggering a new origin fetch (provided the object is still fresh). Without streaming miss, the entire response must complete before any queued requests are served.

**Default caching behavior.** Fastly VCL services respect origin `Cache-Control`, `Expires`, and `Vary` headers by default. If the origin sends `Cache-Control: max-age=3600`, Fastly caches for 1 hour with no VCL configuration needed. Custom VCL (snippets or full VCL) is only needed to override or extend this behavior.

**Fastly VCL is different than mainstream VCL**: Use an up-to-date Fastly VCL reference when developing VCL code.

## Custom VCL

Upload and manage custom VCL files. Set `main` to `true` to designate the main VCL for a version.

| Action                     | Method   | Endpoint                                                                   |
| -------------------------- | -------- | -------------------------------------------------------------------------- |
| List custom VCL            | `GET`    | `/service/{service_id}/version/{version_id}/vcl`                           |
| Create custom VCL          | `POST`   | `/service/{service_id}/version/{version_id}/vcl`                           |
| Get custom VCL             | `GET`    | `/service/{service_id}/version/{version_id}/vcl/{vcl_name}`                |
| Update custom VCL          | `PUT`    | `/service/{service_id}/version/{version_id}/vcl/{vcl_name}`                |
| Delete custom VCL          | `DELETE` | `/service/{service_id}/version/{version_id}/vcl/{vcl_name}`                |
| Set as main                | `PUT`    | `/service/{service_id}/version/{version_id}/vcl/{vcl_name}/main`           |
| Get generated VCL          | `GET`    | `/service/{service_id}/version/{version_id}/generated_vcl`                 |
| Get boilerplate VCL        | `GET`    | `/service/{service_id}/version/{version_id}/boilerplate`                   |
| Download raw VCL           | `GET`    | `/service/{service_id}/version/{version_id}/vcl/{vcl_name}/download`       |
| VCL diff between versions  | `GET`    | `/service/{service_id}/vcl/diff/from/{from_version_id}/to/{to_version_id}` |
| Lint VCL (service context) | `POST`   | `/service/{service_id}/lint`                                               |
| Lint VCL (default flags)   | `POST`   | `/vcl_lint`                                                                |

```bash
# Upload custom VCL
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "name=my_custom_vcl" \
  --data-urlencode "content=sub vcl_recv { set req.http.X-Custom = \"true\"; }" \
  --data-urlencode "main=true" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/vcl"
```

## VCL Snippets

Blocks of VCL injected into specific subroutine locations without replacing the entire generated VCL. Two kinds: **versioned** (locked to a service version, require activation) and **dynamic** (update content in-place without new version).

| Action                   | Method   | Endpoint                                                    |
| ------------------------ | -------- | ----------------------------------------------------------- |
| List snippets            | `GET`    | `/service/{service_id}/version/{version_id}/snippet`        |
| Create snippet           | `POST`   | `/service/{service_id}/version/{version_id}/snippet`        |
| Get versioned snippet    | `GET`    | `/service/{service_id}/version/{version_id}/snippet/{name}` |
| Update versioned snippet | `PUT`    | `/service/{service_id}/version/{version_id}/snippet/{name}` |
| Delete snippet           | `DELETE` | `/service/{service_id}/version/{version_id}/snippet/{name}` |
| Get dynamic snippet      | `GET`    | `/service/{service_id}/snippet/{id}`                        |
| Update dynamic snippet   | `PUT`    | `/service/{service_id}/snippet/{id}`                        |

Snippet `type` determines the subroutine insertion point: `init`, `recv`, `hash`, `hit`, `miss`, `pass`, `fetch`, `error`, `deliver`, `log`, `none`. Set `dynamic` to `"1"` at creation to make it dynamic (updatable without new version). The `priority` field (default `"100"`) controls execution order -- lower numbers run first.

```bash
# Create a dynamic snippet in vcl_recv
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=block-bad-bots&dynamic=1&type=recv&priority=10&content=if (req.http.User-Agent ~ \"BadBot\") { error 403 \"Forbidden\"; }" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/snippet"
```

## Conditions

Control whether logic defined in configured VCL objects is applied for a particular client request. Each condition contains a VCL conditional expression that evaluates to true or false.

| Action           | Method   | Endpoint                                                                |
| ---------------- | -------- | ----------------------------------------------------------------------- |
| List conditions  | `GET`    | `/service/{service_id}/version/{version_id}/condition`                  |
| Create condition | `POST`   | `/service/{service_id}/version/{version_id}/condition`                  |
| Get condition    | `GET`    | `/service/{service_id}/version/{version_id}/condition/{condition_name}` |
| Update condition | `PUT`    | `/service/{service_id}/version/{version_id}/condition/{condition_name}` |
| Delete condition | `DELETE` | `/service/{service_id}/version/{version_id}/condition/{condition_name}` |

Condition `type` determines where it executes: `REQUEST` (everywhere, req namespace), `CACHE` (vcl_fetch, beresp namespace), `RESPONSE` (vcl_deliver, resp namespace), `PREFETCH` (vcl_miss/vcl_pass, bereq namespace).

## Headers

Add, modify, or delete headers on requests and responses. Support regex-based transformations.

| Action        | Method   | Endpoint                                                          |
| ------------- | -------- | ----------------------------------------------------------------- |
| List headers  | `GET`    | `/service/{service_id}/version/{version_id}/header`               |
| Create header | `POST`   | `/service/{service_id}/version/{version_id}/header`               |
| Get header    | `GET`    | `/service/{service_id}/version/{version_id}/header/{header_name}` |
| Update header | `PUT`    | `/service/{service_id}/version/{version_id}/header/{header_name}` |
| Delete header | `DELETE` | `/service/{service_id}/version/{version_id}/header/{header_name}` |

Header `action`: `set`, `append`, `delete`, `regex`, `regex_repeat`. Header `type`: `request` (before lookup), `cache` (before storing), `response` (before delivery). Attach to conditions via `request_condition`, `cache_condition`, or `response_condition` fields.

## Request Settings, Response Objects, Cache Settings, Gzip

These versioned objects configure request handling, synthetic responses, cache behavior, and compression. All follow the same CRUD pattern at `/service/{service_id}/version/{version_id}/{resource}` and `/service/{service_id}/version/{version_id}/{resource}/{name}`.

| Resource         | Base path           | Key fields                                                                               |
| ---------------- | ------------------- | ---------------------------------------------------------------------------------------- |
| Request Settings | `/request_settings` | `action` (lookup/pass), `force_ssl`, `force_miss`, `geo_headers`, `max_stale_age`, `xff` |
| Response Objects | `/response_object`  | `status`, `response`, `content`, `content_type`, `request_condition`                     |
| Cache Settings   | `/cache_settings`   | `action` (pass/cache/restart), `ttl`, `stale_ttl`, `cache_condition`                     |
| Gzip             | `/gzip`             | `extensions` (space-separated), `content_types` (space-separated)                        |

Each supports `GET` (list), `POST` (create), `GET` (by name), `PUT` (update), `DELETE`.

## Edge Dictionaries

Key-value data table for VCL services. Items update without version activation.

| Action                  | Method   | Endpoint                                                                      |
| ----------------------- | -------- | ----------------------------------------------------------------------------- |
| List dictionaries       | `GET`    | `/service/{service_id}/version/{version_id}/dictionary`                       |
| Create dictionary       | `POST`   | `/service/{service_id}/version/{version_id}/dictionary`                       |
| Get dictionary          | `GET`    | `/service/{service_id}/version/{version_id}/dictionary/{dictionary_name}`     |
| Update dictionary       | `PUT`    | `/service/{service_id}/version/{version_id}/dictionary/{dictionary_name}`     |
| Delete dictionary       | `DELETE` | `/service/{service_id}/version/{version_id}/dictionary/{dictionary_name}`     |
| Get dictionary metadata | `GET`    | `/service/{service_id}/version/{version_id}/dictionary/{dictionary_id}/info`  |
| List items              | `GET`    | `/service/{service_id}/dictionary/{dictionary_id}/items`                      |
| Create item             | `POST`   | `/service/{service_id}/dictionary/{dictionary_id}/item`                       |
| Get item                | `GET`    | `/service/{service_id}/dictionary/{dictionary_id}/item/{dictionary_item_key}` |
| Upsert item             | `PUT`    | `/service/{service_id}/dictionary/{dictionary_id}/item/{dictionary_item_key}` |
| Update item             | `PATCH`  | `/service/{service_id}/dictionary/{dictionary_id}/item/{dictionary_item_key}` |
| Delete item             | `DELETE` | `/service/{service_id}/dictionary/{dictionary_id}/item/{dictionary_item_key}` |
| Batch update items      | `PATCH`  | `/service/{service_id}/dictionary/{dictionary_id}/items`                      |

Item keys max 256 characters, values max 8000 characters. Batch updates support up to 1000 items with `op` values: `create`, `update`, `delete`, `upsert`.

```bash
# Create a dictionary
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -d "name=blocked_ips&write_only=false" \
  "https://api.fastly.com/service/{service_id}/version/{version_id}/dictionary"

# Upsert a dictionary item (no version activation needed)
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -d "item_value=blocked" \
  "https://api.fastly.com/service/{service_id}/dictionary/{dictionary_id}/item/192.168.1.1"
```

## Apex Redirects

Redirect apex domains to their WWW subdomain. Status codes: 301, 302, 307, 308.

| Action               | Method   | Endpoint                                                    |
| -------------------- | -------- | ----------------------------------------------------------- |
| List apex redirects  | `GET`    | `/service/{service_id}/version/{version_id}/apex-redirects` |
| Create apex redirect | `POST`   | `/service/{service_id}/version/{version_id}/apex-redirects` |
| Get apex redirect    | `GET`    | `/apex-redirects/{apex_redirect_id}`                        |
| Update apex redirect | `PUT`    | `/apex-redirects/{apex_redirect_id}`                        |
| Delete apex redirect | `DELETE` | `/apex-redirects/{apex_redirect_id}`                        |

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                          | URL                                                                                                                                            |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| VCL snippets guide                              | `https://www.fastly.com/documentation/guides/full-site-delivery/vcl/mixing-and-matching-fastly-vcl-with-custom-vcl/using-regular-vcl-snippets` |
| Dynamic snippets guide                          | `https://www.fastly.com/documentation/guides/full-site-delivery/vcl/mixing-and-matching-fastly-vcl-with-custom-vcl/using-dynamic-vcl-snippets` |
| Edge dictionaries guide                         | `https://www.fastly.com/documentation/guides/full-site-delivery/vcl/edge-dictionaries`                                                         |
| VCL reference                                   | `https://www.fastly.com/documentation/reference/vcl`                                                                                           |
| Cache freshness concept                         | `https://www.fastly.com/documentation/guides/concepts/cache/cache-freshness`                                                                   |
| Stale content concept                           | `https://www.fastly.com/documentation/guides/concepts/cache/stale`                                                                             |
| Compression concept                             | `https://www.fastly.com/documentation/guides/concepts/compression`                                                                             |
| Request collapsing, waiting lists, hit-for-pass | `https://www.fastly.com/documentation/guides/concepts/cache/request-collapsing`                                                                |
| VCL snippets guide                              | `https://www.fastly.com/documentation/guides/full-site-delivery/fastly-vcl/vcl-snippets`                                                       |
| Conditions guide                                | `https://www.fastly.com/documentation/guides/full-site-delivery/conditions`                                                                    |
| Caching best practices, TTL tuning              | `https://www.fastly.com/documentation/guides/full-site-delivery/caching`                                                                       |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

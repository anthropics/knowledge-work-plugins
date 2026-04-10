# Fastly Compute

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/guides/compute

## Key Concepts

**Compute languages.** Fastly Compute supports Rust, JavaScript/TypeScript, and Go. Any language that compiles to WebAssembly (WASM) can also be used.

**Package upload workflow.** Build your application locally (e.g., `fastly compute build`), which produces a `.tar.gz` package. Upload it via `PUT /service/{service_id}/version/{version_id}/package`, then activate the service version.

**Cache APIs.** Compute services access Fastly's cache through three APIs with increasing control: Simple Cache (basic get/set), HTTP Cache (HTTP-semantics-aware caching), and Core Cache (full low-level control over cache transactions).

**Resource linking.** Stores (Config, KV, Secret) must be linked to a service before the Compute code can access them. Link via `fastly service resource-link create` CLI command or the resource linking API.

**Client-side encryption for secrets.** For additional security, secrets can be encrypted locally before upload using a client key (X25519 public key from the API) and libsodium sealed boxes.

## Package Management

| Action              | Method | Endpoint                                             |
| ------------------- | ------ | ---------------------------------------------------- |
| Get package details | `GET`  | `/service/{service_id}/version/{version_id}/package` |
| Upload package      | `PUT`  | `/service/{service_id}/version/{version_id}/package` |

Upload is `multipart/form-data` with a `package` field containing the `.tar.gz` binary. Use `Expect: 100-continue` header to catch errors before the full upload completes.

## Config Stores

| Action               | Method   | Endpoint                                                                  |
| -------------------- | -------- | ------------------------------------------------------------------------- |
| List config stores   | `GET`    | `/resources/stores/config`                                                |
| Create config store  | `POST`   | `/resources/stores/config`                                                |
| Get config store     | `GET`    | `/resources/stores/config/{config_store_id}`                              |
| Update config store  | `PUT`    | `/resources/stores/config/{config_store_id}`                              |
| Delete config store  | `DELETE` | `/resources/stores/config/{config_store_id}`                              |
| Get store metadata   | `GET`    | `/resources/stores/config/{config_store_id}/info`                         |
| List linked services | `GET`    | `/resources/stores/config/{config_store_id}/services`                     |
| List items           | `GET`    | `/resources/stores/config/{config_store_id}/items`                        |
| Create item          | `POST`   | `/resources/stores/config/{config_store_id}/item`                         |
| Get item             | `GET`    | `/resources/stores/config/{config_store_id}/item/{config_store_item_key}` |
| Upsert item          | `PUT`    | `/resources/stores/config/{config_store_id}/item/{config_store_item_key}` |
| Update item          | `PATCH`  | `/resources/stores/config/{config_store_id}/item/{config_store_item_key}` |
| Delete item          | `DELETE` | `/resources/stores/config/{config_store_id}/item/{config_store_item_key}` |
| Bulk update items    | `PATCH`  | `/resources/stores/config/{config_store_id}/items`                        |

Bulk update accepts JSON with `items` array; each entry has `op` (`create`, `update`, `upsert`, `delete`), `item_key`, and `item_value`.

## KV Stores

| Action          | Method   | Endpoint                                     |
| --------------- | -------- | -------------------------------------------- |
| List KV stores  | `GET`    | `/resources/stores/kv`                       |
| Create KV store | `POST`   | `/resources/stores/kv`                       |
| Get KV store    | `GET`    | `/resources/stores/kv/{store_id}`            |
| Update KV store | `PUT`    | `/resources/stores/kv/{store_id}`            |
| Delete KV store | `DELETE` | `/resources/stores/kv/{store_id}`            |
| List item keys  | `GET`    | `/resources/stores/kv/{store_id}/keys`       |
| Get item        | `GET`    | `/resources/stores/kv/{store_id}/keys/{key}` |
| Upsert item     | `PUT`    | `/resources/stores/kv/{store_id}/keys/{key}` |
| Delete item     | `DELETE` | `/resources/stores/kv/{store_id}/keys/{key}` |
| Batch upsert    | `PUT`    | `/resources/stores/kv/{store_id}/batch`      |

KV store creation accepts optional `location` query param (`US`, `EU`, `ASIA`, `AUS`). Item values are `application/octet-stream`. Batch upsert uses `application/x-ndjson` with Base64-encoded values. List keys supports `prefix`, `consistency` (`strong`/`eventual`), and cursor pagination.

## Secret Stores

| Action                    | Method   | Endpoint                                                    |
| ------------------------- | -------- | ----------------------------------------------------------- |
| List secret stores        | `GET`    | `/resources/stores/secret`                                  |
| Create secret store       | `POST`   | `/resources/stores/secret`                                  |
| Get secret store          | `GET`    | `/resources/stores/secret/{store_id}`                       |
| Delete secret store       | `DELETE` | `/resources/stores/secret/{store_id}`                       |
| List secrets              | `GET`    | `/resources/stores/secret/{store_id}/secrets`               |
| Create secret             | `POST`   | `/resources/stores/secret/{store_id}/secrets`               |
| Create or recreate secret | `PUT`    | `/resources/stores/secret/{store_id}/secrets`               |
| Recreate existing secret  | `PATCH`  | `/resources/stores/secret/{store_id}/secrets`               |
| Get secret metadata       | `GET`    | `/resources/stores/secret/{store_id}/secrets/{secret_name}` |
| Delete secret             | `DELETE` | `/resources/stores/secret/{store_id}/secrets/{secret_name}` |
| Create client key         | `POST`   | `/resources/stores/secret/client-key`                       |
| Get signing key           | `GET`    | `/resources/stores/secret/signing-key`                      |

Secret values must be Base64-encoded in the `secret` field. Optional `client_key` field for client-side encryption using libsodium sealed boxes. Max secret size is 64KB (before Base64 encoding).

## Object Storage Access Keys

| Action            | Method   | Endpoint                                             |
| ----------------- | -------- | ---------------------------------------------------- |
| List access keys  | `GET`    | `/resources/object-storage/access-keys`              |
| Create access key | `POST`   | `/resources/object-storage/access-keys`              |
| Get access key    | `GET`    | `/resources/object-storage/access-keys/{access_key}` |
| Delete access key | `DELETE` | `/resources/object-storage/access-keys/{access_key}` |

Permissions (immutable after creation): `read-write-admin`, `read-only-admin`, `read-write-objects`, `read-only-objects`. The `buckets` field scopes `*-objects` permissions to specific buckets.

## ACLs in Compute

| Action             | Method   | Endpoint                                  |
| ------------------ | -------- | ----------------------------------------- |
| List ACLs          | `GET`    | `/resources/acls`                         |
| Create ACL         | `POST`   | `/resources/acls`                         |
| Describe ACL       | `GET`    | `/resources/acls/{acl_id}`                |
| Delete ACL         | `DELETE` | `/resources/acls/{acl_id}`                |
| Lookup IP in ACL   | `GET`    | `/resources/acls/{acl_id}/entry/{acl_ip}` |
| List ACL entries   | `GET`    | `/resources/acls/{acl_id}/entries`        |
| Update ACL entries | `PATCH`  | `/resources/acls/{acl_id}/entries`        |

Entries use CIDR prefixes with `ALLOW` or `BLOCK` actions. Batch update supports `op` values: `create`, `update`, `delete`.

## Examples

```bash
# Upload a Compute package
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Expect: 100-continue" \
  -F "package=@./pkg/my-app.tar.gz" \
  "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/package"

# Create a KV store
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-kv-store"}' \
  "https://api.fastly.com/resources/stores/kv"

# Put an item in a KV store
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  -d 'my-value' \
  "https://api.fastly.com/resources/stores/kv/$STORE_ID/keys/my-key"

# Create a secret store and add a secret
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-secret-store"}' \
  "https://api.fastly.com/resources/stores/secret"

curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"api-key","secret":"bXktc2VjcmV0LXZhbHVl"}' \
  "https://api.fastly.com/resources/stores/secret/$STORE_ID/secrets"

# Create a config store item
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -d "item_key=feature-flag&item_value=enabled" \
  "https://api.fastly.com/resources/stores/config/$CONFIG_STORE_ID/item"
```

## Edge Data Store Decision Framework

| Criteria         | Config Store                                | KV Store                                              | Secret Store                                          |
| ---------------- | ------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| Scale            | ~500 items per store                        | Large datasets                                        | Credentials/keys                                      |
| Item size limit  | 8,000 char value                            | 25MB value                                            | 64KB value                                            |
| Read performance | Cached in all POPs, low-latency reads       | Cached per-POP on first request                       | Cached in all POPs, read only from Compute at runtime |
| Write pattern    | Infrequent updates, outside Compute         | More frequent updates, within Compute                 | Write-only via API                                    |
| TTL/expiration   | No expiration                               | Optional per-item TTL                                 | No expiration                                         |
| Consistency      | Eventually consistent                       | Eventually consistent (strong option for key listing) | Eventually consistent                                 |
| Use case         | Feature flags, routing rules, small configs | Personalization, security, list management            | API keys, tokens, certificates                        |

**All edge data stores are Compute-only.** VCL services use Edge Dictionaries for key-value storage (see `vcl-services.md`).

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                         | URL                                                                                   |
| ------------------------------ | ------------------------------------------------------------------------------------- |
| Compute product page           | `https://docs.fastly.com/products/compute`                                            |
| Edge data storage product page | `https://docs.fastly.com/products/edge-data-storage`                                  |
| Cache APIs product page        | `https://docs.fastly.com/products/cache-apis`                                         |
| Compute developer guides       | `https://www.fastly.com/documentation/guides/compute/developer-guides`                |
| KV Store guide                 | `https://www.fastly.com/documentation/guides/compute/edge-data-storage/kv-stores`     |
| Config Store guide             | `https://www.fastly.com/documentation/guides/compute/edge-data-storage/config-stores` |
| Secret Store guide             | `https://www.fastly.com/documentation/guides/compute/edge-data-storage/secret-stores` |
| Dynamic config concept         | `https://www.fastly.com/documentation/guides/concepts/dynamic-config`                 |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

# Fastly Service Management

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/services

## Key Concepts

**Version lifecycle: draft, active, locked.** Every service has numbered versions. A version starts as a draft (editable). Activating it deploys its configuration to the edge and automatically locks the previous active version. Locked versions are immutable -- objects cannot be added or edited.

**Clone-modify-activate workflow.** The standard change workflow is:

1. Clone the current active version (`PUT .../version/{v}/clone`) -- creates a new draft.
2. Modify the draft (add backends, domains, VCL, etc.).
3. Validate (`GET .../version/{v}/validate`).
4. Activate (`PUT .../version/{v}/activate`) -- deploys to production.

**Version locking.** Activation automatically locks the previously active version. Locked versions cannot be edited. To make changes to a locked version's config, clone it.

**Service types.** A service is either `vcl` (VCL-based delivery) or `wasm` (Compute). The type is set at creation and cannot be changed. VCL services invoke code at predefined subroutine points in the request-response cycle. Compute services handle the entire cycle in your own code, in any language that compiles to WebAssembly (with official support for Rust, JavaScript, and Go). Most capabilities are shared. VCL-only: clustering, load balancing, segmented caching. Compute-only: general-purpose compute, content transformation, Fanout real-time messaging, Edge Data Stores.

**Staging environment.** Test service configuration changes on a staging network before deploying to production. Stage a version via `PUT /service/{id}/version/{v}/activate/staging` and deactivate via `PUT /service/{id}/version/{v}/deactivate/staging`. Staging runs on the same type of POPs as production. Staging metrics are kept separate. Use `fastly.is_staging` (VCL) or `FASTLY_IS_STAGING` (Compute) to detect staging. Access staging via the Anycast IP address (obtained from domain list with `?include=staging_ips`). Purge staging cache using `Fastly-Purge-Environment: staging` header.

**Paused services.** Services without traffic for an extended period are automatically paused. They resume when a draft version is activated or a locked version is cloned and reactivated.

## Services API

| Action                   | Method   | Endpoint                        |
| ------------------------ | -------- | ------------------------------- |
| List services            | `GET`    | `/service`                      |
| Create service           | `POST`   | `/service`                      |
| Get service              | `GET`    | `/service/{service_id}`         |
| Get service details      | `GET`    | `/service/{service_id}/details` |
| Search by name           | `GET`    | `/service/search?name={name}`   |
| Update service           | `PUT`    | `/service/{service_id}`         |
| Delete service           | `DELETE` | `/service/{service_id}`         |
| List domains for service | `GET`    | `/service/{service_id}/domain`  |

Create request body (form-encoded): `name` (required), `type` (`vcl` or `wasm`), `comment`, `customer_id`.

List supports pagination: `?page=1&per_page=20&sort=created&direction=descend`.

```bash
# Create a VCL service
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -d "name=my-service&type=vcl" \
  "https://api.fastly.com/service"

# Search for a service by name
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/search?name=my-service"
```

## Versions API

| Action                    | Method | Endpoint                                                                   |
| ------------------------- | ------ | -------------------------------------------------------------------------- |
| List versions             | `GET`  | `/service/{service_id}/version`                                            |
| Create version            | `POST` | `/service/{service_id}/version`                                            |
| Get version               | `GET`  | `/service/{service_id}/version/{version_id}`                               |
| Update version            | `PUT`  | `/service/{service_id}/version/{version_id}`                               |
| Validate version          | `GET`  | `/service/{service_id}/version/{version_id}/validate`                      |
| Activate version          | `PUT`  | `/service/{service_id}/version/{version_id}/activate`                      |
| Activate on environment   | `PUT`  | `/service/{service_id}/version/{version_id}/activate/{environment_name}`   |
| Deactivate version        | `PUT`  | `/service/{service_id}/version/{version_id}/deactivate`                    |
| Deactivate on environment | `PUT`  | `/service/{service_id}/version/{version_id}/deactivate/{environment_name}` |
| Clone version             | `PUT`  | `/service/{service_id}/version/{version_id}/clone`                         |
| Lock version              | `PUT`  | `/service/{service_id}/version/{version_id}/lock`                          |

Environment name for activate/deactivate on environment is currently limited to `staging`.

```bash
# Clone the active version to create a new draft
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/$SERVICE_ID/version/3/clone"

# Activate a version (deploy to production)
curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/$SERVICE_ID/version/4/activate"
```

## Service Authorizations

JSON:API format (`application/vnd.api+json`). Grants limited users access to specific services.

| Action               | Method   | Endpoint                                             |
| -------------------- | -------- | ---------------------------------------------------- |
| List authorizations  | `GET`    | `/service-authorizations`                            |
| Create authorization | `POST`   | `/service-authorizations`                            |
| Show authorization   | `GET`    | `/service-authorizations/{service_authorization_id}` |
| Update authorization | `PATCH`  | `/service-authorizations/{service_authorization_id}` |
| Delete authorization | `DELETE` | `/service-authorizations/{service_authorization_id}` |
| Bulk update          | `PATCH`  | `/service-authorizations`                            |
| Bulk delete          | `DELETE` | `/service-authorizations`                            |

Permission values: `read_only`, `purge_select`, `purge_all`, `full`.

Bulk operations use content type `application/vnd.api+json; ext=bulk` and accept a `data` array.

## Domains (Versioned)

Domains are versioned resources -- they belong to a specific service version.

| Action                          | Method   | Endpoint                                                                |
| ------------------------------- | -------- | ----------------------------------------------------------------------- |
| List domains                    | `GET`    | `/service/{service_id}/version/{version_id}/domain`                     |
| Create domain                   | `POST`   | `/service/{service_id}/version/{version_id}/domain`                     |
| Get domain                      | `GET`    | `/service/{service_id}/version/{version_id}/domain/{domain_name}`       |
| Update domain                   | `PUT`    | `/service/{service_id}/version/{version_id}/domain/{domain_name}`       |
| Remove domain from a service    | `DELETE` | `/service/{service_id}/version/{version_id}/domain/{domain_name}`       |
| Validate domain DNS config      | `GET`    | `/service/{service_id}/version/{version_id}/domain/{domain_name}/check` |
| Validate all domains DNS config | `GET`    | `/service/{service_id}/version/{version_id}/domain/check_all`           |

```bash
# List domains on the active version
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/service/$SERVICE_ID/version/4/domain"
```

Domain check returns an array of `[domain_details, current_cname, is_properly_configured]`.

For test domains, use the versioned domain endpoint to add `foo.global.ssl.fastly.net` — DNS and TLS are pre-configured. This also makes `foo.freetls.fastly.net` (HTTP/2) available automatically. Do NOT use the Domain Management API (`/domain-management/v1/domains`) for test domains — it rejects `*.global.ssl.fastly.net` with a 400 error.

### Custom Domains Require TLS Setup

Adding a custom domain (e.g., `www.example.com`) to a service version is **only step 1**. For HTTPS to work, you also need:

1. **Add domain to service version** (versioned domain API above)
2. **Activate the version** to deploy the domain config to edge
3. **Create a TLS subscription or activation** linking the domain to a certificate (see `tls.md`)
4. **Configure DNS** to point the domain to Fastly (CNAME for subdomains, A records for apex)
5. **Wait for certificate issuance** (Platform TLS subscriptions take minutes after DNS propagates)

Omitting step 3 means HTTPS visitors will see TLS errors. The versioned domain and TLS subscription are independent API resources — the domain tells Fastly which service handles the hostname, while the TLS subscription/activation provides the certificate for that hostname.

## VCL Service Settings

Default settings for a VCL service version (default host, default TTL, stale-if-error, stale-if-error TTL).

| Action          | Method | Endpoint                                              |
| --------------- | ------ | ----------------------------------------------------- |
| Get settings    | `GET`  | `/service/{service_id}/version/{version_id}/settings` |
| Update settings | `PUT`  | `/service/{service_id}/version/{version_id}/settings` |

Configurable fields: `general.default_host`, `general.default_ttl`, `general.stale_if_error` (boolean), `general.stale_if_error_ttl` (seconds, default 43200).

If you override TTLs with custom VCL, the `general.default_ttl` value will not be honored.

## VCL Service Version Diff

Compare generated VCL between two versions. Version numbers can be positive (absolute) or negative (-1 = latest).

| Action            | Method | Endpoint                                                               |
| ----------------- | ------ | ---------------------------------------------------------------------- |
| Diff two versions | `GET`  | `/service/{service_id}/diff/from/{from_version_id}/to/{to_version_id}` |

Query parameter `format`: `text` (default), `html`, `html_simple`.

Response fields: `from`, `to`, `format`, `diff`. Returns the full config if versions are identical.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                     | URL                                                                                         |
| ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Services API reference                     | `https://www.fastly.com/documentation/reference/api/services/service`                       |
| Versions API reference                     | `https://www.fastly.com/documentation/reference/api/services/version`                       |
| Service authorizations reference           | `https://www.fastly.com/documentation/reference/api/account/service-authorization`          |
| Concepts -- services                       | `https://www.fastly.com/documentation/guides/concepts/services`                             |
| Service setup, versions, activation guides | `https://www.fastly.com/documentation/guides/getting-started/services`                      |
| Staging environment setup and testing      | `https://www.fastly.com/documentation/guides/getting-started/services/working-with-staging` |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

# Fastly TLS Configuration

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Content-Type: `application/vnd.api+json` | Docs: https://www.fastly.com/documentation/reference/api/tls

Three approaches: **Platform TLS** (managed certs via Certainly/Let's Encrypt/GlobalSign), **Custom TLS** (upload your own certs), **Bulk/Platform TLS Certificates** (upload certs at scale with auto-activation).

## Platform TLS Subscriptions

| Action              | Method   | Endpoint                                   |
| ------------------- | -------- | ------------------------------------------ |
| List subscriptions  | `GET`    | `/tls/subscriptions`                       |
| Create subscription | `POST`   | `/tls/subscriptions`                       |
| Get subscription    | `GET`    | `/tls/subscriptions/{tls_subscription_id}` |
| Update subscription | `PATCH`  | `/tls/subscriptions/{tls_subscription_id}` |
| Delete subscription | `DELETE` | `/tls/subscriptions/{tls_subscription_id}` |

Subscription states: `pending` -> `processing` -> `issued`. Renewals: `issued` -> `renewing` -> `issued`. Failures: any state -> `failed`.

| State        | Meaning                        | Action                                         |
| ------------ | ------------------------------ | ---------------------------------------------- |
| `pending`    | Awaiting DNS challenge records | Configure DNS, then wait                       |
| `processing` | DNS validated, CA issuing cert | Wait (typically 1-5 minutes)                   |
| `issued`     | Certificate live and active    | Done                                           |
| `renewing`   | Auto-renewal in progress       | No action needed                               |
| `failed`     | Issuance failed                | Check warnings, fix, PATCH with `state: retry` |

Authorization states (in `tls_authorizations`): `blocked` (DNS not configured or CAA conflict) -> challenge validated -> cert issued. Check `included[].attributes.warnings` for details on `blocked` state.

Certificate authorities: `certainly`, `lets-encrypt`, `globalsign`. Migrate between CAs via PATCH `certificate_authority`; to migrate from 'globalsign' to 'certainly', contact Fastly Support. To retry a `failed` subscription, PATCH with `state: retry`.

**CAA record verification.** Before choosing a CA, check the domain's CAA records with `dig CAA example.com +short`. If a CAA record restricts issuance (e.g., `0 issue "letsencrypt.org"`), the subscription's CA must match. Using a different CA (e.g., `certainly`) will result in a `blocked` authorization with warning `"Found conflicting CAA record(s)"`. If no CAA records exist, any CA works.

| CA             | Required CAA `issue` value |
| -------------- | -------------------------- |
| `lets-encrypt` | `letsencrypt.org`          |
| `certainly`    | `certainly.com`            |
| `globalsign`   | `globalsign.com`           |

List filters: `filter[state]`, `filter[tls_domains.id]`, `filter[has_active_order]`, `filter[certificate_authority]`. Include: `tls_authorizations` (required to get DNS challenge records), `tls_certificates`.

Delete requires no domains in TLS-enabled state. Use `force=true` query param on PATCH or DELETE with active domains (may break TLS).

```bash
# Create a Platform TLS subscription
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data":{"type":"tls_subscription","attributes":{"certificate_authority":"certainly"},"relationships":{"tls_domains":{"data":[{"type":"tls_domain","id":"www.example.com"}]},"tls_configuration":{"data":{"type":"tls_configuration","id":"CONFIG_ID"}}}}}' \
  "https://api.fastly.com/tls/subscriptions"

# Check subscription status (include authorization challenges)
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/tls/subscriptions/{tls_subscription_id}?include=tls_authorizations"

# Retry a failed subscription
curl -X PATCH -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data":{"type":"tls_subscription","attributes":{"state":"retry"}}}' \
  "https://api.fastly.com/tls/subscriptions/{tls_subscription_id}"
```

## Custom TLS Certificates

| Action             | Method   | Endpoint                                      |
| ------------------ | -------- | --------------------------------------------- |
| List certificates  | `GET`    | `/tls/certificates`                           |
| Create certificate | `POST`   | `/tls/certificates`                           |
| Get certificate    | `GET`    | `/tls/certificates/{tls_certificate_id}`      |
| Update certificate | `PATCH`  | `/tls/certificates/{tls_certificate_id}`      |
| Delete certificate | `DELETE` | `/tls/certificates/{tls_certificate_id}`      |
| Get cert blob (LA) | `GET`    | `/tls/certificates/{tls_certificate_id}/blob` |

Upload requires PEM-formatted `cert_blob`. Update (replace) requires the new cert to contain all existing SAN entries (superset OK). Cannot delete a cert that is active for a domain.

## TLS Private Keys

| Action     | Method   | Endpoint                                 |
| ---------- | -------- | ---------------------------------------- |
| List keys  | `GET`    | `/tls/private_keys`                      |
| Create key | `POST`   | `/tls/private_keys`                      |
| Get key    | `GET`    | `/tls/private_keys/{tls_private_key_id}` |
| Delete key | `DELETE` | `/tls/private_keys/{tls_private_key_id}` |

PEM-formatted via `key` attribute (write-only, never returned). Response includes `key_type`, `key_length`, `public_key_sha1`. Filter unused keys: `filter[in_use]=false`. Cannot delete a key matched to any certificate.

## TLS Activations

| Action                | Method   | Endpoint                               |
| --------------------- | -------- | -------------------------------------- |
| List activations      | `GET`    | `/tls/activations`                     |
| Enable TLS for domain | `POST`   | `/tls/activations`                     |
| Get activation        | `GET`    | `/tls/activations/{tls_activation_id}` |
| Update certificate    | `PATCH`  | `/tls/activations/{tls_activation_id}` |
| Disable TLS           | `DELETE` | `/tls/activations/{tls_activation_id}` |

Create links three resources via `relationships`: a `tls_certificate`, a `tls_configuration`, and a `tls_domain`. Filters: `filter[tls_certificate.id]`, `filter[tls_configuration.id]`, `filter[tls_domain.id]`. Include: `tls_certificate`, `tls_configuration`, `tls_domain`.

```bash
# Upload a custom cert (key must already exist)
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data":{"type":"tls_certificate","attributes":{"cert_blob":"-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----","name":"My cert"}}}' \
  "https://api.fastly.com/tls/certificates"

# Activate TLS on a domain with a custom cert
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data":{"type":"tls_activation","relationships":{"tls_certificate":{"data":{"id":"CERT_ID","type":"tls_certificate"}},"tls_configuration":{"data":{"id":"CONFIG_ID","type":"tls_configuration"}},"tls_domain":{"data":{"id":"www.example.com","type":"tls_domain"}}}}}' \
  "https://api.fastly.com/tls/activations"
```

## TLS Configurations

| Action               | Method  | Endpoint                                     |
| -------------------- | ------- | -------------------------------------------- |
| List configurations  | `GET`   | `/tls/configurations`                        |
| Get configuration    | `GET`   | `/tls/configurations/{tls_configuration_id}` |
| Update configuration | `PATCH` | `/tls/configurations/{tls_configuration_id}` |

Configurations apply to sets of IP pools and define HTTP protocols, TLS protocol versions, and the `bulk` flag for Platform TLS. **Always include `dns_records`** to get A/AAAA/CNAME records needed for DNS setup. Filter: `filter[bulk]`.

Typical configurations available on most accounts (IDs vary per account):

| Name                   | HTTP Protocols           | TLS Protocols | Best For                            |
| ---------------------- | ------------------------ | ------------- | ----------------------------------- |
| TLS v1.3               | http/1.1, http/2         | 1.2, 1.3      | Standard setup (usually default)    |
| TLS v1.3+0RTT          | http/1.1, http/2         | 1.2, 1.3+0RTT | Lower latency (idempotent requests) |
| HTTP/3 & TLS v1.3      | http/1.1, http/2, http/3 | 1.2, 1.3      | Modern clients, best performance    |
| HTTP/3 & TLS v1.3+0RTT | http/1.1, http/2, http/3 | 1.2, 1.3+0RTT | Maximum performance                 |

0-RTT (early data) improves latency but has replay risk for non-idempotent requests. HTTP/3 uses QUIC for better mobile/lossy-network performance. List your account's configs with `GET /tls/configurations`.

```bash
# Get config with DNS records for domain setup
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/tls/configurations/{tls_configuration_id}?include=dns_records"
# Response includes A records (for apex) and CNAME target (for subdomains)
```

## TLS Domains

| Action       | Method | Endpoint       |
| ------------ | ------ | -------------- |
| List domains | `GET`  | `/tls/domains` |

Read-only view of all domains across certificates and subscriptions. Filters: `filter[in_use]`, `filter[tls_certificates.id]`, `filter[tls_subscriptions.id]`. Include: `tls_activations`, `tls_certificates`, `tls_subscriptions`.

```bash
# Check domain TLS status
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/tls/domains?filter[in_use]=true&include=tls_activations,tls_subscriptions"
```

## Mutual TLS

| Action                 | Method   | Endpoint                                                                           |
| ---------------------- | -------- | ---------------------------------------------------------------------------------- |
| List authentications   | `GET`    | `/tls/mutual_authentications`                                                      |
| Create authentication  | `POST`   | `/tls/mutual_authentications`                                                      |
| Get authentication     | `GET`    | `/tls/mutual_authentications/{mutual_authentication_id}`                           |
| Update authentication  | `PATCH`  | `/tls/mutual_authentications/{mutual_authentication_id}`                           |
| Delete authentication  | `DELETE` | `/tls/mutual_authentications/{mutual_authentication_id}`                           |
| Set mTLS on activation | `PATCH`  | `/tls/activations/{tls_activation_id}` (with `mutual_authentication` relationship) |

Upload a PEM-formatted CA `cert_bundle` for client certificate validation. `enforced: true` (default) fails closed; `enforced: false` fails open. Attach to a TLS activation by PATCHing the activation with a `mutual_authentication` relationship. Pass `null` ID to detach.

Requires existing server-side TLS (custom cert activation or Platform TLS subscription).

## Bulk Certificates (Platform TLS)

| Action           | Method   | Endpoint                                  |
| ---------------- | -------- | ----------------------------------------- |
| List bulk certs  | `GET`    | `/tls/bulk/certificates`                  |
| Upload bulk cert | `POST`   | `/tls/bulk/certificates`                  |
| Get bulk cert    | `GET`    | `/tls/bulk/certificates/{certificate_id}` |
| Update bulk cert | `PATCH`  | `/tls/bulk/certificates/{certificate_id}` |
| Delete bulk cert | `DELETE` | `/tls/bulk/certificates/{certificate_id}` |

Requires both `cert_blob` and `intermediates_blob` (separate from Custom TLS which uses a single blob). Uploading automatically enables TLS for all SAN domains. Must associate with a `tls_configuration` (bulk type). Deployment averages 60 seconds, may take up to 1 hour.

## Certificate Signing Requests

| Action     | Method | Endpoint                            |
| ---------- | ------ | ----------------------------------- |
| Create CSR | `POST` | `/tls/certificate_signing_requests` |

Generates a CSR with specified SANs. Key types: `RSA2048`, `ECDSA256`. Optionally reference an existing `tls_private_key`; otherwise Fastly generates one. Cannot specify both `key_type` and `tls_private_key`.

## How It Works

**Platform TLS**: Create subscription with domain(s) -> Fastly returns DNS challenges -> configure DNS -> DNS records are checked and Fastly procures cert -> auto-renews provided DNS is maintained. Challenge types: `managed-dns` (CNAME for ACME challenge), `managed-http-cname` (CNAME to Fastly), `managed-http-a` (A records for apex).
**Custom TLS**: Upload private key -> upload certificate -> create TLS activation linking cert + config + domain. You manage renewal.

**Bulk/Platform TLS Certificates**: Upload cert + intermediates -> Fastly auto-activates all SAN domains. Most specific hostname wins if certs overlap. You manage procurement and renewal.

**DNS setup**: Subdomains/wildcards use CNAME to the CNAME target from the configuration's `dns_records`. Apex domains use A records (AAAA for IPv6). Get the correct records from `GET /tls/configurations/{id}?include=dns_records`.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                  | URL                                                                                                                      |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| TLS product overview and prerequisites  | `https://docs.fastly.com/products/tls-service-options`                                                                   |
| TLS subscriptions API reference         | `https://www.fastly.com/documentation/reference/api/tls/subs`                                                            |
| Custom certificates API reference       | `https://www.fastly.com/documentation/reference/api/tls/custom-certs/certificates`                                       |
| TLS activations API reference           | `https://www.fastly.com/documentation/reference/api/tls/custom-certs/activations`                                        |
| Private keys API reference              | `https://www.fastly.com/documentation/reference/api/tls/custom-certs/private-keys`                                       |
| Bulk certificates API reference         | `https://www.fastly.com/documentation/reference/api/tls/platform`                                                        |
| Mutual TLS authentication API reference | `https://www.fastly.com/documentation/reference/api/tls/mutual-tls/authentication`                                       |
| TLS security guides overview            | `https://www.fastly.com/documentation/guides/security/tls`                                                               |
| TLS prerequisites and limitations       | `https://www.fastly.com/documentation/guides/getting-started/domains/securing-domains/tls-prerequisites-and-limitations` |
| TLS dashboard overview                  | `https://www.fastly.com/documentation/guides/getting-started/domains/securing-domains/about-the-tls-dashboard`           |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

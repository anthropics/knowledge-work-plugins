# Fastly Domains & Networking

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/services/domain

## Key Concepts

**Domain Management API vs. versioned domains.** The Domain Management API (`/domain-management/v1/`) is the newer approach -- domains are service-agnostic top-level objects identified by UUID, optionally linked to a service via `service_id`. Versioned domains (`/service/{id}/version/{v}/domain`) are the legacy approach where domains belong to a specific service version and follow the clone-modify-activate workflow. The versioned domain endpoints are documented in the `service-management` reference.

**Domain ownership verification.** Ownership is proven by obtaining a Fastly-managed TLS certificate for the domain, or by providing a publicly-trusted CA certificate that covers the domain (or a matching wildcard). Ownership records have an expiration date. Verification appears as the `verified` flag on Domain Management objects.

**CNAME vs. A records for routing traffic to Fastly.** Subdomains (e.g., `www.example.com`) use a CNAME record pointing to a Fastly-provided hostname (typically ending in `.fastly.net` or `.customer.fastly.net` for SPP). CNAME routing enables smart routing via Fastly Insights for optimal POP selection. Apex/root domains (e.g., `example.com`) cannot use CNAME records per RFC 1034 -- they require anycast A records pointing to Fastly IP addresses, which use standard BGP routing to reach a nearby POP. Fastly recommends against DNS providers' ALIAS/ANAME records for apex domains because they may degrade performance.

**Routing traffic to Fastly.** After configuring a domain on a Fastly service, update your DNS records to point to Fastly. Until DNS is properly configured, Fastly cannot serve traffic for that domain. Incoming requests are routed to the correct service based on the Host header matching a configured domain. The versioned domain check endpoints (`/check` and `/check_all`) verify whether DNS is correctly pointed.

**Test domains with shared TLS.** For quick testing without DNS or TLS setup, add a versioned domain like `my-name.global.ssl.fastly.net` to your service. DNS for `*.global.ssl.fastly.net` already points to Fastly edge IPs and uses a shared TLS certificate. Adding `foo.global.ssl.fastly.net` automatically makes `foo.freetls.fastly.net` available with HTTP/2. Use the versioned domain API (`/service/{id}/version/{v}/domain`) or the CLI command `fastly service domain create` — the versionless Domain Management API (`fastly domain create`) rejects these domains with a 400 error.

**Billing zones.** TLS configurations expose a maximum billing zone (MBZ) controlling which POPs serve traffic, because IP transit costs vary by region. **MBZ100**: North America, Hawaii, and Europe only (lowest egress cost). **MBZ200**: all POPs except Africa, India, and South Korea. **Global**: all POPs worldwide. The billing zone is a property of the DNS name associated with a TLS configuration, not the TLS configuration itself.

**Wildcard domains.** Attaching a wildcard domain (e.g., `*.example.com`) to a service causes any hostname matching the pattern to be handled by that service. This can be combined with `req.http.host` inspection in VCL or Compute to differentiate behavior per hostname.

**Dedicated IPs and service pinning.** For hosting services with thousands of domains, dedicated Fastly IP addresses can be pinned to a single service. All requests arriving on those IPs invoke the service regardless of `Host` header. Requires Fastly provisioning. A valid TLS certificate covering each domain is still required.

**DNS zones are secondary-only.** Fastly DNS zones currently support only the `secondary` type -- Fastly acts as a secondary DNS server, receiving zone transfers from your primary DNS server via AXFR. TSIG keys secure these transfers. After creating a zone, configure your primary DNS server to allow transfers to the nameservers and NOTIFY IP addresses returned in the zone response.

## Domain Management API

The newer, service-agnostic Domain Management API. Domains are top-level objects identified by UUID, optionally associated with a service.

| Action        | Method   | Endpoint                                    |
| ------------- | -------- | ------------------------------------------- |
| List domains  | `GET`    | `/domain-management/v1/domains`             |
| Create domain | `POST`   | `/domain-management/v1/domains`             |
| Get domain    | `GET`    | `/domain-management/v1/domains/{domain_id}` |
| Update domain | `PATCH`  | `/domain-management/v1/domains/{domain_id}` |
| Delete domain | `DELETE` | `/domain-management/v1/domains/{domain_id}` |

Create request body (JSON): `fqdn` (required, immutable after creation), `service_id` (optional, nullable), `description` (optional).

Update request body (JSON): `service_id` (nullable -- set to `null` to disassociate from service), `description`.

List supports query parameters: `fqdn` (fuzzy match), `service_id`, `activated` (boolean), `verified` (boolean), `sort` (`fqdn` or `-fqdn`), `cursor`, `limit` (default 20, max 100).

Response fields: `id` (UUID), `fqdn`, `service_id`, `description`, `activated` (read-only, true if domain has at least one TLS activation), `verified` (read-only, true if ownership is proven via TLS certificate), `created_at`, `updated_at`.

```bash
# Create a domain and associate it with a service
curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fqdn":"www.example.com","service_id":"SU1Z0isxPaozGVKXdv0eY"}' \
  "https://api.fastly.com/domain-management/v1/domains"

# List domains filtered by service
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/domain-management/v1/domains?service_id=SU1Z0isxPaozGVKXdv0eY"
```

## End-to-End: Custom Domain with TLS

Complete workflow for making a Fastly service accessible at a custom domain (e.g., `www.example.com`) with HTTPS. This involves three systems: the Fastly service (versioned domain), the Fastly TLS API (certificate), and your DNS provider (records).

### Pre-flight

```bash
# 1. Check CAA records — determines which CA to use for TLS subscription
dig CAA example.com +short
# If "0 issue letsencrypt.org" -> use lets-encrypt
# If "0 issue certainly.com" -> use certainly
# If no CAA records -> any CA works

# 2. Pick a TLS configuration (get IDs and DNS records)
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/tls/configurations?include=dns_records"
# Note the config ID and the CNAME target (e.g., m.sni.global.fastly.net)
```

### Steps

1. **Add domain to service version** (versioned domain API):

   ```bash
   # If the active version is locked, clone it first
   curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
     "https://api.fastly.com/service/$SERVICE_ID/version/$ACTIVE_VERSION/clone"
   # Add domain to the new version
   curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
     -d "name=www.example.com" \
     "https://api.fastly.com/service/$SERVICE_ID/version/$NEW_VERSION/domain"
   ```

2. **Activate the version**:

   ```bash
   curl -X PUT -H "Fastly-Key: $FASTLY_API_TOKEN" \
     "https://api.fastly.com/service/$SERVICE_ID/version/$NEW_VERSION/activate"
   ```

3. **Create TLS subscription** (choose CA based on CAA records):

   ```bash
   curl -X POST -H "Fastly-Key: $FASTLY_API_TOKEN" \
     -H "Content-Type: application/vnd.api+json" \
     -d '{"data":{"type":"tls_subscription","attributes":{"certificate_authority":"lets-encrypt"},"relationships":{"tls_domains":{"data":[{"type":"tls_domain","id":"www.example.com"}]},"tls_configuration":{"data":{"type":"tls_configuration","id":"CONFIG_ID"}}}}}' \
     "https://api.fastly.com/tls/subscriptions"
   ```

4. **Get DNS challenge records** (must use `?include=tls_authorizations`):

   ```bash
   curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
     "https://api.fastly.com/tls/subscriptions/$SUBSCRIPTION_ID?include=tls_authorizations"
   ```

   Look in `included[].attributes.challenges` for the records to create. Also check `included[].attributes.warnings` for issues (e.g., CAA conflicts).

5. **Configure DNS** (at your DNS provider):

   - **ACME challenge**: `_acme-challenge.www.example.com` CNAME to the value from step 4 (e.g., `xyz.fastly-validations.com`)
   - **Traffic routing**: `www.example.com` CNAME to `m.sni.global.fastly.net` (from TLS config's `dns_records`)
   - For apex domains: use A records instead of CNAME (get IPs from TLS config's `dns_records`)

6. **Wait for certificate issuance** (typically 1-5 minutes after DNS propagates):

   ```bash
   # Poll until state is "issued"
   curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
     "https://api.fastly.com/tls/subscriptions/$SUBSCRIPTION_ID"
   # States: pending -> processing -> issued
   ```

7. **Verify**:

   ```bash
   curl -sI https://www.example.com/
   # Should return HTTP/2 200 with x-served-by: cache-*
   ```

## Domain Ownership

Domain ownership records confirm that a customer has validated control over a domain. Ownership is established by obtaining a Fastly-managed TLS certificate or providing a publicly-trusted CA certificate that covers the domain (or a matching wildcard).

| Action                 | Method | Endpoint             |
| ---------------------- | ------ | -------------------- |
| List domain ownerships | `GET`  | `/domain-ownerships` |

Response format: `application/vnd.api+json` (JSON:API). Each record includes `id` (the domain FQDN), `type` (`domain_ownership`), and attributes: `expires_at`, `created_at`, `updated_at`.

Pagination via `page[number]` and `page[size]` (default 100). Response includes `links` (self, first, prev, next, last) and `meta` (per_page, current_page, record_count, total_pages).

```bash
# List domain ownership records
curl -H "Fastly-Key: $FASTLY_API_TOKEN" \
  "https://api.fastly.com/domain-ownerships"
```

## DNS Zones (Beta)

Fastly DNS zones for managing DNS namespace segments. Currently supports secondary zones only -- Fastly acts as a secondary DNS server receiving zone transfers from your primary.

| Action      | Method   | Endpoint                  |
| ----------- | -------- | ------------------------- |
| List zones  | `GET`    | `/dns/v1/zones`           |
| Create zone | `POST`   | `/dns/v1/zones`           |
| Get zone    | `GET`    | `/dns/v1/zones/{zone_id}` |
| Update zone | `PATCH`  | `/dns/v1/zones/{zone_id}` |
| Delete zone | `DELETE` | `/dns/v1/zones/{zone_id}` |

Create request body (JSON): `name` (required, domain name), `type` (required, currently only `secondary`), `description` (optional, nullable), `xfr_config_inbound` (optional, with `primaries` array of `{address, description}` objects and `inbound_tsig_key_id`).

Update request body (JSON): `description` (nullable), `xfr_config_inbound`.

List supports query parameters: `name` (filter by partial match), `sort` (`name`, `-name`, `created_at`, `-created_at`), `cursor`, `limit` (default 10, max 100).

Response fields (full): `id` (UUID), `name`, `description`, `type`, `serial` (SOA serial number), `nameservers` (array of assigned nameserver hostnames), `xfr_config_inbound` (includes `primaries`, `notify_ip_addresses` with `ipv4` array, and `inbound_tsig_key_id`), `created_at`, `updated_at`.

## DNS TSIG Keys (Beta)

TSIG (Transaction Signature) keys are shared credentials used to secure zone transfers between DNS servers. Referenced by DNS zones via `inbound_tsig_key_id`.

| Action          | Method   | Endpoint                          |
| --------------- | -------- | --------------------------------- |
| List TSIG keys  | `GET`    | `/dns/v1/tsig-keys`               |
| Create TSIG key | `POST`   | `/dns/v1/tsig-keys`               |
| Get TSIG key    | `GET`    | `/dns/v1/tsig-keys/{tsig_key_id}` |
| Update TSIG key | `PATCH`  | `/dns/v1/tsig-keys/{tsig_key_id}` |
| Delete TSIG key | `DELETE` | `/dns/v1/tsig-keys/{tsig_key_id}` |

Create request body (JSON): `name` (required), `algorithm` (required: `hmac-sha224`, `hmac-sha256`, `hmac-sha384`, or `hmac-sha512`), `secret` (required, Base64-encoded), `description` (optional, nullable).

Update request body (JSON): any combination of `name`, `description`, `algorithm`, `secret`.

List supports: `name` (filter), `sort` (`name`, `-name`, `created_at`, `-created_at`), `cursor`, `limit` (default 10, max 100).

Delete returns 409 Conflict if the key is still in use by a zone. Name conflicts on create also return 409.

## SPP / IP Configuration (Limited Availability)

Service Platform Provisioning (SPP) endpoints for customers with Subscriber Provided Prefix (BYOIP). These manage DNS and TLS configurations associated with customer-owned IP address pools.

### SPP DNS Configuration

Associates an FQDN with a TLS configuration (IP pool). The `name` attribute must be a valid FQDN ending with `.customer.fastly.net`.

| Action            | Method   | Endpoint                                     |
| ----------------- | -------- | -------------------------------------------- |
| List DNS configs  | `GET`    | `/dns/configurations`                        |
| Create DNS config | `POST`   | `/dns/configurations`                        |
| Get DNS config    | `GET`    | `/dns/configurations/{dns_configuration_id}` |
| Update DNS config | `PATCH`  | `/dns/configurations/{dns_configuration_id}` |
| Delete DNS config | `DELETE` | `/dns/configurations/{dns_configuration_id}` |

Request/response format: `application/vnd.api+json` (JSON:API). Attributes: `name` (FQDN, must end with `.customer.fastly.net`), `dualstack` (boolean, default false -- true enables IPv6 alongside IPv4), `region` (read-only, always `global`).

Relationship: `tls_configuration` -- the TLS configuration (IP pool) this DNS config is associated with.

### SPP TLS Configuration

Manages TLS configurations representing access to IP pools, with configurable protocol and cipher settings.

| Action            | Method   | Endpoint                                     |
| ----------------- | -------- | -------------------------------------------- |
| List TLS configs  | `GET`    | `/tls/configurations`                        |
| Create TLS config | `POST`   | `/tls/configurations`                        |
| Get TLS config    | `GET`    | `/tls/configurations/{tls_configuration_id}` |
| Update TLS config | `PATCH`  | `/tls/configurations/{tls_configuration_id}` |
| Delete TLS config | `DELETE` | `/tls/configurations/{tls_configuration_id}` |

Request/response format: `application/vnd.api+json` (JSON:API). Attributes: `name`, `http_protocols` (array -- `http/1.1` required, `http/2` and `http/3` optional), `tls_protocols` (array, e.g. `["1.2", "1.3"]`), `tls_1_2_cipher_suite_profile` (advanced, requires Fastly Support enablement), `vipspace` (must be `customer_assigned_vipspace`).

List supports: `filter[bulk]`, `include=dns_records`, `page[number]`, `page[size]`.

Relationships: `dns_records`, `service`, `default_certificate`, `default_ecdsa_certificate`.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                          | URL                                                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Routing traffic to Fastly concept               | `https://www.fastly.com/documentation/guides/concepts/routing-traffic-to-fastly`           |
| Domain management guide                         | `https://www.fastly.com/documentation/guides/full-site-delivery/domains`                   |
| Domain API reference                            | `https://www.fastly.com/documentation/reference/api/services/domain`                       |
| Domain ownerships API reference                 | `https://www.fastly.com/documentation/reference/api/services/domain-ownerships`            |
| Domain setup, DNS records, domain management UI | `https://www.fastly.com/documentation/guides/getting-started/domains/working-with-domains` |
| Fastly DNS (secondary zones)                    | `https://www.fastly.com/documentation/guides/platform/fastly-dns`                          |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

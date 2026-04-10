# Fastly Service Management

Manage Fastly CDN services and their configurations.

## Choosing a Service Type

| Type    | Flag                   | Best for                                                                            |
| ------- | ---------------------- | ----------------------------------------------------------------------------------- |
| VCL     | `--type vcl` (default) | Caching proxies, CDN configs, header manipulation. No build step, no runtime costs. |
| Compute | `--type wasm`          | Custom logic in Rust/JS/Go at the edge. Requires build and has per-request costs.   |

For tasks like "create a caching frontend" or "set up a reverse proxy," always use VCL.

## JSON Output Field Names

**IMPORTANT**: When using `--json` with Fastly CLI commands, field names are **PascalCase**, not lowercase. Common fields:

| JSON field      | Example value              |
| --------------- | -------------------------- |
| `Name`          | `"my-service"`             |
| `ServiceID`     | `"5qNP5VBgxNzTm24XcYLW4j"` |
| `ActiveVersion` | `3`                        |
| `Type`          | `"vcl"`                    |
| `Comment`       | `"Production service"`     |
| `CreatedAt`     | `"2025-01-15T10:30:00Z"`   |

Use `.Name` (not `.name`) in jq filters:
```bash
# Correct
fastly service list --json | jq -r '.[] | select(.Name=="my-service") | .ServiceID'

# WRONG — returns nothing
fastly service list --json | jq -r '.[] | select(.name=="my-service") | .id'
```

## Service CRUD Operations

```bash
fastly service list
fastly service create --name "My Service"
fastly service create --name "My Service" --type wasm
fastly service describe --service-id SERVICE_ID
fastly service search --name "production"
fastly service update --service-id SERVICE_ID --name "New Name" --comment "Updated"
fastly service delete --service-id SERVICE_ID
```

## Service Versions

Every service has versions. Only one version can be active at a time. Active versions are automatically locked and cannot be modified — you must clone them first.

**New services start with version 1, which is unlocked.** Configure everything (domain, backend, snippets) on version 1 using `--version 1`, then activate once. Do NOT use `--autoclone` or `--version latest` on a brand new service — `--autoclone` is only needed when modifying an already-active (locked) version, and `--version latest` combined with `--autoclone` in chained commands causes each command to clone a new version, scattering your configuration across multiple versions.

```bash
fastly service version list --service-id SERVICE_ID
fastly service version clone --service-id SERVICE_ID --version 1
fastly service version activate --service-id SERVICE_ID --version 2
fastly service version deactivate --service-id SERVICE_ID --version 2
fastly service version lock --service-id SERVICE_ID --version 2
fastly service version update --service-id SERVICE_ID --version 2 --comment "Production release"
fastly service version stage --version=VERSION --service-id SERVICE_ID
fastly service version unstage --version=VERSION --service-id SERVICE_ID
```

To modify a live service: clone the active version, make changes on the new version, validate, then activate. Many CLI commands accept `--autoclone` to do this automatically.

Via the REST API, clone with:

```bash
curl -s -X PUT "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/clone" \
  -H "Fastly-Key: $FASTLY_API_TOKEN"
```

## Backends (Origins)

```bash
fastly service backend list --service-id SERVICE_ID --version 1

fastly service backend create \
  --service-id SERVICE_ID \
  --version 1 \
  --name origin \
  --address origin.example.com \
  --port 443 \
  --use-ssl \
  --override-host origin.example.com \
  --ssl-cert-hostname origin.example.com \
  --ssl-sni-hostname origin.example.com

fastly service backend update \
  --service-id SERVICE_ID \
  --version 1 \
  --name origin \
  --autoclone \
  --weight 100

fastly service backend delete --service-id SERVICE_ID --version 1 --name origin
```

### Backend SSL

When connecting to HTTPS origins, use `--use-ssl` and set both `--ssl-cert-hostname` and `--ssl-sni-hostname`:

- `--use-ssl`: Enable SSL/TLS for connections to this backend
- `--ssl-cert-hostname`: Hostname used to verify the origin's TLS certificate
- `--ssl-sni-hostname`: Hostname sent in the TLS SNI extension during the handshake
- `--override-host`: Sets the Host header sent to the origin

Certificate verification (`ssl_check_cert`) is enabled by default — do not pass `--ssl-check-cert` (it's deprecated). Use `--no-ssl-check-cert` only if you need to disable verification.

All three hostnames should typically match the origin's hostname. Omitting `--ssl-sni-hostname` causes TLS handshake failures when the origin uses SNI-based certificate selection (shared hosting, CDNs, cloud load balancers).

**When the Host header differs from the origin hostname** (e.g., sending `Host: cdn.example.com` to `origin.example.com`): set `--override-host` to the desired Host header value, and set `--ssl-cert-hostname` and `--ssl-sni-hostname` to the origin's actual hostname (what its TLS certificate covers). Example:
```bash
fastly service backend create \
  --service-id SERVICE_ID --version 1 --name origin \
  --address origin.example.com --port 443 --use-ssl \
  --override-host cdn.example.com \
  --ssl-cert-hostname origin.example.com \
  --ssl-sni-hostname origin.example.com
```

#### Known-good reverse proxy recipe: Host override + HTTPS cert mismatch

Use this exact pattern when the origin answers for one `Host` header, but its TLS certificate only covers a different hostname. This is the most common source of Fastly `503 hostname doesn't match against certificate` errors.

Generic example:

- Public URL to cache: `https://cache.example.com`
- Origin address to connect to: `origin.example.net`
- `Host` header required by origin: `cache.example.com`
- Hostname covered by the origin certificate: `origin.example.net`

```bash
# Pre-flight: confirm the origin responds when sent the desired Host header.
curl -sI -H 'Host: cache.example.com' https://origin.example.net/

# Pre-flight: confirm which hostname the cert actually covers.
echo | openssl s_client -connect origin.example.net:443 -servername origin.example.net 2>/dev/null | \
  openssl x509 -noout -text | grep -A1 'Subject Alternative Name'

# Backend: connect to origin.example.net, but send Host: cache.example.com.
# TLS validation and SNI stay on origin.example.net because that is what the cert covers.
fastly service backend create \
  --service-id SERVICE_ID \
  --version 1 \
  --name origin \
  --address origin.example.net \
  --port 443 \
  --use-ssl \
  --override-host cache.example.com \
  --ssl-cert-hostname origin.example.net \
  --ssl-sni-hostname origin.example.net
```

Rule of thumb:

- `--address`: where Fastly connects
- `--override-host`: HTTP `Host` header sent to origin
- `--ssl-cert-hostname`: hostname Fastly uses for certificate validation
- `--ssl-sni-hostname`: hostname Fastly sends in TLS SNI

If the cert covers `origin.example.net` but you set either SSL hostname flag to `cache.example.com`, Fastly will return `503 hostname doesn't match against certificate`.

For simple HTTP origins that don't require TLS, omit SSL flags and use `--port 80`:

```bash
fastly service backend create \
  --service-id SERVICE_ID \
  --version 1 \
  --name origin \
  --address origin.example.com \
  --port 80 \
  --override-host origin.example.com
```

## Domains

Domains control which hostnames route to your service.

**IMPORTANT**: There are two CLI command families with similar names but completely different behavior:

- `fastly service domain create` — version-scoped, calls `/service/{id}/version/{v}/domain`. **Use this one.**
- `fastly domain create` — calls the newer `/domain-management/v1/domains` API, uses `--fqdn` instead of `--name`, and **returns 403 Forbidden** for most accounts. For test domains (`*.global.ssl.fastly.net`, `*.edgecompute.app`), it returns **400 Bad Request** with "Invalid value for fqdn". Never use it.

### Test Domains

For quick testing without DNS setup, use a subdomain of `global.ssl.fastly.net`. Any name under this wildcard resolves to Fastly edge IPs and routes through the CDN, so pick any unique name and add it to your service:

```
my-project.global.ssl.fastly.net
```

This gives you a working HTTPS URL immediately — no DNS or TLS setup needed. Do not use `*.edgecompute.app` (Compute/wasm only, rejected for VCL services).

Adding `foo.global.ssl.fastly.net` automatically makes `foo.freetls.fastly.net` available too (HTTP/2 enabled). Both URLs work for testing; `freetls.fastly.net` is preferred for HTTP/2 clients.

**WARNING**: The test domain is the name **you choose** (e.g. `my-project.global.ssl.fastly.net`), NOT the service ID. Using `SERVICE_ID.global.ssl.fastly.net` does not work — that hostname does not route to your service.

### CLI (Recommended)

Use the version-scoped `fastly service domain` commands:

```bash
fastly service domain list --service-id SERVICE_ID --version 1

fastly service domain create \
  --service-id SERVICE_ID \
  --version 1 \
  --name my-project.global.ssl.fastly.net

fastly service domain delete \
  --service-id SERVICE_ID \
  --version 1 \
  --name my-project.global.ssl.fastly.net

fastly service domain validate --version=VERSION --service-id SERVICE_ID
```

### REST API (Fallback)

Only needed if `fastly service domain create` is unavailable:

```bash
curl -s -X POST "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/domain" \
  -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-project.global.ssl.fastly.net"}'
```

To get `$FASTLY_API_TOKEN` for REST calls, prefer `FASTLY_API_TOKEN=$(fastly auth token)` inside a shell substitution or use the existing `FASTLY_API_TOKEN` environment variable directly. Only use `fastly auth show TOKEN_NAME --reveal --quiet | awk '/^Token:/ {print $2}'` when you specifically need a stored token by name; omitting the token name fails when the CLI is authenticated via `FASTLY_API_TOKEN` or another non-stored source.

## Healthchecks

```bash
fastly service healthcheck list --service-id SERVICE_ID --version 1

fastly service healthcheck create \
  --service-id SERVICE_ID \
  --version 1 \
  --name origin-health \
  --host origin.example.com \
  --path /health \
  --check-interval 30000 \
  --threshold 3

fastly service healthcheck update \
  --service-id SERVICE_ID \
  --version 1 \
  --name origin-health \
  --threshold 5

fastly service healthcheck delete --service-id SERVICE_ID --version 1 --name origin-health
```

## Cache Purging

```bash
fastly service purge --service-id SERVICE_ID --all
fastly service purge --service-id SERVICE_ID --key "product-123"
fastly service purge --service-id SERVICE_ID --url "https://www.example.com/page"
fastly service purge --service-id SERVICE_ID --key "product-123" --soft
fastly service purge --service-id SERVICE_ID --file=keys.txt
```

The `--file` flag accepts a path to a newline-delimited list of surrogate keys to purge.

## ACLs (Access Control Lists)

```bash
fastly service acl list --version=VERSION --service-id SERVICE_ID [--json]
fastly service acl create --version=VERSION --service-id SERVICE_ID [--name NAME] [--autoclone]
fastly service acl delete --name=NAME --version=VERSION --service-id SERVICE_ID [--autoclone]
fastly service acl describe --name=NAME --version=VERSION --service-id SERVICE_ID [--json]
fastly service acl update --name=NAME --new-name=NEW-NAME --version=VERSION --service-id SERVICE_ID [--autoclone]

fastly service acl-entry create \
  --service-id SERVICE_ID \
  --acl-id ACL_ID \
  --ip 192.168.1.0 \
  --subnet 24

fastly service acl-entry list --service-id SERVICE_ID --acl-id ACL_ID
fastly service acl-entry delete --service-id SERVICE_ID --acl-id ACL_ID --id ENTRY_ID
```

## Edge Dictionaries

```bash
fastly service dictionary list --version=VERSION --service-id SERVICE_ID [--json]
fastly service dictionary create --version=VERSION --service-id SERVICE_ID [--name NAME] [--autoclone] [--write-only]
fastly service dictionary delete --name=NAME --version=VERSION --service-id SERVICE_ID [--autoclone]
fastly service dictionary describe --name=NAME --version=VERSION --service-id SERVICE_ID [--json]
fastly service dictionary update --name=NAME --version=VERSION --service-id SERVICE_ID [--new-name] [--autoclone] [--write-only]

fastly service dictionary-entry create --dictionary-id=DICT_ID --key=KEY --value=VALUE --service-id SERVICE_ID
fastly service dictionary-entry delete --dictionary-id=DICT_ID --key=KEY --service-id SERVICE_ID
fastly service dictionary-entry describe --dictionary-id=DICT_ID --key=KEY --service-id SERVICE_ID
fastly service dictionary-entry list --dictionary-id=DICT_ID --service-id SERVICE_ID [--json]
fastly service dictionary-entry update --dictionary-id=DICT_ID --service-id SERVICE_ID [--file] [--id] [--key] [--value]
```

## Rate Limiting

```bash
fastly service rate-limit list --version=VERSION --service-id SERVICE_ID

fastly service rate-limit create \
  --service-id SERVICE_ID \
  --version 1 \
  --name api-limit \
  --rps-limit 100 \
  --window-size 60 \
  --action response \
  --response-status 429

fastly service rate-limit describe --id=ID [--json]
fastly service rate-limit update --id=ID --rps-limit 200
fastly service rate-limit delete --id=ID
```

## VCL Snippets

VCL snippets inject small blocks of VCL logic into your service without writing a full custom VCL file. The `type` controls where in the request lifecycle the snippet runs.

| Type      | Runs in       | Use for                                           |
| --------- | ------------- | ------------------------------------------------- |
| `recv`    | `vcl_recv`    | URL rewrites, redirects, access control           |
| `fetch`   | `vcl_fetch`   | Cache TTL overrides, response header manipulation |
| `deliver` | `vcl_deliver` | Add/remove response headers sent to clients       |
| `miss`    | `vcl_miss`    | Modify backend requests on cache miss             |
| `pass`    | `vcl_pass`    | Modify backend requests that bypass cache         |

### CLI

**Command paths**: VCL snippet and custom VCL commands live under `fastly service vcl`:

```bash
fastly service vcl custom list --service-id SERVICE_ID --version 1

fastly service vcl custom create \
  --service-id SERVICE_ID \
  --version 1 \
  --name main \
  --content "$(cat main.vcl)" \
  --main

fastly service vcl snippet create \
  --service-id SERVICE_ID \
  --version 1 \
  --name redirect-old \
  --type recv \
  --content 'if (req.url ~ "^/old") { set req.url = "/new"; }'

fastly service vcl snippet create \
  --service-id SERVICE_ID \
  --version 1 \
  --name cache-30min \
  --type fetch \
  --content 'set beresp.ttl = 1800s; set beresp.grace = 3600s;' \
  --dynamic \
  --priority 100

fastly service vcl condition list --service-id SERVICE_ID --version 1
```

**IMPORTANT — `--content` takes inline VCL, not a file path.** Passing a file path like `--content /tmp/snippet.vcl` sets the snippet content to the literal string "/tmp/snippet.vcl". To load from a file, use shell substitution: `--content "$(cat /tmp/snippet.vcl)"`.

Use `fastly service vcl snippet describe --content` to print only the raw snippet body for either versioned snippets (`--name`) or dynamic snippets (`--dynamic --snippet-id`). `--content` is mutually exclusive with `--json` and `--verbose`.

The `--dynamic` flag creates a dynamic snippet that can be updated without activating a new version. The `-p`/`--priority` flag controls the execution order of snippets (lower values run first).

### REST API

When creating snippets via the REST API, the `dynamic` field is **required**. Use `0` for regular (version-locked) snippets, `1` for dynamic snippets that can be updated without activating a new version.

```bash
curl -s -X POST "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/snippet" \
  -H "Fastly-Key: $FASTLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "cache-30min",
    "type": "fetch",
    "dynamic": 0,
    "priority": 100,
    "content": "set beresp.ttl = 1800s;\nset beresp.grace = 300s;"
  }'
```

## Service Alerts

```bash
fastly service alert list [--json] [--service-id] [--cursor] [--limit] [--name] [--order] [--sort]

fastly service alert create \
  --name "High Error Rate" \
  --description "Alert when 5xx errors exceed threshold" \
  --source stats \
  --type percent \
  --metric status_5xx \
  --threshold 5 \
  --period 5m \
  [--service-id SERVICE_ID] \
  [--dimensions] [--ignoreBelow] [--integrations] [--json]

fastly service alert describe --id=ID [--json]
fastly service alert delete --id=ID [--json]
fastly service alert history [--json] [--after] [--before] [--cursor] [--definition-id] [--limit] [--order] [--sort] [--service-id] [--status]

fastly service alert update \
  --id=ID \
  --name "High Error Rate" \
  --description "Alert when 5xx errors exceed threshold" \
  --source stats \
  --type percent \
  --metric status_5xx \
  --threshold 5 \
  --period 5m \
  [--dimensions] [--ignoreBelow] [--integrations] [--json]
```

## Resource Links

```bash
fastly service resource-link list --version=VERSION --service-id SERVICE_ID
fastly service resource-link create --resource-id=ID --version=VERSION --service-id SERVICE_ID [--name]
fastly service resource-link describe --id=ID --version=VERSION --service-id SERVICE_ID
fastly service resource-link update --id=ID --name=NAME --version=VERSION --service-id SERVICE_ID
fastly service resource-link delete --id=ID --version=VERSION --service-id SERVICE_ID
```

## Image Optimizer Defaults

```bash
fastly service imageoptimizer get --service-id SERVICE_ID --version 1

fastly service imageoptimizer update \
  --service-id SERVICE_ID \
  --version 1 \
  --jpeg-quality 85 \
  --webp auto
```

## Validating a Version

Always validate before activating when you can do so safely.

```bash
fastly service version validate --service-id SERVICE_ID --version VERSION
```

Returns validation status on success, or a list of errors explaining what's missing (e.g., no domain, no backend).

Alternatively, via the REST API:

```bash
curl -s "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/validate" \
  -H "Fastly-Key: $FASTLY_API_TOKEN"
```

## Common Workflows

### Create a Caching Proxy

Set up a VCL service that caches responses from an HTTPS origin. **Configure everything on version 1 before activating — do not use `--autoclone` or `--version latest` for new services.**

**Default caching behavior**: Fastly VCL services respect origin `Cache-Control` and `Expires` headers by default. If the origin already sends appropriate caching headers (e.g., `Cache-Control: max-age=3600`), you do not need a VCL snippet — skip the snippet step entirely. The pre-flight check (`curl -sI`) reveals these headers. Only add a VCL snippet if the origin sends no caching headers, sends `no-cache`/`no-store` when you want to cache, or you want to override the TTL.

#### Pre-flight checklist (do this BEFORE creating the service)

```bash
# 1. Verify the origin serves content with the Host header you intend to use
curl -sI -H "Host: DESIRED_HOST" https://ORIGIN_ADDRESS/
# Check for: 200 status, Cache-Control/Expires headers

# 2. Check which hostnames the origin's TLS certificate covers
echo | openssl s_client -connect ORIGIN_ADDRESS:443 -servername ORIGIN_ADDRESS 2>/dev/null | \
  openssl x509 -noout -text | grep -A1 "Subject Alternative Name"
# IMPORTANT: If DESIRED_HOST is not in the SANs, you MUST set
# --ssl-cert-hostname and --ssl-sni-hostname to ORIGIN_ADDRESS (not DESIRED_HOST)

# 3. If using a custom domain (not *.global.ssl.fastly.net), check CAA records
dig CAA DOMAIN +short
# If a CAA record exists (e.g., "0 issue letsencrypt.org"), you MUST use a
# matching --cert-auth when creating the TLS subscription later.
# See tls.md for the full custom domain + TLS workflow.
```

#### Example: Same hostname for address and Host header

```bash
# Step 1: Create the service (note: --json is NOT supported on this command)
fastly service create --name "my-proxy" --non-interactive
# Parse the service ID from "SUCCESS: Created service XXXXX"

# Step 2: Add domain, backend, and optional snippet — ALL on version 1
fastly service domain create \
  --service-id $SERVICE_ID \
  --version 1 \
  --name my-proxy.global.ssl.fastly.net

fastly service backend create \
  --service-id $SERVICE_ID \
  --version 1 \
  --name origin \
  --address origin.example.com \
  --port 443 \
  --use-ssl \
  --override-host origin.example.com \
  --ssl-cert-hostname origin.example.com \
  --ssl-sni-hostname origin.example.com

# Optional: override origin TTL (skip if origin sends good Cache-Control headers)
fastly service vcl snippet create \
  --service-id $SERVICE_ID \
  --version 1 \
  --name cache-30min \
  --type fetch \
  --content 'set beresp.ttl = 1800s; set beresp.grace = 300s;'

# Step 3: Activate once — all configuration is on version 1
fastly service version activate --service-id $SERVICE_ID --version 1
```

#### Example: Different Host header from origin address

When the origin address differs from the Host header (e.g., origin at `example.com` but you need to send `Host: cdn.example.com`), the SSL settings must match the origin's TLS certificate, NOT the Host header:

```bash
fastly service backend create \
  --service-id $SERVICE_ID \
  --version 1 \
  --name origin \
  --address example.com \
  --port 443 \
  --use-ssl \
  --override-host cdn.example.com \
  --ssl-cert-hostname example.com \
  --ssl-sni-hostname example.com
```

If `--ssl-cert-hostname` and `--ssl-sni-hostname` are omitted or set to the override-host value, Fastly will return **503 "hostname doesn't match against certificate"** because it validates the TLS cert against the wrong hostname.

#### Testing and verifying

```bash
# Wait 15-30s for propagation, then test
# Expected progression: 500 from Fastly CDN while the new domain propagates
# (normal) → 200 (working). If you see 503 instead, check backend SSL settings.

# Use GET first so you do not confuse a cached propagation error with origin health.
curl -sS -D - -o /tmp/body.txt https://my-proxy.freetls.fastly.net/ | sed -n '1,25p'

# Then confirm Fastly is honoring the origin cache headers and serving HITs.
curl -sI https://my-proxy.freetls.fastly.net/ | grep -iE "x-cache|age|cache-control|expires"
# Expected: x-cache: HIT, age: N, cache-control/expires from origin

# NOTE: HEAD requests may return a cached 500 from the propagation period even
# after the service is live. Always test with GET first on a fresh hostname.
```

### Create New Service with Backend

Configure domain and backend on version 1, then activate once:

```bash
fastly service create --name "My CDN" --non-interactive
# note the service ID from the output

fastly service domain create \
  --service-id $SERVICE_ID \
  --version 1 \
  --name my-cdn.global.ssl.fastly.net

fastly service backend create \
  --service-id $SERVICE_ID \
  --version 1 \
  --name origin \
  --address origin.example.com

fastly service version activate --service-id $SERVICE_ID --version 1
```

### Update Live Service Safely

```bash
fastly service backend update \
  --service-id SERVICE_ID \
  --version active \
  --autoclone \
  --name origin \
  --address new-origin.example.com
fastly service version activate --service-id SERVICE_ID --version latest
```

### Add Custom Domain with TLS to Existing Service

To serve traffic at a custom domain (not `*.global.ssl.fastly.net`), you need both a domain on the service AND a TLS subscription. See `tls.md` for full details.

```bash
# 1. Check CAA records to choose the right CA
dig CAA example.com +short

# 2. Add domain to service (autoclone since active version is locked)
fastly service domain create \
  --service-id SERVICE_ID \
  --version active --autoclone \
  --name www.example.com

# 3. Activate the new version
fastly service version activate --service-id SERVICE_ID --version latest

# 4. Create TLS subscription (use --cert-auth matching CAA records)
fastly tls-subscription create \
  --domain www.example.com \
  --cert-auth lets-encrypt \
  --config CONFIG_ID

# 5. Get DNS challenge details (--include + --json required)
fastly tls-subscription describe --id SUBSCRIPTION_ID --include tls_authorizations --json
# Look for Authorizations[].Challenges[] — see tls.md for details

# 6. USER ACTION: Create DNS records at your DNS provider:
#    a) _acme-challenge.www.example.com CNAME -> (value from step 5)
#    b) www.example.com CNAME -> m.sni.global.fastly.net

# 7. Wait for certificate issuance (poll until state is "issued")
fastly tls-subscription describe --id SUBSCRIPTION_ID --json

# 8. Verify
curl -sI https://www.example.com/
```

### Rollback to Previous Version

```bash
fastly service version activate --service-id SERVICE_ID --version 1
```

## Propagation Delays

After activating a service version, allow time for changes to propagate across Fastly's network before testing:
- **New service (first activation)**: 500 "Domain Not Found" for 10-60 seconds while the domain propagates. This is normal.
- **Version updates**: 15-30 seconds for the new version to take effect at all POPs, up to 10 minutes in rare cases.
- **Error diagnosis**: If you see 503 after the 500 clears, it's a backend configuration issue (commonly SSL hostname mismatch), not a propagation issue. Fix the backend config instead of waiting longer.

## Dangerous Operations

Ask the user for explicit confirmation before running these commands:

- `fastly service delete` - Permanently deletes a service and all its versions
- `fastly service purge --all` - Purges entire cache, causing origin load spike
- `fastly service version deactivate` - Takes a live service offline

These operations are irreversible or have significant production impact.

## Global Flags

These flags work with most service commands:

- `--service-id SERVICE_ID` or `-s SERVICE_ID`: Target service
- `--version VERSION`: Target version (use "active" or "latest" as shortcuts)
- `--autoclone`: Automatically clone if version is locked/active
- `--json`: Output in JSON format
- `--verbose`: Detailed output

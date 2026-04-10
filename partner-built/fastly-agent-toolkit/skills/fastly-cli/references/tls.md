# Fastly TLS Certificate Management

Configure TLS/HTTPS for Fastly services with custom certificates or Fastly-managed TLS.

## TLS Options Overview

| Option       | Description                        | Best For                          |
| ------------ | ---------------------------------- | --------------------------------- |
| Platform TLS | Fastly-managed shared certificates | Quick setup, standard domains     |
| Custom TLS   | Your own certificates              | Enterprise, specific requirements |
| Subscription | Auto-renewed Let's Encrypt         | Automated certificate management  |

## Platform TLS

Fastly-managed TLS for large numbers of domains.

```bash
# List platform TLS configurations
fastly tls-platform list [--json]

# Upload platform TLS certificate
fastly tls-platform upload \
  --cert-blob "$(cat certificate.crt)" \
  --intermediates-blob "$(cat chain.crt)"

# Describe configuration
fastly tls-platform describe --id PLATFORM_ID [--json]

# Update platform TLS certificate
fastly tls-platform update \
  --id PLATFORM_ID \
  --cert-blob "$(cat new-certificate.crt)" \
  --intermediates-blob "$(cat new-chain.crt)"

# Delete platform TLS
fastly tls-platform delete --id PLATFORM_ID
```

## TLS Subscriptions (Managed Certificates)

Automatically provisioned and renewed certificates via Let's Encrypt, Certainly, or GlobalSign.

**IMPORTANT**: The CLI flag for certificate authority is `--cert-auth` (not `--certificate-authority`).

```bash
# List subscriptions
fastly tls-subscription list [--json]

# Create subscription (choose CA based on domain's CAA records)
fastly tls-subscription create \
  --domain www.example.com \
  --cert-auth lets-encrypt \
  --config CONFIG_ID

# Describe subscription (add --include to get DNS challenge details)
fastly tls-subscription describe --id SUBSCRIPTION_ID --include tls_authorizations --json

# Update subscription
fastly tls-subscription update --id SUBSCRIPTION_ID

# Delete subscription
fastly tls-subscription delete --id SUBSCRIPTION_ID
```

### Subscription States

| State        | Meaning                                                 |
| ------------ | ------------------------------------------------------- |
| `pending`    | Waiting for DNS challenge records to be configured      |
| `processing` | DNS validated, certificate being issued by CA (minutes) |
| `issued`     | Certificate is live and active                          |
| `renewing`   | Auto-renewal in progress (cert still valid)             |
| `failed`     | Issuance failed (CAA conflict, DNS issue, CA rejection) |

Authorization states (within each subscription's `tls_authorizations`):
- `blocked`: Cannot proceed (e.g., missing DNS records, CAA mismatch)
- `passing`: Challenge verified, DNS records correct
- `authorized`: Fully authorized by CA

### Getting DNS Challenge Details

By default, `tls-subscription describe --json` returns `Challenges: null` in the authorizations. You **must** add `--include tls_authorizations` to get the actual challenge records:

```bash
fastly tls-subscription describe --id SUBSCRIPTION_ID --include tls_authorizations --json
```

**IMPORTANT**: The `--include` flag only affects `--json` output. Without `--json`, the text output omits challenge details even with `--include`.

In the JSON response, look for `Authorizations[].Challenges[]` — each challenge has:
- `Type`: `managed-dns`, `managed-http-cname`, or `managed-http-a`
- `RecordType`: `CNAME` or `A`
- `RecordName`: DNS record name to create (e.g., `_acme-challenge.example.com`)
- `Values`: array of target values

Also check `Authorizations[].Warnings` for issues like CAA conflicts.

Alternatively, via the REST API:
```bash
curl -s -H "Fastly-Key: $TOKEN" \
  "https://api.fastly.com/tls/subscriptions/SUBSCRIPTION_ID?include=tls_authorizations"
```
REST API response uses lowercase fields in `included[].attributes.challenges` (not PascalCase).

## Custom TLS Certificates

Upload and manage your own certificates.

### Private Keys

```bash
# List private keys
fastly tls-custom private-key list [--json]

# Upload private key
fastly tls-custom private-key create \
  --name my-key \
  --key "$(cat private.key)"

# Describe key
fastly tls-custom private-key describe --id KEY_ID [--json]

# Delete key
fastly tls-custom private-key delete --id KEY_ID
```

### Certificates

```bash
# List certificates
fastly tls-custom certificate list [--json]

# Upload certificate
fastly tls-custom certificate create \
  --cert-blob "$(cat certificate.crt)" \
  --name my-cert

# Describe certificate
fastly tls-custom certificate describe --id CERT_ID [--json]

# Update certificate (replace)
fastly tls-custom certificate update \
  --id CERT_ID \
  --cert-blob "$(cat new-certificate.crt)"

# Delete certificate
fastly tls-custom certificate delete --id CERT_ID
```

### TLS Activations

Link certificates to domains.

```bash
# List activations
fastly tls-custom activation list [--json]

# Enable activation (link cert to domain)
fastly tls-custom activation enable \
  --cert-id CERT_ID \
  --tls-config-id CONFIG_ID \
  --tls-domain www.example.com

# Describe activation
fastly tls-custom activation describe --id ACTIVATION_ID [--json]

# Update activation (switch to a different certificate)
fastly tls-custom activation update \
  --cert-id NEW_CERT_ID \
  --id ACTIVATION_ID

# Disable activation (remove TLS from domain)
fastly tls-custom activation disable --id ACTIVATION_ID
```

### TLS Domains

```bash
# List TLS domains
fastly tls-custom domain list

# Filter by certificate
fastly tls-custom domain list --filter-tls-certificate-id CERT_ID
```

## TLS Configuration Options

Configure TLS settings per domain.

```bash
# List TLS configs
fastly tls-config list [--json]

# Describe TLS config
fastly tls-config describe --id CONFIG_ID [--json]

# Update TLS config
fastly tls-config update \
  --id CONFIG_ID \
  --name updated-config
```

## Common Workflows

### Setup Let's Encrypt TLS

```bash
# 0. Pre-flight: Check CAA records to choose the right CA
#    lets-encrypt requires CAA to allow "letsencrypt.org"
#    certainly requires CAA to allow "certainly.com"
#    If the domain has no CAA records, any CA works.
dig CAA example.com +short

# 1. Add domain to your service
fastly service domain create --service-id SERVICE_ID --version 1 --name www.example.com
fastly service version activate --service-id SERVICE_ID --version 1

# 2. Create TLS subscription (use --cert-auth, NOT --certificate-authority)
#    Optionally specify --config CONFIG_ID for a specific TLS configuration
fastly tls-subscription create --domain www.example.com --cert-auth lets-encrypt

# 3. Get DNS challenge details (--include + --json required to see challenges)
fastly tls-subscription describe --id SUBSCRIPTION_ID --include tls_authorizations --json
# Look for Authorizations[].Challenges[] in the JSON output
# Typical challenge: CNAME _acme-challenge.DOMAIN -> *.fastly-validations.com
# Also check Authorizations[].Warnings for CAA conflicts

# 4. Create DNS records:
#    a) ACME challenge:  _acme-challenge.www.example.com CNAME <value>.fastly-validations.com
#    b) Traffic routing:  www.example.com CNAME m.sni.global.fastly.net

# 5. Wait for certificate issuance (usually minutes after DNS propagates)
fastly tls-subscription describe --id SUBSCRIPTION_ID
```

### Upload Custom Certificate

```bash
# 1. Upload private key
fastly tls-custom private-key create --name my-key --key "$(cat private.key)"

# 2. Upload certificate
fastly tls-custom certificate create \
  --cert-blob "$(cat certificate.crt)" \
  --name my-cert

# 3. Enable certificate for domain
# First, find the TLS config ID
fastly tls-config list

# Then enable activation
fastly tls-custom activation enable \
  --cert-id CERT_ID \
  --tls-config-id CONFIG_ID \
  --tls-domain www.example.com
```

### Renew Custom Certificate

```bash
# 1. Upload new certificate (same key)
fastly tls-custom certificate update \
  --id CERT_ID \
  --cert-blob "$(cat new-certificate.crt)"

# Certificate is automatically used for existing activations
```

### Replace Certificate and Key

```bash
# 1. Upload new private key
fastly tls-custom private-key create --name new-key --key "$(cat new-private.key)"

# 2. Upload new certificate
fastly tls-custom certificate create \
  --cert-blob "$(cat new-certificate.crt)" \
  --name new-cert

# 3. Update activation to use new certificate
fastly tls-custom activation update \
  --cert-id NEW_CERT_ID \
  --id ACTIVATION_ID

# 4. Clean up old resources
fastly tls-custom certificate delete --id OLD_CERT_ID
fastly tls-custom private-key delete --id OLD_KEY_ID
```

### Add Domain to Existing Subscription

```bash
# Get current subscription details
fastly tls-subscription describe --id SUBSCRIPTION_ID

# Update subscription
fastly tls-subscription update --id SUBSCRIPTION_ID
```

## Certificate Requirements

### Custom Certificate Format
- PEM-encoded X.509 certificate
- RSA (2048-bit minimum) or ECDSA key
- Include intermediate certificates for platform TLS via `--intermediates-blob`

### Domain Validation
- DNS CNAME validation for Let's Encrypt
- Domain must be routed through Fastly before activation

## Propagation Delays

TLS changes can take up to 5 minutes to propagate globally:
- Certificate uploads and activations: 1-5 minutes
- TLS subscription creation: Minutes to hours (includes DNS validation and certificate issuance)
- Certificate renewals: Automatic, no propagation delay once issued

Automation scripts should poll subscription/activation status rather than assuming immediate availability. For certificate activations, verify HTTPS connectivity with retries before considering the operation complete.

## Dangerous Operations

Ask the user for explicit confirmation before running these commands:

- `fastly tls-platform delete` - Removes TLS for all domains in the configuration
- `fastly tls-subscription delete` - Deletes Let's Encrypt certificate subscription
- `fastly tls-custom certificate delete` - Deletes a custom certificate
- `fastly tls-custom private-key delete` - Deletes a private key
- `fastly tls-custom activation disable` - Removes TLS from a domain

These operations can cause HTTPS to stop working for affected domains.

## Troubleshooting

**Certificate not working**: Ensure domain points to Fastly (CNAME to `m.sni.global.fastly.net` for subdomains, or A records for apex). Get exact records from `fastly tls-config describe --id CONFIG_ID --json` or `GET /tls/configurations/{id}?include=dns_records`.

**Subscription stuck in `pending`**: DNS challenge records not configured or not propagated. Verify with `dig CNAME _acme-challenge.DOMAIN +short`. The value should match the challenge from the REST API.

**Subscription `failed` with CAA warning**: The domain's CAA records restrict which CAs can issue certificates. Check with `dig CAA DOMAIN +short`. If it says `0 issue "letsencrypt.org"`, you must use `--cert-auth lets-encrypt` (not `certainly`). If no CAA records exist, any CA works. Fix: delete the failed subscription, recreate with the correct `--cert-auth` value.

**Authorization state `blocked`**: Check `included[].attributes.warnings` in the REST API response for details. Common causes: CAA record mismatch, domain not resolving.

**Chain validation error**: Include intermediate certificates with `--intermediates-blob` when using platform TLS.

**Private key mismatch**: Ensure certificate matches uploaded private key.

**`--certificate-authority` flag not found**: The correct flag is `--cert-auth`.

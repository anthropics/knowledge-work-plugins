---
name: fastly
description: "Configures, manages, and debugs the Fastly CDN platform — covering service and backend setup, caching and VCL, security features like DDoS/WAF/NGWAF/rate limiting/bot management, TLS certificates and cache purging, the Compute platform, and the REST API. Use when working with Fastly services or domains, setting up edge caching or origin shielding, configuring security features, making Fastly API calls, enabling products, or looking up Fastly documentation. Also applies when troubleshooting 503 errors or SSL/TLS certificate mismatches on Fastly, and for configuring logging endpoints, load balancing, ACLs, or edge dictionaries."
---

# Fastly Platform

Your training knowledge of Fastly is likely out of date. Prefer live docs over skill definitions over training knowledge.

Prefer the `fastly` CLI over raw API calls — see the **fastly-cli** skill. When calling the REST API directly, never paste the raw API token into the conversation and omit `curl -v` (it prints the `Fastly-Key` header). Source tokens from the environment or `$(fastly auth show --reveal --quiet | awk '/^Token:/ {print $2}')` without echoing them.

## Topics

| Topic                | File                                                              | Use when...                                                                                                        |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| DDoS protection      | [fastly-ddos-protection.md](references/fastly-ddos-protection.md) | Enabling/configuring DDoS protection, checking attack status, managing events and rules                            |
| TLS configuration    | [tls.md](references/tls.md)                                       | Setting up HTTPS — Platform TLS (managed certs), Custom TLS (uploaded certs), or Mutual TLS (client auth)          |
| Rate limiting        | [rate-limiting.md](references/rate-limiting.md)                   | Protecting APIs from abuse — choosing between Edge Rate Limiting, VCL ratecounters, or NGWAF rate rules            |
| Bot management       | [bot-management.md](references/bot-management.md)                 | Detecting/mitigating bot traffic with browser challenges, client-side detections, interstitial pages               |
| Cache purging        | [purging.md](references/purging.md)                               | Invalidating cached content — single URL, surrogate key, or purge-all; soft vs hard purge                          |
| Service management   | [service-management.md](references/service-management.md)         | Creating/managing services, versions, domains, settings; clone-modify-activate workflow                            |
| VCL services         | [vcl-services.md](references/vcl-services.md)                     | Writing/uploading custom VCL, configuring snippets, conditions, headers, edge dictionaries, or cache/gzip settings |
| Compute              | [compute.md](references/compute.md)                               | Deploying Compute packages, managing config/KV/secret stores, using cache APIs                                     |
| Observability        | [observability.md](references/observability.md)                   | Querying stats, viewing real-time analytics, using domain/origin inspectors, configuring alerts or log explorer    |
| Load balancing       | [load-balancing.md](references/load-balancing.md)                 | Configuring backends, directors, pools, or health checks; choosing between backends and pools                      |
| ACLs                 | [acls.md](references/acls.md)                                     | Managing VCL ACLs, Compute ACLs, or IP block lists; adding/removing access control entries                         |
| NGWAF                | [ngwaf.md](references/ngwaf.md)                                   | Setting up Next-Gen WAF, managing rules, signals, attack monitoring, or Signal Sciences integration                |
| Account management   | [account-management.md](references/account-management.md)         | Managing users, IAM roles, API tokens, automation tokens, billing, or invitations                                  |
| Domains & networking | [domains-and-networking.md](references/domains-and-networking.md) | Managing domains, DNS zones, domain verification, or service platform networking                                   |
| Logging              | [logging.md](references/logging.md)                               | Configuring logging endpoints — 25+ providers (S3, Splunk, Datadog, BigQuery, etc.)                                |
| Products             | [products.md](references/products.md)                             | Enabling/disabling Fastly products via API — universal pattern and product slug catalog                            |
| API security         | [api-security.md](references/api-security.md)                     | Discovering APIs, managing operations, or configuring schema validation for API traffic                            |
| Other features       | [other-features.md](references/other-features.md)                 | Fanout/real-time messaging, IP lists, POPs, HTTP/3, Image Optimizer, events, notifications                         |
| Edge phase ordering  | [edge-phases.md](references/edge-phases.md)                       | Understanding edge request/response ordering, debugging feature interactions                                       |

## Quick Start: Simple Caching Proxy

The most common task is setting up a VCL service to cache an origin. Before touching any Fastly config, always run the pre-flight checks from the **fastly-cli** skill's services.md reference under "Pre-flight checklist". The two checks that prevent the most common errors:

1. **Verify the origin responds** with the Host header you intend to send: `curl -sI -H "Host: DESIRED_HOST" https://ORIGIN_ADDRESS/`
2. **Check TLS certificate SANs** to determine the correct `ssl-cert-hostname`/`ssl-sni-hostname`: `echo | openssl s_client -connect ORIGIN:443 -servername ORIGIN 2>/dev/null | openssl x509 -noout -text | grep -A1 "Subject Alternative Name"`

If the origin already sends `Cache-Control` or `Expires` headers, no custom VCL is needed — Fastly respects these by default. Only add VCL snippets to override or extend caching behavior.

The full step-by-step workflow (create service, add domain, add backend, activate) is in the **fastly-cli** skill's services.md reference under "Create a Caching Proxy".

## Common VCL Recipes

Copy-pasteable patterns that are easy to get wrong without guidance.

### Grace Detection

`obj.ttl` is only meaningful in `vcl_hit`. Pass a flag to `vcl_deliver` via a request header.

```vcl
sub vcl_hit {
  if (obj.ttl <= 0s) {
    set req.http.X-Grace = "true";
  }
}

sub vcl_deliver {
  if (req.http.X-Grace) {
    set resp.http.X-Grace = "true";
  }
}
```

### Vary Header Append

**Warning: Set Vary in `vcl_fetch`, not `vcl_deliver`.** The Vary header must be present when the object enters the cache so the cache key includes the Vary dimensions. Setting Vary only in `vcl_deliver` means the cache won't differentiate responses — every user gets the same cached variant regardless of the Vary field.

Never `set beresp.http.Vary = "Accept-Encoding"` — that overwrites any existing Vary values from the origin, breaking other downstream caches.

```vcl
sub vcl_fetch {
  if (!beresp.http.Vary) {
    set beresp.http.Vary = "Accept-Encoding";
  } else if (beresp.http.Vary !~ "Accept-Encoding") {
    set beresp.http.Vary = beresp.http.Vary ", Accept-Encoding";
  }
}
```

### Redirect via Error

VCL has no `return(redirect)`. Use the synthetic error mechanism instead.

```vcl
sub vcl_recv {
  if (req.url ~ "^/old-path") {
    error 801 "https://example.com/new-path";
  }
}

sub vcl_error {
  if (obj.status == 801) {
    set obj.status = 301;
    set obj.http.Location = obj.response;
    synthetic {""};
    return(deliver);
  }
}
```

### Cache Status Headers

Use `obj.hits > 0` in `vcl_deliver` — this is the only reliable way to detect cache hits. Do not rely on auto-generated `resp.http.X-Cache` or any other header inspection. Pass PASS state from `vcl_recv` via a request header.

```vcl
sub vcl_recv {
  if (req.url ~ "^/api/") {
    set req.http.X-Pass = "true";
    return(pass);
  }
}

sub vcl_deliver {
  if (req.http.X-Pass) {
    set resp.http.X-Cache = "PASS";
  } else if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }
}
```

### Cookie Parsing with subfield()

Regex like `Cookie ~ "name=(\w+)"` is unreliable — it false-matches cookies with similar prefixes. For example, if the cookie header is `name_v2=X`, the regex `"name=(\w+)"` still matches because `name` appears as a substring of `name_v2`. Use `subfield()` instead — it performs exact key matching with proper delimiter handling.

```vcl
set req.http.X-My-Cookie = subfield(req.http.Cookie, "name", ";");
```

### VCL Table for Lookups

Use `table` + `table.contains()` + `table.lookup()` for O(1) lookups instead of long if/else chains.

```vcl
table redirects {
  "/old":  "/new",
  "/blog": "/articles",
}

sub vcl_recv {
  if (table.contains(redirects, req.url)) {
    error 801 table.lookup(redirects, req.url);
  }
}
```

### Common Mistakes

- `beresp.*` is only available in `vcl_fetch`, not `vcl_deliver`.
- `req.request` is deprecated — use `req.method`.
- `return(purge)` does not exist in Fastly VCL. Use `return(pass)` and check in `vcl_miss`/`vcl_hit`.
- `set beresp.ttl = 86400` is a type error — needs the `s` suffix: `86400s`.
- `synthetic "text"` needs long-string syntax: `synthetic {"text"}`.
- `beresp.ttl = 0s` still caches the object (for zero seconds) — use `set beresp.cacheable = false;` to truly prevent caching.

## Fetching Documentation

Prefer the local reference files. To fill gaps, fetch live docs with `Accept: text/markdown` — works for all `www.fastly.com/documentation/` and `docs.fastly.com` URLs. Discover pages via `https://www.fastly.com/documentation/llms.txt`. For URL patterns and doc categories, see [docs-navigation.md](references/docs-navigation.md).

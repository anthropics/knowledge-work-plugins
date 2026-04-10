# Fastly Bot Management

Base: `https://api.fastly.com` | Auth: `Fastly-Key: $FASTLY_API_TOKEN` | Docs: https://www.fastly.com/documentation/reference/api/products/bot-management

## How It Works

Bot Management uses server-side fingerprinting, client challenges, and client-side detections to distinguish legitimate users from automated traffic.

### Detection Mechanisms

- **Client fingerprinting**: JA3/JA4 TLS fingerprinting at the edge. Identifies client types from TLS handshake signatures without origin-side configuration. Detects credential stuffing, credential cracking, and IP rotation bots.
- **Client challenges**: Three types -- *dynamic* (auto-selects best method: PATs, non-interactive PoW, or interactive), *interactive* (CAPTCHA-like), and *non-interactive* (JavaScript Proof-of-Work). Challenges present an interstitial page while processing.
- **Private Access Tokens (PATs)**: Cryptographic device attestation that verifies humans without puzzles or revealing identity. Apple devices only (iOS 16+, macOS Ventura+). Rate-limited to 10 tokens/min per device. Selected automatically by dynamic challenges when available.
- **Client-side detections**: JavaScript snippet that detects headless browsers by collecting browser signals. Must be **manually embedded** in your HTML pages -- not injected automatically.
- **Verified bots**: Allowlisting for known legitimate bots (search crawlers, etc.). Adds an NGWAF signal for use in rule conditions.

### Execution Ordering

Bot Management runs in the `edge_waf_request_inspection` phase, which executes **after** `edge_app_request_processing` (VCL/Compute):

```
client -> adaptive_threat_engine -> edge_app_request_processing (VCL/Compute)
       -> edge_waf_request_inspection (Bot Management, Edge WAF)
       -> external_origin_fetch
```

Key implications:
- **VCL/Compute executes before Bot Management**, so bot decisions occur after app logic has run
- **VCL/Compute can set headers** that Bot Management reads, but should not manipulate challenge cookies (`Set-Cookie`/`Cookie` headers) as these are essential for challenge processing
- **Bot Management sees the request as modified by VCL/Compute**, including any header rewrites or URL changes
- Bot Management shares the `edge_waf_request_inspection` phase with Edge WAF (NGWAF)

### Prerequisites

- Active **NGWAF (Next-Gen WAF) subscription** -- Bot Management is an add-on to NGWAF, not a standalone product
- Requires an NGWAF subscription (Bot Management is purchased as an add-on to NGWAF)
- The client-side detection JavaScript snippet must be deployed in your HTML pages

## Enablement

Product slug: `bot_management`. Requires an NGWAF subscription. No product-specific configuration. See `products.md` for the universal enablement pattern.

## Documentation

URLs below serve Markdown (use the `Accept: text/markdown` header).

| Source                                           | URL                                                                                                         |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Product overview, prerequisites, billing         | `https://docs.fastly.com/products/bot-management`                                                           |
| Setup guides, configuration, challenge tuning    | `https://www.fastly.com/documentation/guides/security/bot-management`                                       |
| API endpoints, request/response schemas          | `https://www.fastly.com/documentation/reference/api/products/bot-management`                                |
| Client challenge types, embedding, configuration | `https://www.fastly.com/documentation/guides/security/bot-management/client-challenges`                     |
| Advanced client-side detection setup             | `https://www.fastly.com/documentation/guides/security/bot-management/using-advanced-client-side-detections` |

For general Fastly platform guidance, documentation source index, and other specialized skills, see the `fastly` skill.

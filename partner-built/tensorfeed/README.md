# TensorFeed for Claude Cowork

Live, machine-readable AI ecosystem and regulated-domain data through TensorFeed.ai's hosted MCP server. Designed for knowledge workers who need fresh, sourced facts in their daily workflows.

## What's covered

The TensorFeed MCP server at `https://tensorfeed.ai/api/mcp` exposes **17 free tools** across five domains:

| Domain | Use cases |
|---|---|
| News + AI ecosystem | Track competitor AI launches, monitor industry news, check AI service status before relying on a vendor |
| Security advisories | Look up CVE severity + exploitation likelihood, audit a package for OSV advisories, check the CISA KEV catalog |
| Finance + filings | SEC EDGAR full-text search across 10-Ks/10-Qs/8-Ks, recent filings by ticker, ticker-to-CIK lookup |
| FDA regulatory | Query FAERS adverse events, SPL drug labels, drug/food recall enforcement reports, MAUDE device events |
| Energy + macro | US energy time-series (oil, gas, electricity), via EIA Open Data |

## Who benefits

- **Finance + accounting** — SEC EDGAR full-text search, BLS/FRED macro indicators, audit prep
- **Legal + compliance** — Filings research, CVE/security disclosure monitoring, FDA recall lookups for medical-device or pharma clients
- **Bio-research + life sciences** — openFDA queries (FAERS, recalls, labels, MAUDE) alongside the dedicated bio-research plugin
- **Marketing + competitive intelligence** — Real-time AI news across 12+ sources, model pricing comparison
- **Sales** — Ticker-to-company-context lookups for prospect research

## Auth

No auth required for these 17 tools. TensorFeed also exposes ~33 premium REST endpoints with LLM-ready transforms and ~80-99% token reduction; these are accessed separately and require a bearer token purchased via x402 V2 payment on Base (USDC). See [TensorFeed agent payments docs](https://tensorfeed.ai/developers/agent-payments).

## License

- Plugin metadata: MIT
- Underlying data: most is US Government public domain (SEC, BLS, FRED, MITRE, CISA, EIA) or CC0 (openFDA), with FIRST.org EPSS free-for-any-use and OSV.dev under Apache 2.0. Commercial redistribution permitted across the surface; attribution preserved on every response per upstream policies.

## Links

- Endpoint catalog: https://tensorfeed.ai/api/meta
- Agent-friendly entry doc: https://tensorfeed.ai/llms.txt
- Source: https://github.com/RipperMercs/tensorfeed (public)

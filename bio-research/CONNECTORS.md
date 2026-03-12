# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~literature` might mean PubMed, bioRxiv, or any other literature source with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (literature, clinical trials, chemical database, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Literature | `~~literature` | PubMed, bioRxiv, BGPT | Google Scholar, Semantic Scholar |
| Scientific illustration | `~~scientific illustration` | BioRender | — |
| Clinical trials | `~~clinical trials` | ClinicalTrials.gov | EU Clinical Trials Register |
| Chemical database | `~~chemical database` | ChEMBL | PubChem, DrugBank |
| Drug targets | `~~drug targets` | Open Targets | UniProt, STRING |
| Data repository | `~~data repository` | Synapse | Zenodo, Dryad, Figshare |
| Journal access | `~~journal access` | Wiley Scholar Gateway | Elsevier, Springer Nature |
| AI research | `~~AI research` | Owkin | — |
| Lab platform | `~~lab platform` | Benchling\* | — |

\* Placeholder — MCP URL not yet configured

## Notes

- **BGPT** uses SSE transport (`"type": "sse"`) rather than streamable HTTP. It provides structured experimental data extracted from full-text papers, including methods, results, sample sizes, quality scores, and conclusions — complementing PubMed and bioRxiv's standard metadata. Free tier: 50 searches per network, no API key required. See [bgpt.pro/mcp](https://bgpt.pro/mcp) or [github.com/connerlambden/bgpt-mcp](https://github.com/connerlambden/bgpt-mcp).

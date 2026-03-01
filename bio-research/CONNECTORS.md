# Connectors

## Two types of data sources

This plugin uses two types of MCP connections:

1. **Biosciences-MCP Gateway** — the plugin's own server providing 34 tools across 12 life sciences databases. This is the primary data source for all biosciences skills (genomics, proteomics, pharmacology, clinical, graph-builder, etc.) and the `/ob-research` command. The gateway is **not interchangeable** — it enforces the Fuzzy-to-Fact protocol with `slim` parameter support, structured responses, and `UNRESOLVED_ENTITY` error handling.

2. **Partner MCP Servers** — external tools referenced by `~~category` placeholders (see below). These provide literature search, visualization, data management, and other capabilities. They are interchangeable — any MCP server in a given category works.

### When to use which

| Task | Use | Why |
|------|-----|-----|
| Gene/protein/drug/disease resolution | Biosciences-MCP gateway | LOCATE→RETRIEVE discipline, `slim` parameter, CURIE-based IDs |
| Graph-based research (`/ob-research`) | Biosciences-MCP gateway | 34 tools orchestrated by graph-builder skill |
| Literature search | `~~literature` partner MCP | Gateway doesn't cover literature databases |
| Scientific illustrations | `~~scientific illustration` partner MCP | Gateway doesn't generate figures |
| Dataset grounding | `~~data repository` partner MCP | Synapse MCP used during `/ob-publish` Stage 1b |
| Quick compound/target lookup | Either | Partner MCPs for casual browsing; gateway for structured pipelines |

## How `~~category` placeholders work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~literature` might mean PubMed, bioRxiv, or any other literature source with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (literature, clinical trials, chemical database, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Partner connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Literature | `~~literature` | PubMed, bioRxiv | Google Scholar, Semantic Scholar |
| Scientific illustration | `~~scientific illustration` | BioRender | — |
| Clinical trials | `~~clinical trials` | ClinicalTrials.gov | EU Clinical Trials Register |
| Chemical database | `~~chemical database` | ChEMBL | PubChem, DrugBank |
| Drug targets | `~~drug targets` | Open Targets | UniProt, STRING |
| Data repository | `~~data repository` | Synapse | Zenodo, Dryad, Figshare |
| Journal access | `~~journal access` | Wiley Scholar Gateway | Elsevier, Springer Nature |
| AI research | `~~AI research` | Owkin | — |
| Lab platform | `~~lab platform` | Benchling\* | — |

\* Placeholder — MCP URL not yet configured

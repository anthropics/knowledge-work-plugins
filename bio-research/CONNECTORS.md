# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~literature` might mean PubMed, bioRxiv, or any other literature source with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (literature, clinical trials, chemical database, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

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
| Gene databases | `~~gene databases` | Life Sciences Gateway\*\* (HGNC, Ensembl, NCBI) | NCBI Gene, Ensembl REST |
| Protein databases | `~~protein databases` | Life Sciences Gateway\*\* (UniProt, STRING, BioGRID) | UniProt REST, STRING API |
| Pharmacology | `~~pharmacology` | Life Sciences Gateway\*\* (ChEMBL, PubChem, IUPHAR) | DrugBank, GtoPdb |
| Pathway databases | `~~pathway databases` | Life Sciences Gateway\*\* (WikiPathways) | Reactome, KEGG |
| CRISPR screens | `~~CRISPR screens` | BioGRID ORCS API (curl) | DepMap Portal |
| CQ evaluation | `~~CQ evaluation` | CQ-Eval MCP\*\*\* | — |

\* Placeholder — MCP URL not yet configured

\*\* Life Sciences Gateway is a FastMCP composite server providing 34 tools across 12 databases via the Fuzzy-to-Fact protocol. Source: https://github.com/donbr/lifesciences-research

\*\*\* CQ-Eval MCP is a local FastMCP server providing 8 tools for competency question golden test set management and scoring. Tools: `cq_list`, `cq_get`, `cq_add`, `cq_import_from_markdown`, `cq_record_step`, `cq_score`, `cq_results`, `cq_compare`. Validates data federation accuracy by comparing tool results to gold standard mechanistic paths (Drug→Target→Gene→Disease). Scoring aligned with BTE-RAG benchmark methodology (Xu et al. 2025).

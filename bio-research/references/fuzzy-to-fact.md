# Fuzzy-to-Fact Protocol

The Fuzzy-to-Fact protocol is a bi-modal discipline for grounding life sciences research in API-verified data. Every entity — gene, protein, drug, disease, trial — must pass through a LOCATE step (fuzzy search) before a RETRIEVE step (strict lookup by canonical ID). This prevents hallucination by ensuring all facts trace to tool calls, not training knowledge.

## The Bi-Modal Contract

| Mode | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| **LOCATE** (fuzzy) | Find candidates from natural language | `query="BRCA1"`, `slim=true`, `page_size=5` | Ranked candidates with canonical IDs (~20 tokens each) |
| **RETRIEVE** (strict) | Get verified metadata by canonical ID | `hgnc_id="HGNC:1100"`, `slim=false` | Full structured record with cross-references (~115-300 tokens) |

```
# LOCATE: fuzzy search returns candidates
Call hgnc_search_genes with: {"query": "BRCA1", "slim": true, "page_size": 5}
  → Returns candidates → select best match: HGNC:1100

# RETRIEVE: strict lookup by resolved CURIE
Call hgnc_get_gene with: {"hgnc_id": "HGNC:1100"}
  → Returns verified metadata: symbol, name, UniProt, Ensembl cross-refs
```

## UNRESOLVED_ENTITY Error

Passing a raw string (e.g., `"BRCA1"`) to a strict RETRIEVE endpoint triggers an `UNRESOLVED_ENTITY` error. The fix is always: run LOCATE first, extract the canonical ID, then call RETRIEVE.

If LOCATE returns no candidates after **3 search attempts** (varying query terms), mark the entity as `"status": "unresolved"` and move on. Do not guess IDs.

## The 6 Phases

| Phase | Name | Mode | What Happens |
|-------|------|------|--------------|
| 1 | ANCHOR | LOCATE → RETRIEVE | Resolve every gene, drug, disease to canonical CURIEs |
| 2 | ENRICH | RETRIEVE | Decorate entities with metadata and cross-references |
| 3 | EXPAND | LOCATE → RETRIEVE | Build interaction network from STRING, BioGRID, WikiPathways |
| 4a | TRAVERSE_DRUGS | LOCATE → RETRIEVE | Find drugs targeting identified proteins via Open Targets, ChEMBL |
| 4b | TRAVERSE_TRIALS | LOCATE → RETRIEVE | Find clinical trials for identified drugs via ClinicalTrials.gov |
| 5 | VALIDATE | RETRIEVE | Verify every NCT ID, drug mechanism, and gene-disease link |
| 6a | PERSIST | — | Format validated graph as JSON, persist to Graphiti |
| 6b | REPORT | — | Select template, grade evidence, format report |

## Token Budgeting

The `slim` parameter controls token usage per tool call. Use `slim=true` during LOCATE phases (Phases 1, 3) for fast candidate lists at ~20 tokens/entity. Use `slim=false` (default) during RETRIEVE phases (Phases 2, 4, 5) for full metadata. This enables batch resolution of 10-50 entities per LLM turn.

See [token-budgeting.md](token-budgeting.md) for detailed examples and impact analysis.

## Domain Skill Architecture

| Skill | Phases | Primary Databases |
|-------|--------|-------------------|
| biosciences-genomics | 1-2 | HGNC, Ensembl, NCBI Entrez |
| biosciences-proteomics | 2-3 | UniProt, STRING, BioGRID |
| biosciences-pharmacology | 4a | ChEMBL, PubChem, IUPHAR, Open Targets |
| biosciences-clinical | 4b, 5 | Open Targets associations, ClinicalTrials.gov |
| biosciences-crispr | 3 (extension) | BioGRID ORCS essentiality screens |
| biosciences-graph-builder | 1-6a | All databases (orchestrator) |

## Downstream Consumers

The graph-builder's Phase 1-6a output feeds three downstream skills:

| Skill | Consumes | Produces |
|-------|----------|----------|
| biosciences-reporting | Phase 1-6a data | Template-formatted report with evidence grading (Phase 6b) |
| biosciences-reporting-quality-review | Report + KG JSON | 10-dimension quality assessment (Stage 2) |
| biosciences-publication-pipeline | All prior outputs | 5 publication files: report, KG JSON, Synapse grounding, quality review, BioRxiv draft (Stages 1-4) |

These downstream skills do **not** make new API calls to life sciences databases. They synthesize, format, and validate existing pipeline data. The only exception is Synapse MCP tools used during publication pipeline Stage 1b grounding.

## See Also

- [token-budgeting.md](token-budgeting.md) — `slim` parameter usage and token savings
- [api-keys.md](api-keys.md) — Required API keys for each skill

---
name: lifesciences-cq-catalog
description: Manage the competency question golden test set — add, version, import, and curate CQs for data federation validation.
license: Complete terms in LICENSE.txt
---

# Competency Question Catalog Management Skill

## Purpose

Manage the golden test set of competency questions (CQs) used to validate data federation accuracy. This skill handles the lifecycle of CQs: importing from existing catalogs, creating new questions, versioning, tagging, and curating gold standard paths.

## Getting Started

### Bootstrap from existing catalog

The initial CQ set comes from `competency-questions-catalog.md`. Import it:

```
Use: cq_import_from_markdown(markdown_path="/path/to/competency-questions-catalog.md")
```

This parses the structured markdown and creates CQ entries. Review and refine:

```
Use: cq_list()           → See all imported CQs
Use: cq_get(cq_id="cq1") → Review details of a specific CQ
Use: cq_add(cq_json=...) → Update with corrected entities/edges/workflow
```

### CQ Structure

Each competency question has:

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique identifier | `cq1` |
| `title` | Short descriptive title | `Palovarotene mechanism for FOP` |
| `question` | Natural language question | `How does Palovarotene treat Fibrodysplasia Ossificans Progressiva?` |
| `category` | Question type | `mechanistic`, `genetic`, `clinical`, `network` |
| `difficulty` | Complexity level | `basic`, `moderate`, `advanced`, `expert` |
| `entities` | Gold standard entities with CURIEs | `[{name: "ACVR1", curie: "HGNC:171", entity_type: "gene"}]` |
| `edges` | Gold standard mechanistic path | `[{source: "CHEMBL:2105648", target: "CHEMBL:2003", relation: "agonist"}]` |
| `workflow` | Ordered validation steps | `[{step_id: "anchor", tool_pattern: "chembl_search_compounds"}]` |
| `tags` | Filtering tags | `["pharmacology", "rare_disease"]` |
| `source` | Origin of the CQ | `manual`, `drugmechdb`, `bte-rag`, `literature` |
| `version` | Semantic version | `1.0.0` |

### Entity Reference Format

Entities use canonical CURIEs from the Fuzzy-to-Fact protocol:

| Entity Type | CURIE Format | Example |
|-------------|-------------|---------|
| Gene (HGNC) | `HGNC:NNNNN` | `HGNC:171` (ACVR1) |
| Gene (Ensembl) | `ENSGXXXXXXXXXXX` | `ENSG00000115170` |
| Gene (NCBI) | `NCBIGene:NNNNN` | `NCBIGene:90` |
| Protein (UniProt) | `UniProtKB:XXXXXX` | `UniProtKB:Q04771` |
| Compound (ChEMBL) | `CHEMBL:NNNNN` | `CHEMBL:2105648` |
| Compound (PubChem) | `PubChem:CIDNNNNN` | `PubChem:CID135565588` |
| Disease (MONDO) | `MONDO:NNNNNNN` | `MONDO:0007606` |
| Disease (EFO) | `EFO_NNNNNNN` | `EFO_0000305` |
| Pathway (WikiPathways) | `WP:WPNNNNN` | `WP:WP2760` |
| Target (IUPHAR) | `IUPHAR:NNN` | `IUPHAR:215` |

### Edge Evidence Tiers

Each edge in the gold standard path is tagged with the expected validation tier:

| Tier | Source | When to Use |
|------|--------|-------------|
| `tier1` | MCP Tool (Fuzzy-to-Fact) | Verified entity lookups, associations, interactions |
| `tier2` | curl Skill (direct API) | Mechanism retrieval, bulk enrichment, STRING functional enrichment |
| `tier3` | Literature / Graphiti | Edges supported only by published evidence, not structured APIs |

This aligns with `prior-art-api-patterns.md` §7.5 (Three-Tier Architecture).

## Creating New CQs

### From a research question

1. Identify the mechanistic path you want to validate
2. Resolve all entities to canonical CURIEs using Fuzzy-to-Fact
3. Define edges with relation types and evidence tiers
4. Design workflow steps mapping to specific tools or curl patterns
5. Add to catalog:

```json
{
  "id": "cq16",
  "title": "PCSK9 inhibition for hypercholesterolemia",
  "question": "How do PCSK9 inhibitors lower LDL cholesterol?",
  "category": "mechanistic",
  "difficulty": "moderate",
  "entities": [
    {"name": "Evolocumab", "curie": "CHEMBL:1743070", "entity_type": "drug"},
    {"name": "PCSK9", "curie": "HGNC:20001", "entity_type": "gene"},
    {"name": "LDLR", "curie": "HGNC:6547", "entity_type": "gene"},
    {"name": "Hypercholesterolemia", "curie": "MONDO:0005148", "entity_type": "disease"}
  ],
  "edges": [
    {"source": "CHEMBL:1743070", "target": "HGNC:20001", "relation": "inhibitor", "evidence_tier": "tier2"},
    {"source": "HGNC:20001", "target": "HGNC:6547", "relation": "degrades", "evidence_tier": "tier1"},
    {"source": "HGNC:6547", "target": "MONDO:0005148", "relation": "associated_with", "evidence_tier": "tier1"}
  ],
  "workflow": [
    {"step_id": "anchor", "description": "Resolve Evolocumab", "tool_pattern": "chembl_search_compounds", "tier": "tier1"},
    {"step_id": "mechanism", "description": "Get PCSK9 inhibition mechanism", "tool_pattern": "curl chembl/mechanism", "tier": "tier2"},
    {"step_id": "target_gene", "description": "Resolve PCSK9 gene", "tool_pattern": "hgnc_search_genes → hgnc_get_gene", "tier": "tier1"},
    {"step_id": "interaction", "description": "PCSK9-LDLR interaction", "tool_pattern": "string_get_interactions", "tier": "tier1"},
    {"step_id": "disease", "description": "LDLR-hypercholesterolemia association", "tool_pattern": "opentargets_get_associations", "tier": "tier1"}
  ],
  "tags": ["pharmacology", "cardiovascular", "antibody"],
  "source": "manual"
}
```

### From DrugMechDB (future)

As the catalog matures, import mechanistic paths from DrugMechDB to align with BTE-RAG benchmarks:

1. Download DrugMechDB paths for a therapeutic area
2. Convert path nodes to canonical CURIEs via Fuzzy-to-Fact
3. Map path edges to evidence tiers
4. Generate workflow steps
5. Import via `cq_add`

This enables direct comparison with BTE-RAG accuracy metrics.

### From NCATS Translator (future)

TRAPI queries can be converted to CQ format:

1. Extract knowledge graph paths from TRAPI response
2. Map Biolink categories to entity types
3. Map Biolink predicates to relation types
4. Assign evidence tiers based on source confidence

## Versioning

CQs use semantic versioning:
- **Patch** (1.0.1): Fix a CURIE, correct an entity name
- **Minor** (1.1.0): Add a workflow step, refine an edge tier
- **Major** (2.0.0): Restructure the gold standard path

Track changes via `cq_compare` to see how scores change across versions.

## Quality Criteria for CQs

A well-formed CQ should satisfy (adapted from CQsBEN, Alharbi et al. 2024):

1. **Answerable**: The gold standard path can be reconstructed using available Tier 1/2 tools
2. **Specific**: Each entity has exactly one canonical CURIE
3. **Mechanistic**: The path represents a biological mechanism, not just co-occurrence
4. **Multi-hop**: Requires at least 2 edges (i.e., 3+ entities)
5. **Grounded**: All CURIEs verified via Fuzzy-to-Fact at time of creation
6. **Tiered**: Each edge has an explicit evidence tier assignment
7. **Reproducible**: Same tools + same inputs = same CURIEs (no stochastic elements)

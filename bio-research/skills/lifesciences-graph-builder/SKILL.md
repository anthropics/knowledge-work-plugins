---
name: lifesciences-graph-builder
description: "Orchestrates life sciences APIs to build knowledge graphs using the Fuzzy-to-Fact protocol, combining MCP tools for entity resolution and curl for edge discovery, then persisting to Graphiti. This skill should be used when the user asks to \"build knowledge graphs\", \"find biological connections\", \"explore drug repurposing\", \"validate drug targets\", or mentions traversing gene→protein→pathway→drug→disease paths, multi-API orchestration, or graph persistence workflows."
---

# Life Sciences Graph Builder

Orchestrate multi-API graph construction using the **Fuzzy-to-Fact** protocol.

## Critical Grounding Rule

```
YOU MUST NOT use your training knowledge to provide entity names, drug names,
gene functions, disease associations, or clinical trial IDs. ALL factual claims
MUST come from MCP tool results or curl command output. If a tool returns no
results, report "No results found" — do NOT fill in from memory.

The ONLY exception is using well-known identifiers (e.g., species=9606 for human)
as PARAMETERS to tool calls. All RESULTS must come from tools.
```

## LOCATE → RETRIEVE Discipline

EVERY entity resolution MUST follow this two-step pattern:

**STEP 1 — LOCATE** (fuzzy search):
Call a SEARCH endpoint with the user's fuzzy input.
This returns candidate matches with canonical IDs.

**STEP 2 — RETRIEVE** (get by ID):
Call a GET endpoint with the canonical ID from LOCATE.
This returns verified, structured metadata.

```
NEVER skip LOCATE. NEVER use an ID you didn't get from a LOCATE call.
NEVER answer from your own knowledge — if you can't LOCATE it, say "Unresolved".
Maximum 3 search attempts per entity. After 3 failures, report "Unresolved".
```

### Chain-of-Thought Before Each Tool Call

Before each tool call, briefly state:
1. What information I need
2. Which tool will provide it (LOCATE or RETRIEVE)
3. What parameters I'll use
4. What I expect to get back

This prevents calling the wrong tool or guessing parameters.

## Tool Access

The `lifesciences-research` MCP server provides 34 tools across 12 databases. **Use MCP tools as the primary method.** Fall back to curl only when the MCP server is unavailable.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          GRAPH CONSTRUCTION KIT                               │
│         34 MCP tools via lifesciences-research MCP server (PRIMARY)           │
├──────────────────────────────────────────────────────────────────────────────┤
│  TIER 1: GENE/PROTEIN FOUNDATION                                             │
│  ├── HGNC: hgnc_search_genes (LOCATE), hgnc_get_gene (RETRIEVE)             │
│  ├── UniProt: uniprot_search_proteins (LOCATE), uniprot_get_protein          │
│  ├── STRING: string_search_proteins (LOCATE), string_get_interactions,       │
│  │           string_get_network_image_url                                     │
│  └── BioGRID: biogrid_search_genes (LOCATE), biogrid_get_interactions        │
├──────────────────────────────────────────────────────────────────────────────┤
│  TIER 2: DRUG DISCOVERY                                                       │
│  ├── ChEMBL: chembl_search_compounds (LOCATE), chembl_get_compound,          │
│  │           chembl_get_compounds_batch                                       │
│  ├── Open Targets: opentargets_search_targets (LOCATE),                      │
│  │           opentargets_get_target, opentargets_get_associations             │
│  ├── PubChem: pubchem_search_compounds (LOCATE), pubchem_get_compound        │
│  └── IUPHAR: iuphar_search_ligands, iuphar_get_ligand,                      │
│              iuphar_search_targets, iuphar_get_target                         │
├──────────────────────────────────────────────────────────────────────────────┤
│  TIER 3: PATHWAYS & CLINICAL                                                  │
│  ├── WikiPathways: wikipathways_search_pathways,                             │
│  │           wikipathways_get_pathway, wikipathways_get_pathways_for_gene,    │
│  │           wikipathways_get_pathway_components                              │
│  └── ClinicalTrials: clinicaltrials_search_trials (LOCATE),                  │
│              clinicaltrials_get_trial, clinicaltrials_get_trial_locations     │
├──────────────────────────────────────────────────────────────────────────────┤
│  TIER 4: GENOMICS & IDENTIFIERS                                               │
│  ├── Ensembl: ensembl_search_genes (LOCATE), ensembl_get_gene,               │
│  │            ensembl_get_transcript                                          │
│  └── Entrez: entrez_search_genes (LOCATE), entrez_get_gene,                  │
│              entrez_get_pubmed_links                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│  DIRECT API (curl — for GraphQL & edge discovery when MCP unavailable)        │
│  ├── Open Targets GraphQL: knownDrugs, associatedDiseases, tractability      │
│  ├── ChEMBL /mechanism: Drug → Target edges                                  │
│  └── STRING /enrichment: Protein Set → GO/KEGG terms                         │
├──────────────────────────────────────────────────────────────────────────────┤
│  GRAPHITI (Persistence)                                                       │
│  └── persist_to_graphiti: Save validated subgraph as JSON episode             │
└──────────────────────────────────────────────────────────────────────────────┘
```

## MCP Token Budgeting (`slim` Parameter)

ALL 34 MCP tools support a `slim` parameter for phase-specific token budgeting:

**Phase-Specific Usage:**
- **LOCATE phases (1 ANCHOR, 3 EXPAND)**: Use `slim=true, page_size=3-5` for fast candidate lists
- **RETRIEVE phases (2 ENRICH, 4 TRAVERSE, 5 VALIDATE)**: Use `slim=false` (default) for full metadata

**Token Savings:**
- `slim=true`: ~20 tokens/entity (ID, symbol, name only)
- `slim=false`: ~115-300 tokens/entity (full metadata + cross-references)

**Example (Phase 1 ANCHOR):**
```
# LOCATE: Find gene candidates with slim=true
Call `hgnc_search_genes` with: {"query": "ACVR", "slim": true, "page_size": 5}
→ Returns 5 candidates at ~20 tokens each = 100 tokens total

# RETRIEVE: Get full record for selected candidate
Call `hgnc_get_gene` with: {"hgnc_id": "HGNC:171"}
→ Returns complete metadata (~115 tokens)
```

**Impact:** Using `slim=true` during LOCATE phases enables batch resolution of 10-50 entities per LLM turn, critical for network expansion (Phase 3) and drug discovery (Phase 4a).

**Reference:** Token budgeting pattern documented in `reference/prior-art-api-patterns.md` (Section 7.1).

## CURIE Format Conventions

Two contexts require different ID formats:

### API Arguments (bare IDs)
Use bare IDs matching what the MCP server or API accepts:
- `"Q04771"` for UniProt
- `"CHEMBL25"` for ChEMBL compounds
- `"9606.ENSP00000269305"` for STRING proteins
- `"ENSG00000141510"` for Ensembl genes
- `"HGNC:11998"` for HGNC (includes prefix — this is how HGNC API works)

### Graph Node IDs (full CURIEs for Graphiti)
Use `PREFIX:LOCAL_ID` format for persistence:
- `"HGNC:11998"` for genes
- `"UniProtKB:P04637"` for proteins
- `"CHEMBL:3137309"` for compounds
- `"STRING:9606.ENSP00000269305"` for STRING proteins
- `"NCT03312634"` for trials (no prefix needed — NCT is the standard)
- `"EFO:0000574"` or `"MONDO:0018875"` for diseases
- `"WP:WP1742"` for pathways

## Fuzzy-to-Fact Execution Checklist

- [ ] Phase 1 ANCHOR: LOCATE gene/drug/disease → RETRIEVE canonical CURIEs
- [ ] Phase 2 ENRICH: RETRIEVE metadata for each CURIE (UniProt function, cross-refs)
- [ ] Phase 3 EXPAND: LOCATE interaction partners → RETRIEVE pathway membership
- [ ] Phase 4a TRAVERSE_DRUGS: LOCATE drugs targeting identified proteins → RETRIEVE mechanisms
- [ ] Phase 4b TRAVERSE_TRIALS: LOCATE trials for identified drugs → RETRIEVE trial details
- [ ] Phase 5 VALIDATE: RETRIEVE verification for every NCT ID, drug mechanism, gene-disease link
- [ ] Phase 6a PERSIST: Format validated graph as JSON → persist to Graphiti
- [ ] Phase 6b REPORT: Select template → grade evidence → format final report (lifesciences-reporting skill)

## Phase 1: ANCHOR — Entity Resolution

**Goal**: Resolve every gene, drug, and disease in the user's query to canonical CURIEs.

**LOCATE** (always start with HGNC for genes — fastest, most reliable):

PRIMARY (MCP tool):
```
Call `hgnc_search_genes` with: {"query": "TP53"}
→ Returns candidates with HGNC IDs → select best match: HGNC:11998
```

FALLBACK (curl):
```bash
curl -s "https://rest.genenames.org/search/symbol/TP53" \
  -H "Accept: application/json" | jq '.response.docs[0] | {hgnc_id, symbol, name}'
```

**RETRIEVE** (get full record with cross-references):

PRIMARY (MCP tool):
```
Call `hgnc_get_gene` with: {"hgnc_id": "HGNC:11998"}
→ Returns: symbol, name, UniProt cross-ref, Ensembl cross-ref, Entrez cross-ref
```

FALLBACK (curl):
```bash
curl -s "https://rest.genenames.org/fetch/hgnc_id/11998" \
  -H "Accept: application/json" | jq '.response.docs[0]'
```

**For drugs** (try ChEMBL search, note failure for Phase 4a fallback):

PRIMARY (MCP tool):
```
Call `chembl_search_compounds` with: {"query": "Venetoclax"}
→ If 500 error: note it, move on — drugs resolved in Phase 4a via Open Targets
```

**For diseases** (use ClinicalTrials.gov or Open Targets search):

PRIMARY (MCP tool):
```
Call `clinicaltrials_search_trials` with: {"query": "fibrodysplasia ossificans progressiva"}
```

**Output**: JSON with resolved entities:
```json
{
  "entities": [
    {"mention": "TP53", "type": "Gene", "curie": "HGNC:11998", "symbol": "TP53", "status": "resolved"},
    {"mention": "FOP", "type": "Disease", "curie": "MONDO:0018875", "status": "resolved"}
  ],
  "unresolved": []
}
```

## Phase 2: ENRICH — Metadata Enrichment

**Goal**: Decorate each resolved entity with metadata and cross-references. UniProt function text is the most valuable output.

**RETRIEVE** gene metadata (captures cross-references for downstream phases):

PRIMARY (MCP tool):
```
Call `hgnc_get_gene` with: {"hgnc_id": "HGNC:11998"}
→ Extract: uniprot_id="P04637", ensembl_id="ENSG00000141510", entrez_id="7157"
```

**RETRIEVE** protein function (reveals interactors, pathways, disease connections):

PRIMARY (MCP tool):
```
Call `uniprot_get_protein` with: {"uniprot_id": "P04637"}
→ Parse function text for interactor mentions: BAX, BCL2, FAS, MDM2
```

**RETRIEVE** drug metadata (if drug was resolved in Phase 1):

PRIMARY (MCP tool):
```
Call `chembl_get_compound` with: {"chembl_id": "CHEMBL3137309"}
→ May return 500 — note failure, continue
```

**LOCATE** disease CURIE (use Ensembl ID from HGNC cross-references above):

PRIMARY (MCP tool):
```
Call `opentargets_get_associations` with: {"ensembl_id": "ENSG00000115170"}
→ Returns diseases with MONDO/EFO/Orphanet IDs + association scores
→ Pick the highest-scoring disease matching the user's query
→ Record disease CURIE (e.g., MONDO:0007606 for FOP) for Phase 4a/4b
```

**Disease CURIE Optionality**:
- REQUIRED if drug discovery (Phase 4a) or clinical trial search (Phase 4b) is in scope
- OPTIONAL for gene network questions (Template 2) without therapeutic focus
- If query is about biological mechanisms (not therapeutics), disease CURIE may be omitted

FALLBACK (curl):
```bash
curl -s -X POST "https://api.platform.opentargets.org/api/v4/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ target(ensemblId: \"ENSG00000115170\") { associatedDiseases(page: {index: 0, size: 5}) { rows { disease { name id } score } } } }"}'
```

**Critical outputs for downstream phases**:
- Ensembl ID (ENSG...) → needed by Phase 4a for Open Targets GraphQL
- UniProt ID → needed by Phase 3 for STRING
- Interactor mentions from function text → guides Phase 3 expansion
- **Disease CURIE** (MONDO/EFO ID) → needed by Phase 4a/4b for drug/trial filtering (OPTIONAL if Phases 4a/4b not in scope)

## Phase 3: EXPAND — Network Expansion

**Goal**: Build adjacency list from interaction databases.

**LOCATE** STRING protein ID:

PRIMARY (MCP tool):
```
Call `string_search_proteins` with: {"query": "TP53", "species": 9606}
→ Returns: 9606.ENSP00000269305
```

**RETRIEVE** protein interactions:

PRIMARY (MCP tool):
```
Call `string_get_interactions` with: {"string_id": "9606.ENSP00000269305", "species": 9606, "required_score": 700}
→ Returns: MDM2 (0.999), SIRT1 (0.999), ATM (0.995), BCL2
```

**RETRIEVE** pathway membership:

PRIMARY (MCP tool):
```
Call `wikipathways_get_pathways_for_gene` with: {"gene_id": "TP53"}
```

**RETRIEVE** gene-disease associations (Open Targets):

PRIMARY (MCP tool):
```
Call `opentargets_get_associations` with: {"ensembl_id": "ENSG00000141510"}
→ Returns associated diseases with scores
```

FALLBACK (curl — for custom GraphQL queries):
```bash
curl -s -X POST "https://api.platform.opentargets.org/api/v4/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ target(ensemblId: \"ENSG00000141510\") { associatedDiseases(page: {index: 0, size: 5}) { rows { disease { name id } score } } } }"}'
```

**Pitfalls**:
- STRING batch queries (multiple proteins) return protein names; single queries may NOT. Prefer batch.
- STRING rate limit is 1 req/s.
- Always use `species=9606` (human) unless explicitly doing comparative genomics.
- BioGRID requires `BIOGRID_API_KEY` — check with `grep BIOGRID_API_KEY .env`.

## Phase 4a: TRAVERSE_DRUGS — Drug Discovery

**Goal**: Find drugs targeting identified proteins. Open Targets is the PRIMARY source (more reliable than ChEMBL).

**LOCATE** drugs via Open Targets (preferred — returns drugs + mechanisms + phases in one call):

PRIMARY (MCP tool):
```
Call `opentargets_get_target` with: {"ensembl_id": "ENSG00000171791"}
→ Returns knownDrugs with drug name, mechanismOfAction, phase
```

FALLBACK (curl — for full GraphQL control):
```bash
curl -s -X POST "https://api.platform.opentargets.org/api/v4/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ target(ensemblId: \"ENSG00000171791\") { knownDrugs(size: 25) { rows { drug { name id } mechanismOfAction phase } } } }"}'
```

**Open Targets `knownDrugs` Pagination**:
- Use `size` parameter only (e.g., `size: 25`) — this is the reliable pattern
- Do NOT use `page` or `index` — these cause intermittent failures
- For paginated results, use `cursor` (returned in the response) as the continuation token
- If first query fails, retry with `size` only (no other pagination params)

**LOCATE** drugs via ChEMBL (secondary fallback — frequently 500s on detail endpoints):

PRIMARY (MCP tool):
```
Call `chembl_search_compounds` with: {"query": "BCL2 inhibitor"}
→ Search endpoint is generally reliable
```

**Gain-of-Function Disease Filter** (CRITICAL for diseases like FOP):
```
For GAIN-OF-FUNCTION diseases (e.g., FOP caused by constitutive ACVR1 activation),
you need INHIBITORS or ANTAGONISTS. Do NOT return agonists — they worsen the disease.

Check the "mechanismOfAction" field from Open Targets:
- INCLUDE: "inhibitor", "antagonist", "negative modulator", "antibody (blocking)"
- EXCLUDE: "agonist", "positive modulator", "activator"
```

**Pitfalls**:
- Open Targets GraphQL `knownDrugs`: use `size` only (e.g., `size: 25`). Do NOT use `page`/`index`. Use `cursor` for pagination.
- The Ensembl ID (ENSG...) is required for Open Targets target queries — get from Phase 2.
- ChEMBL detail endpoints (`chembl_get_compound`) often return 500 errors; search endpoints (`chembl_search_compounds`) are generally reliable.
- Do NOT retry ChEMBL more than once — switch to Open Targets.

## Phase 4b: TRAVERSE_TRIALS — Clinical Trial Discovery

**Goal**: Find clinical trials for identified drugs. Can run in parallel with Phase 4a.

**LOCATE** trials by drug + disease:

PRIMARY (MCP tool):
```
Call `clinicaltrials_search_trials` with: {"query": "venetoclax AND leukemia"}
→ Returns trials with NCT IDs, phases, statuses
```

FALLBACK (curl):
```bash
curl -s "https://clinicaltrials.gov/api/v2/studies?query.cond=cancer&query.intr=venetoclax&pageSize=5&format=json" \
  | jq '.studies[] | {nct: .protocolSection.identificationModule.nctId, title: .protocolSection.identificationModule.briefTitle, phase: .protocolSection.designModule.phases, status: .protocolSection.statusModule.overallStatus}'
```

**Fallback** — disease-only search (when drug-specific search returns zero):
```bash
curl -s "https://clinicaltrials.gov/api/v2/studies?query.cond=fibrodysplasia+ossificans+progressiva&pageSize=10&format=json"
```

**ClinicalTrials.gov v2 Valid Parameters**:
- `query.cond` — condition/disease
- `query.intr` — intervention/drug
- `query.term` — general search (supports `AREA[StudyType]INTERVENTIONAL`)
- `filter.overallStatus` — e.g., `RECRUITING`, `COMPLETED`
- `pageSize` — results per page
- `format` — `json`

**Invalid parameter**: `filter.studyType` does NOT exist in v2 API. Use `query.term=AREA[StudyType]INTERVENTIONAL` instead.

**Pitfalls**:
- Use SPECIFIC drug names from Phase 4a output, NOT broad terms like "inhibitor".
- Search for each drug separately to avoid missing trials.
- If drug-specific search returns zero, try disease-only search as fallback.

## Phase 5: VALIDATE — Fact Verification

**Goal**: Verify every NCT ID, drug mechanism, and gene-disease claim. Prevents hallucinations.

**RETRIEVE** trial verification:

PRIMARY (MCP tool):
```
Call `clinicaltrials_get_trial` with: {"nct_id": "NCT03312634"}
→ If "Entity Not Found" → mark as INVALID
```

**RETRIEVE** cross-database ID verification:

FALLBACK (curl — for Ensembl xrefs):
```bash
curl -s "https://rest.ensembl.org/xrefs/id/ENSG00000141510?content-type=application/json" \
  | jq '.[] | select(.dbname | test("HGNC|UniProt|OMIM|RefSeq")) | {db: .dbname, id: .primary_id}'
```

**Validation checklist**:
- [ ] Every NCT ID verified via `clinicaltrials_get_trial`
- [ ] Drug mechanisms match what Open Targets/ChEMBL reported
- [ ] Gene-protein ID mappings consistent across HGNC, UniProt, Ensembl
- [ ] No entity was introduced from parametric knowledge (everything traces to a tool call)

**Verdicts**: Mark each fact as `VALIDATED`, `INVALID` (with reason), or `UNVERIFIABLE`.

## Phase 6a: PERSIST — Graph Persistence

**Goal**: Format validated graph as JSON and persist to Graphiti.

**Structure** (only include VALIDATED entities and relationships):
```python
graph_data = {
    "nodes": [
        {"id": "HGNC:11998", "type": "Gene", "label": "TP53", "properties": {"ensembl": "ENSG00000141510"}},
        {"id": "HGNC:990", "type": "Gene", "label": "BCL2", "properties": {"ensembl": "ENSG00000171791"}},
        {"id": "CHEMBL:3137309", "type": "Compound", "label": "Venetoclax", "properties": {"phase": 4}}
    ],
    "edges": [
        {"source": "HGNC:11998", "target": "HGNC:990", "type": "REGULATES", "properties": {}},
        {"source": "CHEMBL:3137309", "target": "HGNC:990", "type": "INHIBITOR", "properties": {"mechanism": "BCL2 inhibitor"}}
    ]
}
```

**Persist** (if Graphiti is available):
```python
persist_to_graphiti(
    name="TP53-BCL2-Venetoclax pathway",
    episode_body=json.dumps(graph_data),
    source="json",
    group_id="drug-repurposing"
)
```

## Phase 6b: REPORT — Formatted Report with Evidence Grading

**Goal**: Produce a professional report using the **lifesciences-reporting** skill.

Use the `lifesciences-reporting` skill to format the Phases 1-5 output. The skill will:
1. **Template selection**: Route query through its Template Decision Tree (7 templates)
2. **Evidence grading**: Apply L1-L4 levels + modifiers to all claims
3. **Confidence calculation**: Compute median of all claim scores (resistant to outliers)
4. **Source attribution**: Include `[Source: tool(param)]` on every factual claim

The reporting skill consumes Phases 1-5 output and the graph structure from Phase 6a. It does NOT make new API calls.

**Fallback** (if reporting skill unavailable):
```
## Summary
[Direct answer with source citations on every claim]

## Confidence
[State that full evidence grading was not performed and why]
```

## Edge Discovery Commands

These curl commands are for edge types not covered by MCP tools:

| Edge Type | Command |
|-----------|---------|
| Drug → Target | `curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id={ID}&format=json"` |
| Target → Drugs | Open Targets `knownDrugs` GraphQL (preferred) or `curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?target_chembl_id={ID}&format=json"` |
| Drug → Disease | `curl -s "https://www.ebi.ac.uk/chembl/api/data/drug_indication?molecule_chembl_id={ID}&format=json"` |
| Gene → Disease | Open Targets `associatedDiseases` GraphQL |
| Gene → Orthologs | `curl -s "https://rest.ensembl.org/homology/id/human/{ENSG}?type=orthologues&content-type=application/json"` |
| Protein Set → GO | `curl -s "https://string-db.org/api/json/enrichment?identifiers={IDs}&species=9606"` |
| Gene → PubMed | `curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=pubmed&id={ID}&retmode=json"` |

## Node Types

| Type | CURIE Pattern | API Argument Format |
|------|---------------|---------------------|
| Gene | `HGNC:\d+` | `"HGNC:11998"` (HGNC includes prefix) |
| Protein | `UniProtKB:[A-Z0-9]+` | `"P04637"` (bare accession) |
| Compound | `CHEMBL:\d+` | `"CHEMBL3137309"` (bare, no colon) |
| Target | `CHEMBL:\d+` | `"CHEMBL4860"` (bare) |
| Disease | `EFO:\d+` or `MONDO:\d+` | Varies by API |
| Pathway | `WP:WP\d+` | `"WP1742"` (bare) |
| Trial | `NCT\d+` | `"NCT03312634"` (bare) |
| STRING Protein | `STRING:9606.ENSP\d+` | `"9606.ENSP00000269305"` (bare) |

## Edge Types

| Edge | Source → Target | Key Properties |
|------|----------------|----------------|
| ENCODES | Gene → Protein | — |
| REGULATES | Gene → Gene | direction: activation/repression |
| INTERACTS | Protein → Protein | score, evidence_type |
| INHIBITOR | Compound → Target | Ki, IC50 |
| AGONIST | Compound → Target | EC50 |
| TREATS | Compound → Disease | max_phase |
| ASSOCIATED_WITH | Gene → Disease | score, evidence_sources |
| MEMBER_OF | Gene → Pathway | — |

## API Reliability & Fallback Patterns

| Primary Source | Fallback | When to Switch |
|---------------|----------|----------------|
| ChEMBL `chembl_get_compound` | Open Targets `opentargets_get_target` | On 500 error (common for detail endpoints) |
| ChEMBL `chembl_search_compounds` | (generally reliable) | Retry once, then report failure |
| STRING `string_get_interactions` | BioGRID `biogrid_get_interactions` | On <3 interactions returned |
| WikiPathways | STRING `/enrichment` endpoint | On no pathways found |
| ClinicalTrials.gov drug search | Disease-only search | On zero results for drug+disease |

## Query Best Practices

### Human-Centric Defaults
- Default to `species=9606` (human) for gene/protein searches
- Use `page_size=10` for exploration, `page_size=50` for batch operations
- Only omit organism filter for comparative genomics across species

### Drug Discovery vs Repurposing
- **Drug repurposing**: Use `phase >= 2` (clinical validation, shorter approval path)
- **General discovery**: No phase filter (include preclinical tools, mechanism probes)
- **Always check mechanisms** before bioactivity data

### Clinical Trial Defaults
- Default `filter.overallStatus=RECRUITING` for active research
- No phase filter for full landscape view
- Use phase filter only for specific analysis (PHASE3+ for commercialization)

## See Also

- **lifesciences-genomics**: HGNC, Ensembl, NCBI gene resolution endpoints (Phases 1-2)
- **lifesciences-proteomics**: UniProt, STRING, BioGRID interaction endpoints (Phases 2-3)
- **lifesciences-pharmacology**: ChEMBL, PubChem, IUPHAR, Open Targets drug endpoints (Phase 4a)
- **lifesciences-clinical**: Open Targets associations, ClinicalTrials.gov trial endpoints (Phases 4b, 5)
- **lifesciences-crispr**: BioGRID ORCS essentiality validation (extends Phase 3 with CRISPR screen data)
- **lifesciences-reporting**: Domain-specific report templates and evidence grading (Phase 6b)

### MCP Server Reference

All 34 tools are available via the `lifesciences-research` MCP server.
Gateway source: `/home/donbr/graphiti-org/lifesciences-research/src/lifesciences_mcp/servers/gateway.py`

---
name: lifesciences-cq-eval
description: Execute and score competency questions against live MCP tools and curl patterns. Validates data federation accuracy by comparing tool results to gold standard mechanistic paths.
license: Complete terms in LICENSE.txt
---

# Competency Question Evaluation Skill

## Purpose

Execute competency questions (CQs) from the golden test set against live data federation tools. Each CQ defines a gold standard mechanistic path (e.g., Drug→Target→Gene→Disease) and a workflow of validation steps. This skill orchestrates those steps, records results via the `cq-eval` MCP server, and generates scored reports.

**This is NOT RAG evaluation.** CQs validate structured API access and data federation — the ability to resolve entities across databases, discover mechanistic edges, and reconstruct biological paths. This aligns with the BTE-RAG benchmark methodology (Xu et al. 2025) which measured accuracy improvements from federated API access (+24.8pp for GPT-4o mini).

## Architecture Alignment

Per `prior-art-api-patterns.md` §7.5 (Three-Tier Architecture):

| Tier | Role | CQ Evaluation Target |
|------|------|---------------------|
| **Tier 1: MCP Tools** | Verified node retrieval (Fuzzy-to-Fact) | Entity resolution accuracy |
| **Tier 2: curl Skills** | Relationship edge discovery | Edge coverage and mechanism retrieval |
| **Tier 3: Graphiti** | Research memory | Path documentation completeness |

Per §7.6 (Competency Questions as Validation):
> CQs serve dual purpose — scope definition AND benchmark validation.

## Scoring Methodology

Aligned with BTE-RAG benchmark patterns (federated API evaluation, not document retrieval):

| Metric | Weight | What It Measures |
|--------|--------|-----------------|
| **Entity Score** | 0.40 | Fraction of gold standard CURIEs correctly resolved via Tier 1 MCP tools |
| **Edge Score** | 0.40 | Fraction of mechanistic edges validated via Tier 1 or Tier 2 patterns |
| **Path Complete** | 0.20 | Bonus: full gold standard path reconstructed end-to-end |
| **Overall** | 1.00 | Weighted composite |

## Workflow: Executing a CQ

### Step 0: Load the CQ

```
Use: cq_get(cq_id="cq1")
Returns: Gold standard entities, edges, workflow steps
```

### Step 1: Entity Resolution (Tier 1 — MCP Tools)

For each entity in the gold standard path, execute the Fuzzy-to-Fact protocol:

```
Phase 1 (LOCATE):  ~~gene databases search_genes("ACVR1") → candidates
Phase 2 (RETRIEVE): ~~gene databases get_gene("HGNC:171") → authoritative record
```

After each resolution, record the step:
```
Use: cq_record_step(
    cq_id="cq1",
    step_id="entity_acvr1",
    status="pass",
    expected_curie="HGNC:171",
    actual_curie="HGNC:171",
    tool_used="hgnc_search_genes → hgnc_get_gene",
    tier="tier1"
)
```

### Step 2: Edge Discovery (Tier 2 — curl or MCP)

For mechanistic edges, use the skill's documented curl patterns:

```bash
# Mechanism retrieval (Tier 2 — intentional design per §7.5)
curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL2105648&format=json"
```

Record the result:
```
Use: cq_record_step(
    cq_id="cq1",
    step_id="edge_drug_target",
    status="pass",
    expected_curie="CHEMBL:2003",
    actual_curie="CHEMBL:2003",
    tool_used="curl chembl/mechanism",
    tier="tier2",
    notes="action_type=AGONIST, direct_interaction=True"
)
```

### Step 3: Regulatory / Network Edges

For edges requiring protein interaction or pathway data:

```
Use: ~~protein databases string_get_interactions("STRING:9606.ENSP...")
 OR: ~~pathway databases wikipathways_get_pathways_for_gene("RARG")
```

### Step 4: Disease Association (Tier 1)

```
Use: ~~gene databases opentargets_get_associations(target_id="ENSG00000115170")
```

### Step 5: Score

```
Use: cq_score(cq_id="cq1")
Returns: entity_score, edge_score, path_complete, overall_score
```

## Parallel Validation Pattern

For CQs involving dataset-dependent evidence (e.g., CQ8 synthetic lethality, CQ14 CRISPR essentiality), run skill workflow AND Synapse query in parallel:

```
# Skill path (Tier 1/2)
Use: ~~gene databases biogrid_get_interactions("BRCA1", slim=True)

# Synapse path (complementary)
Use: search_synapse(query_term="BRCA1 synthetic lethality", entity_type="file")
```

Compare results for cross-validation. Neither replaces the other.

## Comparing Tool Implementations

When evaluating whether an alternative tool (e.g., DeepSense ChEMBL MCP) produces equivalent results to the authoritative source (e.g., curl to ChEMBL REST API):

1. Select 5-10 entities from the CQ catalog with well-known properties
2. Execute both paths for each entity
3. Compare key fields (action_type, target_chembl_id, direct_interaction)
4. Record discrepancies as step notes
5. Use `cq_compare` to track concordance over time

**Important**: Do not prefer an unvalidated tool over a validated Tier 2 curl pattern (§7.5). Validation must precede recommendation.

## Output: CQ Evaluation Report

After scoring, generate a report with:

1. **Header**: CQ id, title, timestamp, overall score
2. **Entity Resolution Table**: Each entity with expected vs actual CURIE, status
3. **Edge Coverage Table**: Each edge with relation, evidence tier, validation status
4. **Path Visualization**: Gold standard path with pass/fail annotations
5. **Findings**: Any gaps, discrepancies, or validation notes
6. **Trend**: If prior results exist, show score trajectory via `cq_compare`

## Established Frameworks and Prior Art

This evaluation approach draws from:

| Framework | Relevance | Reference |
|-----------|-----------|-----------|
| **BTE-RAG** (Xu et al. 2025) | DrugMechDB-derived benchmarks for federated API evaluation; 3 datasets (gene-centric, metabolite, drug-process) | DOI: 10.1101/2025.08.01.668022 |
| **CQsBEN** (Alharbi et al. 2024) | Benchmark framework for competency question engineering with evaluation criteria | EKAW 2024 proceedings |
| **PheKnowLator** (2024) | Benchmarks for KG construction tool validation and knowledge representation comparison | DOI: 10.1038/s41597-024-03171-w |
| **KG-Based Thought** (Wang et al. 2025) | KG validation of LLM responses for drug-cancer associations | DOI: 10.1093/gigascience/giae082 |
| **TRAPI** (NCATS Translator) | Standardized biomedical KG query patterns; CURIE-based entity resolution | github.com/NCATSTranslator/ReasonerAPI |

As the test set matures, look for opportunities to align CQ structure with DrugMechDB path format for cross-benchmark comparison.

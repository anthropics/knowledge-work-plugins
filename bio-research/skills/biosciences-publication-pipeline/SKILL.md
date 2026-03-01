---
name: biosciences-publication-pipeline
description: "Produces publication-quality outputs from completed Fuzzy-to-Fact pipeline data: formatted report, knowledge graph JSON with Synapse grounding, quality review, and BioRxiv preprint draft. Use when the user asks to 'publish results', 'create publication outputs', 'generate biorxiv draft', 'run publication pipeline', 'format for publication', or mentions producing manuscript-ready files from pipeline output."
---

# Biosciences Publication Pipeline

Transform completed Fuzzy-to-Fact pipeline output (Phases 1-6) into 5 publication-quality files.

## Scope and Grounding Rule

**In scope**: Formatting, template selection, evidence grading, Synapse.org dataset grounding, quality review, and manuscript drafting from existing pipeline data.

**Out of scope**: New API calls to life sciences databases (HGNC, UniProt, STRING, etc.). This skill consumes completed Phase 1-5 output -- it does NOT generate new facts.

**Exception**: Synapse MCP tools (`search_synapse`, `get_entity`, `get_entity_annotations`, `get_entity_children`) are permitted for Stage 1b grounding.

```
ALL claims in publication outputs MUST trace to specific tool calls from Phases 1-5.
Do NOT introduce new entities, drug names, gene functions, or trial IDs from
training knowledge. If pipeline data is missing for a section, report
"No data retrieved" with the tool name. Do NOT fill gaps from memory.
```

## Pipeline Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `slug` | Kebab-case identifier for the CQ | `doxorubicin-nf1-toxicity` |
| `output_dir` | Output directory path | `output/cqs/doxorubicin-nf1-toxicity/` |
| `cq_text` | The competency question text | "What known genes or pathways..." |
| `phase_6a_data` | Phase 6a JSON (from conversation or file) | KG JSON with nodes/edges |
| `phase_6b_narrative` | Phase 6b report narrative | Report text from graph-builder |

**File naming convention**: `{slug}-{type}.{ext}`

| File | Naming Pattern | Stage |
|------|---------------|-------|
| Report | `{slug}-report.md` | 1a |
| Knowledge Graph | `{slug}-knowledge-graph.json` | 1a |
| Synapse Grounding | `{slug}-synapse-grounding.md` | 1b |
| Quality Review | `{slug}-quality-review.md` | 2 |
| BioRxiv Draft | `{slug}-biorxiv-draft.md` | 3 |

## 4-Stage Workflow

```
                    +-----------------------+
                    |   Pipeline Input      |
                    | Phase 6a JSON +       |
                    | Phase 6b Narrative    |
                    +-----------+-----------+
                                |
                    +-----------v-----------+
            +-------+    STAGE 1 (parallel)  +-------+
            |       +------------------------+       |
            |                                        |
    +-------v-------+                    +-----------v-----------+
    | Stage 1a:     |                    | Stage 1b:             |
    | Report        |                    | Synapse               |
    | Formatter     |                    | Grounder              |
    | (report.md +  |                    | (synapse-grounding.md |
    |  KG JSON)     |                    |  + inject into JSON)  |
    +-------+-------+                    +-----------+-----------+
            |                                        |
            +-------------------+--------------------+
                                |
                    +-----------v-----------+
                    | Stage 2:              |
                    | Quality Reviewer      |
                    | (quality-review.md)   |
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    | Stage 3:              |
                    | BioRxiv Drafter       |
                    | (biorxiv-draft.md)    |
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    | Stage 4:              |
                    | Verification          |
                    | (automated checks)    |
                    +-----------------------+
```

## Stage 1a: Report Formatter

**Goal**: Produce `{slug}-report.md` and `{slug}-knowledge-graph.json`.

**Inputs**: Phase 6a JSON + Phase 6b narrative from conversation context or files.

**Process**:

1. **Template selection** via the `biosciences-reporting` skill decision tree:
   ```
   1. HOW does a drug work?              --> Template 6: Mechanism Elucidation
   2. Drug SAFETY or off-targets?        --> Template 7: Safety / Off-Target
   3. REGULATORY milestones or filings?  --> Template 5: Regulatory / Commercialization
   4. FIND or REPURPOSE drugs?           --> Template 1: Drug Discovery / Repurposing
   5. GENE/PROTEIN interactions?         --> Template 2: Gene / Protein Network
   6. CLINICAL TRIALS broadly?           --> Template 3: Clinical Landscape
   7. VALIDATE a target?                 --> Template 4: Target Validation
   8. Multiple categories?               --> Combine sections from relevant templates
   ```

2. **Evidence grading** using L1-L4 levels with modifiers:
   - L4 (0.90-1.00): Clinical -- FDA-approved or Phase 2+ with published endpoints
   - L3 (0.70-0.89): Functional -- Multi-DB concordance + druggable target
   - L2 (0.50-0.69): Multi-DB -- 2+ independent databases confirm
   - L1 (0.30-0.49): Single-DB -- One database source only
   - Modifiers: active trial (+0.10), mechanism match (+0.10), literature (+0.05), high STRING (+0.05), conflicting (-0.10), single source (-0.10), unverified (-0.15), mechanism mismatch (-0.20)

3. **Source attribution**: Every factual claim gets `[Source: tool(param)]` citation.

4. **KG JSON schema** (matches existing doxorubicin-toxicity pattern):
   ```json
   {
     "query": "{cq_text}",
     "disease": {"id": "...", "name": "...", "type": "Disease"},
     "nodes": [
       {
         "id": "HGNC:NNNNN",
         "type": "Gene",
         "label": "SYMBOL",
         "properties": {"symbol": "...", "name": "...", "ensembl": "...", "uniprot": "..."},
         "synapse_grounding": []
       }
     ],
     "edges": [
       {
         "source": "HGNC:NNNNN",
         "target": "HGNC:NNNNN",
         "type": "INTERACTS",
         "properties": {"score": 0.95},
         "synapse_grounding": []
       }
     ],
     "metadata": {
       "protocol": "Fuzzy-to-Fact",
       "phases_completed": ["ANCHOR","ENRICH","EXPAND","TRAVERSE_DRUGS","TRAVERSE_TRIALS","VALIDATE","PERSIST"],
       "date": "YYYY-MM-DD",
       "data_sources": [],
       "synapse_datasets": [],
       "notes": ""
     }
   }
   ```

**Outputs**: `{slug}-report.md`, `{slug}-knowledge-graph.json`

## Stage 1b: Synapse Grounder

**Goal**: Produce `{slug}-synapse-grounding.md` and inject `synapse_grounding` arrays into KG JSON.

**Runs in parallel with Stage 1a** (or sequentially if KG JSON needs to be finalized first).

**Synapse MCP Tools Used**:
- `search_synapse` -- keyword search across Synapse entities
- `get_entity` -- full metadata for candidate datasets
- `get_entity_annotations` -- structured annotations (species, platform, samples)
- `get_entity_children` -- explore container entities for sub-datasets

**Platform Suitability Check** (run BEFORE searching):

Synapse.org has uneven disease domain coverage. Check the matrix below and add fallback sources for underrepresented domains:

| Disease Domain | Synapse Coverage | Fallback Sources |
|---------------|-----------------|------------------|
| Neurodegenerative (AD, PD, ALS) | **High** | — (Synapse is primary) |
| Neurofibromatosis (NF1, NF2) | **High** | — (NF-OSI datasets) |
| Cancer genomics | **Moderate-High** | GEO (NCBI), cBioPortal |
| Cardiovascular | **Low** | GEO, ArrayExpress/BioStudies (EBI) |
| Lysosomal storage diseases | **Very Low** | GEO, disease-specific registries (Fabry Outcome Survey, Gaucher Registry) |
| Rare metabolic diseases | **Very Low** | GEO, ArrayExpress, OMIM, Orphanet |
| Infectious disease | **Low** | GEO, ImmPort, SRA |

If the disease domain has Low or Very Low coverage, document this in the grounding report's Limitations section and note which fallback sources would provide better coverage. The grounding agent should still search Synapse exhaustively but set expectations for low coverage.

**Search Query Construction** (build from entity labels in the KG, **compound queries first**):

| Priority | Entity Type | Query Pattern | Example |
|----------|-------------|--------------|---------|
| 1 (try first) | Compound + Disease | `"{compound} {disease}"` | `"doxorubicin cardiotoxicity"` |
| 1 (try first) | Gene + Disease | `"{gene} {disease}"` | `"GLA Fabry disease"` |
| 2 | Gene + Compound | `"{gene} {compound}"` | `"TOP2B doxorubicin"` |
| 3 | Pathway | `"{pathway_name}"` | `"NRF2 oxidative stress"` |
| 4 (fallback) | Drug name | `"{drug}"` | `"dexrazoxane"` |
| 4 (fallback) | Gene symbol only | `"{gene}"` | `"NFE2L2"` |

**Query priority**: Always start with compound queries (gene+disease, compound+disease) which have much higher precision. Fall back to single-term queries only when compound queries return zero relevant results. Short gene symbols (GLA, GAA, SI) generate extreme false-positive rates as standalone queries.

**Grounding Strength Classification**:

| Strength | Criteria |
|----------|----------|
| **Strong** | Dataset directly tests the mechanistic claim through perturbation (drug treatment, gene KO, enzyme assay) with relevant readout in the same disease |
| **Moderate** | Dataset profiles relevant genes/pathways in the same disease but design does not directly test the specific edge |
| **Analogous** | Dataset tests the same biological mechanism (e.g., lysosomal enzyme deficiency, ERT delivery) in a related disease or model system. The mechanism is shared but the specific gene/substrate/disease differs. |
| **Weak** | Dataset provides contextual or pathway-level support without gene/compound-specific evidence |

**When to use Analogous**: Cross-disease grounding is common for rare diseases with limited data. Examples:
- Gaucher ERT data grounding Fabry ERT claims (shared M6P-mediated lysosomal targeting)
- Sandhoff lysosomal accumulation data grounding Fabry accumulation claims (shared sphingolipid pathway)
- Cancer KO screen data grounding rare disease synthetic lethality claims (shared gene function)

**Analogous** is distinct from **Moderate** — Moderate means "right disease, indirect assay"; Analogous means "right mechanism, different disease."

**Edge Grounding Coverage Calculation**:

When calculating edge grounding coverage, **exclude MEMBER_OF edges from the denominator**. MEMBER_OF edges represent ontological pathway membership (from WikiPathways) and are definitional -- they are not amenable to experimental dataset grounding. Including them artificially deflates coverage percentages.

```
Example:
  Total edges: 20
  MEMBER_OF edges: 7
  Groundable edges: 20 - 7 = 13
  Grounded edges: 7
  Edge coverage: 7/13 = 54% (not 7/20 = 35%)
```

Report both the raw count and the adjusted denominator in the summary.

**Synapse Grounding Document Structure**:

1. Summary (node/edge coverage stats, with MEMBER_OF exclusion noted)
2. Dataset-to-Graph Mapping Table (Synapse ID, nodes grounded, edges grounded, evidence type, species, samples)
3. Node Grounding Coverage (each node: Grounded/Ungrounded with datasets)
4. Edge Grounding Coverage (grounded edges with evidence, ungrounded edges with notes; MEMBER_OF edges listed separately as "ontological -- not groundable")
5. Evidence Level Upgrades (L2->L2+, L1->L1+ where supported)
6. Grounding Confidence Matrix (claim, datasets, strength, justification)
7. Methodology (tools used, matching criteria, MEMBER_OF exclusion rationale)
8. Limitations (specificity, cross-species, platform age, coverage gaps)

**KG JSON Injection**: After grounding, add `synapse_grounding` arrays to matched nodes and edges in the KG JSON.

**Outputs**: `{slug}-synapse-grounding.md`, updated `{slug}-knowledge-graph.json`

## Stage 2: Quality Reviewer

**Goal**: Produce `{slug}-quality-review.md`.

**Inputs**: All Stage 1 outputs (report, KG JSON, Synapse grounding).

**Process**: Apply the `biosciences-reporting-quality-review` skill's 10-dimension framework:

| Dimension | What to Check |
|-----------|--------------|
| 1. CURIE Resolution | All entities use proper CURIEs (HGNC:NNNNN, CHEMBL:NNNNN) |
| 2. Source Attribution | >90% of claims cite `[Source: tool(param)]` |
| 3. LOCATE-RETRIEVE | Two-step pattern documented for entity types |
| 4. Disease CURIE | Present when required by template type |
| 5. OT Pagination | Uses `size`-only pattern for knownDrugs |
| 6. Evidence Grading | Claim-level numeric grading with modifiers |
| 7. GoF Filter | Agonists excluded for gain-of-function diseases |
| 8. Trial Validation | All NCT IDs verified via clinicaltrials_get_trial |
| 9. Completeness | CQ fully answered with all components |
| 10. Hallucination Risk | LOW/MEDIUM/HIGH assessment |

**File Read Order** (critical for accurate review):
1. `{slug}-knowledge-graph.json` -- check graph before concluding protocol gaps
2. `{slug}-report.md` -- evaluate against template and grading standards
3. `{slug}-synapse-grounding.md` -- verify cross-file consistency

**Failure Classification**:
- **Protocol failure**: Required step not executed (FAIL)
- **Presentation failure**: Step executed but not shown (PARTIAL)
- **Documentation error**: Step shown but incorrectly attributed (PARTIAL)

**Synapse Grounding Scoring Note**: When scoring Synapse grounding (0-10), use the adjusted edge coverage denominator that excludes MEMBER_OF edges. MEMBER_OF edges are ontological (pathway membership from WikiPathways) and cannot be grounded by experimental datasets.

**Output Format**:
1. Summary Verdict (PASS/PARTIAL/FAIL + template + top 3 issues)
2. Dimension Scores Table
3. Detailed Findings Per Dimension
4. Failure Classification
5. Overall Assessment (protocol 0-10, presentation 0-10, KG structure 0-10, Synapse grounding 0-10)

**Output**: `{slug}-quality-review.md`

## Stage 3: BioRxiv Drafter

**Goal**: Produce `{slug}-biorxiv-draft.md` in IMRaD format.

**Inputs**: All previous outputs (report, KG JSON, Synapse grounding, quality review).

**IMRaD Structure**:

| Section | Content | Target Length |
|---------|---------|--------------|
| Abstract | Background, Methods, Results, Conclusion | 250-350 words |
| 1. Introduction | CQ context, knowledge gap, protocol overview | 500-800 words |
| 2. Methods | Fuzzy-to-Fact protocol, data sources table, evidence grading, Synapse grounding methodology, quality assessment | 800-1200 words |
| 3. Results | KG overview, mechanistic findings (per axis), clinical trials, Synapse grounding, evidence assessment | 1500-2500 words |
| 4. Discussion | Key findings, CQ methodology, multi-DB concordance, Synapse validation, limitations, future directions | 800-1200 words |
| References | Numbered `[N]` from `[Source: tool(param)]` citations | All sources |
| Supplementary | S1: KG Nodes, S2: KG Edges, S3: Evidence Grading, S4: Synapse Mapping | Tables |

**Reference Conversion**: Convert `[Source: tool(param)]` inline citations to numbered references:
```
Inline: "TOP2A (HGNC:11989) is the anti-tumor target [1]."
Reference: [1] HGNC. Gene record for TOP2A (HGNC:11989). Retrieved via hgnc_get_gene(HGNC:11989).
```

**Reference Grouping**:
- Gene and Protein Databases
- Interaction and Pathway Databases
- Clinical Trials
- Compound Databases
- Synapse.org Datasets
- Genomic Databases

**Figure Descriptions** (text-only, no actual figures):
- Figure 1: Knowledge graph topology (node types, edge types, hub genes)
- Figure 2: Primary mechanistic model (varies by CQ)

**Output**: `{slug}-biorxiv-draft.md`

## Stage 4: Verification Checklist

**Goal**: Confirm all outputs are complete and consistent.

**Automated Checks**:

1. **File existence**: All 5 files exist in `{output_dir}`
   - `{slug}-report.md`
   - `{slug}-knowledge-graph.json`
   - `{slug}-synapse-grounding.md`
   - `{slug}-quality-review.md`
   - `{slug}-biorxiv-draft.md`

2. **JSON validity**: `{slug}-knowledge-graph.json` parses without errors

3. **Cross-file consistency**:
   - Node count matches between KG JSON and report
   - Edge count matches between KG JSON and report
   - Synapse dataset count matches between KG JSON metadata and Synapse grounding doc
   - Disease CURIE matches across all files
   - NCT IDs in report match those in BioRxiv draft

4. **No API keys or .env content** in any output file

5. **Quality review verdict**: Must be PASS or PARTIAL (not FAIL)

## See Also

- **biosciences-graph-builder**: Produces Phases 1-6 input data (prerequisite)
- **biosciences-reporting**: Template schemas and evidence grading (Stage 1a reference)
- **biosciences-reporting-quality-review**: 10-dimension evaluation framework (Stage 2 reference)
- **biosciences-genomics**: Gene resolution endpoints (Phase 1-2 data sources)
- **biosciences-proteomics**: Protein interaction endpoints (Phase 2-3 data sources)
- **biosciences-pharmacology**: Drug mechanism endpoints (Phase 4a data sources)
- **biosciences-clinical**: Trial and association endpoints (Phase 4b-5 data sources)

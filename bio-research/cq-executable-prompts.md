# CQ Executable Prompts

**Purpose**: Step-by-step instructions for running each of the 15 competency questions through the lifesciences-research MCP tools with automated scoring via the cq-eval MCP server.

**Prerequisites**:
- Life Sciences Gateway MCP (34 tools across 12 databases)
- Open Targets Platform MCP (`search_entities`, `query_open_targets_graphql`)
- ClinicalTrials.gov MCP (`search_trials`, `get_trial_details`)
- ChEMBL MCP (`compound_search`, `get_mechanism`, `get_bioactivity`)
- bioRxiv MCP (`search_preprints`)
- cq-eval MCP server (8 tools: `cq_list`, `cq_get`, `cq_add`, `cq_import_from_markdown`, `cq_record_step`, `cq_score`, `cq_results`, `cq_compare`)
- Graphiti (`graphiti-docker` for dev, `graphiti-aura` for prod)
- curl (Tier 2 edge discovery)

**Scoring**: BTE-RAG aligned — entity (0.4) + edge (0.4) + path_complete (0.2) = 1.0

---

## How to Use These Prompts

Each CQ prompt below follows the same 6-phase structure:

1. **LOAD** — Retrieve the CQ definition from the cq-eval catalog
2. **RESOLVE ENTITIES** — Fuzzy-to-Fact Phase 1 (LOCATE) + Phase 2 (RETRIEVE) via Tier 1 MCP tools; record each step
3. **DISCOVER EDGES** — Tier 1 MCP and/or Tier 2 curl; record each step
4. **SCORE** — Call `cq_score` to compute entity/edge/path metrics
5. **PERSIST** — Store results in Graphiti with the CQ's designated `group_id`
6. **REPORT** — Generate evaluation report markdown

To run a single CQ, copy its prompt section into a conversation with Claude that has the bio-research plugin active.

To run all 15, execute them sequentially or in parallel (CQs have no cross-dependencies).

---

## CQ1: FOP Mechanism (Palovarotene)

**Gold Standard Path**: `Drug(Palovarotene)` → `Protein(RARG)` → `Protein(ACVR1)` → `Disease(FOP)`

### Prompt

```
Execute CQ1 evaluation: "By what mechanism does Palovarotene treat FOP?"

PHASE 1 — LOAD:
cq_get(cq_id="cq1")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve Palovarotene
  chembl_search_compounds(query="palovarotene", slim=True)
  → expect CHEMBL:2105648
  cq_record_step(cq_id="cq1", step_id="entity_palovarotene", status="pass|fail",
    expected_curie="CHEMBL:2105648", actual_curie="<result>",
    tool_used="chembl_search_compounds", tier="tier1")

Step 2: Resolve RARG
  hgnc_search_genes(query="RARG", slim=True)
  → expect HGNC:9866
  cq_record_step(cq_id="cq1", step_id="entity_rarg", status="pass|fail",
    expected_curie="HGNC:9866", actual_curie="<result>",
    tool_used="hgnc_search_genes", tier="tier1")

Step 3: Resolve ACVR1
  hgnc_search_genes(query="ACVR1", slim=True)
  → expect HGNC:171
  cq_record_step(cq_id="cq1", step_id="entity_acvr1", status="pass|fail",
    expected_curie="HGNC:171", actual_curie="<result>",
    tool_used="hgnc_search_genes", tier="tier1")

Step 4: Resolve FOP
  ot search_entities(query_strings=["Fibrodysplasia Ossificans Progressiva"])
  → expect MONDO_0007606
  cq_record_step(cq_id="cq1", step_id="entity_fop", status="pass|fail",
    expected_curie="MONDO_0007606", actual_curie="<result>",
    tool_used="ot_search_entities", tier="tier1")

PHASE 3 — EDGE DISCOVERY:

Edge 1: Palovarotene → RARG (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL2105648&format=json"
  → expect action_type=AGONIST, target_chembl_id=CHEMBL2003
  cq_record_step(cq_id="cq1", step_id="edge_drug_rarg", status="pass|fail",
    expected_curie="CHEMBL:2003", actual_curie="<result>",
    tool_used="curl chembl/mechanism", tier="tier2",
    notes="action_type=<result>, direct_interaction=<result>")

Edge 2: RARG → ACVR1 (Tier 1 MCP)
  hgnc_get_gene(hgnc_id="HGNC:171")
  → confirm ACVR1 cross-references to ENSG00000115170
  cq_record_step(cq_id="cq1", step_id="edge_rarg_acvr1", status="pass|fail",
    expected_curie="ENSG00000115170", actual_curie="<result>",
    tool_used="hgnc_get_gene", tier="tier1",
    notes="BMP signaling regulatory link")

Edge 3: ACVR1 → FOP (Tier 1 MCP — Fuzzy-to-Fact)
  opentargets_search_targets(query="ACVR1", slim=True)
  → confirm Ensembl ID ENSG00000115170
  opentargets_get_associations(target_id="ENSG00000115170", disease_id="MONDO_0007606")
  → expect association score > 0
  cq_record_step(cq_id="cq1", step_id="edge_acvr1_fop", status="pass|fail",
    expected_curie="MONDO_0007606", actual_curie="<result>",
    tool_used="opentargets_search_targets + opentargets_get_associations", tier="tier1",
    notes="association_score=<result>")

PHASE 4 — SCORE:
  cq_score(cq_id="cq1")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(
    name="CQ1: Palovarotene mechanism for FOP",
    episode_body=<JSON of nodes/edges discovered>,
    source="json",
    group_id="cq1-fop-mechanism")

PHASE 6 — REPORT:
  Generate cq1-eval-report.md with entity table, edge table, scores, findings.
```

---

## CQ2: FOP Drug Repurposing (BMP Pathway)

**Gold Standard Path**: `Gene(ACVR1)` → `Pathway(BMP Signaling)` → `Gene(SMAD1/BMPR1A)` → `Drug(LDN-193189)`

### Prompt

```
Execute CQ2 evaluation: "What other drugs targeting the BMP Signaling Pathway could be repurposed for FOP?"

PHASE 1 — LOAD:
cq_get(cq_id="cq2")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve ACVR1
  hgnc_search_genes(query="ACVR1", slim=True)
  → expect HGNC:171
  cq_record_step(cq_id="cq2", step_id="entity_acvr1", ...)

Step 2: Resolve BMP Signaling Pathway
  wikipathways_search_pathways(query="BMP signaling")
  → expect WP:WP2760
  cq_record_step(cq_id="cq2", step_id="entity_bmp_pathway", status="pass|fail",
    expected_curie="WP:WP2760", actual_curie="<result>",
    tool_used="wikipathways_search_pathways", tier="tier1")

Step 3: Resolve LDN-193189
  chembl_search_compounds(query="LDN-193189", slim=True)
  → expect CHEMBL:405130
  cq_record_step(cq_id="cq2", step_id="entity_ldn193189", ...)

Step 4: Resolve Dorsomorphin
  chembl_search_compounds(query="dorsomorphin", slim=True)
  → expect CHEMBL:495727
  cq_record_step(cq_id="cq2", step_id="entity_dorsomorphin", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: ACVR1 → BMP Pathway (Tier 1)
  wikipathways_get_pathways_for_gene(gene_id="ACVR1")
  → expect WP:WP2760 in results
  cq_record_step(cq_id="cq2", step_id="edge_acvr1_bmp", ...)

Edge 2: Pathway Components (Tier 1)
  wikipathways_get_pathway_components(pathway_id="WP:WP2760")
  → expect SMAD1, SMAD5, BMPR1A among genes
  cq_record_step(cq_id="cq2", step_id="edge_pathway_genes", status="pass|fail",
    expected_curie="SMAD1,SMAD5,BMPR1A", actual_curie="<genes found>",
    tool_used="wikipathways_get_pathway_components", tier="tier1")

Edge 3: LDN-193189 → ACVR1 mechanism (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL405130&format=json"
  → expect INHIBITOR of BMP type I receptors
  cq_record_step(cq_id="cq2", step_id="edge_ldn_mechanism", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq2")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ2: BMP pathway drug repurposing for FOP",
    episode_body=<JSON>, source="json", group_id="cq2-fop-repurposing")

PHASE 6 — REPORT:
  Generate cq2-eval-report.md
```

---

## CQ3: Alzheimer's Gene-Protein Networks

**Gold Standard Path**: `Gene(APP)` → `Protein(BACE1/PSEN1)` → `Disease(AD)` + `Pathway(WP:WP2059)`

### Prompt

```
Execute CQ3 evaluation: "What genes and proteins are implicated in Alzheimer's Disease progression, and how do they interact?"

PHASE 1 — LOAD:
cq_get(cq_id="cq3")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve APP
  hgnc_search_genes(query="APP", slim=True)
  → expect HGNC:620
  cq_record_step(cq_id="cq3", step_id="entity_app", ...)

Step 2: Resolve APOE
  hgnc_search_genes(query="APOE", slim=True)
  → expect HGNC:613
  cq_record_step(cq_id="cq3", step_id="entity_apoe", ...)

Step 3: Resolve PSEN1
  hgnc_search_genes(query="PSEN1", slim=True)
  → expect HGNC:9508
  cq_record_step(cq_id="cq3", step_id="entity_psen1", ...)

Step 4: Resolve MAPT
  hgnc_search_genes(query="MAPT", slim=True)
  → expect HGNC:6893
  cq_record_step(cq_id="cq3", step_id="entity_mapt", ...)

Step 5: Resolve Alzheimer's Disease
  ot search_entities(query_strings=["Alzheimer disease"])
  → expect MONDO_0004975 or EFO equivalent
  cq_record_step(cq_id="cq3", step_id="entity_ad", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: APP protein interactions (Tier 1)
  string_search_proteins(query="APP", species=9606)
  → get STRING ID (expect STRING:9606.ENSP00000284981)
  string_get_interactions(string_id="STRING:9606.ENSP00000284981", required_score=700, limit=20)
  → expect BACE1, PSEN1 among interactors
  cq_record_step(cq_id="cq3", step_id="edge_app_interactions", ...)

Edge 2: APP → AD disease association (Tier 1 — Fuzzy-to-Fact)
  opentargets_search_targets(query="APP", slim=True)
  → confirm Ensembl ID ENSG00000142192
  opentargets_get_associations(target_id="ENSG00000142192", disease_id="MONDO_0004975")
  → expect association score > 0.5
  cq_record_step(cq_id="cq3", step_id="edge_app_ad", ...)

Edge 3: Alzheimer pathway (Tier 1)
  wikipathways_search_pathways(query="Alzheimer")
  → expect WP:WP2059
  cq_record_step(cq_id="cq3", step_id="edge_ad_pathway", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq3")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ3: AD gene-protein network",
    episode_body=<JSON>, source="json", group_id="cq3-alzheimers-gene-network")

PHASE 6 — REPORT:
  Generate cq3-eval-report.md
```

---

## CQ4: Alzheimer's Therapeutic Targets

**Gold Standard Path**: `Gene(BACE1)` → `Drug(inhibitors)` → `Trial(Phase 3)` + `Gene(MAPT/GSK3B)` → `Drug(Lecanemab)`

### Prompt

```
Execute CQ4 evaluation: "What drugs target amyloid-beta or tau proteins for Alzheimer's Disease treatment?"

PHASE 1 — LOAD:
cq_get(cq_id="cq4")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve BACE1
  hgnc_search_genes(query="BACE1", slim=True)
  → expect HGNC:933
  cq_record_step(cq_id="cq4", step_id="entity_bace1", ...)

Step 2: Resolve MAPT
  hgnc_search_genes(query="MAPT", slim=True)
  → expect HGNC:6893
  cq_record_step(cq_id="cq4", step_id="entity_mapt", ...)

Step 3: Resolve GSK3B
  hgnc_search_genes(query="GSK3B", slim=True)
  → expect HGNC:4617
  cq_record_step(cq_id="cq4", step_id="entity_gsk3b", ...)

Step 4: Resolve Lecanemab
  chembl_search_compounds(query="lecanemab", slim=True)
  → expect CHEMBL:4594344
  cq_record_step(cq_id="cq4", step_id="entity_lecanemab", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: BACE1 inhibitor drugs (Tier 1 + Tier 2)
  chembl_search_compounds(query="BACE1 inhibitor")
  → identify drug candidates
  curl -s "https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id=CHEMBL4822&standard_type=IC50&limit=10&format=json"
  → binding affinities
  cq_record_step(cq_id="cq4", step_id="edge_bace1_drugs", ...)

Edge 2: Lecanemab mechanism (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL4594344&format=json"
  → expect anti-amyloid mechanism
  cq_record_step(cq_id="cq4", step_id="edge_lecanemab_mechanism", ...)

Edge 3: AD clinical trials (Tier 1)
  clinicaltrials_search_trials(query="Alzheimer BACE", phase="PHASE3", slim=True)
  → expect active trials
  cq_record_step(cq_id="cq4", step_id="edge_ad_trials", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq4")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ4: AD therapeutic targets",
    episode_body=<JSON>, source="json", group_id="cq4-alzheimers-therapeutics")

PHASE 6 — REPORT:
  Generate cq4-eval-report.md
```

---

## CQ5: MAPK Regulatory Cascade

**Gold Standard Path**: `Protein(RAF1)` → `Protein(MAP2K1/MEK1)` → `Protein(MAPK1/ERK2)` with directional regulation

### Prompt

```
Execute CQ5 evaluation: "In the MAPK signaling cascade, which proteins regulate downstream targets and with what direction?"

PHASE 1 — LOAD:
cq_get(cq_id="cq5")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve RAF1
  string_search_proteins(query="RAF1", species=9606)
  → expect STRING:9606.ENSP00000251849
  cq_record_step(cq_id="cq5", step_id="entity_raf1", ...)

Step 2: Resolve MAP2K1
  string_search_proteins(query="MAP2K1", species=9606)
  → expect STRING:9606.ENSP00000302486
  cq_record_step(cq_id="cq5", step_id="entity_map2k1", ...)

Step 3: Resolve MAPK1
  string_search_proteins(query="MAPK1", species=9606)
  → expect STRING:9606.ENSP00000215832
  cq_record_step(cq_id="cq5", step_id="entity_mapk1", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: RAF1 → MAP2K1 interaction (Tier 1)
  string_get_interactions(string_id="STRING:9606.ENSP00000251849", required_score=700, limit=20)
  → expect MAP2K1 among interactors with high score
  cq_record_step(cq_id="cq5", step_id="edge_raf1_mek1", ...)

Edge 2: MAP2K1 → MAPK1 interaction (Tier 1)
  string_get_interactions(string_id="STRING:9606.ENSP00000302486", required_score=700, limit=20)
  → expect MAPK1 among interactors
  cq_record_step(cq_id="cq5", step_id="edge_mek1_erk2", ...)

Edge 3: MAPK pathway context (Tier 1)
  wikipathways_search_pathways(query="MAPK signaling")
  → expect WP:WP382
  cq_record_step(cq_id="cq5", step_id="edge_mapk_pathway", ...)

Edge 4: Cancer disease associations (Tier 1 — Fuzzy-to-Fact)
  opentargets_search_targets(query="MAP2K1", slim=True)
  → confirm Ensembl ID ENSG00000132155
  opentargets_get_associations(target_id="ENSG00000132155")
  → cancer-related associations
  cq_record_step(cq_id="cq5", step_id="edge_mapk_cancer", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq5")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ5: MAPK regulatory cascade",
    episode_body=<JSON>, source="json", group_id="cq5-mapk-regulatory-cascade")

PHASE 6 — REPORT:
  Generate cq5-eval-report.md

NOTE: STRING 12.5 provides network_type=regulatory for directed edges.
Use string_get_network_image_url(identifiers="RAF1\nMAP2K1\nMAPK1", network_flavor="actions")
to visualize the directional cascade.
```

---

## CQ6: BRCA1 Regulatory Network

**Gold Standard Path**: `TF(E2F1/SP1)` → `Gene(BRCA1)` → `Gene(RAD51)` with regulatory directionality

### Prompt

```
Execute CQ6 evaluation: "What transcription factors regulate BRCA1 expression, and what genes does BRCA1 regulate?"

PHASE 1 — LOAD:
cq_get(cq_id="cq6")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve BRCA1
  hgnc_search_genes(query="BRCA1", slim=True)
  → expect HGNC:1100
  cq_record_step(cq_id="cq6", step_id="entity_brca1", ...)

Step 2: Resolve E2F1
  hgnc_search_genes(query="E2F1", slim=True)
  → expect HGNC:3113
  cq_record_step(cq_id="cq6", step_id="entity_e2f1", ...)

Step 3: Resolve SP1
  hgnc_search_genes(query="SP1", slim=True)
  → expect HGNC:11205
  cq_record_step(cq_id="cq6", step_id="entity_sp1", ...)

Step 4: Resolve RAD51
  hgnc_search_genes(query="RAD51", slim=True)
  → expect HGNC:9817
  cq_record_step(cq_id="cq6", step_id="entity_rad51", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: BRCA1 protein interactions (Tier 1)
  string_search_proteins(query="BRCA1", species=9606)
  string_get_interactions(string_id=<result>, required_score=700, limit=30)
  → filter for regulatory edges pointing TO BRCA1 (upstream TFs)
  → filter for regulatory edges pointing FROM BRCA1 (downstream targets)
  cq_record_step(cq_id="cq6", step_id="edge_brca1_network", ...)

Edge 2: BioGRID interactions for physical evidence (Tier 1)
  biogrid_search_genes(query="BRCA1")
  biogrid_get_interactions(gene_symbol="BRCA1", slim=True, max_results=100)
  → count physical vs genetic interactions
  cq_record_step(cq_id="cq6", step_id="edge_brca1_biogrid", ...)

Edge 3: Network visualization
  string_get_network_image_url(identifiers="BRCA1\nE2F1\nSP1\nRAD51", network_flavor="evidence")

PHASE 4 — SCORE:
  cq_score(cq_id="cq6")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ6: BRCA1 regulatory network",
    episode_body=<JSON>, source="json", group_id="cq6-brca1-regulatory-network")

PHASE 6 — REPORT:
  Generate cq6-eval-report.md
```

---

## CQ7: NGLY1 Multi-Hop Drug Repurposing

**Gold Standard Path**: `Disease(NGLY1 deficiency)` → `Gene(NGLY1)` → `Pathway(N-glycanase)` → `Genes(pathway members)` → `Drugs(candidates)`

### Prompt

```
Execute CQ7 evaluation: "For NGLY1 deficiency, what are the associated genes, and what existing drugs target proteins in those pathways?"

PHASE 1 — LOAD:
cq_get(cq_id="cq7")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve NGLY1
  hgnc_search_genes(query="NGLY1", slim=True)
  → expect HGNC:17646
  cq_record_step(cq_id="cq7", step_id="entity_ngly1", ...)

Step 2: Resolve NGLY1 deficiency
  ot search_entities(query_strings=["NGLY1 deficiency"])
  → expect MONDO_0014109
  cq_record_step(cq_id="cq7", step_id="entity_ngly1_deficiency", ...)

Step 3: Resolve N-glycanase pathway
  wikipathways_search_pathways(query="NGLY1")
  → expect WP:WP5078 or related
  cq_record_step(cq_id="cq7", step_id="entity_ngly1_pathway", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: NGLY1 → Pathways (Tier 1)
  wikipathways_get_pathways_for_gene(gene_id="NGLY1")
  → list of pathways containing NGLY1
  cq_record_step(cq_id="cq7", step_id="edge_ngly1_pathways", ...)

Edge 2: Pathway components (Tier 1)
  wikipathways_get_pathway_components(pathway_id="WP:WP5078")
  → extract all member genes/proteins
  cq_record_step(cq_id="cq7", step_id="edge_pathway_components", ...)

Edge 3: Drug search for pathway members (Tier 1 + Tier 2)
  For top pathway proteins:
    chembl_search_compounds(query="<protein_name> inhibitor")
    curl ChEMBL /mechanism for each hit
  → identify druggable targets within the pathway
  cq_record_step(cq_id="cq7", step_id="edge_drug_candidates", ...)

Edge 4: Disease associations (Tier 1 — Fuzzy-to-Fact)
  opentargets_search_targets(query="NGLY1", slim=True)
  → resolve to Ensembl ID
  opentargets_get_associations(target_id="<NGLY1_ensembl_id>")
  → confirm NGLY1 deficiency association
  cq_record_step(cq_id="cq7", step_id="edge_ngly1_disease", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq7")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ7: NGLY1 multi-hop drug repurposing",
    episode_body=<JSON>, source="json", group_id="cq7-ngly1-drug-repurposing")

PHASE 6 — REPORT:
  Generate cq7-eval-report.md

NOTE: This CQ tests multi-hop reasoning (disease → gene → pathway → pathway genes → drugs).
The BioThings Explorer benchmark (Callaghan et al. 2023) validated this pattern across 34 federated APIs.
```

---

## CQ8: ARID1A Synthetic Lethality

**Gold Standard Path**: `Gene(ARID1A)` → `Complex(SWI/SNF)` → `Gene(EZH2)` [SL partner] → `Drug(Tazemetostat)` → `Trial(NCT03348631)`

### Prompt

```
Execute CQ8 evaluation: "How can we identify therapeutic strategies for ARID1A-deficient Ovarian Cancer using synthetic lethality?"

PHASE 1 — LOAD:
cq_get(cq_id="cq8")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve ARID1A
  hgnc_search_genes(query="ARID1A", slim=True)
  → expect HGNC:11110
  cq_record_step(cq_id="cq8", step_id="entity_arid1a", ...)

Step 2: Resolve EZH2
  hgnc_search_genes(query="EZH2", slim=True)
  → expect HGNC:3527
  cq_record_step(cq_id="cq8", step_id="entity_ezh2", ...)

Step 3: Resolve ATR
  hgnc_search_genes(query="ATR", slim=True)
  → expect HGNC:882
  cq_record_step(cq_id="cq8", step_id="entity_atr", ...)

Step 4: Resolve Tazemetostat
  chembl_search_compounds(query="tazemetostat", slim=True)
  → expect CHEMBL:3414621
  cq_record_step(cq_id="cq8", step_id="entity_tazemetostat", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: ARID1A protein function (Tier 1)
  uniprot_search_proteins(query="ARID1A", slim=True)
  uniprot_get_protein(uniprot_id="UniProtKB:O14497")
  → confirm SWI/SNF complex member
  cq_record_step(cq_id="cq8", step_id="edge_arid1a_swisnf", ...)

Edge 2: ARID1A interaction network (Tier 1)
  string_search_proteins(query="ARID1A", species=9606)
  string_get_interactions(string_id=<result>, required_score=700)
  → SWI/SNF complex members
  cq_record_step(cq_id="cq8", step_id="edge_arid1a_network", ...)

Edge 3: Tazemetostat mechanism (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL3414621&format=json"
  → expect EZH2 INHIBITOR
  cq_record_step(cq_id="cq8", step_id="edge_tazemetostat_mechanism", ...)

Edge 4: Clinical trial (Tier 1)
  clinicaltrials_search_trials(query="tazemetostat ARID1A ovarian", slim=True)
  → expect NCT:03348631 or similar
  cq_record_step(cq_id="cq8", step_id="edge_clinical_trial", ...)

PARALLEL VALIDATION (Synapse):
  search_synapse(query_term="ARID1A synthetic lethality", entity_type="file")
  → cross-validate with Synapse datasets

PHASE 4 — SCORE:
  cq_score(cq_id="cq8")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ8: ARID1A synthetic lethality in ovarian cancer",
    episode_body=<JSON>, source="json", group_id="cq8-arid1a-synthetic-lethality")

PHASE 6 — REPORT:
  Generate cq8-eval-report.md
```

---

## CQ9: Dasatinib Drug Safety

**Gold Standard Path**: `Drug(Dasatinib)` → `Targets(ABL1, DDR2, hERG)` → safety profile comparison with `Drug(Imatinib)`

### Prompt

```
Execute CQ9 evaluation: "What are the off-target risks of Dasatinib, specifically cardiotoxicity from hERG (KCNH2) and DDR2 activity?"

PHASE 1 — LOAD:
cq_get(cq_id="cq9")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve Dasatinib
  chembl_search_compounds(query="dasatinib", slim=True)
  → expect CHEMBL:1421
  cq_record_step(cq_id="cq9", step_id="entity_dasatinib", ...)

Step 2: Resolve Imatinib
  chembl_search_compounds(query="imatinib", slim=True)
  → expect CHEMBL:941
  cq_record_step(cq_id="cq9", step_id="entity_imatinib", ...)

Step 3: Resolve KCNH2 (hERG)
  hgnc_search_genes(query="KCNH2", slim=True)
  → expect HGNC:6251
  cq_record_step(cq_id="cq9", step_id="entity_kcnh2", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: Dasatinib mechanisms (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL1421&format=json"
  → expect ABL1, PDGFR, KIT targets
  cq_record_step(cq_id="cq9", step_id="edge_dasatinib_mechanisms", ...)

Edge 2: Dasatinib activity vs DDR2 (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/activity?molecule_chembl_id=CHEMBL1421&target_chembl_id=CHEMBL5122&standard_type=IC50&limit=10&format=json"
  → DDR2 binding affinities (off-target risk for pleural effusion)
  cq_record_step(cq_id="cq9", step_id="edge_dasatinib_ddr2", ...)

Edge 3: Dasatinib activity vs hERG (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/activity?molecule_chembl_id=CHEMBL1421&target_chembl_id=CHEMBL240&standard_type=IC50&limit=10&format=json"
  → hERG IC50 (cardiotoxicity risk if < 10μM)
  cq_record_step(cq_id="cq9", step_id="edge_dasatinib_herg", ...)

Edge 4: Imatinib comparison (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL941&format=json"
  → cleaner target profile
  cq_record_step(cq_id="cq9", step_id="edge_imatinib_comparison", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq9")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ9: Dasatinib off-target safety profile",
    episode_body=<JSON>, source="json", group_id="cq9-dasatinib-safety")

PHASE 6 — REPORT:
  Generate cq9-eval-report.md
```

---

## CQ10: Huntington's Novel Targets

**Gold Standard Path**: `Gene(HTT)` → `Disease(HD)` → `Targets(VMAT2 covered)` → gap analysis → `Target(SLC2A3 novel)`

### Prompt

```
Execute CQ10 evaluation: "What novel therapeutic targets exist for Huntington's Disease that are not covered by current Phase 3 interventions?"

PHASE 1 — LOAD:
cq_get(cq_id="cq10")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve HTT
  hgnc_search_genes(query="HTT", slim=True)
  → expect HGNC:4851
  cq_record_step(cq_id="cq10", step_id="entity_htt", ...)

Step 2: Resolve VMAT2/SLC18A2
  hgnc_search_genes(query="SLC18A2", slim=True)
  → confirm current target (covered by tetrabenazine)
  cq_record_step(cq_id="cq10", step_id="entity_vmat2", ...)

Step 3: Resolve Tetrabenazine
  chembl_search_compounds(query="tetrabenazine", slim=True)
  → expect CHEMBL:117785
  cq_record_step(cq_id="cq10", step_id="entity_tetrabenazine", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: HD clinical trial landscape (Tier 1)
  clinicaltrials_search_trials(query="Huntington disease", phase="PHASE3", slim=True, page_size=50)
  → catalog all Phase 3 interventions and their targets
  cq_record_step(cq_id="cq10", step_id="edge_hd_trials", ...)

Edge 2: Tetrabenazine mechanism (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL117785&format=json"
  → confirm VMAT2 inhibitor
  cq_record_step(cq_id="cq10", step_id="edge_tetrabenazine_mechanism", ...)

Edge 3: HTT disease associations — ranked targets (Tier 1 — Fuzzy-to-Fact)
  opentargets_search_targets(query="HTT", slim=True)
  → confirm Ensembl ID ENSG00000197386
  opentargets_get_associations(target_id="ENSG00000197386")
  → ranked targets for Huntington's
  cq_record_step(cq_id="cq10", step_id="edge_htt_associations", ...)

Edge 4: Gap analysis
  Compare Open Targets ranked targets vs Phase 3 trial targets
  → identify targets with high association scores but no Phase 3 coverage
  → expect SLC2A3/GLUT3 (ENSG00000059804) among novel opportunities
  cq_record_step(cq_id="cq10", step_id="edge_gap_analysis", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq10")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ10: Huntington's novel therapeutic targets",
    episode_body=<JSON>, source="json", group_id="cq10-huntingtons-novel-targets")

PHASE 6 — REPORT:
  Generate cq10-eval-report.md
```

---

## CQ11: p53-MDM2-Nutlin Pathway Validation

**Gold Standard Path**: `Gene(TP53)` ↔ `Gene(MDM2)` [interaction score ~0.999] → `Drug(Nutlin-3)` [MDM2 inhibitor]

### Prompt

```
Execute CQ11 evaluation: "How do we build and validate a knowledge graph for the p53-MDM2-Nutlin therapeutic axis?"

PHASE 1 — LOAD:
cq_get(cq_id="cq11")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve TP53
  hgnc_search_genes(query="TP53", slim=True)
  → expect HGNC:11998
  cq_record_step(cq_id="cq11", step_id="entity_tp53", ...)

Step 2: Resolve MDM2
  hgnc_search_genes(query="MDM2", slim=True)
  → expect HGNC:6973
  cq_record_step(cq_id="cq11", step_id="entity_mdm2", ...)

Step 3: Resolve Nutlin-3
  chembl_search_compounds(query="Nutlin-3", slim=True)
  → expect CHEMBL:191334
  cq_record_step(cq_id="cq11", step_id="entity_nutlin3", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: TP53-MDM2 interaction (Tier 1)
  string_search_proteins(query="TP53", species=9606)
  string_get_interactions(string_id=<result>, required_score=900, limit=10)
  → expect MDM2 among top interactors with score ~0.999
  cq_record_step(cq_id="cq11", step_id="edge_tp53_mdm2", ...)

Edge 2: BioGRID physical evidence (Tier 1)
  biogrid_search_genes(query="TP53")
  biogrid_get_interactions(gene_symbol="TP53", slim=True, max_results=50)
  → count MDM2-specific physical interactions
  cq_record_step(cq_id="cq11", step_id="edge_tp53_mdm2_biogrid", ...)

Edge 3: Nutlin-3 mechanism (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL191334&format=json"
  → expect MDM2 INHIBITOR
  cq_record_step(cq_id="cq11", step_id="edge_nutlin_mechanism", ...)

Edge 4: Network visualization
  string_get_network_image_url(identifiers="TP53\nMDM2", network_flavor="confidence")

PHASE 4 — SCORE:
  cq_score(cq_id="cq11")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ11: p53-MDM2-Nutlin axis",
    episode_body=<JSON>, source="json", group_id="cq11-p53-mdm2-nutlin")

PHASE 6 — REPORT:
  Generate cq11-eval-report.md
```

---

## CQ12: Health Emergencies 2026

**Gold Standard**: Parallel trial landscape search across major disease areas with count totals

### Prompt

```
Execute CQ12 evaluation: "What are the key health emergencies or emerging health priorities that multiple clinical trials are targeting right now?"

PHASE 1 — LOAD:
cq_get(cq_id="cq12")

PHASE 2 — ENTITY RESOLUTION (via trial counts):

Run parallel ClinicalTrials.gov searches:

Step 1: Cancer trials
  search_trials(condition="cancer", status=["RECRUITING"], count_total=true, page_size=5)
  → expect 18,000+ recruiting trials
  cq_record_step(cq_id="cq12", step_id="entity_cancer_trials", status="pass",
    expected_curie="18000+", actual_curie="<count>",
    tool_used="c-trials search_trials", tier="tier1")

Step 2: Diabetes trials
  search_trials(condition="diabetes", status=["RECRUITING"], count_total=true, page_size=5)
  → expect 1,900+ trials
  cq_record_step(cq_id="cq12", step_id="entity_diabetes_trials", ...)

Step 3: Alzheimer's trials
  search_trials(condition="Alzheimer", status=["RECRUITING"], count_total=true, page_size=5)
  → expect 500+ trials
  cq_record_step(cq_id="cq12", step_id="entity_alzheimer_trials", ...)

Step 4: Long COVID trials
  search_trials(condition="long COVID", status=["RECRUITING"], count_total=true, page_size=5)
  → expect 100+ trials
  cq_record_step(cq_id="cq12", step_id="entity_long_covid_trials", ...)

Step 5: CAR-T trials
  search_trials(intervention="CAR-T", status=["RECRUITING"], count_total=true, page_size=5)
  → expect 800+ trials
  cq_record_step(cq_id="cq12", step_id="entity_cart_trials", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: Innovation discovery — GLP-1 trials
  search_trials(intervention="GLP-1", status=["RECRUITING"], count_total=true, page_size=5)
  cq_record_step(cq_id="cq12", step_id="edge_glp1_innovation", ...)

Edge 2: Immunotherapy landscape
  search_trials(intervention="immunotherapy", status=["RECRUITING"], count_total=true, page_size=5)
  cq_record_step(cq_id="cq12", step_id="edge_immunotherapy", ...)

Edge 3: AI in clinical trials
  search_trials(intervention="artificial intelligence", status=["RECRUITING"], count_total=true, page_size=5)
  cq_record_step(cq_id="cq12", step_id="edge_ai_trials", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq12")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ12: Health emergencies 2026 landscape",
    episode_body=<JSON of counts and patterns>, source="json",
    group_id="cq12-health-emergencies-2026")

PHASE 6 — REPORT:
  Generate cq12-eval-report.md with trial count table and trend analysis.
```

---

## CQ13: High-Commercialization Trials

**Gold Standard**: Top Phase 3 trials ranked by commercialization potential with drug mechanisms

### Prompt

```
Execute CQ13 evaluation: "Which clinical trials have the highest potential for commercialization or are attracting the most investment interest?"

PHASE 1 — LOAD:
cq_get(cq_id="cq13")

PHASE 2 — ENTITY RESOLUTION:

Step 1: Discover Phase 3 recruiting trials
  search_trials(phase=["PHASE3"], status=["RECRUITING"], page_size=20)
  → identify high-profile sponsors (Eli Lilly, Gilead, etc.)
  cq_record_step(cq_id="cq13", step_id="entity_phase3_trials", ...)

Step 2: Resolve Retatrutide (Eli Lilly obesity drug)
  chembl_search_compounds(query="retatrutide", slim=True)
  cq_record_step(cq_id="cq13", step_id="entity_retatrutide", ...)

Step 3: Resolve Sacituzumab Govitecan
  chembl_search_compounds(query="sacituzumab govitecan", slim=True)
  cq_record_step(cq_id="cq13", step_id="entity_sacituzumab", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: Drug mechanisms (Tier 2 curl)
  For each identified drug:
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=<ID>&format=json"
  cq_record_step(cq_id="cq13", step_id="edge_drug_mechanisms", ...)

Edge 2: Target disease associations (Tier 1 — Fuzzy-to-Fact)
  opentargets_search_targets(query="<target_gene_symbol>", slim=True)
  → resolve to Ensembl ID
  opentargets_get_associations(target_id=<target_ensembl_id>)
  → validate drug target–disease link
  cq_record_step(cq_id="cq13", step_id="edge_target_validation", ...)

Edge 3: Sponsor pipeline depth (Tier 1)
  search_by_sponsor(sponsor_name="Eli Lilly", phase=["PHASE3"], status=["RECRUITING"], count_total=true)
  search_by_sponsor(sponsor_name="Gilead", phase=["PHASE3"], status=["RECRUITING"], count_total=true)
  cq_record_step(cq_id="cq13", step_id="edge_sponsor_pipeline", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq13")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ13: High-commercialization Phase 3 trials",
    episode_body=<JSON>, source="json", group_id="cq13-high-commercialization-trials")

PHASE 6 — REPORT:
  Generate cq13-eval-report.md with ranked candidate table.
```

---

## CQ14: Feng et al. Synthetic Lethality Validation

**Gold Standard Path**: `Gene(TP53)` --[SL]--> `Gene(TYMS)` --[target_of]--> `Drug(Pemetrexed)` --[in_trial]--> `Trial(NCT04695925)`

### Prompt

```
Execute CQ14 evaluation: "How can we validate synthetic lethal gene pairs from Feng et al. (2022) and identify druggable opportunities for TP53-mutant cancers?"

PHASE 1 — LOAD:
cq_get(cq_id="cq14")

PHASE 2 — ENTITY RESOLUTION (Tier 1):

Step 1: Resolve TP53
  hgnc_search_genes(query="TP53", slim=True)
  → expect HGNC:11998
  cq_record_step(cq_id="cq14", step_id="entity_tp53", ...)

Step 2: Resolve TYMS
  hgnc_search_genes(query="TYMS", slim=True)
  → expect HGNC:12441
  cq_record_step(cq_id="cq14", step_id="entity_tyms", ...)

Step 3: Resolve 5-fluorouracil
  chembl_search_compounds(query="fluorouracil", slim=True)
  → expect CHEMBL:185
  cq_record_step(cq_id="cq14", step_id="entity_5fu", ...)

Step 4: Resolve Pemetrexed
  chembl_search_compounds(query="pemetrexed", slim=True)
  → expect CHEMBL:225072
  cq_record_step(cq_id="cq14", step_id="entity_pemetrexed", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: BioGRID ORCS CRISPR screens (Tier 2 curl)
  curl -s "https://orcsws.thebiogrid.org/gene/7298"
  → expect 1,446+ screens confirming TYMS essentiality
  cq_record_step(cq_id="cq14", step_id="edge_biogrid_orcs", status="pass|fail",
    expected_curie="1446+ screens", actual_curie="<result>",
    tool_used="curl biogrid_orcs", tier="tier2",
    notes="TYMS essentiality across CRISPR screens")

Edge 2: Drug mechanisms (Tier 2 curl)
  curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism?molecule_chembl_id=CHEMBL225072&format=json"
  → expect TYMS INHIBITOR
  cq_record_step(cq_id="cq14", step_id="edge_pemetrexed_mechanism", ...)

Edge 3: Clinical trials for TP53+Pemetrexed (Tier 1)
  clinicaltrials_search_trials(query="TP53 pemetrexed", slim=True)
  → expect NCT:04695925 or similar
  cq_record_step(cq_id="cq14", step_id="edge_tp53_pemetrexed_trial", ...)

PARALLEL VALIDATION (Synapse):
  search_synapse(query_term="TP53 synthetic lethality CRISPR", entity_type="file")
  → cross-validate with DepMap/Synapse datasets

PHASE 4 — SCORE:
  cq_score(cq_id="cq14")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ14: TP53/TYMS synthetic lethality validation",
    episode_body=<JSON>, source="json", group_id="cq14-feng-synthetic-lethality")

PHASE 6 — REPORT:
  Generate cq14-eval-report.md

NOTE: Dataset references for validation:
  - dwb2023/sl_gene_pairs (209 SL pairs) on HuggingFace
  - dwb2023/pmc_35559673_table_s6_sl_gene_detail (81 genes) on HuggingFace
```

---

## CQ15: CAR-T Regulatory Landscape

**Gold Standard**: Phase 3 CAR-T trials ranked by regulatory velocity with FDA/EMA milestone analysis

### Prompt

```
Execute CQ15 evaluation: "Which CAR-T cell trials are currently navigating FDA or EMA milestones most rapidly?"

PHASE 1 — LOAD:
cq_get(cq_id="cq15")

PHASE 2 — ENTITY RESOLUTION:

Step 1: Discover CAR-T Phase 3 trials
  search_trials(intervention="CAR-T cell therapy", phase=["PHASE3"],
    status=["RECRUITING", "ACTIVE_NOT_RECRUITING"], page_size=30)
  → expect 27+ Phase 3 trials
  cq_record_step(cq_id="cq15", step_id="entity_cart_phase3", ...)

Step 2: Discover CAR-T Phase 2 trials
  search_trials(intervention="CAR-T cell therapy", phase=["PHASE2"],
    status=["RECRUITING"], page_size=50, count_total=true)
  → expect 297+ Phase 2 trials
  cq_record_step(cq_id="cq15", step_id="entity_cart_phase2", ...)

PHASE 3 — EDGE DISCOVERY:

Edge 1: Protocol analysis for top Phase 3 trials (Tier 1)
  For top 5 Phase 3 trials:
    get_trial_details(nct_id=<trial_id>)
    → extract sponsor, timeline, primary endpoints, FDA designations
  cq_record_step(cq_id="cq15", step_id="edge_protocol_analysis", ...)

Edge 2: Drug mechanisms for identified CAR-T products (Tier 1 + Tier 2)
  chembl_search_compounds(query="<CAR-T product name>")
  curl ChEMBL /mechanism for any ChEMBL-registered products
  cq_record_step(cq_id="cq15", step_id="edge_cart_mechanisms", ...)

Edge 3: Regulatory signal extraction
  From trial details: identify breakthrough therapy designations,
  PRIME pathway, accelerated approval signals
  cq_record_step(cq_id="cq15", step_id="edge_regulatory_signals", ...)

Edge 4: Sponsor landscape
  search_by_sponsor(sponsor_name="Novartis", condition="lymphoma", phase=["PHASE3"])
  search_by_sponsor(sponsor_name="Gilead", condition="lymphoma", phase=["PHASE3"])
  cq_record_step(cq_id="cq15", step_id="edge_sponsor_landscape", ...)

PHASE 4 — SCORE:
  cq_score(cq_id="cq15")

PHASE 5 — PERSIST:
  graphiti-docker add_memory(name="CQ15: CAR-T regulatory landscape",
    episode_body=<JSON>, source="json", group_id="cq15-car-t-regulatory")

PHASE 6 — REPORT:
  Generate cq15-eval-report.md with velocity ranking table.
```

---

## Batch Execution Script

To run all 15 CQs sequentially and generate a comparative report:

```
STEP 1: Import catalog (one-time setup)
  cq_import_from_markdown(markdown_path="competency-questions-catalog.md")

STEP 2: Execute each CQ (use prompts above)
  For cq_id in [cq1, cq2, ..., cq15]:
    Execute the 6-phase prompt for that CQ

STEP 3: Retrieve all results
  cq_results()
  → returns all scored CQs with timestamps

STEP 4: Compare over time
  cq_compare(cq_ids=["cq1","cq2",...,"cq15"])
  → score trends across runs

STEP 5: Aggregate report
  Generate cq-batch-eval-report.md with:
    - Summary table (cq_id, overall_score, entity_score, edge_score, path_complete)
    - Category analysis (mechanistic, network, clinical, regulatory)
    - Tool coverage matrix (which tools used per CQ)
    - Tier distribution (% tier1 vs tier2 steps)
    - Recommendations for gap closure
```

---

## Tool Reference

| Tool | MCP Server | Tier | Used By CQs |
|------|-----------|------|-------------|
| `chembl_search_compounds` | Life Sciences Gateway | tier1 | cq1,2,4,7,8,9,11,13,14,15 |
| `chembl_get_compound` | Life Sciences Gateway | tier1 | cq1,2 |
| `hgnc_search_genes` | Life Sciences Gateway | tier1 | cq1-11,14 |
| `hgnc_get_gene` | Life Sciences Gateway | tier1 | cq1,2 |
| `string_search_proteins` | Life Sciences Gateway | tier1 | cq3,5,6,8,11 |
| `string_get_interactions` | Life Sciences Gateway | tier1 | cq3,5,6,8,11 |
| `string_get_network_image_url` | Life Sciences Gateway | tier1 | cq5,6,11 |
| `biogrid_search_genes` | Life Sciences Gateway | tier1 | cq6,11 |
| `biogrid_get_interactions` | Life Sciences Gateway | tier1 | cq6,11 |
| `wikipathways_search_pathways` | Life Sciences Gateway | tier1 | cq2,3,5,7 |
| `wikipathways_get_pathways_for_gene` | Life Sciences Gateway | tier1 | cq2,7 |
| `wikipathways_get_pathway_components` | Life Sciences Gateway | tier1 | cq2,7 |
| `uniprot_search_proteins` | Life Sciences Gateway | tier1 | cq8 |
| `uniprot_get_protein` | Life Sciences Gateway | tier1 | cq8 |
| `opentargets_search_targets` | Life Sciences Gateway | tier1 | cq1,3,5,7,10,13 |
| `opentargets_get_associations` | Life Sciences Gateway | tier1 | cq1,3,5,7,10,13 |
| `ot search_entities` | Open Targets Platform | tier1 | cq1,3,7 |
| `clinicaltrials_search_trials` | Life Sciences Gateway | tier1 | cq4,8,10,14 |
| `clinicaltrials_get_trial` | Life Sciences Gateway | tier1 | cq15 |
| `search_trials` | ClinicalTrials.gov MCP | tier1 | cq12,13,15 |
| `get_trial_details` | ClinicalTrials.gov MCP | tier1 | cq15 |
| `search_by_sponsor` | ClinicalTrials.gov MCP | tier1 | cq13,15 |
| `curl chembl/mechanism` | ChEMBL REST API | tier2 | cq1,4,8,9,10,11,13,14,15 |
| `curl chembl/activity` | ChEMBL REST API | tier2 | cq4,9 |
| `curl biogrid_orcs` | BioGRID ORCS API | tier2 | cq14 |
| `search_synapse` | Synapse | complementary | cq8,14 |
| `cq_record_step` | cq-eval MCP | scoring | all |
| `cq_score` | cq-eval MCP | scoring | all |
| `graphiti-docker add_memory` | Graphiti | tier3 | all |

# Competency Questions Catalog

**Purpose**: Research questions for building knowledge graphs using the `lifesciences-graph-builder` skill.

**Target**: Use `graphiti-docker` for development/testing.

---

## Quick Reference

| cq# | Category | Question Summary | group_id | Source |
|-----|----------|------------------|----------|--------|
| cq1 | FOP Mechanism | Palovarotene mechanism for FOP | `cq1-fop-mechanism` | DrugMechDB |
| cq2 | FOP Repurposing | BMP pathway drug repurposing | `cq2-fop-repurposing` | DrugMechDB |
| cq3 | AD Gene Networks | Alzheimer's gene-protein interactions | `cq3-alzheimers-gene-network` | DALK (Li et al.) |
| cq4 | AD Therapeutics | Amyloid/Tau targeting drugs | `cq4-alzheimers-therapeutics` | DALK (Li et al.) |
| cq5 | MAPK Regulation | Directed signaling cascades | `cq5-mapk-regulatory-cascade` | STRING 2025 |
| cq6 | TF Networks | BRCA1 regulatory network | `cq6-brca1-regulatory-network` | STRING 2025 |
| cq7 | Multi-Hop Repurposing | NGLY1 federated drug discovery | `cq7-ngly1-drug-repurposing` | BioThings Explorer |
| cq8 | Synthetic Lethality | ARID1A-deficient Ovarian Cancer | `cq8-arid1a-synthetic-lethality` | Original |
| cq9 | Drug Safety | Dasatinib off-target risks | `cq9-dasatinib-safety` | Original |
| cq10 | Orphan Drug | Huntington's novel targets | `cq10-huntingtons-novel-targets` | Original |
| cq11 | Pathway Validation | p53-MDM2-Nutlin axis | `cq11-p53-mdm2-nutlin` | Original |
| cq12 | Health Emergencies | 2026 clinical trial priorities | `cq12-health-emergencies-2026` | Original |
| cq13 | Commercialization | High-investment Phase 3 trials | `cq13-high-commercialization-trials` | Original |
| cq14 | Synthetic Lethality | TP53 SL partners from Feng et al. | `cq14-feng-synthetic-lethality` | Feng et al. 2022 |
| cq15 | CAR-T Regulatory | FDA/EMA milestone velocity | `cq15-car-t-regulatory` | Original |

**Validation Files**: `docs/competency-questions/validiation/2026{month}{day}/cq{N}-*.md`

---

## cq1: FOP Mechanism (DrugMechDB Style)

**Question**: *By what mechanism does Palovarotene treat Fibrodysplasia Ossificans Progressiva (FOP)?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| Palovarotene | CHEMBL:2105648 | RAR-gamma agonist |
| RARG | HGNC:9866 | Retinoic acid receptor gamma |
| ACVR1 | HGNC:171 | BMP receptor (causal gene) |
| FOP | MONDO:0007606 | Target disease |

**Gold Standard Path**:
`Drug(Palovarotene)` --[agonist]--> `Protein(RARG)` --[regulates]--> `Protein(ACVR1)` --[causes]--> `Disease(FOP)`

**Structured Definition (BioLink)**:
```json
{
  "question": "What is the mechanism of Palovarotene for FOP?",
  "indication": {
    "drug": "CHEMBL:2105648",
    "disease": "MONDO:0007606",
    "name": "Fibrodysplasia Ossificans Progressiva"
  },
  "graph": {
    "nodes": [
      {"id": "CHEMBL:2105648", "name": "Palovarotene", "type": "biolink:SmallMolecule"},
      {"id": "HGNC:9866", "name": "RARG", "type": "biolink:Gene"},
      {"id": "HGNC:171", "name": "ACVR1", "type": "biolink:Gene"},
      {"id": "MONDO:0007606", "name": "FOP", "type": "biolink:Disease"}
    ],
    "edges": [
      {"source": "CHEMBL:2105648", "target": "HGNC:9866", "type": "biolink:agonist_of"},
      {"source": "HGNC:9866", "target": "HGNC:171", "type": "biolink:regulates"},
      {"source": "HGNC:171", "target": "MONDO:0007606", "type": "biolink:gene_associated_with_condition"}
    ]
  }
}
```

**Workflow**:
1. **Anchor**: `chembl_search_compounds("palovarotene")` → CHEMBL:2105648
2. **Enrich**: `chembl_get_compound("CHEMBL:2105648")` → Max Phase 4, indications
3. **Mechanism**: curl ChEMBL /mechanism → RARG agonist
4. **Target Gene**: `hgnc_get_gene("HGNC:171")` → ACVR1 details
5. **Disease Link**: `opentargets_get_associations("ENSG00000115170")` → FOP association
6. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq1-fop-mechanism")`

**Validation**: `docs/competency-validations/cq1-fop-mechanism-validation.md`

**Target group_id**: `cq1-fop-mechanism`

---

## cq2: FOP Drug Repurposing

**Question**: *What other drugs targeting the BMP Signaling Pathway could be repurposed for FOP?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| ACVR1 | HGNC:171 | Causal gene |
| BMP Signaling Pathway | WP:WP2760 | Target pathway |
| LDN-193189 | CHEMBL:405130 | ACVR1/BMPR1A inhibitor |
| Dorsomorphin | CHEMBL:495727 | BMP inhibitor |

**Required Reasoning**:
1. Identify Target: `ACVR1` (Gene)
2. Identify Pathway: `BMP Signaling Pathway` (WikiPathways)
3. Identify Member Genes: `SMAD1`, `SMAD5`, `BMPR1A`
4. Identify Inhibitors: `LDN-193189` (inhibits ACVR1/BMPR1A)

**Workflow**:
1. **Anchor**: `hgnc_get_gene("HGNC:171")` → ACVR1
2. **Pathway Discovery**: `wikipathways_get_pathways_for_gene("ACVR1")` → BMP pathway
3. **Pathway Components**: `wikipathways_get_pathway_components("WP:WP2760")` → Member genes
4. **Drug Search**: `chembl_search_compounds("ACVR1 inhibitor")` → Candidates
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq2-fop-repurposing")`

**Expected Output**:
- **Candidate**: LDN-193189 (CHEMBL:405130)
- **Evidence**: "Inhibits BMP signaling downstream of ACVR1"
- **Safety Check**: Verification via ChEMBL activity data required

**Validation**: `docs/competency-validations/cq2-fop-repurposing-validation.md`

**Target group_id**: `cq2-fop-repurposing`

---

## cq3: Alzheimer's Gene-Protein Networks

**Source**: Li, D., Yang, S., Tan, Z., et al. (2024). *DALK: Dynamic Co-Augmentation of LLMs and KG to answer Alzheimer's Disease Questions with Scientific Literature*. arXiv:2405.04819v1.

**Question**: *What genes and proteins are implicated in Alzheimer's Disease progression, and how do they interact?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| APP | HGNC:620 | Amyloid precursor protein |
| APOE | HGNC:613 | Apolipoprotein E (risk factor) |
| PSEN1 | HGNC:9508 | Presenilin 1 (gamma-secretase) |
| MAPT | HGNC:6893 | Tau protein |
| Alzheimer's Disease | MONDO:0004975 | Target disease |

**Workflow**:
1. **Anchor**: `hgnc_search_genes("APP")` → HGNC:620
2. **Expand**: `string_get_interactions("STRING:9606.ENSP00000284981")` → APP interactors (BACE1, PSEN1)
3. **Disease Links**: `opentargets_get_associations("ENSG00000142192")` → AD association scores
4. **Pathway Context**: `wikipathways_search_pathways("Alzheimer")` → WP:WP2059
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq3-alzheimers-gene-network")`

**Validation**: `docs/competency-validations/cq3-alzheimers-gene-network.md`

**Target group_id**: `cq3-alzheimers-gene-network`

---

## cq4: Alzheimer's Therapeutic Targets

**Question**: *What drugs target amyloid-beta or tau proteins for Alzheimer's Disease treatment?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| BACE1 | HGNC:933 | Beta-secretase 1 |
| MAPT | HGNC:6893 | Tau protein |
| GSK3B | HGNC:4617 | Tau kinase |
| Lecanemab | CHEMBL:4594344 | Anti-amyloid antibody |

**Workflow**:
1. **Anchor Targets**: `hgnc_search_genes("BACE1")` → HGNC:933
2. **Drug Discovery**: `chembl_search_compounds("BACE1 inhibitor")`
3. **Activity Data**: curl ChEMBL /activity → binding affinities
4. **Clinical Trials**: `clinicaltrials_search_trials("Alzheimer BACE", phase="PHASE3")`
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq4-alzheimers-therapeutics")`

**Validation**: `docs/competency-validations/cq4-alzheimers-therapeutics.md`

**Target group_id**: `cq4-alzheimers-therapeutics`

---

## cq5: MAPK Regulatory Cascade

**Source**: Szklarczyk, D., Nastou, K., Koutrouli, M., et al. (2025). *The STRING database in 2025: protein networks with directionality of regulation*. Nucleic Acids Research, gkae1113.

**Question**: *In the MAPK signaling cascade, which proteins regulate downstream targets and with what direction (activation vs inhibition)?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| RAF1 | STRING:9606.ENSP00000251849 | MAPKKK |
| MAP2K1 | STRING:9606.ENSP00000302486 | MEK1 |
| MAPK1 | STRING:9606.ENSP00000215832 | ERK2 |

**Workflow**:
1. **Anchor**: `string_search_proteins("RAF1")` → STRING:9606.ENSP00000251849
2. **Directed Edges**: `string_get_interactions(required_score=700)` → Regulatory type
3. **Pathway Mapping**: `wikipathways_search_pathways("MAPK signaling")` → WP:WP382
4. **Disease Context**: `opentargets_get_associations()` → Cancer associations
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq5-mapk-regulatory-cascade")`

**Note**: STRING 12.5 provides `network_type=regulatory` for directed edges with activation/inhibition annotations.

**Validation**: `docs/competency-validations/cq5-mapk-regulatory-cascade.md`

**Target group_id**: `cq5-mapk-regulatory-cascade`

---

## cq6: BRCA1 Regulatory Network

**Question**: *What transcription factors regulate BRCA1 expression, and what genes does BRCA1 regulate?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| BRCA1 | HGNC:1100 | Tumor suppressor |
| E2F1 | HGNC:3113 | Upstream TF |
| SP1 | HGNC:11205 | Upstream TF |
| RAD51 | HGNC:9817 | Downstream target |

**Workflow**:
1. **Anchor**: `hgnc_search_genes("BRCA1")` → HGNC:1100
2. **Regulatory Network**: `string_get_interactions()` → Filter for regulatory edges
3. **Upstream TFs**: Parse STRING regulatory evidence for edges pointing TO BRCA1
4. **Downstream Targets**: Parse STRING for edges pointing FROM BRCA1
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq6-brca1-regulatory-network")`

**Validation**: `docs/competency-validations/cq6-brca1-regulatory-network.md`

**Target group_id**: `cq6-brca1-regulatory-network`

---

## cq7: NGLY1 Multi-Hop Drug Repurposing

**Source**: Callaghan, J., Xu, C.H., Xin, J., et al. (2023). *BioThings Explorer: a query engine for a federated knowledge graph of biomedical APIs*. Bioinformatics, btad570.

**Question**: *For NGLY1 deficiency, what are the associated genes, and what existing drugs target proteins in those pathways?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| NGLY1 | HGNC:17646 | Causal gene |
| NGLY1 deficiency | MONDO:0014109 | Target disease |
| N-glycanase pathway | WP:WP5078 | Member pathway |

**Workflow**:
1. **Disease Anchor**: Search for NGLY1 deficiency (MONDO:0014109)
2. **Gene Discovery**: `hgnc_search_genes("NGLY1")` → HGNC:17646
3. **Pathway Context**: `wikipathways_get_pathways_for_gene("NGLY1")` → Member pathways
4. **Pathway Expansion**: `wikipathways_get_pathway_components()` → All pathway members
5. **Drug Search**: For each pathway protein → `chembl_search_compounds()` with target filter
6. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq7-ngly1-drug-repurposing")`

**Validation**: `docs/competency-validations/cq7-ngly1-drug-repurposing.md`

**Target group_id**: `cq7-ngly1-drug-repurposing`

---

## cq8: ARID1A Synthetic Lethality

**Question**: *How can we identify therapeutic strategies for ARID1A-deficient Ovarian Cancer using synthetic lethality?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| ARID1A | HGNC:11110 | Tumor suppressor (SWI/SNF) |
| EZH2 | HGNC:3527 | Synthetic lethal partner (PRC2) |
| ATR | HGNC:882 | Synthetic lethal partner |
| Tazemetostat | CHEMBL:3414621 | EZH2 inhibitor (FDA approved) |
| NCT03348631 | NCT:03348631 | Phase 2 trial |

**Workflow**:
1. **Anchor**: `hgnc_search_genes("ARID1A")` → HGNC:11110
2. **Enrich**: `uniprot_get_protein("UniProtKB:O14497")` → SWI/SNF function
3. **Expand**: `string_get_interactions()` → SWI/SNF complex members
4. **Traverse**: `chembl_search_compounds("tazemetostat")` → CHEMBL:3414621
5. **Validate**: curl ChEMBL /mechanism → EZH2 inhibitor
6. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq8-arid1a-synthetic-lethality")`

**Source Documentation**: `docs/scenarios/scenario1-walkthrough.md`

**Validation**: `docs/competency-validations/cq8-arid1a-synthetic-lethality.md`

**Target group_id**: `cq8-arid1a-synthetic-lethality`

---

## cq9: Dasatinib Drug Safety

**Question**: *What are the off-target risks of Dasatinib, specifically cardiotoxicity from hERG (KCNH2) and DDR2 activity?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| Dasatinib | CHEMBL:1421 | Index compound |
| Imatinib | CHEMBL:941 | Cleaner alternative |
| ABL1 | CHEMBL:1862 | Primary target |
| DDR2 | CHEMBL:5122 | Off-target (pleural effusion) |
| hERG/KCNH2 | HGNC:6251 | Safety target (cardiotoxicity) |

**Workflow**:
1. **Anchor**: `chembl_search_compounds("dasatinib")` → CHEMBL:1421
2. **Mechanisms**: curl ChEMBL /mechanism → ABL1, PDGFR, KIT targets
3. **Activity**: curl ChEMBL /activity → IC50 values vs DDR2
4. **Compare**: `chembl_search_compounds("imatinib")` → cleaner profile
5. **Safety Genes**: `hgnc_search_genes("KCNH2")` → HGNC:6251
6. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq9-dasatinib-safety")`

**Source Documentation**: `docs/scenarios/scenario2-walkthrough.md`

**Validation**: `docs/competency-validations/cq9-dasatinib-safety.md`

**Target group_id**: `cq9-dasatinib-safety`

---

## cq10: Huntington's Novel Targets

**Question**: *What novel therapeutic targets exist for Huntington's Disease that are not covered by current Phase 3 interventions?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| HTT | HGNC:4851 | Causal gene |
| SLC18A2/VMAT2 | CHEMBL:1893 | Current target (covered) |
| Tetrabenazine | CHEMBL:117785 | Approved drug |
| SLC2A3/GLUT3 | ENSG00000059804 | Novel target opportunity |

**Workflow**:
1. **Anchor**: `hgnc_search_genes("HTT")` → HGNC:4851
2. **Trial Landscape**: curl ClinicalTrials.gov → Phase 3 trials
3. **Drug Mechanisms**: curl ChEMBL /mechanism → VMAT2 inhibitors
4. **Gap Analysis**: `opentargets_get_associations()` → ranked targets
5. **Find Novel**: Filter for targets with no drug coverage
6. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq10-huntingtons-novel-targets")`

**Source Documentation**: `docs/scenarios/scenario3-huntington-orphan-drug.md`

**Validation**: `docs/competency-validations/cq10-huntingtons-novel-targets.md`

**Target group_id**: `cq10-huntingtons-novel-targets`

---

## cq11: p53-MDM2-Nutlin Pathway Validation

**Question**: *How do we build and validate a knowledge graph for the p53-MDM2-Nutlin therapeutic axis?*

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| TP53 | HGNC:11998 | Tumor suppressor |
| MDM2 | HGNC:6973 | Oncogene (E3 ligase) |
| Nutlin-3 | CHEMBL:191334 | MDM2 inhibitor |

**Workflow**:
1. **Anchor**: `hgnc_search_genes("TP53")` → HGNC:11998
2. **Partner**: `hgnc_search_genes("MDM2")` → HGNC:6973
3. **Interactions**: `string_get_interactions()` → TP53-MDM2 (score 0.999)
4. **Drug**: `chembl_search_compounds("Nutlin-3")` → CHEMBL:191334
5. **Mechanism**: curl ChEMBL /mechanism → MDM2 inhibitor
6. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq11-p53-mdm2-nutlin")`

**Source Documentation**: `docs/scenarios/scenario4-p53-mdm2-nutlin.md`

**Validation**: `docs/competency-validations/cq11-p53-mdm2-nutlin.md`

**Target group_id**: `cq11-p53-mdm2-nutlin`

---

## cq12: Health Emergencies 2026

**Question**: *What are the key health emergencies or emerging health priorities that multiple clinical trials are targeting right now?*

**Key Findings**:
- Cancer: 18,636+ recruiting trials (immunotherapy revolution)
- Diabetes: 1,999+ trials (GLP-1 transformation)
- Alzheimer's: 579+ trials (neuromodulation renaissance)
- Long COVID: 130+ trials (emerging chronic disease)
- CAR-T: 877+ trials (cell therapy maturation)

**Workflow**:
1. **Disease Discovery**: `clinicaltrials_search_trials()` → parallel searches by disease
2. **Innovation Discovery**: Search CAR-T, GLP-1, immunotherapy, AI trials
3. **Pattern Analysis**: Identify therapeutic convergence across diseases
4. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq12-health-emergencies-2026")`

**Source Documentation**: `docs/research-reports/health-emergencies-2026-analysis.md`

**Validation**: `docs/competency-validations/cq12-health-emergencies-2026.md`

**Target group_id**: `cq12-health-emergencies-2026`

---

## cq13: High-Commercialization Trials

**Question**: *Which clinical trials have the highest potential for commercialization or are attracting the most investment interest?*

**Key Findings**:
1. **Retatrutide** (NCT:07232719) - Eli Lilly - Obesity - VERY HIGH potential
2. **Sacituzumab Govitecan** (NCT:06486441) - Gilead - Endometrial Cancer - HIGH potential
3. **Ficerafusp Alfa** (NCT:06788990) - Bicara - Head & Neck Cancer - MODERATE-HIGH (acquisition target)

**Workflow**:
1. **Trial Discovery**: `clinicaltrials_search_trials(phase="PHASE3", status="RECRUITING")`
2. **Drug Identification**: `chembl_search_compounds()` → CURIEs
3. **Mechanism Extraction**: curl ChEMBL /mechanism → Drug→Target edges
4. **Target Validation**: `opentargets_get_associations()` → disease associations
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq13-high-commercialization-trials")`

**Source Documentation**: `docs/research-reports/high-commercialization-trials-research.md`

**Validation**: `docs/competency-validations/cq13-high-commercialization-trials.md`

**Target group_id**: `cq13-high-commercialization-trials`

---

## cq14: Feng et al. Synthetic Lethality Validation

**Question**: *How can we validate synthetic lethal gene pairs from Feng et al. (2022) and identify druggable opportunities for TP53-mutant cancers?*

**Source Paper**: Feng et al., *Sci. Adv.* 8, eabm6638 (2022) - [PMC35559673](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9098673/)

**Datasets**:
- [dwb2023/sl_gene_pairs](https://huggingface.co/datasets/dwb2023/sl_gene_pairs) - 209 SL pairs
- [dwb2023/pmc_35559673_table_s6_sl_gene_detail](https://huggingface.co/datasets/dwb2023/pmc_35559673_table_s6_sl_gene_detail) - 81 genes

**Key Entities**:
| Entity | CURIE | Role |
|--------|-------|------|
| TP53 | HGNC:11998 | Tumor suppressor (50% of cancers) |
| TYMS | HGNC:12441 | Synthetic lethal partner |
| 5-fluorouracil | CHEMBL:185 | TYMS inhibitor (approved) |
| Pemetrexed | CHEMBL:225072 | TYMS inhibitor (approved) |

**Gold Standard Path**:
`Gene(TP53)` --[synthetic_lethal_with]--> `Gene(TYMS)` --[target_of]--> `Drug(Pemetrexed)` --[in_trial]--> `Trial(NCT04695925)`

**Workflow**:
1. **Anchor**: `hgnc_search_genes("TP53")` → HGNC:11998, `hgnc_search_genes("TYMS")` → HGNC:12441
2. **Validate**: BioGRID ORCS: `curl "https://orcsws.thebiogrid.org/gene/7298"` → 1,446 screens
3. **Druggability**: `chembl_search_compounds("fluorouracil")` → CHEMBL:185
4. **Clinical**: `clinicaltrials_search_trials("TP53 pemetrexed")` → NCT:04695925
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq14-feng-synthetic-lethality")`

**Validation Results**:
- 1,446 BioGRID ORCS screens confirm TYMS essentiality
- Approved drugs exist (5-FU, pemetrexed, raltitrexed)
- Active clinical trials exploring TP53/TYMS combinations

**Source Documentation**: `docs/scenarios/scenario5-synthetic-lethality-feng-walkthrough.md`

**Target group_id**: `cq14-feng-synthetic-lethality`

---

## cq15: CAR-T Regulatory Landscape

**Question**: *Which CAR-T cell trials are currently navigating FDA or EMA milestones most rapidly? What regulatory hurdles are emerging in personalized medicine?*

**Key Findings**:
- 324+ trials analyzed (27 Phase 3, 297 Phase 2)
- Top velocity trials: ENACT-2, ABALL2, HebeCART, CALM, NXC-201
- Regulatory patterns: FDA breakthrough designation, EMA PRIME pathway

**Workflow**:
1. **Trial Search**: `clinicaltrials_search_trials("CAR-T cell therapy", phase="PHASE3")`
2. **Protocol Analysis**: `clinicaltrials_get_trial()` → sponsor, timeline, endpoints
3. **Drug Mechanisms**: `chembl_search_compounds()` + curl /mechanism
4. **Regulatory Signals**: Extract FDA/EMA designations from trial data
5. **Persist**: `mcp__graphiti-docker__add_memory(group_id="cq15-car-t-regulatory")`

**Source Documentation**: `docs/research-reports/car-t-regulatory-landscape.md`

**Validation**: `docs/competency-validations/cq15-car-t-regulatory.md`

**Target group_id**: `cq15-car-t-regulatory`

---

## Re-run Instructions

### Using the lifesciences-graph-builder Skill

To re-run any competency question:

1. **Invoke the skill**:
   ```
   "Build a knowledge graph for cq{N}: [Question]"
   ```

2. **Follow the 5-phase Fuzzy-to-Fact protocol**:
   - Phase 1: Anchor Node (naming)
   - Phase 2: Enrich Node (functional)
   - Phase 3: Expand Edges (interactions)
   - Phase 4: Target Traversal (pharma)
   - Phase 5: Persist Graph

3. **Target graphiti-docker**:
   ```python
   mcp__graphiti-docker__add_memory(
       name="[Episode Name]",
       episode_body=json.dumps({"nodes": [...], "edges": [...]}),
       source="json",
       group_id="cq{N}-[descriptor]"
   )
   ```

### Graphiti Instance Selection

| Context | MCP Tool | group_id Pattern |
|---------|----------|------------------|
| **Development/Testing** | `mcp__graphiti-docker__add_memory()` | `cq*`, `dev-*`, `test-*` |
| **Production** | `mcp__graphiti-aura__add_memory()` | `graphiti_*`, curated namespaces |

**Default**: Use `graphiti-docker` for all competency question work and research exploration.

---

## Prior Art References

| cq# | Source Paper | Key Contribution |
|-----|--------------|------------------|
| cq3-cq4 | Li et al. (2024) DALK | AD-specific KG from 9,764 PubMed papers |
| cq5-cq6 | Szklarczyk et al. (2025) STRING | Regulatory networks with directionality |
| cq7 | Callaghan et al. (2023) BioThings | Federated KG from 34 biomedical APIs |

Full citations in `docs/prior-art-research/markdown/`.

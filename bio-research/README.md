# Bio-Research Plugin

Connect to preclinical research tools and databases to accelerate early-stage life sciences R&D. Use with [Cowork](https://claude.com/product/cowork) or install directly in Claude Code.

This plugin is built on the [Open Biosciences](https://github.com/open-biosciences) platform — a multi-repo system for AI-powered biosciences research. It brings together a **34-tool MCP gateway** spanning 12 life sciences databases, **9 domain skills** implementing the Fuzzy-to-Fact research protocol, **5 analysis skills** for sequencing and lab data, and **10 partner MCP servers** for literature, visualization, and data management.

## What's Included

### Biosciences MCP Gateway (Primary)

The `biosciences-mcp` gateway provides 34 tools across 12 databases for structured entity resolution and knowledge graph construction. This is the plugin's core research engine — all biosciences skills use it as the primary data source.

| Database | LOCATE (search) | RETRIEVE (get by ID) | What It Covers |
|----------|-----------------|---------------------|----------------|
| HGNC | `hgnc_search_genes` | `hgnc_get_gene` | Gene nomenclature, cross-references |
| UniProt | `uniprot_search_proteins` | `uniprot_get_protein` | Protein function, structure, interactions |
| STRING | `string_search_proteins` | `string_get_interactions` | Protein-protein interaction networks |
| BioGRID | `biogrid_search_genes` | `biogrid_get_interactions` | Genetic and physical interactions |
| ChEMBL | `chembl_search_compounds` | `chembl_get_compound` | Bioactive compounds, drug-like molecules |
| Open Targets | `opentargets_search_targets` | `opentargets_get_target` | Drug targets, disease associations |
| PubChem | `pubchem_search_compounds` | `pubchem_get_compound` | Chemical structures, bioassays |
| IUPHAR | `iuphar_search_ligands` | `iuphar_get_ligand` | Pharmacological targets and ligands |
| WikiPathways | `wikipathways_search_pathways` | `wikipathways_get_pathway` | Biological pathway curation |
| ClinicalTrials.gov | `clinicaltrials_search_trials` | `clinicaltrials_get_trial` | Clinical trial registry |
| Ensembl | `ensembl_search_genes` | `ensembl_get_gene` | Genome annotation, variants |
| Entrez | `entrez_search_genes` | `entrez_get_gene` | NCBI gene records, PubMed links |

All tools support a `slim` parameter for token-efficient queries. See [references/token-budgeting.md](references/token-budgeting.md).

### Partner MCP Servers

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

| Provider | What It Does | Category/Placeholder |
|----------|-------------|---------------------|
| U.S. National Library of Medicine | Search biomedical literature and research articles | `~~literature` |
| deepsense.ai | Access preprints from bioRxiv and medRxiv | `~~literature` |
| John Wiley & Sons | Access academic research and publications | `~~journal access` |
| Sage Bionetworks | Collaborative research data management | `~~data repository` |
| deepsense.ai | Bioactive drug-like compound database | `~~chemical database` |
| OpenTargets | Drug target discovery and prioritization | `~~drug targets` |
| deepsense.ai | NIH/NLM clinical trial registry | `~~clinical trials` |
| BioRender | Scientific illustration creation | `~~scientific illustration` |
| Owkin | AI for biology — histopathology and drug discovery | `~~AI research` |
| Benchling\* | Lab data management platform | `~~lab platform` |

### Optional Binary MCP Servers

These require a separate binary download:

- **10X Genomics txg-mcp** (`~~genomics platform`) — Cloud analysis data and workflows ([GitHub](https://github.com/10XGenomics/txg-mcp/releases))
- **ToolUniverse** (`~~tool database`) — AI tools for scientific discovery from Harvard MIMS ([GitHub](https://github.com/mims-harvard/ToolUniverse/releases))

### Biosciences Skills (Fuzzy-to-Fact Protocol)

These 9 skills implement the **Fuzzy-to-Fact protocol** — a bi-modal discipline where every entity (gene, drug, disease) passes through a LOCATE step (fuzzy search) before a RETRIEVE step (strict lookup by canonical ID). This prevents hallucination by ensuring all facts trace to API calls, not training knowledge. See [references/fuzzy-to-fact.md](references/fuzzy-to-fact.md).

| Skill | What It Does | Databases |
|-------|-------------|-----------|
| **biosciences-genomics** | Gene resolution and cross-referencing | HGNC, Ensembl, NCBI Entrez |
| **biosciences-proteomics** | Protein interactions and network expansion | UniProt, STRING, BioGRID |
| **biosciences-pharmacology** | Drug discovery and mechanism lookup | ChEMBL, PubChem, IUPHAR, Open Targets |
| **biosciences-clinical** | Disease associations and trial discovery | Open Targets, ClinicalTrials.gov |
| **biosciences-crispr** | CRISPR essentiality screen validation | BioGRID ORCS |
| **biosciences-graph-builder** | Full pipeline orchestrator (Phases 1-6a) | All 12 databases |
| **biosciences-reporting** | Template-based report formatting with evidence grading | — (consumes pipeline data) |
| **biosciences-reporting-quality-review** | 10-dimension quality assessment | — (evaluates reports) |
| **biosciences-publication-pipeline** | Publication outputs: report, KG, Synapse grounding, quality review, BioRxiv draft | Synapse MCP only |

### Analysis Skills (Lab & Sequencing)

#### Single-Cell RNA QC
Automated quality control for scRNA-seq data following scverse best practices. Supports `.h5ad` and `.h5` files with MAD-based filtering and comprehensive visualizations.

#### scvi-tools
Deep learning toolkit for single-cell omics. Covers scVI, scANVI, totalVI, PeakVI, MultiVI, DestVI, veloVI, and sysVI models for integration, batch correction, label transfer, and multi-modal analysis.

#### Nextflow Pipelines
Run nf-core bioinformatics pipelines on local or public GEO/SRA sequencing data:
- **rnaseq** — Gene expression and differential expression
- **sarek** — Germline and somatic variant calling (WGS/WES)
- **atacseq** — Chromatin accessibility analysis

#### Instrument Data to Allotrope
Convert laboratory instrument output files (PDF, CSV, Excel, TXT) to Allotrope Simple Model (ASM) format. Supports 40+ instrument types including cell counters, spectrophotometers, plate readers, qPCR, and chromatography systems.

#### Scientific Problem Selection
Systematic framework for research problem selection based on Fischbach & Walsh's framework. Includes 9 skills covering ideation, risk assessment, optimization, decision trees, adversity planning, and synthesis.

### Commands

| Command | What It Does |
|---------|-------------|
| `/start` | Set up environment, check connected tools, survey available skills |
| `/ob-research` | Run graph-based research on a competency question (Phases 1-6a) |
| `/ob-report` | Format a professional report with evidence grading from pipeline output |
| `/ob-review` | Run a 10-dimension quality review on a report |
| `/ob-publish` | Generate full publication pipeline: report, KG JSON, Synapse grounding, quality review, BioRxiv draft |

## Getting Started

```bash
# Install the plugin
/install anthropics/knowledge-work-plugins bio-research

# Run the start command to see available tools
/start
```

## Common Workflows

**Graph-Based Drug Discovery** (uses biosciences skills)
Ask a competency question with `/ob-research`, format results with `/ob-report`, review quality with `/ob-review`, and generate publication files with `/ob-publish`. Example: `/ob-research What drugs targeting BCL2 could treat chronic lymphocytic leukemia?`

**Literature Review**
Search ~~literature database for papers, access full-text through ~~journal access, and create figures with ~~scientific illustration.

**Single-Cell Analysis**
Run QC on scRNA-seq data, then use scvi-tools for integration, batch correction, and cell type annotation.

**Sequencing Pipeline**
Download public data from GEO/SRA, run nf-core pipelines (RNA-seq, variant calling, ATAC-seq), and verify outputs.

**Drug Target Exploration** (uses partner MCPs)
Search ~~chemical database for bioactive compounds, use ~~drug target database for target prioritization, and review clinical trial data. For structured multi-database research, use `/ob-research` instead.

**Research Strategy**
Pitch a new idea, troubleshoot a stuck project, or evaluate strategic decisions using the scientific problem selection framework.

## License

Skills are licensed under Apache 2.0. MCP servers are provided by their respective authors — see individual server documentation for terms.

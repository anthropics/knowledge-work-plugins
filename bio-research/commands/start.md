---
description: Set up your bio-research environment and explore available tools
---

# Bio-Research Start

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

You are helping a biological researcher get oriented with the bio-research plugin. Walk through the following steps in order.

## Step 1: Welcome

Display this welcome message:

```
Bio-Research Plugin

Your AI-powered research assistant for the life sciences. This plugin brings
together literature search, data analysis pipelines, structured research
workflows, and scientific strategy — all in one place.
```

## Step 2: Check Available MCP Servers

Test which MCP servers are connected by listing available tools. Group the results:

**Life Sciences Databases:**
- biosciences-mcp — unified gateway for gene, protein, drug, pathway, and trial databases (HGNC, UniProt, STRING, BioGRID, ChEMBL, Open Targets, PubChem, IUPHAR, WikiPathways, ClinicalTrials.gov, Ensembl, Entrez)

**Literature & Data Sources:**
- ~~literature — biomedical literature search
- ~~literature — preprint access (biology and medicine)
- ~~journal access — academic publications
- ~~data repository — collaborative research data (Sage Bionetworks)

**Drug Discovery & Clinical:**
- ~~chemical database — bioactive compound database
- ~~drug targets — drug target discovery platform
- ~~clinical trials — clinical trial registry

**Visualization & AI:**
- ~~scientific illustration — create scientific figures and diagrams
- ~~AI research — AI for biology (histopathology, drug discovery)

Report which servers are connected and which are not yet set up.

## Step 3: Survey Available Skills

List the skills available in this plugin:

**Biosciences domain skills** (structured research using life sciences APIs):

| Skill | What It Does |
|-------|-------------|
| **biosciences-genomics** | Gene resolution via HGNC, Ensembl, NCBI Entrez |
| **biosciences-proteomics** | Protein interactions via UniProt, STRING, BioGRID |
| **biosciences-pharmacology** | Drug discovery via ChEMBL, PubChem, IUPHAR, Open Targets |
| **biosciences-clinical** | Disease associations and trials via Open Targets, ClinicalTrials.gov |
| **biosciences-crispr** | CRISPR essentiality validation via BioGRID ORCS |
| **biosciences-graph-builder** | Entity resolution, network expansion, knowledge graph construction |
| **biosciences-reporting** | Report formatting with evidence grading |
| **biosciences-reporting-quality-review** | 10-dimension quality assessment |
| **biosciences-publication-pipeline** | Publication outputs: report, KG JSON, Synapse grounding, quality review, BioRxiv draft |

**Analysis skills** (lab and sequencing workflows):

| Skill | What It Does |
|-------|-------------|
| **Single-Cell RNA QC** | Quality control for scRNA-seq data with MAD-based filtering |
| **scvi-tools** | Deep learning for single-cell omics (scVI, scANVI, totalVI, PeakVI, etc.) |
| **Nextflow Pipelines** | Run nf-core pipelines (RNA-seq, WGS/WES, ATAC-seq) |
| **Instrument Data Converter** | Convert lab instrument output to Allotrope ASM format |
| **Scientific Problem Selection** | Systematic framework for choosing research problems |

**Commands** (orchestrate the biosciences skills):

| Command | What It Does |
|---------|-------------|
| `/ob-research` | Structured research on a competency question — entity resolution, network expansion, drug/trial discovery |
| `/ob-report` | Format findings as a report with evidence grading |
| `/ob-review` | Quality review against 10 evaluation dimensions |
| `/ob-publish` | Generate publication files (report, KG JSON, Synapse grounding, quality review, BioRxiv draft) |

## Step 4: Optional Setup — Binary MCP Servers

Mention that two additional MCP servers are available as separate installations:

- **~~genomics platform** — Access cloud analysis data and workflows
  Install: Download `txg-node.mcpb` from https://github.com/10XGenomics/txg-mcp/releases
- **~~tool database** (Harvard MIMS) — AI tools for scientific discovery
  Install: Download `tooluniverse.mcpb` from https://github.com/mims-harvard/ToolUniverse/releases

These require downloading binary files and are optional.

## Step 5: Ask How to Help

Ask the researcher what they're working on today. Suggest starting points based on common workflows:

1. **Literature review** — "Search ~~literature for recent papers on [topic]"
2. **Analyze sequencing data** — "Run QC on my single-cell data" or "Set up an RNA-seq pipeline"
3. **Drug discovery** — "Search ~~chemical database for compounds targeting [protein]" or "Find drug targets for [disease]"
4. **Graph-based research** — "Run `/ob-research What drugs targeting BCL2 could treat CLL?`"
5. **Data standardization** — "Convert my instrument data to Allotrope format"
6. **Research strategy** — "Help me evaluate a new project idea"

Wait for the user's response and guide them to the appropriate tools and skills.

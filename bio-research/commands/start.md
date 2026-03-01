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

Your AI-powered research assistant for the life sciences, built on the
Open Biosciences platform. This plugin combines a 34-tool MCP gateway
spanning 12 databases, 9 domain skills implementing the Fuzzy-to-Fact
research protocol, 5 analysis skills for sequencing and lab data, and
10 partner MCP servers — all in one package.
```

## Step 2: Check Available MCP Servers

Test which MCP servers are connected by listing available tools. Group the results:

**Biosciences-MCP Gateway (primary — 34 tools across 12 databases):**
- biosciences-mcp — HGNC, UniProt, STRING, BioGRID, ChEMBL, Open Targets, PubChem, IUPHAR, WikiPathways, ClinicalTrials.gov, Ensembl, Entrez

This is the core research engine. All biosciences skills and `/ob-research` use it. Test with a lightweight call:
```
Call hgnc_search_genes with: {"query": "TP53", "slim": true, "page_size": 1}
```

**Partner MCP Servers:**

Literature & Data Sources:
- ~~literature — biomedical literature search
- ~~literature — preprint access (biology and medicine)
- ~~journal access — academic publications
- ~~data repository — collaborative research data (Sage Bionetworks)

Drug Discovery & Clinical:
- ~~chemical database — bioactive compound database
- ~~drug targets — drug target discovery platform
- ~~clinical trials — clinical trial registry

Visualization & AI:
- ~~scientific illustration — create scientific figures and diagrams
- ~~AI research — AI for biology (histopathology, drug discovery)

Report which servers are connected and which are not yet set up.

## Step 3: Survey Available Skills

List the skills available in this plugin, organized by type:

**Biosciences Skills** (Fuzzy-to-Fact protocol — structured, API-grounded research):

| Skill | What It Does |
|-------|-------------|
| **biosciences-genomics** | Gene resolution via HGNC, Ensembl, NCBI Entrez |
| **biosciences-proteomics** | Protein interactions via UniProt, STRING, BioGRID |
| **biosciences-pharmacology** | Drug discovery via ChEMBL, PubChem, IUPHAR, Open Targets |
| **biosciences-clinical** | Disease associations and trial discovery via Open Targets, ClinicalTrials.gov |
| **biosciences-crispr** | CRISPR essentiality screen validation via BioGRID ORCS |
| **biosciences-graph-builder** | Full pipeline orchestrator — resolves entities, builds knowledge graphs (Phases 1-6a) |
| **biosciences-reporting** | Template-based report formatting with L1-L4 evidence grading |
| **biosciences-reporting-quality-review** | 10-dimension quality assessment for reports |
| **biosciences-publication-pipeline** | Generates 5 publication files: report, KG JSON, Synapse grounding, quality review, BioRxiv draft |

**Analysis Skills** (lab and sequencing workflows):

| Skill | What It Does |
|-------|-------------|
| **Single-Cell RNA QC** | Quality control for scRNA-seq data with MAD-based filtering |
| **scvi-tools** | Deep learning for single-cell omics (scVI, scANVI, totalVI, PeakVI, etc.) |
| **Nextflow Pipelines** | Run nf-core pipelines (RNA-seq, WGS/WES, ATAC-seq) |
| **Instrument Data Converter** | Convert lab instrument output to Allotrope ASM format |
| **Scientific Problem Selection** | Systematic framework for choosing research problems |

## Step 4: Survey Available Commands

List the commands that orchestrate the biosciences pipeline:

| Command | What It Does |
|---------|-------------|
| `/ob-research` | Run graph-based research on a competency question — resolves entities, builds interaction networks, discovers drugs and trials, validates findings, persists a knowledge graph |
| `/ob-report` | Format a professional report with template selection and L1-L4 evidence grading |
| `/ob-review` | Run a 10-dimension quality review on a report |
| `/ob-publish` | Generate the full publication pipeline — report, KG JSON, Synapse grounding, quality review, BioRxiv draft |

These commands form a pipeline: `/ob-research` → `/ob-report` → `/ob-review` → `/ob-publish`. Each also works standalone.

## Step 5: Optional Setup — Binary MCP Servers

Mention that two additional MCP servers are available as separate installations:

- **~~genomics platform** — Access cloud analysis data and workflows
  Install: Download `txg-node.mcpb` from https://github.com/10XGenomics/txg-mcp/releases
- **~~tool database** (Harvard MIMS) — AI tools for scientific discovery
  Install: Download `tooluniverse.mcpb` from https://github.com/mims-harvard/ToolUniverse/releases

These require downloading binary files and are optional.

## Step 6: Ask How to Help

Ask the researcher what they're working on today. Suggest starting points based on common workflows:

1. **Graph-based research** — "Run `/ob-research What drugs targeting BCL2 could treat CLL?`" to build a knowledge graph with drug candidates, clinical trials, and evidence grading
2. **Literature review** — "Search ~~literature for recent papers on [topic]"
3. **Analyze sequencing data** — "Run QC on my single-cell data" or "Set up an RNA-seq pipeline"
4. **Drug target exploration** — "Search ~~chemical database for compounds targeting [protein]" or "Find drug targets for [disease]"
5. **Data standardization** — "Convert my instrument data to Allotrope format"
6. **Research strategy** — "Help me evaluate a new project idea"

Wait for the user's response and guide them to the appropriate tools and skills.

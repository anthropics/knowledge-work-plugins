---
name: start
description: Set up your bio-research environment and explore available tools. Use when first getting oriented with the plugin, checking which literature, drug-discovery, or visualization MCP servers are connected, or surveying available analysis skills before starting a new project.
---

# Bio-Research Start

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

You are helping a biological researcher get oriented with the bio-research plugin. Walk through the following steps in order.

## Step 1: Welcome

Display this welcome message:

```
Bio-Research Plugin

Your AI-powered research assistant for the life sciences. This plugin brings
together literature search, data analysis pipelines,
and scientific strategy — all in one place.
```

## Step 2: Check Available MCP Servers

Test which MCP servers are connected by listing available tools. Group the results:

**Literature & Data Sources:**
- Literature search (e.g. PubMed, Semantic Scholar) — biomedical literature search
- Preprint server (e.g. bioRxiv) — preprint access (biology and medicine)
- Journal access (e.g. Wiley Scholar Gateway) — academic publications
- Data repository (e.g. Synapse/Zenodo) — collaborative research data

**Drug Discovery & Clinical:**
- Chemical database (e.g. ChEMBL, PubChem) — bioactive compound database
- Drug target database (e.g. Open Targets, UniProt) — drug target discovery platform
- ClinicalTrials.gov — clinical trial registry

**Visualization & AI:**
- Scientific illustration tool (e.g. BioRender) — create scientific figures and diagrams
- AI research platform (e.g. Owkin) — AI for biology (histopathology, drug discovery)

Report which servers are connected and which are not yet set up.

## Step 3: Survey Available Skills

List the analysis skills available in this plugin:

| Skill | What It Does |
|-------|-------------|
| **Single-Cell RNA QC** | Quality control for scRNA-seq data with MAD-based filtering |
| **scvi-tools** | Deep learning for single-cell omics (scVI, scANVI, totalVI, PeakVI, etc.) |
| **Nextflow Pipelines** | Run nf-core pipelines (RNA-seq, WGS/WES, ATAC-seq) |
| **Instrument Data Converter** | Convert lab instrument output to Allotrope ASM format |
| **Scientific Problem Selection** | Systematic framework for choosing research problems |

## Step 4: Optional Setup — Binary MCP Servers

Mention that two additional MCP servers are available as separate installations:

- **Genomics platform (e.g. 10x Genomics)** — Access cloud analysis data and workflows
  Install: Download `txg-node.mcpb` from https://github.com/10XGenomics/txg-mcp/releases
- **Tool database (Harvard MIMS ToolUniverse)** — AI tools for scientific discovery
  Install: Download `tooluniverse.mcpb` from https://github.com/mims-harvard/ToolUniverse/releases

These require downloading binary files and are optional.

## Step 5: Ask How to Help

Ask the researcher what they're working on today. Suggest starting points based on common workflows:

1. **Literature review** — "Search for recent papers on [topic]"
2. **Analyze sequencing data** — "Run QC on my single-cell data" or "Set up an RNA-seq pipeline"
3. **Drug discovery** — "Search for compounds targeting [protein]" or "Find drug targets for [disease]"
4. **Data standardization** — "Convert my instrument data to Allotrope format"
5. **Research strategy** — "Help me evaluate a new project idea"

Wait for the user's response and guide them to the appropriate tools and skills.

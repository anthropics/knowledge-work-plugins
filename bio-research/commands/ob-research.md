---
description: Run graph-based research on a competency question using the Fuzzy-to-Fact protocol
argument-hint: "<competency question>"
---

# Bio-Research: Graph-Based Research

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

You are running graph-based research using the **Fuzzy-to-Fact protocol** (Phases 1-6a). This command orchestrates the `biosciences-graph-builder` skill to resolve entities, build an interaction network, discover drugs and trials, validate findings, and persist a knowledge graph. See [fuzzy-to-fact.md](../references/fuzzy-to-fact.md) for protocol details.

## Usage

```
/ob-research $ARGUMENTS
```

Where `$ARGUMENTS` is a competency question (CQ) — a specific, falsifiable research question.

## How It Works

```
  Competency Question
         │
    ┌────v────┐
    │ Phase 1 │  ANCHOR — resolve genes, drugs, diseases to CURIEs
    │ Phase 2 │  ENRICH — decorate with metadata + cross-references
    │ Phase 3 │  EXPAND — build interaction network (STRING, BioGRID, WikiPathways)
    │ Phase 4a│  TRAVERSE_DRUGS — find drugs targeting identified proteins
    │ Phase 4b│  TRAVERSE_TRIALS — find clinical trials for identified drugs
    │ Phase 5 │  VALIDATE — verify every NCT ID, mechanism, gene-disease link
    │ Phase 6a│  PERSIST — format as JSON, persist to Graphiti
    └────┬────┘
         │
    Knowledge Graph JSON
```

## Workflow

### Step 1: Parse the Competency Question

Extract from `$ARGUMENTS`:
- **Entities**: Gene symbols, drug names, disease terms to resolve
- **Scope**: Which phases apply (e.g., network-only questions skip Phase 4a/4b)
- **Output type**: Drug discovery, gene network, mechanism, safety, clinical landscape, target validation, or regulatory

If the CQ is vague, ask the user to refine it before proceeding.

### Step 2: Check Tool Availability

Verify the biosciences-mcp gateway is connected by testing a lightweight call:

```
Call hgnc_search_genes with: {"query": "TP53", "slim": true, "page_size": 1}
```

If the gateway is unavailable, check for partner MCPs as fallbacks:
- ~~drug targets — Open Targets platform
- ~~chemical database — ChEMBL compound search
- ~~clinical trials — ClinicalTrials.gov trial search
- ~~data repository — Synapse dataset grounding

Report connected and missing tools before proceeding.

### Step 3: Execute Fuzzy-to-Fact Phases

Run Phases 1-6a as defined in the `biosciences-graph-builder` skill:

1. **Phase 1 ANCHOR**: LOCATE each entity via search endpoints (`slim=true`), then RETRIEVE canonical CURIEs. Start with HGNC for genes — fastest and most reliable.
2. **Phase 2 ENRICH**: RETRIEVE full metadata for each CURIE. Extract UniProt function text, Ensembl IDs, and cross-references needed for downstream phases.
3. **Phase 3 EXPAND**: LOCATE interaction partners via STRING, RETRIEVE pathway membership via WikiPathways. Run secondary entity enrichment (HGNC + WikiPathways) for each high-confidence interactor before leaving this phase.
4. **Phase 4a TRAVERSE_DRUGS**: LOCATE drugs via Open Targets (primary) or ChEMBL (fallback). For gain-of-function diseases, filter out agonists.
5. **Phase 4b TRAVERSE_TRIALS**: LOCATE trials by drug+disease via ClinicalTrials.gov. Search each drug separately.
6. **Phase 5 VALIDATE**: RETRIEVE verification for every NCT ID, drug mechanism, and gene-disease link. Mark each as VALIDATED, INVALID, or UNVERIFIABLE.
7. **Phase 6a PERSIST**: Validate all gene nodes have required fields (symbol, name, ensembl, uniprot, location). Persist aggregate counts in metadata. Format as JSON and persist to Graphiti if available.

### Step 4: Present Results

After completing Phases 1-6a, summarize:
- **Entities resolved**: Count of genes, proteins, compounds, diseases with CURIEs
- **Network summary**: Node count, edge count, hub genes, key pathways
- **Drugs found**: Candidates with phases, mechanisms, and targets
- **Trials found**: NCT IDs with phases and recruitment status
- **Validation verdicts**: Counts of VALIDATED, INVALID, UNVERIFIABLE findings
- **KG JSON location**: Where the knowledge graph was saved (file or conversation context)

### Step 5: Offer Next Steps

Suggest the user's next options:

- Run `/ob-report` to format a professional report with evidence grading from the KG JSON
- Run `/ob-review` after reporting to evaluate the report against the 10-dimension quality framework
- Run `/ob-publish` to generate the full publication pipeline (report, Synapse grounding, quality review, BioRxiv draft)
- Refine the competency question and re-run `/ob-research` for deeper exploration

## Tips

- **Be specific**: "What drugs targeting BCL2 could treat CLL?" works better than "Tell me about cancer drugs"
- **Mention the disease**: Disease context activates Phase 4a/4b drug and trial discovery
- **Check API keys first**: Run `/start` to verify which MCP servers are connected before running a long pipeline
- **Token budgeting**: The pipeline uses `slim=true` during LOCATE phases automatically — no manual intervention needed

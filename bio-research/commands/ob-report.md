---
description: Format a professional report with evidence grading from Fuzzy-to-Fact pipeline output
argument-hint: "<KG JSON path or 'use conversation context'>"
---

# Bio-Research: Report Formatting

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

You are formatting a professional report from completed Fuzzy-to-Fact pipeline output (Phases 1-6a). This command orchestrates the `biosciences-reporting` skill to select a template, grade evidence, and produce a publication-ready report. See [fuzzy-to-fact.md](../references/fuzzy-to-fact.md) for protocol context.

## Usage

```
/ob-report $ARGUMENTS
```

Where `$ARGUMENTS` is a path to KG JSON from `/ob-research`, or `"use conversation context"` to use pipeline data from the current session.

## Input

This command requires completed Phase 1-6a output:
- **KG JSON** with `nodes`, `edges`, and `metadata` arrays
- **Phase narrative** from the conversation (entity resolutions, tool call results, validation verdicts)

If the input is missing or malformed, ask the user to run `/ob-research` first.

## Workflow

### Step 1: Load Pipeline Output

Read the KG JSON (from file or conversation context). Validate it contains:
- `nodes` array with entity CURIEs and properties
- `edges` array with source/target/type
- `metadata` with `phases_completed`, `data_sources`, and aggregate counts

If validation fails, report what's missing and suggest re-running `/ob-research`.

### Step 2: Select Report Template

Route the competency question through the template decision tree:

```
Query about drug mechanism?            → Template 6: Mechanism Elucidation
Query about drug safety/off-targets?   → Template 7: Safety / Off-Target
Query about regulatory/filings?        → Template 5: Regulatory / Commercialization
Query about finding/repurposing drugs? → Template 1: Drug Discovery / Repurposing
Query about gene/protein interactions? → Template 2: Gene / Protein Network
Query about clinical trials broadly?   → Template 3: Clinical Landscape
Query about validating a target?       → Template 4: Target Validation
Multiple categories?                   → Combine sections from relevant templates
```

For multi-template queries, share Resolved Entities and Evidence Assessment sections across templates and include distinctive sections from each.

### Step 3: Grade Evidence

Apply the L1-L4 evidence grading system to each claim:

| Level | Range | Name | Criteria |
|-------|-------|------|----------|
| L4 | 0.90-1.00 | Clinical | FDA-approved or Phase 2+ with published endpoints |
| L3 | 0.70-0.89 | Functional | Multi-DB concordance + druggable target + known mechanism |
| L2 | 0.50-0.69 | Multi-DB | 2+ independent API endpoints confirm the relationship |
| L1 | 0.30-0.49 | Single-DB | One database source only |

Apply modifiers: active trial (+0.10), mechanism match (+0.10), literature support (+0.05), high STRING score (+0.05), conflicting evidence (-0.10), single source (-0.10), unverified ID (-0.15), mechanism mismatch (-0.20).

Compute **median** confidence across all claim scores. Report the range (lowest to highest).

### Step 4: Format Report

Apply the selected template structure from the `biosciences-reporting` skill:
- **Resolved Entities** table with CURIEs and source citations
- **Template-specific sections** (Drug Candidates, Interaction Network, Mechanism Chain, etc.)
- **Evidence Assessment** with claim-level grades and overall confidence
- **Gaps and Limitations** — what was not found, which tools returned errors

Ensure every factual claim includes a `[Source: tool(param)]` citation. If a phase returned no results for a section, write "No data retrieved" with the tool name — do not fill gaps from training knowledge.

### Step 5: Offer Next Steps

Suggest the user's next options:

- Run `/ob-review` to evaluate the report against the 10-dimension quality framework
- Run `/ob-publish` to generate the full publication pipeline (adds Synapse grounding, quality review, BioRxiv draft)

## Tips

- **No new API calls**: This command synthesizes existing Phase 1-6a data. It does not call life sciences APIs.
- **Multi-template queries**: When a question spans drug discovery and mechanism (e.g., "What drugs targeting the BMP pathway could be repurposed for FOP?"), combine Template 1 + Template 6 sections.
- **Unsourced claims**: If you find yourself writing a factual claim without a `[Source: tool(param)]` citation, stop — the claim either needs a source from the pipeline data or should not be included.

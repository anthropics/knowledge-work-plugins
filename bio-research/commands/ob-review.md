---
description: Run a structured quality review on a Fuzzy-to-Fact report
argument-hint: "<report path and KG JSON path>"
---

# Bio-Research: Quality Review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

You are running a structured quality review using the `biosciences-reporting-quality-review` skill. This evaluates a report against 10 dimensions, distinguishes protocol failures from presentation gaps, and produces a scored assessment.

## Usage

```
/ob-review $ARGUMENTS
```

Where `$ARGUMENTS` includes:
- Path to the report markdown file
- Path to the KG JSON file
- Optionally, path to Synapse grounding document

If paths are not provided, use artifacts from the current conversation context.

## Input

This command requires:
- **Report markdown** — the formatted report from `/ob-report` or the publication pipeline
- **KG JSON** — the knowledge graph from `/ob-research` Phase 6a output

Optional:
- **Synapse grounding document** — if available from `/ob-publish` Stage 1b

## Workflow

### Step 1: Gather Artifacts

Read artifacts in this order (critical for accurate review):

1. **KG JSON first** — check the knowledge graph before concluding that protocol steps weren't executed. Many steps execute correctly but aren't documented in the final report.
2. **Report markdown** — evaluate against template and grading standards
3. **Synapse grounding** (if available) — verify cross-file consistency

### Step 2: Identify Template

Determine which reporting template (1-7) the report uses:

- **Template 1**: Drug Discovery/Repurposing — has "Drug Candidates" table with CHEMBL IDs
- **Template 2**: Gene/Protein Network — has "Interaction Network" and "Hub Genes" tables
- **Template 3**: Clinical Landscape — has trial tables with NCT IDs and recruitment status
- **Template 4**: Target Validation — has tractability assessment and druggability scoring
- **Template 5**: Regulatory/Commercialization — has regulatory timeline and market analysis
- **Template 6**: Mechanism Elucidation — has mechanism chain table with step-by-step process
- **Template 7**: Safety/Off-Target — has off-target hits and selectivity comparison

Record the template — it determines which dimensions are required, optional, or N/A.

### Step 3: Evaluate 10 Dimensions

Apply each dimension using template-specific criteria:

| Dimension | Check |
|-----------|-------|
| 1. CURIE Resolution | All core entities resolved to canonical CURIEs (HGNC:, CHEMBL:, MONDO:) |
| 2. Source Attribution | >90% of claims cite `[Source: tool(param)]` |
| 3. LOCATE-RETRIEVE | Two-step pattern documented for entity types |
| 4. Disease CURIE | Present when required by template (required for T1/T4/T6; optional for T2 without Phase 4) |
| 5. OT Pagination | Uses `size`-only pattern for Open Targets knownDrugs (N/A if OT not used) |
| 6. Evidence Grading | Claim-level numeric grading with L1-L4 levels and modifiers |
| 7. GoF Filter | Agonists excluded for gain-of-function diseases (N/A if not GoF) |
| 8. Trial Validation | All NCT IDs verified via clinicaltrials_get_trial |
| 9. Completeness | Competency question fully answered with all components |
| 10. Hallucination Risk | LOW/MEDIUM/HIGH — check for unsourced statistics, fabricated IDs, ungrounded claims |

Score each dimension as **PASS**, **PARTIAL**, **FAIL**, or **N/A** with justification.

### Step 4: Classify Failures

For each FAIL or PARTIAL dimension, classify the root cause:

| Classification | Meaning | Severity |
|---------------|---------|----------|
| **Protocol failure** | Required step not executed — entity not in graph, no tool call made | Critical |
| **Presentation failure** | Step executed (in graph) but not shown in report | Moderate |
| **Documentation error** | Step shown but incorrectly attributed or cited | Minor |

### Step 5: Produce Review Output

Generate a structured quality review document:

```markdown
## Summary Verdict
- **Overall**: PASS / PARTIAL / FAIL
- **Template**: [identified template number and name]
- **Top issues**: [1-3 most significant findings]

## Dimension Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| 1. CURIE Resolution | [PASS/PARTIAL/FAIL/N/A] | [brief justification] |
| ... | | |

## Detailed Findings
[Per-dimension evidence, issues found, positive observations]

## Failure Classification
[For each FAIL/PARTIAL: type, severity, specific recommendation]

## Overall Assessment
- Protocol execution: [0-10]
- Report presentation: [0-10]
- Overall verdict with justification
```

### Step 6: Offer Next Steps

Based on the review verdict:

- **PASS or PARTIAL**: Suggest running `/ob-publish` to generate the full publication pipeline
- **FAIL**: Identify specific fixes needed, then suggest re-running `/ob-report` after corrections

## Tips

- **Read the graph first**: The #1 reviewer mistake is marking a dimension as FAIL when the data exists in the KG JSON but wasn't shown in the report. That's a presentation failure (PARTIAL), not a protocol failure (FAIL).
- **Template matters**: Template 2 (Gene/Protein Network) does not require disease CURIEs or trial validation unless drug/trial phases were explicitly executed. Check the applicability matrix before scoring.
- **Paraphrasing is not hallucination**: Faithful paraphrasing of UniProt function text (e.g., "Binds to 3 E-boxes" → "binds E-boxes in CDH1 promoter") is acceptable synthesis, not a hallucination. Only flag claims that introduce information not present in any tool call.

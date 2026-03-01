---
description: Run the full publication pipeline from Fuzzy-to-Fact pipeline output
argument-hint: "<CQ slug and output directory>"
---

# Bio-Research: Publication Pipeline

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

You are running the full publication pipeline using the `biosciences-publication-pipeline` skill. This produces 5 publication-quality files from completed Fuzzy-to-Fact pipeline data (Phases 1-6a).

## Usage

```
/ob-publish $ARGUMENTS
```

Where `$ARGUMENTS` includes:
- **CQ slug**: Kebab-case identifier for the competency question (e.g., `doxorubicin-nf1-toxicity`)
- **Output directory**: Where to write files (default: `output/cqs/{slug}/`)

## Input

**Required**: Phase 1-6a data from `/ob-research` (KG JSON with nodes, edges, metadata).

**Optional**: Phase 6b report from `/ob-report` — if available, Stage 1a reuses it instead of regenerating.

## Publication Files

| File | Naming Pattern | Stage |
|------|---------------|-------|
| Report | `{slug}-report.md` | 1a |
| Knowledge Graph | `{slug}-knowledge-graph.json` | 1a |
| Synapse Grounding | `{slug}-synapse-grounding.md` | 1b |
| Quality Review | `{slug}-quality-review.md` | 2 |
| BioRxiv Draft | `{slug}-biorxiv-draft.md` | 3 |

## Workflow

### Stage 1a: Report Formatting

If `/ob-report` output is available, use it directly. Otherwise, run the `biosciences-reporting` skill:

1. Select template via the decision tree (Templates 1-7)
2. Apply L1-L4 evidence grading with modifiers to each claim
3. Format with `[Source: tool(param)]` citations on every factual claim
4. Write `{slug}-report.md` and `{slug}-knowledge-graph.json`

The KG JSON follows the standard schema with `nodes`, `edges`, and `metadata` arrays. Each node and edge includes empty `synapse_grounding` arrays to be populated in Stage 1b.

### Stage 1b: Synapse Dataset Grounding

If ~~data repository is connected, ground KG entities against Synapse.org datasets:

1. **Check domain coverage** — Synapse has strong coverage for neurodegenerative and neurofibromatosis domains but limited coverage for cardiovascular, lysosomal storage, and rare metabolic diseases
2. **Search with compound queries first** — `"gene disease"` and `"compound disease"` queries have much higher precision than single-term searches
3. **Classify grounding strength** for each match:
   - **Strong**: Dataset directly tests the mechanistic claim
   - **Moderate**: Dataset profiles relevant genes/pathways in the same disease
   - **Analogous**: Same mechanism tested in a related disease or model system
   - **Weak**: Contextual or pathway-level support only
4. **Inject grounding** into KG JSON `synapse_grounding` arrays and write `{slug}-synapse-grounding.md`

If ~~data repository is not connected, skip Stage 1b gracefully. Write a minimal Synapse grounding document noting that the data repository was not available, and leave `synapse_grounding` arrays empty in the KG JSON.

### Stage 2: Quality Review

Run the `biosciences-reporting-quality-review` skill's 10-dimension framework (same as `/ob-review`):

1. Read KG JSON first, then report, then Synapse grounding
2. Identify the template type
3. Evaluate all 10 dimensions with template-specific criteria
4. Classify failures as protocol, presentation, or documentation
5. Write `{slug}-quality-review.md`

If `/ob-review` was already run on this report, note the prior review and highlight any changes since then.

### Stage 3: BioRxiv Manuscript Draft

Generate `{slug}-biorxiv-draft.md` in IMRaD format using all prior outputs:

| Section | Target Length |
|---------|--------------|
| Abstract | 250-350 words |
| 1. Introduction | 500-800 words |
| 2. Methods | 800-1200 words |
| 3. Results | 1500-2500 words |
| 4. Discussion | 800-1200 words |
| References | All `[Source: tool(param)]` citations converted to numbered references |
| Supplementary | S1: KG Nodes, S2: KG Edges, S3: Evidence Grading, S4: Synapse Mapping |

Convert inline `[Source: tool(param)]` citations to numbered references grouped by database category.

### Stage 4: Verification Checklist

Run 8 automated checks on all outputs:

1. **File existence**: All 5 files exist in `{output_dir}`
2. **JSON validity**: `{slug}-knowledge-graph.json` parses without errors
3. **Node count consistency**: KG JSON node count matches report entity count
4. **Edge count consistency**: KG JSON edge count matches report relationship count
5. **Synapse dataset consistency**: Dataset count in KG JSON metadata matches Synapse grounding document
6. **Disease CURIE consistency**: Same disease CURIE used across all files
7. **NCT ID consistency**: Trial IDs in report match those in BioRxiv draft
8. **No API keys or secrets**: No `.env` content or real API keys in any output file

Report the checklist results. If any check fails, identify the inconsistency and suggest a fix.

## Tips

- **Run `/ob-research` first**: The publication pipeline requires completed Phase 1-6a data. Without it, there's nothing to publish.
- **Synapse coverage varies by domain**: Neurodegenerative and NF1 domains have strong Synapse coverage. Cardiovascular and rare metabolic diseases may yield few or no grounding datasets — this is expected, not a failure.
- **No new facts**: This pipeline does not call life sciences APIs (HGNC, UniProt, STRING, etc.). The only new API calls are Synapse MCP tools in Stage 1b for dataset grounding. All scientific claims must trace to Phase 1-5 tool calls.
- **Standalone or chained**: Each stage validates its own inputs. If `/ob-report` was run separately, Stage 1a reuses that output. If `/ob-review` was run separately, Stage 2 notes the prior review.

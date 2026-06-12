---
description: Magellan knowledge management system — show status or run the full discovery pipeline
---

# Magellan

The main entry point for Magellan. Shows workspace status or runs the full
pipeline (Phase 1 Discovery + Phase 2 Design).

## Usage

```
/magellan                  Run incremental pipeline (or full if first run)
/magellan <path>           Run pipeline on a specific workspace
/magellan --status         Show workspace status only (no processing)
/magellan --full           Force full pipeline re-run (ignore change detection)
/magellan --from-step N    Re-run pipeline starting from Step N (skip earlier steps)
```

## Critical Rules

1. ALL file writes to `.magellan/` MUST follow the schemas defined in the
   file-conventions skill. Read the skill before writing any JSON file.
2. Facts MUST follow the atomic fact schema (required fields: statement, subject,
   subject_domain, predicate, object, source with quote, confidence).
3. Entities are one file per entity in `domains/<domain>/entities/`.
4. Do NOT create a monolithic `knowledge_graph.json`. The KG is stored as individual
   entity files.
5. Facts MUST be organized by domain: `domains/<domain>/facts/<source_document>.json`.
6. When appending to contradictions or open questions, always read the existing file
   first, add to the array, then write back.

## Execution Rules

1. **No background agents.** Every step runs in the foreground. Process files
   sequentially. Complete each step fully before starting the next.

2. **No step skipping.** Every numbered step is MANDATORY. Do not combine steps.
   If a step fails, record the failure and continue — never skip silently.

3. **Quality gate after every step.** Apply the pipeline-review skill after each
   step. Fix blockers before proceeding. Accumulate findings in
   `.magellan/pipeline_feedback.json`.

4. **No subagent delegation.** Every step executes in the main conversation context.

5. **Context hygiene.** Use Glob to count files rather than reading them all.
   Use Read with offset/limit for large files. Read only the fields you need.

## Behavior

When run, determine the target workspace:
- If a path argument is provided, use that path.
- If no argument is provided, use the current working directory.

Then determine the run mode:

- **`--status`** → show status only (Status Mode).
- **`--full`** → force full pipeline re-run.
- **`--from-step N`** → skip to Step N using existing data from earlier steps.
- `.magellan/` does not exist → full pipeline.
- `.magellan/` exists with `last_run` in state.json → incremental mode.
- `.magellan/` exists without `last_run` → show status.

## Status Mode

1. Read `.magellan/state.json` and `.magellan/index.json`.
2. Use Glob to find `domains/*/open_questions.json` and `domains/*/contradictions.json`.
   Read each and count entries.
3. Read `.magellan/processed_files.json` for file tracking data.
4. If `state.json` has `last_run.git_ref`, run `git diff --name-only <ref> HEAD`
   via Bash to detect changes.
5. Display status dashboard:

```
Magellan Knowledge Graph Status
================================
Files tracked:    200 (197 ingested, 3 no_facts)
Domains:          5 (billing, title, transportation, dealer_management, infrastructure)
Total entities:   312
Total edges:      489

Open questions:   12
Contradictions:   4

Top priority items:
  [critical] c_003: Settlement threshold mismatch between code and config
  [high]     oq_003: Is the $10,000 MANUAL_REVIEW threshold still active?
```

If no `.magellan/` directory is found:

```
No Magellan workspace found.
  /magellan /path/to/workspace    Run the full discovery pipeline
  /magellan:add <file>            Add a single document
```

---

## Pipeline

### Step 1: Initialize and Discover Files

**Initialize** (if `.magellan/` doesn't exist):

1. Create directory structure via Bash:
   ```
   mkdir -p .magellan/domains .magellan/diagrams .magellan/language_guides
   ```
2. Write `.magellan/state.json`: `{"initialized_at": "<ISO timestamp>"}`
3. Copy starter language guides from `skills/ingestion/language_guides/` to
   `.magellan/language_guides/` (skip existing — user may have customized).
4. Initialize `.magellan/pipeline_feedback.json` with empty structure.

**Resume check**: If `.magellan/` exists and `state.json` has `pipeline_step`,
offer to resume from the last completed step.

**Discover files**:

- **Full mode**: Use Glob to list all files, excluding `.magellan/` and `.git/`.
- **Incremental mode**: Read `state.json` for `last_run.git_ref`. Use
  `git diff --name-only <ref> HEAD` and `git ls-files --others --exclude-standard`
  via Bash to find new/modified files. Skip unchanged files.

Display: "Found N files to process."

**Quality Gate.** Update state.json.

### Step 2: Extract Facts (Stage 1)

For each file in the processing list:

1. **Check file size** via Bash (`wc -l` for text, `wc -c` for binary).
2. **Read** the file following the ingestion skill's reading strategy:
   - Small files (under ~5,000 lines): read entire file in one pass.
   - Large files (over ~5,000 lines): read in sections using `offset` and `limit`.
     See the "Reading Large Documents" section in the ingestion skill.
   - If it's a code file, check `.magellan/language_guides/` for a matching guide.
     Read the guide once per language (cache in context for subsequent files).
3. **Extract facts** by applying the ingestion skill.
4. **Write facts** to `.magellan/domains/<domain>/facts/<source_slug>.json`
   following the fact schema in file-conventions.
5. **Record disposition** in `.magellan/processed_files.json` (read, update, write back).
6. Display: "Ingested [N/total]: filename (M facts → domain)"

**Track affected domains** as you process files.

If a file cannot be read or produces no facts, record the disposition and continue.
**Nothing is silently skipped.**

After all files, display:

```
File Processing Summary
=======================
Total files:   52
  ingested:    47
  no_facts:     3
  unreadable:   2
  ---
  Accounted:   52/52
```

**Verify — File Ledger Reconciliation:**
1. Count all files in the workspace via Glob (excluding `.magellan/`, `.git/`).
2. Count all entries in `.magellan/processed_files.json`.
3. If workspace files > ledger entries, list the missing files by name.
   These were silently skipped — this is a **blocker**. Process them before continuing.
4. Display: "Ledger: N/N files accounted for ✓" or "MISSING: file1, file2, ..."

**Verify — Fact Count Cross-Check:**
1. For each domain, sum `fact_count` across all files in `domains/<domain>/facts/`.
2. Compare this to the total facts reported during ingestion.
3. If they differ, some facts were lost during write. Flag as blocker.

**Quality Gate.** Update state.json.

### Step 3: Build Graph (Stage 2a)

Build entities and intra-domain relationships from atomic facts.

For each fact file in affected domains:
1. Read the facts.
2. Apply the graph-building skill: process 5-10 facts at a time, write each
   entity immediately to `.magellan/domains/<domain>/entities/<name>.json`.
3. Apply contradiction-detection: compare new facts against existing entities.
   Append contradictions and open questions to the domain's JSON files.
4. Write relationships to `.magellan/domains/<domain>/relationships.json`.
5. Display: "Built: domain (N entities, M relationships)"

**Verify — Entity-to-Source Traceability:**
For each domain, read 3 entities and verify each evidence entry references a
source document that has a corresponding fact file in `domains/<domain>/facts/`.
If an entity cites a source with no matching fact file, flag as warning — the
evidence chain is broken.

**Quality Gate.** Update state.json.

### Step 4: Cross-Domain Linking (Stage 2b)

Separate, mandatory pass. Do NOT fold into Step 3.

1. Use Glob to list all domains.
2. For each domain, list entities and read names + summaries.
3. Compare across domains for SAME_AS candidates.
4. Write `.magellan/cross_domain.json`.
5. Detect cross-domain contradictions.
6. Display: "Cross-domain: N SAME_AS, M relationships"

Skip if fewer than 2 domains.

**Verify — Relationship Integrity:**
Read `cross_domain.json` and each domain's `relationships.json`. For every edge,
verify both the `from` and `to` entity IDs exist as files in their respective
`entities/` directories (use Glob). List any dangling references — these point
to entities that were never created or were lost. Flag as warning.

**Quality Gate.** Update state.json.

### Step 5: Entity Deduplication

Scan each domain for near-duplicate entities (>80% name similarity or
near-identical summaries). Merge duplicates: keep the entity with more evidence,
mark the other as superseded.

**Verify — Evidence Preservation:**
For each merge performed, read the kept entity and verify its `evidence` array
contains entries from both original entities. Count evidence entries before and
after — the kept entity must have ≥ the sum of both originals. If evidence was
lost during merge, flag as blocker and restore from the superseded entity file
(which still exists, marked as superseded).

**Quality Gate.** Update state.json.

### Step 6: Domain Summarization (Stage 2c)

For each domain:
1. Count entities, read relationships, calculate hub scores.
2. Read top 10-15 hub entities.
3. Count contradictions and open questions.
4. Synthesize a 3-8 paragraph narrative.
5. Write `.magellan/domains/<domain>/summary.json`.

**Quality Gate.** Update state.json.

### Step 7: Onboarding Guide

Apply the onboarding-guide skill to generate `.magellan/onboarding_guide.md`.

**Quality Gate.** Update state.json.

### Step 8: Contradictions Dashboard

Apply the dashboard-generation skill to generate the markdown and HTML dashboard.

**Quality Gate.** Update state.json.

### Step 9: C4 Architecture Diagrams

Apply the diagram-generation skill. Generate both Mermaid and PlantUML for
each level (context, containers, per-domain components).

**Quality Gate.** Update state.json.

### Step 10: Update State and Index

1. Update `state.json` with `last_run` block (timestamp, git_ref, mode, file count).
2. Update `index.json` with domain stats.
3. Display status dashboard.

### Step 11: Phase 1 Verification

Verify Phase 1 outputs exist and contain meaningful content:
- At least 1 domain with entities
- Entities have summaries (50+ chars), evidence with quotes, weight > 0
- Relationships exist for domains with 3+ entities
- Domain summaries have narratives (200+ chars) with hubs
- Onboarding guide, dashboard, and diagrams exist

Failure conditions STOP the pipeline. Warning conditions are logged.

---

## Phase 2: Design Generation

Runs automatically after Phase 1 verification.

### Step 12: Business Rules Per Domain

Classify rules as HARD / SOFT / QUESTIONABLE. Cite source entities.

### Step 13: DDD Specs Per Domain

Bounded context: entities, aggregates, events, commands, integration points.

### Step 14: Implementation Contracts Per Domain

API contracts, event schemas, data models, integration contracts.

### Step 15: Per-Domain Review Documents

Decisions, proposed system, differences, risks, open items.

**Quality Gate** for Steps 12-15.

### Step 16: Business Rules Export (MANDATORY)

DMN XML, JSON, CSV, Gherkin — four formats per domain.

**Quality Gate.**

### Step 17: OpenAPI + AsyncAPI Specs (MANDATORY)

Per-domain specs + cross-domain integration specs in `_integration/`.

**Quality Gate.**

### Step 18: Phase 2 Verification

Verify all deliverables exist with meaningful content.

### Step 19-20: Regenerate Dashboard and Diagrams

Capture any new contradictions or relationships from Phase 2.

### Step 21: Update State and Index

Final stats.

### Step 22: Final Summary Report

Display the summary, then run the coverage matrix.

```
Pipeline Complete (Phase 1 + Phase 2)
======================================
Phase 1: Discovery
  Files processed:    47
  Facts extracted:    312
  Entities:           89
  Relationships:      134
  Contradictions:     4
  Open questions:     12

Phase 2: Design
  Business rules:     142 (52 HARD, 63 SOFT, 27 QUESTIONABLE)
  DDD specs:          5 domains
  Rules exports:      DMN, JSON, CSV, Gherkin
  API specs:          OpenAPI + AsyncAPI
```

**Verify — Coverage Matrix:**
For each source document in processed_files.json with disposition `ingested`:
1. Verify it has a corresponding fact file in `domains/<domain>/facts/`.
2. Read the fact file and get the fact_count.
3. Check if any entities reference this source in their evidence arrays.

Display a coverage table:

```
Source Coverage
===============
  Source Document              Facts  Entities  Domain
  Q3_ops_runbook.pdf           12     8         billing
  CBBLKBOOK.cblle              15     6         billing
  dealer_manual.pdf             3     2         dealer_management
  README.md                     0     0         — (no_facts)
  config.bin                    —     —         — (unreadable)
  ---
  47/52 files contributed to the knowledge graph.
  5 files produced no knowledge (3 no_facts, 2 unreadable).
```

Flag any file with disposition `ingested` but 0 entities referencing it — those
facts were extracted but never built into the graph.

```
Next steps:
  /magellan:ask <question>    Query the knowledge graph
  /magellan:add <file>        Add more materials
  /magellan                   Check status
```

---

## Error Handling

Every file must reach a recorded disposition:

| Status | Meaning |
|--------|---------|
| `ingested` | Facts extracted successfully |
| `no_facts` | File read but no extractable facts |
| `unreadable` | File could not be read |
| `extraction_error` | Error during fact extraction |
| `skipped_by_rule` | Excluded by project rule |

Rules:
- Never let a file failure stop the pipeline.
- Every failure is logged with the error and filename.
- The final summary includes counts for every disposition.

## Context Window Management

The pipeline is **resumable**:

- `state.json` tracks the last completed pipeline step.
- `processed_files.json` tracks every file's disposition.
- On resume, processed files are skipped automatically.

When context runs low, save progress and tell the user to run `/magellan` again.

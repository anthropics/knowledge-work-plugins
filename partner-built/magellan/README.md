# Magellan

Enterprise knowledge discovery. Point Magellan at a folder of collected materials —
code, documents, meeting transcripts, API specs, diagrams — and it builds a structured,
queryable knowledge graph organized by business domain. Contradictions and open questions
are surfaced as primary outputs, not side effects.

## Quick Start

```bash
claude plugin install magellan@knowledge-work-plugins
```

```
/magellan                              Run the discovery pipeline
/magellan:add /path/to/document.pdf    Add a file
/magellan:add --correction "..."       Record a verbal correction
/magellan:add --resolve c_001 "..."    Resolve a contradiction
/magellan:add --resolve oq_003 "..."   Answer an open question
/magellan:ask How does billing work?   Query the knowledge graph
```

## What You Get

```
.magellan/
  contradictions_dashboard.md      ← Contradictions & open questions (the priority)
  contradictions_dashboard.html    ← Print-friendly version
  onboarding_guide.md              ← Briefing for new team members
  diagrams/                        ← C4 architecture diagrams (Mermaid + PlantUML)

  domains/<domain>/
    facts/                         ← Atomic facts from source documents
    entities/                      ← One file per knowledge graph entity
    relationships.json             ← How entities connect within this domain
    summary.json                   ← Plain language domain narrative
    contradictions.json            ← What disagrees
    open_questions.json            ← What's unknown
    deliverables/                  ← Business rules, DDD specs, API specs, contracts
```

## How It Works

The pipeline runs in two phases with quality gates after every step:

**Phase 1 — Discovery**: Read files → extract atomic facts → build entities and
relationships → detect contradictions → link across domains → summarize each domain
→ generate onboarding guide, dashboard, and C4 diagrams.

**Phase 2 — Design**: Formalize business rules (HARD / SOFT / QUESTIONABLE) → generate
DDD specs → implementation contracts → export rules as DMN, JSON, CSV, Gherkin →
generate OpenAPI and AsyncAPI specs.

Every fact traces to a source document with an exact quote. Nothing is invented.
On subsequent runs, only new and modified files are processed.

## Input Files

Magellan reads anything Claude can read — text, code, markdown, CSV, JSON, YAML, XML,
PDF, images, and meeting transcripts.

> **Note:** Claude does not yet natively read DOCX, PPTX, or XLSX files. Until it
> does, convert these to PDF before adding them to your workspace.

Includes 12 language guides for legacy systems (RPG, COBOL, CL, DDS, JCL, CICS,
Assembler/370, NATURAL/ADABAS, IDMS, Easytrieve, PL/I, REXX) that improve extraction
precision. Add your own for proprietary languages.

## Installation

```bash
claude plugin install magellan@knowledge-work-plugins
```

Requires only Claude Code. No Python, no build steps, no system dependencies.

## Contributing

- **Skills**: Add or improve domain expertise in `skills/`
- **Language guides**: Add guides for new languages in `skills/ingestion/language_guides/`
- **Feature requests**: Open an issue

Apache 2.0 license.

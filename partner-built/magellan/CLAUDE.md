# CLAUDE.md

Magellan is an enterprise knowledge discovery plugin. It extracts structured
knowledge from collected materials and builds a queryable knowledge graph.

## Commands

- `/magellan` — Run the discovery pipeline or show status
- `/magellan:add <path>` — Add a file or directory
- `/magellan:add --correction "..."` — Record a verbal correction
- `/magellan:ask <question>` — Query the knowledge graph

## Four Principles

1. Every fact traces to a source document. Nothing is invented.
2. Contradictions and open questions are the primary output, not a side effect.
3. Nothing is silently skipped. Every file gets a recorded disposition.
4. The model does the heavy lifting. Humans steer and correct.

## Key Skills

- `skills/file-conventions/` — JSON schemas for all KG file types. Read this
  before writing any file to `.magellan/`.
- `skills/ingestion/` — Fact extraction rules and language guides for legacy code.
- `skills/pipeline-review/` — Quality gate criteria. Run after every pipeline step.

## Output Location

All outputs go in `<workspace>/.magellan/`. See the file-conventions skill for
the complete directory layout and JSON schemas.

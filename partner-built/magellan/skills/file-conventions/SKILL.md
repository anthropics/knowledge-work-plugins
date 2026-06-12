# File Conventions

All Magellan outputs go in `.magellan/` within the workspace root. This skill defines
every file type, its exact JSON schema, path pattern, and validation rules. Follow these
schemas exactly when reading or writing Magellan files.

## Directory Layout

```
.magellan/
├── state.json
├── index.json
├── cross_domain.json
├── processed_files.json
├── pipeline_feedback.json
├── onboarding_guide.md
├── contradictions_dashboard.md
├── contradictions_dashboard.html
├── language_guides/            ← reference guides for legacy languages
├── diagrams/                   ← C4 architecture diagrams (Mermaid + PlantUML)
│   ├── context.mmd / .puml
│   ├── containers.mmd / .puml
│   └── components_<domain>.mmd / .puml
└── domains/
    └── <domain>/
        ├── facts/              ← one file per source document
        │   └── <source>.json
        ├── entities/           ← one file per entity
        │   └── <entity_name>.json
        ├── relationships.json
        ├── summary.json
        ├── contradictions.json
        ├── open_questions.json
        ├── discovered_links.json
        ├── resolved/
        │   ├── contradictions_resolved.json
        │   └── questions_answered.json
        └── deliverables/       ← Phase 2 outputs
            ├── business_rules.md
            ├── ddd_spec.md
            ├── contracts.md
            ├── review.md
            ├── rules_<domain>.dmn
            ├── rules_<domain>.json
            ├── rules_<domain>.csv
            ├── rules_<domain>.feature
            ├── openapi.yaml
            └── asyncapi.yaml
```

## ID Generation

Generate IDs using this pattern:
- **fact_id**: `f_` + 8 random hex chars (e.g., `f_a1b2c3d4`)
- **contradiction_id**: `c_` + 3-digit sequence (e.g., `c_001`)
- **question_id**: `oq_` + 3-digit sequence (e.g., `oq_001`)
- **edge_id**: `e_` + 3-digit sequence (e.g., `e_001`), or `cx_` prefix for cross-domain
- **entity_id**: `<domain>:<snake_case_name>` (e.g., `billing:invoice_generation`)

When generating sequence IDs (c_001, oq_001, e_001), read the existing file first to
find the next available number.

## File Path Safety

Entity IDs containing `/` or spaces are converted to underscores for filenames.
The entity_id `billing:invoice_generation` is stored at
`.magellan/domains/billing/entities/invoice_generation.json`.

---

## Schemas

### Atomic Fact

**Path**: `.magellan/domains/<domain>/facts/<source_document_slug>.json`

The source document slug is the filename with extension replaced (e.g., `Q3_ops_runbook`
for `Q3_ops_runbook.pdf`).

```json
{
  "source_document": "path/to/source.pdf",
  "domain": "billing",
  "extracted_at": "2026-03-15T10:30:45Z",
  "fact_count": 2,
  "facts": [
    {
      "fact_id": "f_a1b2c3d4",
      "statement": "Invoices exceeding $10,000 are routed to MANUAL_REVIEW",
      "subject": "Invoice Generation",
      "subject_domain": "billing",
      "predicate": "has exception rule",
      "object": "Manual review bypass for high-value invoices",
      "source": {
        "document": "Q3_ops_runbook.pdf",
        "location": "page 12, section 'Exception Handling'",
        "quote": "Invoices exceeding $10,000 are routed to MANUAL_REVIEW."
      },
      "confidence": 0.75,
      "tags": ["business_rule", "exception_handling"]
    }
  ]
}
```

**Required fields per fact**: `statement` (min 10 chars), `subject`, `subject_domain`
(lowercase, letters/digits/underscores only), `predicate`, `object`,
`source.document`, `source.location`, `source.quote` (max 500 chars), `confidence`
(0.0–1.0).

**Optional**: `tags` (default empty array). `fact_id` should always be generated.

**Rules**:
- Every fact MUST have a source quote. No exceptions.
- `subject_domain` must be lowercase: `^[a-z][a-z0-9_]*$`
- Update `fact_count` to match the actual length of the `facts` array.
- Write facts incrementally (every 10–15 facts), not all at the end.

### Entity

**Path**: `.magellan/domains/<domain>/entities/<entity_name>.json`

```json
{
  "entity_id": "billing:invoice_generation",
  "name": "Invoice Generation",
  "type": "BusinessProcess",
  "domain": "billing",
  "summary": "Four-state invoice lifecycle (DRAFT → ISSUED → PAID) with a MANUAL_REVIEW bypass for invoices exceeding $10k...",
  "properties": {
    "states": ["DRAFT", "ISSUED", "PAID", "MANUAL_REVIEW"]
  },
  "evidence": [
    {
      "source": "Q3_ops_runbook.pdf",
      "location": "page 12",
      "quote": "Invoices exceeding $10,000 are routed to MANUAL_REVIEW...",
      "confidence": 0.75
    }
  ],
  "tags": ["business_rule"],
  "confidence": 0.85,
  "weight": 0.9,
  "version": {
    "current": "v1",
    "status": "active"
  },
  "related_entities": [
    {
      "entity_id": "billing:manual_review_bypass",
      "relationship": "ENFORCES",
      "direction": "outgoing"
    }
  ],
  "open_questions": ["oq_003"]
}
```

**Required fields**: `entity_id`, `name`, `type`, `domain`, `summary` (min 50 chars),
`evidence` (at least one entry with non-empty quote), `confidence`, `weight`.

**Entity types**: `BusinessProcess`, `BusinessRule`, `Component`, `Service`, `Database`,
`DataEntity`, `Integration`, `Infrastructure`, `Person`, `Team`, `Operational`,
`Constraint`.

**Version status**: `active`, `superseded`, `deprecated`. Never delete entities — mark
as superseded.

**Rules**:
- Each entity is self-contained. A reader with just this one file has everything needed.
- Write entities one at a time, immediately after building. Do not accumulate.
- The `summary` field is the most important — models read it first.

### Relationships (Intra-Domain)

**Path**: `.magellan/domains/<domain>/relationships.json`

```json
{
  "domain": "billing",
  "edges": [
    {
      "edge_id": "e_001",
      "from": "billing:invoice_generation",
      "to": "billing:manual_review_bypass",
      "type": "ENFORCES",
      "properties": {
        "description": "Invoice generation enforces the manual review bypass rule"
      },
      "evidence": {
        "source": "CBBLKBOOK.cblle",
        "location": "lines 142-198"
      },
      "confidence": 0.95,
      "weight": 0.9
    }
  ]
}
```

**Required per edge**: `edge_id`, `from`, `to`, `type`, `properties.description`,
`evidence.source`, `evidence.location`, `confidence`, `weight`.

**Rules**: Write once per domain after all facts in that domain are processed.

### Cross-Domain Relationships

**Path**: `.magellan/cross_domain.json`

```json
{
  "domain": "_cross_domain",
  "edges": [
    {
      "edge_id": "cx_001",
      "from": "billing:vehicle",
      "to": "title:vehicle_title",
      "type": "SAME_AS",
      "confidence": 0.92,
      "properties": {
        "description": "Same vehicle concept across billing and title domains"
      },
      "evidence": {
        "source": "billing/CBBLKBOOK.cblle",
        "location": "line 45"
      }
    }
  ]
}
```

**SAME_AS rules**: Confidence ≥ 0.70 required. Never merge entities — link them.
SAME_AS only between different domains (intra-domain handled by the entity itself).

### Contradiction

**Path (active)**: `.magellan/domains/<domain>/contradictions.json`
**Path (resolved)**: `.magellan/domains/<domain>/resolved/contradictions_resolved.json`

```json
{
  "contradictions": [
    {
      "contradiction_id": "c_001",
      "description": "Threshold mismatch: one source says $10k, another says $15k",
      "domain": "billing",
      "severity": "high",
      "status": "open",
      "related_entities": ["billing:invoice_generation"],
      "sources": [
        { "source": "Q3_ops_runbook.pdf", "quote": "...exceeding $10,000..." },
        { "source": "Policy_v2.docx", "quote": "...exceeding $15,000..." }
      ]
    }
  ]
}
```

**Required**: `contradiction_id`, `description`, `domain`, `status` (`open` or `resolved`).

**Resolved** adds: `resolution_note`, `resolved_at` (ISO 8601 timestamp).

**To add**: Read the existing file, append to the array, write back. If the file
doesn't exist, create it with an empty `contradictions` array first.

### Open Question

**Path (active)**: `.magellan/domains/<domain>/open_questions.json`
**Path (answered)**: `.magellan/domains/<domain>/resolved/questions_answered.json`

```json
{
  "questions": [
    {
      "question_id": "oq_001",
      "question": "Is the $10k threshold still active in the current system?",
      "domain": "billing",
      "priority": "high",
      "status": "open",
      "related_entities": ["billing:invoice_generation"],
      "raised_by": "Ingestion Pass 2",
      "context": "Found conflicting documentation about threshold"
    }
  ]
}
```

**Required**: `question_id`, `question`, `domain`, `status` (`open` or `answered`).

**Answered** adds: `answer_source` (path to material), `answered_at` (ISO 8601).

**Same append pattern** as contradictions: read, append, write back.

### Domain Summary

**Path**: `.magellan/domains/<domain>/summary.json`

```json
{
  "domain": "billing",
  "entity_count": 42,
  "narrative": "The billing domain manages the complete lifecycle of invoice generation...",
  "hub_entities": [
    {
      "entity_id": "billing:invoice_generation",
      "hub_score": 3.85,
      "relationships": 5,
      "summary": "Generates invoices..."
    }
  ],
  "hub_count": 2,
  "contradiction_count": 1,
  "question_count": 2
}
```

**Required**: `domain`, `entity_count`, `narrative` (min 200 chars), `hub_entities`,
`hub_count`.

**Hub detection**: `hub_score = relationship_count × entity_weight`. Exclude entities
with weight < 0.5. Select top 10–15 hubs per domain.

### State

**Path**: `.magellan/state.json`

```json
{
  "initialized_at": "2026-03-15T09:00:00Z",
  "last_ingest": "2026-03-15T10:30:00Z",
  "last_summary_entity_counts": {
    "billing": 42,
    "title": 28
  },
  "pipeline_step": 6
}
```

Tracks pipeline progress. `last_summary_entity_counts` triggers re-summarization
when entity count changes > 10%.

### Index

**Path**: `.magellan/index.json`

```json
{
  "domains": {
    "billing": {
      "entity_count": 42,
      "edge_count": 15,
      "contradiction_count": 2,
      "question_count": 3
    }
  },
  "total_entities": 70,
  "total_edges": 25
}
```

Updated at pipeline end. Provides quick stats without reading all domain files.

### Processed Files Ledger

**Path**: `.magellan/processed_files.json`

```json
{
  "files": {
    "src/billing/CBBLKBOOK.cblle": {
      "disposition": "ingested",
      "domain": "billing",
      "fact_count": 12,
      "processed_at": "2026-03-15T10:30:00Z"
    },
    "docs/corrupted.bin": {
      "disposition": "unreadable",
      "domain": null,
      "fact_count": 0,
      "error": "Binary file, could not read content",
      "processed_at": "2026-03-15T10:31:00Z"
    }
  }
}
```

**Dispositions**: `ingested`, `no_facts`, `unreadable`, `extraction_error`,
`skipped_unchanged`, `skipped_by_rule`.

Every file MUST reach a terminal disposition. Nothing is silently dropped.

### Pipeline Feedback

**Path**: `.magellan/pipeline_feedback.json`

```json
{
  "entries": [
    {
      "step": 3,
      "step_name": "Fact Extraction",
      "reviewed_at": "2026-03-15T10:45:00Z",
      "findings": [
        {
          "severity": "warning",
          "message": "Low fact density for Q3_ops_runbook.pdf (2 facts from 45 pages)"
        }
      ],
      "blocker_count": 0,
      "warning_count": 1,
      "suggestion_count": 0
    }
  ]
}
```

Accumulated during pipeline. Each quality gate appends an entry.

---

## Entity Weight Formula

```
effective_weight = base_weight + corroboration + recency + references
```

Clamp result to [0.0, 1.0].

**Base weights**:

| Source Type | Weight |
|-------------|--------|
| correction | 0.95 |
| production_source_code | 0.90 |
| database_schema | 0.85 |
| official_policy | 0.85 |
| formal_design_document | 0.80 |
| api_specification | 0.80 |
| qa_operational_manual | 0.75 |
| interview_transcript | 0.70 |
| meeting_transcript | 0.50 |
| email_chain | 0.40 |
| informal_notes | 0.30 |

**Modifiers**:
- Corroboration: +0.05 per additional source (cap +0.15)
- Recency: −0.05 for 1–3 year old docs, −0.10 for 3+ years
- References: +0.05 if referenced by 5+ other entities

Weight is metadata for prioritization. It never filters entities out of the graph.

---

## Key Rules

1. **Append-only**: Never delete entities. Mark superseded with `version.status: "superseded"`.
2. **One file per entity**: Prevents merge conflicts and git bloat.
3. **Self-contained entities**: Each entity file has everything needed to understand it.
4. **Source tracing**: Every fact, entity, and edge traces to a source document with a quote.
5. **Nothing silently skipped**: Every file reaches a disposition in the processed files ledger.
6. **Read before write**: When appending to contradictions/questions, read the existing file first.
7. **Domain naming**: Lowercase, letters/digits/underscores: `^[a-z][a-z0-9_]*$`

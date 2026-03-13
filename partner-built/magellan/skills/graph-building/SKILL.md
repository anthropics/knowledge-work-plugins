---
name: graph-building
description: Transform atomic facts into knowledge graph entities and relationships. Use after fact extraction to build the structured KG from raw facts.
---

# Graph Building (Stage 2a)

You transform atomic facts into knowledge graph entities and relationships.

## Critical: Use Built-In Tools for All File Operations

You MUST use Claude's built-in tools for every read and write operation:
- **Read** tool to read facts from `.magellan/domains/<domain>/facts/<source>.json`
- **Glob** tool on `.magellan/domains/<domain>/entities/*.json` to list existing entities
- **Read** tool on `.magellan/domains/<domain>/entities/<name>.json` to read an entity
- **Write** tool to `.magellan/domains/<domain>/entities/<name>.json` for each entity
- **Write** tool to `.magellan/domains/<domain>/relationships.json` for relationships
- **Read + Write** pattern for contradictions and open questions (read existing file, append, write back)

Do NOT create a monolithic `knowledge_graph.json`. The KG is stored as individual entity files.

You receive a set of facts from one source document and produce:

1. Entity files — one self-contained JSON file per entity
2. Relationships — edges connecting entities within the same domain
3. Contradictions — when new facts conflict with existing entities
4. Open questions — when facts are ambiguous or incomplete

## Process

### Critical: Write Incrementally

Do NOT accumulate all entities in your response and write them at the end.
This will hit output token limits on large fact files. Instead, write each
entity immediately after building it.

The pattern is: read a few facts → build one entity → write it → move on.

### Steps

1. Read the facts file using the **Read** tool on `.magellan/domains/<domain>/facts/<source>.json`.
2. List existing entities in the domain using the **Glob** tool on `.magellan/domains/<domain>/entities/*.json`.
3. Process facts in small batches (5-10 facts at a time):
   a. For each fact in the batch, determine:
      - Does this fact describe an existing entity? → Read it with the **Read** tool, update, write it back with the **Write** tool.
      - Does this describe a new entity? → Build it, write it immediately with the **Write** tool.
      - Does this fact establish a relationship? → Add to a running list.
      - Does this fact contradict an existing entity? → Write contradiction immediately (see Contradiction Append Pattern below).
      - Is this fact ambiguous or incomplete? → Write open question immediately (see Open Question Append Pattern below).
   b. Write each entity with the **Write** tool as soon as it's built — do not wait.
   c. Write contradictions and open questions as soon as detected — do not wait.
4. After all facts are processed, write relationships once using the **Write** tool to `.magellan/domains/<domain>/relationships.json`.
5. Briefly report what was created: "N entities, M relationships, K contradictions, J open questions."

### Contradiction Append Pattern

To add a contradiction:
1. **Read** the file `.magellan/domains/<domain>/contradictions.json`.
   - If it does not exist, start with `{"contradictions": []}`.
2. Append the new contradiction object to the `contradictions` array.
3. **Write** the updated JSON back to `.magellan/domains/<domain>/contradictions.json`.

### Open Question Append Pattern

To add an open question:
1. **Read** the file `.magellan/domains/<domain>/open_questions.json`.
   - If it does not exist, start with `{"questions": []}`.
2. Append the new question object to the `questions` array.
3. **Write** the updated JSON back to `.magellan/domains/<domain>/open_questions.json`.

### Why This Matters

A document with 50 facts might produce 20 entities. If you try to build all 20
entities as JSON in your response before writing any of them, you will exceed the
output token limit and produce nothing. By writing each entity immediately via
the Write tool, your response stays small and the work is saved incrementally.

## Entity Types

Assign one of these types to each entity based on the facts:

- `BusinessProcess` — a workflow, procedure, or business operation
- `BusinessRule` — a rule governing decisions or behavior
- `Component` — a software module, program, or library
- `Service` — an API or network-accessible service
- `Database` — a data store (relational, file-based, etc.)
- `DataEntity` — a business data concept (Customer, Invoice, Vehicle)
- `Integration` — a connection between systems
- `Infrastructure` — a hosting environment or platform
- `Person` — a team member or stakeholder mentioned by name
- `Team` — an organizational unit
- `Operational` — a runbook, batch job, or operational procedure
- `Constraint` — a limitation or regulatory requirement

If a fact doesn't fit any type, use `Insight` as a catch-all.

## Entity ID Convention

Entity IDs follow the pattern `<domain>:<snake_case_name>`:

- `billing:invoice_generation`
- `billing:manual_review_bypass`
- `title:vehicle_title_transfer`
- `dealer_management:floor_plan_bank`

When updating an existing entity, keep its ID unchanged. When creating a new entity,
derive the ID from the domain and a clear, descriptive snake_case name.

## Entity Format

Each entity must match this structure exactly:

```json
{
  "entity_id": "billing:invoice_generation",
  "name": "Invoice Generation",
  "type": "BusinessProcess",
  "domain": "billing",
  "summary": "Clear, complete natural language summary of what this entity represents and why it matters. This is the most important field — it's what models read first.",
  "properties": {
    "key": "value pairs specific to this entity type"
  },
  "evidence": [
    {
      "source": "path/to/source/document",
      "location": "page/line/section reference",
      "quote": "Exact quote from the source",
      "confidence": 0.85,
      "extracted_from_fact": "facts/domain/source.json#f_abc123"
    }
  ],
  "tags": ["business_rule", "exception_handling"],
  "confidence": 0.85,
  "weight": 0.9,
  "version": {
    "current": "v1",
    "git_commit": "",
    "ingested_at": "2026-03-15T09:00:00Z",
    "status": "active"
  },
  "related_entities": [
    {"entity_id": "billing:manual_review_bypass", "relationship": "ENFORCES", "direction": "outgoing"}
  ],
  "open_questions": []
}
```

## Writing the Summary

The `summary` field is the most critical. It must:
- Be a complete, standalone description (a model reading only this field understands the entity)
- Include key facts, not just a label
- Mention known constraints, thresholds, or conditions
- Note if the entity is contested (involved in a contradiction)
- Be 2-5 sentences

Bad: "Invoice generation process"
Good: "Four-state invoice lifecycle (DRAFT → ISSUED → PAID) with a MANUAL_REVIEW bypass for invoices exceeding $10,000. The bypass was added in response to a tax audit finding and skips standard approval flow. The $10k threshold is contested — the ops runbook says $10k but a DB config sets it to $5k."

## Updating Existing Entities

When a new fact provides additional evidence for an existing entity:

1. Read the existing entity using the **Read** tool on its file path.
2. Add the new evidence to the `evidence` array.
3. Update the `summary` if the new fact adds significant information.
4. Recalculate weight using the weight formula below (evidence_count = len(evidence)).
5. Add any new `related_entities` references.
6. Write the updated entity using the **Write** tool to the same file path.

Do not overwrite existing evidence — append to it.

## Relationship Types

Use these relationship types for edges:

| Type | Meaning |
|------|---------|
| `DEPENDS_ON` | A requires B to function |
| `CALLS` | A invokes B (API call, function call, program call) |
| `READS_FROM` | A reads data from B |
| `WRITES_TO` | A writes data to B |
| `INTEGRATES_WITH` | System-level integration |
| `ENFORCES` | A enforces business rule B |
| `CONTAINS` | A contains B (database contains table, system contains component) |
| `TRIGGERS` | A causes B to execute |
| `PRODUCES` | A creates/outputs B |
| `CONSUMES` | A uses/inputs B |
| `PART_OF` | A is a component of B |
| `SUCCEEDED_BY` | A is replaced by B |

## Relationship Format

Each relationship in `relationships.json`:

```json
{
  "edge_id": "e_<unique_id>",
  "from": "billing:invoice_generation",
  "to": "billing:manual_review_bypass",
  "type": "ENFORCES",
  "properties": {
    "description": "Invoice generation enforces the manual review bypass rule for amounts over $10k",
    "criticality": "high"
  },
  "evidence": {
    "source": "CBBLKBOOK.cblle",
    "location": "lines 142-198",
    "quote": "IF WS-INV-AMT > 10000 PERFORM 3200-MANUAL-REVIEW"
  },
  "confidence": 0.95,
  "weight": 0.9
}
```

Every relationship must have a `description` explaining WHY the relationship exists.

## Weight Calculation

Calculate the weight for each entity directly using this formula:

```
effective_weight = base_weight + corroboration + recency + references
```

Clamp the result to **[0.0, 1.0]**.

### Base Weight Table

Look up the base weight from the source type (passed through from ingestion):

| Source Type | Base Weight |
|-------------|-------------|
| `correction` | 0.95 |
| `production_source_code` | 0.90 |
| `database_schema` | 0.85 |
| `official_policy` | 0.85 |
| `formal_design_document` | 0.80 |
| `api_specification` | 0.80 |
| `qa_operational_manual` | 0.75 |
| `interview_transcript` | 0.70 |
| `meeting_transcript` | 0.50 |
| `email_chain` | 0.40 |
| `informal_notes` | 0.30 |

If the source type is not listed, use **0.50** as the default base weight.

### Modifiers

- **Corroboration**: +0.05 per additional source beyond the first (cap at +0.15).
  - 1 source: +0.00, 2 sources: +0.05, 3 sources: +0.10, 4+ sources: +0.15
- **Recency**: based on the age of the source document (if known).
  - Less than 1 year old: +0.00
  - 1–3 years old: −0.05
  - More than 3 years old: −0.10
- **References**: +0.05 if referenced by 5 or more other entities (0 for new entities).

### Example Calculation

An entity from `production_source_code` with 3 evidence entries, document less than 1 year old, and 0 references from other entities:
- base_weight = 0.90
- corroboration = +0.10 (3 sources → 2 additional sources × 0.05)
- recency = 0.00 (less than 1 year)
- references = 0.00 (fewer than 5 references)
- effective_weight = clamp(0.90 + 0.10 + 0.00 + 0.00) = **1.00**

Weight is metadata for prioritization. It never filters entities out of the graph.

## What You Do NOT Do

- Do not invent facts. Every claim must come from the atomic facts you received.
- Do not assign relationships between entities that aren't evidenced in the facts.
- Do not skip facts. Every fact must contribute to at least one entity or relationship.
- Do not merge entities across domains. Cross-domain linking (SAME_AS) is handled in Stage 2b.

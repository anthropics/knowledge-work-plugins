---
name: cross-domain-linking
description: Detect SAME_AS entities and cross-domain relationships across the knowledge graph. Use after graph building (Stage 2a) to link entities that represent the same concept in different domains.
---

# Cross-Domain Linking (Stage 2b)

## Critical: Use Built-in Tools for All Operations

You MUST use Claude's built-in tools for reading and writing:
- Glob on `.magellan/domains/*/` to discover domains
- Glob on `.magellan/domains/<domain>/entities/*.json` to discover entities
- Read tool on entity files to read entity details
- Read/Write tools on `.magellan/cross_domain.json` for cross-domain edges
- Read/Write tools on `.magellan/domains/<domain>/contradictions.json` for contradictions
- Read/Write tools on `.magellan/domains/<domain>/open_questions.json` for open questions

Do NOT skip this step.

You scan all domains in the knowledge graph to detect:

1. SAME_AS entities — the same concept appearing in different domains
2. Cross-domain relationships — edges connecting entities across domains
3. Cross-document contradictions — facts in one domain that conflict with another

## Process

1. Get the inventory first — never load the entire graph into context.
   a. Use Glob on `.magellan/domains/*/` to discover all domains (each subdirectory name is a domain).
   b. For each domain, use Glob on `.magellan/domains/<domain>/entities/*.json` to get entity file paths.
   c. For each entity, use the Read tool on the entity file to get its name, type, domain, and summary.
   d. Build a lightweight inventory: `[{entity_id, name, type, domain, summary_snippet}]`

2. Compare entities across domains for SAME_AS candidates.
   Two entities are SAME_AS candidates when:
   - They have similar names (e.g., "Vehicle Title" in billing and "Title Record" in title)
   - They describe the same real-world concept from different perspectives
   - They reference the same external system, database, or data entity

   Do NOT create SAME_AS edges for:
   - Generic entities that happen to share a name (e.g., "Config" in two domains)
   - Entities that are clearly different things with similar names
   - Entities within the same domain (intra-domain linking is handled in Stage 2a)

3. For each SAME_AS candidate pair, read the full entities to confirm.
   Only create the edge if the entities genuinely represent the same concept.

4. Detect cross-domain relationships.
   When one domain's entity references another domain's entity (e.g., billing's
   settlement process triggers title's transfer event), create a cross-domain edge.

5. Detect cross-document contradictions.
   When entities in different domains make conflicting claims about the same system
   behavior, create a contradiction. Read `.magellan/domains/<domain>/contradictions.json`
   using the Read tool, append the new contradiction to the `active` array, and write
   it back using the Write tool. If the file does not exist yet, start with
   `{"active": [], "resolved": []}`.

6. Write results.
   - Read existing `.magellan/cross_domain.json` using the Read tool.
     If the file does not exist yet, start with `{"edges": []}`.
   - Append new edges to the `edges` array (don't overwrite existing ones).
   - Write the updated file back using the Write tool.

## Weight Calculation

When assigning weights to cross-domain edges, calculate directly using this formula:

```
effective_weight = clamp(base_weight + modifiers, 0.0, 1.0)
```

Base weights by source type:
- production_source_code: 0.95
- database_schema: 0.90
- api_spec: 0.85
- config_file: 0.80
- official_documentation: 0.70
- meeting_transcript: 0.50
- email_thread: 0.40
- informal_notes: 0.30

Modifiers:
- Corroboration: +0.05 per additional independent source (max +0.15)
- Recency: +0.05 if document is less than 6 months old
- Reference count: +0.02 per entity referencing this one (max +0.10)

Clamp the final value to the range [0.0, 1.0].

## SAME_AS Edge Format

Every cross-domain edge MUST include evidence tracing it back to source facts.
Cross-domain edges without evidence are untraceable and untrustworthy.

```json
{
  "edge_id": "cx_<unique_id>",
  "from": "billing:vehicle_record",
  "to": "title:vehicle_title",
  "type": "SAME_AS",
  "properties": {
    "description": "Same vehicle entity referenced in both billing and title domains"
  },
  "evidence": {
    "from_entity_source": "billing:vehicle_record evidence from Dealer Master Manual p.12",
    "to_entity_source": "title:vehicle_title evidence from Title Inventory Report p.3",
    "linking_rationale": "Both entities reference VIN-keyed vehicle records with overlapping fields (VIN, year, make, model)"
  },
  "confidence": 0.92,
  "weight": 0.85
}
```

## Cross-Domain Relationship Format

Same as intra-domain relationships but the `from` and `to` span different domains:

```json
{
  "edge_id": "cx_<unique_id>",
  "from": "billing:settlement_service",
  "to": "title:title_transfer_event",
  "type": "TRIGGERS",
  "properties": {
    "description": "Settlement completion triggers title transfer to buyer",
    "trigger": "settlement finalized"
  },
  "evidence": {
    "source": "Architecture overview.pdf",
    "location": "page 8",
    "quote": "Title transfer is initiated upon settlement confirmation."
  },
  "confidence": 0.75,
  "weight": 0.80
}
```

## Cross-Domain Relationship Types

In addition to the standard relationship types (DEPENDS_ON, CALLS, etc.), these
are common across domains:

| Type | Meaning |
|------|---------|
| `SAME_AS` | Same real-world concept in different domains |
| `TRIGGERS` | Action in domain A causes action in domain B |
| `SHARES_DATA_WITH` | Two domains exchange data |
| `DEPENDS_ON` | Domain A requires domain B to function |
| `INTEGRATES_WITH` | System-level integration across domains |

## Confidence for SAME_AS

- 0.95+: Entities have the same name, same type, and overlapping evidence
- 0.85-0.94: Strong name similarity and matching descriptions
- 0.70-0.84: Related concepts that likely represent the same thing
- Below 0.70: Do not create a SAME_AS edge. If unsure, raise an open question instead.

## Scale Awareness

For large graphs with hundreds of entities across many domains, be strategic:
- Start with entity names — look for obvious matches first
- Group by entity type — compare Components with Components, not Components with Rules
- Use summary snippets for quick comparison before loading full entities
- Skip domains with no plausible overlap (e.g., infrastructure vs. security)

Do NOT try to compare every entity with every other entity. Use the inventory
to identify candidates efficiently.

## What You Do NOT Do

- Do not create SAME_AS edges within the same domain.
- Do not merge entities. SAME_AS preserves both entities independently.
- Do not create ANY edge without an `evidence` field. Every cross-domain link
  must cite the source entities and explain why the link exists. Edges without
  evidence are the #1 quality issue found in production runs.
- Do not overwrite existing cross-domain edges. Append to them.

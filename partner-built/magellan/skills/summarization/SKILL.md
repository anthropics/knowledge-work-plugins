---
name: summarization
description: Synthesize domain narratives from knowledge graph entities. Identifies hub entities and produces summary.json per domain. Use after graph building to create readable overviews.
---

# Domain Summarization (Stage 2c)

## Critical: Use Built-in Tools for All Operations

You MUST use Claude's built-in tools for reading and writing:
- Glob on `.magellan/domains/*/` to discover domains
- Glob on `.magellan/domains/<domain>/entities/*.json` to discover entities
- Read tool on entity files to read entity details
- Read tool on `.magellan/domains/<domain>/relationships.json` for edge counts (hub detection)
- Read tool on `.magellan/domains/<domain>/open_questions.json` and `.magellan/domains/<domain>/contradictions.json` for counts
- Read tool on `.magellan/domains/<domain>/summary.json` to check existing summaries
- Write tool to `.magellan/domains/<domain>/summary.json` for each domain's summary
- Read/Write tools on `.magellan/state.json` to update state with summary entity counts

Do NOT compress summaries into index.json.
Each domain MUST get its own `summary.json` written via the Write tool.

You produce a master narrative for each domain by identifying hub entities and
synthesizing a coherent summary. This bridges the gap between hundreds of individual
entity files and the high-level understanding a model or architect needs.

## When to Run

- After Stage 2b (cross-domain linking) when a domain's entity count has changed by
  more than 10% since the last summary
- Before Phase 2 (design generation) for all domains
- On demand when an architect requests regeneration

## Process

1. Read `.magellan/state.json` using the Read tool to get `last_summary_entity_counts`.

2. For each domain (discovered via Glob on `.magellan/domains/*/`):
   a. Count current entities using Glob on `.magellan/domains/<domain>/entities/*.json`.
   b. Compare against `last_summary_entity_counts[domain]` from state.json.
   c. If the count changed by more than 10% or no summary exists, regenerate.

3. For domains that need regeneration:
   a. Read all entity files and relationships for the domain using the Read tool.
   b. Calculate hub scores.
   c. Read the top hub entities in detail.
   d. Synthesize the domain narrative.
   e. Write `summary.json` to `.magellan/domains/<domain>/summary.json` using the Write tool.
   f. Update `.magellan/state.json` with current entity count for the domain using
      the Read tool (to get current state) then the Write tool (to save updated state).

## Hub Detection

Hub entities are the most important concepts in a domain — the ones everything else
clusters around. Identify them using:

```
hub_score = relationship_count * entity_weight
```

Where `relationship_count` is the total inbound + outbound edges for the entity,
and `entity_weight` is the weight field on the entity.

Exclusion rule: entities with weight below 0.5 are excluded from hub candidacy
entirely. They are infrastructure or utility concepts, not business hubs.

Example:
- `Invoice_Generation` (weight 0.9, 43 connections) -> hub_score = 38.7 -> hub
- `DateFormatter` (weight 0.3, 200 connections) -> excluded (weight < 0.5)

Select the top 10-15 hub entities per domain.

## Narrative Writing

The `narrative` field in `summary.json` is the most important output. It must:

- Explain the domain in plain language, as if briefing an architect who has never
  seen this system
- Start with the core business process (what does this domain DO)
- Describe the key entities and how they relate
- Mention known risks, contradictions, and contested entities
- Reference open questions that affect this domain
- Be 3-8 paragraphs — long enough to be useful, short enough to fit in a context window

Structure the narrative:
1. Overview: what this domain is responsible for
2. Core processes: the main workflows and how they operate
3. Key entities: the hubs and what they do
4. Integrations: how this domain connects to other domains
5. Risks and open items: contradictions, open questions, contested facts

## summary.json Format

```json
{
  "domain": "billing",
  "generated_at": "2026-03-20T10:00:00Z",
  "entity_count": 487,
  "hub_entities": 12,
  "narrative": "The billing domain centers on Invoice Generation, a four-state lifecycle...",
  "hub_summaries": [
    {
      "entity_id": "billing:invoice_generation",
      "name": "Invoice Generation",
      "hub_score": 38.7,
      "connected_entities": 43,
      "summary": "Core billing process. Four states with a MANUAL_REVIEW exception...",
      "open_questions": 2,
      "contradictions": 1
    }
  ],
  "open_question_count": 8,
  "contradiction_count": 3,
  "cross_domain_connections": ["title", "transportation"]
}
```

## Cross-Domain Connections

Read `.magellan/cross_domain.json` using the Read tool for edges involving entities
in this domain. List the other domains this domain connects to in the
`cross_domain_connections` field. Mention these connections in the narrative.

## Open Questions and Contradictions

Read `.magellan/domains/<domain>/open_questions.json` and
`.magellan/domains/<domain>/contradictions.json` using the Read tool. Count how many
relate to this domain. Include the counts in the summary and mention the most critical
ones in the narrative.

## Updating State

After writing each domain's summary, update `.magellan/state.json`:

1. Read `.magellan/state.json` using the Read tool.
2. Update `last_summary_entity_counts[domain]` to the current entity count.
3. Write the updated state back using the Write tool.

This enables the 10% change threshold check on the next run.

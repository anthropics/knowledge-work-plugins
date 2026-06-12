---
name: contradiction-detection
description: Detect contradictions between facts and existing KG entities, and raise open questions for ambiguous or incomplete information. Use during graph building (Stage 2a) and cross-domain linking (Stage 2b).
---

# Contradiction Detection

You detect two types of issues during graph building:

1. Contradictions — when new facts conflict with existing entities
2. Open questions — when facts are ambiguous, incomplete, or reference undocumented behavior

These are the most valuable outputs of the system. The faster they are surfaced,
the faster the team builds a complete and trustworthy picture.

## Detecting Contradictions

A contradiction exists when:

- A new fact states a different value for the same property of an existing entity
  (e.g., threshold is $10k in one source, $5k in another)
- A new fact describes behavior that conflicts with documented behavior
  (e.g., "batch runs nightly" vs. "batch runs weekly")
- A new fact says something was removed or deprecated that another source says is active

When you detect a contradiction, record it by reading the existing contradictions file
for the domain, appending the new entry, and writing it back:

1. Read `.magellan/domains/<domain>/contradictions.json` using the Read tool.
   If the file does not exist yet, start with `{"active": [], "resolved": []}`.
2. Append the new contradiction to the `active` array.
3. Write the updated file back using the Write tool.

The contradiction object format:

```json
{
  "contradiction_id": "c_<unique_id>",
  "description": "Clear, human-readable description of the conflict",
  "domain": "billing",
  "sources": [
    {
      "document": "Q3_ops_runbook.pdf",
      "claim": "Invoices exceeding $10,000 are routed to MANUAL_REVIEW",
      "location": "page 12",
      "confidence": 0.75
    },
    {
      "document": "billing_db_config.sql",
      "claim": "MANUAL_REVIEW_THRESHOLD = 5000",
      "location": "line 47",
      "confidence": 0.90
    }
  ],
  "related_entities": ["billing:manual_review_bypass"],
  "severity": "high",
  "status": "open",
  "detected_at": "<current ISO 8601 timestamp>"
}
```

## Severity Levels

- `critical` — contradicts a HARD business rule or compliance requirement
- `high` — contradicts a core system behavior or significant threshold
- `medium` — contradicts operational detail or non-critical configuration
- `low` — minor discrepancy in descriptive or contextual information

## Raising Open Questions

An open question should be raised when:

- A fact references undocumented behavior ("the system does X but no documentation explains why")
- A fact mentions a system, process, or rule that no other source corroborates
- A fact is ambiguous and could be interpreted multiple ways
- A code path exists but its purpose is unclear
- A business rule is implemented but no policy document defines it

Record the open question by reading the existing open questions file for the domain,
appending the new entry, and writing it back:

1. Read `.magellan/domains/<domain>/open_questions.json` using the Read tool.
   If the file does not exist yet, start with `{"active": [], "resolved": []}`.
2. Append the new question to the `active` array.
3. Write the updated file back using the Write tool.

The open question object format:

```json
{
  "question_id": "oq_<unique_id>",
  "question": "Clear question that a client SME could answer",
  "context": "Why this question matters and what evidence prompted it",
  "domain": "billing",
  "related_entities": ["billing:invoice_generation", "billing:manual_review_bypass"],
  "directed_to": "senior_developer",
  "priority": "high",
  "status": "open",
  "raised_at": "<current ISO 8601 timestamp>",
  "raised_by": "ingestion of <source document>"
}
```

## Who Should Answer (directed_to)

- `senior_developer` — questions about code behavior, undocumented logic
- `dba` — questions about database schemas, data relationships, configs
- `business_analyst` — questions about business rules, domain logic
- `operations` — questions about batch jobs, monitoring, runbooks
- `finance_ops` — questions about financial rules, thresholds, compliance
- `security` — questions about access control, encryption, audit
- `management` — questions about organizational structure, ownership

## Priority

- `critical` — blocks understanding of a core business process
- `high` — significant gap that affects design decisions
- `medium` — useful context but not blocking
- `low` — nice to know, can be deferred

## When Contradictions Affect Existing Entities

When you create a contradiction, also update the affected entity:
1. Read the entity file at `.magellan/domains/<domain>/entities/<entity_id>.json` using the Read tool.
2. Add a `contested: true` property to flag it.
3. Update the summary to mention the contradiction.
4. Write the entity back to the same path using the Write tool.

This ensures that any model reading the entity sees the dispute immediately
rather than having to check contradictions.json separately.

## What You Do NOT Do

- Do not resolve contradictions yourself. Surface them for the team.
- Do not lower an entity's weight because of a contradiction. Set `contested: true` instead.
- Do not create contradictions for minor wording differences that don't change meaning.
- Do not create open questions for things that are clearly explained in other documents
  you haven't processed yet — those will be resolved when those documents are ingested.

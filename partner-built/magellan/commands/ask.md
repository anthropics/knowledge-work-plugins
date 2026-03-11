---
description: Query the Magellan knowledge graph using natural language
---

# Ask the Knowledge Graph

Answer questions about the target systems using the knowledge graph.

## Usage

```
/magellan:ask <question>
```

## Behavior

1. Locate the `.magellan/` directory in the workspace. If it doesn't exist, inform
   the user that no knowledge graph has been built yet and suggest running
   `/magellan:add` to ingest materials first.

2. Read `.magellan/index.json` to understand the current KG scope (domains, entity
   counts).

3. Apply the querying skill to answer the question. The skill determines the right
   approach based on question type:
   - Overview questions → read domain summaries via Read tool
   - Factual lookups → read specific entity files via Read tool
   - Structural/dependency questions → read relationships.json and cross_domain.json,
     traverse edges manually by following entity references
   - Cross-domain questions → read cross_domain.json + follow edges
   - Open questions/contradictions → read the per-domain JSON files

4. Present the answer with:
   - Direct response to the question
   - Source citations for every factual claim (entity ID, document, location, confidence)
   - Any relevant contradictions or open questions
   - Low-confidence facts flagged explicitly

## Examples

```
/magellan:ask How does the billing system process invoices?
/magellan:ask What systems depend on the AS/400 batch job?
/magellan:ask What are the known contradictions in the title domain?
/magellan:ask List all components that handle PII data
/magellan:ask What open questions do we have for the client?
```

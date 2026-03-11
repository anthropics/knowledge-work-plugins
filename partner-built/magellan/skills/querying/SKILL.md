---
name: querying
description: Answer questions about the knowledge graph using a combination of direct entity reads, domain summaries, and graph traversal. Use when responding to /magellan:ask queries.
---

# Querying the Knowledge Graph

You answer questions about the client's systems using the knowledge graph. Every
answer must include source citations. You never invent information — if the KG
doesn't have the answer, say so and identify it as an open question.

## Query Strategy

Choose your approach based on the question type:

### Semantic / Overview Questions
"How does billing work?" "What do we know about the title transfer process?"

1. Read the domain summary file at `.magellan/domains/<domain>/summary.json` using
   the Read tool.
2. If the summary answers the question, respond with it + citations.
3. If more detail is needed, read specific entity files for the relevant hubs
   (paths are in the summary's hub list).

### Factual / Lookup Questions
"What is the MANUAL_REVIEW threshold?" "What language is CBBLKBOOK written in?"

1. Identify the likely domain and entity from the question.
2. Use Glob on `.magellan/domains/<domain>/entities/*.json` to find matching
   entity IDs. If you don't know the domain, Glob across all domains:
   `.magellan/domains/*/entities/*.json`.
3. Read the matching entity file using the Read tool.
4. Answer with the specific fact + source citation.

### Structural / Dependency Questions
"What systems does billing depend on?"
"What would break if we decommission the AS/400 batch job?"
"List all components downstream of payment that touch PII data."

1. These require graph traversal — do NOT try to answer from entity files alone.
2. Perform manual graph traversal by reading relationship and cross-domain files,
   then following edges hop-by-hop. See the "Manual Graph Traversal" section below
   for the detailed procedure for each operation type:
   - "depends on" / "connects to" → **walk** (follow outgoing edges)
   - "what depends on" / "affected by" → **impact** (follow incoming edges)
   - "how are X and Y connected" → **between** (BFS from start to end)
   - "which entities have property X" → **filter** (walk + check entity properties)
3. Present the results with the full traversal path.

### Cross-Domain Questions
"How does billing interact with the title system?"
"What data flows between transportation and auction operations?"

1. Read `.magellan/cross_domain.json` using the Read tool to get cross-domain
   edges (SAME_AS links and inter-domain relationships).
2. Perform a manual graph walk starting from the relevant entity to find
   cross-domain paths (see "Manual Graph Traversal" below).
3. Read summaries for both domains for context.

### Cross-Domain Workflow / Saga Questions
"Trace the sale-to-settlement workflow across all domains."
"What happens end-to-end when a vehicle is sold?"
"Show the complete flow from check-in to title transfer with compensation actions."

1. Identify the start and end entities from the question. If the user specifies
   both endpoints, use the **between** traversal to find all paths. If only a
   start is given, use **walk** (outgoing) to trace the full chain.
2. Read `.magellan/cross_domain.json` using the Read tool to understand domain
   boundaries.
3. For each step in the traversal path, read the entity to get its domain,
   type, and summary.
4. Present the results as an **ordered step sequence** with:
   - Step number and domain swimlane
   - Entity name and what happens at this step
   - Domain event that triggers the next step (from relationship edge descriptions)
   - Which domain owns each step
5. Include a **Mermaid sequence diagram** showing the temporal flow across
   domain swimlanes:

```mermaid
sequenceDiagram
    participant SAL as Sales & Auction
    participant FIN as Financial Mgmt
    participant TIT as Title Docs

    SAL->>FIN: SaleCompleted event
    activate FIN
    FIN->>FIN: Calculate fees, generate invoice
    FIN-->>SAL: InvoiceCreated event
    deactivate FIN

    SAL->>TIT: InitiateTitleTransfer
    activate TIT
    alt Title clear
        TIT-->>SAL: TitleTransferApproved
    else Title issue
        TIT-->>SAL: TitleHold raised
        SAL->>FIN: Initiate fee reversal (compensation)
    end
    deactivate TIT
```

6. If the question asks about compensation actions or failure modes, add `alt`
   blocks for each step that can fail, showing the compensation path.
7. If the question asks about SLAs or timeouts, add `Note over` annotations
   where timing constraints are known from the KG.

### Open Questions and Contradictions
"What don't we know about billing?"
"What contradictions have been found?"

1. For domain-specific queries, read the file directly:
   - Open questions: Read `.magellan/domains/<domain>/open_questions.json`
   - Contradictions: Read `.magellan/domains/<domain>/contradictions.json`
2. For cross-domain queries (e.g., "What contradictions have been found?"),
   use Glob to find all files across domains, then read each:
   - Open questions: Glob `.magellan/domains/*/open_questions.json`, then Read each
   - Contradictions: Glob `.magellan/domains/*/contradictions.json`, then Read each
3. Present organized by priority/severity.

---

## Manual Graph Traversal

Since there is no dedicated graph walk tool, you traverse the knowledge graph
manually by reading relationship files and following edges hop-by-hop. This
section describes the procedure for each traversal operation.

### Data Files

- **Intra-domain edges**: `.magellan/domains/<domain>/relationships.json`
  Each file contains `{ "domain": "<name>", "edges": [...] }` where each edge has:
  `edge_id`, `from`, `to`, `type`, `properties.description`, `evidence`, `confidence`.
  Entity IDs are prefixed with their domain (e.g., `billing:invoice_generation`).

- **Cross-domain edges**: `.magellan/cross_domain.json`
  Contains SAME_AS links and inter-domain relationship edges. Same edge structure
  but `from` and `to` span different domain prefixes.

### Walk (Outgoing Traversal)

Use for: "What does X depend on?", "What does X connect to?"

1. Identify the start entity (e.g., `billing:invoice_generation`).
2. Extract the domain from the entity ID prefix (e.g., `billing`).
3. Read `.magellan/domains/billing/relationships.json`.
4. Also read `.magellan/cross_domain.json`.
5. Find all edges where `from` equals the start entity. Collect the `to` entities.
6. For each `to` entity found, read its entity file for context if needed.
7. To continue deeper (multi-hop), repeat steps 2-6 for each discovered entity,
   up to a maximum depth of 8 hops.
8. Track visited entities to avoid infinite cycles — never revisit an entity
   you have already expanded.
9. Present the full traversal path showing each hop and the edge type/description.

### Impact (Incoming / Reverse Traversal)

Use for: "What depends on X?", "What would break if we changed X?"

1. Identify the start entity.
2. Read relationships.json for all domains (Glob `.magellan/domains/*/relationships.json`,
   then Read each).
3. Also read `.magellan/cross_domain.json`.
4. Find all edges where `to` equals the start entity. Collect the `from` entities —
   these are the entities that depend on the start entity.
5. To continue deeper, repeat: for each discovered `from` entity, find edges where
   `to` equals that entity.
6. Track visited entities to avoid cycles. Maximum depth: 8 hops.
7. Present results showing the reverse dependency chain.

### Between (Path Finding)

Use for: "How are X and Y connected?", "Trace the path from X to Y."

1. Identify the start entity and end entity.
2. Read relationships.json for all relevant domains + cross_domain.json.
3. Build an adjacency picture by scanning all edges.
4. Perform a breadth-first search (BFS) from the start entity:
   - Maintain a queue of `(current_entity, path_so_far)` tuples.
   - At each step, find all edges where `from` equals the current entity.
     Add each `to` entity to the queue (if not already visited) with the
     extended path.
   - If the current entity equals the end entity, record the path as a result.
5. Stop after finding up to 20 paths, or after reaching depth 8, whichever
   comes first. Prefer shortest paths.
6. For each path found, read the entities along the way for context.
7. Present each path as a chain: `A -[EDGE_TYPE]-> B -[EDGE_TYPE]-> C`.

### Filter (Walk + Property Filter)

Use for: "Which entities have property X?", "Find all BusinessRule entities downstream of Y."

1. Perform a **walk** (outgoing) from the start entity as described above.
2. At each hop, read the discovered entity file.
3. Check if the entity's properties match the filter criteria (e.g.,
   `entity_type == "BusinessRule"`, or `properties.handles_pii == true`).
4. Collect only the entities that pass the filter.
5. Present the filtered results with their traversal paths.

### Traversal Guardrails

- **Start small**: Read the start entity first to confirm it exists and get its domain.
- **Hard depth limit**: Stop at 5 hops. Do not increase this — deeper traversals
  consume too much context and produce unreliable results.
- **Cycle detection**: Maintain a `visited` set of entity IDs. Before expanding any
  entity, check if it's already in `visited`. If so, skip it. This is mandatory —
  without it, cycles cause infinite loops.
- **Cross-domain awareness**: Always read cross_domain.json. An entity in billing
  may have edges to the title domain only visible there.
- **Edge direction matters**: `from` is the source, `to` is the target.
- **Graph size check**: Before traversing, count total entities via Glob. If the
  graph has more than 200 entities, tell the user:
  "This is a large knowledge graph (N entities). Traversal results may be
  incomplete. For comprehensive structural queries on large graphs, consider
  using the production version with the graph walk tool."
  Then proceed with best effort — this is a warning, not a stop.
- **Honest incompleteness**: If you hit the depth limit or visited-set limit before
  finding an answer, say so: "Traversal reached depth limit without finding a
  connection. The relationship may exist at a deeper level or through an indirect
  path not explored." Never fabricate a path you didn't actually traverse.

---

## Answer Format

Every answer must include:

1. The direct answer to the question
2. Source citations for every factual claim:
   - Entity ID that contains the fact
   - Original source document and location
   - Confidence level
3. Any caveats:
   - Low-confidence facts (weight < 0.5): flag explicitly
   - Contested facts: mention the contradiction
   - Open questions: mention what we don't know

## Example Answer

Question: "How does invoice processing work?"

> Invoice processing in the billing domain follows a four-state lifecycle:
> DRAFT → ISSUED → PAID, with a MANUAL_REVIEW bypass for invoices exceeding
> $10,000.
>
> The MANUAL_REVIEW threshold is contested — the Q3 ops runbook states $10,000
> (source: Q3_ops_runbook.pdf, page 12, confidence: 0.75) but a database
> config sets it to $5,000 (source: billing_db_config.sql, line 47,
> confidence: 0.90). See contradiction c_001.
>
> The settlement process triggers after an invoice reaches PAID status,
> which in turn initiates title transfer in the title domain.
> (source: billing:settlement_service, evidence from Architecture overview.pdf)
>
> Open question: Is the $10k threshold still active? (oq_003, directed to
> senior_developer, priority: high)

## What You Do NOT Do

- Do not invent facts. If the KG doesn't have the information, say "The knowledge
  graph does not contain information about [topic]. This should be raised as an
  open question."
- Do not guess at relationships. Use the manual graph traversal procedure for
  structural questions.
- Do not omit source citations. Every factual claim needs provenance.
- Do not present low-weight entities (< 0.5) as established facts. Qualify them
  as "low-confidence" or "from informal sources."
- Do not hide contradictions. Always surface them when relevant to the question.

## When the KG is Empty or Sparse

If the workspace has few or no entities:
- Say so clearly: "The knowledge graph has N entities across M domains."
- Suggest what materials should be ingested to answer the question.
- Offer to help add materials using `/magellan:add`.

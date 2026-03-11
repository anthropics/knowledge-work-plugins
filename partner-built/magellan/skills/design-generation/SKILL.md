---
name: design-generation
description: Generate business rules, DDD specs, and implementation contracts from the knowledge graph. Phase 2 capability — use when the team is ready to move from discovery to design.
---

# Design Generation (Phase 2)

You generate the deliverables that implementation teams need to build the new system.
You work from the knowledge graph — domain summaries, entities, relationships,
contradictions, and open questions.

The goal is a greenfield design based on requirements extracted from the current
system analysis — not a strangler fig migration. AI-accelerated development means
building new is fast enough that the old architecture doesn't need to be preserved.

## Critical: Use Built-in Tools for Reading

You MUST use Claude's built-in tools to read the KG:
- **Discover domains**: Glob on `.magellan/domains/*/`
- **Discover entities**: Glob on `.magellan/domains/<domain>/entities/*.json`
- **Read entity details**: Read tool on `.magellan/domains/<domain>/entities/<entity_id>.json`
- **Read domain summaries**: Read tool on `.magellan/domains/<domain>/summary.json`
- **Read relationships**: Read tool on `.magellan/domains/<domain>/relationships.json`
- **Read cross-domain edges**: Read tool on `.magellan/cross_domain.json`
- **Read contradictions**: Read tool on `.magellan/domains/<domain>/contradictions.json`
- **Read open questions**: Read tool on `.magellan/domains/<domain>/open_questions.json`

Do NOT invent or assume system details. Every claim in a deliverable must trace
to a KG entity with evidence.

## Process — One Domain at a Time

Process each domain independently to avoid output limits. For each domain:

1. Read the domain summary using the Read tool on `.magellan/domains/<domain>/summary.json`.
2. Use Glob on `.magellan/domains/<domain>/entities/*.json` to discover entities,
   then Read the key entities (hubs first, then others).
3. Read `.magellan/domains/<domain>/relationships.json` using the Read tool.
4. Read `.magellan/cross_domain.json` using the Read tool for inter-domain connections.
5. Read `.magellan/domains/<domain>/contradictions.json` and
   `.magellan/domains/<domain>/open_questions.json` using the Read tool to get
   this domain's entries only.
6. Generate the four deliverables (described below), writing each file
   immediately after generating it — do NOT accumulate all four in one response.

## Deliverables (Per Domain)

All outputs go to `.magellan/domains/<domain>/deliverables/`.

### 1. business_rules.md

Extract and formalize all business rules from the KG entities. The output has
two sections: a cross-domain summary table, then per-classification rule tables.

#### Cross-Domain Summary

Start with a summary showing the distribution across all domains (when processing
the first domain) or this domain's distribution:

```markdown
# Business Rules: Billing Domain

## Summary

| Classification | Count | Description |
|----------------|------:|-------------|
| HARD           |     8 | Legal, regulatory, compliance — must preserve |
| SOFT           |    12 | Business policy — can be revisited |
| QUESTIONABLE   |     5 | Likely tech debt — challenge actively |
| **Total**      |**25** | |

Rules without source citations: 2 (flagged below)
```

#### Per-Classification Rule Tables

For each classification (HARD, SOFT, QUESTIONABLE), generate a structured table.
Model each rule as a condition/action pair where possible:

```markdown
## HARD Rules (Legal/Regulatory — must preserve)

| ID | Rule | Condition | Action | Source Entity | Source Document | Confidence |
|----|------|-----------|--------|---------------|-----------------|------------|
| BR-001 | Invoice manual review threshold | `invoice_amount > $10,000` | Route to MANUAL_REVIEW queue | `billing:manual_review_bypass` | CBBLKBOOK.cblle:142 | 0.95 |
| BR-002 | Title lien check required | `title_transfer = true` | Verify no outstanding liens with DMV | `title:lien_verification` | Title_Process_Manual.pdf p.8 | 0.90 |

### Evidence

**BR-001** — "Invoices exceeding $10,000 are routed to MANUAL_REVIEW, skipping
standard approval." (CBBLKBOOK.cblle, lines 142-198)

**BR-002** — "All title transfers must include a lien check with the state DMV
before release." (Title_Process_Manual.pdf, page 8, section 3.2)
```

Repeat for SOFT and QUESTIONABLE classifications.

#### Rules Without Source Citations

At the end, list any rules that lack direct source citations:

```markdown
## Rules Without Source Citations

| ID | Rule | Why No Citation |
|----|------|-----------------|
| BR-015 | Late payment penalty rate | Inferred from multiple entities, no single source quote |
```

#### Classification Criteria

- **HARD**: legal, regulatory, compliance, contractual obligation
- **SOFT**: business policy that could be changed if the business decides to
- **QUESTIONABLE**: likely a workaround, technical limitation, or outdated constraint

Every rule MUST cite its source entity ID and original document. Rules that
cannot be traced to a specific source quote are flagged in the "Rules Without
Source Citations" section rather than silently omitted.

Group rules by subdomain or business process within each classification when
a domain has more than 10 rules of the same type.

### 2. ddd_spec.md

Bounded context specification:

- Context name and responsibility
- Entities and value objects
- Aggregates and aggregate roots
- Domain events (published and consumed)
- Commands and queries
- Integration points (APIs, events, data flows)
- Invariants (HARD business rules that must always be true)
- Cross-domain workflows (saga specifications)

#### Cross-Domain Workflows Section

When a domain participates in multi-domain workflows, include a
"Cross-Domain Workflows" section in the DDD spec. For each workflow that
touches this domain:

1. Trace the cross-domain path manually: read `.magellan/cross_domain.json`
   to find inter-domain edges, then read the referenced entities from
   `.magellan/domains/<domain>/entities/<entity_id>.json` and follow the
   edges in `.magellan/domains/<domain>/relationships.json` to build the
   path across domains. Repeat for each domain the workflow touches.
2. Document each workflow with:
   - **Step sequence**: ordered list of steps across domains
   - **Domain events**: the event at each boundary crossing
   - **Compensation actions**: what to undo if a step fails
   - **Timeout considerations**: SLAs or time constraints from the KG
   - **Failure modes**: what can go wrong and the impact

3. Include a **Mermaid sequence diagram** embedded in the markdown showing
   the temporal flow across domain swimlanes:

```markdown
## Cross-Domain Workflows

### Sale-to-Settlement Saga

Steps:
1. **Sales** → SaleCompleted event
2. **Financial** → Calculate fees, generate invoice → InvoiceCreated event
3. **Title** → Title check with DMV → TitleTransferApproved or TitleHold
4. **Financial** → Settlement → SettlementCompleted event
5. **Transportation** → Schedule transport → VehicleDispatched event

Compensation:
- Step 3 fails (TitleHold): Financial reverses fees (Step 2 compensation)
- Step 4 fails (SettlementFailed): Title transfer is rolled back

\```mermaid
sequenceDiagram
    participant SAL as Sales
    participant FIN as Financial
    participant TIT as Title
    participant TRN as Transportation

    SAL->>FIN: SaleCompleted
    FIN->>FIN: Calculate fees
    FIN-->>SAL: InvoiceCreated
    SAL->>TIT: InitiateTitleTransfer
    alt Title clear
        TIT-->>SAL: TitleTransferApproved
    else Title issue
        TIT-->>SAL: TitleHold
        SAL->>FIN: ReverseFees (compensation)
    end
    FIN->>TRN: SettlementCompleted
    TRN->>TRN: Schedule transport
\```
```

Only include workflows where the KG has evidence of cross-domain interactions.
Do not invent workflows — they must be traceable to cross-domain edges and
domain events in the KG.

### 3. contracts.md

Implementation contracts. These are what developers build from — they must be
complete enough to code against without guessing.

API contracts (for each endpoint):
- HTTP method, path, description
- Request schema (body, path params, query params)
- Success response schema (200/201)
- Error response schemas (400, 401, 403, 404, 409, 500) with error code and message format
- Authentication requirements (JWT, API key, service-to-service)
- Pagination pattern (cursor-based or offset-based, with standard envelope)
- Idempotency requirements (which operations need idempotency keys)
- Rate limiting (if applicable)

Event schemas:
- Event name, topic/queue
- Payload schema with all fields typed
- Publishing trigger (what causes this event)
- Expected consumers

Data model:
- Entities with field names, types, constraints
- Relationships and foreign keys
- Indexes for common query patterns

Integration contracts:
- How this context communicates with others (sync API calls, async events)
- Which direction data flows
- Error handling for cross-context failures

### 4. review.md

Review document for the architect team:

- What was decided and why
- What the proposed new system looks like for this domain
- Key differences from the current system
- Risks and assumptions
- Contested facts (from contradictions) that affect the design
- Open items that need team discussion

## Weight-Based Prioritization

Prioritize entities with weight > 0.7. Include lower-weight entities only when
they provide context for a high-weight entity. Never base a design decision
solely on an entity with weight < 0.5.

## Output Limits

Write each deliverable file immediately after generating it. Do NOT try to
generate all four files for a domain in one response — this will hit output
limits. The pattern is:

1. Generate business_rules.md → write it
2. Generate ddd_spec.md → write it
3. Generate contracts.md → write it
4. Generate review.md → write it
5. Move to next domain

---
name: onboarding-guide
description: Generate a beginner-friendly narrative document that explains everything discovered about the client's systems. Use after domain summarization to produce onboarding_guide.md.
---

# Onboarding Guide Generation

You produce `onboarding_guide.md` — a document that a new architect reads on their
first day to understand the client's business and systems. It is written for someone
who knows nothing about the client.

This document auto-regenerates every time the pipeline runs. It is derived from the
domain summaries, open questions, and contradictions — not from the raw entity files.

## When to Generate

- After Stage 2c (domain summarization) in a full pipeline run
- On demand when an architect requests it
- After significant new material is ingested (determined by the orchestrator)

## Process

1. Discover all domains using Glob on `.magellan/domains/*/` (each subdirectory name
   is a domain).
2. Read each domain's summary using the Read tool on
   `.magellan/domains/<domain>/summary.json`.
3. Read open questions and contradictions for each domain using the Read tool on
   `.magellan/domains/<domain>/open_questions.json` and
   `.magellan/domains/<domain>/contradictions.json`. To get consolidated data across
   all domains, read each domain's files and aggregate.
4. Read `.magellan/index.json` using the Read tool for overall stats.
5. Read `.magellan/cross_domain.json` using the Read tool for inter-domain connections.
6. Synthesize the guide following the structure below.
7. Write the guide to `.magellan/onboarding_guide.md` using the Write tool.

## Guide Structure

Write the guide in Markdown with these sections:

### 1. The Business

What does this company do? Who are their customers? What industry are they in?
What are their core operations?

Derive this from the domain summaries and entity types. If the KG contains a
Statement of Work, SOW, or project description, reference it. Otherwise, infer
from the systems and business rules discovered.

Write 2-3 paragraphs. Use plain language, no jargon.

### 2. The Systems

What software runs the business? Give a high-level map of the technology landscape:
- What are the main systems (AS/400, web apps, APIs, databases)?
- How do they connect?
- What technology stack is each system built on?

Explain this as a narrative, not a list. "When a vehicle arrives at the auction,
here's what happens in the system..." Walk through a key business flow to make
the technology concrete.

Derive from domain summaries and cross-domain connections.

### 3. The Domains

For each domain in the KG, write a section with:
- What this domain is responsible for
- The most important entities (from hub summaries)
- Key business rules
- How this domain connects to other domains

When mentioning a hub entity, include its entity ID as a cross-reference so
readers can look it up in the KG (e.g., "the Invoice Generation process
(`billing:invoice_generation`) handles...").

Start each domain section with a metrics line:

```markdown
#### Billing (23 entities, 5 hubs, 3 open questions, 1 contradiction)
```

Order domains by importance (most hub entities, most cross-domain connections first).

### 4. The Gotchas

Things that would take weeks to discover by reading source materials directly:
- Undocumented behaviors found in code that aren't in any manual
- Workarounds or hacks that are still in production
- Contested facts (from contradictions) — where sources disagree
- Systems or processes that behave differently than documented

These are the facts that an architect needs to know but wouldn't find in an
architecture diagram.

Link each gotcha to the specific contradiction or open question by ID so it's
traceable:

```markdown
- **Invoice threshold mismatch**: The MANUAL_REVIEW threshold is $10,000 in the
  ops runbook but $5,000 in the database config. Both are in production.
  (See contradiction `c_001`, directed to senior_developer)
```

### 5. Open Questions

What we still don't know, organized by domain and priority:
- Critical questions that block understanding of core processes
- High-priority questions needed for design decisions
- Medium/low questions for completeness

For each question, note who should be asked (the `directed_to` field).

### 6. Coverage Summary

A brief summary of what has been ingested and what hasn't:
- Total documents ingested
- Total entities, relationships, contradictions, open questions
- Domains covered and their entity counts
- Which source documents contributed to each domain's knowledge
- Any known gaps — domains with thin coverage (fewer than 5 entities),
  directories that haven't been ingested, file types that failed

Highlight domains with thin coverage so the team knows where to focus
next:

```markdown
| Domain | Entities | Sources | Coverage |
|--------|----------|---------|----------|
| billing | 23 | 8 documents | Strong |
| title | 18 | 6 documents | Strong |
| transportation | 4 | 2 documents | **Thin — needs more source materials** |
```

### 7. Suggested First Touches

Auto-generate 2-3 safe, low-risk discovery tasks for a new engineer joining
the engagement. These tasks should be:

- **Low-risk**: read/investigate only, not change
- **Domain-specific**: builds expertise in one area
- **Directly useful**: resolves an open question or adds coverage

Derive suggestions from:
- Open questions tagged for developers that could be resolved by reading
  one specific document or code module
- Domains with thin coverage that need more source material reviewed
- Simple contradictions that could be resolved by reading one more document

Example:

```markdown
## Suggested First Touches

1. **Review CBBLKBOOK module** — The billing domain has an open question about
   the invoice threshold (see `oq_003`). Reading the CBBLKBOOK COBOL source
   will clarify whether the $10k or $5k threshold is active. This is a
   well-scoped task that familiarizes you with the billing domain and the
   AS/400 codebase.

2. **Add transportation documents** — The transportation domain has only 4
   entities from 2 source documents. Adding the dispatch manual or route
   planning docs would significantly improve coverage.

3. **Verify title transfer timing** — Contradiction `c_004` notes a conflict
   between immediate and batch title transfers. The Title_Process_Manual.pdf
   section 4.1 likely resolves this.
```

### 8. Discovered Materials

If `discovered_links.json` files exist in domain directories, include a section
showing what the pipeline found and what still needs to be collected.

Read `discovered_links.json` for each domain and aggregate by terminal status:

```markdown
## Discovered Materials

During ingestion, the pipeline discovered 47 links across all documents.

| Status | Count | Action Needed |
|--------|------:|---------------|
| Ingested automatically | 12 | None — already in the KG |
| Skipped by rule | 18 | None — matched project skip rules |
| Auth required | 5 | Download manually and add via `/magellan:add` |
| Tool unavailable | 3 | Install required tools (see below) |
| Manual collection needed | 4 | Ask client team for these documents |
| Fetch failed | 1 | Retry or download manually |
| Dead links | 2 | No action — links are broken |
| Already ingested | 2 | None — already processed |

### Materials to Collect

These references were found in source documents but couldn't be fetched
automatically. Prioritized by how many source documents reference them:

1. **Dealer Master Manual, section 3.2** — referenced by 3 documents
   (Q3_ops_runbook.pdf, Architecture_Overview.pdf, billing_procedures.docx).
   Status: manual_collection. Ask the client team for a copy.

2. **company.sharepoint.com/sites/arch/designs.pdf** — referenced by 2 documents.
   Status: auth_required. Requires VPN + SSO. Download and add via `/magellan:add`.

### Configure These Tools

The following link types couldn't be resolved because the tool isn't configured:

- **GitHub**: 3 links found. Install and configure `gh` CLI.
```

If no `discovered_links.json` files exist, omit this section entirely.

## Writing Style

- Write for a reader who is new to this client's systems
- Use plain language — explain acronyms on first use
- Be specific — "the AS/400 runs a nightly batch job that reconciles settlements"
  not "there is a batch process"
- Be honest about uncertainty — if confidence is low, say so
- Put the most important information first in each section
- Keep it under 3000 words total — this is a briefing, not a book

## What You Do NOT Do

- Do not copy entity JSON into the guide. Translate everything to natural language.
- Do not list every entity. Focus on hubs and key facts.
- Do not hide contradictions or open questions. They are features, not bugs.
- Do not invent information beyond what the KG contains.

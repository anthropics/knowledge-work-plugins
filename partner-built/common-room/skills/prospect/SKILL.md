---
name: prospect
description: "Build targeted account or contact lists using Common Room's Prospector. Triggers on 'find companies that match [criteria]', 'build a prospect list', 'find contacts at [type of company]', 'show me companies hiring [role]', or any list-building request."
---

# Prospecting

Build targeted account and contact lists using Common Room's Prospector. Supports iterative refinement through natural conversation, intent-based discovery, and both net-new prospecting and signal-based queries against existing accounts.

## Critical Distinction: Two Object Types

Common Room's Prospector operates against two fundamentally different object types. Always clarify which one is in play before running a query:

**`ProspectorOrganization`** — Companies **not yet in Common Room**
- Net-new companies that match specified criteria
- Available fields are firmographic only: name, domain, size, industry, capital raised, annual revenue, location
- Fewer filter options — no signal-based filters, no scores, no activity history
- Use when: building a brand-new target list, territory planning, top-of-funnel expansion

**`Organization`** (in Common Room) — Companies **already in your CR workspace**
- Full signal data available: product usage, community activity, CRM fields, scores, custom fields
- Much richer filter set — includes signal-based, score-based, segment-based, and firmographic filters
- Use when: finding warm accounts to prioritize, identifying expansion candidates, surfacing intent signals within existing pipeline

When a user's request could apply to both (e.g., "Show companies hiring AI engineers this month"), clarify:
> "Are you looking for net-new companies not yet in Common Room, or filtering accounts already in your workspace?"

The catalog should make this distinction explicit so the LLM can select the right Prospector endpoint.

## Step 0: Load User Context (Me)

Fetch the `Me` object to get the user's segments. When prospecting against `Organization` records (accounts already in CR), default to filtering within "My Segments" unless the user asks for a broader search.

## Step 1: Gather Targeting Criteria

If criteria are already provided, proceed. Otherwise ask:

> "What kind of accounts or contacts are you looking for? For example: company size, industry, job titles, signals like recent product activity or community engagement, geographic region, or specific intent signals like recent funding or job postings."

Use the Common Room object catalog to see available filters for each object type. The key distinction:
- **ProspectorOrganization** — firmographic and technographic filters only (industry, size, geography, funding, tech stack)
- **Organization** — all firmographic filters plus signal-based, score-based, segment-based, and CRM filters

**Lookalike search:** If the user asks to "find companies like [X]", first look up the reference company in Common Room (or via web search if not in CR). Extract its key attributes — industry, employee range, tech stack, funding stage, geography — and propose those as filter criteria. Present the derived criteria to the user for confirmation before running the search, since lookalike targeting works best when the user can refine which attributes matter most.

## Step 2: Support Iterative Refinement

Prospecting is conversational. Support multi-turn refinement naturally:

1. Run initial query with provided criteria
2. If results are large (50+), summarize and offer: "I found [N] results. Want to narrow by [suggested filter]?"
3. If results are too few (< 5), suggest: "Only [N] results with those filters — I can broaden by relaxing [specific criterion]."
4. Apply each refinement as a follow-up query, not a new search from scratch

Example flow:
- Rep: "Find cybersecurity companies in California." → 500 results
- Rep: "Only show ones over 300 employees using AWS." → 47 results
- Rep: "Focus on the ones with recent hiring activity." → 12 results ✓

## Step 3: Run the Query and Present Results

Execute the Prospector query with confirmed criteria. Sort by signal strength or fit score where available (not alphabetically).

**For `ProspectorOrganization` (net-new) results:**

| Company | Domain | Industry | Size | Capital Raised | Revenue | Location |
|---------|--------|----------|------|---------------|---------|----------|

**For `Organization` (in CR) results:**

| Company | Industry | Size | Top Signal | Signal Date | Score | CRM Stage |
|---------|----------|------|-----------|-------------|-------|-----------|

Flag any results where data is thin or the most recent signal is older than 90 days.

## Step 3.5: Enrich Net-New Results with Web Search

For `ProspectorOrganization` results (net-new companies not in CR), run a quick web search on the top 3–5 companies to add context beyond firmographics. CR has no behavioral signals for these companies, so web search fills the gap — look for recent funding, product launches, leadership changes, or news coverage. Include findings as brief annotations next to each company in the results.

## Step 4: Offer Next Steps

- "Want me to draft outreach for the top 3–5 prospects?"
- "Should I run a full account brief on any of these?"
- "Want to refine the criteria or add another filter?"
- "I can format this as a CSV if you'd like to export it."
- "For any net-new companies here, I can add them to Common Room for enrichment." *(future capability)*

## Quality Standards

- Always confirm which object type (ProspectorOrg vs Organization) before running the query
- Default to "My Segments" when querying Organization records, unless user specifies otherwise
- Support iterative refinement — treat each follow-up as a filter adjustment, not a fresh start
- Never mix result fields from ProspectorOrganization and Organization in the same list
- Fewer high-quality results beat a long unqualified list
- **Only show data the query returned** — leave blank or "—" for missing fields, don't invent values

## Reference Files

- **`references/prospect-guide.md`** — filter types, signal-based sorting, object type distinctions, and list-building strategies

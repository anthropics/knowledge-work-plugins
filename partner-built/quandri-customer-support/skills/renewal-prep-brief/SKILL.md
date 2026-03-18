---
name: renewal-prep-brief
description: >
  Generates a comprehensive renewal preparation brief for an upcoming customer renewal — pulls
  account health from HubSpot, open ticket analysis from Linear, relationship history from Granola,
  sentiment signals from Slack, and produces a structured renewal strategy with risk assessment
  and talking points. Use when: renewal prep, prepare for renewal, renewal brief, renewal strategy,
  account up for renewal, renewing soon, renewal conversation, QBR prep, renewal risk, at-risk renewal,
  accounts coming up for renewal, who is renewing soon.
---

# Renewal Prep Brief

## Purpose
Produce a structured renewal preparation brief for a specific customer account — covering account health, ticket load, relationship history, risk signals, and a recommended renewal strategy. This is deeper than a pre-call brief: it's meant to be used in advance (days, not minutes) to inform how the CSM should approach the renewal conversation.

## When to Use
- "Renewal prep for [Customer]"
- "Prepare for my renewal with [Customer]"
- "Who is renewing in the next 60 days?"
- "Renewal brief for [Customer]"
- "What's the risk on [Customer]'s renewal?"
- "Run a renewal strategy for [Customer]"
- Any time a CSM or manager wants to get ahead of an upcoming renewal

---

## Core Workflow

### Step 1 — Identify the Account(s)

**If the user names a specific customer**: proceed with that account.

**If the user asks "who is renewing soon" or similar**:
- Use `HubSpot:search_crm_objects` (object type: `companies`) filtered by renewal date
- Surface all accounts renewing within the next **90 days**, sorted by soonest first
- Present the list with: Company name | Renewal date | ARR | CSM
- Ask the user which account(s) to prepare a brief for before proceeding

---

### Step 2 — Pull HubSpot Account Context

Look up the company using `HubSpot:search_crm_objects` (object type: `companies`).

Collect:
- **Full company name**, plan tier, ARR
- **Renewal date** — calculate days remaining from today
- **Named CSM** and account owner
- **HubSpot health score or status** (Green / Yellow / Red), NPS if available
- **Customer since** (original close date if available — calculate tenure)
- **Contact history**: last logged activity, last email, last call note
- **Open HubSpot support tickets** — count and any high-priority ones (use `HubSpot:search_crm_objects` filtered to `tickets` linked to this company)
- **Any HubSpot notes or deal properties** relevant to renewal (expansion opportunities, known concerns, competitor mentions)

If the company is not found in HubSpot, note this and continue with what's available from other sources.

---

### Step 3 — Analyze Linear Ticket Health

Use the Linear Customers API to pull all tickets linked to this account:
- Call `list_customers` with `query: [company name]`, `includeNeeds: true`, `limit: 250`
- Paginate with `cursor` until all tickets are retrieved

**Categorize tickets by renewal impact:**

| Category | What to flag |
|----------|-------------|
| 🔴 Blocking | Urgent/High tickets open > 30 days, or any Blocked ticket |
| 🟡 Watch | Medium tickets open > 14 days, or no recent updates |
| ✅ Resolved recently | Tickets moved to Done/Released in last 30 days — these are wins to highlight |
| 📋 Backlog burden | Count of low-priority backlog items (signals accumulated debt) |

Summarize:
- Total open tickets (by status)
- Blocking and Watch tickets (list them individually)
- Recent wins (count + top 2–3 titles)
- Overall ticket health signal: 🔴 / 🟡 / 🟢

---

### Step 4 — Review Relationship History in Granola

Use `Granola:query_granola_meetings` to find all past meetings with this customer.

Pull the **5 most recent meetings**. For each:
- Date, meeting type (QBR, onboarding, sync, escalation review, etc.)
- 2–3 sentence summary of what was discussed and committed to
- Any unresolved Quandri commitments or outstanding promises

Also note:
- **Last QBR date** — flag if no QBR in the last 6 months
- **Overall meeting cadence** — regular check-ins signal healthy engagement; long gaps are a risk signal
- **Sentiment trend** — have recent meetings been positive, neutral, or escalation-heavy?

If no meeting history is found, flag this explicitly — it may indicate low engagement.

---

### Step 5 — Scan Slack for Sentiment Signals

Use `Slack:slack_search_public_and_private` to search for the customer name, looking back **60 days**.

Look for:
- Escalations or urgent flags raised internally about this account
- Positive signals — expansion interest, praise from the customer, success stories shared
- Competitive mentions — any signals the customer is evaluating alternatives
- Internal concerns raised by the CSM or implementation team
- Any commitments made informally in Slack that aren't reflected elsewhere

Summarize any notable signals. If nothing relevant is found, note "No notable Slack activity in the last 60 days."

---

### Step 6 — Assess Renewal Risk

Based on everything gathered, assign an overall **Renewal Risk Rating**:

| Rating | Criteria |
|--------|----------|
| 🟢 **Low Risk** | Renewing 60+ days out, healthy ticket load, positive meeting history, strong CSM relationship, no escalations |
| 🟡 **Medium Risk** | Renewing within 60 days, or elevated ticket count, or irregular meeting cadence, or one unresolved escalation |
| 🔴 **High Risk** | Renewing within 30 days AND open issues, or active escalation, or long gap since last QBR, or competitive signals |
| ⚫ **Unknown** | Insufficient data to assess — flag what's missing |

Write a **2–3 sentence risk narrative** explaining the rating — not just the label.

---

### Step 7 — Build the Renewal Strategy

Based on the full picture, produce:

**Recommended approach** (choose one):
- **Standard renewal** — relationship is healthy, focus on value recap and contract execution
- **Value reinforcement needed** — relationship is okay but the customer may not see enough ROI; lead with wins and usage data
- **Issue resolution first** — open tickets or escalations must be addressed before the renewal conversation can go well; prioritize closing them
- **Executive escalation** — risk is high enough that the CSM alone may not be sufficient; recommend involving Nick or leadership

**Talking points for the renewal conversation** (5–7 specific, evidence-based points):
- Lead with measurable wins from the past year (resolved tickets, product improvements, usage milestones)
- Address known concerns head-on — don't avoid the elephant in the room
- Frame open issues with a clear resolution timeline
- Anchor to value delivered vs. original goals
- If expansion is appropriate, suggest a natural moment to introduce it

---

### Step 8 — Compose the Brief

Follow the structure in `references/renewal-brief-template.md` exactly.

---

### Step 9 — Offer Next Steps

After presenting the brief, offer:

1. **Pre-call brief** — "Want a quick pre-call brief when you have the renewal meeting on the calendar?"
2. **Ticket breakdown** — "Want the full ticket audit for [Customer] to see everything in detail?"
3. **Draft renewal email** — Offer to draft an outreach email to open the renewal conversation
4. **Create a task in Asana** — Offer to create a renewal prep task so nothing falls through the cracks

---

## Smart Defaults & Judgment Calls

| Situation | Default Behavior |
|-----------|-----------------|
| Renewal date not in HubSpot | Note "Renewal date not on file" — flag this as a data quality issue |
| No meeting history in Granola | Flag as a risk signal — low engagement |
| No open Linear tickets | Treat as a positive health signal |
| Multiple HubSpot companies match | Show top matches and ask the user to confirm |
| User asks for all renewing accounts | List all within 90 days, sorted soonest first, with a one-line health signal for each |
| Customer has no CSM assigned | Flag as a gap — note "No CSM assigned in HubSpot" |

---

## Tool Reference

| Tool | Use |
|------|-----|
| `HubSpot:search_crm_objects` | Look up company, renewal date, open tickets |
| `HubSpot:get_crm_objects` | Retrieve detailed account, contact, or deal records |
| `Linear:list_customers` | Find all Linear tickets linked to this customer |
| `Linear:get_issue` | Pull individual ticket details and latest activity |
| `Linear:list_comments` | Get most recent comment on a ticket |
| `Linear:list_issue_statuses` | Confirm exact status names for this workspace |
| `Granola:query_granola_meetings` | Find past meetings with this customer |
| `Granola:get_meeting_transcript` | Pull notes and action items from specific meetings |
| `Slack:slack_search_public_and_private` | Check 60-day Slack history for this customer |
| `Asana:asana_create_task` | Create a renewal prep task if requested |
| `Gmail:gmail_create_draft` | Draft a renewal outreach email if requested |

---

## Team Context (Quandri CX)

- **CSM team**: Jenel McKenney (CSM Manager), Andrew Millar, Jonathan Cox
- **Support team**: Nick (Manager), Alma St. Hilaire, Syed
- **Renewal owner**: Named CSM on the account, with Jenel as escalation point
- **Linear workspace**: linear.app/quandriio
- **Tone**: Strategic and direct — this brief is for internal planning, not customer-facing

---

## Example Invocations

- "Renewal prep for BrokerLink"
- "Who's renewing in the next 60 days?"
- "Renewal brief for Acera — they're up in 3 weeks"
- "What's the renewal risk on First America?"
- "Prepare a renewal strategy for Wawanesa"
- "Which accounts are at risk of not renewing?"

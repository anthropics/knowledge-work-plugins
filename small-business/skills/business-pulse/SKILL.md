---
name: business-pulse
description: >
  Produces a one-page cross-functional business snapshot for SMB owners —
  cash position (the ledger: MYOB, NetSuite, QuickBooks, Xero, or Zoho Books), sales trend
  (PayPal/Square/Stripe), pipeline movement (HubSpot), this week's commitments
  (Calendar), urgent watch-list items (Gmail or M365, Slack), and the single most
  important thing needing attention today.
  Proactively tries every available connector and gracefully scopes to
  whatever is connected — one connector gives a partial pulse; the full stack
  gives the full picture. Trigger when the user asks how the business is
  doing, wants a snapshot, a daily brief, a Friday recap, or says anything
  like "what am I missing" or "catch me up on the business." A start-of-week
  briefing routes to /monday-brief, which runs this skill as its first link.
allowed-tools: Read, WebFetch
---

# Business Pulse

One prompt, one page. Pull live data from every connected tool, synthesize it into a single scannable brief, and surface the single most important thing to act on today. Do the work — don't ask the user to help find the data.

## Step 1 — Pull data in parallel

**Dispatch all connector calls in a single parallel batch** — see `reference/data_sources.md` for the exact tool-to-metric mapping. Do not pull serially; latency turns a 30-second skill into a painful wait.

Connectors to attempt simultaneously:

- **QuickBooks** — cash balance, MTD revenue, outstanding receivables, overdue invoices
- **Xero** — same ledger read for Xero shops: cash position, receivables, P&L trend
- **Zoho Books** — same ledger read for Zoho shops: bank balances, invoiced revenue, overdue invoices (no P&L endpoint, so the revenue line is invoiced revenue and says so)
- **PayPal / Square** — 7-day settlements, sales trend, failed/pending transactions
- **Stripe** — settlements and sales trend, failed payments, and any new disputes — a fresh dispute goes straight to the watch list (if connected)
- **Ramp** — company card spend for the week and the account balance, read-only (if connected)
- **Gusto** — next payroll run date and amount, the week's biggest cash commitment (if connected)
- **TikTok Ads** — last week's ad spend, results, and cost per result, so paid spend shows up next to the sales it claims to drive (if connected)
- **Expensify** — last week's card spend and any expenses missing receipts, read-only, so spending surprises surface before the month-end scramble (if connected)
- **HubSpot** — pipeline by stage, deals moved/closed, deals gone cold, new leads
- **Google Calendar** — key meetings, deadlines, events this week and next 7 days
- **Gmail or Microsoft 365** — threads flagged urgent, customer complaints, time-sensitive requests
- **Slack / Teams** — urgent internal signals, threads needing owner attention
- **RingEx Chat** — the same internal-signal read for RingEx shops: urgent team-chat posts needing the owner (if connected)
- **DocuSign** — envelopes sitting unsigned, flagged once they are more than a few days old — money waiting on a signature (if connected)
- **Zoho Desk** — open tickets, escalations (if connected)
- **Shopify** — orders, revenue, sales trend, and fulfillment issues, so a commerce business sees its actual day (if connected)
- **Square** — fulfillment issues (if connected)

If a connector errors or returns no data, record it internally and move on. Never block the pulse on a single bad integration.

**QuickBooks fallback**: if QBO returns an unexpected state (account not connected, sync pending, empty response), mark the Cash section "n/a — QuickBooks unavailable" and proceed. Do not retry or ask the user to reconnect.

**Gmail fallback**: Gmail auth is intermittently flaky. If the call errors, skip the Watch List section silently and note "Gmail unavailable" in the appendix — do not surface an error mid-pulse.

**Nothing connected at all is a supported path, not a failure.** If every connector is unavailable, don't stop and don't tell the owner to go connect things. Ask once, in one short message, for the handful of numbers that carry the pulse:

- Cash in the bank right now, and roughly what it was a week ago
- Anything overdue — invoices owed to them, bills they owe
- Sales this week versus a normal week, even roughly
- Anything already worrying them this week

Build the same one-page pulse from those answers, label the source line "owner-supplied, not pulled," and skip any section they had no number for. If they'd rather not type numbers, point them at the siblings that run off a file export instead — `cash-flow-snapshot` and `report-builder` both take a CSV — and say plainly that gives a partial picture, not the full one.

## Step 2 — Compute metrics

Read `reference/thresholds.md` for red/yellow/green cutoffs. Compute:

- **AR aging** — open QuickBooks invoices grouped by days since due date (0–30, 31–60, 61+)
- **Pipeline coverage** — HubSpot weighted pipeline ÷ monthly revenue target
- **Revenue trend** — this month's QBO revenue vs. prior month (or 7-day PayPal/Square vs. prior 7 days)

Assign a 🟢/🟡/🔴 status to each section. If a source returned nothing, mark the metric "n/a" and note it in the appendix.

## Step 3 — Flag risks proactively

Scan for actionable items. Every risk entry must name a specific record and a next step — "some overdue invoices" is useless; "USD 3,400 from Acme Corp, 47 days overdue, no response since Mar 12" is actionable.

- Ledger invoices past due > 30 days — name customer, amount, days overdue
- HubSpot deals with no activity in 7+ days, or close date in past but still open
- Mail threads marked urgent or containing "escalation," "complaint," "cancel," "refund"
- Failed or pending PayPal/Square/Stripe transactions above the threshold in `reference/thresholds.md` (200 in the business's currency)

## Step 4 — Compose the output

Use the exact template in `reference/output_template.md`. Include only sections where real data exists — omit headers for connectors that weren't available. Adapt depth to context: a casual "how are we doing" gets a fuller report; "quick snapshot before a call" gets a tighter one.

Cross-connector synthesis is where this skill earns its keep. If a Slack message connects to a stalled HubSpot deal, surface that link in the #1 Priority section. Synthesis is what makes the pulse more useful than checking each tool separately.

Writing rules:
- Numbers lead, words follow. Never write "revenue is healthy" — write "USD 43k this month, ▲ 8% MoM" and let the owner judge.
- Every number carries a delta vs. the prior period where available. Absolute snapshots (cash balance) still show WoW delta.
- Names and dollars, not adjectives. "USD 4,200 from Acme, 23 days overdue" beats "some concerning receivables."
- No filler. If a section has nothing worth reporting, write "No material changes" and move on.

## Step 5 — Deliver the pulse page

Alongside the chat pulse — never instead of it — deliver the full pulse per
the owner's stored output preference — never default to a markdown file.
Check the `## Business context` block's `Output preference` (shared style
guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the pulse as an HTML page in the
  house style. Cash balance, MTD revenue, and weighted pipeline are stat tiles
  with their deltas as context lines; each section's 🟢/🟡/🔴 becomes a status
  pill (good, warn, critical); the watch-list risks are a table with
  tabular-nums amount columns; the #1 Priority gets its own panel at the top;
  unavailable connectors go in one quiet appendix line.
- **docx / md / notion / canva preference:** deliver the same content in that
  form — a DOCX or markdown file, a Notion page created via the connector
  (named destination, never overwriting), or a Canva Doc created via the Canva
  connector (a new design each run, named with the date; tables become
  lists); fall back to the visual artifact if Notion or Canva is not
  connected — and say that is why.
- **Best for skill:** use the visual artifact — a pulse is scanned, not filed.

## Step 6 — Export and share (once)

After presenting the pulse, offer once:
- "Want me to save this as a file?" (use Files connector if available — this means a copy in their drive, not a second HTML download beside the artifact)
- "Should I post this to your Slack?" (only if Slack is connected and the user confirms — Slack write requires explicit approval)

If they say yes, do it. If they say no or don't respond, move on — don't ask again.

## After the run

Close with one line on what the pulse covered, then the single most relevant
next step and at most two others nearby:

- If cash or AR flagged red: "who owes me money" runs `invoice-chase`.
- If growth questions dominate: "is my marketing working" runs `growth-pulse`.
- To make this recurring: "Monday brief" runs `/monday-brief` every week.

Max three offers. Never repeat an offer the owner declined this session.

## Scope variants

The owner may ask for a narrower cut:

- **"Just cash" / "financial check"** → only Cash & Finance + AR-related risks
- **"Pipeline only" / "deals check"** → only Pipeline section + stalled-deal risks
- **"Watch list" / "anything urgent"** → only Watch List + all risks, no metric sections
- **"Quick snapshot before a call"** → TL;DR + #1 Priority only, no full sections

## What not to do

- **Do not ask permission before pulling data.** If the skill was invoked, run it. Asking "should I check QuickBooks?" defeats the whole point.
- **Do not invent or estimate numbers.** If a source returned nothing, say "n/a" explicitly. Never fill a gap with guesswork.
- **Do not skip the delta.** A number without a comparison is a missed insight. If there's no prior-period baseline, say "(no prior baseline)" rather than omitting the field.
- **Do not surface connector errors mid-pulse.** Log them to the appendix. The pulse leads with what was delivered.
- **Do not trust a QuickBooks summary object.** Expenses, margin, and AP aging buckets come from the rows or the detail call (`../../shared/quickbooks-report-traps.md`).

## More sources, and scheduled presets

Read `reference/v2_sources.md` for the mapping:

- **Shopify** — orders, revenue, and fulfillment status, so a commerce business sees its actual day in the pulse
- **Any ledger** — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books feed the Cash & Finance section; they are peers (`../../shared/connector-neutrality.md`). With two connected, the owner names one as the source of record for totals

The pulse still builds from whatever is connected and degrades gracefully — one connector gives a partial pulse, the full stack gives the full picture.

### Scheduled presets

This skill is schedulable, and the preset decides the shape:

| Preset | When | Shape |
|---|---|---|
| Monday | Start of week | Full pulse, forward-looking. What's coming and what needs attention |
| Friday | End of week | Recap. What moved, what closed, what slipped |

Scheduling is a property of this skill, not a reason for a separate command.

Offer a cadence once, after a pulse the owner found useful. Don't ask twice.

## Reference files

- `reference/data_sources.md` — exact connector tool → metric mapping with fallbacks
- `reference/thresholds.md` — 🟢/🟡/🔴 cutoffs, tunable per owner
- `reference/output_template.md` — exact markdown structure; do not deviate
- `reference/gotchas.md` — known failure modes (QB states, Gmail auth, Slack write)

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.

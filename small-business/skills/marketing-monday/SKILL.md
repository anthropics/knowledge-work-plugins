---
name: marketing-monday
description: Delivers the weekly growth briefing as one merged read — whether the growth engine is working, what customers are saying in public and private, what competitors actually changed, and the three growth actions worth taking this week. The growth twin of the Monday brief, chaining growth-pulse and review-reputation and adding a web-native competitor scan, merged into a single page rather than three reports. Offers to run on a weekly cadence once, and sets it up on a yes. Use this whenever the owner wants a recurring or one-off growth check, including phrasings like "how's marketing doing," "growth check for the week," "give me my Monday growth brief," "what should I be doing about growth this week," "are we winning or losing out there," or "set up a weekly marketing update." Reach for it when the owner asks how the business is growing rather than how it is paying its bills.
allowed-tools: Read, WebFetch
---

Run the weekly growth briefing by chaining two skills — `growth-pulse` for whether the engine is working and `review-reputation` for what customers are saying — then adding a web-native competitor scan. The three parts feed one merged brief; this is not three reports stapled together.

Connectors: any one of PayPal, Shopify, or HubSpot is enough to run. Apollo, Clay, Mailchimp, Square, Stripe, and TikTok Ads each add a layer. TikTok Ads contributes the paid layer to Step 1 through growth-pulse: last week's spend, results, and cost per result beside the sales trend, reported as the platform's own claim next to the CRM's lead count, never blended (`../growth-pulse/reference/data_sources.md`). Mailchimp contributes the email channel to Step 1 (its `get_capabilities` call needs `user_request` and a `category`; `../../shared/connector-call-shapes.md`) — campaign analytics with revenue attribution and audience-growth numbers. It is read-only in this brief: nothing is drafted or sent from here, and its attributed revenue is reported as the email channel's own claim beside the platform and CRM numbers, never blended into one figure. With none of them, CSV exports and pasted reviews go in, and the competitor scan runs web-native with no connector at all.

Default window: the last 7 days for the pulse, the last 90 days for reviews, and since the last run for the competitor watchlist.

## Step 1 — Is the engine working (growth-pulse)

Trigger the `growth-pulse` skill workflow. Pull every connector in one parallel batch; a serial run is a wait nobody sits through twice.

**In:** whatever is connected, or exports. **Out:** channel trend, funnel conversion, campaign return, product performance, and sentiment — each with a status, and anything missing marked "n/a" rather than silently dropped.

**Handoff:** carry forward the single sentence that explains the period, plus the biggest drop-off in the funnel and any product carrying the whole trend. Do not carry the full five-view dashboard into the merged brief.

**No gate here.** The command was invoked; run it. Reading data is not an approval-worthy action.

## Step 2 — What customers are saying (review-reputation)

Trigger the `review-reputation` skill workflow.

**In:** public reviews, PayPal disputes, HubSpot tickets, complaint-language email threads, and pasted or exported reviews when nothing reads them directly. **Out:** three to five themes with verbatim quotes, reviews needing a reply, and customers who have gone quiet.

**Handoff:** carry forward the themes and the rating direction. Carry the drafted replies as a separate approval queue, not as brief content.

**Gate:** nothing posts publicly without the owner reading it first, one review at a time. This gate survives the chain intact — a merged brief does not become blanket approval to reply on the owner's behalf.

If the quiet-customer list is worth working, point at `/reactivate` rather than starting win-back drafts inside this brief.

## Step 3 — What competitors did (web research)

Run this leg inline — it needs no connector. Check the owner's saved watchlist of competitors (or ask for three or four names the first time, then save them) and scan public sources: their site and pricing pages, social and ad activity, job postings, and any press. Add HubSpot win-loss notes when HubSpot is connected.

**Out:** what changed, with observed facts and inferences labeled separately and everything dated. Never present an inference as an observation.

**Handoff:** carry forward only material changes. A quiet week is reported as a quiet week — three lines, no padding. That honesty is what makes the week something real happens land hard.

**Gate:** nothing acts on the intel. A price move or a campaign is the owner's decision.

## Step 4 — Merge into one brief

This is the step that makes the command worth having, so do not shortcut it.

The output is **one page**, not three sections handed over intact. Read the three inputs together and find where they explain each other. The connections that usually matter:

- Sentiment sliding while revenue holds is the early warning that shows up in revenue two months out.
- A competitor's price move against a product whose margin is already thin is a decision, not a note.
- Falling win rate with strong lead volume, plus review complaints about response time, is one story told twice.
- A quiet-customer list growing alongside a new competitor location is churn with a named cause.

Structure:

1. **Headline** — the one thing that matters this week, in a sentence
2. **How growth performed** — the numbers, each with its comparison
3. **What customers said** — themes with verbatim quotes
4. **What changed around you** — competitor moves, observed and dated
5. **Do these three things this week** — exactly three, ranked by size of impact

Every action needs what to do, the number from this brief that justifies it, and roughly what it is worth. Rank by impact, not by ease — Ray Okonkwo can judge what is easy; only the brief can tell him what is big.

If the honest answer is that nothing needs to change, say that. A brief that manufactures three actions every week trains the owner to ignore all of them.

## Step 5 — Offer the cadence, once

Offer to run this weekly. Ask once. On a yes, set the schedule and confirm the day and time. On a no or no answer, move on and do not ask again in the same run.

Each scheduled run compares against the previous one and rolls the baseline forward, because change only means anything against a baseline.

## Approval gates (must hold)

- No public review response posts without per-review approval.
- No win-back message sends from this command — that is `/reactivate`.
- No pricing or campaign action is taken on competitor intel. Recommend and stop.
- The cadence is set only on an explicit yes.
- If a connector fails, name it in the sources line and continue. A named gap is information; a silent one looks like good news.

## What not to do

- **Do not staple three reports together.** One merged brief with three actions at the end is the deliverable. If the output reads as a growth section, then a review section, then a competitor section with no connective sentence between them, it failed.
- **Do not pad a quiet week.** "Nothing material changed" protects the credibility of the week something did.
- **Do not invent attribution or a competitor move.** Both get repeated to other people.
- **Do not report CRM forecast value as revenue.** Deal values are hopes; invoices are facts.
- **Do not ask about the schedule more than once.**
- **Do not exceed three actions.** Four is a to-do list nobody works.
- **Do not read expenses or margin from the QuickBooks P&L summary.** Its `totalExpenses` can be zero against real rows; total the rows or `monthlyBreakdown` (`../../shared/quickbooks-report-traps.md`, Trap 2).

## Output

One page in chat, with the three actions last. Offer once to save it as a file or post it to Slack, then stop asking.

Also deliver the merged brief per the owner's stored output preference — never default to a markdown file. Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the brief as an HTML page in the house style. One page, mirroring the merge: growth stat tiles for the headline numbers, a sentiment-themes panel with verbatim quotes, the competitor-changes list dated and labeled observed vs. inferred, and a three-actions panel last. The chat summary stays — the artifact is additive, never the only copy.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — a weekly brief is scanned, not filed.

## Closing offer

End with one line on what was delivered — the week's headline and the three actions. Then offer the single most relevant next step with its exact trigger phrase, usually "win back quiet customers" (`/reactivate`) when the quiet-customer list is worth working. Offer at most two others drawn from the router's table, such as "what should I promote?" (`content-strategy`) or "who should I call?" (`lead-triage`). Three offers maximum, and never re-offer something the owner already declined this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.

---
name: growth-pulse
description: >
  Answers one question for an SMB owner — is the growth engine actually working?
  Pulls sales trend by channel, funnel conversion, campaign return, best and
  worst performing products, and customer sentiment from whatever is connected,
  then ends with the three growth actions worth taking this week. The growth-side
  twin of business-pulse, which covers the finance side. Use this whenever the
  owner asks how marketing or sales is performing, whether a campaign paid off,
  where leads are coming from, why the pipeline is stalling, which products are
  moving, or says anything like "is my marketing working," "growth check,"
  "how's the funnel," or "where should I put my money next month." Reach for it
  even when the owner names a single channel rather than growth overall.
allowed-tools: Read, WebFetch
---

# Growth Pulse

One page that answers whether the growth engine is working, and what to do about it this week.

Owners describe pulling numbers from three dashboards and trying to find the story themselves. The story is the deliverable here — not the dashboards.

## Step 1 — Pull everything in parallel

Dispatch all connector calls in a single batch. See `reference/data_sources.md` for the metric-to-tool mapping. Serial pulls turn this into a wait nobody sits through twice.

- **HubSpot** — deals by stage, new contacts, lead source, win rate, cycle time, stalled deals
- **PayPal, Stripe, Square** — revenue trend, transaction counts, refunds
- **Shopify** — orders, SKU-level revenue, repeat purchase rate
- **QuickBooks** — realized revenue, the number the books agree with
- **TikTok Ads** — last week's spend, impressions, clicks, results, and cost per result per campaign, from the native connector (`report_integrated_get`, last 7 days against the prior 7), so paid spend sits beside the sales it claims to drive
- **Mailchimp** — campaign, e-commerce, and audience-growth analytics, with revenue attribution on campaigns
- **Gmail or Microsoft 365** — inbound inquiry volume and response times
- **Public reviews** — recent ratings and review text, via web research

If a source errors or is missing, record it and move on. This skill is designed to say something useful on one connector and something excellent on six.

**Zero connectors is a supported path.** Ask for exports — a CRM deal export, a sales report, an ads performance CSV — and build the same pulse from files. Say it plainly rather than stalling.

## Step 2 — Compute the five views

Read `reference/thresholds.md` for the cutoffs. Compute each view and assign it a status.

1. **Channel trend** — revenue by channel this period versus last, and versus the same period last year where available
2. **Funnel conversion** — leads in, qualified, opportunities, won; the conversion rate between each step and where the biggest drop-off sits
3. **Campaign return** — spend versus attributed revenue per campaign, and cost per lead
4. **Product performance** — top three and bottom three by revenue and by growth rate
5. **Customer sentiment** — recent review scores, review themes, disputes, churn signals

A view with no data gets marked "n/a" and named in the appendix. It does not silently vanish.

## Step 3 — Find the actual story

This is where the skill earns its keep. Five views on their own are still a dashboard. The job is to connect them.

The connections that matter most:

- **Spend rising while cost per lead rises** means the channel is saturating, not scaling
- **Strong lead volume with falling win rate** points at lead quality or response speed, not at marketing
- **One product carrying the whole trend** means the growth is more fragile than the total suggests
- **Sentiment dropping while revenue holds** is the early warning that shows up in revenue two months later
- **A stage where the funnel drops off sharply** is usually worth more than any new campaign

Look for the single sentence that explains the period. Lead with it.

## Step 4 — Write the three actions

Every pulse ends with exactly three actions. Not five, not a list of everything noticed.

Each action needs three things or it isn't an action:

- **What to do** — specific enough to start today
- **Why** — the number from this pulse that justifies it
- **What it's worth** — the rough size of the opportunity or the risk

Rank them by size of impact, not by ease. Owners can decide what's easy; only this pulse can tell them what's big.

If the honest answer is that nothing needs to change, say that. A pulse that manufactures three actions every week trains the owner to ignore them.

## Step 5 — Compose

Use the exact structure in `reference/output_template.md`. Include only sections with real data.

Writing rules:

- Numbers lead, words follow. Not "paid social performed well" — "paid social drove 41 leads at USD 18 each, down from USD 31 last month."
- Every number carries its comparison. A figure with no baseline is a missed insight.
- Name the specific campaign, product, channel, or customer. "Some campaigns underperformed" is unusable.
- No marketing vocabulary the owner doesn't use. Not "top of funnel velocity" — "how many new leads came in and how fast."
- If a section has nothing worth saying, write "No material change" and move on.

## Step 6 — Deliver the pulse page

Alongside the chat pulse — additive, never a replacement — deliver the full pulse per the owner's stored output preference — never default to a markdown file. Check the `## Business context` block's `Output preference` (shared style guide rule, `../../shared/artifact-style.md`):

- **Visual artifact (the default):** render the pulse as an HTML page in the house style. Each of the five views gets a panel; revenue trend, cost per lead, and win rate are stat tiles with their comparison as the context line; campaign return and product performance are tables with tabular-nums spend and revenue columns; each view's status becomes a status pill (good, warn, critical, or n/a in plain text); the three actions close the page in their own panel, ranked.
- **docx / md / notion / canva preference:** deliver the same content in that form — a DOCX or markdown file, a Notion page created via the connector (named destination, never overwriting), or a Canva Doc created via the Canva connector (a new design each run, named with the date; tables become lists); fall back to the visual artifact if Notion or Canva is not connected — and say that is why.
- **Best for skill:** use the visual artifact — five views compare best side by side on one screen.

## Step 7 — Offer to save, once

After presenting, offer once to save the pulse as a file or post it to Slack. Posting to Slack is an outward write, so it only happens on that explicit yes — the offer is the approval gate. If yes, do it. If no or no response, move on. Do not ask twice.

Then close with what the pulse found in one line, plus the single most relevant next step and at most two others nearby:

- If the actions point at content or promotion: "what should I promote" runs `content-strategy`.
- If the funnel is the problem: "fill my funnel" runs `/grow-pipeline`.
- For the finance-side twin: "how's the business doing" runs `business-pulse`.

Max three offers. Never repeat an offer the owner declined this session.

## Scope variants

Owners often want a slice rather than the whole pulse:

- **"How did the campaign do"** — campaign return only, plus the sentiment check
- **"How's the pipeline"** — funnel conversion and stalled deals only
- **"What's selling"** — product performance only
- **"Are we getting reviews"** — sentiment only
- **"Where should I spend next month"** — channel trend and campaign return, with the three actions weighted toward budget

Give them the slice they asked for. Don't force the full pulse on a narrow question.

## What not to do

- **Do not ask permission before pulling data.** The skill was invoked. Run it.
- **Do not invent attribution.** If a campaign's revenue can't be traced, say the attribution is unavailable rather than assigning revenue on a guess. Fake attribution has moved real budgets.
- **Do not report CRM forecast value as revenue.** Deal values are hopes; invoices are facts. Label which is which.
- **Do not double-count across sources.** A Shopify order settled in Stripe is one sale. Pick one revenue source and name it.
- **Do not double-count inside one source.** The sales-by-customer summary returns both a parent summary row and a separate total row for the same customer. Filter rows marked as totals before you rank customers or compute concentration, or the same customer lands in the list twice and the concentration figure comes out too high.
- **Do not manufacture urgency.** If growth is steady, the pulse should read as steady.
- **Do not read expenses or margin from the QuickBooks P&L summary.** Total the rows (`../../shared/quickbooks-report-traps.md`, Trap 2).

## Reference files

- `reference/data_sources.md` — connector to metric mapping, with fallbacks
- `reference/thresholds.md` — status cutoffs for each of the five views
- `reference/output_template.md` — exact output structure
- `reference/gotchas.md` — the failure modes that produce confidently wrong growth advice

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.

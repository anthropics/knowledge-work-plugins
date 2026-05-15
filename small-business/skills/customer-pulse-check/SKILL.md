---
name: customer-pulse-check
description: Synthesizes themes from PayPal disputes, HubSpot tickets, and review exports into a top-3 fixable issues list with drafted response templates. Accepts optional since-date argument.
allowed-tools: Read, WebFetch, Bash
---

Run the customer voice synthesis. Pull feedback signals from all connected sources, identify the themes that are actually fixable, and produce drafted responses the owner can review and send.

Parse arguments:
- `--since` (default: last 30 days) — start date `YYYY-MM-DD` for the lookback window

## Step 1 — Gather feedback signals

Using the `customer-pulse` skill workflow:

1. Pull PayPal disputes and chargebacks for the period: reason codes, amounts, resolution status.
2. Pull HubSpot support tickets and conversation notes for the period.
3. If review export files are available (Google Reviews CSV, Yelp export, etc.) in Files: read and parse them.
4. Count total signals per source.

## Step 2 — Theme extraction

Cluster all signals into recurring themes. For each theme:
- Count how many signals mention it
- Classify: Product quality / Delivery / Billing / Communication / Expectation mismatch / Other
- Rate impact: 🔴 High (revenue risk, churn) / 🟡 Medium / 🟢 Low

## Step 3 — Top-3 fixable issues

Using the `ticket-deflector` skill workflow:

Select the top 3 themes by: frequency × impact rating. For each:
1. State the issue in one sentence
2. Explain the root cause (where evident)
3. Suggest a specific operational fix
4. Draft a customer response template

Response template format:
```
Subject: Re: {issue topic}

Hi {first name},

Thank you for reaching out. {Acknowledgment of their experience in 1-2 sentences}.

{What we're doing about it / what happened / resolution offered}.

{Next step or offer}.

{Sign-off}
```

## Step 4 — Summary table

Format the output as:

```
Customer Voice — {date range}
Total signals: {n} ({PayPal disputes: n} | {HubSpot tickets: n} | {Reviews: n})

TOP 3 FIXABLE ISSUES
1. {Issue} ({frequency}) — {impact} — Fix: {one-line fix}
2. {Issue} ({frequency}) — {impact} — Fix: {one-line fix}
3. {Issue} ({frequency}) — {impact} — Fix: {one-line fix}
```

## Connector failures

Run with whatever sources are connected — this command degrades gracefully. If PayPal is missing, skip dispute data and note "PayPal not connected — dispute data skipped." If HubSpot is missing, skip ticket data and note it. If no sources are connected at all, stop and tell the owner: "No feedback sources connected. Connect at least one of PayPal, HubSpot, or upload a review export CSV."

## Approval gates

- **Never send response emails automatically.** Present drafts for owner review only.
- **Never close HubSpot tickets or resolve PayPal disputes without explicit owner confirmation.**
- **Never include customer PII in the summary** — use first name + last initial only.

## Output

Present the summary table, then each response template. Ask the owner which templates they'd like to send, then wait for explicit approval before drafting the send.

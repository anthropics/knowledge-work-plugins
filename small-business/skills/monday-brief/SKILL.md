---
name: monday-brief
description: Generates a one-page Monday morning briefing — cash, sales, pipeline, week ahead, top three to-dos. Accepts optional post destination and save-to arguments.
allowed-tools: Read, WebFetch, Bash
---

Run the Monday Morning Briefing. Pull from every connector that's live, gracefully degrade when one isn't, and deliver a one-page brief the owner can read in under two minutes.

Parse arguments:
- `--post` (default `none`) — post the brief summary to `slack`, `teams`, or `none`
- `--save-to` (default `files`) — `files` (Google Drive / OneDrive), `desktop` (local), or `both`

## Step 1 — Run business-pulse

Trigger the `business-pulse` skill workflow. It pulls in this order, scoping to whatever is connected:

1. **Cash** — QuickBooks balance + last 7 days of net flow
2. **Sales trend** — PayPal/Square last 7 days vs. prior 7 days, % change, top SKU
3. **Pipeline** — HubSpot deals moved, deals stalled (>14 days no activity), new inbound leads
4. **This week's commitments** — Calendar events with external attendees, deliverable deadlines
5. **Watch-list** — unread Gmail flagged "needs reply," Slack DMs awaiting response
6. **The 3 things** — the three highest-leverage actions for today, ranked

If a connector is missing, note it in the brief ("PayPal not connected — sales trend skipped") rather than failing.

## Step 2 — Format the one-page brief

Layout (markdown, fits on one screen):

```
# Monday Brief — {Mon DD, YYYY}

## Cash
{$X balance · {+/-}$Y net last 7 days · runway note}

## Sales (last 7d vs prior 7d)
{$X total · {+/-}Z% · top SKU: {name} ({$})}

## Pipeline
{N deals moved · M stalled · K new leads}

## Week ahead
- {Tue 10am} — {Customer X discovery call}
- {Thu EOD}  — {Proposal due to Y}
- ...

## Three things that need you today
1. {Highest-leverage action with one-line why}
2. {...}
3. {...}
```

## Step 3 — Save and (optionally) post

1. Save the brief to the chosen `--save-to` location:
   - `files` — Google Drive or OneDrive root, filename `monday-brief-YYYY-MM-DD.md`
   - `desktop` — `~/Desktop/monday-brief-YYYY-MM-DD.md`
   - `both` — both locations
2. If `--post slack` or `--post teams`, post the **Three things** section only (not the full brief — keep the channel post short) and link to the saved file.
3. Show the full brief in chat regardless of save target.

## Approval gates

- **Saving the file is auto.** No approval needed — it's the owner's own drive.
- **Posting to Slack/Teams requires confirmation.** Show the post draft and wait for "post it" before publishing.
- **Never post if the brief surfaces unflattering numbers** (significant cash drop, deal slipping) without explicitly asking the owner — the channel may have non-leadership members.

## Cadence note

This command is designed to run weekly. The owner may schedule it via Cowork's task scheduler — when run on Monday at 7am ET, the output goes straight to their drive and (if configured) Slack/Teams DM channel.

---
name: call-list
description: Ranks the top-5 leads most worth calling today, supplies talking points from email history, blocks time on the calendar, and drafts follow-up messages. Accepts optional count and date arguments.
allowed-tools: Read, WebFetch, Bash
---

Run the lead prioritization. Scan the pipeline, rank by urgency and opportunity, pull relevant email context, and get the owner ready to make calls.

Parse arguments:
- `--n` (default: `5`) — number of leads to surface (1–10)
- `--date` (default: today) — date to build the call list for (`YYYY-MM-DD`)

## Step 1 — Pipeline scan

Using the `lead-triage` skill workflow:

1. Pull open HubSpot deals and contacts with activity in the last 30 days.
2. Pull email threads from Mail for each lead (last 3 emails per contact).
3. Score each lead on:
   - **Recency**: days since last owner touchpoint (lower = better)
   - **Stage**: how close to close (later stage = higher priority)
   - **Signal**: any recent inbound activity (email open, reply, calendar hold, web visit)
   - **Value**: deal size from HubSpot

## Step 2 — Rank and select top N

Rank all scored leads and select the top `--n`. For ties, prefer leads with unanswered inbound signals.

For each selected lead, produce a call card:

```
{Rank}. {Contact Name} — {Company}
Deal: ${amount} | Stage: {stage} | Last contact: {X days ago}
Signal: {most recent activity}

TALKING POINTS
• {point from email/deal context}
• {point from email/deal context}
• {open question to ask}

GOAL FOR THIS CALL: {one sentence — advance to next stage / re-engage / close}
```

## Step 3 — Calendar block

For each lead on the list, offer to block 20 minutes on the owner's calendar for the target date.

Show the proposed calendar entries:
```
{time slot} — Call: {Contact Name} ({Company})
```

Wait for owner to confirm which calls to block before creating calendar events.

## Step 4 — Draft follow-ups

For any lead that has an unanswered email older than 3 days, draft a brief follow-up:
```
Subject: Re: {thread subject}

Hi {first name},

{One sentence referencing prior conversation}. {One sentence with a clear next step or question}.

{Sign-off}
```

## Connector failures

If HubSpot is unreachable, stop and tell the owner — lead scoring requires CRM data. If Mail is unreachable, skip Steps 3-4 (email context and follow-ups) and note "Mail not connected — email context and follow-up drafts skipped" in output. If Google Calendar is unreachable, skip calendar blocking and note it.

## Approval gates

- **Never send emails automatically.** Present drafts for owner approval only.
- **Never create calendar blocks without owner confirmation** — show the proposed list first.
- **Never update HubSpot deal stages automatically.**

## Output

Present the ranked call list with talk tracks. Then show proposed calendar blocks and ask for confirmation. Then show follow-up drafts and ask which to send.

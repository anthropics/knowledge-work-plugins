---
name: call-list
description: Builds today's call list. Runs lead-triage to rank the top-5 leads most worth calling, supplies talking points from email history, blocks time on the calendar, and drafts follow-up messages. Trigger on "call list," "who am I calling today," "top five to call today," or "block time for calls." An owner who wants leads scored or ranked with no calendar blocks routes to lead-triage directly. Accepts optional count and date arguments.
allowed-tools: Read, WebFetch
---

Run the lead prioritization. Scan the pipeline, rank by urgency and opportunity, pull relevant email context, and get the owner ready to make calls.

Parse arguments:
- `--n` (default: `5`) — number of leads to surface (1–10)
- `--date` (default: today) — date to build the call list for (`YYYY-MM-DD`)

## Step 1 — Pipeline scan (lead-triage)

Run the `lead-triage` skill workflow for the pull and the scoring — it owns the HubSpot field list, the four-dimension model, the note-body urgency fetch, the flat-score guard, and the enrichment leg (with Apollo or Clay connected, company fit for leads that have no company on file — metered, so lead-triage asks once about the credit cost; pass that question through to the owner rather than answering it). Do not rebuild any of that here. Then pull email threads from Mail for each surviving lead (last 3 emails per contact) for the talking points.

## Step 2 — Rank and select top N

Take lead-triage's ranking and select the top `--n` — always exactly `--n` when that many leads exist, regardless of pipeline size. For ties, prefer leads with unanswered inbound signals. If lead-triage reports flat scores, present its CRM-fact ladder order instead and say so.

For each selected lead, produce a call card:

```
{Rank}. {Contact Name} — {Company}
Deal: {currency code} {amount} | Stage: {stage} | Last contact: {X days ago}
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

If HubSpot is unreachable, stop and tell the owner — lead scoring requires CRM data. If Mail is unreachable, skip the email-context pull in Step 1 and the follow-up drafts in Step 4, and note "Mail not connected — email context and follow-up drafts skipped" in output; calendar blocking in Step 3 still runs. If Google Calendar is unreachable, skip calendar blocking and note it. If the lead-data connector is unreachable or the owner declines the enrichment spend, company fit stays flat for leads with no company on file — say so in the output rather than presenting the order as fit-ranked.

## Approval gates

- **Never send emails automatically.** Present drafts for owner approval only.
- **Never create calendar blocks without owner confirmation** — show the proposed list first.
- **Never update HubSpot deal stages automatically.**

## Output

Present the ranked call list with talk tracks. Then show proposed calendar blocks and ask for confirmation. Then show follow-up drafts and ask which to send.

Alongside the chat summary — never replacing it — render the list as a CALL SHEET artifact using the house style (`../../shared/artifact-style.md`): something the owner prints and works from while dialing. Print-friendly rows, one per lead, each with the call goal and two or three short talking points, plus a blank outcome line to scribble on. This is a work sheet, not a dashboard — no stat tiles, no charts.

## Closing offer

Close with one line on what got built, then the single most relevant next step with its trigger phrase — usually "write this outreach" (`outreach-composer`) for the leads that need email instead of a call. Up to two others: "fill my funnel" (`/grow-pipeline`) or "update the CRM" (`crm-autopilot`). Max three, and skip anything the owner declined earlier this session.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.

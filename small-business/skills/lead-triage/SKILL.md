---
name: lead-triage
version: 0.1.1
description: >
  Scores inbound HubSpot leads by engagement signals, company fit, and urgency
  markers, ranks the ones worth a call today with talking points, drafts the
  follow-ups, and proposes calendar times for the owner to book. Use when the
  owner asks to prioritize, score, or rank leads, asks "who should I call
  first," or asks about their pipeline. An ask that wants the ranked leads
  turned into a call list with time blocked on the calendar routes to
  /call-list, which runs this skill first and then books the time.
allowed-tools: Read, WebFetch
---

# Lead Triage

## Quick start

Pull inbound leads from HubSpot, score them, and surface a ranked call list with talking points. Drafts follow-ups and proposes calendar slots — never sends or books without owner approval.

```
User: "prioritize my leads"
→ Pull contacts: lifecycle stage Lead or MQL, status ≠ Unqualified
→ Score each across engagement, company fit, urgency, recency
→ Return ranked list (size adapts to volume) with talking points
→ Offer to draft follow-ups and propose calendar slots
```

## Workflow

1. **Pull leads from HubSpot.** Fetch contacts with `lifecyclestage` = `Lead` or `MQL` and `hs_lead_status` ≠ `Unqualified`. Use the field list in [reference/hubspot-scoring.md](reference/hubspot-scoring.md). If HubSpot is unavailable — not installed, not connected, or erroring — do not stop. Say so plainly and run the "No HubSpot?" path at the bottom of this file: ask for a CSV export or a rough pasted list, and score that instead.
   - **Empty portal check.** If the pull returns zero contacts of any lifecycle stage, the portal is empty, not filtered wrong. Say so in one line, offer HubSpot's own setup (`manage_onboarding`, action `SET_GOAL`) or the "No HubSpot?" path, and do not diagnose lifecycle stages on a portal with nothing in it. The count is the test: `get_user_details` returns an `onboarded` flag, but a portal can report `onboarded: false` while holding hundreds of contacts, so the flag alone never decides this.

2. **Clarify if trigger is ambiguous.** If the user said only "pipeline" without a qualifier, ask: *"Quick pipeline overview (deal stages + total value) or prioritized call list?"* — then route accordingly. Do not score leads on a bare "pipeline."

3. **Score each lead.** Apply the four-dimension model in [reference/hubspot-scoring.md](reference/hubspot-scoring.md):
   - **Engagement** — email replies, opens, site visits in HubSpot (last 30 days only)
   - **Company fit** — industry and employee count vs. owner's ICP (default: any industry, 1–50 employees). Read these from the company associated with the lead, not from the contact record — see the scoring reference. When leads have no associated company and a lead-data connector (Apollo or Clay) is connected, the enrichment leg in the scoring reference fills industry and size from the lead's email domain. It is metered — say how many rows it would enrich and what that costs in credits, and run it only on the owner's yes for this run. Nothing enriched is written back to the CRM from here.
   - **Urgency** — lead age, stage duration, notes containing "urgent / ASAP / deadline / budget approved". The keyword check requires actually fetching note bodies via the contact → notes association — follow the "Fetch note bodies" section of the scoring reference; the note count alone cannot fire it.
   - **Recency penalty** — subtract points if last activity was <24 hours ago (already touched today)

   **Then check whether the scores actually separated.** If the highest and lowest composite differ by less than 10 points, the CRM has no signal to rank on. Do not present the order as a ranking — run the flat-score path in the scoring reference, say plainly that the signals are empty, and order by CRM facts instead. A false ranking sends the owner to call the wrong person.

4. **Build the ranked list.** Sort descending by composite score. Adapt list size to volume:
   - ≤10 leads → show all
   - 11–30 leads → show top 5
   - >30 leads → show top 8

   For each lead: name, company, score, one-paragraph talking point, last activity summary. If engagement signals are all >30 days old, flag: *"Engagement signals are stale — approach as cold outreach."*

5. **Offer follow-up drafts.** Ask: *"Draft follow-ups for any of these?"* If yes, write one email per selected lead in the owner's voice per [the shared voice profile](../../shared/voice-profile.md). If that file has no profile yet, follow its "When there is no sample" instruction — ask for three emails the owner was happy with; if they decline, draft plain and neutral and say the drafts are un-voiced. Never invent a personality. Show drafts; do not send. If Mail is unavailable, hand the drafts over in chat as subject plus body for the owner to paste — that is a complete outcome.

6. **Render the triage board as an artifact.** After the short chat answer — never instead of it — build an HTML page using the house artifact style (`../../shared/artifact-style.md`): a ranked table with each lead's composite score in mono, an urgency status pill per row (good / warn / critical), and a talking-points line under each lead. If the flat-score path fired, say so on the page and drop the pill colors to neutral.

7. **Offer calendar slots.** Ask: *"Propose call slots for any of these?"* If yes, check Calendar for open 30-minute windows in the next two business days (avoid slots with existing events ±15 min). Propose two options per lead. Never create calendar events without explicit owner approval. If Calendar is unavailable, ask the owner for two or three windows they can offer and use those instead of inventing times.

## Approval gates

- **Never send an email.** Draft only; owner sends from their inbox.
- **Never create calendar events until approved by the user.**
- **Never change lifecycle stage or mark a lead Unqualified** unless the owner explicitly asks.
- **Never include `Customer` or `Evangelist` lifecycle contacts** in the lead list.
- **If zero leads match the filter**, explain why and offer to check what lifecycle stages are in use — do not fabricate a list.

## Reference

- [reference/hubspot-scoring.md](reference/hubspot-scoring.md) — HubSpot field names, scoring weights, ICP defaults
- [reference/gotchas.md](reference/gotchas.md) — edge cases: stale data, zero leads, pipeline disambiguation, customer contamination
- [reference/examples/happy-path-triage.md](reference/examples/happy-path-triage.md) — worked output for a 7-lead list with draft and slot proposal

## Closing offer

End with one line on what the triage produced, then the most relevant next step with its trigger phrase — usually "call list" (`/call-list`) to add calendar blocks around the ranking. Up to two others when they fit: "write this outreach" (`outreach-composer`) or "update the CRM" (`crm-autopilot`). Never more than three, and never re-offer something the owner already declined this session.

## No HubSpot?

Paste or upload the lead list — a CSV export or even a rough list works. Scoring and talking points run the same; the ranked call list comes back as chat plus a file instead of writing to the CRM.

## Using a tool that isn't listed

The connectors named in this skill are the tested paths, not a wall. If the owner wants this flow to use a tool that isn't connected or listed, offer `build-connector` — it checks the connector directory first and connects through Zapier otherwise, never hand-building against a raw API. Once the connection exists, the tool joins this skill like any other optional connector, under the same approval gates.

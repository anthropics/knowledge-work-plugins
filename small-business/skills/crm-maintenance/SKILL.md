---
name: crm-maintenance
description: >
  Keeps HubSpot current without the owner opening it: creates and updates
  contacts and deals from email and calendar context, logs notes and calls,
  and flags stale records. The "stop doing data entry" skill. Use when the
  user asks to update the CRM, log a call, clean up HubSpot, or add context
  to a deal.
---

# CRM Maintenance

## Quick start

Pull context from the referenced email or calendar event, resolve the right HubSpot contact and deal, log the activity, and surface what changed. For a deal cleanup, audit the deal against recent email/calendar activity and propose updates — never apply them without approval.

```
User: "log this call to the Acme deal"
→ Read the most recent completed calendar event
→ Confirm attendees map to the Acme deal's contacts
→ Write a call activity on the Acme deal
→ Report: "Logged call to Acme Q2 Expansion. [deal link]"
```

## Workflow

1. **Identify intent.** Decide which of three paths applies from the user's message and context:
   - **Email path** — "update my CRM", "add this to the deal", or any reference to an email thread
   - **Call path** — "log this call", "log the meeting", or any reference to a calendar event
   - **Cleanup path** — "clean up HubSpot", "is this deal up to date", or any request to audit a specific deal
   If the intent is ambiguous (e.g. "update HubSpot" with no referenced email/meeting/deal), ask which path before proceeding.

2. **Gather context.**
   - Email path: read the thread (subject, participants, last 1–3 messages). Identify the primary external contact.
   - Call path: read the calendar event (title, attendees, time, description). If no event was specified, use the most recent completed meeting in the last 24 hours and confirm with the user before proceeding.
   - Cleanup path: pull the deal (stage, amount, close date, next-step, associated contacts, activities in last 60 days), plus the last 14 days of email threads and calendar events involving the deal's contacts.

3. **Resolve the HubSpot contact and deal.** For email/call paths:
   - Search HubSpot contacts by email address. If a contact is missing, create it from email signature or calendar invite data — announce creation in chat before writing.
   - Find the right deal in this order: (a) explicit match if the user named one, (b) the contact's sole open deal, (c) fuzzy match across the contact's open deals against the email subject or meeting title — confirm before writing, (d) ask the user if no match. **Never auto-create a deal.**
   - For field names, activity types, and association rules, read [reference/hubspot-fields.md](reference/hubspot-fields.md) before writing anything to HubSpot.
   - If deduplication or deal-resolution feels ambiguous, check [reference/gotchas.md](reference/gotchas.md) before proceeding — it covers the most common failure modes.

4. **Execute the action.**
   - Email path: write an email activity with the thread subject as the title and a concise summary (not the full thread) as the body. Timestamp to the latest message. For a worked example, see [reference/examples/log-email-happy-path.md](reference/examples/log-email-happy-path.md).
   - Call path: write a call activity with the event title, duration, and any notes available. Timestamp to the event start. For a worked example including a missing-contact scenario, see [reference/examples/log-call-happy-path.md](reference/examples/log-call-happy-path.md).
   - Cleanup path: walk each field per [reference/cleanup-checklist.md](reference/cleanup-checklist.md) and assemble a proposed-changes list. Show current → proposed side-by-side. Write only what the user approves. For a full worked example, see [reference/examples/cleanup-deal.md](reference/examples/cleanup-deal.md).

5. **Approval gate — every externally visible write.** For contact creation and activity logging, announce before writing and surface the result after. For cleanup edits, do not write anything until the user approves the specific changes.

6. **Report what happened.** Tell the user what was written and what's pending. Include a HubSpot link to the affected deal when possible. Keep it short.

## Approval gates

- **Never delete records.** Not contacts, not deals, not activities. If the user asks, say the skill cannot and direct them to HubSpot.
- **Never change deal stage or close a deal without explicit user approval.** Even if evidence is strong. Flag and defer.
- **Never create a new deal unprompted.** Ask if the right deal can't be resolved.
- **Announce contact creation before writing.** One line — lets the user catch typos or duplicates.
- **Side-by-side diffs for cleanup.** Show current value and proposed value; wait for approval per item.

## Reference

- [reference/hubspot-fields.md](reference/hubspot-fields.md) — activity types, field names, association rules used in this skill
- [reference/cleanup-checklist.md](reference/cleanup-checklist.md) — the fields checked during a deal cleanup and the evidence needed to flag each
- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for contact resolution, activity summaries, and cleanup proposals
- [reference/examples/log-email-happy-path.md](reference/examples/log-email-happy-path.md) — worked example: email to existing deal
- [reference/examples/log-call-happy-path.md](reference/examples/log-call-happy-path.md) — worked example: meeting to existing deal, missing contact
- [reference/examples/cleanup-deal.md](reference/examples/cleanup-deal.md) — worked example: stale deal audit

# Example: log a call with a missing contact

Worked scenario for the call path — calendar event has three attendees, one of them isn't in HubSpot yet.

## Setup

- User just finished a 30-minute Google Meet titled "Acme — technical deep dive" at 10:00am
- Attendees on the calendar invite: the user, `sarah.lin@acme.com`, `ben.rivera@acme.com`
- Sarah Lin is an existing HubSpot contact on the "Acme Q2 Expansion" deal
- Ben Rivera is NOT in HubSpot
- The Acme Q2 Expansion deal is the only open deal for Sarah

## User says

> "Log this call."

## Skill behavior

**Step 1 — Identify intent.**
Call path. No specific event named — falls back to the most recent completed meeting in the last 24 hours.

**Step 2 — Gather context.**
Finds the "Acme — technical deep dive" event from 10:00am. Confirms with the user before proceeding:

> *"Logging the 'Acme — technical deep dive' call from 10:00am this morning — correct?"*

User confirms.

Reads event details: 30 minutes, external attendees `sarah.lin@acme.com` and `ben.rivera@acme.com`. No description on the event.

**Step 3 — Resolve contact + deal.**
- Looks up `sarah.lin@acme.com` → exists (Sarah Lin, on Acme Q2 Expansion).
- Looks up `ben.rivera@acme.com` → does not exist.
- Announces contact creation:

> *"Ben Rivera (ben.rivera@acme.com) isn't in HubSpot. Creating the contact and associating to the Acme Q2 Expansion deal."*

Creates the contact with `email`, `firstname: Ben`, `lastname: Rivera`, `company: Acme` (inferred from email domain). Associates to the deal.

Deal resolution: Sarah's only open deal is Acme Q2 Expansion — unambiguous match.

**Step 4 — Execute.**
Writes a call activity on Acme Q2 Expansion:
- `hs_call_title`: Acme — technical deep dive
- `hs_call_body`: "Meeting held; notes to be added." (No description on the calendar event; placeholder surfaced to user so they know to add detail.)
- `hs_call_duration`: 30 min
- `hs_timestamp`: 10:00am today
- Associated contacts: Sarah Lin, Ben Rivera
- Associated deal: Acme Q2 Expansion

**Step 5 — Approval gate.**
Announced the contact creation before writing. Activity write is inline per the user's explicit "log this call" request.

**Step 6 — Report.**

> Logged call activity to Acme Q2 Expansion:
> *"Acme — technical deep dive" (30 min, 10:00am)*
> Created new contact: Ben Rivera (ben.rivera@acme.com) — associated to the deal.
> Call body is a placeholder — add your notes if you want them on the deal timeline.
> [HubSpot: Acme Q2 Expansion]

## What this example demonstrates

- Fallback to most-recent-meeting when the user doesn't specify an event
- Confirmation before acting on inferred context
- Contact creation with inferred company from email domain
- Placeholder body with user notification when no meeting notes exist
- Associating multiple contacts (existing + newly created) to the same activity

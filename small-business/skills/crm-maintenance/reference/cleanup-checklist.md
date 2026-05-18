# Cleanup checklist

The fields the `crm-maintenance` skill checks during a deal cleanup, plus the evidence needed to flag each. This runs when the user says "clean up HubSpot" or "is this deal up to date" scoped to a specific deal.

Work through every item. Present findings as a review list; write only what the user approves.

## 1. Last activity date

**Check:** Is the deal's `hs_lastactivitydate` older than the most recent real interaction (email or meeting) involving its associated contacts?

**Evidence to flag:** An email thread or calendar event in the last 14 days with one of the deal's contacts, newer than `hs_lastactivitydate`.

**Proposed action:** Offer to log the missing activity. Don't mark the deal itself; logging the activity updates `hs_lastactivitydate` automatically.

## 2. Next-step field (`hs_next_step`)

**Check:** Does the current `hs_next_step` still reflect what was agreed in the latest email or meeting?

**Evidence to flag:** The field says "send pricing" and a subsequent email shows pricing was sent. Or the field is blank and a recent meeting explicitly set a next action.

**Proposed action:** Propose a new value (or blank if the step is completed). Show current → proposed side-by-side.

## 3. Deal stage (`dealstage`)

**Check:** Do recent interactions suggest the deal has moved stage — e.g., proposal sent, contract signed, lost to a competitor?

**Evidence to flag:** Explicit language in email/meeting notes like "we're moving forward," "we signed," "we went with [competitor]," or a change in meeting cadence.

**Proposed action:** **Flag only — never change stage automatically.** Surface the evidence and let the user decide.

## 4. Close date (`closedate`)

**Check:** Has the latest email/meeting referenced a revised timeline that conflicts with the current `closedate`?

**Evidence to flag:** Phrases like "pushing to Q3," "we'll sign by end of month," or "delayed until next quarter."

**Proposed action:** Propose an updated date. Show current → proposed.

## 5. Amount (`amount`)

**Check:** Has the latest email/meeting mentioned a different deal size?

**Evidence to flag:** Explicit revised pricing in a pricing email, expanded scope in a meeting, or reduced scope the customer accepted.

**Proposed action:** Propose an updated amount. Show current → proposed.

## 6. Associated contacts

**Check:** Are there people on recent emails or meetings with the deal's contacts who aren't themselves associated to the deal?

**Evidence to flag:** An email CC or meeting attendee whose domain matches an existing deal contact's domain but who isn't on the deal.

**Proposed action:** Propose adding the missing contact(s) to the deal. Create the contact in HubSpot first if they don't exist yet.

## 7. Notes hygiene

**Check:** Are there notes or activities older than 90 days that explicitly contradict the current deal state?

**Evidence to flag:** A note saying "customer is lost" on a deal still in an open stage, or a note with an outdated contract amount.

**Proposed action:** Add a new note clarifying the current state — **never edit or delete** the old note. Append, don't rewrite history.

## Output format

Present findings as a numbered list, each item showing:
- What was flagged
- The evidence (email subject + date, or meeting title + date)
- The proposed action (or "flag only" for stage changes)

Then ask for approval item-by-item or bulk-approve. Write only what's approved.

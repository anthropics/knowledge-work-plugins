# Example: clean up a stale deal

Worked scenario for the cleanup path — user asks the skill to audit one specific deal, skill surfaces findings and waits for approval.

## Setup

- Deal: "Acme Q2 Expansion" — stage "Proposal Sent," amount $18K, close date May 15, next step "send pricing," `hs_lastactivitydate` 22 days ago
- Deal has two associated contacts: Sarah Lin and Ben Rivera
- Last 14 days of email with Sarah include an Apr 18 thread titled "Re: Acme pricing" where Sarah confirmed the pricing and said "we'll sign once our legal review wraps, should be mid-June"
- A calendar event on Apr 20 titled "Acme — legal review walkthrough" included a new person, `maria.chen@acme.com`, who is not in HubSpot and not on the deal
- No email, meeting, or note suggests the deal has moved stage

## User says

> "Clean up the Acme Q2 Expansion deal."

## Skill behavior

**Step 1 — Identify intent.**
Cleanup path, scoped to one named deal.

**Step 2 — Gather context.**
Pulls the deal record. Pulls email threads from the last 14 days involving Sarah and Ben. Pulls calendar events from the same window.

**Step 3 — Resolve.**
Deal explicitly named — no resolution needed. Contacts on recent emails/meetings: Sarah (on deal), Ben (on deal), Maria Chen (not on deal, not in HubSpot).

**Step 4 — Walk the cleanup checklist.**

Skill does NOT write anything yet. Produces this review list:

> **Cleanup review — Acme Q2 Expansion**
>
> **1. Last activity date.** Deal shows 22 days old. Newer activity found: Apr 18 email from Sarah ("Re: Acme pricing"), Apr 20 meeting ("Acme — legal review walkthrough"). Neither is logged to HubSpot.
> **→ Propose:** Log the Apr 18 email and the Apr 20 meeting as activities on this deal.
>
> **2. Next-step field.** Currently "send pricing." The Apr 18 email shows pricing was sent and confirmed by Sarah.
> **→ Propose:** `hs_next_step`: "send pricing" → "wait for legal review sign-off."
>
> **3. Deal stage.** Currently "Proposal Sent." No evidence of stage movement — Sarah said they'll sign *after* legal review. Stage is consistent with reality.
> **→ Flag only — no change.**
>
> **4. Close date.** Currently May 15. Sarah's Apr 18 email says "should be mid-June."
> **→ Propose:** `closedate`: May 15 → June 15.
>
> **5. Amount.** Currently $18K. Apr 18 email confirms 50 seats at $360 = $18K. No change needed.
> **→ No action.**
>
> **6. Associated contacts.** Maria Chen (`maria.chen@acme.com`) attended the Apr 20 legal review meeting. Not on the deal, not in HubSpot.
> **→ Propose:** Create the contact and associate to the deal.
>
> **7. Notes hygiene.** No conflicting notes found in the last 90 days.
> **→ No action.**
>
> Approve items 1, 2, 4, 6 to write? Or specify which ones.

**Step 5 — Approval gate.**
Waits for the user. User replies: *"Yes to all except 4 — leave close date alone, she might be optimistic."*

**Step 6 — Execute approved items.**
- Logs the Apr 18 email as an email activity
- Logs the Apr 20 meeting as a call activity with attendees Sarah, Ben, and (newly created) Maria
- Updates `hs_next_step` to "wait for legal review sign-off"
- Does NOT update `closedate`
- Creates Maria Chen contact and associates to the deal

**Report.**

> Wrote changes to Acme Q2 Expansion:
> - Logged Apr 18 email and Apr 20 call activities
> - Updated next step to "wait for legal review sign-off"
> - Created contact Maria Chen (maria.chen@acme.com) and added to deal
> Close date unchanged per your call.
> Deal stage was flagged as consistent with reality — no change needed.
> [HubSpot: Acme Q2 Expansion]

## What this example demonstrates

- Every field check from `reference/cleanup-checklist.md` applied to one deal
- Side-by-side current → proposed framing for every proposed change
- Stage change correctly held as flag-only
- User selectively approves items — skill honors the exact selection
- Contact creation folded into the same approval cycle

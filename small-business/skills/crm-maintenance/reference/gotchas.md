# Gotchas

Edge cases where the `crm-maintenance` skill is most likely to produce bad CRM data. Each entry uses the Good / Bad pattern.

---

## Gotcha: Creating a duplicate contact when the email is already in HubSpot under a different case

**Why it matters:** HubSpot dedupes on exact email match. `Sarah.Lin@acme.com` and `sarah.lin@acme.com` are treated as distinct, but an owner who already created one will see a silent duplicate appear. That destroys the owner's trust in the skill.

### ✗ Bad

> Searched HubSpot for `Sarah.Lin@acme.com` — no match. Creating new contact: Sarah Lin (Sarah.Lin@acme.com).

New contact is created; owner's existing `sarah.lin@acme.com` contact now has a duplicate.

### ✓ Good

> Searched HubSpot for `sarah.lin@acme.com` (case-insensitive) — no match. Creating new contact: Sarah Lin (sarah.lin@acme.com). Announcing before write.

Always normalize email to lowercase before lookup. Announce the creation so the owner can catch misses.

---

## Gotcha: Writing the full email thread as the activity body

**Why it matters:** HubSpot activities are signal surfaces for fast scanning, not a transcript archive. A 12-message thread pasted into the activity body is useless; a three-sentence summary of what was agreed is actionable.

### ✗ Bad

> **Activity body:**
> *From: Sarah Lin — Thu Apr 9…*
> *Hi! Following up on our call, here are the specs we discussed…*
> *[1,200 more words]*

Owner scrolls past it every time.

### ✓ Good

> **Activity body:** Sarah confirmed scope for Q2 expansion — 50 seats, $18K ACV, start date June 1. She'll send the signed SOW by Friday. No open questions.

Summary names the decisions, the numbers, and the next step.

---

## Gotcha: Auto-creating a deal when the right one can't be resolved

**Why it matters:** Duplicate deals are very hard to untangle in HubSpot — they split activity history, confuse reporting, and the owner usually notices weeks later when a forecast looks wrong.

### ✗ Bad

> No open deal found for Sarah Lin at Acme. Creating new deal: "Acme — new opportunity" and logging the call to it.

Now there are two Acme deals and the owner has no idea which one is real.

### ✓ Good

> No open deal found for Sarah Lin at Acme. Which deal should I log this to? Options: (1) Acme Q2 Expansion (closed-won Feb), (2) Acme Renewal 2027 (open). Or do you want to skip logging for now?

Ask. Never create a deal on behalf of the owner.

---

## Gotcha: Proposing a deal stage change based on email language

**Why it matters:** "We're moving forward" in an email doesn't always mean "advance to closed-won." Customers say it when they're moving forward with evaluation, or with a procurement step. Owners have context the skill doesn't. Auto-advancing stage is destructive to the pipeline.

### ✗ Bad

> Email from Sarah says "we're moving forward." Proposing `dealstage` → Closed Won. Writing now.

### ✓ Good

> Flagging: the Apr 18 email from Sarah ("we're moving forward with the Anthropic evaluation") may indicate stage movement. Current stage is "Proposal Sent." Do you want to advance it? I won't change stage without your explicit go-ahead.

Surface the evidence, hold the write.

---

## Gotcha: Overwriting an owner-set next-step during cleanup

**Why it matters:** The owner may have set a next step that reflects context the skill can't see — a phone call, a Slack thread, a private note. Overwriting it because a recent email suggests something different erases real work.

### ✗ Bad

> `hs_next_step` currently says "wait for legal review." Latest email from Sarah says "let's schedule pricing review." Updating `hs_next_step` to "schedule pricing review."

### ✓ Good

> `hs_next_step` currently reads "wait for legal review" (set by you 3 days ago). The Apr 19 email from Sarah suggests a pricing review is also needed. Propose appending or replacing? Current → Proposed: "wait for legal review" → "wait for legal review; then schedule pricing review." Approve?

Show the current value, propose the change explicitly, wait for approval.

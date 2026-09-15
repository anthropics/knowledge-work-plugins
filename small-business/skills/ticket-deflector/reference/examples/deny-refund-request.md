# Example: Refund request outside policy — declined, alternative offered

**Scenario:** A long-standing customer is angry. She wants a refund on an item bought fourteen months ago. The written policy allows returns for 60 days. The item is still covered by a two-year manufacturer warranty. The owner forwards the email and says "answer this one, she's a good customer."

This is the harder case. The reply says no, and it still has to keep the customer.

---

## Customer email (forwarded)

> **Subject:** This is ridiculous
>
> I have bought from you for four years and spent thousands. The stand mixer I got from you has started making a grinding noise and now it barely turns. I want my money back. I am not paying to fix something that should not have broken in the first place.
>
> — Deb Whitaker

---

## Step 2 — PayPal lookup result

Found 1 transaction matching deb.whitaker@email.com:

- **Transaction ID:** PP-5512-XXXX
- **Amount:** USD 329.00
- **Date:** 2025-05-14 (14 months ago)
- **Status:** Completed
- **Refund issued:** No

---

## Step 3 — HubSpot lookup result

Contact found: Deb Whitaker (deb.whitaker@email.com)
- Lifecycle stage: Customer
- Prior orders: 11
- Notes: "Repeat customer since 2022. Referred two others."

---

## Step 4 — Policy check (the step that decides this reply)

Read before drafting:

- **Refund policy:** returns and refunds accepted within 60 days of purchase, item unused or defective on arrival. Fourteen months is well outside it.
- **Help-centre article "Appliance warranty claims":** stand mixers carry a two-year manufacturer warranty covering motor and gearbox failure. The business files the claim on the customer's behalf; the manufacturer ships a repair or a replacement unit.

So: the refund she asked for is not available, and a real remedy that costs her nothing is.

**What not to do here.** Do not draft a refund because she is a good customer and the email is angry. Eleven orders is a reason to handle her carefully, not a reason to invent an exception the owner never wrote. If the owner wants to make an exception, that is the owner's call, made after reading the draft.

---

## Step 5 — Draft reply (presented to owner for review)

> **Subject:** Re: This is ridiculous
>
> Hi Deb,
>
> A grinding motor at fourteen months is not what should happen, and I'm sorry you're dealing with it.
>
> Straight answer on the refund: our returns window is 60 days, so I can't refund the mixer. What I can do is better than it sounds — that model has a two-year manufacturer warranty that covers exactly this, motor and gearbox. I file the claim for you, you don't pay anything, and they either repair it or send a replacement unit.
>
> If you can send me a short video of the noise it's making, I'll open the claim today. Usual turnaround is about two weeks.
>
> [Owner name]
>
> *[Note: Refund declined per the 60-day policy. Warranty claim offered per the appliance warranty article. If you want to make an exception for her, tell me and I'll redraft.]*

Three things the draft does: it says no early and plainly, it gives the reason once without apologising for the policy twice, and it lands on the thing she can actually do next.

---

## Step 6 — Owner reviews

The owner replies: "Good. Send it, and if the claim gets denied I'll eat the repair cost."

That second half is a new commitment the owner just made. It does not go in this email — it goes in the notes, so it is there if the claim is denied.

---

## Step 7 — Refund approval prompt

Skipped. No refund is being issued, so no refund prompt is shown. Never show a refund confirmation for a declined request; it invites an accidental yes.

---

## Step 8 — Send + HubSpot note

Reply sent via Gmail.

HubSpot note logged on Deb Whitaker's contact:
> "Ticket Deflector — 2026-07-27: Refund requested on PP-5512-XXXX (USD 329, 14 months old). Declined — outside 60-day window. Offered manufacturer warranty claim (motor/gearbox, 2-year). Awaiting video from customer. Owner has agreed to cover repair cost personally if the warranty claim is denied."

---

## Step 9 — Report

> Reply sent to Deb Whitaker · Refund declined, outside the 60-day window · Warranty claim offered, waiting on her video · HubSpot note logged, including your offer to cover the repair if the claim fails.

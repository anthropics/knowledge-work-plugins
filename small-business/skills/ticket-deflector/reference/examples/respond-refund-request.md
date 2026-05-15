# Example: Refund request — PayPal transaction found

**Scenario:** A customer emails saying their product arrived damaged and they want a full refund. The owner forwards the email and says "answer this customer."

---

## Customer email (forwarded)

> **Subject:** Damaged product — need refund
>
> Hi, I ordered a cutting board set last month and it arrived cracked. I'd like a full refund please. My order number is PP-3847-XXXX.
>
> — Sarah M.

---

## Step 2 — PayPal lookup result

Found 1 transaction matching sarah.m@email.com:

- **Transaction ID:** PP-3847-XXXX
- **Amount:** $64.00
- **Date:** 2026-03-28
- **Status:** Completed
- **Refund issued:** No

---

## Step 3 — HubSpot lookup result

Contact found: Sarah M. (sarah.m@email.com)
- Lifecycle stage: Customer
- Prior orders: 2
- Notes: "Returning customer — sent holiday promo Dec 2025."

---

## Step 4 — Draft reply (presented to owner for review)

> **Subject:** Re: Damaged product — need refund
>
> Hi Sarah,
>
> So sorry to hear your cutting board set arrived cracked — that's definitely not okay. I've pulled up your order and I'm issuing a full refund of $64.00. You should see it back on your original payment method within 3–5 business days.
>
> Thanks for letting me know, and I appreciate your patience. Really sorry about this.
>
> [Owner name]

---

## Step 5 — Owner approves draft (no edits)

---

## Step 6 — Refund approval prompt

> *"Issue refund of $64.00 to Sarah M. (sarah.m@email.com) for transaction PP-3847-XXXX? Reply Y to proceed."*

Owner replies: **Y**

→ Refund issued via PayPal.

---

## Step 7 — Send + HubSpot note

Reply sent via Gmail.

HubSpot note logged on Sarah M.'s contact:
> "Ticket Deflector — 2026-04-23: Customer reported damaged product. Full refund of $64.00 issued via PayPal (PP-3847-XXXX). Reply sent via email."

---

## Step 8 — Report

> Reply sent to Sarah M. · Refund of $64.00 issued (PP-3847-XXXX) · HubSpot note logged.

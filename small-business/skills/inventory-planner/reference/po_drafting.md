# PO Drafting and Vendor Emails

Turning an approved buy list into documents, and the gate in front of both.

---

## The gate

A purchase order commits the owner's money and a vendor email goes out under their name. Neither happens without an explicit yes.

State before asking:

> Ferguson: 8 items, 640 units, USD 4,180. Watsco: 3 items, USD 2,290.
> Total USD 6,470 across two POs. Draft them?

**The dollar total goes before the question.** The owner is deciding about cash, and units alone do not tell them what they need to know.

Approve per vendor, not per buy list. An owner may want the Ferguson order today and the Watsco one next week, and forcing an all-or-nothing yes gets a no.

---

## Purchase order structure

One PO per vendor. Standard contents:

- PO number, following the owner's existing numbering if they have one — ask rather than starting a new series
- Date, and the requested delivery date based on lead time
- Ship-to and bill-to
- Line items: SKU, description, quantity, pack or unit of measure, unit price, extended price
- Subtotal, expected freight, total
- The owner's terms, payment method, and contact

**Use the last known price per item and say when it is from.** A price from four months ago is fine to work with; a price presented as current when it is not sets up a variance argument later. When there is no known price, leave it blank rather than guessing — the vendor will price it.

---

## Vendor email

Read the shared voice profile at `../../../shared/voice-profile.md` before writing. These go out under the owner's name to people they have real relationships with, and a message that sounds like software damages that.

Keep it short. The useful content is:

- What is being ordered, or a reference to the attached PO
- When they need it by, and why if the timing is tight
- Any question — availability, a substitution, a price check
- How the owner wants confirmation

What to avoid: apologizing for ordering, over-explaining, and any pleasantry the owner would not actually write.

**A price question is worth including when the last known price is stale.** Asking "is this still USD 14.80 a case?" costs one line and prevents the variance that `ap-processor` would otherwise flag when the bill arrives.

---

## Substitutions and backorders

When a vendor comes back with a substitution or a partial:

- Recompute days of cover on what is actually coming, not what was ordered
- Report the gap and whether it changes the stockout date
- Never accept a substitution on the owner's behalf. A different part number is a decision about what goes on a customer's job

---

## Handoff to AP

When QuickBooks or NetSuite is connected, approved POs go into the ledger so `ap-processor` can run the three-way match when the bill arrives. That closes the loop: what was ordered, what showed up, what was billed.

When they are not connected, keep the POs as files and tell the owner they are the matching record. A PO nobody can find later is a PO that cannot catch an overbilling.

---

## Calendar rhythm

With Google Calendar connected, offer a recurring block for the restock review — weekly or biweekly, depending on lead times.

This works far better as a rhythm than as an emergency. An owner who looks at the buy list every Tuesday for twenty minutes rarely stocks out. One who looks when a customer asks for something already has the problem.

Offer once. If they decline, do not ask again.

---

## Worked example

Ray's June order, after approval.

**PO 2041 — Ferguson Supply**, requested 6/12
- 240 ea, Merv 11 filter 20x25x1, USD 3.70 ea, USD 888.00
- 24 ea, 45/5 capacitor, USD 11.40 ea, USD 273.60
- 6 ea, contactor 2-pole 30A, USD 18.90 ea, USD 113.40
- Subtotal USD 1,275.00, freight per usual terms

Email drafted to Ray's rep, three sentences, asking whether the filter price still holds and confirming the Thursday delivery. Held for Ray's approval before sending.

# Matching and Exceptions

The three-way match, and how to word what it finds.

---

## What matches what

| Document | Answers |
|---|---|
| Purchase order | What was ordered, at what price |
| Receiving ticket or packing slip | What actually showed up |
| Vendor bill | What is being charged |

A clean three-way match means all three agree within tolerance. That bill needs no attention beyond a glance.

Many small businesses do not issue POs. **Absence of a PO is not an exception** — it is the normal state for a lot of the bills that come through here. Note it and move on. Only treat a missing PO as a problem when the owner has said they require POs above a dollar threshold.

---

## Tolerances

Ask the owner once and remember the answer. Sensible defaults when they have no policy:

- **Price variance:** flag above 2% or USD 25 per line, whichever is larger
- **Quantity variance:** flag any overage at all
- **Freight and fuel surcharges not on the PO:** flag above USD 50
- **Total variance:** flag above 1% of PO value

The asymmetry is deliberate. Being billed for more units than arrived is theft or error every time; a small price move is often just a market.

---

## Exception types and how to say them

Each exception gets the vendor, the invoice number, both numbers, and the dollar impact. Vague exceptions get ignored.

**Price above PO**
> Ferguson inv 88231, line 2: billed USD 1,240 per unit, PO says USD 1,160. Two units. USD 160 over.

**Billed more than received**
> Johnstone inv 4471: billed 12 filters, receiving ticket shows 8. USD 84 over. Nothing was signed for the other 4.

**Received but never billed**
> Receiving ticket 2201 from Ferguson, 3/14, has no matching bill. Either it is coming or it was missed. Worth knowing before the month closes.

**Billed, never received**
> Grainger inv 55019 for USD 612. No receiving record. Ask whether this shipped.

**Duplicate**
> Ferguson inv 88231 appears twice — emailed 3/2 as a PDF and again on the March statement. Same invoice number. One of them is a copy.

**Unreadable field**
> Photo of a Watsco invoice, total unreadable from glare. Vendor and date are clear. I need the total before this can be staged.

---

## Statements

Vendor statements are for finding gaps, not for creating entries.

Reconcile the statement's open items against what is in the ledger:

- On the statement, not in the books → a bill the owner never received. Ask the vendor for a copy.
- In the books, not on the statement → often already paid and applied. Confirm before chasing.
- Amounts disagree → a credit memo or a partial payment is usually the reason.

**Never create a bill from a statement line.** A statement line has no invoice detail, no line items, and no tax breakdown. Entering one produces an entry nobody can audit later.

---

## Escalation

Some exceptions are the owner's problem and some are the vendor's. Sort them before presenting:

- **Owner decides:** coding questions, whether to accept a price increase, whether to short-pay
- **Vendor must answer:** quantity shorts, missing invoices, charges for undelivered goods
- **Bookkeeper handles:** prior-period corrections, anything already closed

Draft the vendor-facing message for the second bucket, but it does not send without approval. See `payment_run.md` for how disputes interact with a scheduled payment.

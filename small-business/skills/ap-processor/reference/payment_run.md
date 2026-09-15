# Payment Run

Proposing what to pay, and the gate in front of it.

---

## The gate

Staging coded bills and proposing a payment are two separate approvals with two separate questions.

1. **Coding gate:** "Stage 19 bills totaling USD 41,208 as unpaid bills in QuickBooks?"
2. **Payment gate:** "Pay these 11 bills, USD 22,140 out of the operating account on Thursday?"

Collapsing these is the single worst thing this skill could do. An owner who says yes to bookkeeping has not said yes to money leaving. Ask twice, always, even when the owner says to just handle it — and if they do say that, explain once why the second question still gets asked.

**State the total before the question, not after.** The dollar amount is what the owner is actually deciding.

---

## Building the proposal

Order bills into the run by this logic:

1. **Already late** — anything past due, with how late and any relationship risk noted
2. **Early-pay discount worth taking** — 2/10 net 30 on a USD 10,000 bill is USD 200 for paying 20 days early. Show the dollar value, not the terms code
3. **Due within the run window** — normally the next 7 to 14 days
4. **Everything else** — hold

Exclude automatically:

- Bills with unresolved exceptions
- Bills with a low-confidence total
- Anything already paid by card through Ramp or Expensify
- Bills in active dispute

Say what was excluded and why. A silently dropped bill becomes a late bill.

---

## Cash awareness

When `cash-flow-snapshot` data is available, show the balance after the run and whether payroll still clears. When it is not available, say that plainly rather than implying the run is affordable.

If the proposed run would take the balance below the owner's stated floor, say so before asking, and offer a trimmed version. Do not just present a smaller run without explaining what was held back — the owner needs to know a vendor is waiting.

---

## Payment methods

Group by how each vendor gets paid: ACH, check, card, or vendor portal. The owner executes the payment in their bank or ledger; this skill stages and proposes.

**No payment is ever initiated here.** Even where a connector technically allows it, the owner presses the button. That boundary is worth more than the two minutes it saves.

---

## Short pays and disputes

When the owner wants to pay part of a bill:

- Record the amount being paid and the amount held
- Draft the note to the vendor explaining the short pay, with the invoice number and the specific line — read the shared voice profile at `../../../shared/voice-profile.md` before writing it
- Hold the note for approval
- Keep the disputed balance visible in aging so it does not quietly age into a collections call

---

## Worked example

Ray's Thursday run, proposed:

- 11 bills, USD 22,140 total
- 2 past due: Johnstone USD 1,880 (18 days), Ferguson USD 940 (7 days)
- 1 discount available: Watsco USD 6,200 at 2/10, worth USD 124 if paid by Friday
- 3 held: two with quantity variances, one with an unreadable total
- Balance after run, per the cash snapshot: USD 31,400, payroll of USD 18,900 clears on the 15th

Asked as: "That's USD 22,140 out on Thursday, leaving USD 31,400 against an USD 18,900 payroll on the 15th. Send it?"

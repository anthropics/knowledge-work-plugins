# Absent is not zero

The single most common way these skills produce a confident wrong answer.

Every defect below shows up against a real connector, not against
fixtures, and the reason is structural: **fixtures are complete by
construction, and real data is full of holes.** A hole reads as good news unless
the skill is told otherwise.

---

## The shape of it

A field comes back empty, zero, truncated, or untracked. The skill reads that as
a fact about the business rather than a fact about the data. The answer that
comes out is clean, confident, and wrong in the direction that hides the
problem — which is the worst direction, because nothing looks like it needs
checking.

| What the data did | What the skill concluded | What was true |
|---|---|---|
| Aging report truncated to top 10 | Receivables total USD 25,907 | USD 37,055, and the only 91-day debt was missing |
| P&L summary omitted expenses | Zero expenses, 100% gross margin | USD 984,591 of expenses in the rows below |
| Reply timestamp dated in the future | Hottest lead in the pipeline | Corrupt record, no recent contact at all |
| Activity date absent on a deal | Deal is fresh, pipeline is clean | Never touched by anyone, ever |
| Label search by ID returned nothing | No leads in the inbox | 201 real inquiries under that label |
| Inventory tracking off for a variant | Product nobody buys, never reorder | Best-selling coffee in the catalogue |
| Four older payrolls unprocessed | One payroll due | Four periods where nobody got paid |
| Revenue field returned `0.0` | Company earns nothing | Data provider has no figure for it |
| Processor balance `available: 0` | No money at this processor | USD 3,071 pending, landing in two days |

Nine instances, nine different connectors, one mistake.

---

## The rule

**Before reporting any figure, ask what would make it look like this if the
business were fine, and what would make it look like this if the data were
broken. If you cannot tell the two apart, say so instead of picking one.**

Concretely, in order of how often it bites:

1. **A constrained or paginated call describes its own slice, never the whole.**
   Totals come from an unconstrained source — a balance-sheet line, a full count —
   or they are labelled as partial. Never present a top-N summary as a book total.

2. **A summary object is a convenience, not a source.** When a payload offers
   both a summary and the rows it was computed from, total the rows. Several
   connectors ship summaries that contradict their own rows.

3. **Zero and absent are different facts, and most APIs conflate them.** A
   revenue of `0.0`, an empty date, a `null` count — decide which is plausible.
   A company with no revenue is rare; a data provider with no figure is common.
   When zero is implausible, read it as unknown and say unknown.

4. **Empty is not fresh.** A record with no activity date has never been touched,
   which is the worst case rather than the healthiest. Date comparisons silently
   exclude empty fields, so the records in most trouble drop out of the very list
   built to find them. Rank absent above the oldest date, and name it differently.

5. **A date later than today is corrupt.** Recency scoring reads it as maximally
   recent, so bad records float to the top. Compare every date against today
   before scoring it, and treat anything in the future as empty.

6. **An empty result and a failed query look identical.** Cross-check before
   reporting nothing: if a label search returns zero but the label reports
   messages, the query is wrong, not the mailbox. "No results" is a claim about
   the business and deserves the same scrutiny as any other.

7. **One count disagreeing with another is a finding, not a rounding error.**
   When two endpoints describe the same thing and differ by an order of
   magnitude, one of them is measuring something else. Say which you used and
   why, rather than picking silently.

---

## Saying it well

The owner does not need the mechanism. They need to know which numbers to trust.

> *"Your books show USD 37,055 owed across 20 customers. One account, Pearl Street
> Bistro, is 91 days late at USD 467 — that is the only genuinely old debt."*

Not "receivables are USD 25,907," which was true of the slice and false of the
business.

> *"Shopify's inventory report shows far fewer units sold than its sales report,
> so tracking looks switched off on most variants. I used the sales figures for
> velocity and the inventory figures only for stock on hand."*

One sentence, and the owner knows exactly how much to trust the number.

When something genuinely cannot be determined, say that and stop. **A named gap
is useful. A fabricated zero is worse than silence**, because the owner acts on
it — and these outputs get forwarded to banks, boards and accountants.

---

## Connector-specific instances

The detail lives with the connector it belongs to:

- `quickbooks-report-traps.md` — summary objects contradicting their own rows
- `gmail-inbox-traps.md` — label queries, machine noise, and credentials

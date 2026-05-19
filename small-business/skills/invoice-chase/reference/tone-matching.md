# Tone Matching

Scoring logic and email tone guidelines for invoice-chase.

## Scoring

Score each customer using QuickBooks payment history for the last 12 months. Require a minimum of 3 invoices to score; fewer than 3 defaults to `occasionally-late`.

| Score | Criteria |
|---|---|
| `good-payer` | Paid on time or early in ≥ 75% of invoices |
| `occasionally-late` | Paid late in 25–50% of invoices, or fewer than 3 invoices on record |
| `repeat-late` | Paid late in > 50% of invoices |

"On time" means payment received on or before the invoice due date.

## Tone by score

| Score | Tone | Character |
|---|---|---|
| `good-payer` | Gentle | Friendly, assumes oversight. Opens with grace. |
| `occasionally-late` | Neutral | Professional, no judgment. Factual follow-up. |
| `repeat-late` | Firm | Direct, states a deadline. No warmth, no accusation. |

## Subject lines

- Gentle: `Quick reminder: Invoice #[N] for $[amount]`
- Neutral: `Following up: Invoice #[N] — $[amount] past due`
- Firm: `Past due notice: Invoice #[N] — $[amount] ([X] days overdue)`

## Body structure (all tones)

Every reminder includes: invoice number(s), total amount due, original due date, days overdue, and payment link or instructions.

Tone-specific additions:
- **Gentle**: one acknowledgment sentence ("I know things get busy")
- **Neutral**: none — facts only
- **Firm**: one deadline sentence ("Please remit by [date]")

One call to action per email. Never two.

## Consolidation rule

If a customer has multiple overdue invoices, combine into one email. List each invoice (number, amount, due date), then state the combined total. Use the customer's score, not the most overdue invoice's score.

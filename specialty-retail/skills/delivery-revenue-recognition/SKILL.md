---
name: delivery-revenue-recognition
description: >
  ASC 606-compliant revenue recognition for deposit-at-sale, recognize-at-delivery
  transactions. When a customer puts a deposit down weeks or months before
  delivery, that deposit is a liability (Customer Deposits), not revenue. This
  skill identifies invoices stuck in deposit state, generates the JEs that
  recognize revenue + sales tax + COGS at delivery, and flags deposits aged
  past a configurable threshold (default 180 days) for review. Use when the
  user says "recognize the revenue", "what's stuck in customer deposits",
  "ASC 606", "deposit posting", or "delivered but not invoiced".
compatibility: "Requires QuickBooks (or any GL with a Customer Deposits liability account) + a sales-order / invoice system that tracks deposit_at_sale and delivered_at timestamps separately."
---

# Delivery Revenue Recognition

ASC 606-compliant revenue recognition for the deposit-at-sale, recognize-at-delivery business model. This is the standard pattern for any large-ticket item where the customer pays before taking delivery:

- Hot tubs, swim spas, saunas (4–12 week order-to-delivery)
- Custom furniture (6–8 week production lead times)
- Powersports / RV / boats (factory-build orders)
- Appliances (special-order kitchens)
- Pre-sold inventory ordered to a customer specification

## Why this matters

Generic SMB accounting tools recognize revenue when the customer pays. Under ASC 606, **revenue is recognized when the performance obligation is satisfied** — for tangible-goods delivery, that's when the customer takes possession.

The wrong way:
```
Customer pays $5,000 deposit on April 1
→ Books show $5,000 revenue + $413 sales tax on April 1
→ Unit delivers June 15 — books already recognized it
→ April P&L overstated, June P&L understated
→ Sales tax remitted in April based on overstatement
→ If unit never delivers (customer cancels): revenue must be reversed, sales tax refunded
```

The right way:
```
Customer pays $5,000 deposit on April 1
→ DR Bank $5,000 / CR Customer Deposits (liability) $5,000
→ Unit delivers June 15
→ DR Customer Deposits $5,000 / CR Revenue $4,587 / CR Sales Tax Payable $413
→ DR COGS / CR Inventory at delivery (separate JE)
→ Revenue recognized in the month of delivery, sales tax remitted on that month's filing
```

This skill identifies which invoices need the delivery JE and produces it.

## Workflow

### Step 1 — Pull invoices in deposit state

For each invoice with a deposit applied but the unit not yet delivered:

```sql
SELECT
  i.id,
  i.invoice_number,
  i.customer_id,
  c.name AS customer_name,
  i.invoice_date,
  i.total,
  i.balance_due,
  so.id AS sales_order_id,
  so.delivered_at,
  so.status AS so_status,
  SUM(p.amount) AS deposit_applied,
  CURRENT_DATE - i.invoice_date AS days_open
FROM invoices i
JOIN sales_orders so ON so.id = i.sales_order_id
LEFT JOIN payment_applications pa ON pa.invoice_id = i.id
LEFT JOIN payments p ON p.id = pa.payment_id
JOIN customers c ON c.id = i.customer_id
WHERE so.status IN ('sold', 'awaiting_delivery', 'partial')
  AND so.delivered_at IS NULL
  AND i.status IN ('open', 'partial')
GROUP BY i.id, c.name, so.id;
```

Equivalent QuickBooks query: invoices linked to sales orders, with status not "Delivered" and at least one received payment.

### Step 2 — Split into action buckets

| Bucket | Criteria | Action |
|---|---|---|
| **Ready to recognize** | so.delivered_at IS NOT NULL AND no delivery JE posted | Generate delivery JE (Step 3) |
| **Awaiting delivery** | so.delivered_at IS NULL AND days_open ≤ 180 | Hold — deposit correctly in liability |
| **Aged for review** | days_open > 180 AND so.delivered_at IS NULL | Flag for user review |
| **Stuck / orphaned** | so.status='cancelled' AND deposit still applied | Flag — needs refund or reclassification |

The "aged for review" threshold defaults to 180 days. Configurable per-dealer (some categories have factory lead times that exceed this naturally — RV custom builds can run 9+ months).

### Step 3 — Generate the delivery JE for each "ready" invoice

For each invoice in the "ready to recognize" bucket:

```
Date: <so.delivered_at>
Description: Revenue recognition — Invoice #<number>, Customer <name>, delivered <date>

DR  Customer Deposits (2410 or similar)               <deposit_applied>
DR  Accounts Receivable (1200)                         <balance_due if any>
  CR Revenue — <product category> (4010/4020/etc.)    <invoice subtotal>
  CR Sales Tax Payable (2200)                          <sales tax amount>
```

Separately, post COGS at delivery if your inventory method requires it:

```
DR  COGS — <product category> (5010/5020/etc.)         <unit cost>
  CR Inventory — <product category> (1210/1220/etc.)   <unit cost>
```

Show the proposed JEs to the user **before posting**. Group multiple deliveries from the same date into one batch for approval but post them as separate JEs (one per invoice) so the audit trail stays clean.

### Step 4 — Apply approved JEs

After the user approves a batch, post via the GL connection. Record the JE IDs back on the invoice in a `recognition_je_id` field if the schema supports it; otherwise note it in the JE description for traceability.

### Step 5 — Handle the "aged for review" bucket

For deposits aged past the threshold without delivery:

For each flagged invoice, surface:
- Customer name and contact
- Invoice number, deposit amount, days open
- Sales order status, expected delivery date if set
- Last activity (last payment, last note, last contact)

Present as a watchlist. Common dispositions:
- **Factory lead time** — confirm with the customer, update the sales order delivery ETA, leave the deposit in liability
- **Customer abandoned the order** — start a refund process (separate skill or manual) and reclassify the deposit if non-refundable
- **Lost track / book error** — investigate; may need a corrective JE

Do **not** auto-recognize aged deposits as revenue without a delivery event. That would be both ASC 606 non-compliant and a real audit risk.

### Step 6 — Handle the "stuck / orphaned" bucket

For cancelled sales orders with applied deposits still showing:

If the deposit was refunded:
```
DR  Customer Deposits     <amount>
  CR Bank                  <amount>
```

If the deposit was kept as a forfeiture per a signed contract clause:
```
DR  Customer Deposits     <amount>
  CR Other Income — Forfeitures (4090 or similar)  <amount>
```

Both require user approval. Forfeiture is also potentially taxable as ordinary income — flag for CPA review on amounts over $1,000.

### Step 7 — Output summary

```
Delivery Revenue Recognition — [scope]

Ready to recognize:    N invoices, $XXX,XXX revenue + $X,XXX sales tax
Awaiting delivery:     N invoices in deposit (correctly held)
Aged > 180 days:       N invoices for review ($XX,XXX total)
Stuck / cancelled:     N invoices with leftover deposits ($X,XXX total)

Proposed JEs (ready batch):
  [list of JEs with DR/CR detail]

Awaiting your approval to post. Reply 'approve all', or specify which to post.
```

## Approval gates

- **Never auto-post.** Always present proposed JEs and wait for explicit approval.
- **Never recognize revenue without a delivery event.** Aged deposits stay in liability until delivery, refund, or forfeiture per signed contract.
- **Never plug the difference.** If deposit_applied doesn't equal invoice total exactly (off by sales tax handling, deposit overpayment, etc.), surface the discrepancy and ask.
- **Flag forfeitures over $1,000 for CPA review.** Forfeiture income has tax implications.
- **Closed-period awareness.** Don't post into a closed period. If delivery date falls in a closed period, the JE must be approved as a prior-period correction.

## Graceful degradation

| Missing piece | Fallback |
|---|---|
| No sales_orders.delivered_at field | Ask user to provide a delivery list (invoice # + delivery date) |
| Customer Deposits account not in CoA | Recommend setting up a current liability account (typical CoA code 2410) |
| Sales tax handling unclear | Ask user how their state recognizes tax (some states tax on deposit, some on delivery) |
| Inventory method unclear | Skip the COGS JE if user can't confirm method; flag for follow-up |

## Reference

- `reference/asc-606-summary.md` — Plain-English ASC 606 for SMB dealers (not legal advice)
- `reference/state-sales-tax-timing.md` — Which US states tax at deposit vs delivery (TX, CA, NY, FL, etc.)
- `reference/cancelled-order-handling.md` — Refund vs forfeiture mechanics
- `reference/examples/hot-tub-delivery.md` — Worked example: April deposit → June delivery for a Hot Spring Grandee

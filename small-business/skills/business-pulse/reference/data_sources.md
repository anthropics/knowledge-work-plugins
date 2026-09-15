# Data Sources

Exact mapping from each pulse section to the MCP tool that produces it. **Dispatch all calls in a single parallel batch** — do not pull serially.

## Cash & Finance (the ledger)

Whichever ledger is connected feeds this section — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books, as peers (`../../../shared/connector-neutrality.md`). The QuickBooks table is first only because it is the longest; the Xero, NetSuite, MYOB, and Zoho Books tables below map the same metrics. Amounts carry the business's currency code (`../../../shared/currency-and-locale.md`); thresholds are in that currency.

### QuickBooks

| Metric | Tool | Notes |
|---|---|---|
| Cash / bank balance | `cash_flow_quickbooks_account` | Current balance; show delta vs. prior week if available |
| MTD revenue | `profit_loss_quickbooks_account` | Current month vs. prior month. Read income and expenses from the report rows or `monthlyBreakdown`; the response's top-level `totalExpenses`, `grossProfit`, and `grossProfitMargin` report 0 / 100% against real rows (a defect in the response shape), so never read them |
| Outstanding receivables | QuickBooks invoice list | Filter to open/unpaid |
| AR aging | QuickBooks invoice list | Group by days since due: 0–30, 31–60, 61+ |
| Overdue invoices | QuickBooks invoice list | Filter to due_date > 30 days past; name customer + amount + days overdue |

**Ledger state handling**: if the ledger's cash read returns an error, empty response, or "not connected" state, mark the entire Cash section as "n/a — ledger unavailable" (naming which) and continue. Do not retry.

### Xero

| Metric | Tool | Notes |
|---|---|---|
| Cash / bank balance | `get_cash_position` | Same role as the QuickBooks cash read |
| MTD revenue, P&L trend | `get_profit_and_loss` | Current month vs. prior |
| Receivables, AR aging, overdue | `get_aged_receivables` | Name customer + amount + days overdue. (`get_contacts_and_receivables` is deprecated in the Xero server; do not call it) |

### NetSuite

| Metric | Tool | Notes |
|---|---|---|
| Cash, receivables, P&L | `ns_runReport` / `ns_runCustomSuiteQL` | Same metrics, same section |

### MYOB

| Metric | Tool | Notes |
|---|---|---|
| MTD revenue, P&L trend | `myob_get_profit_loss` | Resolve the financial year first with `myob_get_financial_year_dates` |
| Receivables, overdue | `myob_get_outstanding_customer_balances` | No cash balance exists in MYOB; leave the cash line as "not available from MYOB" |

### Zoho Books

Every call takes `organization_id` from `list_organizations`.

| Metric | Tool | Notes |
|---|---|---|
| Cash / bank balance | `list_bank_accounts` with `filter_by=Status.Active` | Sum `current_balance` across bank and cash accounts (`bcy_balance` is the same figure in base currency). No history endpoint, so the WoW delta needs the prior pulse's stored figure or is omitted |
| MTD revenue | `list_invoices` with `date_start`/`date_end` for the month and `response_option=3` | Returns the count and the summed `total`; invoiced revenue, not a P&L — say so. Zoho Books exposes no P&L report endpoint |
| Outstanding receivables | `list_invoices` with `status=unpaid` and `response_option=3` | Summed `balance` |
| AR aging, overdue invoices | `list_invoices` with `status=overdue`, sorted by `due_date` | Each carries `due_days` ("Overdue by 323 days"), `customer_name`, `balance`, `email`; bucket by due date yourself |

Zoho Desk is a separate connector and a separate organisation ID; it feeds the support section below, not this one.

## Revenue & Sales (PayPal / Square / Stripe)

| Metric | Tool | Notes |
|---|---|---|
| 7-day settlement total | PayPal transactions | Sum completed settlements in window |
| Sales trend | PayPal transactions | This 7 days vs. prior 7 days; compute delta |
| Failed / pending transactions | PayPal transactions | Flag any > 200 (business currency; `thresholds.md`) |
| Square settlements | Square (if connected) | Same as PayPal — sum + trend |
| Stripe revenue | Stripe `list_invoices` (if connected) | Paid invoices in window |
| Stripe failed payments | Stripe API read — charges/payment intents (if connected) | Failed charges in window; flag any > 200 (business currency) |
| Stripe disputes | Stripe API read — disputes (if connected) | Any dispute opened in window goes to the watch list, named |

Use whichever payment connectors are available. If both PayPal and Square are connected, report combined and per-source.

## Pipeline (HubSpot)

| Metric | Tool | Notes |
|---|---|---|
| Pipeline by stage | `search_crm_objects` type=deals (`get_crm_objects` needs explicit IDs; see `../../../shared/connector-call-shapes.md`) | Group by deal stage; sum amount |
| Deals closed this week | `search_crm_objects` | Filter closedate in window, stage = closed-won |
| Deals gone cold | `search_crm_objects` | Filter `notes_last_updated` > 7 days ago, open stage. That is HubSpot's "Last Activity Date" on deals — there is no `hs_last_activity_date` or `hs_lastactivitydate` property |
| New leads this week | `search_crm_objects` | Filter createdate in window |
| Stalled/slipped deals | `search_crm_objects` | Open deals where closedate < today |

## Commitments (Google Calendar)

| Metric | Tool | Notes |
|---|---|---|
| This week's key items | `list_events` | Filter to current week; surface meetings with customers, deadlines, important holds |
| Next 7 days | `list_events` | Forward-looking view; highlight anything with external parties |

## Watch List (Gmail or Microsoft 365)

| Metric | Tool | Notes |
|---|---|---|
| Urgent threads | `search_threads` | Query: `is:important OR is:starred` in last 7 days |
| Customer escalations | `search_threads` | Query: terms like "escalation," "complaint," "cancel," "refund," "urgent" in last 7 days |
| Time-sensitive requests | `search_threads` | Query: `is:unread` + keywords like "deadline," "ASAP," "today" |

**Gmail fallback**: if the Gmail call errors (auth flaky), skip Watch List silently and add "Gmail unavailable" to the appendix. Do not surface the error in the pulse body.

## Internal Signals (Slack / Teams)

| Metric | Tool | Notes |
|---|---|---|
| Urgent threads | Slack search (if connected) | Threads with @mentions or urgency signals in owner-relevant channels |
| Action items | Slack search | Messages directed at the owner or tagged for follow-up |

Every section below this point follows the same rule: include only if the connector is available; omit the section entirely if not.

## Commerce (Shopify, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Orders, revenue, sales trend | `list-orders`, `run-analytics-query` | This 7 days vs. prior 7 |
| Fulfillment issues | `list-orders` filtered to unfulfilled past promise | Named orders to the watch list |

## Fulfillment (Square, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Fulfillment issues | Square orders API via `make_api_request` | Same watch-list treatment as Shopify |

## Payroll (Gusto, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Next payroll run | `list_payrolls` / `list_pay_periods` | Date and expected amount — the week's biggest cash commitment |

## Ads (TikTok Ads, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Ad spend, results, cost per result | TikTok reporting (`report_integrated_get`) | Last 7 days vs. prior 7; sits beside the sales trend |

## Card spend (Ramp / Expensify, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Week's card spend | Ramp `ramp_get_transactions` | Sum for window; call out any single transaction > 500 (business currency) |
| Account balance | Ramp `ramp_get_ramp_business_account_balance` | Read-only |
| Card spend + missing receipts | Expensify `Search` | Read-only; count expenses without receipts |

## Signatures (DocuSign, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Unsigned envelopes | `getEnvelopes` filtered to sent status | Flag any sitting unsigned > 3 days, named |

## Internal signals (RingEx Chat, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Urgent team-chat posts | `read_team_chat` | Same role as Slack: escalation keywords, threads needing the owner. Chat only — no call data exists here |

## Customer Support (Zoho Desk, if connected)

| Metric | Tool | Notes |
|---|---|---|
| Open tickets, escalations | `getTickets` (`status`, `priority`, `sortBy=recentThread`) / `getTicketsMetrics` | Count open; flag any > 48h unresolved and any priority High, named. `getTickets` rejects an `include` parameter — request extra fields with `fields` |

## Risks scan

Run these alongside the metric pulls — don't wait for metrics to finish first.

| Risk | Source | Trigger condition |
|---|---|---|
| Overdue AR | Ledger invoices / aged receivables | due_date > 30 days past, unpaid |
| Stalled deals | HubSpot | Open deal, no activity 7+ days |
| Slipped deals | HubSpot | Open deal, closedate in past |
| Urgent mail threads | Gmail or Microsoft 365 | `is:important` or escalation keywords |
| Failed payments | PayPal / Square / Stripe | Failed or pending > 200 (business currency) |
| New dispute | Stripe / PayPal | Any dispute opened in window — always a watch-list item |
| Stale unsigned envelope | DocuSign | Sent envelope unsigned > 3 days |
| Missing receipts piling up | Expensify | 5+ expenses without receipts in window |

## Parallelization

All of the above should fire in a single tool-call batch. A complete pulse is typically 8–15 parallel calls. If one errors, the rest proceed normally and the failed source appears in "Sources unavailable" at the bottom of the pulse.

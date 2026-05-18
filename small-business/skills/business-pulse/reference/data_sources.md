# Data Sources

Exact mapping from each pulse section to the MCP tool that produces it. **Dispatch all calls in a single parallel batch** — do not pull serially.

## Cash & Finance (QuickBooks)

| Metric | Tool | Notes |
|---|---|---|
| Cash / bank balance | `cash-flow-quickbooks-account` | Current balance; show delta vs. prior week if available |
| MTD revenue | `profit-loss-quickbooks-account` | Current month vs. prior month |
| Outstanding receivables | QuickBooks invoice list | Filter to open/unpaid |
| AR aging | QuickBooks invoice list | Group by days since due: 0–30, 31–60, 61+ |
| Overdue invoices | QuickBooks invoice list | Filter to due_date > 30 days past; name customer + amount + days overdue |

**QB state handling**: if `cash-flow-quickbooks-account` returns an error, empty response, or "not connected" state, mark the entire Cash section as "n/a — QuickBooks unavailable" and continue. Do not retry.

## Revenue & Sales (PayPal / Square / Stripe)

| Metric | Tool | Notes |
|---|---|---|
| 7-day settlement total | PayPal transactions | Sum completed settlements in window |
| Sales trend | PayPal transactions | This 7 days vs. prior 7 days; compute delta |
| Failed / pending transactions | PayPal transactions | Flag any > $200 |
| Square settlements | Square (if connected) | Same as PayPal — sum + trend |
| Stripe revenue | Stripe `list_invoices` (if connected) | Paid invoices in window |

Use whichever payment connectors are available. If both PayPal and Square are connected, report combined and per-source.

## Pipeline (HubSpot)

| Metric | Tool | Notes |
|---|---|---|
| Pipeline by stage | `get_crm_objects` type=deals | Group by deal stage; sum amount |
| Deals closed this week | `search_crm_objects` | Filter closedate in window, stage = closed-won |
| Deals gone cold | `search_crm_objects` | Filter hs_last_activity_date > 7 days ago, open stage |
| New leads this week | `search_crm_objects` | Filter createdate in window |
| Stalled/slipped deals | `search_crm_objects` | Open deals where closedate < today |

## Commitments (Google Calendar)

| Metric | Tool | Notes |
|---|---|---|
| This week's key items | `list_events` | Filter to current week; surface meetings with customers, deadlines, important holds |
| Next 7 days | `list_events` | Forward-looking view; highlight anything with external parties |

## Watch List (Gmail)

| Metric | Tool | Notes |
|---|---|---|
| Urgent threads | `search_threads` | Query: `is:important OR is:starred` in last 7 days |
| Customer escalations | `search_threads` | Query: terms like "escalation," "complaint," "cancel," "refund," "urgent" in last 7 days |
| Time-sensitive requests | `search_threads` | Query: `is:unread` + keywords like "deadline," "ASAP," "today" |

**Gmail fallback**: if the Gmail call errors (auth flaky — this is a known issue), skip Watch List silently and add "Gmail unavailable" to the appendix. Do not surface the error in the pulse body.

## Internal Signals (Slack / Teams)

| Metric | Tool | Notes |
|---|---|---|
| Urgent threads | Slack search (if connected) | Threads with @mentions or urgency signals in owner-relevant channels |
| Action items | Slack search | Messages directed at the owner or tagged for follow-up |

## Customer Support (Intercom / Zendesk)

| Metric | Tool | Notes |
|---|---|---|
| Open tickets | Intercom `search_conversations` / Zendesk | Count open; flag any > 48h unresolved |
| Escalations | Intercom `search_conversations` | Filter to priority or tagged escalation |

Include only if connector is available; omit section entirely if not.

## Risks scan

Run these alongside the metric pulls — don't wait for metrics to finish first.

| Risk | Source | Trigger condition |
|---|---|---|
| Overdue AR | QuickBooks invoices | due_date > 30 days past, unpaid |
| Stalled deals | HubSpot | Open deal, no activity 7+ days |
| Slipped deals | HubSpot | Open deal, closedate in past |
| Urgent Gmail threads | Gmail | `is:important` or escalation keywords |
| Failed payments | PayPal / Square | Failed or pending > $200 |

## Parallelization

All of the above should fire in a single tool-call batch. A complete pulse is typically 8–15 parallel calls. If one errors, the rest proceed normally and the failed source appears in "Sources unavailable" at the bottom of the pulse.

# Connector call shapes — parameters that are easy to get wrong

**Shared across the plugin.** Each line below is a call that fails
on the obvious shape and works with the right one. None is a
bug; all are shapes the connector requires and the tool description does not
make obvious. Read the row for a connector before the first call to it.

**Before any row: which entry to call.** A connector can be registered twice —
the owner's own entry and the plugin's manifest copy (`small-business:<manifest
key>`, tools prefixed `mcp__plugin_small-business_`). Call whichever is
authorized, the owner's if both. A refused call from the plugin copy while the
owner's entry is live is not "not connected" and not a reason to take a
skill's degradation path or ask for exports. The rule is
`connector-neutrality.md`, "One connector, two registrations".

| Connector | Tool | Shape that works |
|---|---|---|
| Airwallex | `list_billing_invoices` | For "what is unpaid" pass both `status: FINALIZED` and `payment_status: UNPAID`; a `VOIDED` invoice still reports `UNPAID`. Rows carry `billing_customer_id`, not a customer name — `retrieve_billing_customer` for the name and email. Airwallex's `number` is its own numbering; the ledger invoice number, when present, is in `metadata`. Date filters (`from_created_at`, `to_created_at`) take the `+0000` offset form; a trailing `Z` is rejected on the invoice list (Airwallex's own trap list). Take tool names from the connected server's tool list. |
| Gusto | `update_payroll` | `get_payroll` first, always. Values **replace**: `hours: "45"` sets 45, it does not add 45 — compute the total from the current value and show "40 → 45" before calling. Omitted employees and lines are left alone (partial update). A payroll with no materialized roster (`employee_compensations` empty, `calculated_at` null) takes one call with an empty `employee_compensations` array to populate it, then the real call. Hourly lines edit only for nonexempt FLSA statuses; a salaried person's adjustment goes in `fixed_compensations` under an existing name. Cannot submit — that is `run_payroll`, which this plugin never calls. |
| Gusto | `list_time_records` | Takes the period's start and end dates. Read `source` before any field: `native` gives `shifts`, `third_party` gives `timesheets`, `none` gives neither. A company with both returns only third-party. Contractor clock times come back null unless an admin entered them. |
| Gusto | `record_time` | Required: `company_uuid`, `company_member_uuid` (from `list_time_records`, not an employee uuid), `shift_started_at` and `shift_ended_at` as ISO8601 **with an explicit UTC offset** and in the past, and `timezone` as an IANA name. `on_existing` defaults to `add`; pass `update` plus `shift_id` to correct an entry, or the hours land twice. `shift_id` is the shift's id under `shifts` on native tracking, and the timesheet's **top-level** id on third-party (the nested entry id refuses). On native tracking an `update` also requires `job_uuid`, and an `add` for a worker with several jobs refuses with `ambiguous_job` until one is chosen; omit `job_uuid` for a contractor. The native response carries no resulting hours: confirm by re-reading `list_time_records` — and a contractor's re-read shows the hours with blank clock times, which is success, not failure; do not write again. |
| Gusto | `list_payrolls` | A bare call covers pay periods ending in the past six months up to today, so a current period that has not ended yet is missing. To find the run to stage: `processing_statuses: unprocessed` with `end_date` up to three months ahead, then the item whose `check_date` is nearest. `calculated_at: null` marks a payroll whose roster is not yet materialized (see `update_payroll`). |
| HubSpot | `get_crm_objects` | Takes explicit object IDs only. For any list or filter query ("open deals," "contacts created this month") use `search_crm_objects` with filters, then `get_crm_objects` for the full records if needed. |
| HubSpot | `query_crm_data` | One required parameter, `sql`: a HubSpot-dialect query (one object type per query, no JOINs, `hs_object_id` as the id). Free text or any other parameter name fails with a raw "Missing required field" error that does not name the field. Call `tool_guidance` first (its own rule) and confirm property names with `search_properties`; for simple filters `search_crm_objects` is the easier path. |
| Intuit QuickBooks | `qbo_contact_search_customer` | The parameter is `customer_name`, not `query`. |
| Intuit QuickBooks | `qbo_accounting_get_ap_aging_summary` | Nets vendor credits into buckets and reports negative overdue totals with any books; read `qbo_accounting_get_ap_aging_detail` with `transaction_type` unset and bucket the rows (`quickbooks-report-traps.md`, Trap 6). |
| Intuit QuickBooks | `profit_loss_quickbooks_account` | The response's `totalExpenses`, `grossProfit`, and `grossProfitMargin` report 0 / 100% while the rows and `monthlyBreakdown` carry the real figures; read those (Trap 2). |
| Intuit QuickBooks | `qbo_payroll_get_company_payroll_readiness` | Can answer `has_employees: false` while `qbo_payroll_get_employees` returns a `total_count` on the same company. Read both, say both, stage nothing while readiness says not ready (Trap 7). |
| Mailchimp | `get_capabilities` | Needs both `user_request` (what the owner is trying to do, in words) and a `category` from its enum. Present the reply verbatim, per the connector's own instruction. |
| Salesforce | `discover`, `describe`, `dispatch_readonly`, `dispatch` | Four tools, one flow, every time: `discover` with what you are trying to do in plain words returns ranked operations; `describe` the one you pick and read its parameters before calling; `dispatch_readonly` runs it for any read (a count, a SOQL query, a search); `dispatch` only for the write the owner approved, and it enforces the signed-in user's access. Never `dispatch` a read, never `dispatch` an operation you did not `describe`, and there is no delete. The Headless 360 server is owner-added (custom connector, per-org address). |
| Shopify | `get-inventory-levels` | One `productId` per call; there is no bulk read. Loop the products the run needs, and say how many were read if the catalog is large. |
| Square | `get_service_info` and `get_type_info` | Need a `service` string first (e.g. `payments`, `refunds`, `inventory`, `customers`); a bare call fails. Then `make_api_request` against that service. |

**Adding a row.** When a call fails on shape and succeeds on retry, add the
row here rather than to one skill: every skill that touches the connector
gets the fix at once. Keep it to shape; behaviour traps go in the connector's
own trap file (`quickbooks-report-traps.md`, `gmail-inbox-traps.md`).

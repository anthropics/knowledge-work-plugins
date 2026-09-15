# Gotchas

Known failure modes for invoice-chase.

---

**Customer paid via check or bank transfer — not visible in PayPal.**

The PayPal cross-reference only catches PayPal payments. A customer who paid by check or ACH may still appear as overdue in AR. Note this in the summary: "PayPal history only — check/ACH payments not verified." Let the owner confirm before sending.

---

**QuickBooks AR includes internal or test accounts.**

Some setups include internal billing accounts or test records in AR. Before drafting, filter out customers whose email domain matches the owner's domain, and flag any customer name containing "Test," "Internal," or "Demo."

---

**Multiple overdue invoices from the same customer — send one email only.**

Never draft two separate reminders to the same customer in one batch. Consolidate all overdue invoices into one email with a total amount and a list of invoice numbers. Two emails to the same person in one batch looks disorganized and may trigger a spam filter.

---

**PayPal reminder send fails for customers without a PayPal account.**

PayPal reminders only work if the customer has an active PayPal account. If PayPal returns a send error, fall back to queuing a mail draft and report the fallback: "PayPal send failed for [customer] — queued as [mail app] draft instead." Do not silently drop the reminder.

---

**Stripe and QuickBooks may both carry the same invoice.**

If Stripe is enabled and a customer appears in both QuickBooks AR and Stripe overdue, it may be the same invoice in two systems. Match on invoice number first; if no number match, match on amount + due date. When uncertain, flag to the owner and send only one reminder rather than two.

---

**PayPal API returns 429 rate limit errors.**

PayPal's MCP connector rate-limits aggressively when the requested date window is wide. The most common cause is querying 14–30 days of transactions in a single call.

*Fix:* Always query with `transaction_status: S` (settled only) and a **7-day window** ending today. This is the default in the workflow.

*Retry pattern:* If a 7-day query returns 429, retry immediately with a **3-day window**. A narrower window reduces the response payload and usually succeeds.

*Fallback:* If the 3-day retry also returns 429, skip the PayPal cross-reference for this run entirely. Flag every customer in the batch as "PayPal unavailable — verify manually" in the summary table. Proceed with QuickBooks-only scoring. Do not silently drop the caveat — the owner needs to know the cross-reference was skipped before approving any sends.

---

**Airwallex invoice numbers match nothing in the ledger.**

Airwallex numbers its invoices itself (`INV-XXXX-0002` style). Its numbers do not match a ledger invoice, while the ledger invoice number stored in each invoice's `metadata` does. Match on `metadata` first. When an invoice has no `metadata` (subscription-generated invoices often do not), resolve `billing_customer_id` with `retrieve_billing_customer` and match on customer plus amount plus due date. Never put Airwallex's own number in a reminder as the invoice number; the customer's copy carries the ledger number.

---

**Airwallex voided invoices still report `payment_status: UNPAID`.**

A voided invoice keeps `payment_status: UNPAID`, so a list filtered on payment status alone includes invoices nobody owes. Always pass `status: FINALIZED` too (or drop any row whose `status` is `VOIDED`).

---

**Airwallex account name may not match the business name.**

`get_account_details` can return a legal name that does not match the owner's business while the account nickname does. Confirm the account by the nickname or identifiers before treating it as the wrong account; do not stop the run on the legal name alone.

---

**Airwallex cannot send a reminder.**

There is no send-reminder or notify tool on an invoice; Airwallex's own billing skill says the same ("no API to email invoices directly"). Every Airwallex-sourced reminder goes out through the owner's mail connector, or comes back as copy, with the invoice's `hosted_url` as the pay link. `hosted_url` only exists when `collection_method` is `CHARGE_ON_CHECKOUT`; an `OUT_OF_BAND` invoice may have only `pdf_url` — link that and tell the owner the customer will pay by bank transfer. `create_payment_link` does take a `shopper_email` that emails the link from Airwallex — do not use it here; the reminder is the owner's message, in the owner's voice, from the owner's mailbox.

---

**Two Airwallex connectors exist; the owner wants the production one.**

There are two: **airwallex-agentos** (production account, `mcp.airwallex.com/mcp`) and **airwallex-developer** (sandbox plus docs). The plugin declares the production one. Airwallex's own guidance is to take tool names from the connected server's tool list rather than assume them, so on first use confirm `list_billing_invoices`, `retrieve_billing_customer`, and `create_payment_link` exist by name and adapt if the production server names them differently. If the owner connected the developer connector by mistake, every figure is sandbox data: say so and stop.

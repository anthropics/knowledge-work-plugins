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

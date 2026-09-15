# More sources

More invoices in scope. Same tone-matching, same approval gates.

---

## AR sources

Ledgers are peers (`../../../shared/connector-neutrality.md`): whichever is connected is the AR source. If two are connected, ask which holds the invoices and name it.

| Source | Notes |
|---|---|
| MYOB | Per-customer outstanding balances with at-risk flags, plus standard payment terms. Read-only, three financial years of history |
| NetSuite | AR aging via reports and SuiteQL |
| QuickBooks | AR aging report with invoice dates, due dates, and days outstanding |
| Xero | Aged receivables by contact (`get_aged_receivables`) with invoice detail |
| Zoho Books | `list_invoices` with `status=overdue` (sort by `due_date`): each row carries `due_days`, `balance`, `customer_name`, `email`, `reminders_sent`, `last_reminder_sent_date`, and the hosted `invoice_url` to put in the reminder. `list_contacts` with `filter_by=Invoice.OverDue` gives the per-customer total. No send-reminder tool: reminders route to the mail connector or come back as copy, as for MYOB |
| PayPal | Invoices and settlement timing |
| Stripe | Overdue invoices and failed subscription charges. Pull it whenever it's connected |
| Airwallex | `list_billing_invoices` with `status: FINALIZED` and `payment_status: UNPAID`. Each row carries `amount_due`, `currency`, `due_at`, `days_until_due`, `billing_customer_id`, and the `hosted_url` pay page to put in the reminder. Airwallex assigns its own `number` (`INV-XXXX-0002`) that matches nothing in the ledger — match by the ledger invoice number in `metadata` when the invoice was created with one, else by customer (`retrieve_billing_customer` on `billing_customer_id` for the name and email) plus amount plus due date. `VOIDED` invoices still report `UNPAID`; the status filter drops them. `hosted_url` is present only for `CHARGE_ON_CHECKOUT` invoices; an `OUT_OF_BAND` (bank transfer) invoice may carry only `pdf_url`. No send-reminder tool: reminders route to the mail connector with the pay link in the body |

**Pull from every connected source, then deduplicate.** The same invoice can appear in both the ledger and the processor. Match on customer plus amount plus date, and prefer the ledger's version — it is what the owner's books say.

**MYOB gives you the balance and not the person.** It returns customer names and what they owe, with no email address or phone number attached. Match each name to a contact in Gmail, Microsoft 365, or the CRM before drafting, and when no match exists say so by name — "three customers on the list have no email on file" — rather than dropping them out of the run quietly.

MYOB is also the one AR source that cannot send. Every MYOB-sourced reminder routes to the mail connector or comes back as copy.

---

## The paid-in-the-last-14-days check

This check runs across every connected processor, not just PayPal.

A customer who paid through Stripe on Friday and gets a QuickBooks-driven reminder on Monday is the single most damaging failure in this skill. It is embarrassing, it looks careless, and it lands on the customers who pay reliably.

Check PayPal, Stripe, Square, and Shopify settlements before drafting anything. If any of them shows a recent payment, flag as "possibly paid — verify" rather than drafting.

Window: 14 days for every source except PayPal, which is queried over 7 days (3 on a rate-limit retry) because wider windows trigger its 429s. Say in the summary when PayPal ran on the short window.

Matching key: email where both the ledger and the processor or storefront expose one; otherwise name, marked "name match only — verify" in the table. A processor's customer record and a ledger's customer record for the same person routinely differ in name form; the email is the stable key.

Airwallex's check is the invoice's own `payment_status`: an Airwallex invoice that reads `PAID` while the ledger still carries the balance is "possibly paid — verify." One list call, no date window.

---

## Sending

| Route | When |
|---|---|
| PayPal | The invoice originated in PayPal. Sends directly, with approval |
| Stripe | Stripe's own reminder, with approval |
| Airwallex | No send tool (Airwallex Billing has no API to email an invoice). The reminder goes out through the mail connector (or as copy) with the invoice's `hosted_url` as the pay link, or `pdf_url` when there is no hosted page. For a ledger-only invoice the owner can ask for a link: `create_payment_link` with `title`, `amount`, `currency`, `reference` and `metadata` set to the ledger invoice number, no `shopper_email`. Minted inside the batch approval, never on its own |
| Gmail or Microsoft 365 | Everything else — queues a real draft in the owner's mailbox |
| Draft only | No mail connector. Copy formatted to paste |

Queuing into the owner's actual mail client is a meaningful improvement over handing back text. It lands in their drafts folder where they already work, and it keeps the thread history intact.

---

## Voice

Reminders go out under the owner's name. Read [the shared voice profile](../../../shared/voice-profile.md) before drafting.

Two separate things are at work and both matter:

- `tone-matching.md` decides **how firm** the message is, from payment history
- The voice profile decides **how it sounds**

A correctly firm reminder that doesn't sound like the owner still gets rewritten by hand, which is the outcome the skill exists to prevent.

---

## What doesn't change

- Nothing sends without explicit approval, one batch at a time
- No reminder to anyone not in an AR report. Never from memory
- Good payers get gentle, repeat-late payers get firm, and the scoring is unchanged
- No connector at all still works: an AR CSV in, drafted reminders out

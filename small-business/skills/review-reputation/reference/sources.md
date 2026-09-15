# Sources

One required backbone, everything else deepens it. The skill works on day one
with nothing connected at all.

| Source | Status | What it gives |
|---|---|---|
| A CRM (HubSpot, Monday.com, Salesforce, Zoho CRM), a payments connector (PayPal, Square, Stripe), **or** a storefront (Shopify, Square) | Required — one of any of the three categories | Tickets and feedback; disputes and refunds; or order history (who bought what and when) plus fulfillment and refund patterns |
| Support desk (Zoho Desk) | Optional | Tickets by customer, priority, and status — complaints in the customer's own words |
| Gmail | Optional | Complaint and praise language in threads |
| Web research | Always available | Publicly visible reviews on Google, Yelp, Facebook |
| Pasted or exported reviews | Always available | The best source there is, with dates and ratings |

---

## Public reviews

**Preferred: an export.** Google Business Profile and Yelp both let the owner
download their reviews. An export carries the rating, date, reviewer name, and
full text, and it includes reviews the public page paginates away. Ask for one
the first time this skill runs; it takes the owner two minutes and improves
every run afterward.

**Fallback: what is visible on the web.** Fetch the business's public review
pages and read what renders. This is genuinely useful and genuinely partial —
pages truncate, paginate, and reorder. Say so in the Sources section rather
than presenting a partial pull as a complete one.

**Also fine: pasted text.** The owner drops reviews into the chat. Tag them
`[Review]` like any other source and use them.

When counting, never total a rating average across sources. Google's average
and Yelp's average are different numbers about different populations, and an
owner who repeats a blended figure to a customer will be wrong.

---

## Disputes and tickets

**PayPal disputes.** Fetch disputes opened in the window. PayPal throttles
aggressively on wide date windows. On the first rate-limit error, stop, record
`PayPal: rate-limited — not included` in Sources, and continue. Do not retry
silently; suggest a narrower window instead.

**Stripe disputes and refunds.** `GET /v1/disputes` created in the window
(via `stripe_api_read`), with `reason` and `status`; `GET /v1/refunds` for
the same window, since a run of refunds against one product is a theme
before it is a review. A dispute's `evidence_details.due_by` is a deadline —
surface any open one in the "do these three things" list.

**Square disputes.** The disputes endpoint through `make_api_request` for the
window. Same treatment as Stripe.

**HubSpot tickets and feedback.** Fetch open and recently closed tickets, plus
any feedback submissions. Zero tickets is a legitimate state for a new or
small portal — record `HubSpot tickets: 0` and move on. Only flag a connector
problem when authentication itself fails.

**Zoho Desk tickets.** `getTickets` for the window (`receivedInDays` 30 or
90 to match it; sort by `recentThread`), then `getThreads` on the ones whose
subject reads as a complaint, for the verbatim. `getTicketsMetrics` gives the
open, overdue, and on-hold counts for the header. Open tickets with priority
High belong in the Disputes and tickets count, not only in the theme list.
`getTickets` rejects an `include` parameter — ask for extra fields with
`fields`.

---

## Email

Search the window for threads containing complaint and praise language. Seed
list, deliberately wide:

```
refund  cancel  unhappy  issue  problem  disappointed  frustrated  broken
late  slow  wrong  missing  never again  took forever  thank you  lifesaver
recommend  great job
```

Customers rarely use the word "disappointed." They write "took forever" and
"never again." Over-inclusion is cheap here because theme extraction filters
the noise; a narrow keyword list silently loses whole themes.

Pull the subject line and one or two sentences of the customer's own words —
enough to quote verbatim later.

---

## Shopify

Covered in `churn-signals.md`. In short: orders, fulfillment times, and
refunds, read as behavior rather than opinion.

---

## Reporting what you got

Every run ends with an honest Sources block. Counts, and named failures:

```
Sources pulled — Apr 28 to Jul 27

  Google reviews (export)      14
  Yelp (web, partial)           6   — page shows most recent only
  Stripe disputes               3
  Stripe refunds                7
  HubSpot tickets               0
  Zoho Desk tickets            12   — 2 open, priority High
  Gmail threads                11
  Shopify orders              182
```

Name the connector that was actually read on each line (the example above is
a Stripe and Zoho Desk shop; a PayPal and HubSpot shop lists those). The dash
matters as much as the numbers. A source that is missing looks exactly like a
source with nothing bad in it unless it is named.

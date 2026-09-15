# Gotchas — review-reputation

## Gotcha: Posting a public response without approval

**Why it matters:** A review response is permanent, public, and attributed to
the owner by name. It is read by every future customer who finds the review.
There is no version of "we'll fix it next run" that undoes it.

### ✗ Bad

Draft eight responses, post them all, then show the owner what went out.

### ✓ Good

Present each draft next to the review it answers and get a yes on that one
before posting it. Approve one at a time — a batch approval on eight public
responses is how the wrong one goes live.

---

## Gotcha: Blending rating averages across platforms

**Why it matters:** Google's 4.3 and Yelp's 4.0 describe different populations
of reviewers. An average of the two is a number that exists nowhere, and the
owner will repeat it to a customer or put it on a truck.

### ✗ Bad

> Your overall rating is 4.2 across 45 reviews.

### ✓ Good

> Google: 4.3 (34 reviews), down from 4.6 last quarter.
> Yelp: 4.0 (11 visible). Different reviewer pools — not averaged.

---

## Gotcha: Treating a partial web scrape as a complete pull

**Why it matters:** Public review pages paginate, truncate, and reorder. A
report built on the first page reads as the whole picture, so the owner
concludes there are no new complaints when there are three on page two.

### ✗ Bad

> Yelp reviews: 6

### ✓ Good

> Yelp (web, partial): 6 — page shows most recent only

Then ask for an export once. It takes the owner two minutes and fixes every
run afterward.

---

## Gotcha: Ranking quiet customers by silence alone

**Why it matters:** A list sorted by longest gap fills with annual customers
who are perfectly happy and one-time buyers who were never coming back. The
owner works the top of the list, finds it worthless, and stops using it.

### ✗ Bad

Sort every customer by days since last order and hand over 200 names.

### ✓ Good

Measure each customer against their own median interval, then rank by past
value. Fifteen names the owner will actually call beats two hundred they
won't. Put anyone who left a bad review and then went quiet at the top
regardless of value — they said what was wrong and left anyway.

---

## Gotcha: Offering a discount the owner never authorized

**Why it matters:** A win-back message that promises 20% off is a commitment
the owner has to honor once it lands. Drafting it before asking turns a churn
problem into a margin problem, and the owner finds out when the customer
redeems it.

### ✗ Bad

> Hi Dana — we've missed you. Here's 20% off your next service.

Nobody agreed to 20%.

### ✓ Good

Ask what is on the table before drafting: an offer, a plain note, or a call
from the owner. Draft only inside that answer, and say plainly when a call
beats a coupon — an email to someone who spent USD 9,000 reads as a mailing list.

---

## Gotcha: Arguing with a reviewer in public

**Why it matters:** The audience is not the reviewer. It is the next customer
reading the exchange, deciding how this business behaves when provoked. A
correct, well-evidenced rebuttal still loses that reader.

### ✗ Bad

> Our records show the technician arrived within the scheduled window and our
> policy clearly states parts orders take 5-7 business days.

### ✓ Good

Correct one factual point, offer a real contact route, and stop. Under 60
words. If the review breaks platform rules, explain the removal path to the
owner honestly — including that most requests are declined — rather than
promising it will come down.

---

## Gotcha: PayPal rate limits on dispute queries

**Why it matters:** PayPal's disputes API throttles aggressively on date windows with many disputes. Silent retries burn the user's time with no feedback.

### ✗ Bad
Retry 3× automatically with no feedback. User sees a spinner for 30+ seconds before an error.

### ✓ Good
On the first rate-limit error, skip PayPal, add `PayPal: rate-limited — not included` to the Sources section, and continue with the remaining connectors. Mention that the user can try again with a narrower date window.

---

## Gotcha: Verbatim quotes paraphrased or summarized

**Why it matters:** The owner needs to see the actual customer words — not Claude's interpretation. Paraphrase destroys the credibility of the report.

### ✗ Bad
**Theme: Slow shipping** (8 signals)
> Customers reported that deliveries arrived later than expected.

### ✓ Good
**Theme: Slow shipping** (8 signals)
> "Ordered 2 weeks ago and still nothing — this is unacceptable." — [Gmail]
> "Package was 10 days late and support never responded." — [Zoho Desk]

---

## Gotcha: HubSpot returning 0 tickets treated as an error

**Why it matters:** Test portals and new accounts legitimately have 0 tickets. Surfacing a warning creates noise and erodes trust.

### ✗ Bad
> ⚠️ HubSpot returned 0 tickets. Check your connection or permissions.

### ✓ Good
Record `HubSpot tickets: 0` in the Sources section and continue. Only flag a connector issue if authentication itself fails.

---

## Gotcha: Gmail keyword list too narrow

**Why it matters:** Customers don't use standard complaint keywords. A 1-star experience often surfaces as "took forever" or "never again," not "disappointed."

### ✗ Bad
Search only for: `refund cancel unhappy`

### ✓ Good
Use the full seed list in `sources.md`, which includes phrasings like "took forever" and "never again." Let theme extraction filter signal from noise — over-inclusion is cheaper than a missed theme.

# Example: Customer Pulse Report

**Trigger used:** "How are customers feeling this month?"
**Date range:** April 1–30, 2026

---

## Customer Pulse — April 1–30, 2026

### Sources pulled
- PayPal disputes: 4
- HubSpot tickets: 9
- Gmail threads: 14
- Intercom conversations: 6
- Pasted reviews: 0

### Themes

**1. Shipping delays causing repeat complaints** (11 signals)
> "Ordered 2 weeks ago and still nothing — this is unacceptable." — [Gmail]
> "Package was 10 days late and support never responded." — [Intercom]
> "Where is my order? The tracking hasn't updated in 5 days." — [HubSpot]

**2. Refund process too slow** (8 signals)
> "I filed a dispute because I never got a response to my refund request." — [PayPal]
> "It's been two weeks since I asked for a refund. Still waiting." — [Gmail]
> "Your return policy says 5 days but it's been 12." — [HubSpot]

**3. Product quality below expectations** (5 signals)
> "The stitching came apart after one wash." — [Intercom]
> "Looks nothing like the photo." — [Gmail]
> "Would not buy again — quality is not what I expected for the price." — [HubSpot]

### Do these 3 things this week
1. **Fix shipping comms** — Email every open order older than 7 days with a status update and a new ETA. This alone will cut Intercom volume before the root cause is resolved.
2. **Speed up refunds** — Set a 48-hour SLA for refund approvals and assign one person to clear the current backlog this week.
3. **Audit product listing photos** — Pull the top 3 products by complaint volume and update photos to match what's actually shipped.

---

## Example: PayPal rate-limited run

**Trigger used:** "Customer pulse for last 30 days"

### Sources pulled
- PayPal disputes: rate-limited — not included
- HubSpot tickets: 7
- Gmail threads: 11
- Intercom conversations: 4
- Pasted reviews: 3

*(Report continues normally with available sources. PayPal note appears only in Sources — no error message in the body.)*

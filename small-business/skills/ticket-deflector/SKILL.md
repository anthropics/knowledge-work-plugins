---
name: ticket-deflector
description: >
  Reads a forwarded customer email or ticket, pulls order/refund status from
  PayPal and account history from HubSpot, drafts a tone-matched reply in the
  owner's writing voice, and can issue a PayPal refund with explicit owner
  approval. Use when the user says "draft a response," "answer this customer,"
  "where's my order," or "I want a refund."
compatibility: "Requires PayPal, HubSpot, Mail. Optional: Intercom, Square."
---

# Ticket Deflector

## Quick start

Forward or paste a customer email — Claude pulls order status from PayPal, looks up the customer in HubSpot, and drafts a reply in the owner's voice. If a refund is needed, it stages the details and waits for explicit approval before issuing anything.

```
User: "answer this customer" [forwards email]
→ Extract customer email + issue from thread
→ Pull PayPal transaction status
→ Pull HubSpot contact history
→ Draft reply in owner's voice
→ Owner approves draft → send or stage
→ If refund needed: approval prompt → owner confirms → issue
```

## Workflow

1. **Read the customer message.** Accept a forwarded Gmail thread or pasted text. Extract: customer email address, name, order or transaction ID (if present), and the core issue — refund request, order status question, or general complaint. If multiple issues are present, address them in the order they appear.

2. **Pull order status from PayPal.** Search PayPal transactions by customer email or transaction ID. Capture: amount, date, status, and whether a refund has already been issued. If PayPal is not connected, note it in the draft and continue. If no transaction matches, flag it — do not guess at a match.
   - **PayPal rate limit:** If the customer provided a transaction ID, use it — single-record lookups avoid throttling entirely. If searching by email, use a 7-day window (not 30 days). PayPal's transaction list endpoint throttles aggressively on wide date-range queries; back-to-back tickets in the same session will hit this limit if the window is too broad.
   - If Intercom is connected, check for open support tickets from this customer.
   - If Square is connected, check Square transaction history as a secondary source.
   - If multiple transactions match, surface all of them and ask the owner which one applies before drafting.

3. **Pull customer history from HubSpot.** Search contacts by email address. Pull: lifecycle stage, notes, open deals, and recent activity. If no contact exists, note it and offer to create one after the reply is sent — do not create during the response workflow.

4. **Draft the reply.** Write in the owner's writing voice. Adjust tone to fit the issue type:
   - Refund request → empathetic, clear, action-oriented
   - Order status question → factual, reassuring
   - General complaint → acknowledge, explain, offer resolution
   Flag any data gaps inline in the draft with a bracketed note (e.g., *[Note: No PayPal transaction found — verify order ID before sending]*) so the owner sees the gap before sending. For a worked example, see [reference/examples/respond-refund-request.md](reference/examples/respond-refund-request.md). For common pitfalls, see [reference/gotchas.md](reference/gotchas.md).

5. **Approval gate — owner reviews the draft.** Present the full draft. Do not send or stage it until the owner approves. The owner may edit freely before approving.

6. **Approval gate — refund issuance.** If a refund is warranted, surface a dedicated confirmation prompt after the owner approves the draft:

   > *"Issue refund of $[amount] to [customer name] ([email]) for transaction [ID]? Reply Y to proceed."*

   Wait for explicit confirmation. If the owner's reply is anything other than a clear yes, stop and ask what they'd like to do instead.

7. **Send or stage the reply.** After draft approval, ask the owner: send via Gmail now, or save as a draft? Execute their choice. Then log the interaction as a note on the HubSpot contact timeline.

8. **Report.** One short paragraph: reply sent or staged, refund issued or not, HubSpot note logged.

## Approval gates

- **Never issue a PayPal refund without explicit owner confirmation** — always show amount, customer name, email, and transaction ID before executing.
- **Never send the reply without owner review.** Always present the full draft first.
- **Never create a HubSpot contact during the response flow.** Offer it afterward.
- **Never auto-select a PayPal transaction.** If multiple match, surface them all and let the owner choose.
- **Never fabricate order details.** If PayPal has no record, say so inline in the draft — do not invent a status.

## Reference

- [reference/gotchas.md](reference/gotchas.md) — Good / Bad patterns for tone, PayPal lookup, and ambiguous refund scenarios
- [reference/examples/respond-refund-request.md](reference/examples/respond-refund-request.md) — worked example: refund request with PayPal transaction found

# Gotchas — ticket-deflector

Edge cases where this skill is most likely to go wrong.

---

## Gotcha: Matching the owner's voice, not a generic "professional" tone

**Why it matters:** The value of this skill is that responses sound like the owner wrote them. A bland corporate draft gets rewritten from scratch — wasted effort.

### ✗ Bad

> Dear Customer,
>
> Thank you for reaching out. We apologize for any inconvenience and are committed to resolving your issue in a timely manner. Please allow 3–5 business days for processing.
>
> Sincerely, Customer Support

### ✓ Good

Read `../../../shared/voice-profile.md` first and draft in the owner's actual register. If that file holds no profile yet, follow its "When there is no sample" instruction — ask for three emails the owner was happy with. If they decline or have nothing handy, write plainly and say the draft is un-voiced rather than inventing a personality. A short, direct owner gets a short direct draft. A warm, chatty owner gets warmth and their punctuation quirks preserved.

---

## Gotcha: Flagging data gaps inline, not at the end

**Why it matters:** If PayPal has no matching transaction and the draft says "your refund of USD 64.00 is being processed," the owner will send a false claim. Data gaps must be visible at the point they affect the message.

### ✗ Bad

Draft the reply as if all data is available, then add a footnote: "Note: I couldn't find a PayPal transaction."

### ✓ Good

Insert the gap notice inside the draft at the exact sentence where it matters:

> Hi Sarah, thanks for reaching out. I've looked into your order *[Note: No PayPal transaction found for this email — verify order ID before sending]* and want to get this sorted.

The owner sees the problem before clicking send.

---

## Gotcha: Multiple PayPal transactions for the same customer

**Why it matters:** A customer with two orders — one refunded, one not — will break a simple "most recent" lookup and produce the wrong draft.

### ✗ Bad

Auto-pick the most recent transaction and proceed without telling the owner.

### ✓ Good

Surface all matching transactions and pause:

> *"Found 2 PayPal transactions for this customer: (1) USD 49.00 · 2026-03-14 · Completed · (2) USD 129.00 · 2026-04-01 · Completed. Which one is this about?"*

Wait for the owner to confirm before writing the draft.

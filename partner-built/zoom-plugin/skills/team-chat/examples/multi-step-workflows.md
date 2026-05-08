# Multi-Step Workflows (Chatbot API)

## Pattern

1. Send a card with buttons (step 1).
2. On click, update stored state and respond with step 2 card.
3. Repeat until completion.

## Pitfalls

- Webhooks can be delivered more than once; de-dupe by event ID if available.
- Avoid storing PII in logs.


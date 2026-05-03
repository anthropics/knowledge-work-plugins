# Button Actions (Chatbot API)

Buttons in message cards send a webhook when clicked.

## Pattern

1. You send a card with `actions.items[]` where each button has a unique `value`.
2. Zoom sends `interactive_message_actions` to your webhook.
3. Your handler routes based on that `value`.

## Routing Tip

Use stable action IDs like:

- `approve_request`
- `reject_request`
- `open_ticket:123`


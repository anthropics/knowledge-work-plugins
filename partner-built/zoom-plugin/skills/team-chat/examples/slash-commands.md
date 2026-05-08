# Slash Commands (Chatbot API)

Slash commands are configured on the Marketplace app and trigger webhook events.

## Pattern

1. Configure `/yourcommand` in the Chatbot feature settings.
2. User runs the command in Team Chat.
3. Your webhook receives `bot_notification` (or equivalent) with the command text.
4. Parse args and respond with a message card.

## Pitfalls

- Commands are account-scoped; make sure you're testing in the right account.
- Don’t rely on client-side parsing; parse on your server.


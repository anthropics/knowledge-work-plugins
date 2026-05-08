# Webhook Events (Chatbot API)

Common webhook event types you will handle:

- `bot_notification`: user messages your bot or triggers a command
- `interactive_message_actions`: user clicks a button
- `chat_message.submit`: user submits a form
- `bot_installed`: bot added to an account
- `app_deauthorized`: bot removed / app deauthorized

## Handler Checklist

- Verify the request (per Zoom's verification guidance).
- Parse payload carefully (treat as untrusted input).
- Route by event type and action values.
- Respond quickly; do heavy work async if needed.


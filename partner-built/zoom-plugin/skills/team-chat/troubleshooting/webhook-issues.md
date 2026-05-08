# Webhook Issues (Chatbot API)

## No Events Arriving

- Ensure your endpoint is publicly reachable over HTTPS.
- Confirm the correct app/account is installed and subscribed.
- Check verification settings (secret token, validation flow).

## Duplicate Events

- Webhooks can be delivered more than once.
- Add idempotency (store processed event IDs if available).


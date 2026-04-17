# Scheduled Alerts (Team Chat)

## Two Common Approaches

1. Team Chat API (as user):
   - Cron triggers, refresh user token, send message to a channel.
2. Chatbot API (as bot):
   - Cron triggers, request bot token, send message card.

## Pitfalls

- Don’t store tokens in plaintext.
- Ensure your cron job is idempotent (avoid duplicate messages).


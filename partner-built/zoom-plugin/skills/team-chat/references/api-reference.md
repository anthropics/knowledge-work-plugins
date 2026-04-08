# API Reference Pointers

This doc is intentionally lightweight; prefer the official REST reference for the authoritative schema.

## Team Chat API (user-level)

- Send message: `POST /v2/chat/users/me/messages`
- Typical needs:
  - list channels
  - post to channel / DM
  - thread replies

## Chatbot API (bot-level)

- Send bot message: `POST /v2/im/chat/messages`

## Notes

- If you see "invalid access token" errors, check:
  - app type (General App OAuth vs others)
  - scopes
  - whether the user re-consented after scope changes


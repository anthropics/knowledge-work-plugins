# Authentication Flows (Team Chat vs Chatbot)

Zoom Team Chat integrations commonly use one of two auth models:

## Team Chat API (user-level)

Use **User OAuth (authorization code)** when you want messages/actions to appear as a user.

- Typical endpoints:
  - Send message (as the user): `POST /v2/chat/users/me/messages`
- Typical scopes:
  - `chat_message:write`
  - `chat_channel:read` (for listing channels)

## Chatbot API (bot-level)

Use **client credentials** when you want messages/actions to appear as a bot.

- Typical endpoint:
  - Send bot message: `POST /v2/im/chat/messages`
- Typical “scope”:
  - `imchat:bot` (added by enabling Chatbot feature on the app)

## Decision Checklist

- If you need to post to a channel “as a bot” and handle slash command interactions: use **Chatbot API**.
- If you need to post “as the user” (and respect the user’s channel membership): use **Team Chat API**.

## Common Pitfalls

- **Server-to-Server OAuth** is not a fit for Zoom Team Chat chatbot features.
- Team Chat API calls require a user token with the right scopes; “invalid access token” errors are almost always missing scopes or wrong app type.
- OAuth URL split is easy to mix up:
  - authorize step: `https://zoom.us/oauth/authorize`
  - token step (all grant types): `https://zoom.us/oauth/token`
- In browser demos, complete OAuth end-to-end in app (state verify -> callback -> code exchange -> token store) to avoid copy/paste mistakes.

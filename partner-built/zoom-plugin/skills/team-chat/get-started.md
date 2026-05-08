# Team Chat Get Started

This is the fast path for Zoom Team Chat integrations.

## Step 1: Pick Integration Type First

- **User type** (Team Chat API)
  - Auth: `authorization_code` (User OAuth)
  - Endpoint family: `/v2/chat/users/...`
  - Messages appear as user

- **Bot type** (Chatbot API)
  - Auth: `client_credentials`
  - Endpoint family: `/v2/im/chat/messages`
  - Messages appear as bot

If this decision is wrong, auth/scopes/endpoints will all mismatch.

## Step 2: Set Up App + Credentials

1. Create **General App (OAuth)** in Zoom Marketplace.
2. Configure scopes and feature settings.
3. Gather credentials from app config:
   - `ZOOM_CLIENT_ID`
   - `ZOOM_CLIENT_SECRET`
   - `ZOOM_BOT_JID` (bot type)
   - `ZOOM_ACCOUNT_ID` (bot type use cases)

See: `concepts/environment-setup.md`

## Step 3A: User Type (Team Chat API)

1. Implement OAuth code flow.
2. Call `POST /v2/chat/users/me/messages` with bearer token.
3. Use OAuth endpoints correctly:
   - authorize: `https://zoom.us/oauth/authorize`
   - token exchange: `https://zoom.us/oauth/token`

See:
- `examples/oauth-setup.md`
- `examples/send-message.md`

## Step 3B: Bot Type (Chatbot API)

1. Get token via `grant_type=client_credentials`.
2. Call `POST /v2/im/chat/messages`.
3. Add webhook endpoint for interactive events.
4. Use `https://zoom.us/oauth/token` for `client_credentials` token requests.

See:
- `examples/chatbot-setup.md`
- `concepts/webhooks.md`
- `references/message-cards.md`

## Step 4: Validate with a Minimal Smoke Test

- User type: send one plain text channel message.
- Bot type: send one plain text bot message.

Then add advanced features (buttons/forms/slash commands).

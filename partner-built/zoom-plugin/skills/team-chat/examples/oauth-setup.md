# OAuth Setup (Team Chat API)

This is for the **Team Chat API** (user-level actions).

## What You Need

- App type: **General App (OAuth)**
- Redirect URL: your app's callback URL
- Scopes (typical):
  - `chat_message:write`
  - `chat_channel:read`

## Flow Summary

1. Redirect user to Zoom authorize URL.
2. Receive `code` at your redirect URL.
3. Exchange `code` for `access_token` + `refresh_token`.
4. Store tokens per-user.
5. Refresh the access token when it expires.

## In-App Web Flow Pattern (Recommended)

For browser demos, keep the whole flow in your app to avoid manual copy/paste mistakes:

1. User clicks **Connect Zoom User** in your UI.
2. Backend returns authorize URL (`https://zoom.us/oauth/authorize`) with a generated `state`.
3. Redirect browser to Zoom consent screen.
4. Callback route validates `state` and exchanges `code` at `https://zoom.us/oauth/token`.
5. Callback page stores token in app storage (for demo: localStorage, for production: server session/DB) and redirects back to app.

## Token Exchange (Server Side)

Pseudo-code (Node style):

```js
// POST https://zoom.us/oauth/token
// grant_type=authorization_code&code=...&redirect_uri=...
// Authorization: Basic base64(client_id:client_secret)
```

## Common Errors

- `Invalid redirect`: redirect URL mismatch between code exchange and Marketplace config.
- `Invalid access token, does not contain scopes`: missing scopes on the app or user didn't re-consent after scope change.

## Next

- `send-message.md` to post a message once you have a user token.
- `token-management.md` for refresh strategy.

# Zoom Phone Environment Variables

## Standard `.env` keys

| Variable | Required | Used for | Where to find |
| --- | --- | --- | --- |
| `ZOOM_CLIENT_ID` | Yes | OAuth app identity for Phone APIs | Zoom Marketplace -> General OAuth app -> App Credentials |
| `ZOOM_CLIENT_SECRET` | Yes | OAuth token exchange | Zoom Marketplace -> General OAuth app -> App Credentials |
| `ZOOM_REDIRECT_URI` | Yes (user OAuth) | OAuth callback URL | Zoom Marketplace -> OAuth redirect/allow list |
| `ZOOM_ACCOUNT_ID` | Optional (S2S patterns) | Account-level service integrations | Zoom Marketplace -> Server-to-Server OAuth app credentials |
| `ZOOM_WEBHOOK_SECRET` or `WEBHOOK_SECRET_TOKEN` | Recommended | Webhook signature verification | Zoom Marketplace -> Features -> Event Subscriptions -> Secret Token |
| `ZOOM_PHONE_SMART_EMBED_URL` | Optional | Smart Embed iframe URL override | Zoom Phone Smart Embed docs (`applications.zoom.us` path) |
| `ZOOM_PHONE_SMART_EMBED_ORIGIN` | Recommended | Allowed postMessage origin | Set to `https://applications.zoom.us` |

## Common runtime keys

- `NEXTAUTH_URL` (if using NextAuth)
- `NEXTAUTH_SECRET` (if using NextAuth)
- `PORT`
- `NODE_ENV`

## Notes

- Keep OAuth secrets server-side only.
- Smart Embed approved domains are configured in Marketplace app settings, not in `.env`.
- Re-authorize app after changing scopes.

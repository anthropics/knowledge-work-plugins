# Zoom Apps SDK Environment Variables

## Standard `.env` keys

| Variable | Required | Used for | Where to find |
| --- | --- | --- | --- |
| `ZOOM_APP_CLIENT_ID` | Yes | OAuth and app identity | Zoom Marketplace -> your Zoom App -> App Credentials |
| `ZOOM_APP_CLIENT_SECRET` | Yes | OAuth token exchange | Zoom Marketplace -> your Zoom App -> App Credentials |
| `ZOOM_APP_REDIRECT_URI` | Yes | OAuth callback URL | Zoom Marketplace -> your Zoom App -> OAuth allow list / redirect settings |
| `ZOOM_APP_URL` | Usually | URL loaded by Zoom client | Zoom Marketplace -> your Zoom App -> Basic Information (Development URL / Home URL) |
| `ZOOM_APP_BASE_URL` | Optional | Internal base URL alias | Set to your deployed app origin |
| `SESSION_SECRET` | Recommended | Session signing/encryption | Generate and manage in your own secret manager |

## Runtime-only values

- `ZOOM_ACCESS_TOKEN`
- `ZOOM_REFRESH_TOKEN`

Generate these during OAuth flow; do not hardcode them in repo files.

## Notes

- Keep `ZOOM_APP_CLIENT_SECRET` server-side only.
- Use separate development and production app credentials.

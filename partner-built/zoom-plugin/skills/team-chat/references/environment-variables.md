# Zoom Team Chat Environment Variables

## Standard `.env` keys

| Variable | Required | Used for | Where to find |
| --- | --- | --- | --- |
| `ZOOM_CLIENT_ID` | Yes | Team Chat app OAuth identity | Zoom Marketplace -> Team Chat app -> App Credentials |
| `ZOOM_CLIENT_SECRET` | Yes | OAuth token exchange | Zoom Marketplace -> Team Chat app -> App Credentials |
| `ZOOM_REDIRECT_URI` | OAuth code flow | Callback URL for installs/auth | Zoom Marketplace -> OAuth redirect/allow list |
| `ZOOM_BOT_JID` | Chatbot flows | Target bot identifier | Team Chat app/chatbot configuration after setup |
| `ZOOM_SECRET_TOKEN` | Recommended | Event/webhook signature verification | Zoom Marketplace -> Event Subscriptions -> Secret Token |
| `ZOOM_VERIFICATION_TOKEN` | Legacy only | Legacy verification path | Zoom Marketplace legacy fields (older apps) |

## Runtime-only values

- `ZOOM_ACCESS_TOKEN`
- `ZOOM_REFRESH_TOKEN`

## Notes

- Prefer secret-token signature verification over legacy verification token.

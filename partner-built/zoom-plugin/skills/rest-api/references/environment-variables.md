# Zoom REST API Environment Variables

## Standard `.env` keys

| Variable | Required | Used for | Where to find |
| --- | --- | --- | --- |
| `ZOOM_CLIENT_ID` | Yes | OAuth app identity for API access | Zoom Marketplace -> OAuth app -> App Credentials |
| `ZOOM_CLIENT_SECRET` | Yes | OAuth app secret | Zoom Marketplace -> OAuth app -> App Credentials |
| `ZOOM_ACCOUNT_ID` | S2S OAuth mode | Account token grant | Zoom Marketplace -> Server-to-Server OAuth app credentials |
| `ZOOM_REDIRECT_URI` | User OAuth mode | Authorization callback URL | Zoom Marketplace -> OAuth redirect/allow list |
| `ZOOM_WEBHOOK_SECRET` | If receiving events | Signature validation for webhook events | Zoom Marketplace -> Event Subscriptions -> Secret Token |

## Runtime-only values

- `ZOOM_ACCESS_TOKEN`
- `ZOOM_REFRESH_TOKEN`

## Notes

- Use `ZOOM_ACCOUNT_ID` for server-to-server service integrations.
- User-level integrations require authorization code flow and `ZOOM_REDIRECT_URI`.

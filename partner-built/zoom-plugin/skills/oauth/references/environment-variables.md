# Zoom OAuth Environment Variables

## Standard `.env` keys

| Variable | Required | Used for | Where to find |
| --- | --- | --- | --- |
| `ZOOM_CLIENT_ID` | Yes | OAuth client identity | Zoom Marketplace -> OAuth app -> App Credentials |
| `ZOOM_CLIENT_SECRET` | Yes | OAuth client secret | Zoom Marketplace -> OAuth app -> App Credentials |
| `ZOOM_REDIRECT_URI` | User-level OAuth | Authorization code callback | Zoom Marketplace -> OAuth redirect/allow list |
| `ZOOM_ACCOUNT_ID` | S2S OAuth | Account-level token grant | Zoom Marketplace -> Server-to-Server OAuth app credentials |

## Runtime-only values

- `ZOOM_AUTH_CODE`
- `ZOOM_ACCESS_TOKEN`
- `ZOOM_REFRESH_TOKEN`

Generate these at runtime and keep in secure storage.

## Notes

- Use S2S OAuth where user consent is not required.
- Use Authorization Code flow when acting on behalf of a Zoom user.

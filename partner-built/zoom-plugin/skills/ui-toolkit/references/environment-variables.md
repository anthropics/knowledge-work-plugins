# Zoom UI Toolkit (Video SDK) Environment Variables

## Standard `.env` keys

| Variable | Required | Used for | Where to find |
| --- | --- | --- | --- |
| `ZOOM_VIDEO_SDK_KEY` | Yes | Video SDK identity for token generation | Zoom Marketplace -> Video SDK app -> App Credentials |
| `ZOOM_VIDEO_SDK_SECRET` | Yes | Server-side token/signature generation | Zoom Marketplace -> Video SDK app -> App Credentials |
| `ZOOM_UI_TOOLKIT_BASE_URL` | Optional | App base URL used by your token service | Set to your deployed app origin |

## Runtime-only values

- `VIDEO_SDK_JWT`

Generate server-side and return short-lived tokens to the browser.

## Notes

- UI Toolkit depends on Video SDK auth; keep `ZOOM_VIDEO_SDK_SECRET` off the client.

# Zoom Video SDK Environment Variables

## Standard `.env` keys

| Variable | Required | Used for | Where to find |
| --- | --- | --- | --- |
| `ZOOM_VIDEO_SDK_KEY` | Yes | Video SDK app identity | Zoom Marketplace -> Video SDK app -> App Credentials |
| `ZOOM_VIDEO_SDK_SECRET` | Yes (server only) | Video SDK token/signature generation | Zoom Marketplace -> Video SDK app -> App Credentials |
| `VIDEO_SDK_TOKEN_ENDPOINT` | Yes | URL your clients call to fetch short-lived Video SDK token | Your backend deployment config |
| `VIDEO_SDK_BASE_URL` | Optional | Base URL for your app backend | Set to your deployed environment |
| `VIDEO_SDK_SESSION_NAME` | Runtime | Session/topic identifier | Created by your app workflow |
| `VIDEO_SDK_USER_NAME` | Runtime | Display name in session | App user profile/context |

## Runtime-only values

- `VIDEO_SDK_TOKEN` / `VIDEO_SDK_JWT` (short-lived; generated server-side)

## Notes

- Some older samples use `ZOOM_SDK_KEY`/`ZOOM_SDK_SECRET`; prefer explicit `ZOOM_VIDEO_SDK_*` names.
- Platform-specific variants:
  - [Android env vars](../android/references/environment-variables.md)
  - [iOS env vars](../ios/references/environment-variables.md)
  - [macOS env vars](../macos/references/environment-variables.md)
  - [Unity env vars](../unity/references/environment-variables.md)

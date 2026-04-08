# Cross-Product Environment Variables (Hub)

Use this file as a normalization map. Product-specific details are maintained in each product skill reference.

## Common `.env` keys

| Variable | Typical products | Where to find |
| --- | --- | --- |
| `ZOOM_CLIENT_ID` | OAuth, REST API, Team Chat, WebSockets, RTMS (OAuth mode), Contact Center APIs | Zoom Marketplace -> your app -> App Credentials |
| `ZOOM_CLIENT_SECRET` | OAuth, REST API, Team Chat, WebSockets, RTMS (OAuth mode), Contact Center APIs | Zoom Marketplace -> your app -> App Credentials |
| `ZOOM_ACCOUNT_ID` | Server-to-Server OAuth flows | Zoom Marketplace -> Server-to-Server OAuth app credentials |
| `ZOOM_REDIRECT_URI` | User-level OAuth apps | Zoom Marketplace -> OAuth redirect/allow list |
| `ZOOM_WEBHOOK_SECRET` / `WEBHOOK_SECRET_TOKEN` | Webhooks and event validation | Zoom Marketplace -> Event Subscriptions -> Secret Token |
| `ZOOM_SDK_KEY` / `ZOOM_SDK_SECRET` | Meeting SDK or SDK-based products | Zoom Marketplace -> SDK app credentials |
| `ZOOM_VIDEO_SDK_KEY` / `ZOOM_VIDEO_SDK_SECRET` | Video SDK and UI Toolkit | Zoom Marketplace -> Video SDK app credentials |
| `PROBE_JS_URL` / `PROBE_WASM_URL` | Probe SDK | Your app/CDN hosted Probe SDK assets (or bundler output paths) |
| `PROBE_DOMAIN` / `PROBE_CONNECT_TIMEOUT_MS` | Probe SDK | Product policy + Probe SDK diagnostics configuration |

## Product references

- [../../zoom-apps-sdk/references/environment-variables.md](../../zoom-apps-sdk/references/environment-variables.md)
- [../../cobrowse-sdk/references/environment-variables.md](../../cobrowse-sdk/references/environment-variables.md)
- [../../meeting-sdk/references/environment-variables.md](../../meeting-sdk/references/environment-variables.md)
- [../../oauth/references/environment-variables.md](../../oauth/references/environment-variables.md)
- [../../rest-api/references/environment-variables.md](../../rest-api/references/environment-variables.md)
- [../../rtms/references/environment-variables.md](../../rtms/references/environment-variables.md)
- [../../team-chat/references/environment-variables.md](../../team-chat/references/environment-variables.md)
- [../../ui-toolkit/references/environment-variables.md](../../ui-toolkit/references/environment-variables.md)
- [../../video-sdk/references/environment-variables.md](../../video-sdk/references/environment-variables.md)
- [../../webhooks/references/environment-variables.md](../../webhooks/references/environment-variables.md)
- [../../websockets/references/environment-variables.md](../../websockets/references/environment-variables.md)
- [../../contact-center/references/environment-variables.md](../../contact-center/references/environment-variables.md)
- [../../phone/references/environment-variables.md](../../phone/references/environment-variables.md)
- [../../probe-sdk/references/environment-variables.md](../../probe-sdk/references/environment-variables.md)

## Probe SDK note

- Probe SDK core diagnostics do not require Zoom OAuth/Marketplace credentials.

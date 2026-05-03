# Zoom Phone Architecture and Lifecycle

## Architecture

```text
User/Agent UI
  |
  | (A) Smart Embed postMessage events
  v
Smart Embed Iframe (applications.zoom.us)
  |
  | event stream + call controls
  v
CRM Web App (event bridge + UI state)
  |
  | OAuth token on server only
  v
Backend API Layer
  |\
  | \-- Zoom Phone REST APIs (call history, call handling, contacts)
  |
  \---- Webhook endpoint (phone.* events)
```

## Lifecycle Workflow

1. Provision:
- Account has Zoom Phone and optional SMS enablement.

2. Authorize:
- OAuth app installed and scoped for required Phone operations.

3. Initialize UI:
- Load Smart Embed iframe/script.
- Wait for `onZoomPhoneIframeApiReady`.
- Send `zp-init-config` and register event handlers.

4. Engage:
- Start calls/SMS via `zp-make-call` or `zp-input-sms`.
- Receive events (`zp-call-*`, `zp-sms-log-event`, optional AI/contact/notes events).

5. Persist:
- Save event snapshots keyed by `callId`.
- Reconcile to call history/call element records after completion.

6. Post-call:
- Save call notes/disposition and optional recording/voicemail links.

7. Operate:
- Track deprecations and apply endpoint/event mapping updates.

## Version Drift Strategy

- Normalize inbound payloads in one adapter layer.
- Keep endpoint constants centralized by version target.
- Feature-flag optional payload fields.
- Keep webhook + Smart Embed event handlers tolerant to added fields and enum expansion.

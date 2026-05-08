# Zoom Phone 5-Minute Preflight Runbook

Use this before deep debugging.

## 1) Confirm Product Prerequisites

- Zoom Phone licenses assigned.
- Admin access available for Phone settings.
- If SMS is required, 10DLC/SMS setup is complete.

## 2) Confirm App and OAuth

- App type: General OAuth app for user/admin flows.
- Redirect URI and allow list are exact and current.
- Required Phone scopes are added.
- App is installed/re-authorized after scope changes.

## 3) Confirm Integration Surface

- Smart Embed: iframe/script loaded and approved domain configured.
- API/Webhook: access token valid and webhook endpoint reachable.
- URI launch: endpoint uses supported scheme and client is signed in.

## 4) Confirm Event/Data Correlation

- Persist `call_id` for real-time events.
- Persist `call_history_uuid` and `call_element_id` for post-call lookup.
- Keep idempotency logic for duplicate event deliveries.

## 5) Confirm Migration Posture

- Do not build new features on legacy v1 call logs.
- Webhook consumers are ready for `call_element` event names/fields.
- Field-mapping adapter exists for old/new payload shapes.

## 6) Confirm Security Controls

- Smart Embed `postMessage` enforces trusted origin.
- Webhook signatures validated with secret token.
- OAuth secrets are server-side only.

## 7) Fast Decision Tree

- Smart Embed iframe visible but no events -> missing init sequence or bad origin filtering.
- OAuth works but API fails with 401/403 -> scope mismatch or stale authorization.
- Data pipeline breaks after endpoint/event upgrade -> missing v2/v3 field mapping.
- URI click does nothing -> unsupported platform/client state, or wrong scheme.

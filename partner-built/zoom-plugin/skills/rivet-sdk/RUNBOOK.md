# Rivet SDK 5-Minute Preflight Runbook

Use this before deep debugging.

## Skill Doc Standard Note

- Skill entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- SDK/API names can drift by version; validate names against changelog and TypeDoc before release.

## 1) Confirm Integration Surface

- Confirm this is a server-side Node.js integration path using `@zoom/rivet`.
- Confirm module boundaries (Chatbot, Team Chat, Meetings, Phone, Accounts, Users, Video SDK).
- Confirm whether the app needs event receiver mode, API-only mode, or both.

## 2) Confirm Required Credentials

- `clientId`, `clientSecret` for each module auth flow.
- `webhooksSecretToken` for webhook verification (required for receiver flows).
- `accountId` for S2S modules.
- `redirectUri` and `stateStore` for User OAuth modules.

## 3) Confirm Lifecycle Order

1. Instantiate module client(s) with auth/receiver options.
2. Register webhook listeners before traffic.
3. Start client server(s) and note per-module port(s).
4. Expose `/zoom/events` for each active receiver endpoint.
5. Execute API calls through `client.endpoints.*`.

## 4) Confirm Event/State Handling

- Match event names exactly (`bot_notification`, `interactive_message_fields_editable`, etc.).
- Keep module-specific webhook endpoints aligned with Marketplace subscription settings.
- Persist OAuth tokens/state for long-lived integrations.
- Keep idempotency in event handlers for retries/duplicates.

## 5) Confirm Cleanup + Upgrade Posture

- Revalidate all module constructors and options on each upgrade.
- Keep compatibility shims when module/type names change.
- Review changelog version-by-version from current deployment to target.

## 6) Quick Probes

- Client starts and binds to expected port(s).
- Webhook verification succeeds for subscribed events.
- One API call and one event callback complete successfully for each active module.
- User OAuth install/callback flow works end-to-end when applicable.

## 7) Fast Decision Tree

- API works but events fail -> wrong endpoint URL/port/path (`/zoom/events`) or bad webhook token.
- OAuth install fails -> redirect URI/state store mismatch or unsupported receiver mode.
- Multi-module collisions -> duplicate ports or shared env keys incorrectly mapped.
- Lambda flow issues -> receiver type mismatch or missing `webhooksSecretToken`.

## 8) Source Checkpoints

### Official docs

- https://developers.zoom.us/docs/rivet/
- https://developers.zoom.us/docs/rivet/javascript/
- https://zoom.github.io/rivet-javascript/

### Raw docs in repo

- `tools/zoom-crawler/raw-docs/developers.zoom.us/docs/rivet/`
- `tools/zoom-crawler/raw-docs/zoom.github.io/rivet-javascript/`

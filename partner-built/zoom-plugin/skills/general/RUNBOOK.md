# General Skill 5-Minute Preflight Runbook

Use this before deep debugging.

## Skill Doc Standard Note

- Skill entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- SDK/API names can drift by version; validate current names against docs/raw-docs before release.

## 1) Confirm Integration Surface

- Use `general` as the routing hub for cross-product intent selection.
- Confirm each use-case links to the correct product skill chain.
- Use this runbook before troubleshooting multi-product integrations.

## 2) Confirm Required Credentials

- Validate OAuth model selection (User OAuth vs Server-to-Server OAuth) before implementation.
- Ensure required scopes are documented in each use-case.
- Keep credential storage server-side; only expose short-lived tokens to clients.

## 3) Confirm Lifecycle Order

1. Pick product path (`REST`, `Meeting SDK`, `Video SDK`, `Apps SDK`, `Phone`, `Contact Center`, etc.).
2. Map auth flow and required scopes.
3. Define event model (`webhooks` or `websockets`) and correlation IDs.
4. Validate deployment model and operational monitoring requirements.

## 4) Confirm Event/State Handling

- Keep use-case assumptions explicit when combining multiple products.
- Store cross-system identifiers (meeting/session/call/engagement IDs) for traceability.
- Document fallback behavior when API names/fields drift between versions.

## 5) Confirm Cleanup + Upgrade Posture

- Remove stale route links whenever skills are renamed or moved.
- Keep `.env` key references centralized in environment variable reference docs.
- Refresh compatibility notes after each major SDK/API update cycle.

## 6) Quick Probes

- Routing matrix still points to existing `SKILL.md` files.
- Use-cases include at least one concrete implementation chain.
- OAuth/scopes guidance matches current Marketplace app model.

## 7) Fast Decision Tree

- Unsure between Meeting SDK and Video SDK -> route by UX model (Zoom meeting UI vs fully custom session).
- Need lowest-latency events -> use websockets; otherwise webhooks are acceptable.
- Scope/auth failures in execution -> pause and re-authorize with correct app type and scopes.

## 8) Source Checkpoints

### Official docs

- https://developers.zoom.us/
- https://marketplace.zoom.us/
- https://devforum.zoom.us/

### Raw docs in repo

- `raw-docs/developers.zoom.us/docs/`
- `raw-docs/marketplacefront.zoom.us/sdk/`

# UI Toolkit 5-Minute Preflight Runbook

Use this before deep debugging. It catches the most common UI Toolkit failures quickly.

## Skill Doc Standard Note

- Agent-skill standard entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- `SKILL.md` is also a navigation convention for larger skill docs.

## 1) Confirm Token Source

- UI Toolkit still needs Video SDK JWT.
- Generate JWT server-side only (never expose SDK secret client-side).

## 2) Confirm Basic Config

- `videoSDKJWT`, `sessionName`, `userName` must be present.
- Verify enabled features match your expected UI behavior.

## 3) Confirm Framework Constraints

- Validate your installed package peer dependencies (React version mismatch is common).
- In SSR frameworks, load toolkit client-side and clean up on unmount.

## 4) Confirm CSS and Lifecycle

- Ensure toolkit CSS is loaded.
- Call `closeSession`/`destroy` on teardown to avoid stale UI state.

## 5) Confirm Deployment Paths

- In basePath/subpath deployments, verify API route URLs and asset paths.
- If API returns HTML instead of JSON, re-check route mapping/proxy.

## 6) Quick Probes

- Token endpoint returns JSON token.
- `joinSession` succeeds and session events fire.
- Closing session cleans up container without errors.

### Copy/Paste Validation Commands

```bash
# 1) Verify token endpoint responds with JSON
curl -sS -i "$UI_TOOLKIT_BASE_URL/api/token"

# 2) Verify app route is reachable
curl -sS -i "$UI_TOOLKIT_BASE_URL"
```

Expected: valid JSON for token endpoint and valid HTML for app route.

## 7) Fast Decision Tree

- **Session won't join** -> invalid/missing JWT or bad session config.
- **UI partially broken** -> missing CSS or unsupported feature config.
- **Works local, fails prod** -> basePath/proxy mismatch.

## 8) SDK Selection Guardrail

- Use UI Toolkit for low-code prebuilt Video SDK UI.
- Use raw Video SDK for full custom rendering and control.

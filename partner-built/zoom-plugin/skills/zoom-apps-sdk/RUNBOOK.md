# Zoom Apps SDK 5-Minute Preflight Runbook

Use this before deep debugging. It catches common Zoom Apps integration failures quickly.

## Skill Doc Standard Note

- Agent-skill standard entrypoint is `SKILL.md`.
- This runbook is an operational convention (recommended), not a required skill file.
- `SKILL.md` is also a navigation convention for larger skill docs.

## 1) Confirm App Type and Context

- App type must be Zoom App in Marketplace.
- Confirm expected running context (`inMeeting`, `inMainClient`, `inWebinar`, etc.).

Context mismatch often looks like missing APIs.

## 2) Confirm Domain Allowlist

- Whitelist the exact dev/prod domains used by your app.
- If app panel is blank or refuses to load, domain allowlist is first check.

### Blank Panel Triage (60s)

- Confirm app URL is HTTPS and reachable directly in a browser.
- Confirm the exact host is allowlisted in Marketplace (including subdomain differences).
- Confirm no redirect loop (watch network tab for repeated 30x responses).
- Confirm CSP/X-Frame-Options do not block Zoom embedded browser usage.
- Confirm local tunnel URL in app config matches current active tunnel.

## 3) Confirm In-Client OAuth Setup

- Use correct redirect/callback handling for Zoom Apps flow.
- Validate state/PKCE handling if implemented.
- Confirm scopes and re-authorize after scope changes.

## 4) Confirm SDK Capability Usage

- Call APIs only when supported in current context/capability set.
- Inspect initialization and capability negotiation results.

### Capability Probe Snippet

Use this early in app startup to avoid calling unavailable APIs:

```javascript
import zoomSdk from '@zoom/appssdk';

async function probeSdk() {
  const config = await zoomSdk.config({
    capabilities: [
      'getSupportedJsApis',
      'getRunningContext',
      'authorize',
      'openUrl',
      'shareApp',
    ],
  });

  console.log('runningContext:', config.runningContext);
  console.log('supportedApis:', config.supportedApis || []);

  const supported = new Set(config.supportedApis || []);
  if (!supported.has('authorize')) {
    console.warn('authorize API unavailable in this context/capability set');
  }
}
```

## 5) Confirm Local Development Tunnel

- Use stable HTTPS tunnel (ngrok or equivalent).
- Update Marketplace config when tunnel URL changes.

## 6) Quick Probes

- App loads inside Zoom client without blank panel.
- SDK init succeeds and returns expected capabilities.
- OAuth flow completes and API calls work with granted scopes.

### Copy/Paste Validation Commands

```bash
# 1) Verify app URL is reachable and returns HTML
curl -sS -i "$ZOOM_APP_URL"

# 2) Verify OAuth callback URL is reachable
curl -sS -i "$ZOOM_APP_CALLBACK_URL"

# 3) Verify backend token/config endpoint returns JSON
curl -sS -i "$ZOOM_APP_BASE_URL/api/config"
```

Expected: HTTP 200/3xx and valid HTML/JSON (not generic 404/502 pages).

## 7) Fast Decision Tree

- **Blank panel** -> domain allowlist, HTTPS, CSP headers.
- **API unavailable** -> wrong running context or capability not granted.
- **OAuth loop/failure** -> redirect/state/scope mismatch.

## 8) SDK Selection Guardrail

- Use **Zoom Apps SDK** when app runs inside Zoom client contexts.
- Use **Meeting SDK** when embedding Zoom meeting UI into your own website/app.
- If you are debugging "missing Zoom Apps APIs" in a standalone browser page, you are likely in the wrong SDK/runtime.

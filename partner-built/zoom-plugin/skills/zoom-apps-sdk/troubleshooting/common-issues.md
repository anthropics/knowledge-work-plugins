# Common Issues

Quick diagnostics for Zoom Apps SDK problems.

## Diagnostic Table

| Issue | Cause | Solution |
|-------|-------|----------|
| App shows blank panel | Domain not in allowlist | Marketplace > Feature > Add Allow List > add your domain |
| `zoomSdk is not defined` | SDK script not loaded | Add `<script src="https://appssdk.zoom.us/sdk.js"></script>` |
| `SyntaxError: redeclaration of non-configurable global property` | Declared `let zoomSdk` | Use `let sdk = window.zoomSdk` instead |
| `config()` throws error | Not running in Zoom client | Wrap in try/catch, show browser fallback UI |
| `config()` hangs forever | SDK not initialized | Add 3-second timeout fallback |
| API call fails silently | Missing OAuth scope | Add required scopes in Marketplace > Scopes tab |
| `authorize()` doesn't work | Wrong OAuth flow | Use In-Client OAuth: `authorize()` + `onAuthorized` |
| `postMessage` not received | Instances not connected | Call `connect()` first, wait for `onConnect` |
| `runRenderingContext` fails | Missing capability | Add `'runRenderingContext'` to config() capabilities |
| App works then stops | Tunnel URL changed (ngrok/cloudflared/etc.) | Update every Marketplace URL that points at your tunnel domain (home page, redirect URLs, etc.) |
| CORS errors | Backend URL mismatch | Ensure frontend fetches from same-origin or configure CORS |
| Cookies not persisting | Wrong cookie settings | Set `sameSite: 'none', secure: true` |
| OAuth token exchange 400 | Wrong redirect URI | Ensure redirect URI matches exactly in Marketplace and code |
| 403 from Zoom REST API | Token expired | Implement token refresh with `refresh_token` |
| App loads in browser but not in Zoom | CSP headers wrong | Add `frame-ancestors 'self' zoom.us *.zoom.us` |
| `unsupportedApis` contains your API | Old Zoom client | User needs to update Zoom client |
| Collaborate/Layers APIs missing | Host privileges or client/version mismatch | Check `unsupportedApis` + `clientVersion`; ensure required features enabled in Marketplace; test as meeting host where required |
| drawImage fails in camera mode | CEF not ready | Add retry with exponential backoff (see camera-mode example) |

## Error Codes

Common SDK error codes from `config()` and API calls:

| Code | Meaning | Fix |
|------|---------|-----|
| `INVALID_PARAMETERS` | Wrong argument format | Check API docs for correct parameter shape |
| `NOT_SUPPORTED` | API not available in this context | Check running context and unsupportedApis |
| `PERMISSION_DENIED` | Missing capability or scope | Add to config() capabilities AND Marketplace scopes |
| `INTERNAL_ERROR` | SDK internal failure | Retry, check Zoom client version |
| `NOT_CONFIGURED` | config() not called yet | Call config() before any other SDK method |

## Quick Diagnostic Workflow

```
App doesn't work?
    │
    ├─ Blank panel, no errors?
    │       └─ Domain allowlist. Check Marketplace > Feature > Add Allow List
    │
    ├─ JavaScript error in console?
    │       ├─ "redeclaration" → Use `let sdk = window.zoomSdk`
    │       ├─ "not defined" → SDK script not loaded
    │       └─ "not configured" → Call config() first
    │
    ├─ config() fails?
    │       ├─ In browser → Expected. Not running in Zoom.
    │       └─ In Zoom → Check capabilities match scopes
    │
    ├─ API call returns error?
    │       ├─ PERMISSION_DENIED → Add scope in Marketplace
    │       ├─ NOT_SUPPORTED → Wrong running context
    │       └─ INVALID_PARAMETERS → Check argument format
    │
    └─ Works locally, fails after deploy?
            ├─ Domain allowlist updated?
            ├─ HTTPS configured?
            └─ Cookies: SameSite=None, Secure=true?
```

## Enable SDK Debug Logging

```javascript
// Check supported APIs at runtime
const { supportedApis } = await zoomSdk.getSupportedJsApis();
console.log('Supported APIs:', supportedApis);

// Check what was unsupported after config
const config = await zoomSdk.config({...});
console.log('Unsupported:', config.unsupportedApis);
console.log('Client version:', config.clientVersion);
console.log('Running context:', config.runningContext);
```

## Resources

- **Debugging guide**: [debugging.md](debugging.md)
- **Migration guide**: [migration.md](migration.md)

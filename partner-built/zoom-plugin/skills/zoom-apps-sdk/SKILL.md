---
name: zoom-apps-sdk
description: Reference skill for Zoom Apps SDK. Use after routing to an in-client app workflow when building web apps that run inside Zoom meetings, webinars, the main client, or Zoom Phone.
user-invocable: false
triggers:
  - "zoom app"
  - "in-meeting app"
  - "app inside zoom"
  - "zoom client app"
  - "layers api"
  - "immersive mode"
  - "camera mode"
  - "collaborate mode"
  - "appssdk"
  - "in-client oauth"
  - "zoom mail"
  - "domain allowlist"
  - "domain whitelist"
  - "url whitelisting"
  - "blank panel"
  - "runningContext"
  - "zoomSdk"
---

# Zoom Apps SDK

Background reference for web apps that run inside the Zoom client. Prefer `choose-zoom-approach` first, then route here for Layers API, Collaborate Mode, in-client OAuth, and runtime constraints.

# Zoom Apps SDK

Build web apps that run inside the Zoom client - meetings, webinars, main client, and Zoom Phone.

**Official Documentation**: https://developers.zoom.us/docs/zoom-apps/
**SDK Reference**: https://appssdk.zoom.us/
**NPM Package**: https://www.npmjs.com/package/@zoom/appssdk

## Quick Links

**New to Zoom Apps? Follow this path:**

1. **[Architecture](concepts/architecture.md)** - Frontend/backend pattern, embedded browser, deep linking
2. **[Quick Start](examples/quick-start.md)** - Complete working Express + SDK app
3. **[Running Contexts](concepts/running-contexts.md)** - Where your app runs (inMeeting, inMainClient, etc.)
4. **[Zoom Apps vs Meeting SDK](concepts/meeting-sdk-vs-zoom-apps.md)** - Stop mixing app types
4. **[In-Client OAuth](examples/in-client-oauth.md)** - Seamless authorization with PKCE
5. **[API Reference](references/apis.md)** - 100+ SDK methods
6. **Integrated Index** - see the section below in this file
7. **[5-Minute Runbook](RUNBOOK.md)** - Preflight checks before deep debugging

**Reference:**
- **[API Reference](references/apis.md)** - All SDK methods by category
- **[Events Reference](references/events.md)** - All SDK event listeners
- **[Layers API](references/layers-api.md)** - Immersive and camera mode rendering
- **[OAuth Reference](references/oauth.md)** - OAuth flows for Zoom Apps
- **[Zoom Mail](references/zmail-sdk.md)** - Mail plugin integration

**Having issues?**
- App won't load in Zoom → Check [Domain Allowlist](#url-whitelisting-required) below
- SDK errors → [Common Issues](troubleshooting/common-issues.md)
- Local dev setup → [Debugging Guide](troubleshooting/debugging.md)
- Version upgrade → [Migration Guide](troubleshooting/migration.md)
- Forum-derived FAQs → [Forum Top Questions](troubleshooting/forum-top-questions.md)

**Building immersive experiences?**
- [Layers Immersive Mode](examples/layers-immersive.md) - Custom video layouts
- [Camera Mode](examples/layers-camera.md) - Virtual camera overlays

> **Need help with OAuth?** See the **[zoom-oauth](../oauth/SKILL.md)** skill for authentication flows.

## SDK Overview

The Zoom Apps SDK (`@zoom/appssdk`) provides JavaScript APIs for web apps running in Zoom's embedded browser:

- **Context APIs** - Get meeting, user, and participant info
- **Meeting Actions** - Share app, invite participants, open URLs
- **Authorization** - In-Client OAuth with PKCE (no browser redirect)
- **Layers API** - Immersive video layouts and camera mode overlays
- **Collaborate Mode** - Shared app state across participants
- **App Communication** - Message passing between app instances (main client <-> meeting)
- **Media Controls** - Virtual backgrounds, camera listing, recording control
- **UI Controls** - Expand app, notifications, popout
- **Events** - React to meeting state, participants, sharing, and more

## Prerequisites

- Zoom app configured as **"Zoom App"** type in [Marketplace](https://marketplace.zoom.us/)
- OAuth credentials (Client ID + Secret) with Zoom Apps scopes
- Web application (Node.js + Express recommended)
- **Your domain whitelisted** in Marketplace domain allowlist
- ngrok or HTTPS tunnel for local development
- Node.js 18+ (for the backend server)

## Quick Start

### Option A: NPM (Recommended for frameworks)

```bash
npm install @zoom/appssdk
```

```javascript
import zoomSdk from '@zoom/appssdk';

async function init() {
  try {
    const configResponse = await zoomSdk.config({
      capabilities: [
        'shareApp',
        'getMeetingContext',
        'getUserContext',
        'openUrl'
      ],
      version: '0.16'
    });

    console.log('Running context:', configResponse.runningContext);
    // 'inMeeting' | 'inMainClient' | 'inWebinar' | 'inImmersive' | ...

    const context = await zoomSdk.getMeetingContext();
    console.log('Meeting ID:', context.meetingID);
  } catch (error) {
    console.error('Not running inside Zoom:', error.message);
    showDemoMode();
  }
}
```

### Option B: CDN (Vanilla JS)

```html
<script src="https://appssdk.zoom.us/sdk.js"></script>

<script>
// CRITICAL: Do NOT declare "let zoomSdk" - the SDK defines window.zoomSdk globally
// Using "let zoomSdk = ..." causes: SyntaxError: redeclaration of non-configurable global property
let sdk = window.zoomSdk;  // Use a different variable name

async function init() {
  try {
    const configResponse = await sdk.config({
      capabilities: ['shareApp', 'getMeetingContext', 'getUserContext'],
      version: '0.16'
    });

    console.log('Running context:', configResponse.runningContext);
  } catch (error) {
    console.error('Not running inside Zoom:', error.message);
    showDemoMode();
  }
}

function showDemoMode() {
  document.body.innerHTML = '<h1>Preview Mode</h1><p>Open this app inside Zoom to use.</p>';
}

document.addEventListener('DOMContentLoaded', () => {
  init();
  setTimeout(() => { if (!sdk) showDemoMode(); }, 3000);
});
</script>
```

## Critical: Global Variable Conflict

The CDN script defines `window.zoomSdk` globally. **Do NOT redeclare it:**

```javascript
// WRONG - causes SyntaxError in Zoom's embedded browser
let zoomSdk = null;
zoomSdk = window.zoomSdk;

// CORRECT - use different variable name
let sdk = window.zoomSdk;

// ALSO CORRECT - NPM import (no conflict)
import zoomSdk from '@zoom/appssdk';
```

This only applies to the CDN approach. The NPM import creates a module-scoped variable, no conflict.

## Browser Preview / Demo Mode

The SDK only functions inside the Zoom client. When accessed in a regular browser:
- `window.zoomSdk` exists but `sdk.config()` throws an error
- Always implement try/catch with fallback UI
- Add timeout (3 seconds) in case SDK hangs

## URL Whitelisting (Required)

**Your app will NOT load in Zoom unless the domain is whitelisted.**

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Open your app -> **Feature** tab
3. Under **Zoom App**, find **Add Allow List**
4. Add your domain (e.g., `yourdomain.com` for production, `xxxxx.ngrok.io` for dev)

Without this, the Zoom client shows a blank panel with no error message.

## OAuth Scopes (Required)

Capabilities require matching OAuth scopes enabled in Marketplace:

| Capability | Required Scope |
|------------|----------------|
| `getMeetingContext` | `zoomapp:inmeeting` |
| `getUserContext` | `zoomapp:inmeeting` |
| `shareApp` | `zoomapp:inmeeting` |
| `openUrl` | `zoomapp:inmeeting` |
| `sendAppInvitation` | `zoomapp:inmeeting` |
| `runRenderingContext` | `zoomapp:inmeeting` |
| `authorize` | `zoomapp:inmeeting` |
| `getMeetingParticipants` | `zoomapp:inmeeting` |

**To add scopes:** Marketplace -> Your App -> **Scopes** tab -> Add required scopes.

Missing scopes = capability fails silently or throws error. Users must re-authorize if you add new scopes.

## Running Contexts

Your app runs in different surfaces within Zoom. The `configResponse.runningContext` tells you where:

| Context | Surface | Description |
|---------|---------|-------------|
| `inMeeting` | Meeting sidebar | Most common. Full meeting APIs available |
| `inMainClient` | Main client panel | Home tab. No meeting context APIs |
| `inWebinar` | Webinar sidebar | Host/panelist. Meeting + webinar APIs |
| `inImmersive` | Layers API | Full-screen custom rendering |
| `inCamera` | Camera mode | Virtual camera overlay |
| `inCollaborate` | Collaborate mode | Shared state context |
| `inPhone` | Zoom Phone | Phone call app |
| `inChat` | Team Chat | Chat sidebar |

See **[Running Contexts](concepts/running-contexts.md)** for context-specific behavior and APIs.

## SDK Initialization Pattern

Every Zoom App starts with `config()`:

```javascript
import zoomSdk from '@zoom/appssdk';

const configResponse = await zoomSdk.config({
  capabilities: [
    // List ALL APIs you will use
    'getMeetingContext',
    'getUserContext',
    'shareApp',
    'openUrl',
    'authorize',
    'onAuthorized'
  ],
  version: '0.16'
});

// configResponse contains:
// {
//   runningContext: 'inMeeting',
//   clientVersion: '5.x.x',
//   unsupportedApis: []  // APIs not supported in this client version
// }
```

**Rules:**
1. `config()` MUST be called before any other SDK method
2. Only capabilities listed in `config()` are available
3. Capabilities must match OAuth scopes in Marketplace
4. Check `unsupportedApis` for graceful degradation

## In-Client OAuth (Summary)

Best UX for authorization - no browser redirect:

```javascript
// 1. Get code challenge from your backend
const { codeChallenge, state } = await fetch('/api/auth/challenge').then(r => r.json());

// 2. Trigger in-client authorization
await zoomSdk.authorize({ codeChallenge, state });

// 3. Listen for authorization result
zoomSdk.addEventListener('onAuthorized', async (event) => {
  const { code, state } = event;
  // 4. Send code to backend for token exchange
  await fetch('/api/auth/token', {
    method: 'POST',
    body: JSON.stringify({ code, state })
  });
});
```

See **[In-Client OAuth Guide](examples/in-client-oauth.md)** for complete implementation.

## Layers API (Summary)

Build immersive video layouts and camera overlays:

```javascript
// Start immersive mode - replaces gallery view
await zoomSdk.runRenderingContext({ view: 'immersive' });

// Position participant video feeds
await zoomSdk.drawParticipant({
  participantUUID: 'user-uuid',
  x: 0, y: 0, width: 640, height: 480, zIndex: 1
});

// Add overlay images
await zoomSdk.drawImage({
  imageData: canvas.toDataURL(),
  x: 0, y: 0, width: 1280, height: 720, zIndex: 0
});

// Exit immersive mode
await zoomSdk.closeRenderingContext();
```

See **[Layers Immersive](examples/layers-immersive.md)** and **[Camera Mode](examples/layers-camera.md)**.

## Environment Variables

| Variable | Description | Where to Find |
|----------|-------------|---------------|
| `ZOOM_APP_CLIENT_ID` | App client ID | Marketplace -> App -> App Credentials |
| `ZOOM_APP_CLIENT_SECRET` | App client secret | Marketplace -> App -> App Credentials |
| `ZOOM_APP_REDIRECT_URI` | OAuth redirect URL | Your server URL + `/auth` |
| `SESSION_SECRET` | Cookie signing secret | Generate random string |
| `ZOOM_HOST` | Zoom host URL | `https://zoom.us` (or `https://zoomgov.com`) |

## Common APIs

| API | Description |
|-----|-------------|
| `config()` | Initialize SDK, request capabilities |
| `getMeetingContext()` | Get meeting ID, topic, status |
| `getUserContext()` | Get user name, role, participant ID |
| `getRunningContext()` | Get current running context |
| `getMeetingParticipants()` | List participants |
| `shareApp()` | Share app screen with participants |
| `openUrl({ url })` | Open URL in external browser |
| `sendAppInvitation()` | Invite users to open your app |
| `authorize()` | Trigger In-Client OAuth |
| `connect()` | Connect to other app instances |
| `postMessage()` | Send message to connected instances |
| `runRenderingContext()` | Start Layers API (immersive/camera) |
| `expandApp({ action })` | Expand/collapse app panel |
| `showNotification()` | Show notification in Zoom |

## Complete Documentation Library

### Core Concepts
- **[Architecture](concepts/architecture.md)** - Frontend/backend pattern, embedded browser, deep linking, X-Zoom-App-Context
- **[Running Contexts](concepts/running-contexts.md)** - All contexts, context-specific APIs, multi-instance communication
- **[Security](concepts/security.md)** - OWASP headers, CSP, cookie security, PKCE, token storage

### Complete Examples
- **[Quick Start](examples/quick-start.md)** - Hello World Express + SDK app
- **[In-Client OAuth](examples/in-client-oauth.md)** - PKCE authorization flow
- **[Layers Immersive](examples/layers-immersive.md)** - Custom video layouts
- **[Camera Mode](examples/layers-camera.md)** - Virtual camera overlays
- **[Collaborate Mode](examples/collaborate-mode.md)** - Shared state across participants
- **[Guest Mode](examples/guest-mode.md)** - Unauthenticated/authenticated/authorized states
- **[Breakout Rooms](examples/breakout-rooms.md)** - Room detection and cross-room state
- **[App Communication](examples/app-communication.md)** - connect + postMessage between instances

### Troubleshooting
- **[Common Issues](troubleshooting/common-issues.md)** - Quick diagnostics and error codes
- **[Debugging](troubleshooting/debugging.md)** - Local dev, ngrok, browser preview
- **[Migration](troubleshooting/migration.md)** - SDK version upgrade notes

### References
- **[API Reference](references/apis.md)** - All 100+ SDK methods
- **[Events Reference](references/events.md)** - All SDK event listeners
- **[Layers API Reference](references/layers-api.md)** - Drawing and rendering methods
- **[OAuth Reference](references/oauth.md)** - OAuth flows for Zoom Apps
- **[Zoom Mail](references/zmail-sdk.md)** - Mail plugin integration

## Sample Repositories

### Official (by Zoom)

| Repository | Type | Last Updated | Status | SDK Version |
|-----------|------|-------------|--------|-------------|
| [zoomapps-sample-js](https://github.com/zoom/zoomapps-sample-js) | Hello World (Vanilla JS) | Dec 2025 | Active | ^0.16.26 |
| [zoomapps-advancedsample-react](https://github.com/zoom/zoomapps-advancedsample-react) | Advanced (React + Redis) | Oct 2025 | Active | 0.16.0 |
| [zoomapps-customlayout-js](https://github.com/zoom/zoomapps-customlayout-js) | Layers API | Nov 2023 | Stale | ^0.16.8 |
| [zoomapps-texteditor-vuejs](https://github.com/zoom/zoomapps-texteditor-vuejs) | Collaborate (Vue + Y.js) | Oct 2023 | Stale | ^0.16.7 |
| [zoomapps-serverless-vuejs](https://github.com/zoom/zoomapps-serverless-vuejs) | Serverless (Firebase) | Aug 2024 | Stale | ^0.16.21 |
| [zoomapps-cameramode-vuejs](https://github.com/zoom/zoomapps-cameramode-vuejs) | Camera Mode | - | - | - |
| [zoomapps-workshop-sample](https://github.com/zoom/zoomapps-workshop-sample) | Workshop | - | - | - |

**Recommended for new projects:** Use `@zoom/appssdk` version `^0.16.26`.

### Community

| Type | Repository | Description |
|------|------------|-------------|
| Library | [harvard-edtech/zaccl](https://github.com/harvard-edtech/zaccl) | Zoom App Complete Connection Library |

**Full list**: See [general/references/community-repos.md](../general/references/community-repos.md)

### Learning Path

1. **Start**: `zoomapps-sample-js` - Simplest, most up-to-date
2. **Advanced**: `zoomapps-advancedsample-react` - Comprehensive (In-Client OAuth, Guest Mode, Collaborate)
3. **Specialized**: Pick based on feature (Layers, Serverless, Camera Mode)

## Critical Gotchas (From Real Development)

### 1. Global Variable Conflict
The CDN script defines `window.zoomSdk`. Declaring `let zoomSdk` in your code causes `SyntaxError: redeclaration of non-configurable global property`. Use `let sdk = window.zoomSdk` or the NPM import.

### 2. Domain Allowlist
Your app URL **must** be in the Marketplace domain allowlist. Without it, Zoom shows a blank panel with no error. Also add `appssdk.zoom.us` and any CDN domains you use.

### 3. Capabilities Must Be Listed
Only APIs listed in `config({ capabilities: [...] })` are available. Calling an unlisted API throws an error. This is also true for event listeners.

### 4. SDK Only Works Inside Zoom
`zoomSdk.config()` throws outside the Zoom client. Always wrap in try/catch with browser fallback:
```javascript
try { await zoomSdk.config({...}); } catch { showBrowserPreview(); }
```

### 5. ngrok URL Changes
Free ngrok URLs change on restart. You must update 4 places in Marketplace: Home URL, Redirect URL, OAuth Allow List, Domain Allow List. Consider ngrok paid plan for stable subdomain.

### 6. In-Client OAuth vs Web OAuth
Use `zoomSdk.authorize()` (In-Client) for best UX - no browser redirect. Only fall back to web redirect for initial install from Marketplace.

### 7. Camera Mode CEF Race Condition
Camera mode uses CEF which takes time to initialize. `drawImage`/`drawWebView` may fail if called too early. Implement retry with exponential backoff.

### 8. Cookie Configuration
Zoom's embedded browser requires cookies with `SameSite=None` and `Secure=true`. Without this, sessions break silently.

### 9. State Validation
Always validate the OAuth `state` parameter to prevent CSRF attacks. Generate cryptographically random state, store it, and verify on callback.

## Resources

- **Official docs**: https://developers.zoom.us/docs/zoom-apps/
- **SDK reference**: https://appssdk.zoom.us/
- **NPM package**: https://www.npmjs.com/package/@zoom/appssdk
- **Developer forum**: https://devforum.zoom.us/
- **GitHub SDK source**: https://github.com/zoom/appssdk

---

**Need help?** Start with Integrated Index section below for complete navigation.

---

## Integrated Index

_This section was migrated from `SKILL.md`._

## Quick Start Path

**If you're new to Zoom Apps, follow this order:**

1. **Run preflight checks first** -> [RUNBOOK.md](RUNBOOK.md)

2. **Read the architecture** -> [concepts/architecture.md](concepts/architecture.md)
   - Frontend/backend pattern, embedded browser, deep linking
   - Understand how Zoom loads and communicates with your app

3. **Build your first app** -> [examples/quick-start.md](examples/quick-start.md)
   - Complete Express + SDK Hello World
   - ngrok setup for local development

4. **Understand running contexts** -> [concepts/running-contexts.md](concepts/running-contexts.md)
   - Where your app runs (inMeeting, inMainClient, inWebinar, etc.)
   - Context-specific APIs and limitations

5. **Implement OAuth** -> [examples/in-client-oauth.md](examples/in-client-oauth.md)
   - In-Client OAuth with PKCE (best UX)
   - Token exchange and storage

6. **Add features** -> [references/apis.md](references/apis.md)
   - 100+ SDK methods organized by category
   - Code examples for each

7. **Troubleshoot** -> [troubleshooting/common-issues.md](troubleshooting/common-issues.md)
   - Quick diagnostics for common problems

---

## Documentation Structure

```
zoom-apps-sdk/
├── SKILL.md                           # Main skill overview
├── SKILL.md                           # This file - navigation guide
│
├── concepts/                          # Core architectural patterns
│   ├── architecture.md               # Frontend/backend, embedded browser, OAuth flow
│   ├── running-contexts.md           # Where your app runs + context-specific APIs
│   └── security.md                   # OWASP headers, CSP, data access layers
│
├── examples/                          # Complete working code
│   ├── quick-start.md                # Hello World - minimal Express + SDK app
│   ├── in-client-oauth.md            # In-Client OAuth with PKCE
│   ├── layers-immersive.md           # Layers API - immersive mode (custom layouts)
│   ├── layers-camera.md              # Layers API - camera mode (virtual camera)
│   ├── collaborate-mode.md           # Collaborate mode (shared state)
│   ├── guest-mode.md                 # Guest mode (unauthenticated -> authorized)
│   ├── breakout-rooms.md             # Breakout room integration
│   └── app-communication.md          # connect + postMessage between instances
│
├── troubleshooting/                   # Problem solving guides
│   ├── common-issues.md              # Quick diagnostics, error codes
│   ├── debugging.md                  # Local dev setup, ngrok, browser preview
│   └── migration.md                  # SDK version migration notes
│
└── references/                        # Reference documentation
    ├── apis.md                        # Complete API reference (100+ methods)
    ├── events.md                      # All SDK events
    ├── layers-api.md                  # Layers API detailed reference
    ├── oauth.md                       # OAuth flows for Zoom Apps
    └── zmail-sdk.md                   # Zoom Mail integration
```

---

## By Use Case

### I want to build a basic Zoom App
1. [Architecture](concepts/architecture.md) - Understand the pattern
2. [Quick Start](examples/quick-start.md) - Build Hello World
3. [In-Client OAuth](examples/in-client-oauth.md) - Add authorization
4. [Security](concepts/security.md) - Required headers

### I want immersive video layouts (Layers API)
1. [Layers Immersive](examples/layers-immersive.md) - Custom video positions
2. [Layers API Reference](references/layers-api.md) - All drawing methods
3. [App Communication](examples/app-communication.md) - Sync layout across participants

### I want a virtual camera overlay
1. [Camera Mode](examples/layers-camera.md) - Camera mode rendering
2. [Layers API Reference](references/layers-api.md) - Drawing methods

### I want real-time collaboration
1. [Collaborate Mode](examples/collaborate-mode.md) - Shared state APIs
2. [App Communication](examples/app-communication.md) - Instance messaging

### I want guest/anonymous access
1. [Guest Mode](examples/guest-mode.md) - Three authorization states
2. [In-Client OAuth](examples/in-client-oauth.md) - promptAuthorize flow

### I want breakout room support
1. [Breakout Rooms](examples/breakout-rooms.md) - Room detection and state sync

### I want to sync between main client and meeting
1. [App Communication](examples/app-communication.md) - connect + postMessage
2. [Running Contexts](concepts/running-contexts.md) - Multi-instance behavior

### I want serverless deployment
1. [Quick Start](examples/quick-start.md) - Understand the base pattern first
2. Sample: [zoomapps-serverless-vuejs](https://github.com/zoom/zoomapps-serverless-vuejs) - Firebase pattern

### I want to add Zoom Mail integration
1. [Zoom Mail Reference](references/zmail-sdk.md) - REST API + mail plugins

### I'm getting errors
1. [Common Issues](troubleshooting/common-issues.md) - Quick diagnostic table
2. [Debugging](troubleshooting/debugging.md) - Local dev setup, DevTools
3. [Migration](troubleshooting/migration.md) - Version compatibility

---

## Most Critical Documents

### 1. Architecture (FOUNDATION)
**[concepts/architecture.md](concepts/architecture.md)**

Understand how Zoom Apps work: Frontend in embedded browser, backend for OAuth/API, SDK as the bridge. Without this, nothing else makes sense.

### 2. Quick Start (FIRST APP)
**[examples/quick-start.md](examples/quick-start.md)**

Complete working code. Get something running before diving into advanced features.

### 3. Common Issues (MOST COMMON PROBLEMS)
**[troubleshooting/common-issues.md](troubleshooting/common-issues.md)**

90% of Zoom Apps issues are: domain allowlist, global variable conflict, or missing capabilities.

---

## Key Learnings

### Critical Discoveries:

1. **Global Variable Conflict is the #1 Gotcha**
   - CDN script defines `window.zoomSdk` globally
   - `let zoomSdk = ...` causes SyntaxError in Zoom's browser
   - Use `let sdk = window.zoomSdk` or NPM import

2. **Domain Allowlist is Non-Negotiable**
   - App shows blank panel with zero error if domain not whitelisted
   - Must include your domain AND `appssdk.zoom.us` AND any CDN domains
   - ngrok URLs change on restart - must update Marketplace each time

3. **config() Gates Everything**
   - Must be called first, must list all capabilities
   - Unlisted capabilities throw errors
   - Check `unsupportedApis` for client version compatibility

4. **In-Client OAuth > Web OAuth for UX**
   - `authorize()` keeps user in Zoom (no browser redirect)
   - Web redirect only needed for initial Marketplace install
   - Always implement PKCE (code_verifier + code_challenge)

5. **Two App Instances Can Run Simultaneously**
   - Main client instance + meeting instance
   - Use `connect()` + `postMessage()` to sync between them
   - Pre-meeting setup in main client, use in meeting

6. **Camera Mode Has CEF Quirks**
   - CEF initialization takes time
   - Draw calls may fail if too early
   - Use retry with exponential backoff

7. **Cookie Settings Matter**
   - `SameSite=None` + `Secure=true` required
   - Without this, sessions silently fail in embedded browser

---

## Quick Reference

### "App shows blank panel"
-> [Domain Allowlist](troubleshooting/common-issues.md) - add domain to Marketplace

### "SyntaxError: redeclaration"
-> [Global Variable](troubleshooting/common-issues.md) - use `let sdk = window.zoomSdk`

### "config() throws error"
-> [Browser Preview](troubleshooting/debugging.md) - SDK only works inside Zoom

### "API call fails silently"
-> [OAuth Scopes](troubleshooting/common-issues.md) - add required scopes in Marketplace

### "How do I implement [feature]?"
-> [API Reference](references/apis.md) - find the method, check capabilities needed

### "How do I test locally?"
-> [Debugging Guide](troubleshooting/debugging.md) - ngrok + Marketplace config

---

## Document Version

Based on **@zoom/appssdk v0.16.x** (latest: 0.16.26+)

---

**Happy coding!**

Start with [Architecture](concepts/architecture.md) to understand the pattern, then [Quick Start](examples/quick-start.md) to build your first app.

# Zoom Apps Architecture

## Overview

A Zoom App is a web application that runs inside the Zoom client's embedded browser. It consists of two parts:

- **Frontend**: Your web app loaded inside Zoom (HTML/CSS/JS + `@zoom/appssdk`)
- **Backend**: Your server handling OAuth, REST API calls, and business logic

The SDK (`@zoom/appssdk`) is the bridge between your frontend and the Zoom client.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                    ZOOM CLIENT                       │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │         Embedded Browser (WebView)            │   │
│  │                                               │   │
│  │  ┌─────────────────────────────────────────┐ │   │
│  │  │        YOUR FRONTEND WEB APP            │ │   │
│  │  │                                         │ │   │
│  │  │  import zoomSdk from '@zoom/appssdk'    │ │   │
│  │  │  zoomSdk.config({...})                  │ │   │
│  │  │  zoomSdk.getMeetingContext()             │ │   │
│  │  │                                         │ │   │
│  │  │     fetch('/api/data')  ──────────────────────── YOUR BACKEND
│  │  └─────────────────────────────────────────┘ │   │    (Express/Node.js)
│  │              │                                │   │    - OAuth token exchange
│  │              │ SDK Bridge                     │   │    - REST API calls
│  │              ▼                                │   │    - Business logic
│  │     Zoom Client APIs                         │   │    - Token storage
│  │     (meeting, user, UI)                      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Embedded Browser Details

Zoom uses different browser engines per platform:

| Platform | Browser Engine | Notes |
|----------|---------------|-------|
| Windows | WebView2 (Chromium) | Modern, good DevTools |
| macOS | WKWebView (WebKit) | Safari-like behavior |
| iOS | WKWebView | Mobile viewport |
| Android | WebView | Mobile viewport |
| Some surfaces | CEF (Chromium Embedded) | Camera mode uses this |

**Limitations:**
- No browser extensions
- Limited `window.open` support (use `zoomSdk.openUrl()` instead)
- No access to browser-level storage across different apps
- CSP must allow `frame-ancestors zoom.us *.zoom.us`
- Cookies require `SameSite=None; Secure`

## App Lifecycle

### Initial Install (Web OAuth)

```
User clicks "Add" in Marketplace
         │
         ▼
Browser opens Zoom OAuth page
(https://zoom.us/oauth/authorize?client_id=...&code_challenge=...)
         │
         ▼
User clicks "Allow"
         │
         ▼
Zoom redirects to your redirect URI with ?code=...
         │
         ▼
Your backend exchanges code + code_verifier for access_token
         │
         ▼
Backend calls GET /v2/zoomapp/deeplink with access_token
         │
         ▼
Backend redirects user to deeplink URL
         │
         ▼
Zoom client opens, loads your frontend URL in embedded browser
         │
         ▼
Frontend calls zoomSdk.config({...})
         │
         ▼
App is ready
```

### Subsequent Opens (In-Client OAuth)

```
User opens your app in Zoom client
         │
         ▼
Zoom loads your frontend URL in embedded browser
         │
         ▼
Frontend calls zoomSdk.config({...})
         │
         ▼
Frontend calls zoomSdk.authorize({ codeChallenge, state })
         │
         ▼
User approves in Zoom popup (no browser redirect)
         │
         ▼
onAuthorized event fires with authorization code
         │
         ▼
Frontend sends code to backend
         │
         ▼
Backend exchanges code + code_verifier for tokens
         │
         ▼
App is authorized
```

## Deep Linking

After web-based OAuth, your backend must get a deeplink to open the app in Zoom:

```javascript
// After token exchange, get deeplink
const response = await fetch('https://api.zoom.us/v2/zoomapp/deeplink', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ action: '' })
});

const { deeplink } = await response.json();
// deeplink = 'zoommtg://zoom.us/...' or similar

// Redirect user to open in Zoom client
res.redirect(deeplink);
```

## X-Zoom-App-Context Header

When Zoom loads your frontend, it sends an `X-Zoom-App-Context` HTTP header. This encrypted header contains user and meeting context, allowing your backend to identify the user without OAuth.

### Decryption (Node.js)

```javascript
const crypto = require('crypto');

function decryptContext(header, clientSecret) {
  const buf = Buffer.from(header, 'base64');
  const iv = buf.slice(0, 12);                    // First 12 bytes = IV
  const encryptedData = buf.slice(12, buf.length - 16); // Middle = ciphertext
  const tag = buf.slice(buf.length - 16);          // Last 16 bytes = auth tag

  const key = crypto.createHash('sha256')
    .update(clientSecret)
    .digest();

  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);

  const decrypted = Buffer.concat([
    decipher.update(encryptedData),
    decipher.final()
  ]);

  return JSON.parse(decrypted.toString());
}

// Usage in Express middleware
app.use((req, res, next) => {
  const contextHeader = req.headers['x-zoom-app-context'];
  if (contextHeader) {
    req.zoomContext = decryptContext(contextHeader, process.env.ZOOM_APP_CLIENT_SECRET);
    // { uid: '...', aud: '...', iss: 'marketplace.zoom.us', ts: ..., ... }
  }
  next();
});
```

The decrypted context contains:
- `uid` - Zoom user ID
- `mid` - Meeting ID (if in meeting)
- `aud` - Your app's client ID
- `iss` - Issuer (`marketplace.zoom.us`)
- `ts` - Timestamp

## Data Access Layers

Zoom Apps can access data through three layers:

| Layer | Method | Data Available | Auth Required |
|-------|--------|----------------|---------------|
| **Contextual** | SDK APIs (`getMeetingContext`, etc.) | Meeting/user/participant info | config() only |
| **Server-side** | REST API (via backend) | Full Zoom API (users, meetings, recordings) | OAuth tokens |
| **Header** | X-Zoom-App-Context header | User identity, meeting context | Client secret |

## Domain Allowlist

The Zoom client will **only** load URLs from domains in your app's allowlist.

**Required domains:**
- Your app domain (e.g., `yourdomain.com`)
- `appssdk.zoom.us` (if using CDN)
- Any CDN domains (fonts, CSS, images)
- Any API domains your frontend calls directly

**Configure in:** Marketplace -> Your App -> Feature -> Zoom App -> Add Allow List

Without this, the embedded browser shows a blank panel with no error.

## Resources

- **Architecture docs**: https://developers.zoom.us/docs/zoom-apps/architecture/
- **Data access**: https://developers.zoom.us/docs/zoom-apps/data-access/
- **X-Zoom-App-Context**: https://developers.zoom.us/docs/zoom-apps/zoom-app-context/

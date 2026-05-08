# Security

## Overview

Zoom Apps must meet security requirements for Marketplace approval. This covers required headers, CSP configuration, cookie security, and token storage.

## Required OWASP Headers

Zoom's security review requires these HTTP headers on all responses:

| Header | Required Value | Purpose |
|--------|---------------|---------|
| `Strict-Transport-Security` | `max-age=31536000` | Force HTTPS for 1 year |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME type sniffing |
| `Content-Security-Policy` | `frame-ancestors 'self' zoom.us *.zoom.us` | Allow Zoom to embed your app |
| `Referrer-Policy` | `same-origin` | Limit referrer info |
| `X-Frame-Options` | `ALLOW-FROM zoom.us` | Legacy frame control |

### Express Implementation

```javascript
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Content-Security-Policy',
    "frame-ancestors 'self' zoom.us *.zoom.us"
  );
  res.setHeader('Referrer-Policy', 'same-origin');
  next();
});
```

**Critical:** The `frame-ancestors` CSP directive is what allows Zoom's embedded browser to load your app. Without it, the browser blocks the frame.

## TLS Requirements

- HTTPS required for all endpoints (minimum TLS 1.2)
- HTTP redirects to HTTPS
- Valid SSL certificate (self-signed will fail)
- ngrok provides HTTPS automatically for local development

## Cookie Security

Zoom's embedded browser requires specific cookie settings:

```javascript
// Express cookie-session example
app.use(require('cookie-session')({
  name: 'session',
  keys: [process.env.SESSION_SECRET],
  maxAge: 24 * 60 * 60 * 1000, // 24 hours
  sameSite: 'none',  // REQUIRED - Zoom embeds your app cross-origin
  secure: true       // REQUIRED - SameSite=None requires Secure
}));
```

**Why `SameSite=None`?** Your app runs inside Zoom's embedded browser, which is a different origin. Without `SameSite=None`, the browser won't send cookies to your server, and sessions break silently.

## PKCE OAuth Security

All Zoom Apps OAuth flows should use PKCE (Proof Key for Code Exchange):

```javascript
const crypto = require('crypto');

// Generate PKCE pair
const verifier = crypto.randomBytes(32).toString('hex');
const challenge = crypto.createHash('sha256')
  .update(verifier)
  .digest('base64url');

// Store verifier in session (server-side)
req.session.codeVerifier = verifier;

// Send challenge to frontend (or include in OAuth redirect URL)
res.json({ codeChallenge: challenge, state: req.session.state });
```

PKCE prevents authorization code interception attacks. The `code_verifier` never leaves your server.

## Token Storage

**Never store tokens in the frontend (localStorage, sessionStorage, cookies).**

| Storage | When to Use | Security |
|---------|-------------|----------|
| **Redis** | Multi-instance servers, production | Fast, TTL support, scalable |
| **Encrypted session** | Single server, simple apps | Tied to server process |
| **Firestore/DynamoDB** | Serverless (Firebase/Lambda) | Persistent, managed |
| **Database (encrypted)** | Complex apps with user accounts | Full control, encrypted at rest |

```javascript
// Redis token storage example
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

async function storeTokens(zoomUserId, tokens) {
  await redis.set(
    `zoom:tokens:${zoomUserId}`,
    JSON.stringify(tokens),
    'EX', tokens.expires_in // Auto-expire with token
  );
}

async function getTokens(zoomUserId) {
  const data = await redis.get(`zoom:tokens:${zoomUserId}`);
  return data ? JSON.parse(data) : null;
}
```

## State Parameter (CSRF Protection)

Always validate the OAuth `state` parameter:

```javascript
const crypto = require('crypto');

// Generate state before OAuth redirect
const state = crypto.randomBytes(16).toString('hex');
req.session.oauthState = state;

// Validate state on callback
app.get('/auth', (req, res) => {
  if (req.query.state !== req.session.oauthState) {
    return res.status(403).send('Invalid state - possible CSRF attack');
  }
  // Proceed with token exchange
});
```

## Data Access Layers

| Layer | What You Access | Authorization | Risk Level |
|-------|----------------|---------------|------------|
| **SDK (contextual)** | Meeting context, user info, UI controls | config() capabilities | Low - scoped to current context |
| **REST API (server-side)** | Full Zoom API (users, meetings, recordings) | OAuth access tokens | Medium - broader data access |
| **X-Zoom-App-Context** | User identity, meeting info | Client secret decryption | Low - read-only identity |

**Principle of least privilege:** Only request the OAuth scopes and SDK capabilities you actually need.

## Marketplace Security Review Checklist

- [ ] All OWASP headers set on every response
- [ ] HTTPS enforced (no HTTP endpoints)
- [ ] PKCE used for OAuth flows
- [ ] State parameter validated on OAuth callbacks
- [ ] Tokens stored server-side (never in frontend)
- [ ] Token refresh implemented (tokens expire in 1 hour)
- [ ] `SameSite=None; Secure` on cookies
- [ ] CSP allows `frame-ancestors zoom.us *.zoom.us`
- [ ] No sensitive data logged to console in production
- [ ] Environment variables for all secrets (no hardcoded credentials)

## Resources

- **Security docs**: https://developers.zoom.us/docs/zoom-apps/security/
- **OWASP headers**: https://developers.zoom.us/docs/zoom-apps/security/owasp/

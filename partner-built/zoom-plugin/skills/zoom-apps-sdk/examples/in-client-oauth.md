# In-Client OAuth with PKCE

Authorize users without leaving the Zoom client. Best UX for returning users.

## Why In-Client OAuth?

| Approach | UX | When to Use |
|----------|----|-------------|
| **Web redirect** | Opens browser, redirects back | Initial install from Marketplace |
| **In-Client** | Popup inside Zoom, no redirect | Subsequent authorizations, best UX |

## Flow

```
Frontend                          Backend                         Zoom
────────                          ────────                        ────
GET /api/auth/challenge    -->
                           <--    { codeChallenge, state }
                                  (stores code_verifier in session)

zoomSdk.authorize({        -->                               -->  Shows "Authorize" popup
  codeChallenge, state                                            to user
})

onAuthorized fires         <--                               <--  User clicks "Allow"
{ code, state }

POST /api/auth/token       -->
{ code, state }                   Validates state
                                  Exchanges code + verifier
                                  for access_token
                           <--    { success: true }
```

## Frontend Implementation

```javascript
import zoomSdk from '@zoom/appssdk';

async function init() {
  await zoomSdk.config({
    capabilities: ['authorize', 'onAuthorized', 'getUserContext'],
    version: '0.16'
  });

  // Check if already authorized
  try {
    const response = await fetch('/api/auth/status');
    const { authorized } = await response.json();
    if (authorized) {
      showApp();
      return;
    }
  } catch (e) {
    // Not authorized yet
  }

  // Set up authorization listener BEFORE calling authorize
  zoomSdk.addEventListener('onAuthorized', async (event) => {
    const { code, state } = event;

    const response = await fetch('/api/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, state })
    });

    if (response.ok) {
      showApp();
    } else {
      showError('Authorization failed');
    }
  });

  // Get challenge and start authorization
  const challengeResponse = await fetch('/api/auth/challenge');
  const { codeChallenge, state } = await challengeResponse.json();

  await zoomSdk.authorize({ codeChallenge, state });
}
```

## Backend Implementation

```javascript
const crypto = require('crypto');
const express = require('express');
const axios = require('axios');
const router = express.Router();

// Generate PKCE challenge
router.get('/api/auth/challenge', (req, res) => {
  const verifier = crypto.randomBytes(32).toString('hex');
  const challenge = crypto.createHash('sha256')
    .update(verifier)
    .digest('base64url');
  const state = crypto.randomBytes(16).toString('hex');

  // Store in session (server-side only)
  req.session.codeVerifier = verifier;
  req.session.state = state;

  res.json({ codeChallenge: challenge, state });
});

// Exchange authorization code for tokens
router.post('/api/auth/token', async (req, res) => {
  const { code, state } = req.body;

  // Validate state (CSRF protection)
  if (state !== req.session.state) {
    return res.status(403).json({ error: 'Invalid state' });
  }

  try {
    const tokenResponse = await axios.post('https://zoom.us/oauth/token', null, {
      params: {
        grant_type: 'authorization_code',
        code,
        redirect_uri: process.env.ZOOM_APP_REDIRECT_URI,
        code_verifier: req.session.codeVerifier
      },
      headers: {
        'Authorization': 'Basic ' + Buffer.from(
          `${process.env.ZOOM_APP_CLIENT_ID}:${process.env.ZOOM_APP_CLIENT_SECRET}`
        ).toString('base64')
      }
    });

    // Store tokens securely (session, Redis, or database)
    req.session.tokens = {
      access_token: tokenResponse.data.access_token,
      refresh_token: tokenResponse.data.refresh_token,
      expires_at: Date.now() + (tokenResponse.data.expires_in * 1000)
    };

    // Clean up PKCE data
    delete req.session.codeVerifier;
    delete req.session.state;

    res.json({ success: true });
  } catch (error) {
    console.error('Token exchange failed:', error.response?.data || error.message);
    res.status(500).json({ error: 'Token exchange failed' });
  }
});

// Check authorization status
router.get('/api/auth/status', (req, res) => {
  const tokens = req.session.tokens;
  const authorized = tokens && tokens.expires_at > Date.now();
  res.json({ authorized });
});

// Token refresh helper
async function refreshTokens(req) {
  const { refresh_token } = req.session.tokens;

  const response = await axios.post('https://zoom.us/oauth/token', null, {
    params: {
      grant_type: 'refresh_token',
      refresh_token
    },
    headers: {
      'Authorization': 'Basic ' + Buffer.from(
        `${process.env.ZOOM_APP_CLIENT_ID}:${process.env.ZOOM_APP_CLIENT_SECRET}`
      ).toString('base64')
    }
  });

  req.session.tokens = {
    access_token: response.data.access_token,
    refresh_token: response.data.refresh_token,
    expires_at: Date.now() + (response.data.expires_in * 1000)
  };

  return req.session.tokens;
}

module.exports = router;
```

## Re-Authorization with promptAuthorize

For guest mode users who need to upgrade their authorization:

```javascript
// Use when user needs to grant additional permissions
await zoomSdk.promptAuthorize();

// Same onAuthorized listener fires
zoomSdk.addEventListener('onAuthorized', async (event) => {
  // Handle same as initial authorization
});
```

## Token Refresh Pattern

```javascript
// Middleware to auto-refresh expired tokens
async function ensureAuthorized(req, res, next) {
  if (!req.session.tokens) {
    return res.status(401).json({ error: 'Not authorized' });
  }

  // Refresh if expiring within 5 minutes
  if (req.session.tokens.expires_at < Date.now() + 300000) {
    try {
      await refreshTokens(req);
    } catch (error) {
      return res.status(401).json({ error: 'Token refresh failed' });
    }
  }

  next();
}
```

## Resources

- **Auth guide**: https://developers.zoom.us/docs/zoom-apps/authentication/
- **OAuth reference**: [../references/oauth.md](../references/oauth.md)

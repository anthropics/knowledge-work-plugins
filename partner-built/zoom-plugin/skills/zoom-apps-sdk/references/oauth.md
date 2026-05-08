# Zoom Apps SDK - OAuth Reference

OAuth flows for Zoom Apps: web-based redirect, In-Client, and third-party.

## Three OAuth Flows

| Flow | UX | When to Use |
|------|----|-------------|
| **Web-based redirect** | Opens browser, redirect back | Initial install from Marketplace |
| **In-Client OAuth** | Popup inside Zoom, no redirect | Subsequent authorizations (best UX) |
| **Third-party OAuth** | External provider (Auth0, Google) | When your app needs non-Zoom auth |

## PKCE (Required for All Flows)

All Zoom Apps OAuth must use PKCE (Proof Key for Code Exchange):

```javascript
const crypto = require('crypto');

// Generate PKCE pair
const verifier = crypto.randomBytes(32).toString('hex');
const challenge = crypto.createHash('sha256')
  .update(verifier)
  .digest('base64url');

// verifier: stored server-side (never exposed to client)
// challenge: sent with authorization request
```

## Flow 1: Web-Based OAuth (Initial Install)

```
User clicks "Add" in Marketplace
    |
    v
GET https://zoom.us/oauth/authorize
  ?client_id=YOUR_CLIENT_ID
  &response_type=code
  &redirect_uri=YOUR_REDIRECT_URI
  &code_challenge=CHALLENGE
  &code_challenge_method=S256
  &state=RANDOM_STATE
    |
    v
User authorizes -> Zoom redirects to YOUR_REDIRECT_URI?code=AUTH_CODE&state=STATE
    |
    v
Backend validates state, exchanges code for tokens
    |
    v
Backend gets deeplink, redirects user to Zoom client
```

### Server Route Handler

```javascript
app.get('/auth', async (req, res) => {
  const { code, state } = req.query;

  // Validate state (CSRF protection)
  if (state !== req.session.state) {
    return res.status(403).send('Invalid state');
  }

  // Exchange code for tokens
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

  const { access_token, refresh_token, expires_in } = tokenResponse.data;

  // Store tokens securely
  req.session.tokens = { access_token, refresh_token, expires_at: Date.now() + expires_in * 1000 };

  // Get deeplink to open app in Zoom
  const deeplink = await axios.post('https://api.zoom.us/v2/zoomapp/deeplink',
    { action: '' },
    { headers: { 'Authorization': `Bearer ${access_token}` } }
  );

  res.redirect(deeplink.data.deeplink);
});
```

## Flow 2: In-Client OAuth (Best UX)

No browser redirect - authorization happens inside Zoom:

```javascript
// Frontend
const { codeChallenge, state } = await fetch('/api/auth/challenge').then(r => r.json());

zoomSdk.addEventListener('onAuthorized', async (event) => {
  await fetch('/api/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: event.code, state: event.state })
  });
});

await zoomSdk.authorize({ codeChallenge, state });
```

See **[In-Client OAuth example](../examples/in-client-oauth.md)** for complete implementation.

## Token Exchange Endpoint

```
POST https://zoom.us/oauth/token

Headers:
  Authorization: Basic base64(CLIENT_ID:CLIENT_SECRET)

Parameters:
  grant_type=authorization_code
  code=AUTH_CODE
  redirect_uri=YOUR_REDIRECT_URI
  code_verifier=PKCE_VERIFIER
```

Response:
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "refresh_token": "...",
  "expires_in": 3600,
  "scope": "zoomapp:inmeeting"
}
```

## Token Refresh

Access tokens expire in 1 hour. Use refresh token to get new ones:

```javascript
async function refreshTokens(refreshToken) {
  const response = await axios.post('https://zoom.us/oauth/token', null, {
    params: {
      grant_type: 'refresh_token',
      refresh_token: refreshToken
    },
    headers: {
      'Authorization': 'Basic ' + Buffer.from(
        `${process.env.ZOOM_APP_CLIENT_ID}:${process.env.ZOOM_APP_CLIENT_SECRET}`
      ).toString('base64')
    }
  });

  return response.data; // { access_token, refresh_token, expires_in }
}
```

**Note:** Refresh tokens are single-use. Each refresh returns a new refresh_token.

## Deep Linking

After web OAuth, get a deeplink to open your app in Zoom:

```javascript
const response = await axios.post('https://api.zoom.us/v2/zoomapp/deeplink',
  { action: '' },
  { headers: { 'Authorization': `Bearer ${accessToken}` } }
);

const { deeplink } = response.data;
// Redirect user to this URL to open app in Zoom client
```

## Required Scopes

| Scope | Description |
|-------|-------------|
| `zoomapp:inmeeting` | In-meeting functionality (most common) |
| `user:read` | Read user profile |
| `meeting:read` | Read meeting details |
| `meeting:write` | Create/modify meetings |

## Token Storage Patterns

| Pattern | When to Use |
|---------|-------------|
| **Redis** | Multi-instance production servers |
| **Session cookie** | Simple single-server apps |
| **Firestore** | Serverless (Firebase) |
| **Encrypted database** | Complex apps with user accounts |

## Resources

- **Auth docs**: https://developers.zoom.us/docs/zoom-apps/authentication/
- **In-Client OAuth example**: [../examples/in-client-oauth.md](../examples/in-client-oauth.md)
- **oauth skill**: [../../oauth/SKILL.md](../../oauth/SKILL.md)

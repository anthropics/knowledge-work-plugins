# Authentication Guide

Comprehensive guide to Zoom API authentication methods: OAuth 2.0, Server-to-Server OAuth, and JWT (legacy).

## Overview

Zoom APIs support multiple authentication methods depending on your use case:

| Method | Use Case | Token Lifetime |
|--------|----------|----------------|
| **User OAuth 2.0** | Act on behalf of users | 1 hour (refresh: 15 years) |
| **Server-to-Server OAuth** | Backend automation | 1 hour |
| **JWT (Deprecated)** | Legacy integrations | Custom |

## Server-to-Server OAuth (Recommended for Backend)

For backend services that don't need user interaction.

### Setup

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**
3. Select **Server-to-Server OAuth**
4. Note your credentials:
   - Account ID
   - Client ID
   - Client Secret

### Get Access Token

```bash
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n '{clientId}:{clientSecret}' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=account_credentials&account_id={accountId}"
```

### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "meeting:read meeting:write user:read"
}
```

### Code Example (Node.js)

```javascript
const axios = require('axios');

class ZoomAuth {
  constructor(accountId, clientId, clientSecret) {
    this.accountId = accountId;
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.token = null;
    this.tokenExpiry = null;
  }

  async getAccessToken() {
    // Return cached token if still valid
    if (this.token && this.tokenExpiry > Date.now() + 60000) {
      return this.token;
    }

    const credentials = Buffer.from(
      `${this.clientId}:${this.clientSecret}`
    ).toString('base64');

    const response = await axios.post(
      'https://zoom.us/oauth/token',
      `grant_type=account_credentials&account_id=${this.accountId}`,
      {
        headers: {
          'Authorization': `Basic ${credentials}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );

    this.token = response.data.access_token;
    this.tokenExpiry = Date.now() + (response.data.expires_in * 1000);
    
    return this.token;
  }

  async apiRequest(method, endpoint, data = null) {
    const token = await this.getAccessToken();
    
    const config = {
      method,
      url: `https://api.zoom.us/v2${endpoint}`,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    };

    if (data) {
      config.data = data;
    }

    return axios(config);
  }
}

// Usage
const zoom = new ZoomAuth(
  process.env.ZOOM_ACCOUNT_ID,
  process.env.ZOOM_CLIENT_ID,
  process.env.ZOOM_CLIENT_SECRET
);

const users = await zoom.apiRequest('GET', '/users');
```

## User OAuth 2.0 (For User Actions)

For applications that act on behalf of individual users.

### OAuth Flow

```
1. User clicks "Connect to Zoom"
       ↓
2. Redirect to Zoom authorization URL
       ↓
3. User grants permission
       ↓
4. Zoom redirects to your callback with code
       ↓
5. Exchange code for access token
       ↓
6. Use access token for API calls
       ↓
7. Refresh token when expired
```

### Step 1: Create OAuth App

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click **Develop** → **Build App**
3. Select **OAuth**
4. Configure:
   - Redirect URI(s)
   - Required scopes
   - App information

### Step 2: Authorization URL

Redirect users to:

```
https://zoom.us/oauth/authorize?response_type=code&client_id={clientId}&redirect_uri={redirectUri}&state={state}
```

| Parameter | Description |
|-----------|-------------|
| `response_type` | Always `code` |
| `client_id` | Your OAuth app client ID |
| `redirect_uri` | Must match registered URI |
| `state` | Random string for CSRF protection |

### Step 3: Handle Callback

User is redirected to your callback URL:

```
https://yourapp.com/callback?code=AUTH_CODE&state=STATE
```

### Step 4: Exchange Code for Token

```bash
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n '{clientId}:{clientSecret}' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code={authCode}&redirect_uri={redirectUri}"
```

### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiJ9...",
  "expires_in": 3600,
  "scope": "meeting:read meeting:write user:read"
}
```

### Step 5: Refresh Token

```bash
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n '{clientId}:{clientSecret}' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token={refreshToken}"
```

### Complete OAuth Example (Express.js)

```javascript
const express = require('express');
const axios = require('axios');
const crypto = require('crypto');

const app = express();

const ZOOM_CLIENT_ID = process.env.ZOOM_CLIENT_ID;
const ZOOM_CLIENT_SECRET = process.env.ZOOM_CLIENT_SECRET;
const REDIRECT_URI = 'https://yourapp.com/auth/zoom/callback';

// Step 2: Initiate OAuth
app.get('/auth/zoom', (req, res) => {
  const state = crypto.randomBytes(16).toString('hex');
  req.session.oauthState = state;
  
  const authUrl = new URL('https://zoom.us/oauth/authorize');
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('client_id', ZOOM_CLIENT_ID);
  authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
  authUrl.searchParams.set('state', state);
  
  res.redirect(authUrl.toString());
});

// Step 3 & 4: Handle callback and exchange code
app.get('/auth/zoom/callback', async (req, res) => {
  const { code, state } = req.query;
  
  // Verify state
  if (state !== req.session.oauthState) {
    return res.status(400).send('Invalid state');
  }
  
  try {
    // Exchange code for token
    const credentials = Buffer.from(
      `${ZOOM_CLIENT_ID}:${ZOOM_CLIENT_SECRET}`
    ).toString('base64');
    
    const tokenResponse = await axios.post(
      'https://zoom.us/oauth/token',
      `grant_type=authorization_code&code=${code}&redirect_uri=${REDIRECT_URI}`,
      {
        headers: {
          'Authorization': `Basic ${credentials}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    
    const { access_token, refresh_token, expires_in } = tokenResponse.data;
    
    // Store tokens securely (database)
    await storeTokens(req.user.id, {
      accessToken: access_token,
      refreshToken: refresh_token,
      expiresAt: Date.now() + (expires_in * 1000)
    });
    
    res.redirect('/dashboard');
  } catch (error) {
    console.error('OAuth error:', error.response?.data);
    res.status(500).send('Authentication failed');
  }
});

// Helper: Get valid access token (refresh if needed)
async function getValidToken(userId) {
  const tokens = await getStoredTokens(userId);
  
  // Check if token is expired (with 1 min buffer)
  if (tokens.expiresAt < Date.now() + 60000) {
    const credentials = Buffer.from(
      `${ZOOM_CLIENT_ID}:${ZOOM_CLIENT_SECRET}`
    ).toString('base64');
    
    const response = await axios.post(
      'https://zoom.us/oauth/token',
      `grant_type=refresh_token&refresh_token=${tokens.refreshToken}`,
      {
        headers: {
          'Authorization': `Basic ${credentials}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    
    await storeTokens(userId, {
      accessToken: response.data.access_token,
      refreshToken: response.data.refresh_token,
      expiresAt: Date.now() + (response.data.expires_in * 1000)
    });
    
    return response.data.access_token;
  }
  
  return tokens.accessToken;
}
```

## Scopes

### Common Scopes

| Scope | Description |
|-------|-------------|
| `user:read` | Read user profile |
| `user:write` | Update user profile |
| `meeting:read` | Read meeting data |
| `meeting:write` | Create/update meetings |
| `recording:read` | Access recordings |
| `recording:write` | Manage recordings |
| `phone:read` | Read Zoom Phone data |
| `phone:write` | Manage Zoom Phone |

### Admin Scopes

| Scope | Description |
|-------|-------------|
| `user:read:admin` | Read all users |
| `user:write:admin` | Manage all users |
| `meeting:read:admin` | Read all meetings |
| `account:read:admin` | Read account settings |

### Scope Selection

Request only scopes you need:
- More scopes = more user friction
- Less scopes = better approval chance
- Add scopes incrementally as features grow

## Token Storage Best Practices

```javascript
// DO: Encrypt tokens at rest
const encryptedToken = encrypt(accessToken, encryptionKey);
await db.tokens.save({ userId, encryptedToken });

// DO: Use secure, httpOnly cookies for web apps
res.cookie('zoom_token', accessToken, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 3600000
});

// DON'T: Store tokens in localStorage
localStorage.setItem('zoom_token', token); // BAD

// DON'T: Log tokens
console.log('Token:', accessToken); // BAD
```

## Error Handling

### Common OAuth Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_grant` | Expired/used code | Restart OAuth flow |
| `invalid_client` | Wrong credentials | Check client ID/secret |
| `invalid_scope` | Unauthorized scope | Request only approved scopes |
| `access_denied` | User denied permission | Handle gracefully |

### Token Refresh Errors

```javascript
try {
  const newToken = await refreshToken(refreshToken);
} catch (error) {
  if (error.response?.data?.error === 'invalid_grant') {
    // Refresh token expired or revoked
    // User needs to re-authorize
    redirectToOAuth();
  }
}
```

## Webhook Verification

For webhook security, verify the request signature:

```javascript
const crypto = require('crypto');

function verifyWebhook(req, secret) {
  const message = `v0:${req.headers['x-zm-request-timestamp']}:${JSON.stringify(req.body)}`;
  const signature = crypto
    .createHmac('sha256', secret)
    .update(message)
    .digest('hex');
  
  const expected = `v0=${signature}`;
  return req.headers['x-zm-signature'] === expected;
}

app.post('/webhooks/zoom', (req, res) => {
  if (!verifyWebhook(req, process.env.ZOOM_WEBHOOK_SECRET)) {
    return res.status(401).send('Invalid signature');
  }
  
  // Process webhook
  const event = req.body;
  // ...
});
```

## Migration from JWT (Deprecated)

JWT apps are deprecated. Migrate to Server-to-Server OAuth:

1. Create new Server-to-Server OAuth app
2. Request same scopes
3. Update code to use OAuth token endpoint
4. Test thoroughly
5. Delete JWT app

```javascript
// OLD (JWT - Deprecated)
const token = jwt.sign(payload, apiSecret);

// NEW (Server-to-Server OAuth)
const token = await getServerToServerToken();
```

## Resources

- **OAuth Guide**: https://developers.zoom.us/docs/integrations/oauth/
- **Server-to-Server OAuth**: https://developers.zoom.us/docs/internal-apps/s2s-oauth/
- **Scopes Reference**: https://developers.zoom.us/docs/integrations/oauth-scopes/
- **Migration Guide**: https://developers.zoom.us/docs/internal-apps/jwt-app-migration/

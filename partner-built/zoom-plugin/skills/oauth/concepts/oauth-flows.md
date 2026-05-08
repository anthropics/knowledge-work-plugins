# Zoom OAuth Flows

Zoom supports 4 OAuth 2.0 flows. This guide helps you choose the right one and understand how each works.

Endpoint split to remember:
- Authorization URL: `https://zoom.us/oauth/authorize`
- Token URL: `https://zoom.us/oauth/token`

## Quick Decision Matrix

| Your Scenario | Flow | Grant Type |
|---------------|------|------------|
| Backend automation on **your own account** | S2S OAuth | `account_credentials` |
| SaaS app for **other Zoom users** | User OAuth | `authorization_code` |
| Device without browser (TV, kiosk, IoT) | Device Flow | `urn:ietf:params:oauth:grant-type:device_code` |
| **Team Chat bot only** | Chatbot | `client_credentials` |

## Two-Legged vs Three-Legged

| Type | User Involved? | Zoom Flows |
|------|----------------|------------|
| **Two-legged** | No (app acts on its own) | S2S OAuth, Chatbot |
| **Three-legged** | Yes (user authorizes app) | User OAuth, Device Flow |

---

## 1. Server-to-Server (S2S) OAuth

**When to use:**
- Backend automation on your own Zoom account
- No end-user interaction needed
- Account-wide API access

**Grant type:** `account_credentials`

**Token lifetime:**
- Access token: 1 hour
- Refresh token: None (request new token when expired)

**Credentials required:**
- Account ID
- Client ID
- Client Secret

### Flow Diagram

```
┌──────────────┐                                    ┌──────────────┐
│  Your App    │                                    │  Zoom OAuth  │
│  (Backend)   │                                    │    Server    │
└──────┬───────┘                                    └──────┬───────┘
       │                                                   │
       │  POST /oauth/token                                │
       │  grant_type=account_credentials                   │
       │  account_id={ACCOUNT_ID}                          │
       │  Authorization: Basic {CLIENT_ID:CLIENT_SECRET}   │
       │──────────────────────────────────────────────────>│
       │                                                   │
       │                                                   │ Validate
       │                                                   │ credentials
       │                                                   │
       │  { access_token, expires_in, scope }              │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  API Requests with Bearer token                   │
       │  (valid for 1 hour)                               │
       │                                                   │
```

### Implementation

```javascript
const axios = require('axios');
const qs = require('query-string');

const getToken = async () => {
  const response = await axios.post(
    'https://zoom.us/oauth/token',
    qs.stringify({
      grant_type: 'account_credentials',
      account_id: process.env.ZOOM_ACCOUNT_ID
    }),
    {
      headers: {
        'Authorization': `Basic ${Buffer.from(
          `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
        ).toString('base64')}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
  );

  return response.data; // { access_token, expires_in, scope, token_type }
};
```

### Key Points

✅ **Simple:** No redirect URIs, no user interaction
✅ **Secure:** Credentials stored server-side only
✅ **Account-wide:** Single token for all account operations
⚠️ **No refresh token:** Just request a new token when expired (cache with TTL)

---

## 2. User Authorization OAuth

**When to use:**
- Building a SaaS app for other Zoom users
- Users authorize your app to act on their behalf
- Need per-user access control

**Grant type:** `authorization_code`

**Token lifetime:**
- Access token: 1 hour
- Refresh token: lifetime varies; ~90 days is common for some user-based flows (treat as changeable behavior)

**Credentials required:**
- Client ID
- Client Secret
- Redirect URI (must match marketplace app config)

### Flow Diagram

```
┌────────┐           ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│  User  │           │  Your App    │           │  Zoom OAuth  │           │  Zoom API    │
│Browser │           │   (Server)   │           │    Server    │           │    Server    │
└────┬───┘           └──────┬───────┘           └──────┬───────┘           └──────┬───────┘
     │                      │                          │                          │
     │  1. Click "Add App"  │                          │                          │
     │─────────────────────>│                          │                          │
     │                      │                          │                          │
     │  2. Redirect to authorize                       │                          │
     │https://zoom.us/oauth/authorize?                │                          │
     │    client_id={ID}                               │                          │
     │    redirect_uri={URI}                           │                          │
     │    response_type=code                           │                          │
     │    state={RANDOM}                               │                          │
     │<─────────────────────│                          │                          │
     │                      │                          │                          │
     │  3. User sees "Allow" page                      │                          │
     │─────────────────────────────────────────────────>│                          │
     │                      │                          │                          │
     │  4. User clicks "Allow"                         │                          │
     │─────────────────────────────────────────────────>│                          │
     │                      │                          │                          │
     │  5. Redirect to callback                        │                          │
     │  {REDIRECT_URI}?code={CODE}&state={STATE}       │                          │
     │<─────────────────────────────────────────────────│                          │
     │                      │                          │                          │
     │  6. Send code to app │                          │                          │
     │─────────────────────>│                          │                          │
     │                      │                          │                          │
     │                      │  7. Exchange code for token                         │
     │                      │  POST /oauth/token                                  │
     │                      │  grant_type=authorization_code                      │
     │                      │  code={CODE}                                        │
     │                      │  redirect_uri={URI}                                 │
     │                      │  Authorization: Basic {CLIENT_ID:CLIENT_SECRET}     │
     │                      │─────────────────────────────────────────────────────>│
     │                      │                          │                          │
     │                      │  8. Return tokens        │                          │
     │                      │  { access_token, refresh_token, expires_in }        │
     │                      │<─────────────────────────────────────────────────────│
     │                      │                          │                          │
     │                      │  9. Store tokens (encrypted)                        │
     │                      │  per user                │                          │
     │                      │                          │                          │
     │                      │  10. API requests                                   │
     │                      │  Authorization: Bearer {ACCESS_TOKEN}               │
     │                      │─────────────────────────────────────────────────────────────────>│
```

### Implementation

#### Step 1: Redirect to Authorization

```javascript
const express = require('express');
const crypto = require('crypto');

app.get('/auth', (req, res) => {
  const state = crypto.randomBytes(16).toString('hex');
  req.session.oauthState = state; // Store for verification

  const authURL = new URL('https://zoom.us/oauth/authorize');
  authURL.searchParams.set('response_type', 'code');
  authURL.searchParams.set('client_id', process.env.ZOOM_CLIENT_ID);
  authURL.searchParams.set('redirect_uri', process.env.ZOOM_REDIRECT_URL);
  authURL.searchParams.set('state', state);

  res.redirect(authURL.toString());
});
```

#### Step 2: Handle Callback and Exchange Code

```javascript
app.get('/callback', async (req, res) => {
  const { code, state } = req.query;

  // Verify state to prevent CSRF
  if (state !== req.session.oauthState) {
    return res.status(403).send('Invalid state parameter');
  }

  try {
    const response = await axios.post(
      'https://zoom.us/oauth/token',
      qs.stringify({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: process.env.ZOOM_REDIRECT_URL
      }),
      {
        headers: {
          'Authorization': `Basic ${Buffer.from(
            `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
          ).toString('base64')}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );

    const { access_token, refresh_token } = response.data;

    // Store tokens securely (encrypted) per user
    await saveUserTokens(req.session.userId, {
      access_token,
      refresh_token
    });

    res.send('Authorization successful!');
  } catch (error) {
    res.status(500).send('Token exchange failed');
  }
});
```

### Key Points

✅ **User-controlled:** Users authorize access to their own account
✅ **Per-user tokens:** Each user gets their own access/refresh tokens
✅ **Refresh support:** Tokens can be refreshed while the refresh token remains valid (lifetime varies; ~90 days is common)
⚠️ **Redirect URI must match exactly:** Including trailing slash, protocol, port
⚠️ **State parameter required:** Prevent CSRF attacks
⚠️ **Authorization code expires in 5 minutes:** Exchange immediately

---

## 3. Device Authorization Flow

**When to use:**
- Devices without a browser (smart TVs, kiosks, IoT devices)
- Devices with limited input capabilities
- User authorizes on a separate device (phone/computer)

**Grant type:** `urn:ietf:params:oauth:grant-type:device_code`

**Token lifetime:**
- Access token: 1 hour
- Refresh token: lifetime varies; ~90 days is common for some user-based flows (treat as changeable behavior)

**Credentials required:**
- Client ID
- Client Secret

### Flow Diagram

```
┌────────────┐           ┌──────────────┐           ┌────────────┐
│  Device    │           │  Zoom OAuth  │           │User's Phone│
│ (TV/Kiosk) │           │    Server    │           │ / Computer │
└──────┬─────┘           └──────┬───────┘           └─────┬──────┘
       │                        │                         │
       │  1. POST /oauth/devicecode                       │
       │  client_id={CLIENT_ID}                           │
       │───────────────────────>│                         │
       │                        │                         │
       │  2. Return device_code, user_code, verification_uri, interval
       │  { device_code, user_code, verification_uri, interval }
       │<───────────────────────│                         │
       │                        │                         │
       │  3. Display to user:   │                         │
       │  "Go to zoom.us/activate"                        │
       │  "Enter code: ABC-DEF" │                         │
       │                        │                         │
       │                        │  4. User visits URL     │
       │                        │  and enters user_code   │
       │                        │<────────────────────────│
       │                        │                         │
       │                        │  5. User clicks "Allow" │
       │                        │<────────────────────────│
       │                        │                         │
       │  6. Poll for token (every {interval} seconds)    │
       │  POST /oauth/token                               │
       │  grant_type=urn:ietf:params:oauth:grant-type:device_code
       │  device_code={DEVICE_CODE}                       │
       │───────────────────────>│                         │
       │                        │                         │
       │  7. Response (repeat until success or timeout)   │
       │  - authorization_pending (keep polling)          │
       │  - slow_down (increase interval)                 │
       │  - expired_token (restart flow)                  │
       │  - { access_token, refresh_token } (success!)    │
       │<───────────────────────│                         │
```

### Implementation

#### Step 1: Request Device Code

```javascript
const requestDeviceCode = async () => {
  const response = await axios.post(
    'https://zoom.us/oauth/devicecode',
    qs.stringify({
      client_id: process.env.ZOOM_CLIENT_ID
    }),
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
  );

  return response.data;
  /*
  {
    device_code: "GmRhmhcxhwAzkoEqiMEg_DnyEysNmsh6JCl-fNkAghaUg",
    user_code: "ABC-DEF",
    verification_uri: "https://zoom.us/activate",
    expires_in: 900, // 15 minutes
    interval: 5 // Poll every 5 seconds
  }
  */
};
```

#### Step 2: Display User Code

```javascript
const { device_code, user_code, verification_uri, interval } = await requestDeviceCode();

console.log(`\nGo to: ${verification_uri}`);
console.log(`Enter code: ${user_code}\n`);
```

#### Step 3: Poll for Token

```javascript
const pollForToken = async (device_code, interval) => {
  const pollInterval = interval * 1000; // Convert to milliseconds
  let currentInterval = pollInterval;

  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        const response = await axios.post(
          'https://zoom.us/oauth/token',
          qs.stringify({
            grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
            device_code: device_code
          }),
          {
            headers: {
              'Authorization': `Basic ${Buffer.from(
                `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
              ).toString('base64')}`,
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }
        );

        // Success! Got tokens
        resolve(response.data);

      } catch (error) {
        const errorCode = error.response?.data?.error;

        if (errorCode === 'authorization_pending') {
          // User hasn't authorized yet, keep polling
          setTimeout(poll, currentInterval);

        } else if (errorCode === 'slow_down') {
          // Zoom wants us to slow down, increase interval by 5s
          currentInterval += 5000;
          setTimeout(poll, currentInterval);

        } else if (errorCode === 'expired_token') {
          // Device code expired (15 minutes), restart flow
          reject(new Error('Device code expired. Please restart authorization.'));

        } else {
          // Other error
          reject(error);
        }
      }
    };

    // Start polling
    poll();
  });
};
```

### Key Points

✅ **No browser required:** User authorizes on separate device
✅ **Simple user experience:** Just enter a short code
✅ **Polling-based:** Device polls until user authorizes
⚠️ **Must enable in app settings:** "Use App on Device" feature flag
⚠️ **Device code expires in 15 minutes:** User must complete authorization quickly
⚠️ **Respect polling interval:** Returned by `/devicecode` endpoint (usually 5s)
⚠️ **Handle slow_down:** Increase interval by 5s when requested

---

## 4. Client Authorization (Chatbot)

**When to use:**
- Building a Team Chat bot ONLY
- App needs `imchat:bot` scope
- Simpler than S2S OAuth

**Grant type:** `client_credentials`

**Token lifetime:**
- Access token: 1 hour
- Refresh token: None (request new token when expired)

**Credentials required:**
- Client ID
- Client Secret

### Flow Diagram

```
┌──────────────┐                                    ┌──────────────┐
│ Chatbot App  │                                    │  Zoom OAuth  │
│  (Backend)   │                                    │    Server    │
└──────┬───────┘                                    └──────┬───────┘
       │                                                   │
       │  POST /oauth/token                                │
       │  grant_type=client_credentials                    │
       │  Authorization: Basic {CLIENT_ID:CLIENT_SECRET}   │
       │──────────────────────────────────────────────────>│
       │                                                   │
       │  { access_token, expires_in, scope }              │
       │<──────────────────────────────────────────────────│
       │                                                   │
       │  Chatbot API Requests with Bearer token           │
       │  (valid for 1 hour)                               │
       │                                                   │
```

### Implementation

```javascript
const getChatbotToken = async () => {
  const response = await axios.post(
    'https://zoom.us/oauth/token',
    qs.stringify({
      grant_type: 'client_credentials'
    }),
    {
      headers: {
        'Authorization': `Basic ${Buffer.from(
          `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
        ).toString('base64')}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
  );

  return response.data; // { access_token, expires_in, scope, token_type }
};
```

### Key Points

✅ **Simplest flow:** Just request token with credentials
✅ **Chatbot-specific:** Limited to Team Chat bot operations
⚠️ **No refresh token:** Request new token when expired
⚠️ **Scope limited:** Primarily `imchat:bot` scope

---

## Comparison Table

| Feature | S2S OAuth | User OAuth | Device Flow | Chatbot |
|---------|-----------|------------|-------------|---------|
| **Grant Type** | `account_credentials` | `authorization_code` | `device_code` | `client_credentials` |
| **User Interaction** | No | Yes (browser) | Yes (separate device) | No |
| **Access Token Lifetime** | 1 hour | 1 hour | 1 hour | 1 hour |
| **Refresh Token** | ❌ None | ✅ ~90 days (commonly) | ✅ ~90 days (commonly) | ❌ None |
| **Redirect URI** | ❌ Not needed | ✅ Required | ❌ Not needed | ❌ Not needed |
| **PKCE Support** | ❌ N/A | ✅ Optional | ❌ N/A | ❌ N/A |
| **State Parameter** | ❌ N/A | ✅ Recommended | ❌ N/A | ❌ N/A |
| **Account Access** | Account-wide | Per-user | Per-user | Account-wide |
| **Token Storage** | Redis (ephemeral) | Database (persistent) | Database (persistent) | Redis (ephemeral) |
| **Use Case** | Backend automation | SaaS apps | TV/kiosk apps | Chat bots |

---

## OAuth 2.0 Standards

Zoom OAuth follows these RFCs:

- **RFC 6749**: OAuth 2.0 Authorization Framework
  - https://datatracker.ietf.org/doc/html/rfc6749

- **RFC 7636**: PKCE (Proof Key for Code Exchange)
  - https://datatracker.ietf.org/doc/html/rfc7636

- **RFC 8628**: Device Authorization Grant
  - https://datatracker.ietf.org/doc/html/rfc8628

---

## Next Steps

- **Understand token lifecycle** → [token-lifecycle.md](token-lifecycle.md)
- **Learn about PKCE** → [pkce.md](pkce.md)
- **Implement your flow:**
  - S2S → [../examples/s2s-oauth-redis.md](../examples/s2s-oauth-redis.md)
  - User → [../examples/user-oauth-mysql.md](../examples/user-oauth-mysql.md)
  - Device → [../examples/device-flow.md](../examples/device-flow.md)

# Token Lifecycle

Understanding how Zoom OAuth tokens are created, expire, refresh, and revoke is critical for building reliable integrations.

## Token Types

### Access Token
- **Purpose:** Authenticate API requests
- **Lifetime:** 1 hour (all OAuth flows)
- **Usage:** `Authorization: Bearer {access_token}` header
- **Format:** Opaque string (not JWT)

### Refresh Token
- **Purpose:** Obtain new access tokens without user re-authorization
- **Lifetime:** Varies by flow/account/app configuration; ~90 days is common for some user-based flows (treat as changeable behavior)
- **Availability:** S2S OAuth and Chatbot do NOT have refresh tokens
- **Rotation:** Each refresh returns a NEW refresh token (old one becomes invalid)

### Authorization Code
- **Purpose:** Temporary code exchanged for access token
- **Lifetime:** 5 minutes
- **Usage:** User OAuth and Device Flow only
- **One-time use:** Code becomes invalid after exchange

---

## Expiration Summary

| Flow | Access Token | Refresh Token | Strategy |
|------|--------------|---------------|----------|
| **S2S OAuth** | 1 hour | None | Request new token before expiration |
| **User OAuth** | 1 hour | ~90 days (commonly) | Use refresh token to get new access token |
| **Device Flow** | 1 hour | ~90 days (commonly) | Use refresh token to get new access token |
| **Chatbot** | 1 hour | None | Request new token before expiration |

---

## S2S OAuth & Chatbot Token Lifecycle

### Timeline

```
┌────────────────────────────────────────────────────┐
│                                                    │
│  Token Request                                     │
│       │                                            │
│       v                                            │
│  [ Access Token Valid ]                            │
│                                                    │
│  ├───────────────────── 1 hour ──────────────────┤ │
│                                                    │
│                                           Token    │
│                                           Expires  │
│                                                │   │
│                                                v   │
│  Request New Token ────────────────> [ New Access Token Valid ]
│                                                    │
└────────────────────────────────────────────────────┘
```

### Strategy: Cache with TTL

```javascript
const redis = require('redis');
const client = redis.createClient();

const getToken = async () => {
  // Check cache first
  let token = await client.get('zoom_access_token');
  
  if (!token) {
    // Request new token
    const response = await axios.post('https://zoom.us/oauth/token', ...);
    const { access_token, expires_in } = response.data;
    
    // Cache with TTL (10 second buffer before actual expiration)
    await client.setex('zoom_access_token', expires_in - 10, access_token);
    
    token = access_token;
  }
  
  return token;
};
```

**Key Points:**
- ✅ Cache token in Redis with TTL matching expiration
- ✅ Use 10-second buffer to prevent race conditions
- ✅ Single token shared across all requests
- ❌ Do NOT request new token on every API call
- ❌ Do NOT try to "refresh" (no refresh token exists)

---

## User OAuth & Device Flow Token Lifecycle

### Timeline

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  User Authorizes                                                   │
│       │                                                            │
│       v                                                            │
│  [ Access Token Valid ]                                            │
│  [ Refresh Token Valid ]────────────────────────────────────────┐  │
│                                                                 │  │
│  ├───────────── 1 hour ────────────┤                            │  │
│                                                                 │  │
│                            Access Token Expires                 │  │
│                                     │                           │  │
│                                     v                           │  │
│  Refresh Request ──────────> [ New Access Token Valid ]         │  │
│                              [ New Refresh Token Valid ]────┐   │  │
│                                                            │   │  │
│  ├───────────── 1 hour ────────────┤                       │   │  │
│                                                            │   │  │
│                            Access Token Expires            │   │  │
│                                     │                      │   │  │
│                                     v                      │   │  │
│  Refresh Request ──────────> [ New Access Token Valid ]    │   │  │
│                              [ New Refresh Token Valid ]   │   │  │
│                                                            │   │  │
│  ... Continue refreshing up to ~90 days (commonly) ...      │   │  │
│                                                            │   │  │
│  ├──────────────────────── ~90 days (commonly) ───────────┤   │  │
│                                                                │  │
│                                    Refresh Token Expires       │  │
│                                            │                   │  │
│                                            v                   │  │
│  User Must Re-Authorize (restart OAuth flow)                   │  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Strategy: Auto-Refresh Middleware

```javascript
const tokenMiddleware = async (req, res, next) => {
  const userId = req.session.userId;
  
  // Get user's tokens from database
  let { access_token, refresh_token, token_expiry } = await getUserTokens(userId);
  
  // Check if access token is expired or will expire soon (5 minute buffer)
  const now = Date.now();
  const expiresIn = token_expiry - now;
  
  if (expiresIn < 300000) { // Less than 5 minutes remaining
    // Refresh the token
    const response = await axios.post(
      'https://zoom.us/oauth/token',
      qs.stringify({
        grant_type: 'refresh_token',
        refresh_token: refresh_token
      }),
      {
        headers: {
          'Authorization': `Basic ${Buffer.from(
            `${CLIENT_ID}:${CLIENT_SECRET}`
          ).toString('base64')}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    
    const { access_token: new_access_token, refresh_token: new_refresh_token, expires_in } = response.data;
    
    // CRITICAL: Update BOTH tokens in database
    await updateUserTokens(userId, {
      access_token: new_access_token,
      refresh_token: new_refresh_token, // NEW refresh token
      token_expiry: now + (expires_in * 1000)
    });
    
    access_token = new_access_token;
  }
  
  // Attach token to request
  req.zoomToken = access_token;
  next();
};
```

**Key Points:**
- ✅ Refresh BEFORE token expires (5-minute buffer recommended)
- ✅ **ALWAYS save the NEW refresh token** (old one becomes invalid)
- ✅ Store tokens per user in database
- ✅ Encrypt tokens at rest (AES-256 minimum)
- ❌ Do NOT reuse old refresh token after refresh
- ❌ Do NOT wait for API 401 errors to trigger refresh

---

## Refresh Token Rotation

**CRITICAL:** Zoom rotates refresh tokens on every refresh.

### What Happens During Refresh

```
Before Refresh:
  access_token: "abc123"  (expired)
  refresh_token: "xyz789" (valid)

Request:
  POST /oauth/token
  grant_type=refresh_token
  refresh_token=xyz789

Response:
  {
    "access_token": "def456",      // NEW access token
    "refresh_token": "uvw012",     // NEW refresh token
    "expires_in": 3600
  }

After Refresh:
  access_token: "def456"  (valid for 1 hour)
  refresh_token: "uvw012" (lifetime varies; ~90 days is common)
  
  OLD refresh_token "xyz789" is NOW INVALID
```

### Common Mistake

```javascript
// ❌ WRONG: Not saving new refresh token
const response = await refreshToken(old_refresh_token);
const { access_token } = response.data; // Only saving access token

await updateUserTokens(userId, { access_token }); // Refresh token not updated!

// Next refresh will fail with error 4735 "Invalid refresh token"
```

```javascript
// ✅ CORRECT: Saving both tokens
const response = await refreshToken(old_refresh_token);
const { access_token, refresh_token } = response.data;

await updateUserTokens(userId, {
  access_token,
  refresh_token // MUST save new refresh token
});
```

---

## Authorization Code Expiration

**Lifetime:** 5 minutes

### Timeline

```
User Clicks "Allow"
       │
       v
Authorization Code Issued (expires in 5 minutes)
       │
       │  ← Exchange code for token within 5 minutes
       v
[ Access Token + Refresh Token ]

If code not exchanged within 5 minutes:
  → Error 4733 "Invalid authorization code"
  → User must re-authorize
```

### Implementation

```javascript
app.get('/callback', async (req, res) => {
  const { code } = req.query;
  
  try {
    // Exchange code for token IMMEDIATELY
    const response = await axios.post('https://zoom.us/oauth/token', {
      grant_type: 'authorization_code',
      code: code,
      redirect_uri: process.env.REDIRECT_URI
    }, ...);
    
    // Store tokens
    await saveTokens(response.data);
    
  } catch (error) {
    if (error.response?.data?.error === 'invalid_grant') {
      // Code expired (4733) or already used
      res.send('Authorization code expired. Please re-authorize.');
    }
  }
});
```

**Key Points:**
- ✅ Exchange authorization code **immediately** upon receiving it
- ✅ Authorization codes are one-time use
- ❌ Do NOT cache or store authorization codes
- ❌ Do NOT delay token exchange

---

## Token Revocation

### When Tokens Are Revoked

1. **User re-authorizes your app:**
   - All previous tokens for that user become invalid
   - New tokens are issued

2. **User removes your app:**
   - All tokens for that user become invalid
   - User must re-authorize to grant access again

3. **Explicit revocation:**
   - Your app calls `https://zoom.us/oauth/revoke` endpoint
   - Tokens become invalid immediately

4. **Refresh token expires (lifetime varies):**
   - Can no longer refresh
   - User must re-authorize

### Revoke Token API

```javascript
const revokeToken = async (access_token) => {
  await axios.post(
    'https://zoom.us/oauth/revoke',
    qs.stringify({
      token: access_token
    }),
    {
      headers: {
        'Authorization': `Basic ${Buffer.from(
          `${CLIENT_ID}:${CLIENT_SECRET}`
        ).toString('base64')}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
  );
  
  // Token is now revoked
  // Delete from database
  await deleteUserTokens(userId);
};
```

**What Gets Revoked:**
- Access token becomes invalid immediately
- Refresh token becomes invalid immediately
- All API requests with revoked token return 401

---

## Error Codes

| Code | Error | Meaning | Action |
|------|-------|---------|--------|
| **4733** | Invalid authorization code | Code expired (5 min) or already used | User must re-authorize |
| **4735** | Invalid refresh token | Refresh token expired or rotated | User must re-authorize |
| **4741** | Token has been revoked | Token was explicitly revoked | User must re-authorize |
| **401** | Unauthorized | Access token expired or invalid | Refresh token (if available) or re-authorize |

---

## Best Practices

### 1. Cache S2S Tokens

```javascript
// ✅ Cache in Redis with TTL
await redis.setex('zoom_token', expires_in - 10, access_token);
```

```javascript
// ❌ Request new token on every API call
const token = await getToken(); // Every time? No!
await makeAPIRequest(token);
```

### 2. Refresh BEFORE Expiration

```javascript
// ✅ Refresh with buffer (5 minutes before expiry)
if (expiresIn < 300000) {
  await refreshToken();
}
```

```javascript
// ❌ Wait for 401 error
try {
  await makeAPIRequest(token);
} catch (err) {
  if (err.status === 401) {
    await refreshToken(); // Too late!
  }
}
```

### 3. Always Save New Refresh Token

```javascript
// ✅ Update both tokens
const { access_token, refresh_token } = await refresh();
await saveTokens({ access_token, refresh_token });
```

```javascript
// ❌ Only save access token
const { access_token } = await refresh();
await saveTokens({ access_token }); // Refresh token not saved!
```

### 4. Encrypt Tokens at Rest

```javascript
// ✅ Encrypt before storing
const encrypted = encrypt(access_token, CIPHER_KEY);
await db.query('UPDATE users SET token = ? WHERE id = ?', [encrypted, userId]);
```

```javascript
// ❌ Store in plain text
await db.query('UPDATE users SET token = ? WHERE id = ?', [access_token, userId]);
```

### 5. Handle Revocation Gracefully

```javascript
// ✅ Detect revoked tokens and prompt re-auth
if (error.code === 4741) {
  await deleteUserTokens(userId);
  res.redirect('/auth'); // Re-authorize
}
```

---

## Debugging Token Issues

### Symptom: "Token expired" immediately after getting it

**Cause:** Server clock is incorrect

**Solution:**
```bash
# Sync server time
sudo ntpdate -s time.nist.gov
```

### Symptom: Refresh fails with "Invalid refresh token" (4735)

**Cause:** Using old refresh token after it was rotated

**Solution:**
- Check database: Are you saving the NEW refresh token?
- Check code: Are you updating BOTH access_token AND refresh_token?

### Symptom: Authorization code fails with "Invalid grant" (4733)

**Cause:** Code expired (5 minutes passed) or already used

**Solution:**
- Exchange code immediately in callback
- Codes are one-time use (don't cache)

### Symptom: All tokens revoked unexpectedly

**Cause:** User re-authorized your app or removed it

**Solution:**
- Detect 401/4741 errors
- Prompt user to re-authorize

---

## Next Steps

- **Implement auto-refresh** → [../examples/token-refresh.md](../examples/token-refresh.md)
- **Fix token errors** → [../troubleshooting/token-issues.md](../troubleshooting/token-issues.md)
- **Understand OAuth flows** → [oauth-flows.md](oauth-flows.md)

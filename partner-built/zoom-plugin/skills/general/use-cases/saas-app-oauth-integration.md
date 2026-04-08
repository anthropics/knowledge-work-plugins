# Building a SaaS App with Zoom OAuth Integration

Create a multi-tenant SaaS application that integrates with Zoom using User OAuth for per-user authorization.

## Scenario

You're building a meeting scheduling SaaS that needs to:
- Allow users to authorize your app to access their Zoom account
- Create meetings on behalf of users
- List user's meetings
- Store and refresh tokens securely per user
- Handle token expiration and refresh automatically

## Required Skills

1. **oauth** - User authorization flow, token management
2. **zoom-rest-api** - Meeting creation and management endpoints

## Architecture

```
User Browser → Your SaaS App → Zoom OAuth → Zoom APIs
                 ↓
           Database (user tokens)
```

## Implementation Steps

### 1. OAuth Setup (oauth)

**Configure app in Zoom Marketplace:**
- App Type: OAuth
- Redirect URL: `https://yourapp.com/oauth/callback`
- Required scopes: `meeting:write`, `meeting:read`, `user:read`

**See:** `oauth/concepts/oauth-flows.md#user-authorization-oauth`

### 2. User Authorization Flow (oauth)

```javascript
// Redirect user to Zoom authorization
app.get('/connect-zoom', (req, res) => {
  const state = generateSecureState();
  req.session.oauthState = state;
  
  res.redirect(
    `https://zoom.us/oauth/authorize?` +
    `response_type=code&` +
    `client_id=${CLIENT_ID}&` +
    `redirect_uri=${REDIRECT_URI}&` +
    `state=${state}`
  );
});
```

**See:** `oauth/examples/user-oauth-mysql.md`

### 3. Token Storage (oauth)

Store user tokens with encryption:

```javascript
// After OAuth callback
const { access_token, refresh_token } = await exchangeCode(code);

await db.users.update({
  zoom_access_token: encrypt(access_token),
  zoom_refresh_token: encrypt(refresh_token),
  token_expiry: Date.now() + 3600000
}, { where: { id: userId } });
```

**See:** `oauth/concepts/token-lifecycle.md#user-oauth--device-flow-token-lifecycle`

### 4. Auto-Refresh Middleware (oauth)

```javascript
// Automatically refresh expired tokens
const zoomTokenMiddleware = async (req, res, next) => {
  const user = await db.users.findByPk(req.session.userId);
  
  if (isTokenExpired(user.token_expiry)) {
    const newTokens = await refreshToken(user.zoom_refresh_token);
    await updateUserTokens(user.id, newTokens);
    req.zoomToken = newTokens.access_token;
  } else {
    req.zoomToken = decrypt(user.zoom_access_token);
  }
  
  next();
};
```

**See:** `oauth/examples/token-refresh.md`

### 5. Create Meetings (zoom-rest-api)

```javascript
app.post('/api/meetings', zoomTokenMiddleware, async (req, res) => {
  const meeting = await axios.post(
    'https://api.zoom.us/v2/users/me/meetings',
    {
      topic: req.body.topic,
      type: 2, // Scheduled meeting
      start_time: req.body.start_time,
      duration: req.body.duration
    },
    {
      headers: { Authorization: `Bearer ${req.zoomToken}` }
    }
  );
  
  res.json(meeting.data);
});
```

**See:** `zoom-rest-api` skill for endpoint documentation

## Security Considerations

### Token Encryption (oauth)

**MUST encrypt tokens at rest:**
```javascript
const crypto = require('crypto');

function encrypt(text) {
  const cipher = crypto.createCipher('aes-256-cbc', process.env.CIPHER_KEY);
  return cipher.update(text, 'utf8', 'hex') + cipher.final('hex');
}
```

**See:** `oauth/examples/user-oauth-mysql.md#token-encryption`

### State Parameter (oauth)

**Prevent CSRF attacks:**
```javascript
const state = crypto.randomBytes(16).toString('hex');
req.session.oauthState = state; // Verify in callback
```

**See:** `oauth/concepts/state-parameter.md`

## Handling Edge Cases

### User Revokes Access (webhooks)

Listen for deauthorization webhook:

```javascript
app.post('/webhooks/zoom', (req, res) => {
  if (req.body.event === 'app_deauthorized') {
    const userId = req.body.payload.user_id;
    await deleteUserZoomTokens(userId);
  }
});
```

**Chain to:** `webhooks` skill for webhook setup

### Refresh Token Expired (oauth)

```javascript
try {
  await refreshToken(user.zoom_refresh_token);
} catch (error) {
  if (error.code === 4735) {
    // Refresh token expired - prompt re-authorization
    res.redirect('/connect-zoom');
  }
}
```

**See:** `oauth/troubleshooting/token-issues.md`

## Testing Checklist

- [ ] User authorization flow works
- [ ] Tokens stored encrypted in database
- [ ] Tokens auto-refresh before expiration
- [ ] Meetings created successfully via API
- [ ] Deauthorization webhook handled
- [ ] Refresh token expiration handled

## Related Use Cases

- `meeting-automation.md` - Advanced meeting scheduling
- `user-and-meeting-creation.md` - Bulk user/meeting operations
- `recording-download-pipeline.md` - Download recordings via API

## Skills Used

- **oauth** (primary) - User OAuth, token management, PKCE
- **zoom-rest-api** - Meeting and user API endpoints
- **webhooks** - Deauthorization notifications

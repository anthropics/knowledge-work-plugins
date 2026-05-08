# State Parameter (CSRF Protection)

The `state` parameter prevents Cross-Site Request Forgery (CSRF) attacks in OAuth flows.

## What is CSRF in OAuth?

### Attack Scenario (Without State)

```
1. Attacker initiates OAuth flow for victim's account
2. Attacker gets authorization code in callback
3. Attacker tricks victim into visiting callback URL with attacker's code
4. Victim's app exchanges code and links attacker's Zoom account to victim's app account
5. Attacker now has access to victim's app data
```

### Protection (With State)

```
1. App generates random state before redirecting to OAuth
2. App stores state in user's session
3. Zoom includes state in callback
4. App verifies state matches session
5. If state doesn't match → Reject (CSRF detected)
```

## Implementation

### Step 1: Generate Random State

```javascript
const crypto = require('crypto');

app.get('/auth', (req, res) => {
  // Generate cryptographically secure random state
  const state = crypto.randomBytes(16).toString('hex');
  
  // Store in session (server-side)
  req.session.oauthState = state;
  
  const authURL = new URL('https://zoom.us/oauth/authorize');
  authURL.searchParams.set('response_type', 'code');
  authURL.searchParams.set('client_id', process.env.ZOOM_CLIENT_ID);
  authURL.searchParams.set('redirect_uri', process.env.ZOOM_REDIRECT_URL);
  authURL.searchParams.set('state', state); // Include state
  
  res.redirect(authURL.toString());
});
```

### Step 2: Verify State in Callback

```javascript
app.get('/callback', async (req, res) => {
  const { code, state } = req.query;
  const sessionState = req.session.oauthState;
  
  // Verify state matches
  if (state !== sessionState) {
    return res.status(403).send('Invalid state parameter - possible CSRF attack');
  }
  
  // Clean up state (one-time use)
  delete req.session.oauthState;
  
  // Proceed with token exchange
  const tokens = await exchangeCodeForToken(code);
  // ...
});
```

## State Parameter Flow

```
┌─────────────┐               ┌──────────────┐               ┌──────────────┐
│  Your App   │               │  User Session│               │  Zoom OAuth  │
└──────┬──────┘               └──────┬───────┘               └──────┬───────┘
       │                             │                              │
       │ 1. Generate state           │                              │
       │    state = "abc123"         │                              │
       │                             │                              │
       │ 2. Store in session         │                              │
       │────────────────────────────>│ session.oauthState = "abc123"
       │                             │                              │
       │ 3. Redirect to authorize with state                        │
       │https://zoom.us/oauth/authorize?state=abc123                │
       │───────────────────────────────────────────────────────────>│
       │                             │                              │
       │ 4. User authorizes          │                              │
       │                             │                              │
       │ 5. Redirect to callback with state                         │
       │  /callback?code=xyz&state=abc123                           │
       │<───────────────────────────────────────────────────────────│
       │                             │                              │
       │ 6. Retrieve session state   │                              │
       │<────────────────────────────│ sessionState = "abc123"      │
       │                             │                              │
       │ 7. Verify state === sessionState                           │
       │    "abc123" === "abc123" ✓  │                              │
       │                             │                              │
       │ 8. Exchange code for token  │                              │
       │───────────────────────────────────────────────────────────>│
       │                             │                              │
```

## Common Mistakes

### 1. Not Verifying State

```javascript
// ❌ WRONG: Accepting any state
app.get('/callback', async (req, res) => {
  const { code } = req.query;
  // No state verification!
  await exchangeCodeForToken(code);
});
```

```javascript
// ✅ CORRECT: Verifying state
app.get('/callback', async (req, res) => {
  const { code, state } = req.query;
  
  if (state !== req.session.oauthState) {
    return res.status(403).send('CSRF detected');
  }
  
  await exchangeCodeForToken(code);
});
```

### 2. Using Predictable State

```javascript
// ❌ WRONG: Predictable state
const state = Date.now().toString(); // Attacker can predict!
```

```javascript
// ✅ CORRECT: Cryptographically random state
const state = crypto.randomBytes(16).toString('hex');
```

### 3. Reusing State

```javascript
// ❌ WRONG: Not deleting state after use
if (state === req.session.oauthState) {
  // State remains in session - can be reused!
}
```

```javascript
// ✅ CORRECT: Delete state after verification
if (state === req.session.oauthState) {
  delete req.session.oauthState; // One-time use
}
```

## State + PKCE Together

For maximum security, use both:

```javascript
app.get('/auth', (req, res) => {
  // Generate state (CSRF protection)
  const state = crypto.randomBytes(16).toString('hex');
  req.session.oauthState = state;
  
  // Generate PKCE (authorization code interception protection)
  const { code_verifier, code_challenge } = generatePKCE();
  req.session.pkceVerifier = code_verifier;
  
  const authURL = new URL('https://zoom.us/oauth/authorize');
  authURL.searchParams.set('response_type', 'code');
  authURL.searchParams.set('client_id', CLIENT_ID);
  authURL.searchParams.set('redirect_uri', REDIRECT_URI);
  authURL.searchParams.set('state', state); // CSRF protection
  authURL.searchParams.set('code_challenge', code_challenge); // PKCE
  authURL.searchParams.set('code_challenge_method', 'S256');
  
  res.redirect(authURL.toString());
});

app.get('/callback', async (req, res) => {
  const { code, state } = req.query;
  
  // Verify state (CSRF)
  if (state !== req.session.oauthState) {
    return res.status(403).send('CSRF detected');
  }
  
  // Exchange with code_verifier (PKCE)
  const code_verifier = req.session.pkceVerifier;
  const tokens = await exchangeCode(code, code_verifier);
  
  // Clean up
  delete req.session.oauthState;
  delete req.session.pkceVerifier;
});
```

## Mobile Apps

For mobile apps without server-side sessions:

```javascript
// Store state in secure storage
const state = generateRandomString();
await SecureStore.setItemAsync('oauth_state', state);

// Verify in callback
const storedState = await SecureStore.getItemAsync('oauth_state');
if (receivedState !== storedState) {
  throw new Error('CSRF detected');
}

// Clean up
await SecureStore.deleteItemAsync('oauth_state');
```

## Best Practices

1. **Always use state** for User OAuth and Device Flow
2. **Generate cryptographically random state** (not timestamps, sequential IDs)
3. **Store state server-side** in session (not client-side cookies)
4. **Delete state after verification** (one-time use)
5. **Combine with PKCE** for mobile/SPA apps

## Next Steps

- **Implement state + PKCE** → [../examples/pkce-implementation.md](../examples/pkce-implementation.md)
- **Understand PKCE** → [pkce.md](pkce.md)
- **Fix OAuth errors** → [../troubleshooting/common-errors.md](../troubleshooting/common-errors.md)

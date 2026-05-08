# Video SDK - Authorization

Generate JWT signatures for Video SDK authentication.

## Overview

Video SDK uses JWT (JSON Web Token) signatures to authenticate users joining video sessions. Signatures must be generated server-side to protect your SDK Secret.

**Important**: Unlike Zoom Meetings, Video SDK sessions are NOT pre-created. The `tpc` (topic) in your JWT can be any string you choose - the session is created when the first participant joins with that topic.

## Prerequisites

- Video SDK Key and Secret from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- Server-side code to generate signatures

## JWT Structure

| Claim | Description |
|-------|-------------|
| `app_key` | Your SDK Key |
| `tpc` | Topic (session name) - **any string you choose** |
| `role_type` | 0 = participant, 1 = host |
| `user_identity` | (Optional) Unique user identifier |
| `iat` | Issued at timestamp |
| `exp` | Expiration timestamp |

**Note on `tpc` (Topic)**:
- Can be any string (e.g., `"room-123"`, `"consultation-abc"`, `"game-lobby-5"`)
- All users joining with the same `tpc` value join the same session
- Session is created automatically when first user joins
- No API call needed to create the session beforehand

## Host and Co-Host via roleType

In Video SDK, host/co-host status is determined entirely by `role_type` in the JWT — not by runtime API calls.

| role_type | First to Join | Subsequent Joiners |
|-----------|--------------|-------------------|
| 1 | Host | Co-host |
| 0 | Participant | Participant |

- Only host or co-host can call `client.leave(true)` to end session for all
- A participant calling `leave(true)` only leaves themselves
- No need for `makeHost()` or `makeManager()` API calls — use JWT roleType instead

### Session Creation Pattern (Bot as Host)

For scenarios where you need a bot to create and manage the session:

1. **Bot** joins with `role_type: 1` → becomes host (creates session)
2. **User A** joins with `role_type: 1` → becomes co-host
3. **Bot leaves** → User A remains as co-host, can end session
4. **User B** joins with `role_type: 0` → participant

This pattern avoids race conditions from runtime host assignment.

```javascript
// JWT generation examples
generateJWT(key, secret, sessionName, 1, 'SessionBot');    // Bot: host
generateJWT(key, secret, sessionName, 1, 'Advisor');       // Advisor: co-host
generateJWT(key, secret, sessionName, 0, 'Customer');      // Customer: participant
```

## Signature Generation Best Practices

### Short-Lived Tokens (Recommended)

For security, generate tokens with short expiry:

```javascript
const iat = Math.floor(Date.now() / 1000) - 7200; // 2 hours in the past
const exp = Math.floor(Date.now() / 1000) + 10;   // 10 seconds from now

const payload = {
  app_key: SDK_KEY,
  tpc: topic,
  role_type: role,
  user_identity: userIdentity,
  iat: iat,
  exp: exp
};
```

**Why this works:**
- `exp` is only 10 seconds after generation (short-lived for security)
- `iat` is set 2 hours in the past to satisfy Zoom's requirement that `exp - iat >= 2 hours`
- Token is generated just before joining, so 10 second window is sufficient

### Server-Side Example (Node.js)

```javascript
const jwt = require('jsonwebtoken');

function generateSignature(sdkKey, sdkSecret, topic, role, userIdentity) {
  const iat = Math.floor(Date.now() / 1000) - 7200; // 2 hours ago
  const exp = Math.floor(Date.now() / 1000) + 10;   // 10 seconds from now
  
  const payload = {
    app_key: sdkKey,
    tpc: topic,
    role_type: role,
    user_identity: userIdentity || '',
    iat: iat,
    exp: exp
  };
  
  return jwt.sign(payload, sdkSecret, { algorithm: 'HS256' });
}
```

## Security Guidelines

| Do | Don't |
|----|-------|
| Generate signatures server-side | Expose SDK Secret in client code |
| Use short expiry times | Use long-lived tokens |
| Validate user before generating | Generate for unauthenticated users |

## Resources

- **Auth docs**: https://developers.zoom.us/docs/video-sdk/auth/

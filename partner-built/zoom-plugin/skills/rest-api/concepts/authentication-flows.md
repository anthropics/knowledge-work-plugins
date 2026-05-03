# Authentication Flows

All Zoom REST API requests require OAuth 2.0 authentication. This guide covers all supported OAuth flows and when to use each.

> **Complete OAuth implementation guide:** See the **[zoom-oauth](../../oauth/SKILL.md)** skill for full code examples, token storage, and production patterns.

## Flow Selection

| Flow | Use Case | User Interaction | Token Lifetime |
|------|----------|------------------|----------------|
| **Server-to-Server OAuth** | Backend automation, bots, integrations | None | 1 hour |
| **Authorization Code** | User-facing web apps | User consent flow | 1 hour (refresh: 15 years) |
| **Authorization Code + PKCE** | SPAs, mobile apps | User consent flow | 1 hour (refresh: 15 years) |
| **Device Code** | TV/IoT devices, CLI tools | User enters code on separate device | 1 hour (refresh: 15 years) |
| ~~**JWT**~~ | ~~Legacy~~ | ~~None~~ | **DEPRECATED** — migrate to S2S OAuth |

## Server-to-Server OAuth (Recommended for Backend)

No user interaction required. Best for automation, scheduled tasks, and backend services.

### Setup

1. Go to [Zoom App Marketplace](https://marketplace.zoom.us/) → **Develop** → **Build App**
2. Select **Server-to-Server OAuth**
3. Note: **Account ID**, **Client ID**, **Client Secret**
4. Add required scopes (e.g., `meeting:write:admin`, `user:read:admin`)

### Get Access Token

```bash
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n 'CLIENT_ID:CLIENT_SECRET' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=account_credentials&account_id=ACCOUNT_ID"
```

### Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "meeting:read meeting:write user:read",
  "api_url": "https://api.zoom.us"
}
```

### Node.js — Token Manager with Auto-Refresh

```javascript
class ZoomS2SAuth {
  constructor(accountId, clientId, clientSecret) {
    this.accountId = accountId;
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.token = null;
    this.tokenExpiry = 0;
  }

  async getAccessToken() {
    // Return cached token if valid (with 60s buffer)
    if (this.token && Date.now() < this.tokenExpiry - 60000) {
      return this.token;
    }

    const credentials = Buffer.from(
      `${this.clientId}:${this.clientSecret}`
    ).toString('base64');

    const response = await fetch('https://zoom.us/oauth/token', {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${credentials}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `grant_type=account_credentials&account_id=${this.accountId}`
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(`Token error: ${err.error} - ${err.reason}`);
    }

    const data = await response.json();
    this.token = data.access_token;
    this.tokenExpiry = Date.now() + (data.expires_in * 1000);

    return this.token;
  }

  async request(method, path, body = null) {
    const token = await this.getAccessToken();

    const response = await fetch(`https://api.zoom.us/v2${path}`, {
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: body ? JSON.stringify(body) : undefined
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(`Zoom API ${response.status}: ${JSON.stringify(err)}`);
    }

    // Some endpoints return 204 No Content
    if (response.status === 204) return null;
    return response.json();
  }
}

// Usage
const zoom = new ZoomS2SAuth(
  process.env.ZOOM_ACCOUNT_ID,
  process.env.ZOOM_CLIENT_ID,
  process.env.ZOOM_CLIENT_SECRET
);

const users = await zoom.request('GET', '/users?page_size=300');
const meeting = await zoom.request('POST', '/users/user@example.com/meetings', {
  topic: 'API Meeting', type: 2, duration: 30
});
```

### Python — Token Manager

```python
import requests
import time
from base64 import b64encode

class ZoomS2SAuth:
    def __init__(self, account_id, client_id, client_secret):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiry = 0

    def get_access_token(self):
        if self.token and time.time() < self.token_expiry - 60:
            return self.token

        credentials = b64encode(
            f'{self.client_id}:{self.client_secret}'.encode()
        ).decode()

        response = requests.post(
            'https://zoom.us/oauth/token',
            headers={
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=f'grant_type=account_credentials&account_id={self.account_id}'
        )
        response.raise_for_status()

        data = response.json()
        self.token = data['access_token']
        self.token_expiry = time.time() + data['expires_in']
        return self.token

    def request(self, method, path, json_data=None):
        token = self.get_access_token()
        response = requests.request(
            method,
            f'https://api.zoom.us/v2{path}',
            headers={'Authorization': f'Bearer {token}'},
            json=json_data
        )
        response.raise_for_status()
        return response.json() if response.content else None
```

## User OAuth (Authorization Code)

For apps that act on behalf of individual Zoom users.

### Flow

```
1. User clicks "Connect to Zoom"
2. Redirect to: https://zoom.us/oauth/authorize?response_type=code&client_id=XXX&redirect_uri=YYY&state=ZZZ
3. User grants permission
4. Zoom redirects to callback: https://yourapp.com/callback?code=AUTH_CODE&state=ZZZ
5. Exchange code for tokens
6. Use access_token for API calls
7. Refresh when expired
```

### Exchange Code for Token

```bash
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n 'CLIENT_ID:CLIENT_SECRET' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=AUTH_CODE&redirect_uri=https://yourapp.com/callback"
```

### Refresh Token

```bash
curl -X POST "https://zoom.us/oauth/token" \
  -H "Authorization: Basic $(echo -n 'CLIENT_ID:CLIENT_SECRET' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=REFRESH_TOKEN"
```

### Important: `me` Keyword

User OAuth apps **must** use `me` instead of `userId` in API paths:

```bash
# CORRECT for user OAuth
GET /v2/users/me/meetings

# WRONG for user OAuth — will return "Invalid access token"
GET /v2/users/abc123/meetings
```

## Common Scopes

| Scope | Description |
|-------|-------------|
| `user:read` | Read user profile |
| `user:read:admin` | Read all users (admin) |
| `user:write:admin` | Manage all users (admin) |
| `meeting:read` | Read meeting data |
| `meeting:write` | Create/update meetings |
| `meeting:write:admin` | Create/update any user's meetings |
| `recording:read` | Access recordings |
| `recording:write` | Manage recordings |
| `webinar:read` | Read webinar data |
| `webinar:write` | Manage webinars |
| `report:read:admin` | View reports |

**Best practice:** Request only the scopes you need. Fewer scopes = less user friction and faster app approval.

## Token Storage Best Practices

```javascript
// DO: Encrypt tokens at rest
const encrypted = encrypt(accessToken, process.env.ENCRYPTION_KEY);
await db.tokens.upsert({ userId, encrypted, expiresAt });

// DO: Use httpOnly secure cookies for web apps
res.cookie('zoom_session', sessionId, {
  httpOnly: true, secure: true, sameSite: 'strict', maxAge: 3600000
});

// DON'T: Store tokens in localStorage or log them
localStorage.setItem('zoom_token', token);  // INSECURE
console.log('Token:', accessToken);          // LEAKS CREDENTIALS
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_grant` | Expired/used auth code or refresh token | Restart OAuth flow or re-authenticate |
| `invalid_client` | Wrong client ID or secret | Verify credentials |
| `invalid_scope` | Scope not approved for your app | Check app scopes in Marketplace |
| `access_denied` | User denied permission | Handle gracefully in UI |

```javascript
try {
  const token = await refreshAccessToken(refreshToken);
} catch (error) {
  if (error.response?.data?.error === 'invalid_grant') {
    // Refresh token revoked or expired — re-authenticate
    redirectToOAuthFlow();
  }
}
```

## Migration from JWT (Deprecated)

The JWT app type on Zoom Marketplace is deprecated. This does **not** affect JWT token signatures used elsewhere (e.g., Video SDK).

**Steps:**
1. Create a Server-to-Server OAuth app
2. Request the same scopes
3. Replace JWT token generation with OAuth token endpoint
4. Test all endpoints
5. Delete the JWT app

## Resources

- **OAuth Guide**: https://developers.zoom.us/docs/integrations/oauth/
- **S2S OAuth**: https://developers.zoom.us/docs/internal-apps/s2s-oauth/
- **Scopes Reference**: https://developers.zoom.us/docs/integrations/oauth-scopes/
- **Full OAuth Skill**: See **[zoom-oauth](../../oauth/SKILL.md)**

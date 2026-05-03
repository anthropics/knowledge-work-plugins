# Backend Automation with Server-to-Server OAuth

Automate Zoom account operations using Server-to-Server OAuth for machine-to-machine authentication.

## Scenario

You're building a backend service that needs to:
- Automatically create and manage meetings for your organization
- Generate meeting reports
- Provision and deprovision users
- No user interaction required
- Account-wide API access

## Required Skills

1. **oauth** - S2S OAuth token management
2. **zoom-rest-api** - Account management endpoints

## Architecture

```
Cron Job / Backend Service
       ↓
   Token Cache (Redis)
       ↓
   Zoom APIs (account-wide access)
```

## Implementation

### 1. S2S OAuth Setup (oauth)

**Configure app in Zoom Marketplace:**
- App Type: Server-to-Server OAuth
- Add required scopes: `meeting:write:admin`, `user:write:admin`, `report:read:admin`
- Get credentials: Account ID, Client ID, Client Secret

**See:** `oauth/concepts/oauth-flows.md#server-to-server-s2s-oauth`

### 2. Token Management with Redis (oauth)

```javascript
const redis = require('redis');
const client = redis.createClient();

async function getZoomToken() {
  // Check cache first
  let token = await client.get('zoom_s2s_token');
  
  if (!token) {
    // Request new token
    const response = await axios.post(
      'https://zoom.us/oauth/token',
      'grant_type=account_credentials&account_id=' + ACCOUNT_ID,
      {
        headers: {
          'Authorization': 'Basic ' + Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')
        }
      }
    );
    
    token = response.data.access_token;
    
    // Cache with TTL (10 second buffer before actual expiration)
    await client.setex('zoom_s2s_token', response.data.expires_in - 10, token);
  }
  
  return token;
}
```

**See:** `oauth/examples/s2s-oauth-redis.md`

### 3. Automated User Provisioning (zoom-rest-api)

```javascript
// Daily cron job to sync users
cron.schedule('0 0 * * *', async () => {
  const token = await getZoomToken();
  
  const newUsers = await getNewUsersFromHR();
  
  for (const user of newUsers) {
    await axios.post(
      'https://api.zoom.us/v2/users',
      {
        action: 'create',
        user_info: {
          email: user.email,
          type: 1,
          first_name: user.firstName,
          last_name: user.lastName
        }
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );
  }
});
```

**Chain to:** `zoom-rest-api` for endpoint details

### 4. Meeting Reports (zoom-rest-api)

```javascript
// Generate weekly meeting reports
async function generateWeeklyReport() {
  const token = await getZoomToken();
  
  const response = await axios.get(
    'https://api.zoom.us/v2/report/users',
    {
      params: {
        from: startOfWeek(),
        to: endOfWeek()
      },
      headers: { Authorization: `Bearer ${token}` }
    }
  );
  
  return response.data.users;
}
```

**Chain to:** `zoom-rest-api` reporting endpoints

## Production Deployment

### Docker Setup (oauth)

```yaml
# docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    
  automation-service:
    build: .
    environment:
      - ZOOM_ACCOUNT_ID=${ZOOM_ACCOUNT_ID}
      - ZOOM_CLIENT_ID=${ZOOM_CLIENT_ID}
      - ZOOM_CLIENT_SECRET=${ZOOM_CLIENT_SECRET}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
```

**See:** `oauth/examples/s2s-oauth-redis.md#docker-deployment`

## Error Handling

### Token Errors (oauth)

```javascript
try {
  const token = await getZoomToken();
} catch (error) {
  if (error.response?.data?.error === 'invalid_client') {
    // Invalid credentials
    logger.error('Invalid Zoom credentials');
    alertOps('Zoom integration broken - check credentials');
  }
}
```

**See:** `oauth/troubleshooting/common-errors.md`

### Rate Limiting (zoom-rest-api)

```javascript
// Implement retry logic for rate limits
const retryRequest = async (fn, retries = 3) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.response?.status === 429) {
        // Rate limited - wait and retry
        await sleep(Math.pow(2, i) * 1000);
        continue;
      }
      throw error;
    }
  }
};
```

**Chain to:** `zoom-rest-api` for rate limit details

## Testing

```javascript
// Test S2S token acquisition
describe('S2S OAuth', () => {
  it('should get valid access token', async () => {
    const token = await getZoomToken();
    expect(token).toMatch(/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/);
  });
  
  it('should cache token in Redis', async () => {
    await getZoomToken();
    const cached = await client.get('zoom_s2s_token');
    expect(cached).toBeTruthy();
  });
});
```

## Related Use Cases

- `meeting-automation.md` - Advanced meeting workflows
- `usage-reporting-analytics.md` - Account usage analytics
- `user-and-meeting-creation.md` - Bulk operations

## Skills Used

- **oauth** (primary) - S2S OAuth, token caching
- **zoom-rest-api** - Account management, reporting
- **webhooks** - Real-time event notifications

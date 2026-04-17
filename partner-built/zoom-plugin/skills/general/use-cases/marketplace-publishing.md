# Marketplace Publishing & ISV Guide

Build and publish apps on the Zoom App Marketplace for multiple customers.

## Overview

This guide covers building multi-tenant applications for the Zoom Marketplace, handling multiple customer accounts, and the app review process.

## Skills Needed

- **general** - App configuration
- **zoom-rest-api** - Multi-tenant API calls
- **webhooks** - Per-customer event handling

---

## App Types for Marketplace

| App Type | Visibility | Use Case |
|----------|-----------|----------|
| **Account-level (Private)** | Your org only | Internal tools |
| **User-managed (Public)** | Individual users | User-facing apps |
| **Admin-managed (Public)** | Org admins install | Enterprise tools |

For Marketplace publishing, you'll create **Public** apps.

---

## Multi-Tenant Architecture

### Database Schema

Store per-customer OAuth tokens and settings:

```sql
CREATE TABLE zoom_installations (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(255) UNIQUE NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    token_expires_at TIMESTAMP NOT NULL,
    installed_at TIMESTAMP DEFAULT NOW(),
    settings JSONB DEFAULT '{}'
);

CREATE INDEX idx_zoom_account ON zoom_installations(account_id);
```

### OAuth Token Storage

```javascript
// Store tokens after OAuth callback
async function handleOAuthCallback(code, state) {
  // Exchange code for tokens
  const tokens = await exchangeCodeForTokens(code);
  
  // Get account info
  const accountInfo = await getAccountInfo(tokens.access_token);
  
  // Store or update installation
  await db.query(`
    INSERT INTO zoom_installations 
    (account_id, access_token, refresh_token, token_expires_at)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT (account_id) 
    DO UPDATE SET 
      access_token = $2,
      refresh_token = $3,
      token_expires_at = $4
  `, [
    accountInfo.account_id,
    tokens.access_token,
    tokens.refresh_token,
    new Date(Date.now() + tokens.expires_in * 1000)
  ]);
  
  return accountInfo.account_id;
}
```

### Token Refresh

```javascript
async function getValidToken(accountId) {
  const installation = await db.query(
    'SELECT * FROM zoom_installations WHERE account_id = $1',
    [accountId]
  );
  
  if (!installation) {
    throw new Error('Account not installed');
  }
  
  // Check if token needs refresh
  if (new Date(installation.token_expires_at) < new Date()) {
    const newTokens = await refreshTokens(installation.refresh_token);
    
    await db.query(`
      UPDATE zoom_installations 
      SET access_token = $1, refresh_token = $2, token_expires_at = $3
      WHERE account_id = $4
    `, [
      newTokens.access_token,
      newTokens.refresh_token,
      new Date(Date.now() + newTokens.expires_in * 1000),
      accountId
    ]);
    
    return newTokens.access_token;
  }
  
  return installation.access_token;
}
```

---

## Webhook Handling for Multi-Tenant

### Routing by Account

```javascript
app.post('/webhook', async (req, res) => {
  // Verify signature first
  if (!verifyWebhookSignature(req)) {
    return res.status(401).send('Invalid signature');
  }
  
  const { event, payload } = req.body;
  const accountId = payload.account_id;
  
  // Check if this account has installed our app
  const installation = await getInstallation(accountId);
  if (!installation) {
    console.log(`Webhook for unknown account: ${accountId}`);
    return res.status(200).send(); // Still return 200
  }
  
  // Process event for this customer
  await processEventForCustomer(accountId, event, payload);
  
  res.status(200).send();
});

async function processEventForCustomer(accountId, event, payload) {
  switch (event) {
    case 'meeting.started':
      await handleMeetingStarted(accountId, payload);
      break;
    case 'recording.completed':
      await handleRecordingCompleted(accountId, payload);
      break;
  }
}
```

### Deauthorization Handling

When a customer uninstalls your app:

```javascript
app.post('/webhook', async (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'app_deauthorized') {
    const accountId = payload.account_id;
    
    // Clean up customer data
    await db.query('DELETE FROM zoom_installations WHERE account_id = $1', [accountId]);
    
    // Optional: Delete customer data per compliance requirements
    await cleanupCustomerData(accountId);
    
    console.log(`App deauthorized for account: ${accountId}`);
  }
  
  res.status(200).send();
});
```

---

## API Calls for Specific Customers

```javascript
class ZoomAPIClient {
  constructor(accountId) {
    this.accountId = accountId;
  }
  
  async request(method, endpoint, data = null) {
    const token = await getValidToken(this.accountId);
    
    const response = await axios({
      method,
      url: `https://api.zoom.us/v2${endpoint}`,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data
    });
    
    return response.data;
  }
  
  async createMeeting(userId, meetingData) {
    return this.request('POST', `/users/${userId}/meetings`, meetingData);
  }
  
  async getUsers() {
    return this.request('GET', '/users');
  }
}

// Usage
const client = new ZoomAPIClient('customer_account_id');
const meeting = await client.createMeeting('me', { topic: 'Team Sync' });
```

---

## Scopes for Marketplace Apps

Request minimal scopes needed:

```javascript
// Good - specific scopes
const scopes = [
  'meeting:read',
  'meeting:write',
  'user:read'
];

// Bad - overly broad
const scopes = [
  'account:read:admin',
  'account:write:admin'
];
```

### Scope Descriptions

Provide clear descriptions for each scope in Marketplace:

| Scope | User-Facing Description |
|-------|------------------------|
| `meeting:read` | View your meetings |
| `meeting:write` | Create and update meetings on your behalf |
| `recording:read` | Access your meeting recordings |

---

## App Review Process

### Pre-Submission Checklist

- [ ] All required scopes have descriptions
- [ ] Privacy policy URL is valid and accessible
- [ ] Terms of service URL is valid
- [ ] Support email/URL is configured
- [ ] App description is clear and accurate
- [ ] Screenshots show actual app functionality
- [ ] Deauthorization webhook handles cleanup
- [ ] OAuth flow completes successfully
- [ ] Error handling is user-friendly

### Common Rejection Reasons

1. **Excessive scopes** - Only request what you need
2. **Missing deauthorization handling** - Must handle `app_deauthorized`
3. **Broken OAuth flow** - Test thoroughly
4. **Poor error messages** - Be user-friendly
5. **Privacy policy issues** - Must cover Zoom data usage
6. **Non-functional features** - All advertised features must work

### Testing Before Submission

```javascript
// Test OAuth flow
async function testOAuthFlow() {
  // 1. Generate auth URL
  const authUrl = generateAuthUrl();
  console.log('Auth URL:', authUrl);
  
  // 2. Complete OAuth manually in browser
  // 3. Verify token storage
  
  // 4. Test API calls
  const client = new ZoomAPIClient(testAccountId);
  const users = await client.getUsers();
  console.log('Users:', users);
  
  // 5. Test webhook handling
  await simulateWebhook('meeting.started', testPayload);
}

// Test deauthorization
async function testDeauthorization() {
  // Simulate deauth webhook
  await simulateWebhook('app_deauthorized', {
    account_id: testAccountId
  });
  
  // Verify cleanup
  const installation = await getInstallation(testAccountId);
  console.assert(installation === null, 'Installation should be deleted');
}
```

---

## Data Residency & Compliance

### Handle Regional Requirements

```javascript
// Determine storage region based on user location
async function getStorageRegion(accountId) {
  const accountInfo = await zoomClient.getAccountInfo(accountId);
  
  // Map Zoom data center to storage region
  const regionMap = {
    'US': 'us-east-1',
    'EU': 'eu-west-1',
    'AU': 'ap-southeast-2',
    'IN': 'ap-south-1'
  };
  
  return regionMap[accountInfo.data_residency_region] || 'us-east-1';
}

// Store data in correct region
async function storeData(accountId, data) {
  const region = await getStorageRegion(accountId);
  const regionalStorage = getStorageClient(region);
  
  await regionalStorage.put(data);
}
```

---

## Rate Limiting for Multi-Tenant

Implement per-customer rate limiting:

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');

const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:'
  }),
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute per customer
  keyGenerator: (req) => {
    // Rate limit per customer account
    return req.headers['x-account-id'] || req.ip;
  }
});

app.use('/api/', apiLimiter);
```

---

## Publishing Steps

1. **Development** - Build and test thoroughly
2. **Submit for Review** - In Marketplace portal
3. **Review Period** - 2-4 weeks typically
4. **Address Feedback** - Fix any issues found
5. **Approval** - App goes live
6. **Maintenance** - Monitor, update, support

## Resources

- **Marketplace Portal**: https://marketplace.zoom.us/
- **Publishing Guide**: https://developers.zoom.us/docs/zoom-apps/publishing/
- **App Review**: https://developers.zoom.us/docs/distribute/app-review/
- **ISV Program**: https://zoom.us/partners/isv

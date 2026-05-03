# Testing & Development Environment

Set up development and testing environments for Zoom integrations.

## Overview

Zoom provides several options for development and testing:
- Development app credentials (separate from production)
- Test accounts
- Local webhook testing tools
- SDK sandbox modes

## Skills Needed

- **general** - App configuration
- **webhooks** - Webhook testing

---

## Development vs Production Apps

### Create Separate Apps

**Always create separate apps for development and production:**

| Environment | Purpose | Credentials |
|-------------|---------|-------------|
| Development | Testing, debugging | Dev Client ID/Secret |
| Production | Live users | Prod Client ID/Secret |

1. Go to [Zoom Marketplace](https://marketplace.zoom.us/)
2. Create "MyApp - Development" for testing
3. Create "MyApp - Production" for live deployment
4. Use environment variables to switch between them

```javascript
// .env.development
ZOOM_CLIENT_ID=dev_client_id_here
ZOOM_CLIENT_SECRET=dev_secret_here
ZOOM_ACCOUNT_ID=dev_account_id

// .env.production
ZOOM_CLIENT_ID=prod_client_id_here
ZOOM_CLIENT_SECRET=prod_secret_here
ZOOM_ACCOUNT_ID=prod_account_id
```

---

## Test Accounts

### Option 1: Developer Account

Use your own Zoom account for initial development:
- Free tier works for basic API testing
- Pro account needed for SDK testing
- Create test meetings manually

### Option 2: Zoom Developer Sandbox (ISV Partners)

ISV partners can request sandbox accounts:
- Contact Zoom partnership team
- Isolated test environment
- Multiple test users

### Option 3: Programmatic Test Users

Create test users via API (requires admin account):

```javascript
// Create a test user
const response = await axios.post(
  'https://api.zoom.us/v2/users',
  {
    action: 'create',
    user_info: {
      email: 'testuser+1@yourcompany.com',  // Use + alias
      type: 1,  // Basic user
      first_name: 'Test',
      last_name: 'User'
    }
  },
  { headers: { 'Authorization': `Bearer ${accessToken}` }}
);
```

**Tip**: Use email aliases (`testuser+1@company.com`, `testuser+2@company.com`) that all route to one inbox.

---

## Local Webhook Testing

### Option 1: ngrok (Recommended)

Expose your local development webhook server to the internet for testing:

```bash
# Install ngrok
npm install -g ngrok

# Start your local server
node server.js  # Running on port 3000

# In another terminal, create tunnel
ngrok http 3000
```

Output:
```
Forwarding  https://abc123.ngrok.io -> http://YOUR_DEV_HOST:3000
```

Use `https://abc123.ngrok.io/webhook` as your webhook URL in Zoom Marketplace.

### Option 2: Cloudflare Tunnel

```bash
# Install cloudflared
brew install cloudflare/cloudflare/cloudflared

# Create tunnel
LOCAL_WEBHOOK_BASE_URL="http://YOUR_DEV_HOST:3000"
cloudflared tunnel --url "$LOCAL_WEBHOOK_BASE_URL"
```

### Option 3: localtunnel

```bash
npm install -g localtunnel
lt --port 3000
```

### Webhook URL Validation

Zoom requires validating your webhook endpoint. Your server must respond to the challenge:

```javascript
app.post('/webhook', (req, res) => {
  // Handle Zoom's endpoint validation
  if (req.body.event === 'endpoint.url_validation') {
    const hashForValidate = crypto
      .createHmac('sha256', ZOOM_WEBHOOK_SECRET)
      .update(req.body.payload.plainToken)
      .digest('hex');
    
    return res.json({
      plainToken: req.body.payload.plainToken,
      encryptedToken: hashForValidate
    });
  }
  
  // Handle actual events
  // ...
});
```

---

## SDK Development Mode

### Meeting SDK Web

Enable debug logging:

```javascript
const client = ZoomMtgEmbedded.createClient();

client.init({
  debug: true,  // Enable debug logs
  zoomAppRoot: document.getElementById('meetingSDKElement'),
  language: 'en-US',
});
```

### Video SDK Web

```javascript
const client = ZoomVideo.createClient();

await client.init('en-US', 'CDN', {
  enforceMultipleVideos: true,
  stayAwake: true,
  patchJsMedia: true,
  leaveOnPageUnload: true,
});

// Enable debug mode
ZoomVideo.setLogLevel('debug');
```

### Native SDKs (iOS/Android/Desktop)

Enable verbose logging:

```swift
// iOS
let initParams = ZoomVideoSDKInitParams()
initParams.enableLog = true
initParams.logFilePrefix = "videosdk_debug"
```

```kotlin
// Android
val initParams = ZoomVideoSDKInitParams().apply {
    enableLog = true
    logFilePrefix = "videosdk_debug"
}
```

---

## Mock Webhook Events

### Manual Testing with curl

Test your webhook handler locally:

```bash
LOCAL_WEBHOOK_BASE_URL="http://YOUR_DEV_HOST:3000"

# Simulate meeting.started event
curl -X POST "$LOCAL_WEBHOOK_BASE_URL/webhook" \
  -H "Content-Type: application/json" \
  -H "x-zm-signature: v0=test" \
  -H "x-zm-request-timestamp: $(date +%s)" \
  -d '{
    "event": "meeting.started",
    "payload": {
      "account_id": "abc123",
      "object": {
        "id": "123456789",
        "uuid": "abcd-1234-efgh",
        "topic": "Test Meeting",
        "host_id": "xyz789"
      }
    }
  }'
```

### Webhook Replay Tool

Build a simple replay tool for testing:

```javascript
const fs = require('fs');

// Save incoming webhooks to file
app.post('/webhook', (req, res) => {
  const filename = `webhooks/${Date.now()}_${req.body.event}.json`;
  fs.writeFileSync(filename, JSON.stringify(req.body, null, 2));
  
  // Process normally...
});

// Replay saved webhook
async function replayWebhook(filename) {
  const payload = JSON.parse(fs.readFileSync(filename));
  await processWebhook(payload);
}
```

---

## Testing Checklist

### Before Going Live

- [ ] Test OAuth flow end-to-end
- [ ] Verify webhook signature validation
- [ ] Test with multiple user types (host, participant, admin)
- [ ] Handle rate limiting gracefully
- [ ] Test error scenarios (invalid tokens, network failures)
- [ ] Verify recording download permissions
- [ ] Test SDK on all target platforms
- [ ] Load test with expected user volume

### API Testing

```javascript
// Test helper for API calls
async function testAPICall(name, fn) {
  console.log(`Testing: ${name}`);
  try {
    const result = await fn();
    console.log(`Pass: ${name}`);
    return result;
  } catch (error) {
    console.error(`Fail: ${name}:`, error.message);
    throw error;
  }
}

// Run tests
await testAPICall('Create meeting', () => 
  createMeeting({ topic: 'Test' })
);
await testAPICall('Get meeting', () => 
  getMeeting(meetingId)
);
await testAPICall('Delete meeting', () => 
  deleteMeeting(meetingId)
);
```

---

## Debugging Tips

### Enable Request Logging

```javascript
const axios = require('axios');

// Log all requests
axios.interceptors.request.use(config => {
  console.log(`-> ${config.method.toUpperCase()} ${config.url}`);
  return config;
});

axios.interceptors.response.use(
  response => {
    console.log(`<- ${response.status} ${response.config.url}`);
    return response;
  },
  error => {
    console.error(`<- ${error.response?.status} ${error.config?.url}`);
    console.error('Error:', error.response?.data);
    throw error;
  }
);
```

### SDK Log Collection

See [SDK Logs & Troubleshooting](../references/sdk-logs-troubleshooting.md) for collecting SDK debug logs.

## Resources

- **ngrok**: https://ngrok.com/
- **Postman Collection**: https://developers.zoom.us/docs/api/rest/postman/
- **Developer Forum**: https://devforum.zoom.us/

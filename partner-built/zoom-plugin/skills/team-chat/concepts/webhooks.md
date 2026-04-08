# Webhook Architecture

Complete guide to understanding and implementing Zoom Team Chat webhooks for interactive chatbots.

## Overview

Webhooks are HTTP POST requests that Zoom sends to your **Bot Endpoint URL** when specific events occur (slash commands, button clicks, form submissions, etc.).

### How It Works

```
User action in Zoom → Zoom sends webhook → Your server processes → Send response
```

**Example flow**:
```
1. User types "/weather San Francisco" in Zoom Team Chat
2. Zoom sends POST request to your Bot Endpoint URL
3. Your server receives webhook with payload.cmd = "San Francisco"
4. Your server calls weather API
5. Your server sends chatbot message back with weather data
```

## Webhook Lifecycle

### Setup (One-time)

1. **Configure Bot Endpoint URL** in Zoom Marketplace:
   - Development: `https://abc123.ngrok.io/webhook`
   - Production: `https://yourdomain.com/webhook`

2. **Verify endpoint** - Zoom sends validation request when you save the URL

### Runtime (Per Event)

```
User action → Zoom webhook → Your handler → Response
```

## Webhook Events

| Event | Trigger | When It Fires |
|-------|---------|---------------|
| `endpoint.url_validation` | URL configured/changed | Setup only |
| `bot_installed` | Bot added to account | Installation |
| `bot_notification` | User messages bot or uses slash command | User interaction |
| `interactive_message_actions` | Button clicked | User clicks button |
| `chat_message.submit` | Form submitted | User submits form |
| `app_deauthorized` | Bot removed from account | Uninstallation |

**See**: [Webhook Events Reference](../references/webhook-events.md) for complete event catalog

## Webhook Structure

### Request Headers

Every webhook includes these headers:

```javascript
{
  'x-zm-signature': 'v0=abc123...',          // Signature for verification
  'x-zm-request-timestamp': '1234567890',    // Unix timestamp
  'content-type': 'application/json'
}
```

### Request Body

```javascript
{
  "event": "bot_notification",  // Event type
  "payload": {                   // Event-specific data
    "accountId": "...",
    "toJid": "...",
    "cmd": "...",
    // ... more fields
  }
}
```

## Webhook Verification

**CRITICAL**: Always verify webhook signatures to prevent unauthorized requests.

### Why Verify?

Without verification, anyone can send fake webhooks to your endpoint, potentially:
- Triggering unauthorized actions
- Causing denial-of-service attacks
- Accessing sensitive data

### Verification Algorithm

```javascript
const crypto = require('crypto');

function verifyZoomWebhookSignature(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  const secretToken = process.env.ZOOM_VERIFICATION_TOKEN;

  if (!signature || !timestamp) {
    throw new Error('Missing signature headers');
  }

  // Construct message
  const message = `v0:${timestamp}:${JSON.stringify(req.body)}`;

  // Calculate expected signature
  const expectedSignature = crypto
    .createHmac('sha256', secretToken)
    .update(message)
    .digest('hex');

  // Compare signatures
  if (signature !== `v0=${expectedSignature}`) {
    throw new Error('Invalid webhook signature');
  }

  return true;
}
```

### Verification Flow

```
1. Extract signature and timestamp from headers
2. Construct message: "v0:{timestamp}:{JSON body}"
3. Calculate HMAC-SHA256 with secret token
4. Compare calculated signature with header signature
5. Accept if match, reject if mismatch
```

## Webhook Handler Pattern

### Basic Handler

```javascript
app.post('/webhook', (req, res) => {
  try {
    // Step 1: Verify signature
    verifyZoomWebhookSignature(req);

    // Step 2: Extract event and payload
    const { event, payload } = req.body;

    // Step 3: Handle event
    switch (event) {
      case 'endpoint.url_validation':
        return handleUrlValidation(req, res);
      
      case 'bot_installed':
        return handleBotInstalled(payload, res);
      
      case 'bot_notification':
        return handleBotNotification(payload, res);
      
      case 'interactive_message_actions':
        return handleButtonClick(payload, res);
      
      case 'app_deauthorized':
        return handleBotUninstalled(payload, res);
      
      default:
        console.log('Unsupported event:', event);
        return res.status(200).json({ success: true });
    }
  } catch (error) {
    if (error.message.includes('signature')) {
      return res.status(401).json({ error: 'Invalid webhook signature' });
    }
    return res.status(500).json({ error: error.message });
  }
});
```

## Event Handlers

### 1. URL Validation (`endpoint.url_validation`)

Zoom sends this when you configure or change your Bot Endpoint URL.

**Purpose**: Verify you control the endpoint

**Payload**:
```javascript
{
  "event": "endpoint.url_validation",
  "payload": {
    "plainToken": "xyz123abc"
  }
}
```

**Required Response**:
```javascript
{
  "plainToken": "xyz123abc",
  "encryptedToken": "hmac_sha256(plainToken, secret_token)"
}
```

**Implementation**:
```javascript
function handleUrlValidation(req, res) {
  const { plainToken } = req.body.payload;
  
  const encryptedToken = crypto
    .createHmac('sha256', process.env.ZOOM_VERIFICATION_TOKEN)
    .update(plainToken)
    .digest('hex');

  return res.status(200).json({
    plainToken,
    encryptedToken
  });
}
```

### 2. Bot Installed (`bot_installed`)

Fired when someone adds your bot to their account.

**Payload**:
```javascript
{
  "event": "bot_installed",
  "payload": {
    "accountId": "...",
    "userId": "...",
    "timestamp": 1234567890
  }
}
```

**Use Case**: Initialize bot state, send welcome message

**Implementation**:
```javascript
async function handleBotInstalled(payload, res) {
  console.log('Bot installed for account:', payload.accountId);
  
  // Optional: Initialize database, send welcome message
  // await initializeBotForAccount(payload.accountId);
  
  return res.status(200).json({ success: true });
}
```

### 3. Bot Notification (`bot_notification`)

Fired when:
- User sends message to bot via slash command
- User sends direct message to bot

**Payload**:
```javascript
{
  "event": "bot_notification",
  "payload": {
    "accountId": "...",
    "toJid": "channel@conference.xmpp.zoom.us",
    "robotJid": "bot@xmpp.zoom.us",
    "userJid": "user@xmpp.zoom.us",
    "cmd": "user's input text",
    "userName": "John Doe",
    "channelName": "Marketing",
    "timestamp": 1234567890
  }
}
```

**Key Fields**:
- `cmd` - User's input after the slash command
- `toJid` - Where to send response (channel or DM)
- `accountId` - Account identifier

**Use Case**: Process commands, integrate LLM, send responses

**Implementation**:
```javascript
async function handleBotNotification(payload, res) {
  const { toJid, cmd, accountId, userName } = payload;
  
  console.log(`${userName} sent: ${cmd}`);
  
  // Process command (e.g., call LLM)
  const response = await processCommand(cmd);
  
  // Send response
  await sendChatbotMessage(toJid, accountId, {
    body: [{ type: 'message', text: response }]
  });
  
  return res.status(200).json({ success: true });
}
```

### 4. Interactive Message Actions (`interactive_message_actions`)

Fired when user clicks a button in a chatbot message.

**Payload**:
```javascript
{
  "event": "interactive_message_actions",
  "payload": {
    "accountId": "...",
    "toJid": "...",
    "actionItem": {
      "text": "Approve",
      "value": "approve"  // This is what you check
    },
    "messageId": "...",
    "userName": "John Doe"
  }
}
```

**Key Field**: `actionItem.value` - The button's value you defined

**Implementation**:
```javascript
async function handleButtonClick(payload, res) {
  const { actionItem, toJid, accountId, userName } = payload;
  
  console.log(`${userName} clicked: ${actionItem.value}`);
  
  switch (actionItem.value) {
    case 'approve':
      await sendChatbotMessage(toJid, accountId, {
        body: [{ type: 'message', text: '✅ Approved!' }]
      });
      break;
    
    case 'reject':
      await sendChatbotMessage(toJid, accountId, {
        body: [{ type: 'message', text: '❌ Rejected' }]
      });
      break;
    
    default:
      console.log('Unknown action:', actionItem.value);
  }
  
  return res.status(200).json({ success: true });
}
```

## Webhook Best Practices

### 1. Always Verify Signatures

```javascript
// ✅ GOOD
app.post('/webhook', (req, res) => {
  verifyZoomWebhookSignature(req);
  // ... handle event
});

// ❌ BAD
app.post('/webhook', (req, res) => {
  // No verification - vulnerable to fake webhooks!
});
```

### 2. Respond Quickly

Zoom expects a 200 response within 3 seconds.

```javascript
// ✅ GOOD - Respond immediately, process async
app.post('/webhook', (req, res) => {
  verifyZoomWebhookSignature(req);
  
  // Respond immediately
  res.status(200).json({ success: true });
  
  // Process asynchronously
  processWebhookAsync(req.body);
});

// ❌ BAD - Slow processing blocks response
app.post('/webhook', async (req, res) => {
  await slowLLMCall();  // May timeout!
  res.status(200).json({ success: true });
});
```

### 3. Handle All Events Gracefully

```javascript
// ✅ GOOD - Handle unknown events
switch (event) {
  case 'bot_notification':
    return handleBotNotification(payload, res);
  default:
    console.log('Unsupported event:', event);
    return res.status(200).json({ success: true });
}

// ❌ BAD - Crash on unknown events
switch (event) {
  case 'bot_notification':
    return handleBotNotification(payload, res);
  // Missing default case - crashes on new events!
}
```

### 4. Log Webhook Activity

```javascript
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  console.log(`[Webhook] ${event}`, {
    timestamp: new Date().toISOString(),
    accountId: payload.accountId,
    userId: payload.userId
  });
  
  // ... handle event
});
```

### 5. Use Environment Variables

```javascript
// ✅ GOOD
const SECRET_TOKEN = process.env.ZOOM_VERIFICATION_TOKEN;

// ❌ BAD - Hardcoded secret
const SECRET_TOKEN = 'abc123xyz';
```

## Testing Webhooks

### Local Development with ngrok

```bash
# Install ngrok
npm install -g ngrok

# Expose local server
ngrok http 4000

# Copy HTTPS URL to Zoom Marketplace
# Example: https://abc123.ngrok.io/webhook
```

### Manual Testing

```bash
WEBHOOK_BASE_URL="http://YOUR_DEV_HOST:4000"

# Test with curl (will fail signature verification - expected)
curl -X POST "$WEBHOOK_BASE_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{"event":"test"}'

# Expected response: "Invalid webhook signature" (this is correct!)
```

### Verify Webhook is Working

**Success indicators**:
1. Zoom successfully validates your endpoint URL
2. `bot_installed` event fires when you add the bot
3. `bot_notification` fires when you use slash command
4. Button clicks trigger `interactive_message_actions`

## Common Webhook Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Cannot GET /webhook" | Browser sends GET, webhook is POST | Normal - test with POST or Zoom |
| "Invalid signature" | Wrong secret token | Verify ZOOM_VERIFICATION_TOKEN matches Zoom Marketplace |
| URL validation fails | Response format incorrect | Return plainToken + encryptedToken |
| No webhooks received | Wrong endpoint URL | Verify URL in Zoom Marketplace matches your server |
| Webhooks timeout | Slow response | Return 200 immediately, process async |

## Next Steps

- [Webhook Events Reference](../references/webhook-events.md) - Complete event catalog
- [Button Actions Example](../examples/button-actions.md) - Handle button clicks
- [Slash Commands Example](../examples/slash-commands.md) - Process slash commands
- [LLM Integration Example](../examples/llm-integration.md) - Integrate Claude/GPT

## Resources

- [Chatbot Webhook Events](https://developers.zoom.us/docs/api/chatbot/events/)
- [Webhook Verification](https://developers.zoom.us/docs/api/webhooks/#verify-webhook-events)
- [Chatbot Quickstart](https://github.com/zoom/chatbot-nodejs-quickstart)

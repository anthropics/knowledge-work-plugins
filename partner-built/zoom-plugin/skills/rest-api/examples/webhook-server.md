# Webhook Server - Express.js with CRC Validation and Signature Verification

Production-ready webhook server implementation for receiving Zoom webhook events with CRC (Challenge-Response Check) validation and HMAC signature verification.

> **For comprehensive webhook documentation**, see the **[webhooks skill](../../webhooks/SKILL.md)**.

## Quick Start

### 1. Install Dependencies

```bash
npm install express body-parser crypto
```

### 2. Basic Webhook Server

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

// Zoom webhook secret token (from your app's Feature page)
const WEBHOOK_SECRET_TOKEN = process.env.ZOOM_WEBHOOK_SECRET;

// Parse JSON bodies
app.use(express.json());

// Webhook endpoint
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;

  // Handle CRC validation (Challenge-Response Check)
  if (event === 'endpoint.url_validation') {
    return handleCRC(req, res);
  }

  // Verify signature
  if (!verifySignature(req)) {
    console.error('Invalid signature');
    return res.status(401).send('Unauthorized');
  }

  // Handle events
  handleEvent(event, payload);

  // Always respond with 200 within 3 seconds
  res.status(200).send();
});

app.listen(3000, () => {
  console.log('Webhook server running on port 3000');
});
```

## CRC (Challenge-Response Check) Validation

When you add a webhook URL or make changes, Zoom sends a validation request. You must respond within 3 seconds.

### CRC Flow

1. Zoom sends POST with `event: "endpoint.url_validation"`
2. Your server hashes the `plainToken` using your webhook secret
3. Respond with JSON containing both `plainToken` and `encryptedToken`

### Implementation

```javascript
function handleCRC(req, res) {
  const { plainToken } = req.body.payload;

  // Hash the plainToken with HMAC-SHA256
  const encryptedToken = crypto
    .createHmac('sha256', WEBHOOK_SECRET_TOKEN)
    .update(plainToken)
    .digest('hex');

  // Respond within 3 seconds
  res.status(200).json({
    plainToken,
    encryptedToken
  });

  console.log('CRC validation successful');
}
```

### CRC Request Example

```json
{
  "event": "endpoint.url_validation",
  "payload": {
    "plainToken": "qgg8vlvZRS6UYooatFL8Aw"
  },
  "event_ts": 1654503849680
}
```

### CRC Response Example

```json
{
  "plainToken": "qgg8vlvZRS6UYooatFL8Aw",
  "encryptedToken": "23a89b634c017e5364a1c8d9c8ea909b60dd5599e2bb04bb1558d9c3a121faa5"
}
```

## Signature Verification

Verify that webhook requests actually come from Zoom by checking the HMAC signature.

### Signature Verification Flow

1. Extract `x-zm-signature` and `x-zm-request-timestamp` headers
2. Construct message: `v0:{timestamp}:{body}`
3. Hash message with HMAC-SHA256 using your webhook secret
4. Prepend `v0=` to the hash
5. Compare with `x-zm-signature` header

### Implementation

```javascript
function verifySignature(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];

  if (!signature || !timestamp) {
    console.error('Missing signature headers');
    return false;
  }

  // Construct the message
  const message = `v0:${timestamp}:${JSON.stringify(req.body)}`;

  // Hash the message
  const hashForVerify = crypto
    .createHmac('sha256', WEBHOOK_SECRET_TOKEN)
    .update(message)
    .digest('hex');

  // Prepend v0=
  const computedSignature = `v0=${hashForVerify}`;

  // Compare signatures
  return signature === computedSignature;
}
```

### Signature Headers Example

```http
POST /webhook HTTP/1.1
Host: example.com
x-zm-signature: v0=a05d830fa017433bc47887f835a00b9ff33d3882f22f63a2986a8es270341
x-zm-request-timestamp: 1658940994
Content-Type: application/json

{"event":"meeting.started","payload":{...}}
```

## Event Handling

### Event Router

```javascript
function handleEvent(event, payload) {
  switch (event) {
    case 'meeting.created':
      handleMeetingCreated(payload);
      break;

    case 'meeting.started':
      handleMeetingStarted(payload);
      break;

    case 'meeting.ended':
      handleMeetingEnded(payload);
      break;

    case 'meeting.participant_joined':
      handleParticipantJoined(payload);
      break;

    case 'recording.completed':
      handleRecordingCompleted(payload);
      break;

    default:
      console.log(`Unhandled event: ${event}`);
  }
}
```

### Event Handlers

```javascript
function handleMeetingStarted(payload) {
  const { id, uuid, topic, start_time } = payload.object;
  console.log(`Meeting started: ${topic} (ID: ${id})`);
  
  // Your logic: Send notifications, start recording, etc.
  // Example: Trigger auto-recording
  // await startCloudRecording(id);
}

function handleMeetingEnded(payload) {
  const { id, uuid, topic, duration } = payload.object;
  console.log(`Meeting ended: ${topic} (Duration: ${duration}min)`);
  
  // Your logic: Process analytics, trigger workflows, etc.
}

function handleRecordingCompleted(payload) {
  const { id, uuid, topic, recording_files } = payload.object;
  console.log(`Recording ready: ${topic}`);
  
  // Download recordings (see recording-pipeline.md)
  recording_files.forEach(file => {
    console.log(`- ${file.file_type}: ${file.download_url}`);
    // downloadRecording(file.download_url, file.id);
  });
}

function handleParticipantJoined(payload) {
  const { participant } = payload.object;
  console.log(`Participant joined: ${participant.user_name}`);
  
  // Your logic: Track attendance, send welcome message, etc.
}
```

## Complete Production Server

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

const WEBHOOK_SECRET_TOKEN = process.env.ZOOM_WEBHOOK_SECRET;
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Request logging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Webhook endpoint
app.post('/webhook', async (req, res) => {
  try {
    const { event, payload, event_ts } = req.body;

    // CRC validation
    if (event === 'endpoint.url_validation') {
      return handleCRC(req, res);
    }

    // Verify signature
    if (!verifySignature(req)) {
      console.error('Signature verification failed');
      return res.status(401).send('Unauthorized');
    }

    // Log event
    console.log(`Event received: ${event} at ${new Date(event_ts)}`);

    // Handle event asynchronously
    setImmediate(() => {
      handleEvent(event, payload).catch(error => {
        console.error('Error handling event:', error);
      });
    });

    // Respond immediately (within 3 seconds)
    res.status(200).send();

  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).send('Internal Server Error');
  }
});

// CRC validation
function handleCRC(req, res) {
  const { plainToken } = req.body.payload;

  const encryptedToken = crypto
    .createHmac('sha256', WEBHOOK_SECRET_TOKEN)
    .update(plainToken)
    .digest('hex');

  res.status(200).json({ plainToken, encryptedToken });
  console.log('CRC validation successful');
}

// Signature verification
function verifySignature(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];

  if (!signature || !timestamp) {
    return false;
  }

  const message = `v0:${timestamp}:${JSON.stringify(req.body)}`;

  const hashForVerify = crypto
    .createHmac('sha256', WEBHOOK_SECRET_TOKEN)
    .update(message)
    .digest('hex');

  const computedSignature = `v0=${hashForVerify}`;

  return signature === computedSignature;
}

// Event handler
async function handleEvent(event, payload) {
  switch (event) {
    case 'meeting.started':
      await handleMeetingStarted(payload);
      break;

    case 'meeting.ended':
      await handleMeetingEnded(payload);
      break;

    case 'recording.completed':
      await handleRecordingCompleted(payload);
      break;

    // Add more event handlers as needed
    default:
      console.log(`Unhandled event: ${event}`);
  }
}

async function handleMeetingStarted(payload) {
  console.log(`Meeting started: ${payload.object.topic}`);
  // Your business logic
}

async function handleMeetingEnded(payload) {
  console.log(`Meeting ended: ${payload.object.topic}`);
  // Your business logic
}

async function handleRecordingCompleted(payload) {
  console.log(`Recording completed: ${payload.object.topic}`);
  // Download logic (see recording-pipeline.md)
}

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`Webhook server running on port ${PORT}`);
  console.log(`Webhook endpoint: ${process.env.PUBLIC_BASE_URL || 'https://YOUR_PUBLIC_BASE_URL'}/webhook`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});
```

## Webhook Retry Policy

Zoom automatically retries failed webhooks **3 times** with exponential backoff:

1. **First retry**: 5 minutes after initial failure
2. **Second retry**: 20 minutes after first retry
3. **Third retry**: 60 minutes after second retry

### Retry Conditions

Zoom retries for:
- HTTP status codes ≥ 500
- Network errors (connection refused, timeout, etc.)

Zoom does **NOT** retry for:
- HTTP status codes 200-299 (success)
- HTTP status codes 300-399 (redirects)
- HTTP status codes 400-499 (client errors)

### Handling Retries

```javascript
// Track processed events to avoid duplicate processing
const processedEvents = new Set();

app.post('/webhook', (req, res) => {
  const { event, event_ts, payload } = req.body;

  // Create unique event ID
  const eventId = `${event}-${event_ts}-${payload.object?.id || ''}`;

  // Check if already processed (duplicate due to retry)
  if (processedEvents.has(eventId)) {
    console.log(`Duplicate event: ${eventId}`);
    return res.status(200).send();  // Still return 200
  }

  // Mark as processed
  processedEvents.add(eventId);

  // Handle event
  handleEvent(event, payload);

  res.status(200).send();

  // Clean up old entries after 2 hours
  setTimeout(() => processedEvents.delete(eventId), 2 * 60 * 60 * 1000);
});
```

## Webhook Revalidation

Zoom automatically revalidates webhook endpoints every **72 hours**. If revalidation fails 6 consecutive times, Zoom disables the webhook.

### Revalidation Notifications

- **2 failures**: First email notification
- **4 failures**: Second email notification
- **6 failures**: Webhook disabled

### Ensure Uptime

```javascript
// Health check with monitoring
app.get('/health', (req, res) => {
  // Check dependencies (database, external APIs, etc.)
  const isHealthy = checkDependencies();

  if (isHealthy) {
    res.status(200).json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime()
    });
  } else {
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString()
    });
  }
});

function checkDependencies() {
  // Check database connection, external APIs, etc.
  return true;
}
```

## Environment Variables

```bash
# .env
ZOOM_WEBHOOK_SECRET=your_webhook_secret_token_here
PORT=3000
NODE_ENV=production
```

### Loading Environment Variables

```javascript
require('dotenv').config();

const WEBHOOK_SECRET_TOKEN = process.env.ZOOM_WEBHOOK_SECRET;

if (!WEBHOOK_SECRET_TOKEN) {
  throw new Error('ZOOM_WEBHOOK_SECRET environment variable is required');
}
```

## Deployment

### Requirements

1. **HTTPS required** - Zoom only sends to HTTPS endpoints
2. **Public URL** - Endpoint must be publicly accessible
3. **TLS 1.2+** - Valid certificate from a Certificate Authority (CA)
4. **FQDN** - Fully qualified domain name (not IP address)
5. **Response time** - Respond within 3 seconds

### Deployment Options

- **Heroku**: `git push heroku main`
- **AWS Lambda**: Use API Gateway + Lambda function
- **Vercel/Netlify**: Serverless functions
- **Self-hosted**: Nginx + Node.js + Let's Encrypt

### ngrok for Local Development

```bash
# Install ngrok
npm install -g ngrok

# Start your server
node server.js

# In another terminal, expose to public URL
ngrok http 3000

# Use the HTTPS URL in Zoom webhook configuration
# Example: https://abc123.ngrok.io/webhook
```

## Testing

### Test CRC Validation

```bash
WEBHOOK_BASE_URL="http://YOUR_DEV_HOST:3000"

curl -X POST "$WEBHOOK_BASE_URL/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "endpoint.url_validation",
    "payload": {
      "plainToken": "test_token_123"
    },
    "event_ts": 1654503849680
  }'
```

Expected response:
```json
{
  "plainToken": "test_token_123",
  "encryptedToken": "..."
}
```

### Test Event Handling

```bash
# Generate valid signature
TIMESTAMP=$(date +%s)
MESSAGE="v0:${TIMESTAMP}:{\"event\":\"meeting.started\",\"payload\":{\"object\":{\"id\":\"123\",\"topic\":\"Test\"}}}"
SIGNATURE="v0=$(echo -n "$MESSAGE" | openssl dgst -sha256 -hmac "YOUR_SECRET" -binary | xxd -p)"

WEBHOOK_BASE_URL="http://YOUR_DEV_HOST:3000"

curl -X POST "$WEBHOOK_BASE_URL/webhook" \
  -H "Content-Type: application/json" \
  -H "x-zm-signature: $SIGNATURE" \
  -H "x-zm-request-timestamp: $TIMESTAMP" \
  -d '{"event":"meeting.started","payload":{"object":{"id":"123","topic":"Test Meeting"}}}'
```

## Common Event Types

| Event | Description |
|-------|-------------|
| `meeting.created` | Meeting created |
| `meeting.updated` | Meeting details changed |
| `meeting.deleted` | Meeting deleted |
| `meeting.started` | Meeting begins |
| `meeting.ended` | Meeting ends |
| `meeting.participant_joined` | Participant joins |
| `meeting.participant_left` | Participant leaves |
| `recording.completed` | Cloud recording ready |
| `recording.transcript_completed` | Transcript ready |
| `user.created` | User created |
| `user.updated` | User updated |
| `user.deleted` | User deleted |

> **See complete event catalog**: [webhooks skill](../../webhooks/SKILL.md)

## Related Documentation

- **[webhooks skill](../../webhooks/SKILL.md)** - Comprehensive webhook documentation
- **[Recording Pipeline](recording-pipeline.md)** - Download recordings from webhook events
- **[Meeting Lifecycle](meeting-lifecycle.md)** - Create/update/delete meetings
- **[Common Issues](../troubleshooting/common-issues.md)** - Webhook troubleshooting

## Resources

- [Using Webhooks](https://developers.zoom.us/docs/api/webhooks/)
- [Webhook Sample App](https://github.com/zoom/webhook-sample-node.js)
- [Event Reference](https://developers.zoom.us/docs/api/rest/webhook-reference/)

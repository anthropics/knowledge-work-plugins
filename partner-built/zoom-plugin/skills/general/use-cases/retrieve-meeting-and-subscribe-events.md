# Retrieve Meeting Details and Subscribe to Events

Comprehensive guide showing all ways to retrieve meeting details and subscribe to events in Zoom. The term "subscribe to events" has multiple meanings in Zoom, each requiring different skill combinations.

## Overview

When someone says "retrieve meeting details and subscribe to events," they could mean:

| Pattern | Event Type | Skills | When to Use |
|---------|------------|--------|-------------|
| **Pattern 1** | Server-side webhooks (HTTP) | zoom-rest-api → webhooks | Account-level event monitoring, backend processing |
| **Pattern 2** | Server-side WebSockets (WS) | zoom-rest-api → zoom-websockets | Low-latency events, no exposed endpoint |
| **Pattern 3** | Client-side SDK events | zoom-rest-api → zoom-meeting-sdk | In-meeting participant events, real-time UI updates |
| **Pattern 4** | Real-time media events | zoom-rest-api → rtms | Bot-based transcription, recording, AI analysis |
| **Pattern 5** | Reports API (polling) | zoom-rest-api only | Historical data, batch processing |

## Critical Distinction: Event Subscription Scope

**Important**: Most Zoom event subscriptions are **account-level**, not meeting-specific:

| Subscription Type | Scope | Filtering |
|-------------------|-------|-----------|
| **Webhooks** | Account-level | Filter events by meeting ID in handler |
| **WebSockets** | Account-level | Filter events by meeting ID in handler |
| **Meeting SDK** | Meeting-specific | Only events for joined meeting |
| **RTMS** | Meeting-specific | Only events/media for specific meeting |
| **Reports API** | Account-level | Query by meeting ID |

**You cannot dynamically subscribe to webhooks/WebSockets for a single meeting**. These are configured at app creation time in the Marketplace portal and receive events for ALL meetings in the account. Your code filters events by meeting ID.

---

## Pattern 1: REST API + Webhooks (Server-Side HTTP Events)

**When to use:**
- Backend processing of meeting lifecycle events
- Attendance tracking, post-meeting workflows
- Recording download automation
- Standard event-driven architectures

**Skills needed:** `zoom-rest-api` → `webhooks`

### Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│ SETUP PHASE (One-time in Marketplace Portal):                  │
│                                                                 │
│ 1. Configure Event Subscriptions                               │
│    └── Subscribe to: meeting.started, meeting.ended, etc.      │
│    └── Provide webhook endpoint URL                            │
│    └── Get webhook secret token                                │
└────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│ RUNTIME PHASE:                                                  │
│                                                                 │
│ Step 1: GET /meetings/{meetingId} (zoom-rest-api)              │
│         └── Get meeting details (topic, join_url, host, etc.)  │
│                                                                 │
│ Step 2: Store meeting ID for filtering                         │
│         └── Your backend remembers which meetings to track     │
│                                                                 │
│ Step 3: POST /webhooks/zoom (webhooks)               │
│         └── Zoom sends events for ALL meetings                 │
│         └── Filter by meeting ID in your handler               │
│         └── Process: started, ended, participant events        │
└────────────────────────────────────────────────────────────────┘
```

### Complete Implementation

```javascript
const express = require('express');
const axios = require('axios');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// Track which meetings we care about (use Redis/DB in production)
const trackedMeetings = new Set();

// ============================================
// STEP 1: Retrieve Meeting Details (zoom-rest-api)
// ============================================

async function getAccessToken() {
  const credentials = Buffer.from(
    `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
  ).toString('base64');
  
  const response = await axios.post(
    `https://zoom.us/oauth/token?grant_type=account_credentials&account_id=${process.env.ZOOM_ACCOUNT_ID}`,
    null,
    { headers: { 'Authorization': `Basic ${credentials}` } }
  );
  
  return response.data.access_token;
}

async function getMeetingDetails(meetingId) {
  const token = await getAccessToken();
  
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return response.data;
}

// API: Fetch meeting and start tracking it
app.get('/api/meetings/:meetingId', async (req, res) => {
  try {
    const { meetingId } = req.params;
    
    // Get meeting details
    const meeting = await getMeetingDetails(meetingId);
    
    // Add to tracked set (events for this meeting will be processed)
    trackedMeetings.add(String(meeting.id));
    
    console.log(`✅ Now tracking meeting: ${meeting.topic} (${meeting.id})`);
    
    res.json({
      success: true,
      meeting: {
        id: meeting.id,
        topic: meeting.topic,
        start_time: meeting.start_time,
        join_url: meeting.join_url
      },
      message: 'Meeting tracked. Webhook events will be processed for this meeting.'
    });
  } catch (error) {
    res.status(error.response?.status || 500).json({
      success: false,
      error: error.message
    });
  }
});

// ============================================
// STEP 2: Handle Webhook Events (webhooks)
// ============================================

function verifyWebhookSignature(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  const payload = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  
  const expectedSignature = `v0=${crypto
    .createHmac('sha256', process.env.ZOOM_WEBHOOK_SECRET)
    .update(payload)
    .digest('hex')}`;
  
  return signature === expectedSignature;
}

app.post('/webhooks/zoom', async (req, res) => {
  // Handle URL validation challenge
  if (req.body.event === 'endpoint.url_validation') {
    const hash = crypto
      .createHmac('sha256', process.env.ZOOM_WEBHOOK_SECRET)
      .update(req.body.payload.plainToken)
      .digest('hex');
    
    return res.json({
      plainToken: req.body.payload.plainToken,
      encryptedToken: hash
    });
  }
  
  // Verify signature
  if (!verifyWebhookSignature(req)) {
    console.error('❌ Invalid webhook signature');
    return res.status(401).send('Invalid signature');
  }
  
  const { event, payload } = req.body;
  const meetingId = String(payload.object.id);
  
  // CRITICAL: Filter events - only process tracked meetings
  if (!trackedMeetings.has(meetingId)) {
    console.log(`⏭️  Ignoring event for untracked meeting ${meetingId}`);
    return res.status(200).send();
  }
  
  // Process events for tracked meetings
  console.log(`📩 Event: ${event} for meeting ${meetingId}`);
  
  switch (event) {
    case 'meeting.started':
      console.log(`✅ Meeting started: ${payload.object.topic}`);
      // Handle meeting start
      break;
      
    case 'meeting.ended':
      console.log(`🏁 Meeting ended: ${payload.object.topic}`);
      // Handle meeting end, cleanup
      trackedMeetings.delete(meetingId);
      break;
      
    case 'meeting.participant_joined':
      console.log(`👋 ${payload.object.participant.user_name} joined`);
      // Track attendance
      break;
      
    case 'meeting.participant_left':
      console.log(`👋 ${payload.object.participant.user_name} left`);
      // Update attendance
      break;
  }
  
  res.status(200).send();
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
  console.log('');
  console.log('Endpoints:');
  console.log('  GET  /api/meetings/:id  - Fetch & track meeting');
  console.log('  POST /webhooks/zoom     - Webhook receiver');
});
```

**See also**: [meeting-details-with-events.md](meeting-details-with-events.md) for expanded webhook implementation.

---

## Pattern 2: REST API + WebSockets (Server-Side Low-Latency Events)

**When to use:**
- Lower latency than webhooks required
- Security-sensitive industries (no exposed endpoint)
- Bidirectional communication needed
- Real-time dashboards, live monitoring

**Skills needed:** `zoom-rest-api` → `zoom-websockets`

### Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│ SETUP PHASE (One-time in Marketplace Portal):                  │
│                                                                 │
│ 1. Create Server-to-Server OAuth app                           │
│ 2. Configure WebSocket Event Subscription                      │
│    └── Subscribe to: meeting.started, meeting.ended, etc.      │
│    └── Get subscription ID                                     │
└────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│ RUNTIME PHASE:                                                  │
│                                                                 │
│ Step 1: GET /meetings/{meetingId} (zoom-rest-api)              │
│         └── Get meeting details                                │
│                                                                 │
│ Step 2: Connect to WebSocket (zoom-websockets)                 │
│         └── wss://ws.zoom.us/ws?subscriptionId=...             │
│         └── Authenticate with S2S OAuth access token           │
│                                                                 │
│ Step 3: Receive events via WebSocket                           │
│         └── Filter by meeting ID in message handler            │
│         └── Lower latency than webhooks                        │
└────────────────────────────────────────────────────────────────┘
```

### Complete Implementation

```javascript
const axios = require('axios');
const WebSocket = require('ws');

// Track which meetings we care about
const trackedMeetings = new Set();
let ws = null;

// ============================================
// STEP 1: Retrieve Meeting Details (zoom-rest-api)
// ============================================

async function getAccessToken() {
  const credentials = Buffer.from(
    `${process.env.ZOOM_CLIENT_ID}:${process.env.ZOOM_CLIENT_SECRET}`
  ).toString('base64');
  
  const response = await axios.post(
    'https://zoom.us/oauth/token',
    new URLSearchParams({
      grant_type: 'account_credentials',
      account_id: process.env.ZOOM_ACCOUNT_ID
    }),
    {
      headers: {
        'Authorization': `Basic ${credentials}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
  );
  
  return response.data.access_token;
}

async function getMeetingDetails(meetingId) {
  const token = await getAccessToken();
  
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return response.data;
}

// ============================================
// STEP 2: Connect to WebSocket (zoom-websockets)
// ============================================

async function connectWebSocket() {
  const accessToken = await getAccessToken();
  const subscriptionId = process.env.ZOOM_WEBSOCKET_SUBSCRIPTION_ID;
  
  const wsUrl = `wss://ws.zoom.us/ws?subscriptionId=${subscriptionId}&access_token=${accessToken}`;
  
  ws = new WebSocket(wsUrl);
  
  ws.on('open', () => {
    console.log('✅ WebSocket connection established');
  });
  
  ws.on('message', (data) => {
    const event = JSON.parse(data);
    handleWebSocketEvent(event);
  });
  
  ws.on('close', () => {
    console.log('❌ WebSocket connection closed. Reconnecting...');
    setTimeout(connectWebSocket, 5000);
  });
  
  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });
}

// ============================================
// STEP 3: Handle WebSocket Events
// ============================================

function handleWebSocketEvent(event) {
  const { event: eventType, payload } = event;
  const meetingId = String(payload?.object?.id);
  
  // CRITICAL: Filter events - only process tracked meetings
  if (!meetingId || !trackedMeetings.has(meetingId)) {
    return;
  }
  
  console.log(`📩 WebSocket Event: ${eventType} for meeting ${meetingId}`);
  
  switch (eventType) {
    case 'meeting.started':
      console.log(`✅ Meeting started: ${payload.object.topic}`);
      break;
      
    case 'meeting.ended':
      console.log(`🏁 Meeting ended: ${payload.object.topic}`);
      trackedMeetings.delete(meetingId);
      break;
      
    case 'meeting.participant_joined':
      console.log(`👋 ${payload.object.participant.user_name} joined`);
      break;
      
    case 'meeting.participant_left':
      console.log(`👋 ${payload.object.participant.user_name} left`);
      break;
  }
}

// ============================================
// USAGE: Track Meeting and Receive Events
// ============================================

async function trackMeeting(meetingId) {
  // Get meeting details
  const meeting = await getMeetingDetails(meetingId);
  
  // Add to tracked set
  trackedMeetings.add(String(meeting.id));
  
  console.log(`✅ Now tracking meeting: ${meeting.topic} (${meeting.id})`);
  console.log(`   Events will arrive via WebSocket connection`);
  
  return meeting;
}

// Initialize WebSocket connection
connectWebSocket();

// Track specific meetings
trackMeeting('123456789').catch(console.error);
trackMeeting('987654321').catch(console.error);
```

**Comparison with Webhooks:**

| Aspect | WebSockets | Webhooks |
|--------|------------|----------|
| **Latency** | Lower (persistent connection) | Higher (new HTTP request per event) |
| **Setup** | More complex (S2S OAuth required) | Simpler (just endpoint URL) |
| **Security** | No exposed endpoint | Requires public endpoint + signature verification |
| **Best for** | Real-time dashboards, high-frequency events | Standard backend processing |

---

## Pattern 3: REST API + Meeting SDK Events (Client-Side In-Meeting)

**When to use:**
- Building custom meeting UI with real-time updates
- In-meeting participant tracking
- User joins meeting from your web app
- Real-time UI state updates (active speaker, video on/off, etc.)

**Skills needed:** `zoom-rest-api` → `zoom-meeting-sdk`

### Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│ RUNTIME PHASE (User-initiated):                                │
│                                                                 │
│ Step 1: GET /meetings/{meetingId} (zoom-rest-api)              │
│         └── Get meeting number, password                       │
│         └── Generate SDK signature (JWT)                       │
│                                                                 │
│ Step 2: ZoomMtg.init() + join() (zoom-meeting-sdk)             │
│         └── User joins meeting in browser                      │
│         └── Receive ZoomMtg instance for event listeners       │
│                                                                 │
│ Step 3: ZoomMtg.inMeetingServiceListener() (zoom-meeting-sdk)  │
│         └── Listen to: onUserJoin, onUserLeave, etc.           │
│         └── Events ONLY for this specific meeting              │
│         └── Real-time UI updates                               │
└────────────────────────────────────────────────────────────────┘
```

### Complete Implementation

**Backend: Generate Signature**

```javascript
const KJUR = require('jsrsasign');

// Step 1: Get meeting details
async function getMeetingDetails(meetingId) {
  const token = await getAccessToken();
  
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return {
    id: response.data.id,
    password: response.data.password,
    topic: response.data.topic,
    join_url: response.data.join_url
  };
}

// Generate Meeting SDK signature
function generateSignature(meetingNumber, role) {
  const iat = Math.floor(Date.now() / 1000) - 30;
  const exp = iat + 60 * 60 * 2; // 2 hours
  
  const header = { alg: 'HS256', typ: 'JWT' };
  const payload = {
    sdkKey: process.env.ZOOM_SDK_KEY,
    mn: String(meetingNumber).replace(/\D/g, ''),
    role: parseInt(role, 10), // 0 = participant, 1 = host
    iat,
    exp,
    tokenExp: exp
  };
  
  return KJUR.jws.JWS.sign(
    'HS256',
    JSON.stringify(header),
    JSON.stringify(payload),
    process.env.ZOOM_SDK_SECRET
  );
}

// API endpoint: Get meeting details + signature
app.get('/api/meetings/:meetingId/join', async (req, res) => {
  try {
    const { meetingId } = req.params;
    const { role = 0 } = req.query;
    
    // Get meeting details from Zoom API
    const meeting = await getMeetingDetails(meetingId);
    
    // Generate signature for SDK
    const signature = generateSignature(meeting.id, role);
    
    res.json({
      meetingNumber: meeting.id,
      password: meeting.password,
      signature: signature,
      sdkKey: process.env.ZOOM_SDK_KEY,
      topic: meeting.topic
    });
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: error.message
    });
  }
});
```

**Frontend: Join Meeting and Listen to Events**

```javascript
import { ZoomMtg } from '@zoom/meetingsdk';

// Step 1: Get meeting details + signature from backend
async function getMeetingCredentials(meetingId) {
  const response = await fetch(`/api/meetings/${meetingId}/join`);
  return response.json();
}

// Step 2: Initialize Meeting SDK
async function joinMeeting(meetingId, userName) {
  try {
    // Get meeting details from backend (includes REST API call)
    const credentials = await getMeetingCredentials(meetingId);
    
    // Preload SDK
    ZoomMtg.preLoadWasm();
    ZoomMtg.prepareWebSDK();
    
    // Initialize SDK
    ZoomMtg.init({
      leaveUrl: window.location.origin,
      patchJsMedia: true,
      leaveOnPageUnload: true,
      success: () => {
        // Join meeting
        ZoomMtg.join({
          signature: credentials.signature,
          sdkKey: credentials.sdkKey,
          meetingNumber: credentials.meetingNumber,
          passWord: credentials.password,
          userName: userName,
          success: () => {
            console.log('✅ Joined meeting:', credentials.topic);
            
            // Step 3: Subscribe to in-meeting events
            subscribeToMeetingEvents();
          },
          error: (err) => {
            console.error('Join error:', err);
          }
        });
      },
      error: (err) => {
        console.error('Init error:', err);
      }
    });
  } catch (error) {
    console.error('Failed to join meeting:', error);
  }
}

// Step 3: Listen to Meeting SDK events
function subscribeToMeetingEvents() {
  // User join events
  ZoomMtg.inMeetingServiceListener('onUserJoin', (data) => {
    console.log('👋 User joined:', data);
    // data.userId, data.userName
    // Update UI: add participant to list
  });
  
  // User leave events
  ZoomMtg.inMeetingServiceListener('onUserLeave', (data) => {
    console.log('👋 User left:', data);
    // Update UI: remove participant from list
  });
  
  // Active speaker detection
  ZoomMtg.inMeetingServiceListener('onActiveSpeaker', (data) => {
    console.log('🎤 Active speaker:', data);
    // data: [{ userId, userName }]
    // Update UI: highlight speaker
  });
  
  // Meeting status changes
  ZoomMtg.inMeetingServiceListener('onMeetingStatus', (data) => {
    console.log('📊 Meeting status:', data);
    // status: 1=connecting, 2=connected, 3=disconnected, 4=reconnecting
  });
  
  // Chat messages
  ZoomMtg.inMeetingServiceListener('onReceiveChatMsg', (data) => {
    console.log('💬 Chat message:', data);
    // Display in custom UI
  });
  
  // Recording status
  ZoomMtg.inMeetingServiceListener('onRecordingChange', (data) => {
    console.log('🔴 Recording status:', data);
    // Show recording indicator
  });
  
  // User updates (audio/video state changes)
  ZoomMtg.inMeetingServiceListener('onUserUpdate', (data) => {
    console.log('🔄 User updated:', data);
    // Update UI: show muted/video off indicators
  });
}

// Usage
joinMeeting('123456789', 'John Doe');
```

**Key Differences from Webhooks/WebSockets:**

| Aspect | Meeting SDK Events | Webhooks/WebSockets |
|--------|-------------------|---------------------|
| **Scope** | Meeting-specific (only joined meeting) | Account-level (all meetings) |
| **Location** | Client-side (browser) | Server-side |
| **Authentication** | SDK signature (JWT) | OAuth access token |
| **Use case** | In-meeting UI updates | Backend processing |
| **Event types** | Participant, audio/video, chat, recording | Meeting lifecycle, participants |

---

## Pattern 4: REST API + RTMS (Bot-Based Real-Time Media + Events)

**When to use:**
- AI transcription, translation, sentiment analysis
- Meeting recording bots
- Real-time media processing (audio/video streams)
- Compliance monitoring

**Skills needed:** `zoom-rest-api` → `rtms`

### Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│ SETUP PHASE:                                                    │
│                                                                 │
│ 1. Configure webhook subscription for meeting.rtms_started     │
│ 2. Deploy bot infrastructure                                   │
└────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│ RUNTIME PHASE:                                                  │
│                                                                 │
│ Step 1: GET /meetings/{meetingId} (zoom-rest-api)              │
│         └── Get meeting details                                │
│                                                                 │
│ Step 2: Wait for meeting.rtms_started webhook                  │
│         └── Contains rtmsSessionID, meetingUUID                │
│                                                                 │
│ Step 3: Connect to RTMS WebSocket (rtms)                  │
│         └── wss://rtms.zoom.us/ws                              │
│         └── Subscribe to: audio, video, transcript, chat       │
│                                                                 │
│ Step 4: Receive real-time media + events                       │
│         └── Audio chunks, video frames, transcripts            │
│         └── Events: participant joined/left, speaking status   │
└────────────────────────────────────────────────────────────────┘
```

### Complete Implementation

**See comprehensive implementation:** [rtms/examples/rtms-bot.md](../../rtms/examples/rtms-bot.md)

**Quick Overview:**

```javascript
const axios = require('axios');
const WebSocket = require('ws');

// Step 1: Get meeting details
async function getMeetingDetails(meetingId) {
  const token = await getAccessToken();
  
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return response.data;
}

// Step 2: Wait for meeting.rtms_started webhook
app.post('/webhooks/zoom', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'meeting.rtms_started') {
    const { rtmsSessionID, meetingUUID } = payload.object;
    
    // Step 3: Connect to RTMS
    connectToRTMS(rtmsSessionID, meetingUUID);
  }
  
  res.status(200).send();
});

// Step 3: Connect to RTMS WebSocket
async function connectToRTMS(sessionID, meetingUUID) {
  const token = await getAccessToken();
  
  const ws = new WebSocket('wss://rtms.zoom.us/ws', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'X-Zoom-Session-ID': sessionID
    }
  });
  
  ws.on('open', () => {
    // Subscribe to media types
    ws.send(JSON.stringify({
      type: 'subscribe',
      mediaTypes: ['audio', 'transcript', 'chat']
    }));
  });
  
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    
    // Step 4: Handle real-time media and events
    switch (message.type) {
      case 'audio':
        processAudioChunk(message.data);
        break;
        
      case 'transcript':
        console.log(`📝 Transcript: ${message.data.text}`);
        break;
        
      case 'chat':
        console.log(`💬 Chat: ${message.data.message}`);
        break;
        
      case 'participant_joined':
        console.log(`👋 ${message.data.user_name} joined`);
        break;
        
      case 'participant_left':
        console.log(`👋 ${message.data.user_name} left`);
        break;
    }
  });
}

function processAudioChunk(audioData) {
  // Process raw audio for transcription, analysis, etc.
}
```

**RTMS Events (Different from Webhooks):**

| Event Type | Source | Data |
|------------|--------|------|
| `participant_joined` | RTMS WebSocket | Real-time when user joins |
| `participant_left` | RTMS WebSocket | Real-time when user leaves |
| `active_speaker_change` | RTMS WebSocket | Current speaker info |
| `audio` | RTMS WebSocket | Raw audio stream (PCM) |
| `video` | RTMS WebSocket | Raw video frames |
| `transcript` | RTMS WebSocket | Live transcription |

---

## Pattern 5: REST API + Reports (Historical Data, Not Real Events)

**When to use:**
- Historical analysis, batch processing
- Audit logs, compliance reports
- No real-time requirements
- Backup/recovery systems

**Skills needed:** `zoom-rest-api` only

### Implementation

```javascript
// Get meeting details
async function getMeetingDetails(meetingId) {
  const token = await getAccessToken();
  
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return response.data;
}

// Poll for meeting participants report (after meeting ends)
async function getMeetingParticipantsReport(meetingId) {
  const token = await getAccessToken();
  
  // Get past meeting details
  const response = await axios.get(
    `https://api.zoom.us/v2/past_meetings/${meetingId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return response.data;
}

// Get detailed participant report
async function getParticipantsList(meetingId) {
  const token = await getAccessToken();
  
  const response = await axios.get(
    `https://api.zoom.us/v2/report/meetings/${meetingId}/participants`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return response.data.participants;
}

// Usage: Retrieve meeting + get historical data
async function analyzeMeeting(meetingId) {
  // Get meeting metadata
  const meeting = await getMeetingDetails(meetingId);
  console.log(`Meeting: ${meeting.topic}`);
  
  // Wait for meeting to end, then get reports
  // (typically poll or wait for meeting.ended webhook)
  
  const participants = await getParticipantsList(meetingId);
  console.log(`Total participants: ${participants.length}`);
  
  participants.forEach(p => {
    console.log(`- ${p.name}: ${p.duration} minutes`);
  });
}
```

**Not Real-Time Events:**
- Reports API only provides historical data after meeting ends
- Not suitable for real-time monitoring
- No WebSocket/webhook integration
- Use for: auditing, analytics, compliance

---

## Comparison: When to Use Each Pattern

| Pattern | Latency | Scope | Setup Complexity | Best For |
|---------|---------|-------|------------------|----------|
| **Webhooks** | Medium | Account-level | Low | Standard backend processing |
| **WebSockets** | Low | Account-level | Medium | Real-time dashboards, no exposed endpoint |
| **Meeting SDK** | Very Low | Meeting-specific | Low | In-meeting UI, participant views |
| **RTMS** | Very Low | Meeting-specific | High | AI transcription, recording bots |
| **Reports API** | N/A (historical) | Account-level | Low | Batch processing, analytics |

---

## Skill Chaining Summary

| Scenario | Skills Chain | Order |
|----------|--------------|-------|
| Backend event processing | `zoom-rest-api` → `webhooks` | 1. Get meeting, 2. Filter webhook events |
| Low-latency monitoring | `zoom-rest-api` → `zoom-websockets` | 1. Get meeting, 2. Filter WebSocket events |
| Custom meeting UI | `zoom-rest-api` → `zoom-meeting-sdk` | 1. Get details, 2. Join meeting, 3. Listen to SDK events |
| AI transcription bot | `zoom-rest-api` → `rtms` | 1. Get meeting, 2. Wait for webhook, 3. Connect to RTMS |
| Historical analysis | `zoom-rest-api` only | 1. Get meeting, 2. Poll reports after meeting ends |

---

## Authorization Requirements

**All patterns require different OAuth scopes:**

| Pattern | Required Scopes |
|---------|----------------|
| REST API | `meeting:read:admin` or `meeting:read` |
| Webhooks | Event subscription in app config |
| WebSockets | Server-to-Server OAuth + event subscription |
| Meeting SDK | SDK Key/Secret + signature generation |
| RTMS | `meeting:read:admin` + RTMS-enabled account |

**See also**: [Authorization Patterns](../references/authorization-patterns.md) for complete scope validation strategies.

---

## Common Pitfalls

### ❌ Misconception: "Subscribe to Events for a Specific Meeting"

**Reality**: Most Zoom event systems are **account-level**, not meeting-specific.

| What You Think | What Actually Happens |
|----------------|----------------------|
| "Subscribe to events for meeting 123456789" | You receive events for ALL meetings in the account |
| "Dynamically enable webhooks when meeting starts" | Webhooks are configured at app creation time |
| "Create a webhook subscription per meeting" | One subscription receives events for all meetings |

**Solution**: Filter events by meeting ID in your handler code.

### ❌ Misconception: "All Events Are the Same"

**Reality**: Different event systems provide different event types:

| Event System | Events |
|--------------|--------|
| **Webhooks** | Meeting lifecycle: started, ended, participant_joined/left, recording_completed |
| **WebSockets** | Same as webhooks, but lower latency |
| **Meeting SDK** | In-meeting: onUserJoin, onActiveSpeaker, onUserUpdate, onReceiveChatMsg |
| **RTMS** | Real-time media: participant events + audio/video streams + transcripts |

**Solution**: Choose the right event system for your use case (see comparison table above).

---

## Related Use Cases

- **[Meeting Details with Events](meeting-details-with-events.md)** - Expanded webhook implementation
- **[Meeting Bots](meeting-bots.md)** - Building RTMS bots for transcription
- **[Recording & Transcription](recording-transcription.md)** - Download recordings after meeting ends

---

## Resources

- **REST API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Meetings
- **Webhooks**: https://developers.zoom.us/docs/api/rest/webhook-reference/
- **WebSockets**: https://developers.zoom.us/docs/api/websockets/
- **Meeting SDK**: https://developers.zoom.us/docs/meeting-sdk/web/
- **RTMS**: https://developers.zoom.us/docs/rtms/

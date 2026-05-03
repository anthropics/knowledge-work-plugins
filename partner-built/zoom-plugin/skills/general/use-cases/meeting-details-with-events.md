# Meeting Details with Event Subscription

Retrieve meeting details and subscribe to real-time meeting events.

## Overview

A common integration pattern: get meeting information via REST API, then receive real-time updates via webhooks when meeting events occur (started, ended, participants join/leave).

For implementation-heavy orchestration patterns (token refresh locks, retries, queue-based webhook handling, circuit-breaker and reconciliation fallbacks), see:
- [../references/automatic-skill-chaining-rest-webhooks.md](../references/automatic-skill-chaining-rest-webhooks.md)
- [../references/meeting-webhooks-oauth-refresh-orchestration.md](../references/meeting-webhooks-oauth-refresh-orchestration.md)
- [../references/distributed-meeting-fallback-architecture.md](../references/distributed-meeting-fallback-architecture.md)

## Skills Needed

| Order | Skill | Purpose |
|-------|-------|---------|
| 1 | **zoom-rest-api** | Retrieve meeting details |
| 2 | **webhooks** | Subscribe to and receive meeting events |

## Skill Chaining Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE INTEGRATION FLOW                         │
└─────────────────────────────────────────────────────────────────────────┘

SETUP PHASE (One-time):
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Configure Event Subscriptions (Marketplace Portal or API)            │
│    └── Subscribe to: meeting.started, meeting.ended,                    │
│        meeting.participant_joined, meeting.participant_left             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
RUNTIME PHASE:
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. GET Meeting Details (zoom-rest-api)                                  │
│    └── GET /meetings/{meetingId}                                        │
│    └── Store meeting info (topic, host, settings, join_url)             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. Receive Meeting Events (webhooks)                               │
│    └── meeting.started → Update status, notify users                    │
│    └── meeting.participant_joined → Track attendance                    │
│    └── meeting.participant_left → Log departure time                    │
│    └── meeting.ended → Finalize records, trigger post-processing        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Zoom app with OAuth or Server-to-Server OAuth
- Scopes: `meeting:read` (for REST API)
- Event subscriptions configured for meeting events
- HTTPS endpoint for receiving webhooks
- **See [Authorization Patterns](../references/authorization-patterns.md)** for scope validation and permission checking

## Step 1: Configure Event Subscriptions

### Option A: Via Marketplace Portal (Recommended for most apps)

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us/) → Your App
2. Navigate to **Feature** → **Event Subscriptions**
3. Click **Add Event Subscription**
4. Configure:
   - **Subscription name**: "Meeting Events"
   - **Event notification endpoint URL**: `https://yourapp.com/webhooks/zoom`
5. Select events:
   - ✅ `meeting.started`
   - ✅ `meeting.ended`
   - ✅ `meeting.participant_joined`
   - ✅ `meeting.participant_left`
6. Save and activate

### Option B: Programmatic Setup

Event subscriptions are configured at app creation time in the Marketplace portal. However, you can verify your subscription status via API:

```javascript
// List webhook subscriptions for your app
const response = await fetch(
  'https://api.zoom.us/v2/webhooks',
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const webhooks = await response.json();
console.log('Active webhooks:', webhooks);
```

## Step 2: Retrieve Meeting Details (zoom-rest-api)

```javascript
const axios = require('axios');

/**
 * Get meeting details from Zoom REST API
 * @param {string} meetingId - The meeting ID
 * @param {string} accessToken - Valid OAuth access token
 * @returns {Promise<Object>} Meeting details
 */
async function getMeetingDetails(meetingId, accessToken) {
  try {
    const response = await axios.get(
      `https://api.zoom.us/v2/meetings/${meetingId}`,
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );
    
    const meeting = response.data;
    
    return {
      id: meeting.id,
      uuid: meeting.uuid,
      topic: meeting.topic,
      type: meeting.type,
      status: meeting.status,
      start_time: meeting.start_time,
      duration: meeting.duration,
      timezone: meeting.timezone,
      host_id: meeting.host_id,
      host_email: meeting.host_email,
      join_url: meeting.join_url,
      password: meeting.password,
      settings: meeting.settings
    };
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error(`Meeting ${meetingId} not found`);
    }
    if (error.response?.status === 401) {
      throw new Error('Invalid or expired access token');
    }
    throw error;
  }
}

// Usage
const meeting = await getMeetingDetails('123456789', accessToken);
console.log(`Meeting: ${meeting.topic}`);
console.log(`Join URL: ${meeting.join_url}`);
console.log(`Host: ${meeting.host_email}`);
```

## Step 3: Handle Meeting Events (webhooks)

```javascript
const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// Store meeting state (use database in production)
const meetingState = new Map();

/**
 * Verify Zoom webhook signature
 */
function verifyWebhookSignature(req, webhookSecret) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  const payload = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  
  const expectedSignature = `v0=${crypto
    .createHmac('sha256', webhookSecret)
    .update(payload)
    .digest('hex')}`;
  
  return signature === expectedSignature;
}

/**
 * Handle URL validation challenge (required for new subscriptions)
 */
function handleUrlValidation(req, res, webhookSecret) {
  const hashForValidation = crypto
    .createHmac('sha256', webhookSecret)
    .update(req.body.payload.plainToken)
    .digest('hex');
  
  return res.json({
    plainToken: req.body.payload.plainToken,
    encryptedToken: hashForValidation
  });
}

// Webhook endpoint
app.post('/webhooks/zoom', async (req, res) => {
  const WEBHOOK_SECRET = process.env.ZOOM_WEBHOOK_SECRET;
  
  // 1. Handle URL validation challenge
  if (req.body.event === 'endpoint.url_validation') {
    return handleUrlValidation(req, res, WEBHOOK_SECRET);
  }
  
  // 2. Verify webhook signature
  if (!verifyWebhookSignature(req, WEBHOOK_SECRET)) {
    console.error('Invalid webhook signature');
    return res.status(401).send('Invalid signature');
  }
  
  // 3. Process meeting events
  const { event, payload } = req.body;
  const meetingId = String(payload.object.id);
  
  console.log(`Received event: ${event} for meeting ${meetingId}`);
  
  try {
    switch (event) {
      case 'meeting.started':
        await handleMeetingStarted(meetingId, payload);
        break;
      case 'meeting.ended':
        await handleMeetingEnded(meetingId, payload);
        break;
      case 'meeting.participant_joined':
        await handleParticipantJoined(meetingId, payload);
        break;
      case 'meeting.participant_left':
        await handleParticipantLeft(meetingId, payload);
        break;
      default:
        console.log(`Unhandled event: ${event}`);
    }
    
    res.status(200).send();
  } catch (error) {
    console.error(`Error handling ${event}:`, error);
    // Return 200 to prevent Zoom from retrying
    // Log error for investigation
    res.status(200).send();
  }
});

// Event handlers
async function handleMeetingStarted(meetingId, payload) {
  const { object } = payload;
  
  // Initialize meeting state
  meetingState.set(meetingId, {
    topic: object.topic,
    host_id: object.host_id,
    start_time: object.start_time,
    participants: [],
    status: 'in_progress'
  });
  
  console.log(`✅ Meeting started: ${object.topic} (ID: ${meetingId})`);
  
  // Optional: Fetch full meeting details for additional context
  // const fullDetails = await getMeetingDetails(meetingId, accessToken);
}

async function handleMeetingEnded(meetingId, payload) {
  const { object } = payload;
  const state = meetingState.get(meetingId);
  
  if (state) {
    state.status = 'ended';
    state.end_time = object.end_time;
    state.duration = object.duration;
    
    console.log(`🏁 Meeting ended: ${state.topic}`);
    console.log(`   Duration: ${state.duration} minutes`);
    console.log(`   Total participants: ${state.participants.length}`);
    
    // Trigger post-meeting processing
    await processMeetingRecords(meetingId, state);
  }
}

async function handleParticipantJoined(meetingId, payload) {
  const { object } = payload;
  const participant = object.participant;
  const state = meetingState.get(meetingId);
  
  if (state) {
    state.participants.push({
      user_id: participant.user_id,
      user_name: participant.user_name,
      email: participant.email,
      join_time: participant.join_time,
      status: 'in_meeting'
    });
    
    console.log(`👋 ${participant.user_name} joined meeting ${meetingId}`);
  }
}

async function handleParticipantLeft(meetingId, payload) {
  const { object } = payload;
  const participant = object.participant;
  const state = meetingState.get(meetingId);
  
  if (state) {
    const p = state.participants.find(p => p.user_id === participant.user_id);
    if (p) {
      p.leave_time = participant.leave_time;
      p.status = 'left';
    }
    
    console.log(`👋 ${participant.user_name} left meeting ${meetingId}`);
  }
}

async function processMeetingRecords(meetingId, state) {
  // Save to database, generate reports, notify stakeholders, etc.
  console.log('Processing meeting records...');
  
  // Example: Calculate attendance stats
  const attendanceReport = {
    meeting_id: meetingId,
    topic: state.topic,
    duration_minutes: state.duration,
    total_participants: state.participants.length,
    participants: state.participants.map(p => ({
      name: p.user_name,
      email: p.email,
      joined: p.join_time,
      left: p.leave_time || state.end_time
    }))
  };
  
  console.log(JSON.stringify(attendanceReport, null, 2));
  
  // Clean up in-memory state
  meetingState.delete(meetingId);
}

app.listen(3000, () => {
  console.log('Webhook server running on port 3000');
});
```

## Complete Integration Example

```javascript
/**
 * Complete example: Meeting Dashboard Integration
 * 
 * Skills used:
 * 1. zoom-rest-api - Get meeting details
 * 2. webhooks - Real-time event updates
 */

const express = require('express');
const axios = require('axios');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// In-memory store (use Redis/database in production)
const meetings = new Map();

// ============================================
// AUTHENTICATION HELPER
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

// ============================================
// STEP 1: REST API - Get Meeting Details
// ============================================

async function getMeetingDetails(meetingId) {
  const token = await getAccessToken();
  
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return response.data;
}

// API endpoint to fetch and track a meeting
app.get('/api/meetings/:meetingId', async (req, res) => {
  try {
    const { meetingId } = req.params;
    
    // Get meeting details from Zoom API (zoom-rest-api skill)
    const details = await getMeetingDetails(meetingId);
    
    // Store for tracking (webhook events will update this)
    meetings.set(meetingId, {
      ...details,
      participants: [],
      events: [],
      tracking_status: 'active'
    });
    
    res.json({
      success: true,
      meeting: {
        id: details.id,
        topic: details.topic,
        start_time: details.start_time,
        join_url: details.join_url,
        host_email: details.host_email
      },
      message: 'Meeting tracked. Events will be received via webhook.'
    });
  } catch (error) {
    res.status(error.response?.status || 500).json({
      success: false,
      error: error.message
    });
  }
});

// ============================================
// STEP 2: WEBHOOKS - Receive Meeting Events
// ============================================

function verifyWebhook(req) {
  const signature = req.headers['x-zm-signature'];
  const timestamp = req.headers['x-zm-request-timestamp'];
  const payload = `v0:${timestamp}:${JSON.stringify(req.body)}`;
  const expected = `v0=${crypto
    .createHmac('sha256', process.env.ZOOM_WEBHOOK_SECRET)
    .update(payload)
    .digest('hex')}`;
  
  return signature === expected;
}

app.post('/webhooks/zoom', async (req, res) => {
  // URL validation challenge
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
  if (!verifyWebhook(req)) {
    return res.status(401).send('Invalid signature');
  }
  
  const { event, payload } = req.body;
  const meetingId = String(payload.object.id);
  
  // Get or create meeting record
  let meeting = meetings.get(meetingId);
  if (!meeting) {
    // Meeting wasn't pre-fetched, create minimal record
    meeting = {
      id: meetingId,
      topic: payload.object.topic,
      participants: [],
      events: [],
      tracking_status: 'webhook_only'
    };
    meetings.set(meetingId, meeting);
  }
  
  // Log event
  meeting.events.push({
    type: event,
    timestamp: new Date().toISOString(),
    data: payload
  });
  
  // Update meeting state based on event
  switch (event) {
    case 'meeting.started':
      meeting.status = 'in_progress';
      meeting.actual_start_time = payload.object.start_time;
      console.log(`✅ Meeting started: ${meeting.topic}`);
      break;
      
    case 'meeting.ended':
      meeting.status = 'ended';
      meeting.end_time = payload.object.end_time;
      meeting.actual_duration = payload.object.duration;
      console.log(`🏁 Meeting ended: ${meeting.topic} (${meeting.actual_duration} min)`);
      break;
      
    case 'meeting.participant_joined':
      meeting.participants.push({
        ...payload.object.participant,
        status: 'in_meeting'
      });
      console.log(`👋 ${payload.object.participant.user_name} joined`);
      break;
      
    case 'meeting.participant_left':
      const p = meeting.participants.find(
        p => p.user_id === payload.object.participant.user_id
      );
      if (p) {
        p.status = 'left';
        p.leave_time = payload.object.participant.leave_time;
      }
      console.log(`👋 ${payload.object.participant.user_name} left`);
      break;
  }
  
  res.status(200).send();
});

// ============================================
// STEP 3: Query Meeting Status
// ============================================

app.get('/api/meetings/:meetingId/status', (req, res) => {
  const meeting = meetings.get(req.params.meetingId);
  
  if (!meeting) {
    return res.status(404).json({ error: 'Meeting not tracked' });
  }
  
  res.json({
    id: meeting.id,
    topic: meeting.topic,
    status: meeting.status || 'scheduled',
    participants_in_meeting: meeting.participants.filter(p => p.status === 'in_meeting').length,
    total_participants: meeting.participants.length,
    events_count: meeting.events.length,
    last_event: meeting.events[meeting.events.length - 1]?.type
  });
});

// ============================================
// START SERVER
// ============================================

app.listen(3000, () => {
  console.log('Server running on port 3000');
  console.log('');
  console.log('Endpoints:');
  console.log('  GET  /api/meetings/:id        - Fetch & track meeting (zoom-rest-api)');
  console.log('  GET  /api/meetings/:id/status - Get meeting status');
  console.log('  POST /webhooks/zoom           - Webhook receiver (webhooks)');
});
```

## Meeting Event Types Reference

| Event | Trigger | Key Payload Fields |
|-------|---------|-------------------|
| `meeting.started` | Host starts meeting | `id`, `topic`, `host_id`, `start_time` |
| `meeting.ended` | Meeting ends | `id`, `end_time`, `duration` |
| `meeting.participant_joined` | User joins | `participant.user_id`, `participant.user_name`, `participant.join_time` |
| `meeting.participant_left` | User leaves | `participant.user_id`, `participant.leave_time` |
| `meeting.sharing_started` | Screen share begins | `participant`, `sharing_details` |
| `meeting.sharing_ended` | Screen share ends | `participant` |

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| 404 on GET /meetings | Invalid meeting ID | Verify meeting ID exists |
| 401 on API call | Expired token | Refresh access token |
| Invalid webhook signature | Wrong secret or modified payload | Verify WEBHOOK_SECRET matches app config |
| Missing events | Subscription not active | Check Event Subscriptions in Marketplace |

### Retry Logic for REST API

```javascript
async function getMeetingWithRetry(meetingId, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await getMeetingDetails(meetingId);
    } catch (error) {
      if (error.response?.status === 429) {
        // Rate limited - wait and retry
        const retryAfter = error.response.headers['retry-after'] || 1;
        await new Promise(r => setTimeout(r, retryAfter * 1000));
        continue;
      }
      if (error.response?.status === 401 && attempt < maxRetries) {
        // Token expired - refresh and retry
        await refreshAccessToken();
        continue;
      }
      throw error;
    }
  }
}
```

## Best Practices

1. **Fetch meeting details first** - Get context before events arrive
2. **Handle events idempotently** - Webhooks may be delivered multiple times
3. **Use meeting UUID for tracking** - More reliable than meeting ID for recurring meetings
4. **Store events for audit** - Log all events for debugging and compliance
5. **Implement retry logic** - REST API calls may fail transiently
6. **Return 200 for webhooks** - Even on processing errors, to prevent retries

## Related Use Cases

- **[Recording & Transcription](recording-transcription.md)** - Download recordings after meeting ends
- **[Meeting Automation](meeting-automation.md)** - Create and manage meetings programmatically
- **[Real-Time Media Streams](real-time-media-streams.md)** - Access live audio/video during meeting

## Resources

- **Meetings API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Meetings
- **Webhook Events**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/events/
- **Event Subscriptions**: https://developers.zoom.us/docs/api/rest/webhook-reference/

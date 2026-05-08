# Meeting Lifecycle - Complete CRUD with Webhook Integration

Complete working examples for the full meeting lifecycle: Create → Update → Start → End → Delete, with webhook event integration.

## Prerequisites

- Server-to-Server OAuth token (see [Authentication Flows](../concepts/authentication-flows.md))
- Scopes: `meeting:write`, `meeting:read` (minimum)
- Base URL: `https://api.zoom.us/v2`

## Step 1: Create a Meeting

### Instant Meeting (No Fixed Time)

```bash
curl -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Quick Team Sync",
    "type": 1,
    "settings": {
      "join_before_host": false,
      "waiting_room": true,
      "approval_type": 2
    }
  }'
```

### Scheduled Meeting

```bash
curl -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type": application/json" \
  -d '{
    "topic": "Q1 Planning Meeting",
    "type": 2,
    "start_time": "2025-03-15T10:00:00Z",
    "duration": 60,
    "timezone": "America/New_York",
    "agenda": "Discuss Q1 goals and milestones",
    "settings": {
      "host_video": true,
      "participant_video": false,
      "join_before_host": false,
      "waiting_room": true,
      "mute_upon_entry": true,
      "approval_type": 2,
      "auto_recording": "cloud",
      "alternative_hosts": "alt.host@example.com"
    }
  }'
```

### Node.js Example

```javascript
async function createMeeting(accessToken, meetingData) {
  const response = await fetch('https://api.zoom.us/v2/users/me/meetings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(meetingData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Failed to create meeting: ${error.message}`);
  }

  return await response.json();
}

// Usage
const meetingData = {
  topic: 'Team Standup',
  type: 2,  // Scheduled
  start_time: '2025-03-15T14:00:00Z',
  duration: 30,
  settings: {
    join_before_host: false,
    waiting_room: true
  }
};

const meeting = await createMeeting(accessToken, meetingData);
console.log('Meeting created:', meeting.id);
console.log('Join URL:', meeting.join_url);
```

### Response

```json
{
  "id": 93123456789,
  "uuid": "xyzAbC1234==",
  "host_id": "abc123def456",
  "topic": "Q1 Planning Meeting",
  "type": 2,
  "start_time": "2025-03-15T10:00:00Z",
  "duration": 60,
  "timezone": "America/New_York",
  "created_at": "2025-02-09T12:30:00Z",
  "join_url": "https://zoom.us/j/93123456789",
  "start_url": "https://zoom.us/s/93123456789?zak=...",
  "settings": {
    "host_video": true,
    "participant_video": false,
    "waiting_room": true,
    "auto_recording": "cloud"
  }
}
```

### Meeting Types

| Type | Value | Description |
|------|-------|-------------|
| Instant | `1` | Start immediately, no fixed time |
| Scheduled | `2` | Fixed date/time |
| Recurring (no fixed time) | `3` | PMI meetings |
| Recurring (fixed time) | `8` | Series with schedule |

## Step 2: Update a Meeting

### Update Meeting Details

```bash
curl -X PATCH "https://api.zoom.us/v2/meetings/93123456789" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Q1 Planning - Updated",
    "start_time": "2025-03-15T14:00:00Z",
    "duration": 90,
    "settings": {
      "waiting_room": false
    }
  }'
```

### Node.js Example

```javascript
async function updateMeeting(accessToken, meetingId, updates) {
  const response = await fetch(`https://api.zoom.us/v2/meetings/${meetingId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Failed to update meeting: ${error.message}`);
  }

  // PATCH returns 204 No Content on success
  return response.status === 204;
}

// Usage
const updates = {
  topic: 'Q1 Planning - Updated Agenda',
  duration: 90
};

await updateMeeting(accessToken, 93123456789, updates);
console.log('Meeting updated successfully');
```

### Partial Updates

You only need to include fields you want to change:

```javascript
// Only update topic
await updateMeeting(accessToken, meetingId, {
  topic: 'New Topic'
});

// Only update settings
await updateMeeting(accessToken, meetingId, {
  settings: {
    waiting_room: true,
    mute_upon_entry: true
  }
});
```

## Step 3: Get Meeting Details

```bash
curl "https://api.zoom.us/v2/meetings/93123456789" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### Node.js Example

```javascript
async function getMeeting(accessToken, meetingId) {
  const response = await fetch(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Failed to get meeting: ${error.message}`);
  }

  return await response.json();
}

// Usage
const meeting = await getMeeting(accessToken, 93123456789);
console.log('Meeting:', meeting.topic);
console.log('Start time:', meeting.start_time);
console.log('Join URL:', meeting.join_url);
```

## Step 4: List User's Meetings

```bash
curl "https://api.zoom.us/v2/users/me/meetings?type=scheduled&page_size=30" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### Node.js with Pagination

```javascript
async function listAllMeetings(accessToken, userId = 'me') {
  let allMeetings = [];
  let nextPageToken = '';

  while (true) {
    const params = new URLSearchParams({
      type: 'scheduled',
      page_size: 300,
      ...(nextPageToken && { next_page_token: nextPageToken })
    });

    const response = await fetch(
      `https://api.zoom.us/v2/users/${userId}/meetings?${params}`,
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Failed to list meetings: ${error.message}`);
    }

    const data = await response.json();
    allMeetings = allMeetings.concat(data.meetings);

    nextPageToken = data.next_page_token;
    if (!nextPageToken) break;
  }

  return allMeetings;
}

// Usage
const meetings = await listAllMeetings(accessToken);
console.log(`Found ${meetings.length} meetings`);
meetings.forEach(m => console.log(`- ${m.topic} (${m.start_time})`));
```

### Meeting List Types

| Type | Value | Description |
|------|-------|-------------|
| Scheduled | `scheduled` | Future meetings |
| Live | `live` | Currently active |
| Upcoming | `upcoming` | Within next 30 days |

## Step 5: Delete a Meeting

```bash
curl -X DELETE "https://api.zoom.us/v2/meetings/93123456789" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### Node.js Example

```javascript
async function deleteMeeting(accessToken, meetingId, options = {}) {
  const params = new URLSearchParams();
  
  // Optional: Cancel single occurrence of recurring meeting
  if (options.occurrenceId) {
    params.append('occurrence_id', options.occurrenceId);
  }
  
  // Optional: Send cancellation email
  if (options.scheduleForReminder !== undefined) {
    params.append('schedule_for_reminder', options.scheduleForReminder);
  }

  const url = `https://api.zoom.us/v2/meetings/${meetingId}${params.toString() ? '?' + params.toString() : ''}`;

  const response = await fetch(url, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Failed to delete meeting: ${error.message}`);
  }

  // DELETE returns 204 No Content on success
  return response.status === 204;
}

// Usage
await deleteMeeting(accessToken, 93123456789);
console.log('Meeting deleted successfully');
```

## Webhook Integration

To receive real-time events for meeting lifecycle, set up webhooks. See [Webhook Server Example](webhook-server.md) for full implementation.

### Key Meeting Events

| Event | When It Fires |
|-------|---------------|
| `meeting.created` | Meeting is created |
| `meeting.updated` | Meeting details changed |
| `meeting.deleted` | Meeting is deleted |
| `meeting.started` | Meeting begins |
| `meeting.ended` | Meeting ends |
| `meeting.participant_joined` | Participant joins |
| `meeting.participant_left` | Participant leaves |
| `recording.completed` | Cloud recording finishes processing |

### Webhook Payload Example

**Event:** `meeting.started`

```json
{
  "event": "meeting.started",
  "event_ts": 1707486720000,
  "payload": {
    "account_id": "abc123",
    "object": {
      "id": "93123456789",
      "uuid": "xyzAbC1234==",
      "host_id": "def456",
      "topic": "Q1 Planning Meeting",
      "type": 2,
      "start_time": "2025-03-15T14:00:00Z",
      "duration": 60,
      "timezone": "America/New_York"
    }
  }
}
```

### Webhook Handler Example

```javascript
// Express.js webhook endpoint
app.post('/webhook', express.json(), (req, res) => {
  const { event, payload } = req.body;

  switch (event) {
    case 'meeting.started':
      console.log(`Meeting started: ${payload.object.topic}`);
      // Trigger recording, send notifications, etc.
      break;

    case 'meeting.ended':
      console.log(`Meeting ended: ${payload.object.topic}`);
      // Process analytics, download recordings, etc.
      break;

    case 'recording.completed':
      console.log(`Recording ready: ${payload.object.topic}`);
      // Download recording (see recording-pipeline.md)
      break;

    default:
      console.log(`Unhandled event: ${event}`);
  }

  // Respond with 200 to acknowledge receipt
  res.status(200).send();
});
```

## Complete Lifecycle Workflow

### Automated Meeting Management

```javascript
class MeetingManager {
  constructor(accessToken) {
    this.accessToken = accessToken;
  }

  async createScheduledMeeting(topic, startTime, duration = 60) {
    const meetingData = {
      topic,
      type: 2,
      start_time: startTime,
      duration,
      settings: {
        join_before_host: false,
        waiting_room: true,
        auto_recording: 'cloud'
      }
    };

    const meeting = await this.createMeeting(meetingData);
    console.log(`Created meeting: ${meeting.id}`);
    
    return meeting;
  }

  async updateMeetingTime(meetingId, newStartTime) {
    await this.updateMeeting(meetingId, {
      start_time: newStartTime
    });
    console.log(`Updated meeting ${meetingId} start time`);
  }

  async cancelMeeting(meetingId) {
    await this.deleteMeeting(meetingId, {
      schedule_for_reminder: true  // Send cancellation email
    });
    console.log(`Cancelled meeting ${meetingId}`);
  }

  async getUpcomingMeetings() {
    const meetings = await this.listAllMeetings();
    const now = new Date();
    
    return meetings.filter(m => {
      const startTime = new Date(m.start_time);
      return startTime > now;
    });
  }

  // Helper methods (implementations from above examples)
  async createMeeting(data) { /* ... */ }
  async updateMeeting(id, updates) { /* ... */ }
  async deleteMeeting(id, options) { /* ... */ }
  async listAllMeetings() { /* ... */ }
}

// Usage
const manager = new MeetingManager(accessToken);

// Create meeting
const meeting = await manager.createScheduledMeeting(
  'Team Standup',
  '2025-03-15T10:00:00Z',
  30
);

// Update if needed
await manager.updateMeetingTime(meeting.id, '2025-03-15T14:00:00Z');

// Get all upcoming meetings
const upcoming = await manager.getUpcomingMeetings();
console.log(`${upcoming.length} upcoming meetings`);

// Cancel if needed
await manager.cancelMeeting(meeting.id);
```

## Common Patterns

### Recurring Meeting Series

```javascript
const recurringMeeting = {
  topic: 'Weekly Team Sync',
  type: 8,  // Recurring with fixed time
  start_time: '2025-03-15T10:00:00Z',
  duration: 30,
  recurrence: {
    type: 2,  // Weekly
    repeat_interval: 1,
    weekly_days: '1,3,5',  // Monday, Wednesday, Friday
    end_times: 20  // 20 occurrences
  }
};

const meeting = await createMeeting(accessToken, recurringMeeting);
```

### Meeting with Registration

```javascript
const meetingWithRegistration = {
  topic: 'Product Demo',
  type: 2,
  start_time: '2025-03-15T14:00:00Z',
  duration: 60,
  settings: {
    approval_type: 0,  // Automatic approval
    registration_type: 1,  // Attendees register once
    meeting_authentication: false
  }
};

const meeting = await createMeeting(accessToken, meetingWithRegistration);
console.log('Registration URL:', meeting.registration_url);
```

### PMI Meeting

```javascript
const pmiMeeting = {
  topic: 'My Personal Room',
  type: 3,  // Recurring with no fixed time (PMI)
  settings: {
    use_pmi: true,
    join_before_host: true
  }
};

const meeting = await createMeeting(accessToken, pmiMeeting);
```

## Error Handling

### Per-User Daily Limit

Meeting/webinar create/update operations are limited to **100 per day per user** (resets at 00:00 UTC).

```javascript
async function createMeetingWithRetry(accessToken, meetingData, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await createMeeting(accessToken, meetingData);
    } catch (error) {
      if (error.message.includes('Too many requests')) {
        console.log(`Hit per-user limit. Attempt ${attempt}/${maxRetries}`);
        if (attempt < maxRetries) {
          await sleep(5000);  // Wait 5 seconds
          continue;
        }
      }
      throw error;
    }
  }
}
```

### Validation Errors

```javascript
try {
  await createMeeting(accessToken, meetingData);
} catch (error) {
  if (error.message.includes('Invalid field')) {
    console.error('Validation error:', error);
    // Check start_time format, type value, etc.
  } else if (error.message.includes('User does not exist')) {
    console.error('Invalid userId');
  } else {
    throw error;
  }
}
```

## Related Documentation

- **[API Architecture](../concepts/api-architecture.md)** - Base URLs, `me` keyword, time formats
- **[Authentication Flows](../concepts/authentication-flows.md)** - Get access tokens
- **[Webhook Server](webhook-server.md)** - Receive meeting events
- **[Recording Pipeline](recording-pipeline.md)** - Download meeting recordings
- **[Meetings Reference](../references/meetings.md)** - Complete endpoint documentation

## Resources

- [Create Meeting API](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingCreate)
- [Update Meeting API](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingUpdate)
- [Meeting Events](https://developers.zoom.us/docs/api/meetings/events/)

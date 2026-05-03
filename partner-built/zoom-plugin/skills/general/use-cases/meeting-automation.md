# Meeting Automation

Schedule, update, and delete Zoom meetings programmatically.

## Overview

Use the Zoom REST API to automate meeting management - create meetings, update settings, manage participants, and delete meetings without manual intervention.

If your primary goal is deterministic backend automation, stay on REST API.
If your primary goal is AI-agent tool invocation (for example, natural-language meeting management), route to `zoom-mcp` instead.

## Skills Needed

- **zoom-rest-api** - Primary
- **zoom-mcp** - Optional alternative for AI-driven tool workflows

## Prerequisites

- Server-to-Server OAuth or OAuth app
- `meeting:write` scope

## Quick Start

```bash
# Create a meeting
curl -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer {accessToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Automated Meeting",
    "type": 2,
    "start_time": "2024-01-15T10:00:00Z",
    "duration": 60
  }'
```

## Common Tasks

### Creating Recurring Meetings

```javascript
const axios = require('axios');

// Daily recurring meeting
async function createDailyMeeting() {
  const response = await axios.post(
    'https://api.zoom.us/v2/users/me/meetings',
    {
      topic: 'Daily Standup',
      type: 8,  // Recurring with fixed time
      start_time: '2024-01-15T09:00:00Z',
      duration: 15,
      timezone: 'America/Los_Angeles',
      recurrence: {
        type: 1,  // Daily
        repeat_interval: 1,  // Every day
        end_times: 90  // 90 occurrences
      },
      settings: {
        join_before_host: true,
        waiting_room: false,
        mute_upon_entry: true
      }
    },
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data;
}

// Weekly recurring meeting
async function createWeeklyMeeting() {
  const response = await axios.post(
    'https://api.zoom.us/v2/users/me/meetings',
    {
      topic: 'Weekly Team Sync',
      type: 8,
      start_time: '2024-01-15T14:00:00Z',
      duration: 60,
      recurrence: {
        type: 2,  // Weekly
        repeat_interval: 1,
        weekly_days: '2,4',  // Monday, Wednesday (1=Sun, 2=Mon, etc.)
        end_date_time: '2024-12-31T00:00:00Z'
      }
    },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  return response.data;
}
```

### Updating Meeting Settings

```javascript
// Update meeting details
async function updateMeeting(meetingId, updates) {
  await axios.patch(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    {
      topic: updates.topic,
      start_time: updates.startTime,
      duration: updates.duration,
      settings: {
        host_video: updates.hostVideo ?? true,
        participant_video: updates.participantVideo ?? false,
        join_before_host: updates.joinBeforeHost ?? false,
        waiting_room: updates.waitingRoom ?? true,
        mute_upon_entry: updates.muteOnEntry ?? true,
        auto_recording: updates.autoRecording ?? 'none'  // 'local', 'cloud', 'none'
      }
    },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}

// Add meeting co-hosts
async function addCoHosts(meetingId, emails) {
  // Co-hosts must be set before meeting starts
  await axios.patch(
    `https://api.zoom.us/v2/meetings/${meetingId}`,
    {
      settings: {
        alternative_hosts: emails.join(';'),
        alternative_hosts_email_notification: true
      }
    },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}
```

### Managing Registrants

```javascript
// Add registrant
async function addRegistrant(meetingId, registrant) {
  const response = await axios.post(
    `https://api.zoom.us/v2/meetings/${meetingId}/registrants`,
    {
      email: registrant.email,
      first_name: registrant.firstName,
      last_name: registrant.lastName,
      custom_questions: [
        { title: 'Company', value: registrant.company },
        { title: 'Role', value: registrant.role }
      ]
    },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  // Returns join_url for the registrant
  return response.data;
}

// List registrants
async function listRegistrants(meetingId, status = 'approved') {
  // status: 'pending', 'approved', 'denied'
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${meetingId}/registrants?status=${status}`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  return response.data.registrants;
}

// Approve/deny registrants
async function updateRegistrantStatus(meetingId, registrantId, action) {
  // action: 'approve', 'deny', 'cancel'
  await axios.put(
    `https://api.zoom.us/v2/meetings/${meetingId}/registrants/status`,
    {
      action: action,
      registrants: [{ id: registrantId }]
    },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}
```

### Deleting/Canceling Meetings

```javascript
// Delete meeting
async function deleteMeeting(meetingId, notifyHosts = true) {
  await axios.delete(
    `https://api.zoom.us/v2/meetings/${meetingId}?schedule_for_reminder=${notifyHosts}`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}

// Delete specific occurrence of recurring meeting
async function deleteOccurrence(meetingId, occurrenceId) {
  await axios.delete(
    `https://api.zoom.us/v2/meetings/${meetingId}?occurrence_id=${occurrenceId}`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}

// End a live meeting
async function endMeeting(meetingId) {
  await axios.put(
    `https://api.zoom.us/v2/meetings/${meetingId}/status`,
    { action: 'end' },
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
}
```

### Rate Limit Considerations

| Operation | Limit |
|-----------|-------|
| Create/Update meetings | 100 per user per day |
| API calls (Light) | 30/sec (Pro), 80/sec (Business+) |
| API calls (Heavy) | 10/sec (Pro), 40/sec (Business+) |

```javascript
// Implement rate limiting
const Bottleneck = require('bottleneck');

const limiter = new Bottleneck({
  minTime: 100,  // 10 requests per second max
  maxConcurrent: 5
});

const createMeetingLimited = limiter.wrap(createMeeting);
```

## Resources

- **API Reference**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Meetings
- **Rate Limits**: https://developers.zoom.us/docs/api/rest/rate-limits/

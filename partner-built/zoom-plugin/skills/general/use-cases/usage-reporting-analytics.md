# Usage Reporting & Analytics

Get meeting statistics, usage reports, and billing data from Zoom.

## Overview

Access Zoom's reporting APIs to track meeting usage, participant statistics, and generate analytics for billing, compliance, or business intelligence.

## Skills Needed

- **zoom-rest-api** - Primary

## Report Types

| Report | Description |
|--------|-------------|
| Daily usage | Meetings per day, minutes used |
| Meeting details | Participant list, join/leave times |
| Webinar reports | Attendee, Q&A, poll data |
| Billing reports | Usage for billing purposes |

## Prerequisites

- Admin or owner account
- `report:read` scope

## Quick Start

```bash
# Get daily usage report
curl -X GET "https://api.zoom.us/v2/report/daily?year=2024&month=1" \
  -H "Authorization: Bearer {accessToken}"

# Get meeting participants
curl -X GET "https://api.zoom.us/v2/report/meetings/{meetingId}/participants" \
  -H "Authorization: Bearer {accessToken}"
```

## Common Tasks

### Daily/Monthly Usage Summaries

```javascript
const axios = require('axios');

// Get daily usage report
async function getDailyUsage(year, month) {
  const response = await axios.get(
    `https://api.zoom.us/v2/report/daily`,
    {
      params: { year, month },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  // Returns: dates[], total_meeting_minutes, total_meetings, total_participants
  return response.data;
}

// Aggregate monthly statistics
async function getMonthlyStats(year, month) {
  const daily = await getDailyUsage(year, month);
  
  return {
    totalMeetings: daily.dates.reduce((sum, d) => sum + d.meetings, 0),
    totalMinutes: daily.dates.reduce((sum, d) => sum + d.meeting_minutes, 0),
    totalParticipants: daily.dates.reduce((sum, d) => sum + d.participants, 0),
    averageMeetingDuration: daily.dates.length > 0 
      ? daily.total_meeting_minutes / daily.total_meetings 
      : 0,
    peakDay: daily.dates.reduce((max, d) => 
      d.meetings > max.meetings ? d : max, { meetings: 0 }
    )
  };
}

// Get user-level activity
async function getUserActivity(userId, fromDate, toDate) {
  const response = await axios.get(
    `https://api.zoom.us/v2/report/users/${userId}/meetings`,
    {
      params: { from: fromDate, to: toDate, page_size: 300 },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.data.meetings;
}
```

### Per-Meeting Participant Reports

```javascript
// Get meeting participants
async function getMeetingParticipants(meetingId) {
  // Note: meetingId can be meeting ID or UUID
  // If UUID contains / or //, double-encode it
  const encodedId = meetingId.includes('/') 
    ? encodeURIComponent(encodeURIComponent(meetingId))
    : meetingId;
  
  const response = await axios.get(
    `https://api.zoom.us/v2/report/meetings/${encodedId}/participants`,
    {
      params: { page_size: 300 },
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.data.participants;
}

// Calculate meeting metrics
function calculateMeetingMetrics(participants) {
  const uniqueParticipants = new Set(participants.map(p => p.user_email || p.name));
  
  // Calculate duration per participant
  const durations = participants.map(p => {
    const join = new Date(p.join_time);
    const leave = new Date(p.leave_time);
    return (leave - join) / 1000 / 60; // minutes
  });
  
  return {
    totalParticipants: uniqueParticipants.size,
    peakConcurrent: calculatePeakConcurrent(participants),
    averageAttendanceDuration: average(durations),
    lateJoiners: participants.filter(p => /* logic for late join */).length,
    earlyLeavers: participants.filter(p => /* logic for early leave */).length
  };
}

function calculatePeakConcurrent(participants) {
  const events = [];
  participants.forEach(p => {
    events.push({ time: new Date(p.join_time), delta: 1 });
    events.push({ time: new Date(p.leave_time), delta: -1 });
  });
  
  events.sort((a, b) => a.time - b.time);
  
  let current = 0;
  let peak = 0;
  events.forEach(e => {
    current += e.delta;
    peak = Math.max(peak, current);
  });
  
  return peak;
}
```

### Webinar Analytics

```javascript
// Get webinar participants (panelists + attendees)
async function getWebinarReport(webinarId) {
  const [participants, absentees, qa, polls] = await Promise.all([
    getWebinarParticipants(webinarId),
    getWebinarAbsentees(webinarId),
    getWebinarQA(webinarId),
    getWebinarPolls(webinarId)
  ]);
  
  return { participants, absentees, qa, polls };
}

async function getWebinarParticipants(webinarId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/report/webinars/${webinarId}/participants`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  return response.data.participants;
}

async function getWebinarAbsentees(webinarId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/report/webinars/${webinarId}/absentees`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  return response.data.registrants;
}

async function getWebinarQA(webinarId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/report/webinars/${webinarId}/qa`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  return response.data.questions;
}

async function getWebinarPolls(webinarId) {
  const response = await axios.get(
    `https://api.zoom.us/v2/report/webinars/${webinarId}/polls`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  return response.data.questions;
}

// Calculate webinar engagement score
function calculateEngagementScore(report) {
  const { participants, absentees, qa, polls } = report;
  
  const registeredCount = participants.length + absentees.length;
  const attendedCount = participants.length;
  const participatedInQA = new Set(qa.map(q => q.email)).size;
  const participatedInPolls = new Set(polls.flatMap(p => p.email)).size;
  
  return {
    attendanceRate: (attendedCount / registeredCount * 100).toFixed(1),
    qaParticipation: (participatedInQA / attendedCount * 100).toFixed(1),
    pollParticipation: (participatedInPolls / attendedCount * 100).toFixed(1),
    totalQuestions: qa.length,
    averageAttendanceDuration: average(participants.map(p => p.duration))
  };
}
```

### Exporting Data for BI Tools

```javascript
const { Parser } = require('json2csv');
const fs = require('fs');

// Export to CSV for BI tools
async function exportMeetingsToCSV(fromDate, toDate, outputPath) {
  // Get all meetings in date range
  const meetings = [];
  let nextPageToken = null;
  
  do {
    const response = await axios.get(
      'https://api.zoom.us/v2/report/users/me/meetings',
      {
        params: { 
          from: fromDate, 
          to: toDate, 
          page_size: 300,
          next_page_token: nextPageToken 
        },
        headers: { 'Authorization': `Bearer ${accessToken}` }
      }
    );
    
    meetings.push(...response.data.meetings);
    nextPageToken = response.data.next_page_token;
  } while (nextPageToken);
  
  // Flatten for CSV
  const flatMeetings = meetings.map(m => ({
    id: m.id,
    uuid: m.uuid,
    topic: m.topic,
    start_time: m.start_time,
    end_time: m.end_time,
    duration_minutes: m.duration,
    participants_count: m.participants_count,
    host_email: m.host_email,
    has_recording: m.has_recording ? 'yes' : 'no'
  }));
  
  const parser = new Parser();
  const csv = parser.parse(flatMeetings);
  
  fs.writeFileSync(outputPath, csv);
  return outputPath;
}

// Export to JSON for data warehouse
async function exportToDataWarehouse(fromDate, toDate) {
  const meetings = await getAllMeetings(fromDate, toDate);
  
  // Transform for BigQuery/Snowflake
  const records = meetings.map(m => ({
    ...m,
    _ingested_at: new Date().toISOString(),
    _source: 'zoom_api'
  }));
  
  // Send to warehouse
  await bigquery.dataset('zoom').table('meetings').insert(records);
}

// Scheduled export job
const cron = require('node-cron');

cron.schedule('0 1 * * *', async () => {
  // Run at 1 AM daily
  const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000);
  const from = yesterday.toISOString().split('T')[0];
  const to = from;
  
  await exportToDataWarehouse(from, to);
  console.log(`Exported data for ${from}`);
});
```

## Data Retention Notes

- **Meeting/Webinar reports**: Available for 12 months
- **Participant reports**: Available for 1 month after meeting ends
- **QSS (Quality of Service)**: Available for 30 days

## Resources

- **Reports API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Reports
- **Dashboard API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Dashboards

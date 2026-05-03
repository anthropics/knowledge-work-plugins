# AI Companion Integration

Integrate with Zoom AI Companion for meeting summaries, transcripts, and AI-powered features.

## Overview

Zoom AI Companion provides AI-powered features including:
- Meeting summaries (auto-generated)
- Meeting transcripts
- Real-time transcription
- Smart recording highlights
- Conversation archives

## What's Available via API

| Feature | API Access | Method |
|---------|------------|--------|
| Meeting Summaries | ✅ Yes | REST API |
| Meeting Transcripts | ✅ Yes | REST API (Cloud Recording) |
| Real-Time Transcripts | ✅ Yes | RTMS SDK |
| AI Companion Panel | ⚠️ Limited | Archive only |
| Conversation Archives | ✅ Yes | REST API |
| AI Controls in Meeting | ✅ Yes | Meeting SDK |

## Skills Needed

| Use Case | Skills |
|----------|--------|
| AI-agent search and tool invocation over Zoom meeting context | **zoom-mcp** |
| Get meeting summaries after meeting | **zoom-rest-api** |
| Get meeting transcripts in deterministic backend pipeline | **zoom-rest-api** + **zoom-webhooks** |
| Real-time transcript streaming | **rtms** |
| Control AI features in embedded meetings | **zoom-meeting-sdk** |

## Routing Modes

- Use **zoom-rest-api** when you need deterministic backend jobs, strict retry behavior, and explicit endpoint control.
- Use **zoom-mcp** when an AI system must discover and invoke Zoom tools dynamically.
- Use both when your architecture requires stable API automation plus AI-driven retrieval and assistance.

---

## Get Meeting Summary (REST API)

### Endpoint

```
GET /v2/meetings/{meetingUUID}/meeting_summary
```

### Prerequisites

1. Meeting Summary feature enabled in account settings
2. Server-to-Server OAuth app with admin scopes
3. Meeting must have ended with summary generated

### Example

```javascript
// Get meeting summary
async function getMeetingSummary(meetingUUID) {
  // Double-encode UUID if it contains / or //
  const encodedUUID = meetingUUID.startsWith('/') 
    ? encodeURIComponent(encodeURIComponent(meetingUUID))
    : encodeURIComponent(meetingUUID);
  
  const response = await fetch(
    `https://api.zoom.us/v2/meetings/${encodedUUID}/meeting_summary`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.json();
}

// Response example
{
  "meeting_uuid": "abc123...",
  "meeting_id": 12345678901,
  "meeting_topic": "Weekly Team Sync",
  "meeting_start_time": "2024-01-15T10:00:00Z",
  "meeting_end_time": "2024-01-15T10:45:00Z",
  "summary_start_time": "2024-01-15T10:00:00Z",
  "summary_end_time": "2024-01-15T10:45:00Z",
  "summary_content": {
    "summary": "The team discussed Q1 roadmap priorities...",
    "next_steps": [
      "John to finalize design specs by Friday",
      "Sarah to schedule customer interviews"
    ],
    "keywords": ["roadmap", "Q1", "design", "customers"]
  }
}
```

### Important Notes

- **Admin role required**: Standard users may not have access
- **Make app admin-managed**: Resolves permission issues
- **UUID encoding**: Double-encode UUIDs starting with `/`

---

## Get Meeting Transcript (REST API)

Transcripts are accessed via the Cloud Recording API.

### Endpoint

```
GET /v2/meetings/{meetingId}/recordings
```

### Example

```javascript
async function getMeetingTranscript(meetingId) {
  const response = await fetch(
    `https://api.zoom.us/v2/meetings/${meetingId}/recordings`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  const data = await response.json();
  
  // Find transcript files
  const transcriptFiles = data.recording_files.filter(
    file => file.file_type === 'TRANSCRIPT' || 
            file.file_type === 'CC' ||
            file.file_type === 'SUMMARY'
  );
  
  // Download transcript
  for (const file of transcriptFiles) {
    const transcriptResponse = await fetch(file.download_url, {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    
    if (file.file_extension === 'VTT') {
      const vttContent = await transcriptResponse.text();
      console.log('VTT Transcript:', vttContent);
    } else if (file.file_extension === 'JSON') {
      const jsonContent = await transcriptResponse.json();
      console.log('JSON Transcript:', jsonContent);
    }
  }
  
  return transcriptFiles;
}
```

### Transcript File Types

| File Type | Extension | Description |
|-----------|-----------|-------------|
| `TRANSCRIPT` | VTT, JSON | Full meeting transcript |
| `CC` | VTT | Closed captions |
| `SUMMARY` | JSON | AI-generated summary |

---

## Webhooks for AI Content

Listen for when AI content is ready:

```javascript
// Webhook handler
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  switch (event) {
    case 'recording.transcript_completed':
      // Transcript is ready
      console.log('Transcript ready for meeting:', payload.object.uuid);
      fetchAndStoreTranscript(payload.object.uuid);
      break;
      
    case 'recording.completed':
      // Recording processing complete (may include summary)
      console.log('Recording ready:', payload.object.uuid);
      break;
      
    case 'meeting.ended':
      // Meeting ended - summary will be generated soon
      console.log('Meeting ended:', payload.object.uuid);
      break;
  }
  
  res.sendStatus(200);
});
```

---

## Real-Time Transcripts (RTMS)

For live transcript streaming during meetings, use RTMS SDK.

### Prerequisites

- RTMS access approval from Zoom
- Server infrastructure for WebSocket connections

### Example

```javascript
import { RTMSClient } from "@zoom/rtms";

const client = new RTMSClient({
  clientId: process.env.ZOOM_CLIENT_ID,
  clientSecret: process.env.ZOOM_CLIENT_SECRET,
  secretToken: process.env.ZOOM_SECRET_TOKEN
});

// Connect to meeting
await client.joinMeeting({
  meetingUuid: meetingUUID,
  streamId: streamId,
  serverUrl: "wss://rtms.zoom.us"
});

// Listen for transcript events
client.on('transcript', (data) => {
  console.log(`[${data.speakerName}]: ${data.text}`);
  
  // Process real-time transcript
  // - Send to AI for sentiment analysis
  // - Display live captions
  // - Log for compliance
});
```

See **rtms** skill for full RTMS documentation.

---

## Meeting SDK - AI Companion Controls

Control AI Companion features in embedded meetings.

### Web SDK

```javascript
// Check if AI Companion is available
const aiCompanionStatus = ZoomMtg.getAICompanionStatus();

// AI Companion features are controlled by meeting settings
// The SDK respects account/meeting-level AI Companion settings
```

### Native SDKs (Android/iOS/Desktop)

Use `InMeetingAICompanionController`:

```java
// Android example
InMeetingAICompanionController aiController = 
    ZoomSDK.getInstance().getInMeetingService().getInMeetingAICompanionController();

// Check AI Companion status
boolean isEnabled = aiController.isAICompanionEnabled();

// Get available features
AICompanionFeature[] features = aiController.getAvailableFeatures();
// Features: QUERY, SMART_SUMMARY, SMART_RECORDING
```

```swift
// iOS example
let aiController = MobileRTC.shared().getMeetingService()?.getInMeetingAICompanionController()

if let isEnabled = aiController?.isAICompanionEnabled() {
    print("AI Companion enabled: \(isEnabled)")
}
```

### Feature Constants

| Feature | Description |
|---------|-------------|
| `QUERY` | Ask AI Companion questions |
| `SMART_SUMMARY` | Meeting summary generation |
| `SMART_RECORDING` | Smart recording highlights |

---

## Conversation Archives API

Archive AI Companion panel conversations (new September 2025).

```javascript
// Get conversation archives
async function getConversationArchives(userId) {
  const response = await fetch(
    `https://api.zoom.us/v2/users/${userId}/conversation_archive`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  return response.json();
}
```

---

## Common Integration Patterns

### Pattern 1: Post-Meeting Summary Pipeline

```javascript
// 1. Listen for meeting end
webhooks.on('meeting.ended', async (meeting) => {
  // 2. Wait for transcript to be ready (or use webhook)
  await delay(60000); // Processing time varies
  
  // 3. Fetch summary
  const summary = await getMeetingSummary(meeting.uuid);
  
  // 4. Store or distribute
  await saveSummaryToDatabase(summary);
  await sendSummaryToParticipants(meeting.participants, summary);
});
```

### Pattern 2: Real-Time AI Processing

```javascript
// Using RTMS for live processing
rtmsClient.on('transcript', async (data) => {
  // Send to your AI service for analysis
  const sentiment = await analyzesentiment(data.text);
  const actionItems = await extractActionItems(data.text);
  
  // Update live dashboard
  updateDashboard({ sentiment, actionItems });
});
```

### Pattern 3: Compliance Archival

```javascript
// Archive all AI-generated content
async function archiveMeetingAIContent(meetingId) {
  const [summary, transcript, archives] = await Promise.all([
    getMeetingSummary(meetingId),
    getMeetingTranscript(meetingId),
    getConversationArchives(meetingId)
  ]);
  
  await complianceStore.save({
    meetingId,
    summary,
    transcript,
    aiConversations: archives,
    archivedAt: new Date()
  });
}
```

---

## Required Scopes

| Scope | Description |
|-------|-------------|
| `meeting:read:admin` | Read meeting data including summaries |
| `recording:read:admin` | Access recordings and transcripts |
| `user:read:admin` | Read user data for archives |

---

## Limitations

| Limitation | Notes |
|------------|-------|
| AI Companion Panel | Most panel features NOT available via API |
| Admin access | Some endpoints require admin role |
| Processing time | Summaries/transcripts not instant after meeting |
| RTMS approval | Real-time access requires Zoom approval |
| Bot restrictions | Meeting SDK does NOT support bots (use RTMS) |

---

## Resources

- **AI Companion APIs**: https://developers.zoom.us/docs/api/ai-companion/
- **Meeting Summary API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingSummary
- **Cloud Recording API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Cloud-Recording
- **RTMS Documentation**: https://developers.zoom.us/docs/rtms/

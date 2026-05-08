# Recording & Transcription

Download cloud recordings and access transcripts from Zoom meetings.

## Overview

Access Zoom's cloud recordings and automated transcripts via webhooks and REST API for archival, compliance, or further processing.

For deterministic archival pipelines, keep REST API + webhooks as the primary route.
For AI-agent retrieval of summaries/transcripts through tool discovery, use `zoom-mcp`.

## Skills Needed

- **zoom-webhooks** - Receive recording.completed events (pipeline mode)
- **zoom-rest-api** - Download recordings and transcripts (pipeline mode)
- **zoom-mcp** - AI-driven transcript/summary retrieval (agent mode)

## Flow

```
Recording Flow:
1. Meeting ends
        ↓
2. Cloud recording processes
        ↓
3. Webhook: recording.completed
        ↓
4. API: Download recording files
        ↓
5. API: Get transcript (if enabled)
```

MCP Agent Flow:
1. Agent invokes search tool
        ↓
2. MCP: search meetings / recordings by context
        ↓
3. MCP: retrieve transcript-capable recording details
        ↓
4. Agent fetches transcript file or uses returned summary context

## Prerequisites

- Cloud recording enabled on account
- `recording:read` scope
- Webhook endpoint for `recording.completed`

## Quick Start

```javascript
// Handle recording.completed webhook
app.post('/webhook', async (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'recording.completed') {
    const { recording_files } = payload.object;
    
    for (const file of recording_files) {
      // Download recording
      const response = await fetch(file.download_url, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
    }
  }
  
  res.status(200).send();
});
```

## Common Tasks

### Downloading Video Recordings

```javascript
const axios = require('axios');
const fs = require('fs');

// Handle recording.completed webhook
app.post('/webhook', async (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'recording.completed') {
    const { uuid, recording_files } = payload.object;
    
    for (const file of recording_files) {
      if (file.file_type === 'MP4') {
        await downloadRecording(file, uuid);
      }
    }
  }
  
  res.status(200).send();
});

async function downloadRecording(file, meetingUuid) {
  // Download URL requires authentication
  const downloadUrl = file.download_url;
  
  const response = await axios({
    method: 'GET',
    url: downloadUrl,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    },
    responseType: 'stream'
  });
  
  // Save to file
  const writer = fs.createWriteStream(`recordings/${meetingUuid}.mp4`);
  response.data.pipe(writer);
  
  return new Promise((resolve, reject) => {
    writer.on('finish', resolve);
    writer.on('error', reject);
  });
}
```

### Getting Audio-Only Files

```javascript
// Recording files include multiple formats
const audioFormats = ['M4A'];
const videoFormats = ['MP4'];
const transcriptFormats = ['TRANSCRIPT', 'VTT'];

app.post('/webhook', async (req, res) => {
  const { recording_files } = req.body.payload.object;
  
  for (const file of recording_files) {
    switch (file.file_type) {
      case 'M4A':
        // Audio-only recording
        await saveFile(file, 'audio');
        break;
      case 'MP4':
        // Video recording (includes audio)
        await saveFile(file, 'video');
        break;
      case 'TRANSCRIPT':
        // JSON transcript
        await saveFile(file, 'transcript');
        break;
      case 'VTT':
        // WebVTT caption file
        await saveFile(file, 'captions');
        break;
    }
  }
});
```

### Accessing VTT Transcripts

```javascript
// VTT file comes with recording.completed webhook
async function downloadTranscript(file, meetingUuid) {
  const response = await axios.get(file.download_url, {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });
  
  // Parse VTT format
  const vttContent = response.data;
  const parsed = parseVTT(vttContent);
  
  return parsed;
}

// Simple VTT parser
function parseVTT(vttContent) {
  const lines = vttContent.split('\n');
  const cues = [];
  let currentCue = null;
  
  for (const line of lines) {
    if (line.includes('-->')) {
      const [start, end] = line.split(' --> ');
      currentCue = { start, end, text: '' };
    } else if (currentCue && line.trim()) {
      currentCue.text += line + ' ';
    } else if (currentCue && !line.trim()) {
      cues.push(currentCue);
      currentCue = null;
    }
  }
  
  return cues;
}
```

### Getting Transcript via API

```javascript
// Alternative: Get transcript via REST API
async function getTranscriptFromAPI(meetingUuid) {
  // Double-encode UUID if it contains '/' or '//'
  const encodedUuid = encodeURIComponent(encodeURIComponent(meetingUuid));
  
  const response = await axios.get(
    `https://api.zoom.us/v2/meetings/${encodedUuid}/recordings`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
  
  const transcriptFile = response.data.recording_files.find(
    f => f.file_type === 'TRANSCRIPT'
  );
  
  if (transcriptFile) {
    return await downloadTranscript(transcriptFile, meetingUuid);
  }
}
```

### Handling Recording Expiration

```javascript
// Recordings auto-delete based on account settings (30-120 days)
// Download and archive before expiration

// Option 1: Download immediately on webhook
app.post('/webhook', async (req, res) => {
  if (req.body.event === 'recording.completed') {
    await archiveRecording(req.body.payload);
  }
});

// Option 2: Batch download via scheduled job
async function downloadPendingRecordings() {
  // List recordings from last 7 days
  const from = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  const to = new Date().toISOString().split('T')[0];
  
  const response = await axios.get(
    `https://api.zoom.us/v2/users/me/recordings?from=${from}&to=${to}`,
    { headers: { 'Authorization': `Bearer ${accessToken}` }}
  );
  
  for (const meeting of response.data.meetings) {
    if (!isArchived(meeting.uuid)) {
      await archiveRecording(meeting);
    }
  }
}

// Run daily
cron.schedule('0 0 * * *', downloadPendingRecordings);
```

### Upload to Cloud Storage (S3/GCS)

```javascript
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { Upload } = require('@aws-sdk/lib-storage');

async function uploadToS3(stream, key) {
  const s3 = new S3Client({ region: 'us-east-1' });
  
  const upload = new Upload({
    client: s3,
    params: {
      Bucket: 'zoom-recordings',
      Key: key,
      Body: stream,
      ContentType: 'video/mp4'
    }
  });
  
  await upload.done();
  return `s3://zoom-recordings/${key}`;
}

// Stream directly from Zoom to S3
async function archiveToS3(file, meetingUuid) {
  const response = await axios({
    method: 'GET',
    url: file.download_url,
    headers: { 'Authorization': `Bearer ${accessToken}` },
    responseType: 'stream'
  });
  
  const key = `recordings/${meetingUuid}/${file.file_type.toLowerCase()}.${file.file_extension}`;
  return await uploadToS3(response.data, key);
}
```

## File Types Reference

| File Type | Extension | Description |
|-----------|-----------|-------------|
| MP4 | .mp4 | Video recording (active speaker or gallery) |
| M4A | .m4a | Audio-only recording |
| CHAT | .txt | Chat messages |
| TRANSCRIPT | .json | JSON transcript with timestamps |
| VTT | .vtt | WebVTT captions file |
| TIMELINE | .json | Meeting timeline events |

## Resources

- **Recordings API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Cloud-Recording
- **Recording Webhooks**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/events/#recording-completed

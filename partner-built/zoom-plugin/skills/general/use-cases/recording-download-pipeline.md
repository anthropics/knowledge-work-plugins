# Recording Download Pipeline

Automatically download Zoom Meeting cloud recordings to your own storage (S3, GCS, Azure Blob, etc.) using webhooks and REST API.

> **Note:** This is NOT Video SDK BYOS (Bring Your Own Storage). Video SDK BYOS saves recordings **directly** to S3 without downloading through Zoom servers. See `zoom-video-sdk` for true BYOS.

## Overview

Set up automated pipelines to download Zoom Meeting cloud recordings to your own storage infrastructure for compliance, cost management, or integration with existing media workflows.

## Skills Needed

- **webhooks** - Receive recording events
- **zoom-rest-api** - Download recordings

## Architecture

```
Recording Download Pipeline:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Zoom     │────▶│  Webhook    │────▶│   Your      │
│   Cloud     │     │  Handler    │     │   Storage   │
│  Recording  │     │             │     │  (S3, GCS)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Prerequisites

- Cloud recording enabled
- Webhook endpoint
- Storage bucket (S3, GCS, Azure, etc.)
- `recording:read` scope

## Workflow

1. Meeting ends, cloud recording completes
2. Receive `recording.completed` webhook
3. Download recording via API
4. Upload to your storage
5. (Optional) Delete from Zoom cloud

## Common Tasks

### S3 Upload Integration

```javascript
const axios = require('axios');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { Upload } = require('@aws-sdk/lib-storage');

const s3 = new S3Client({ region: 'us-east-1' });

// Handle recording.completed webhook
app.post('/webhook', async (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'recording.completed') {
    const { uuid, recording_files, host_email, topic } = payload.object;
    
    // Process each recording file
    for (const file of recording_files) {
      await uploadToS3(file, uuid, topic);
    }
    
    // Optionally delete from Zoom after successful upload
    // await deleteZoomRecording(uuid);
  }
  
  res.status(200).send();
});

async function uploadToS3(file, meetingUuid, topic) {
  // Download from Zoom
  const response = await axios({
    method: 'GET',
    url: file.download_url,
    headers: { 'Authorization': `Bearer ${accessToken}` },
    responseType: 'stream'
  });
  
  // Sanitize topic for filename
  const safeTopic = topic.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50);
  const key = `recordings/${meetingUuid}/${safeTopic}_${file.file_type}.${file.file_extension}`;
  
  // Upload to S3 using multipart upload for large files
  const upload = new Upload({
    client: s3,
    params: {
      Bucket: 'your-recordings-bucket',
      Key: key,
      Body: response.data,
      ContentType: getContentType(file.file_extension),
      Metadata: {
        'meeting-uuid': meetingUuid,
        'file-type': file.file_type,
        'recording-start': file.recording_start
      }
    }
  });
  
  await upload.done();
  return `s3://your-recordings-bucket/${key}`;
}
```

### GCS Upload Integration

```javascript
const { Storage } = require('@google-cloud/storage');
const storage = new Storage();
const bucket = storage.bucket('your-recordings-bucket');

async function uploadToGCS(file, meetingUuid, topic) {
  const response = await axios({
    method: 'GET',
    url: file.download_url,
    headers: { 'Authorization': `Bearer ${accessToken}` },
    responseType: 'stream'
  });
  
  const safeTopic = topic.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50);
  const filePath = `recordings/${meetingUuid}/${safeTopic}_${file.file_type}.${file.file_extension}`;
  
  const gcsFile = bucket.file(filePath);
  
  return new Promise((resolve, reject) => {
    const writeStream = gcsFile.createWriteStream({
      metadata: {
        contentType: getContentType(file.file_extension),
        metadata: {
          meetingUuid: meetingUuid,
          fileType: file.file_type
        }
      },
      resumable: true  // Important for large files
    });
    
    response.data.pipe(writeStream)
      .on('finish', () => resolve(`gs://your-recordings-bucket/${filePath}`))
      .on('error', reject);
  });
}
```

### Handling Large Files

```javascript
// Use streaming to avoid memory issues
async function streamDownload(downloadUrl, destination) {
  const response = await axios({
    method: 'GET',
    url: downloadUrl,
    headers: { 'Authorization': `Bearer ${accessToken}` },
    responseType: 'stream',
    maxContentLength: Infinity,  // Allow large files
    maxBodyLength: Infinity
  });
  
  // Track progress
  const totalSize = parseInt(response.headers['content-length'], 10);
  let downloadedSize = 0;
  
  response.data.on('data', (chunk) => {
    downloadedSize += chunk.length;
    const progress = ((downloadedSize / totalSize) * 100).toFixed(2);
    console.log(`Download progress: ${progress}%`);
  });
  
  return response.data;
}

// For very large files, use chunked upload
async function chunkedUploadToS3(stream, key) {
  const upload = new Upload({
    client: s3,
    params: {
      Bucket: 'your-bucket',
      Key: key,
      Body: stream
    },
    queueSize: 4,              // Concurrent part uploads
    partSize: 10 * 1024 * 1024 // 10MB parts
  });
  
  upload.on('httpUploadProgress', (progress) => {
    console.log(`Upload progress: ${progress.loaded}/${progress.total}`);
  });
  
  await upload.done();
}
```

### Retry Logic for Failed Downloads

```javascript
const retry = require('async-retry');

async function downloadWithRetry(file, meetingUuid) {
  return await retry(
    async (bail, attemptNumber) => {
      console.log(`Attempt ${attemptNumber} for ${file.file_type}`);
      
      try {
        return await uploadToS3(file, meetingUuid);
      } catch (error) {
        // Don't retry on permanent errors
        if (error.response?.status === 404) {
          bail(new Error('Recording not found'));
          return;
        }
        if (error.response?.status === 401) {
          // Refresh token and retry
          await refreshAccessToken();
        }
        throw error;  // Retry
      }
    },
    {
      retries: 3,
      factor: 2,
      minTimeout: 1000,
      maxTimeout: 10000,
      onRetry: (error, attempt) => {
        console.log(`Retry attempt ${attempt}: ${error.message}`);
      }
    }
  );
}

// Queue system for processing
const Queue = require('bull');
const recordingQueue = new Queue('recording-uploads', process.env.REDIS_URL || 'redis://YOUR_REDIS_HOST:6379');

recordingQueue.process(async (job) => {
  const { file, meetingUuid, topic } = job.data;
  return await downloadWithRetry(file, meetingUuid, topic);
});

// Add job with retry
app.post('/webhook', async (req, res) => {
  if (req.body.event === 'recording.completed') {
    const { uuid, recording_files, topic } = req.body.payload.object;
    
    for (const file of recording_files) {
      await recordingQueue.add(
        { file, meetingUuid: uuid, topic },
        { attempts: 3, backoff: { type: 'exponential', delay: 5000 }}
      );
    }
  }
  res.status(200).send();
});
```

### Recording Lifecycle Management

```javascript
// Delete from Zoom after successful upload
async function deleteZoomRecording(meetingUuid) {
  // Double-encode UUID if it contains / or //
  const encodedUuid = encodeURIComponent(encodeURIComponent(meetingUuid));
  
  await axios.delete(
    `https://api.zoom.us/v2/meetings/${encodedUuid}/recordings`,
    {
      params: { action: 'trash' },  // Move to trash (recoverable for 30 days)
      // params: { action: 'delete' }, // Permanent delete
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );
}

// Track what's been archived
const db = require('./db');

async function markAsArchived(meetingUuid, s3Path) {
  await db.recordings.upsert({
    meeting_uuid: meetingUuid,
    s3_path: s3Path,
    archived_at: new Date(),
    deleted_from_zoom: false
  });
}

// Clean up old recordings from Zoom
async function cleanupOldRecordings() {
  const archivedRecordings = await db.recordings.findAll({
    where: {
      archived_at: { $lt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) },
      deleted_from_zoom: false
    }
  });
  
  for (const recording of archivedRecordings) {
    await deleteZoomRecording(recording.meeting_uuid);
    await db.recordings.update(
      { deleted_from_zoom: true },
      { where: { meeting_uuid: recording.meeting_uuid }}
    );
  }
}
```

## Resources

- **Recordings API**: https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Cloud-Recording
- **AWS S3 SDK**: https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/
- **Google Cloud Storage**: https://cloud.google.com/storage/docs/reference/libraries

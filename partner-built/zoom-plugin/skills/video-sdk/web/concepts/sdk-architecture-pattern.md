# SDK Architecture Pattern: Universal Formula

## Overview

The Zoom Video SDK for Web follows a consistent pattern for all features. Once you understand this pattern, you can implement ANY feature.

## The Universal 5-Step Pattern

```
1. Create Client    →  client = ZoomVideo.createClient()
2. Initialize SDK   →  await client.init(language, dependentAssets, options)
3. Join Session     →  await client.join(topic, signature, userName, password)
4. Get Stream       →  stream = client.getMediaStream()  ← ONLY AFTER JOIN!
5. Use Features     →  await stream.startVideo() + client.on('event', handler)
```

## Step-by-Step Breakdown

### Step 1: Create Client (Singleton)

```javascript
import ZoomVideo from '@zoom/videosdk';

// Creates a singleton client - returns same instance if called multiple times
const client = ZoomVideo.createClient();
```

**Key Points:**
- The client is a **singleton** - calling `createClient()` multiple times returns the same instance
- This is the entry point for the entire SDK

### Step 2: Initialize SDK

```javascript
await client.init('en-US', 'Global', { 
  patchJsMedia: true,
  // webrtc: true  // Optional: Enable WebRTC mode for HD
});
```

**Parameters:**
- `language`: Language code (e.g., 'en-US', 'zh-CN')
- `dependentAssets`: Asset source ('Global', 'CDN', 'CN', or custom path)
- `options`: Optional settings

**Asset Sources:**
- `'Global'`: `https://source.zoom.us/videosdk/{version}/lib/` (default)
- `'CDN'`: `https://dmogdx0jrul3u.cloudfront.net/videosdk/{version}/lib/`
- `'CN'`: `https://jssdk.zoomus.cn/videosdk/{version}/lib`
- Custom: Full path to self-hosted assets

### Step 3: Join Session

```javascript
await client.join(topic, signature, userName, password);
```

**Parameters:**
- `topic`: Session name (must match JWT `tpc` value)
- `signature`: Video SDK JWT from server
- `userName`: Display name for the user
- `password`: Optional session password

**Important Notes:**
- Session begins when first user joins
- Host is user with `role=1` in JWT
- Password is required for all users if set by host

### Step 4: Get Stream (CRITICAL TIMING!)

```javascript
// ONLY call after join() completes!
const stream = client.getMediaStream();
```

**THE #1 MISTAKE:**
```javascript
// WRONG - stream will be undefined!
const stream = client.getMediaStream();
await client.join(...);

// CORRECT - get stream after join
await client.join(...);
const stream = client.getMediaStream();
```

### Step 5: Use Features + Listen to Events

```javascript
// Start video
await stream.startVideo();

// Start audio
await stream.startAudio();

// Attach video to DOM
const videoElement = await stream.attachVideo(userId, VideoQuality.Video_360P);
container.appendChild(videoElement);

// CRITICAL: Listen for events
client.on('peer-video-state-change', async (payload) => {
  if (payload.action === 'Start') {
    const element = await stream.attachVideo(payload.userId, VideoQuality.Video_360P);
    container.appendChild(element);
  } else {
    await stream.detachVideo(payload.userId);
  }
});
```

## Complete Working Example

```javascript
import ZoomVideo, { VideoQuality } from '@zoom/videosdk';

// Initialize state
let client = null;
let stream = null;

async function initializeSDK() {
  // Step 1: Create client
  client = ZoomVideo.createClient();
  
  // Step 2: Initialize
  await client.init('en-US', 'Global', { patchJsMedia: true });
  
  console.log('SDK initialized');
}

async function joinSession(topic, signature, userName) {
  // Step 3: Join session
  await client.join(topic, signature, userName);
  
  // Step 4: Get stream (AFTER join!)
  stream = client.getMediaStream();
  
  // Step 5: Set up event listeners
  setupEventListeners();
  
  // Start own media
  await stream.startVideo();
  await stream.startAudio();
  
  // Render own video
  const currentUser = client.getCurrentUserInfo();
  const myVideoElement = await stream.attachVideo(
    currentUser.userId, 
    VideoQuality.Video_360P
  );
  document.getElementById('my-video').appendChild(myVideoElement);
  
  // Render existing participants
  await renderExistingParticipants();
}

function setupEventListeners() {
  // Participant video changes
  client.on('peer-video-state-change', async (payload) => {
    const { action, userId } = payload;
    if (action === 'Start') {
      const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
      document.getElementById(`video-${userId}`).appendChild(element);
    } else {
      await stream.detachVideo(userId);
    }
  });
  
  // New participant joined
  client.on('user-added', (payload) => {
    console.log('User joined:', payload);
    // Create UI container for new user
  });
  
  // Participant left
  client.on('user-removed', (payload) => {
    console.log('User left:', payload);
    // Clean up UI for user
    stream.detachVideo(payload[0].userId);
  });
  
  // Connection state
  client.on('connection-change', (payload) => {
    console.log('Connection state:', payload.state);
  });
}

async function renderExistingParticipants() {
  // Small delay to ensure all participants are loaded
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const users = client.getAllUser();
  const currentUserId = client.getCurrentUserInfo().userId;
  
  for (const user of users) {
    if (user.bVideoOn && user.userId !== currentUserId) {
      const element = await stream.attachVideo(user.userId, VideoQuality.Video_360P);
      document.getElementById(`video-${user.userId}`).appendChild(element);
    }
  }
}

async function leaveSession() {
  await client.leave();
  console.log('Left session');
}

// Usage
initializeSDK().then(() => {
  joinSession('my-session', 'JWT_TOKEN', 'User Name');
});
```

## Feature-Specific Patterns

### Video

```javascript
// Start/stop own camera
await stream.startVideo();
await stream.stopVideo();

// Attach/detach video
const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
await stream.detachVideo(userId);

// Switch camera
await stream.switchCamera(deviceId);
```

### Audio

```javascript
// Start/stop audio
await stream.startAudio();
await stream.stopAudio();

// Mute/unmute
await stream.muteAudio();
await stream.unmuteAudio();

// Switch microphone/speaker
await stream.switchMicrophone(micId);
await stream.switchSpeaker(speakerId);
```

### Screen Share

```javascript
// Start sharing
await stream.startShareScreen(canvas);

// Stop sharing
await stream.stopShareScreen();

// Receive share (event-driven)
client.on('active-share-change', async (payload) => {
  if (payload.state === 'Active') {
    await stream.startShareView(canvas, payload.userId);
  } else {
    await stream.stopShareView();
  }
});
```

### Feature Clients

```javascript
// Chat
const chatClient = client.getChatClient();
await chatClient.send('Hello!');

// Recording
const recordingClient = client.getRecordingClient();
await recordingClient.startCloudRecording();

// Transcription
const transcriptionClient = client.getLiveTranscriptionClient();
await transcriptionClient.startLiveTranscription();

// Command channel
const commandClient = client.getCommandClient();
await commandClient.send(JSON.stringify({ type: 'reaction', emoji: '👍' }));
```

## Error Handling Pattern

```javascript
try {
  await client.join(topic, signature, userName, password);
} catch (error) {
  switch (error.type) {
    case 'INVALID_PARAMETERS':
      console.error('Invalid join parameters:', error.reason);
      break;
    case 'INVALID_OPERATION':
      console.error('Duplicate operation:', error.reason);
      break;
    case 'INTERNAL_ERROR':
      console.error('Service unavailable:', error.reason);
      break;
    default:
      console.error('Join failed:', error);
  }
}
```

## Key Insights

1. **Lifecycle is Strict**: Create → Init → Join → Get Stream
2. **Stream After Join**: NEVER call `getMediaStream()` before `join()` completes
3. **Event-Driven**: Listen for events to render participant videos
4. **Singleton Pattern**: Client is a singleton, Stream is obtained from client
5. **Async Everything**: All SDK operations are async, use await

## Related Documentation

- [Singleton Hierarchy](singleton-hierarchy.md) - 4-level navigation guide
- [Video Rendering](../examples/video-rendering.md) - attachVideo() patterns
- [Event Handling](../examples/event-handling.md) - Required events

---

**TL;DR**: Create client → Init → Join → Get stream → Use + listen to events. The stream is ONLY available after join() completes.

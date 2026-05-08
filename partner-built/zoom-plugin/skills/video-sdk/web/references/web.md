# Video SDK - Web

Build custom video experiences in the browser with Zoom Video SDK.

## Overview

The Zoom Video SDK for Web enables fully customized video applications using Zoom's infrastructure. You control the UI, branding, and user experience.

## Prerequisites

- Video SDK credentials from [Marketplace](https://marketplace.zoom.us/) (sign-in required)
- SDK Key and Secret
- Modern browser (Chrome, Firefox, Safari, Edge)

## Installation

### NPM (Recommended)

```bash
npm install @zoom/videosdk
```

### CDN (Fallback Strategy)

> **Note**: Some networks/ad blockers can block `source.zoom.us`. Prefer allowlisting the domain in managed environments. If you need a fallback, consider mirroring/self-hosting only if permitted and you can keep versions in sync.

```bash
# Download SDK locally
curl "https://source.zoom.us/videosdk/zoom-video-1.12.0.min.js" -o public/js/zoom-video-sdk.min.js
```

```html
<!-- Use local copy instead of CDN -->
<script src="js/zoom-video-sdk.min.js"></script>
```

**Note:** Remember to update your local copy when new SDK versions are released.

## Quick Start

### NPM Usage (Bundler)

```javascript
import ZoomVideo from '@zoom/videosdk';

const client = ZoomVideo.createClient();
await client.init('en-US', 'Global', { patchJsMedia: true });
await client.join(topic, signature, userName, password);

// CRITICAL: getMediaStream() ONLY works AFTER join()
const stream = client.getMediaStream();
await stream.startVideo();
await stream.startAudio();
```

### CDN Usage (No Bundler)

```javascript
// CDN exports as WebVideoSDK, NOT ZoomVideo
// Must use .default property
const ZoomVideo = WebVideoSDK.default;
const client = ZoomVideo.createClient();

await client.init('en-US', 'Global', { patchJsMedia: true });
await client.join(topic, signature, userName, password);

// CRITICAL: getMediaStream() ONLY works AFTER join()
const stream = client.getMediaStream();
await stream.startVideo();
await stream.startAudio();
```

### ES Module with CDN (Race Condition)

When using `<script type="module">` with CDN, the SDK may not be loaded yet:

```javascript
function waitForSDK(timeout = 10000) {
  return new Promise((resolve, reject) => {
    if (typeof WebVideoSDK !== 'undefined') {
      resolve();
      return;
    }
    const start = Date.now();
    const check = setInterval(() => {
      if (typeof WebVideoSDK !== 'undefined') {
        clearInterval(check);
        resolve();
      } else if (Date.now() - start > timeout) {
        clearInterval(check);
        reject(new Error('SDK failed to load'));
      }
    }, 100);
  });
}

// Usage
await waitForSDK();
const ZoomVideo = WebVideoSDK.default;
const client = ZoomVideo.createClient();
```

## SDK Lifecycle (CRITICAL ORDER)

The SDK has a strict lifecycle. Violating it causes **silent failures**.

```
1. Create client:     client = ZoomVideo.createClient()
2. Initialize:        await client.init('en-US', 'Global', options)
3. Join session:      await client.join(topic, signature, userName, password)
4. Get stream:        stream = client.getMediaStream()  ← ONLY AFTER JOIN
5. Start media:       await stream.startVideo() / await stream.startAudio()
```

**Common Mistake:**

```javascript
// ❌ WRONG: Getting stream before joining
const stream = client.getMediaStream();  // Returns undefined!
await client.join(...);

// ✅ CORRECT: Get stream after joining
await client.join(...);
const stream = client.getMediaStream();  // Works!
```

## Video Rendering Best Practices

These show up repeatedly in forum "high CPU", "freezing", and "Safari/Firefox rendering" threads.

- Prefer a single rendering pipeline/control rather than one independent renderer per participant.
- Add videos incrementally and measure CPU/GPU usage.
- Degrade gracefully when `isSupportMultipleVideos()` is false (mobile Safari, lower-end devices).
- Consider lower quality subscriptions for non-active speakers.

## Key Features

### WebRTC Mode

Enable WebRTC mode for direct peer-to-peer streaming with HD video support:

```javascript
await client.init('en-US', 'Global', {
  patchJsMedia: true,
  webrtc: true  // Enable WebRTC mode
});
```

**Benefits:**
- Up to 1080p HD video
- Improved performance for direct streaming

### Virtual Backgrounds

**Check support before using:**

```javascript
const stream = client.getMediaStream();

// Always check support first
if (stream.isSupportVirtualBackground()) {
  // Blur background
  await stream.updateVirtualBackgroundImage('blur');
  
  // Custom image background
  await stream.updateVirtualBackgroundImage('https://example.com/bg.jpg');
  
  // Remove virtual background
  await stream.updateVirtualBackgroundImage(undefined);
} else {
  console.log('Virtual backgrounds not supported on this device');
}
```

### HD Video Resolution

#### Check HD Capability (IMPORTANT)

**Always check if HD is supported before enabling:**

```javascript
const stream = client.getMediaStream();

// Check if 720p is supported
const hdSupported = stream.isSupportHDVideo();
console.log('HD (720p) supported:', hdSupported);

// Get maximum video quality (returns VideoQuality enum)
const maxQuality = stream.getVideoMaxQuality();
// 0=90P, 1=180P, 2=360P, 3=720P, 4=1080P

// Check SharedArrayBuffer (required for HD)
const sabAvailable = typeof SharedArrayBuffer === 'function';
if (!sabAvailable) {
  console.warn('HD requires SharedArrayBuffer - enable COOP/COEP headers');
}
```

#### Enable HD Video

```javascript
// Start video with HD quality (720p)
await stream.startVideo({ hd: true });

// Start video with Full HD (1080p)
await stream.startVideo({ hd: true, fullHd: true });

// Subscribe to specific quality
await stream.attachVideo(userId, VideoQuality.Video_720P);
```

#### Check Multiple Video Support

```javascript
// Check if gallery view is possible
const multipleVideosSupported = stream.isSupportMultipleVideos();

// Get max renderable videos
const maxRenderable = stream.getMaxRenderableVideos();
console.log('Can render up to', maxRenderable, 'videos');
```

#### Complete HD Detection Flow

```javascript
async function checkHDCapability(client) {
  // 1. Check SharedArrayBuffer
  const sabAvailable = typeof SharedArrayBuffer === 'function';
  
  // 2. Check system requirements
  const compatibility = ZoomVideo.checkSystemRequirements();
  
  // 3. Check feature requirements
  const features = ZoomVideo.checkFeatureRequirements();
  
  // 4. After joining, check stream capabilities
  const stream = client.getMediaStream();
  
  return {
    sharedArrayBuffer: sabAvailable,
    videoCompatible: compatibility.video,
    hdSupported: stream.isSupportHDVideo(),
    maxQuality: stream.getVideoMaxQuality(),
    maxRenderable: stream.getMaxRenderableVideos(),
    multipleVideos: stream.isSupportMultipleVideos(),
    virtualBackground: stream.isSupportVirtualBackground()
  };
}
```

**Resolution tiers:**
- 1:1 calls: Up to 1080p
- Small groups: Up to 720p
- Larger sessions: Adaptive

**Concurrent HD limits:**
- Max 2 concurrent 720p subscriptions
- Max 1 concurrent 1080p render

### Rendering Modes

Multiple rendering options available:
- WebRTC mode (direct streaming)
- WebAssembly mode (default)
- Canvas rendering
- Video element rendering

## Video Processor (Custom Effects)

The `VideoProcessor` class allows you to intercept and modify video frames before transmission. Use this for custom overlays, effects, face detection, and more.

### How It Works

1. Create a video processor worker
2. Extend `VideoProcessor` class
3. Implement `processFrame()` to modify each frame
4. Output to `OffscreenCanvas`

### Basic Example

```javascript
// video-processor-worker.js
class MyVideoProcessor extends VideoProcessor {
  constructor(port, options) {
    super(port, options);
  }

  processFrame(input, output) {
    const ctx = output.getContext('2d');
    
    // Draw original frame
    ctx.drawImage(input, 0, 0);
    
    // Add overlay (e.g., text, graphics)
    ctx.fillStyle = 'white';
    ctx.font = '24px Arial';
    ctx.fillText('Live', 20, 40);
    
    return true;
  }
}
```

### Face Detection with face-api.js

Combine VideoProcessor with face-api.js for face detection overlays:

```javascript
// video-processor-worker.js
import * as faceapi from 'face-api.js';

class FaceDetectionProcessor extends VideoProcessor {
  async processFrame(input, output) {
    const ctx = output.getContext('2d');
    
    // Draw original frame
    ctx.drawImage(input, 0, 0);
    
    // Detect faces
    const detections = await faceapi.detectAllFaces(input);
    
    // Draw bounding boxes
    detections.forEach(detection => {
      const box = detection.box;
      ctx.strokeStyle = '#00ff00';
      ctx.lineWidth = 2;
      ctx.strokeRect(box.x, box.y, box.width, box.height);
    });
    
    return true;
  }
}
```

### Use Cases

| Use Case | Description |
|----------|-------------|
| Face detection | Bounding boxes, landmarks |
| AR effects | Glasses, hats, masks |
| Beauty filters | Skin smoothing, color correction |
| Overlays | Text, logos, watermarks |
| Real-time translation | OCR + translation overlay |

### Resources

- **VideoProcessor API**: https://marketplacefront.zoom.us/sdk/custom/web/classes/VideoProcessor.html
- **Zoom Blog - AI Text Translation**: https://developers.zoom.us/blog/ai-text-translator-with-videosdk-share-processor/

## Video Rendering (CRITICAL - Event Driven)

The SDK is **event-driven**. You must listen for events and render/detach videos accordingly.

### Use `attachVideo()` NOT `renderVideo()` 

`renderVideo()` is **deprecated**. Use `attachVideo()` which returns a VideoPlayer element to append to DOM.

```javascript
import { VideoQuality } from '@zoom/videosdk';

const stream = client.getMediaStream();

// Start your camera
await stream.startVideo();

// Attach video - returns a VideoPlayer element
const videoElement = await stream.attachVideo(userId, VideoQuality.Video_360P);

// Append to your container
document.getElementById('video-container').appendChild(videoElement);
```

### VideoQuality Enum

```javascript
import { VideoQuality } from '@zoom/videosdk';

VideoQuality.Video_90P   // 0
VideoQuality.Video_180P  // 1
VideoQuality.Video_360P  // 2 (recommended for most cases)
VideoQuality.Video_720P  // 3
VideoQuality.Video_1080P // 4
```

### Detach Video

```javascript
// Detach and remove from DOM
const elements = await stream.detachVideo(userId);
if (Array.isArray(elements)) {
  elements.forEach(e => e.remove());
} else {
  elements.remove();
}
```

### Required Events to Listen

**You MUST listen to these events to properly render participant videos:**

```javascript
// When another participant's video state changes
client.on('peer-video-state-change', async (payload) => {
  const { action, userId } = payload;
  
  if (action === 'Start') {
    // Participant turned on video - attach it
    const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
    container.appendChild(element);
  } else if (action === 'Stop') {
    // Participant turned off video - detach it
    await stream.detachVideo(userId);
  }
});

// When participants join/leave
client.on('user-added', (payload) => {
  // New participant joined - check if their video is on
  const users = client.getAllUser();
  // Render videos for users with bVideoOn === true
});

client.on('user-removed', (payload) => {
  // Participant left - clean up their video element
  const { userId } = payload;
  stream.detachVideo(userId);
});

// Participant state updates (mute, video, etc)
client.on('user-updated', (payload) => {
  // Re-check participant states
  const users = client.getAllUser();
});
```

### Participant Properties

```javascript
const users = client.getAllUser();

users.forEach(user => {
  user.userId      // Unique user ID
  user.displayName // User's display name
  user.bVideoOn    // Boolean - is video enabled?
  user.muted       // Boolean - is audio muted?
  user.audio       // '' | 'computer' | 'phone'
});
```

### Complete React Pattern

```typescript
// When your video turns on
useEffect(() => {
  if (isVideoOn && stream && currentUserId) {
    const attach = async () => {
      const element = await stream.attachVideo(currentUserId, VideoQuality.Video_360P);
      containerRef.current?.appendChild(element);
    };
    attach();
  }
}, [isVideoOn, stream, currentUserId]);

// Listen for other participants
useEffect(() => {
  if (!client) return;
  
  const handleVideoChange = async (payload) => {
    const { action, userId } = payload;
    if (action === 'Start') {
      const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
      // Append to appropriate container
    } else {
      await stream.detachVideo(userId);
    }
  };
  
  client.on('peer-video-state-change', handleVideoChange);
  return () => client.off('peer-video-state-change', handleVideoChange);
}, [client, stream]);
```

### Legacy: renderVideo (Deprecated)

> **Note**: `renderVideo()` is deprecated. Use `attachVideo()` instead.

If you must use canvas rendering:

### Canvas Must Exist in DOM

```javascript
// CORRECT: Canvas exists before rendering
const canvas = document.getElementById('my-canvas');  // Already in DOM
await stream.renderVideo(canvas, userId, 640, 360, 0, 0, 3);

// WRONG: Creating canvas but not adding to DOM
const canvas = document.createElement('canvas');
await stream.renderVideo(canvas, userId);  // Won't display!
```

### Use Single Rendering Control (IMPORTANT)

**For performance, use ONE shared rendering control for all video streams, NOT one control per video.**

```javascript
// CORRECT: Single video container for all participants
const videoContainer = document.getElementById('video-container');
const stream = client.getMediaStream();

// Render all participants to the same container
await stream.renderVideo(videoContainer, userId, width, height, x, y, quality);
```

```javascript
// WRONG: Creating separate controls per participant
// This degrades performance significantly!
participants.forEach(p => {
  const container = document.createElement('div');  // DON'T do this
  stream.renderVideo(container, p.id, ...);
});
```

**Why:**
- Multiple rendering controls consume excessive resources
- Performance degrades significantly with more participants
- Single control handles internal layout management efficiently

## Peer Video on Mid-Session Join (IMPORTANT)

**Existing participants' videos won't auto-render when you join mid-session.**

You must manually iterate all users and attach their video:

```javascript
import { VideoQuality } from '@zoom/videosdk';

// After joining, render existing participants' videos
const renderExistingVideos = async () => {
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const stream = client.getMediaStream();
  const users = client.getAllUser();
  const currentUserId = client.getCurrentUserInfo().userId;
  
  for (const user of users) {
    if (user.bVideoOn && user.userId !== currentUserId) {
      const element = await stream.attachVideo(user.userId, VideoQuality.Video_360P);
      document.getElementById(`video-${user.userId}`).appendChild(element);
    }
  }
};
```

**Key points:**
- Check `user.bVideoOn` to see if video is enabled
- Skip self (`client.getCurrentUserInfo().userId`)
- Add ~500ms delay after join before rendering
- Use `attachVideo()` not `renderVideo()`

## SharedArrayBuffer

For optimal performance, configure these headers on your server:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

**Note:** As of v1.11.2, SharedArrayBuffer is elective (not strictly required).

## Event Handling (CRITICAL)

**The SDK is event-driven. You MUST listen for these events:**

```javascript
// Participant joined
client.on('user-added', (payload) => {
  console.log('User joined:', payload);
  // payload contains user info
});

// Participant left
client.on('user-removed', (payload) => {
  console.log('User left:', payload);
  // Clean up their video element
  stream.detachVideo(payload.userId);
});

// Participant state changed (mute, video, etc)
client.on('user-updated', (payload) => {
  console.log('User updated:', payload);
});

// CRITICAL: Other participant's video turned on/off
client.on('peer-video-state-change', async (payload) => {
  const { action, userId } = payload;
  // action: 'Start' | 'Stop'
  
  if (action === 'Start') {
    const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
    // Append element to container
  } else {
    await stream.detachVideo(userId);
  }
});

// Connection state changed
client.on('connection-change', (payload) => {
  // payload.state: 'Connected' | 'Closed' | 'Reconnecting' | etc
});
```

### Event Cleanup

Always remove listeners when component unmounts:

```javascript
// React pattern
useEffect(() => {
  const handler = (payload) => { /* ... */ };
  client.on('peer-video-state-change', handler);
  
  return () => {
    client.off('peer-video-state-change', handler);
  };
}, [client]);
```

## Common Tasks

### Start/Stop Video
```javascript
await stream.startVideo();
await stream.stopVideo();
```

### Start/Stop Audio
```javascript
await stream.startAudio();
await stream.muteAudio();
await stream.unmuteAudio();
```

### Screen Sharing

#### Receive Screen Share

Listen to `active-share-change` event and render when active:

```javascript
client.on('active-share-change', async (payload) => {
  const stream = client.getMediaStream();
  
  if (payload.state === 'Active') {
    // Add small delay to ensure DOM element exists
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Check if should use video element or canvas
    if (stream.isStartShareScreenWithVideoElement()) {
      const video = document.getElementById('share-video');
      await stream.startShareView(video as unknown as HTMLCanvasElement, payload.userId);
    } else {
      const canvas = document.getElementById('share-canvas');
      await stream.startShareView(canvas, payload.userId);
    }
  } else if (payload.state === 'Inactive') {
    await stream.stopShareView();
  }
});
```

#### Send Screen Share

Check rendering mode before starting:

```javascript
const stream = client.getMediaStream();

// Check which element type to use
if (stream.isStartShareScreenWithVideoElement()) {
  // Use video element
  const video = document.getElementById('share-video');
  await stream.startShareScreen(video as unknown as HTMLCanvasElement);
} else {
  // Use canvas element
  const canvas = document.getElementById('share-canvas');
  await stream.startShareScreen(canvas);
}
```

#### Stop Screen Share

```javascript
await stream.stopShareScreen();
```

#### Type Casting Workaround

SDK types expect `HTMLCanvasElement` even for video elements. Cast when needed:

```typescript
// When using HTMLVideoElement where SDK expects HTMLCanvasElement
const video = document.getElementById('share-video') as HTMLVideoElement;
await stream.startShareView(video as unknown as HTMLCanvasElement, userId);
```

## Host vs Participant

```javascript
// Leave session (others stay)
await client.leave();

// End session for ALL participants (host only)
await client.leave(true);
```

## Chat Implementation

### Initialize Chat

```javascript
const chatClient = client.getChatClient();

// Wait for chat to be ready
chatClient.on('chat-on', () => {
  console.log('Chat is ready');
});
```

### Send Message

```javascript
// Send to everyone
await chatClient.send('Hello, everyone!');

// Send to specific user
await chatClient.sendToUser(userId, 'Private message');
```

### Receive Messages

```javascript
chatClient.on('chat-on-message', (payload) => {
  const { message, sender, timestamp } = payload;
  console.log(`${sender.name}: ${message}`);
});
```

## Error Handling

### Common Join Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid signature` | JWT expired or malformed | Generate new signature |
| `Session does not exist` | Host hasn't started yet | Show "waiting" message, retry |
| `Permission denied` | User denied camera/mic | Request permission again |

### Example Error Handler

```javascript
try {
  await client.join(topic, signature, userName, password);
} catch (error) {
  if (error.reason?.includes('signature')) {
    // Regenerate signature and retry
  } else if (error.reason?.includes('Session')) {
    // Show "Waiting for host..." and poll
  } else if (error.reason?.includes('Permission')) {
    // Guide user to enable permissions
  }
  console.error('Join failed:', error);
}
```

## Recording (Host Only)

Only the host (role=1) can start/stop recording:

```javascript
const recordingClient = client.getRecordingClient();

// Start cloud recording
await recordingClient.startCloudRecording();

// Stop recording
await recordingClient.stopCloudRecording();

// Listen for recording status changes
client.on('recording-change', (payload) => {
  console.log('Recording status:', payload.status);
});
```

## Live Transcription

```javascript
const transcriptionClient = client.getLiveTranscriptionClient();

// Start live transcription
await transcriptionClient.startLiveTranscription();

// Stop live transcription
await transcriptionClient.stopLiveTranscription();

// Listen for captions
client.on('caption-message', (payload) => {
  console.log(`${payload.displayName}: ${payload.text}`);
});
```

## Device Selection

```javascript
// Get available devices
const devices = await ZoomVideo.getDevices();
console.log('Cameras:', devices.cameras);
console.log('Microphones:', devices.microphones);
console.log('Speakers:', devices.speakers);

// Get currently active devices
const stream = client.getMediaStream();
const activeCamera = stream.getActiveCamera();
const activeMic = stream.getActiveMicrophone();
const activeSpeaker = stream.getActiveSpeaker();

// Switch devices
await stream.switchCamera(deviceId);
await stream.switchMicrophone(deviceId);
await stream.switchSpeaker(deviceId);
```

## Network Quality

Monitor network quality in real-time:

```javascript
client.on('network-quality-change', (payload) => {
  // payload.type = 'uplink' or 'downlink'
  // payload.level = 0-5 (5 is best)
  
  if (payload.level < 2) {
    console.warn(`Poor ${payload.type} network quality: ${payload.level}`);
  }
});
```

## File Sharing

```javascript
const chatClient = client.getChatClient();

// Send file to everyone (receiverId = 0)
await chatClient.sendFile(file, 0);

// Send file to specific user
await chatClient.sendFile(file, userId);
```

## Breakout Rooms (Subsessions)

Video SDK uses "Subsessions" instead of native breakout rooms:

```javascript
const subsessionClient = client.getSubsessionClient();

// Create subsessions
const roomNames = ['Room 1', 'Room 2', 'Room 3'];
await subsessionClient.createSubsessions(roomNames);

// Open subsessions
const rooms = subsessionClient.getSubsessionList();
await subsessionClient.openSubsessions(rooms);

// Broadcast message to all rooms
await subsessionClient.broadcast('Please return to main session in 5 minutes');

// Close all subsessions
await subsessionClient.closeAllSubsessions();
```

## Reactions via Command Channel

Use the command channel for custom messages like reactions:

```javascript
const commandClient = client.getCommandClient();

// Send reaction
const reaction = { type: 'reaction', emoji: '👍' };
await commandClient.send(JSON.stringify(reaction));

// Receive reactions
client.on('command-channel-message', (payload) => {
  try {
    const data = JSON.parse(payload.text);
    if (data.type === 'reaction') {
      console.log(`${payload.senderName} reacted with ${data.emoji}`);
    }
  } catch (e) {
    console.log('Non-JSON message:', payload.text);
  }
});
```

## CORS Errors (Telemetry)

**CORS errors to `log-external-gateway.zoom.us` are harmless.**

These are caused by COOP/COEP headers blocking telemetry requests. They don't affect SDK functionality.

```
// These console errors can be safely ignored:
// Access to fetch at 'https://log-external-gateway.zoom.us/...' has been blocked by CORS policy
```

## Resources

- **Official docs**: https://developers.zoom.us/docs/video-sdk/web/
- **API Reference**: https://marketplacefront.zoom.us/sdk/custom/web/modules.html
- **Sample app**: https://github.com/zoom/videosdk-web-sample

## Host Participant Management

```javascript
const stream = client.getMediaStream();

// Mute all participants
await stream.muteAllAudio();

// Mute/unmute specific participant
await stream.muteAudio(userId);
await stream.unmuteAudio(userId);

// Remove participant (host only)
await client.removeUser(userId);

// Transfer host
await client.makeHost(userId);

// Make co-host
await client.makeManager(userId);
```

## Mirror Self View

```javascript
const stream = client.getMediaStream();

// Toggle mirror (useful for self-view)
await stream.mirrorVideo(true);   // Enable mirror
await stream.mirrorVideo(false);  // Disable mirror
```

## Share Screen with Audio

```javascript
const stream = client.getMediaStream();
const shareElement = document.getElementById('share-element');

// Share with system audio
await stream.startShareScreen(shareElement, { 
  secondaryAudio: true 
});
```

## Troubleshooting

### "ZoomVideo is not defined" / "WebVideoSDK is not defined"

**Causes:**
1. Ad blocker blocking `source.zoom.us` CDN
2. ES module loading before SDK script

**Solutions:**
1. Allowlist `source.zoom.us` in your environment, or use a permitted fallback (mirror/self-host) if you can keep versions in sync
2. Use `waitForSDK()` function for ES modules

### Camera/Microphone Not Working

**Causes:**
1. Browser permission denied
2. Device in use by another app
3. No hardware available

**Solutions:**
1. Check browser permissions (Settings → Privacy → Camera/Microphone)
2. Close other apps using the device
3. Try different browser

### Video Not Displaying (Silent Failure)

**Cause:** Called `getMediaStream()` before `join()` completed

**Solution:** Follow the SDK lifecycle order exactly (see SDK Lifecycle section)

### CORS Error on Signature Endpoint

**Cause:** Frontend (HTTPS) calling backend (HTTP) or different origin

**Solutions:**
1. Use nginx proxy to same origin (recommended)
2. Configure CORS on backend with explicit origins
3. Ensure both frontend and backend use HTTPS

### Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Video | ✅ 80+ | ✅ 75+ | ✅ 14+ | ✅ 80+ |
| Audio | ✅ 80+ | ✅ 75+ | ✅ 14+ | ✅ 80+ |
| Screen Share | ✅ 80+ | ✅ 75+ | ⚠️ 15+ | ✅ 80+ |
| Virtual BG | ✅ 80+ | ✅ 90+ | ❌ | ✅ 80+ |

**Safari Notes:**
- Virtual background not supported
- Screen sharing requires macOS 15+

# Session Join Pattern

Complete working example for joining a Zoom Video SDK session.

## Prerequisites

1. Video SDK credentials from [Marketplace](https://marketplace.zoom.us/)
2. JWT token generated server-side
3. Modern browser (Chrome 80+, Firefox 75+, Safari 14+, Edge 80+)

## Complete Example

```javascript
import ZoomVideo, { VideoQuality } from '@zoom/videosdk';

// State
let client = null;
let stream = null;

// Configuration
const config = {
  language: 'en-US',
  dependentAssets: 'Global',  // or 'CDN', 'CN', or custom path
  options: {
    patchJsMedia: true,
    // webrtc: true,  // Enable for HD video
  }
};

/**
 * Initialize the SDK (call once)
 */
async function initializeSDK() {
  // Step 1: Create client (singleton)
  client = ZoomVideo.createClient();
  
  // Optional: Check compatibility first
  const compatibility = ZoomVideo.checkSystemRequirements();
  if (!compatibility.video || !compatibility.audio) {
    throw new Error('Browser not compatible');
  }
  
  // Step 2: Initialize
  await client.init(config.language, config.dependentAssets, config.options);
  
  console.log('SDK initialized successfully');
  return client;
}

/**
 * Join a session
 * @param {string} topic - Session name (must match JWT tpc)
 * @param {string} signature - Video SDK JWT from server
 * @param {string} userName - Display name
 * @param {string} password - Optional session password
 */
async function joinSession(topic, signature, userName, password = '') {
  try {
    // Step 3: Join session
    await client.join(topic, signature, userName, password);
    
    // Step 4: Get stream (ONLY AFTER JOIN!)
    stream = client.getMediaStream();
    
    // Step 5: Set up event listeners
    setupEventListeners();
    
    // Step 6: Get current user info
    const currentUser = client.getCurrentUserInfo();
    console.log('Joined as:', currentUser.displayName, 'ID:', currentUser.userId);
    
    return { client, stream, currentUser };
  } catch (error) {
    handleJoinError(error);
    throw error;
  }
}

/**
 * Set up all required event listeners
 */
function setupEventListeners() {
  // Connection state changes
  client.on('connection-change', (payload) => {
    console.log('Connection state:', payload.state);
    
    if (payload.state === 'Closed') {
      console.log('Disconnected. Reason:', payload.reason);
      cleanup();
    }
    
    if (payload.state === 'Reconnecting') {
      console.log('Reconnecting...', payload.reason);
    }
  });
  
  // New participant joined
  client.on('user-added', (payload) => {
    console.log('User(s) joined:', payload.map(u => u.displayName));
    // Create UI containers for new users
  });
  
  // Participant left
  client.on('user-removed', (payload) => {
    console.log('User(s) left:', payload.map(u => u.displayName));
    // Clean up UI for users
    payload.forEach(user => {
      stream.detachVideo(user.userId);
    });
  });
  
  // Participant updated (name, mute, etc.)
  client.on('user-updated', (payload) => {
    console.log('User(s) updated:', payload);
    // Update UI state
  });
  
  // Peer video state change (CRITICAL for rendering)
  client.on('peer-video-state-change', async (payload) => {
    const { action, userId } = payload;
    console.log(`User ${userId} video: ${action}`);
    
    if (action === 'Start') {
      const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
      document.getElementById(`video-${userId}`)?.appendChild(element);
    } else {
      await stream.detachVideo(userId);
    }
  });
  
  // Audio changes
  client.on('current-audio-change', (payload) => {
    console.log('Audio change:', payload.action, payload.type);
  });
  
  // Active speaker
  client.on('active-speaker', (payload) => {
    if (payload.length > 0) {
      console.log('Active speaker:', payload[0].userId);
    }
  });
}

/**
 * Start media after joining
 */
async function startMedia() {
  // Start video
  try {
    await stream.startVideo();
    console.log('Video started');
    
    // Attach own video
    const currentUser = client.getCurrentUserInfo();
    const myVideoElement = await stream.attachVideo(
      currentUser.userId, 
      VideoQuality.Video_360P
    );
    document.getElementById('my-video')?.appendChild(myVideoElement);
  } catch (error) {
    console.error('Failed to start video:', error);
  }
  
  // Start audio
  try {
    await stream.startAudio();
    console.log('Audio started');
  } catch (error) {
    console.error('Failed to start audio:', error);
  }
  
  // Render existing participants (for mid-session join)
  await renderExistingParticipants();
}

/**
 * Render videos of participants who joined before us
 */
async function renderExistingParticipants() {
  // Small delay to ensure all participants are loaded
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const users = client.getAllUser();
  const currentUserId = client.getCurrentUserInfo().userId;
  
  for (const user of users) {
    if (user.bVideoOn && user.userId !== currentUserId) {
      const element = await stream.attachVideo(user.userId, VideoQuality.Video_360P);
      document.getElementById(`video-${user.userId}`)?.appendChild(element);
    }
  }
}

/**
 * Handle join errors
 */
function handleJoinError(error) {
  console.error('Join error:', error);
  
  const errorMessage = error.reason || error.message || 'Unknown error';
  
  if (errorMessage.includes('signature')) {
    console.error('Invalid signature - regenerate JWT');
  } else if (errorMessage.includes('Session')) {
    console.error('Session not found - host may not have started');
  } else if (errorMessage.includes('password')) {
    console.error('Invalid password');
  } else if (errorMessage.includes('Permission')) {
    console.error('Permission denied - check camera/mic access');
  }
}

/**
 * Leave the session
 * @param {boolean} end - If true, ends session for all (host only)
 */
async function leaveSession(end = false) {
  try {
    await client.leave(end);
    console.log(end ? 'Session ended' : 'Left session');
    cleanup();
  } catch (error) {
    console.error('Leave error:', error);
  }
}

/**
 * Clean up resources
 */
function cleanup() {
  stream = null;
  // Remove event listeners, clear UI, etc.
}

// Usage
async function main() {
  await initializeSDK();
  
  const { currentUser } = await joinSession(
    'my-session-topic',
    'YOUR_JWT_TOKEN',
    'User Name'
  );
  
  await startMedia();
  
  console.log('Ready! User:', currentUser.displayName);
}

main().catch(console.error);
```

## CDN Version

```html
<!DOCTYPE html>
<html>
<head>
  <title>Zoom Video SDK</title>
  <!-- Some environments/ad blockers may block source.zoom.us. Allowlist or use a permitted fallback strategy. -->
  <script src="js/zoom-video-sdk.min.js"></script>
</head>
<body>
  <div id="my-video"></div>
  <div id="participants"></div>
  
  <script>
    // CDN exports as WebVideoSDK.default
    const ZoomVideo = WebVideoSDK.default;
    
    const client = ZoomVideo.createClient();
    let stream;
    
    async function init() {
      await client.init('en-US', 'Global', { patchJsMedia: true });
      await client.join('topic', 'JWT', 'User');
      stream = client.getMediaStream();
      
      // Set up events and start media
      // ... (same as NPM version)
    }
    
    init();
  </script>
</body>
</html>
```

## React Example

```typescript
import React, { useEffect, useRef, useState } from 'react';
import ZoomVideo, { VideoClient, Stream, VideoQuality } from '@zoom/videosdk';

interface Props {
  topic: string;
  signature: string;
  userName: string;
}

export const VideoSession: React.FC<Props> = ({ topic, signature, userName }) => {
  const [client, setClient] = useState<typeof VideoClient | null>(null);
  const [stream, setStream] = useState<typeof Stream | null>(null);
  const [isJoined, setIsJoined] = useState(false);
  const videoContainerRef = useRef<HTMLDivElement>(null);
  
  // Initialize SDK
  useEffect(() => {
    const init = async () => {
      const zmClient = ZoomVideo.createClient();
      await zmClient.init('en-US', 'Global', { patchJsMedia: true });
      setClient(zmClient);
    };
    init();
    
    return () => {
      ZoomVideo.destroyClient();
    };
  }, []);
  
  // Join session
  useEffect(() => {
    if (!client || isJoined) return;
    
    const join = async () => {
      await client.join(topic, signature, userName);
      const mediaStream = client.getMediaStream();
      setStream(mediaStream);
      setIsJoined(true);
    };
    join();
  }, [client, topic, signature, userName, isJoined]);
  
  // Set up event listeners
  useEffect(() => {
    if (!client || !stream) return;
    
    const handleVideoChange = async (payload: { action: string; userId: number }) => {
      const { action, userId } = payload;
      if (action === 'Start') {
        const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
        videoContainerRef.current?.appendChild(element);
      } else {
        await stream.detachVideo(userId);
      }
    };
    
    client.on('peer-video-state-change', handleVideoChange);
    
    return () => {
      client.off('peer-video-state-change', handleVideoChange);
    };
  }, [client, stream]);
  
  // Start own video
  useEffect(() => {
    if (!stream) return;
    
    const startVideo = async () => {
      await stream.startVideo();
      const currentUser = client!.getCurrentUserInfo();
      const element = await stream.attachVideo(currentUser.userId, VideoQuality.Video_360P);
      videoContainerRef.current?.appendChild(element);
    };
    startVideo();
  }, [stream, client]);
  
  return (
    <div>
      <div ref={videoContainerRef} className="video-container" />
      <button onClick={() => client?.leave()}>Leave</button>
    </div>
  );
};
```

## Key Points

1. **Lifecycle order**: `createClient() → init() → join() → getMediaStream()`
2. **Stream timing**: ONLY call `getMediaStream()` after `join()` completes
3. **Event-driven**: Set up event listeners to handle participant video
4. **Mid-session join**: Manually render existing participants' videos
5. **Error handling**: Handle join errors gracefully

## Related Documentation

- [Video Rendering](video-rendering.md) - attachVideo patterns
- [Event Handling](event-handling.md) - Required events
- [Common Issues](../troubleshooting/common-issues.md) - Troubleshooting

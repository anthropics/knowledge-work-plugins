# Video Rendering

Complete guide to rendering video using `attachVideo()` in the Zoom Video SDK for Web.

## Critical Rule

**NEVER use `renderVideo()` - it's deprecated. Always use `attachVideo()`.**

## VideoQuality Enum

```typescript
import { VideoQuality } from '@zoom/videosdk';

// Available quality levels (value = numeric enum)
VideoQuality.Video_90P   // 0 - Thumbnail
VideoQuality.Video_180P  // 1 - Low quality
VideoQuality.Video_360P  // 2 - Standard (recommended default)
VideoQuality.Video_720P  // 3 - HD
VideoQuality.Video_1080P // 4 - Full HD (requires webrtc mode)
```

## Basic Video Rendering

### Start and Render Own Video

```javascript
import ZoomVideo, { VideoQuality } from '@zoom/videosdk';

const client = ZoomVideo.createClient();
let stream;

async function startOwnVideo() {
  // Ensure you're joined first
  stream = client.getMediaStream();
  
  // Step 1: Start capturing video
  await stream.startVideo();
  
  // Step 2: Get current user ID
  const currentUser = client.getCurrentUserInfo();
  
  // Step 3: Attach video to DOM
  const videoElement = await stream.attachVideo(
    currentUser.userId,
    VideoQuality.Video_360P
  );
  
  // Step 4: Add to container
  document.getElementById('my-video-container').appendChild(videoElement);
}
```

### Render Remote Participant Video

```javascript
// Listen for remote video state changes
client.on('peer-video-state-change', async (payload) => {
  const { action, userId } = payload;
  
  if (action === 'Start') {
    // Remote user started video - render it
    const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
    
    // Add to their video container
    const container = document.getElementById(`video-${userId}`);
    if (container) {
      container.appendChild(element);
    }
  } else if (action === 'Stop') {
    // Remote user stopped video - remove element
    await stream.detachVideo(userId);
    
    // Clean up DOM
    const container = document.getElementById(`video-${userId}`);
    if (container) {
      container.innerHTML = '';
    }
  }
});
```

## Mid-Session Join: Rendering Existing Participants

When you join a session that already has participants with video on, you won't receive `peer-video-state-change` events for them. You must manually render their videos.

```javascript
async function renderExistingParticipants() {
  // Wait a moment for participant list to populate
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const participants = client.getAllUser();
  const currentUserId = client.getCurrentUserInfo().userId;
  
  for (const participant of participants) {
    // Skip self
    if (participant.userId === currentUserId) continue;
    
    // Check if they have video on
    if (participant.bVideoOn) {
      const element = await stream.attachVideo(
        participant.userId,
        VideoQuality.Video_360P
      );
      
      const container = document.getElementById(`video-${participant.userId}`);
      if (container) {
        container.appendChild(element);
      }
    }
  }
}

// Call after joining and starting your own video
await startOwnVideo();
await renderExistingParticipants();
```

## Quality Selection Strategy

```javascript
// Determine quality based on use case
function getQualityForLayout(totalParticipants, isSpotlight = false) {
  if (isSpotlight) {
    // Spotlighted/active speaker - highest quality
    return VideoQuality.Video_720P;
  }
  
  if (totalParticipants <= 4) {
    // Small meeting - good quality for all
    return VideoQuality.Video_360P;
  }
  
  if (totalParticipants <= 9) {
    // Medium meeting - balanced quality
    return VideoQuality.Video_180P;
  }
  
  // Large meeting - thumbnails
  return VideoQuality.Video_90P;
}

// Dynamic quality adjustment
async function updateVideoQualities() {
  const participants = client.getAllUser().filter(p => p.bVideoOn);
  const quality = getQualityForLayout(participants.length);
  
  for (const participant of participants) {
    // Re-attach with new quality
    await stream.detachVideo(participant.userId);
    const element = await stream.attachVideo(participant.userId, quality);
    
    const container = document.getElementById(`video-${participant.userId}`);
    if (container) {
      container.innerHTML = '';
      container.appendChild(element);
    }
  }
}
```

## HD Video (720P/1080P)

To use HD video, enable WebRTC mode during initialization:

```javascript
await client.init('en-US', 'Global', {
  patchJsMedia: true,
  webrtc: true,  // Required for HD video
});

// Now you can use higher qualities
const element = await stream.attachVideo(userId, VideoQuality.Video_720P);

// Check if HD is supported on this device
if (stream.isSupportHDVideo()) {
  const hdElement = await stream.attachVideo(userId, VideoQuality.Video_1080P);
}
```

## Multiple Video Rendering

Check device capability for rendering multiple videos:

```javascript
// Check max renderable videos
const maxVideos = stream.getMaxRenderableVideos();
console.log('Can render up to', maxVideos, 'videos');

// Check if multiple video rendering is supported
if (stream.isSupportMultipleVideos()) {
  // Can render multiple participant videos
} else {
  // Limited to fewer simultaneous videos
  // Consider using active speaker mode
}
```

## Detaching Video

```javascript
// Detach specific user's video
const elements = await stream.detachVideo(userId);

// elements can be a single element or array
if (Array.isArray(elements)) {
  elements.forEach(el => el.remove());
} else {
  elements.remove();
}

// Detach from specific element
const specificElement = document.querySelector(`#video-${userId} video-player`);
await stream.detachVideo(userId, specificElement);
```

## Mirror Self Video

```javascript
// Mirror your own video (selfie mode)
await stream.mirrorVideo(true);

// Check current mirror state
const isMirrored = stream.isVideoMirrored();
```

## Stop Video

```javascript
// Stop capturing video (turns off camera)
await stream.stopVideo();

// The attached video element will show black/placeholder
// Detach to clean up
const currentUser = client.getCurrentUserInfo();
await stream.detachVideo(currentUser.userId);
```

## Complete React Component

```typescript
import React, { useEffect, useRef, useState } from 'react';
import ZoomVideo, { VideoClient, Stream, VideoQuality } from '@zoom/videosdk';

interface VideoTileProps {
  userId: number;
  stream: typeof Stream;
  quality?: VideoQuality;
}

export const VideoTile: React.FC<VideoTileProps> = ({ 
  userId, 
  stream, 
  quality = VideoQuality.Video_360P 
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isAttached, setIsAttached] = useState(false);

  useEffect(() => {
    let mounted = true;

    const attachVideo = async () => {
      if (!containerRef.current || !stream) return;

      try {
        const element = await stream.attachVideo(userId, quality);
        if (mounted && containerRef.current) {
          containerRef.current.innerHTML = '';
          containerRef.current.appendChild(element);
          setIsAttached(true);
        }
      } catch (error) {
        console.error('Failed to attach video:', error);
      }
    };

    attachVideo();

    return () => {
      mounted = false;
      if (isAttached) {
        stream.detachVideo(userId).catch(console.error);
      }
    };
  }, [userId, stream, quality, isAttached]);

  return (
    <div 
      ref={containerRef} 
      className="video-tile"
      style={{ width: '100%', height: '100%', background: '#1a1a1a' }}
    />
  );
};

// Usage in parent component
export const VideoGrid: React.FC<{ client: typeof VideoClient; stream: typeof Stream }> = ({ 
  client, 
  stream 
}) => {
  const [participants, setParticipants] = useState<any[]>([]);

  useEffect(() => {
    // Initial load
    setParticipants(client.getAllUser().filter(p => p.bVideoOn));

    // Listen for changes
    const handleVideoChange = async (payload: { action: string; userId: number }) => {
      if (payload.action === 'Start') {
        setParticipants(prev => {
          const user = client.getUser(payload.userId);
          if (user && !prev.find(p => p.userId === payload.userId)) {
            return [...prev, user];
          }
          return prev;
        });
      } else {
        setParticipants(prev => prev.filter(p => p.userId !== payload.userId));
      }
    };

    client.on('peer-video-state-change', handleVideoChange);

    return () => {
      client.off('peer-video-state-change', handleVideoChange);
    };
  }, [client]);

  const quality = participants.length <= 4 
    ? VideoQuality.Video_360P 
    : VideoQuality.Video_180P;

  return (
    <div className="video-grid">
      {participants.map(p => (
        <VideoTile 
          key={p.userId} 
          userId={p.userId} 
          stream={stream} 
          quality={quality}
        />
      ))}
    </div>
  );
};
```

## Error Handling

```javascript
async function safeAttachVideo(userId, quality) {
  try {
    const element = await stream.attachVideo(userId, quality);
    return element;
  } catch (error) {
    console.error('attachVideo failed:', error);
    
    if (error.type === 'INVALID_OPERATION') {
      // User may have stopped video, or not in session
      console.log('User video not available');
    } else if (error.type === 'INTERNAL_ERROR') {
      // SDK internal error - may need to retry
      await new Promise(r => setTimeout(r, 1000));
      return stream.attachVideo(userId, quality);
    }
    
    return null;
  }
}
```

## Key Points

1. **Use `attachVideo()`, NOT `renderVideo()`** - `renderVideo()` is deprecated
2. **Listen to `peer-video-state-change`** - Required for remote video
3. **Handle mid-session join** - Manually render existing participants
4. **Detach before re-attaching** - When changing quality
5. **Check device capabilities** - `getMaxRenderableVideos()`, `isSupportMultipleVideos()`
6. **Enable WebRTC for HD** - Required for 720P/1080P

## Related Documentation

- [Session Join](session-join-pattern.md) - Initial setup
- [Event Handling](event-handling.md) - All video events
- [Common Issues](../troubleshooting/common-issues.md) - Troubleshooting

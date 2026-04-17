# Screen Share

Complete guide to sending and receiving screen shares in the Zoom Video SDK for Web.

## Overview

Screen sharing involves two distinct operations:
1. **Sending** - Sharing your screen to others (`startShareScreen`)
2. **Receiving** - Viewing others' shared screens (`startShareView` or `attachShareView`)

## Sending Screen Share

### Basic Screen Share

```javascript
// Get the media stream
const stream = client.getMediaStream();

// Create a canvas or video element to render the share preview
const shareCanvas = document.getElementById('share-canvas');

// Start sharing
await stream.startShareScreen(shareCanvas);
```

### With Options

```javascript
await stream.startShareScreen(shareCanvas, {
  displaySurface: 'monitor',  // 'monitor' | 'window' | 'browser'
  audio: true,                // Share system/tab audio
  optimizedForSharedVideo: true,  // Optimize for video content
});
```

### Stop Sharing

```javascript
await stream.stopShareScreen();
```

### Pause/Resume

```javascript
// Pause
await stream.pauseShareScreen();

// Resume
await stream.resumeShareScreen();
```

## Receiving Screen Share

### Method 1: Canvas-based (Legacy)

```javascript
// Create a canvas for rendering
const receiveCanvas = document.getElementById('share-view-canvas');

// Listen for active share changes
client.on('active-share-change', async (payload) => {
  const { state, userId } = payload;
  
  if (state === 'Active') {
    // Someone started sharing - render it
    await stream.startShareView(receiveCanvas, userId);
  } else if (state === 'Inactive') {
    // Sharing stopped
    await stream.stopShareView();
  }
});
```

### Method 2: VideoPlayer-based (Recommended - SDK 2.2.10+)

```javascript
// Listen for active share changes
client.on('active-share-change', async (payload) => {
  const { state, userId } = payload;
  
  if (state === 'Active') {
    // Attach share view - returns a VideoPlayer element
    const element = await stream.attachShareView(userId);
    document.getElementById('share-container').appendChild(element);
  } else if (state === 'Inactive') {
    // Detach share view
    const elements = await stream.detachShareView(userId);
    if (Array.isArray(elements)) {
      elements.forEach(e => e.remove());
    } else if (elements) {
      elements.remove();
    }
  }
});
```

## Complete Example

```javascript
import ZoomVideo from '@zoom/videosdk';

class ScreenShareManager {
  constructor(client) {
    this.client = client;
    this.stream = null;
    this.isSharing = false;
    this.activeShareUserId = null;
  }

  init() {
    this.stream = this.client.getMediaStream();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // When someone starts/stops sharing
    this.client.on('active-share-change', async (payload) => {
      const { state, userId } = payload;
      console.log('Share change:', state, 'from user:', userId);
      
      if (state === 'Active') {
        this.activeShareUserId = userId;
        await this.renderReceivedShare(userId);
      } else {
        await this.stopRenderingShare();
        this.activeShareUserId = null;
      }
    });

    // When share content changes (e.g., user switches windows)
    this.client.on('share-content-change', (payload) => {
      console.log('Share content changed for user:', payload.userId);
    });

    // When share dimension changes
    this.client.on('share-content-dimension-change', (payload) => {
      console.log('Share dimension:', payload.width, 'x', payload.height);
      // Resize container if needed
    });

    // When you're forced to stop sharing
    this.client.on('passively-stop-share', (payload) => {
      console.log('Forced to stop sharing. Reason:', payload);
      this.isSharing = false;
    });

    // Share privilege changes
    this.client.on('share-privilege-change', (payload) => {
      console.log('Share privilege:', payload.privilege);
    });
  }

  async startSharing() {
    // Check privilege first
    const privilege = this.stream.getSharePrivilege();
    if (privilege === 0) {
      throw new Error('Sharing not allowed - host has disabled it');
    }

    // Check if share is locked
    if (this.stream.isShareLocked()) {
      throw new Error('Sharing is locked by host');
    }

    const canvas = document.getElementById('share-preview-canvas');
    
    try {
      await this.stream.startShareScreen(canvas, {
        audio: true,
      });
      this.isSharing = true;
      console.log('Screen share started');
    } catch (error) {
      console.error('Failed to start screen share:', error);
      
      if (error.type === 'INVALID_OPERATION' && error.reason?.includes('extension')) {
        // Chrome extension required (legacy browsers)
        console.log('Install extension from:', error.extensionUrl);
      }
      
      throw error;
    }
  }

  async stopSharing() {
    if (!this.isSharing) return;
    
    await this.stream.stopShareScreen();
    this.isSharing = false;
    console.log('Screen share stopped');
  }

  async renderReceivedShare(userId) {
    const container = document.getElementById('share-view-container');
    
    try {
      // Use attachShareView for VideoPlayer-based rendering (SDK 2.2.10+)
      const element = await this.stream.attachShareView(userId);
      container.innerHTML = '';
      container.appendChild(element);
      container.style.display = 'block';
    } catch (error) {
      console.error('Failed to render share view:', error);
    }
  }

  async stopRenderingShare() {
    if (!this.activeShareUserId) return;
    
    const container = document.getElementById('share-view-container');
    container.style.display = 'none';
    
    try {
      await this.stream.detachShareView(this.activeShareUserId);
      container.innerHTML = '';
    } catch (error) {
      console.error('Failed to detach share view:', error);
    }
  }

  // Get who is currently sharing
  getShareUserList() {
    return this.stream.getShareUserList();
  }

  // Get active sharer's user ID
  getActiveShareUserId() {
    return this.stream.getActiveShareUserId();
  }
}

// Usage
const shareManager = new ScreenShareManager(client);
shareManager.init();

// Start sharing
document.getElementById('share-btn').onclick = () => shareManager.startSharing();
document.getElementById('stop-share-btn').onclick = () => shareManager.stopSharing();
```

## Share with Audio

```javascript
// Share screen with system/tab audio
await stream.startShareScreen(canvas, {
  audio: true,
});

// Check share audio status
const audioStatus = stream.getShareAudioStatus();
console.log('Share audio:', audioStatus);

// Mute/unmute share audio
await stream.muteShareAudio();   // Mute
await stream.unmuteShareAudio(); // Unmute
```

## Share Privilege Management (Host Only)

```javascript
import { SharePrivilege } from '@zoom/videosdk';

// Get current privilege
const privilege = stream.getSharePrivilege();

// Set privilege (host only)
await stream.setSharePrivilege(SharePrivilege.Unlocked);     // Anyone can share
await stream.setSharePrivilege(SharePrivilege.Locked);       // Only host can share
await stream.setSharePrivilege(SharePrivilege.OneParticipant); // One at a time

// Lock/unlock share (host only)
await stream.lockShare(true);  // Only host can share
await stream.lockShare(false); // Anyone can share
```

## Multiple Share Views (SDK 2.2.10+)

```javascript
// Check max renderable share views
const maxViews = stream.getMaxRenderableShareViews();
console.log('Can render up to', maxViews, 'share views');

// Get list of users who are sharing
const sharers = stream.getShareUserList();

// Render multiple share views
for (const sharer of sharers) {
  const element = await stream.attachShareView(sharer.userId);
  document.getElementById('multi-share-container').appendChild(element);
}
```

## Share Quality Optimization

```javascript
// Optimize for video content (movies, animations)
await stream.enableOptimizeForSharedVideo(true);

// Check if optimized
const isOptimized = stream.isOptimizeForSharedVideoEnabled();

// Check if optimization is supported
const isSupported = stream.isSupportOptimizedForSharedVideo();

// Update shared video quality
await stream.updateSharedVideoQuality(VideoQuality.Video_720P);
```

## Screenshot Share View

```javascript
// Take screenshot of active share
const blob = await stream.screenshotShareView();

// Convert to image
const url = URL.createObjectURL(blob);
const img = document.createElement('img');
img.src = url;
document.body.appendChild(img);
```

## React Component

```typescript
import React, { useEffect, useRef, useState } from 'react';
import { VideoClient, Stream } from '@zoom/videosdk';

interface ScreenShareProps {
  client: typeof VideoClient;
  stream: typeof Stream;
}

export const ScreenShare: React.FC<ScreenShareProps> = ({ client, stream }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isSharing, setIsSharing] = useState(false);
  const [activeShareUserId, setActiveShareUserId] = useState<number | null>(null);

  useEffect(() => {
    const handleShareChange = async (payload: { state: string; userId: number }) => {
      if (payload.state === 'Active') {
        setActiveShareUserId(payload.userId);
        
        if (containerRef.current) {
          const element = await stream.attachShareView(payload.userId);
          containerRef.current.innerHTML = '';
          containerRef.current.appendChild(element);
        }
      } else {
        if (activeShareUserId) {
          await stream.detachShareView(activeShareUserId);
        }
        setActiveShareUserId(null);
        if (containerRef.current) {
          containerRef.current.innerHTML = '';
        }
      }
    };

    const handlePassiveStop = () => {
      setIsSharing(false);
    };

    client.on('active-share-change', handleShareChange);
    client.on('passively-stop-share', handlePassiveStop);

    return () => {
      client.off('active-share-change', handleShareChange);
      client.off('passively-stop-share', handlePassiveStop);
    };
  }, [client, stream, activeShareUserId]);

  const startShare = async () => {
    try {
      const canvas = document.createElement('canvas');
      await stream.startShareScreen(canvas);
      setIsSharing(true);
    } catch (error) {
      console.error('Share failed:', error);
    }
  };

  const stopShare = async () => {
    await stream.stopShareScreen();
    setIsSharing(false);
  };

  return (
    <div className="screen-share">
      <div className="controls">
        {isSharing ? (
          <button onClick={stopShare}>Stop Sharing</button>
        ) : (
          <button onClick={startShare}>Share Screen</button>
        )}
      </div>
      
      {activeShareUserId && (
        <div 
          ref={containerRef} 
          className="share-view"
          style={{ width: '100%', aspectRatio: '16/9', background: '#000' }}
        />
      )}
    </div>
  );
};
```

## Key Events

| Event | When | Payload |
|-------|------|---------|
| `active-share-change` | Someone starts/stops sharing | `{ state: 'Active' \| 'Inactive', userId }` |
| `share-content-change` | Sharer switches window/tab | `{ userId }` |
| `share-content-dimension-change` | Share resolution changes | `{ width, height, type }` |
| `passively-stop-share` | You're forced to stop | `PassiveStopShareReason` enum |
| `share-privilege-change` | Host changes share settings | `{ privilege }` |
| `peer-share-state-change` | Peer share state changes | `{ action: 'Start' \| 'Stop', userId }` |
| `share-audio-change` | Share audio state changes | `{ state: 'on' \| 'off' }` |

## Key Points

1. **Two methods for receiving**: Canvas-based (`startShareView`) or VideoPlayer-based (`attachShareView`)
2. **Check privileges first**: Use `getSharePrivilege()` and `isShareLocked()` before attempting to share
3. **Handle `passively-stop-share`**: You may be forced to stop sharing by the host
4. **Share audio requires user gesture**: Browsers require user interaction to share audio
5. **Different from video**: Screen share uses separate canvas/container from video

## Related Documentation

- [Video Rendering](video-rendering.md) - Video handling
- [Event Handling](event-handling.md) - All events
- [Common Issues](../troubleshooting/common-issues.md) - Troubleshooting

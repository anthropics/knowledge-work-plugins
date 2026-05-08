# Custom Video

Build fully branded video experiences with complete UI control.

## Overview

Use the Zoom Video SDK to create custom video applications with your own UI, branding, and user experience - powered by Zoom's infrastructure.

## Skills Needed

- **zoom-video-sdk** - Primary

## Meeting SDK vs Video SDK

| Aspect | Meeting SDK | Video SDK |
|--------|-------------|-----------|
| UI | Zoom's UI | Your custom UI |
| Branding | Zoom branding | Your branding |
| Experience | Zoom meetings | Video sessions |
| Features | Full Zoom features | Core video features |

## Platform Options

| Platform | Use Case | Guide |
|----------|----------|-------|
| Web | Browser-based custom video | [video-sdk/SKILL.md](../../video-sdk/SKILL.md) |
| Linux | Headless bots, raw media capture/injection | [video-sdk/linux/linux.md](../../video-sdk/linux/linux.md) |
| iOS | Custom video on iPhone/iPad | - |
| Android | Custom video on Android | - |
| Desktop | Custom desktop video apps | - |

## Quick Start (Web)

```javascript
import ZoomVideo from '@zoom/videosdk';

const client = ZoomVideo.createClient();
await client.init('en-US', 'CDN');
await client.join(topic, signature, userName, password);

const stream = client.getMediaStream();
await stream.startVideo();
await stream.startAudio();
```

## Common Tasks

### Building Custom Video Layouts

```javascript
// Initialize Video SDK
const client = ZoomVideo.createClient();
await client.init('en-US', 'CDN');
await client.join(topic, signature, userName, password);

const stream = client.getMediaStream();

// Start my video
await stream.startVideo();
await stream.renderVideo(
  document.querySelector('#my-video'),
  client.getSessionInfo().userId,
  1280, 720,  // width, height
  0, 0,       // x, y offset
  3           // quality (1-4)
);

// Listen for other participants
client.on('user-added', (payload) => {
  payload.forEach(async (user) => {
    if (user.bVideoOn) {
      await renderParticipantVideo(user.userId);
    }
  });
});

async function renderParticipantVideo(userId) {
  const container = createVideoContainer(userId);
  await stream.renderVideo(container, userId, 640, 360, 0, 0, 2);
}
```

### Gallery View Implementation

```javascript
class GalleryView {
  constructor(containerEl, maxPerPage = 25) {
    this.container = containerEl;
    this.maxPerPage = maxPerPage;
    this.currentPage = 0;
    this.participants = [];
  }
  
  updateLayout() {
    const count = Math.min(this.participants.length, this.maxPerPage);
    const cols = Math.ceil(Math.sqrt(count));
    const rows = Math.ceil(count / cols);
    
    const cellWidth = this.container.clientWidth / cols;
    const cellHeight = this.container.clientHeight / rows;
    
    // Render each participant in grid
    this.participants.slice(0, this.maxPerPage).forEach((userId, index) => {
      const x = (index % cols) * cellWidth;
      const y = Math.floor(index / cols) * cellHeight;
      
      stream.renderVideo(
        this.getCanvas(userId),
        userId,
        cellWidth, cellHeight,
        x, y, 2
      );
    });
  }
  
  addParticipant(userId) {
    this.participants.push(userId);
    this.updateLayout();
  }
  
  removeParticipant(userId) {
    this.participants = this.participants.filter(id => id !== userId);
    this.updateLayout();
  }
}
```

### Speaker View Implementation

```javascript
class SpeakerView {
  constructor(mainEl, stripEl) {
    this.mainVideo = mainEl;
    this.stripContainer = stripEl;
    this.activeSpeaker = null;
    this.participants = [];
  }
  
  setActiveSpeaker(userId) {
    if (this.activeSpeaker === userId) return;
    
    this.activeSpeaker = userId;
    
    // Render active speaker large
    stream.renderVideo(
      this.mainVideo,
      userId,
      1280, 720, 0, 0, 4  // High quality
    );
    
    // Update thumbnail strip
    this.updateStrip();
  }
  
  updateStrip() {
    const others = this.participants.filter(id => id !== this.activeSpeaker);
    const thumbWidth = 160;
    const thumbHeight = 90;
    
    others.forEach((userId, index) => {
      stream.renderVideo(
        this.getStripCanvas(userId),
        userId,
        thumbWidth, thumbHeight,
        index * thumbWidth, 0, 1  // Lower quality
      );
    });
  }
}

// Auto-switch to active speaker
client.on('active-speaker', (payload) => {
  if (payload.userId) {
    speakerView.setActiveSpeaker(payload.userId);
  }
});
```

### Custom Controls

```javascript
// Audio controls
async function toggleMute() {
  const stream = client.getMediaStream();
  const isMuted = stream.isAudioMuted();
  
  if (isMuted) {
    await stream.unmuteAudio();
  } else {
    await stream.muteAudio();
  }
  
  updateMuteButton(!isMuted);
}

// Video controls
async function toggleVideo() {
  const stream = client.getMediaStream();
  const isVideoOn = stream.isCapturingVideo();
  
  if (isVideoOn) {
    await stream.stopVideo();
  } else {
    await stream.startVideo();
    await stream.renderVideo(myCanvas, myUserId, 1280, 720, 0, 0, 3);
  }
  
  updateVideoButton(!isVideoOn);
}

// Device selection
async function switchCamera(deviceId) {
  const stream = client.getMediaStream();
  await stream.switchCamera(deviceId);
}

async function switchMicrophone(deviceId) {
  const stream = client.getMediaStream();
  await stream.switchMicrophone(deviceId);
}

// Get available devices
const cameras = await ZoomVideo.getCameras();
const mics = await ZoomVideo.getMicrophones();
const speakers = await ZoomVideo.getSpeakers();
```

## Resources

- **Video SDK docs**: https://developers.zoom.us/docs/video-sdk/
- **Web sample**: https://github.com/zoom/videosdk-web-sample
- **UI Toolkit**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/

# Layers API - Immersive Mode

Custom video layouts that replace the standard gallery view. Position participant video feeds, backgrounds, and web content anywhere on screen.

## Overview

Immersive mode takes over the entire meeting video area. You control where each participant's video appears, add background images, and overlay web content.

**Use cases:** Podcast layout, talk show, classroom, game show, branded meetings.

## Quick Start

```javascript
import zoomSdk from '@zoom/appssdk';

// 1. Config with Layers capabilities
await zoomSdk.config({
  capabilities: [
    'getRunningContext',
    'runRenderingContext', 'closeRenderingContext',
    'drawParticipant', 'clearParticipant',
    'drawImage', 'clearImage',
    'drawWebView', 'clearWebView',
    'getMeetingParticipants', 'onParticipantChange',
    'postMessage', 'onMessage',
    'sendAppInvitationToAllParticipants',
    'onRenderedAppOpened'
  ],
  version: '0.16'
});

// 2. Start immersive mode (Team = person cutout, Presentation = rectangle)
await zoomSdk.runRenderingContext({
  view: 'immersive',
  defaultCutout: 'person'  // Removes backgrounds via AI segmentation
});

// 3. Draw a background (imageData = JS ImageData object, NOT base64)
const canvas = document.createElement('canvas');
canvas.width = 1280;
canvas.height = 720;
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#1a1a2e';
ctx.fillRect(0, 0, 1280, 720);
const imageData = ctx.getImageData(0, 0, 1280, 720);

await zoomSdk.drawImage({
  imageData,
  x: 0, y: 0,
  zIndex: 0
});

// 4. Position participants
const { participants } = await zoomSdk.getMeetingParticipants();

await zoomSdk.drawParticipant({
  participantUUID: participants[0].participantUUID,
  x: 50, y: 100,
  width: 500, height: 400,
  zIndex: 1,
  cutout: 'person'  // Override default if needed
});

await zoomSdk.drawParticipant({
  participantUUID: participants[1].participantUUID,
  x: 730, y: 100,
  width: 500, height: 400,
  zIndex: 1,
  cutout: 'person'
});
```

## Drawing Methods

### drawParticipant

Position a participant's video feed. In immersive mode, you can draw any participant.

```javascript
await zoomSdk.drawParticipant({
  participantUUID: 'uuid-string',  // From getMeetingParticipants()
  x: 0,          // PixelValue: "Npx", "N%", or number
  y: 0,          // PixelValue
  width: 640,    // PixelValue (aspect ratio maintained)
  height: 480,   // PixelValue (aspect ratio maintained)
  zIndex: 1,     // Stacking order (higher = on top)
  cutout: 'person'  // Optional: "person"|"standard"|"rectangle"|"circle"|"square"|"verticalRectangle"
});
```

**Cutout shapes** (all have 30px rounded corners except `"standard"`):
- `"person"` — AI background removal (v5.9.3+)
- `"standard"` — Full uncropped video, squared corners (v5.11.3+)
- `"rectangle"` — Rounded rectangle (v5.11.0+)
- `"circle"` — Circle (v5.11.3+)
- `"square"` — Square with rounded corners (v5.11.3+)
- `"verticalRectangle"` — Vertical rectangle with rounded corners (v5.11.3+)

> **Deprecated:** `participantId` — use `participantUUID` instead.

### drawImage

Add images (backgrounds, overlays, borders). Uses standard JavaScript `ImageData` (NOT base64):

```javascript
const canvas = document.createElement('canvas');
canvas.width = 1280;
canvas.height = 720;
const ctx = canvas.getContext('2d');
// ... draw on canvas ...
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

const { imageId } = await zoomSdk.drawImage({
  imageData,     // ImageData object from canvas.getImageData()
  x: 0, y: 0,
  zIndex: 0      // Behind participants
});
// Save imageId for clearImage() later
```

### drawWebView

Embed your app's webview as an interactive overlay. Only one webview per rendering context.

```javascript
await zoomSdk.drawWebView({
  x: 400, y: 600,
  width: 480, height: 100,
  zIndex: 2  // On top of everything
});
```

> See [../references/layers-api.md](../references/layers-api.md#drawwebview) for full drawWebView details, webview communication, and the `webviewId` documentation inconsistency.

### Clearing

```javascript
await zoomSdk.clearParticipant({ participantUUID: 'uuid' });
await zoomSdk.clearImage({ imageId: 'id-from-drawImage-response' });
await zoomSdk.clearWebView();  // No params per TypeDoc v0.16.36
```

### Exit Immersive Mode

```javascript
await zoomSdk.closeRenderingContext();
```

## Complete Example: Podcast Layout

Two hosts side-by-side with custom background:

```javascript
import zoomSdk from '@zoom/appssdk';

class PodcastLayout {
  constructor() {
    this.active = false;
  }

  async start() {
    await zoomSdk.runRenderingContext({ view: 'immersive', defaultCutout: 'person' });
    this.active = true;

    // Draw background
    await this.drawBackground();

    // Position hosts
    const { participants } = await zoomSdk.getMeetingParticipants();
    await this.layoutParticipants(participants);

    // React to participant changes
    zoomSdk.addEventListener('onParticipantChange', async () => {
      const { participants } = await zoomSdk.getMeetingParticipants();
      await this.layoutParticipants(participants);
    });
  }

  async drawBackground() {
    const canvas = document.createElement('canvas');
    canvas.width = 1280;
    canvas.height = 720;
    const ctx = canvas.getContext('2d');

    // Gradient background
    const gradient = ctx.createLinearGradient(0, 0, 1280, 720);
    gradient.addColorStop(0, '#1a1a2e');
    gradient.addColorStop(1, '#16213e');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1280, 720);

    // Title
    ctx.fillStyle = 'white';
    ctx.font = 'bold 32px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('The Zoom Podcast', 640, 60);

    const imageData = ctx.getImageData(0, 0, 1280, 720);
    await zoomSdk.drawImage({
      imageData,
      x: 0, y: 0, zIndex: 0
    });
  }

  async layoutParticipants(participants) {
    if (participants.length === 1) {
      // Single host - centered
      await zoomSdk.drawParticipant({
        participantUUID: participants[0].participantUUID,
        x: 340, y: 100, width: 600, height: 500, zIndex: 1
      });
    } else if (participants.length >= 2) {
      // Two hosts - side by side
      await zoomSdk.drawParticipant({
        participantUUID: participants[0].participantUUID,
        x: 40, y: 100, width: 580, height: 500, zIndex: 1
      });
      await zoomSdk.drawParticipant({
        participantUUID: participants[1].participantUUID,
        x: 660, y: 100, width: 580, height: 500, zIndex: 1
      });
    }
  }

  async stop() {
    await zoomSdk.closeRenderingContext();
    this.active = false;
  }
}
```

## HiDPI Support

For Retina/HiDPI displays, multiply coordinates by `window.devicePixelRatio`:

```javascript
const dpr = window.devicePixelRatio || 1;

await zoomSdk.drawParticipant({
  participantUUID: uuid,
  x: 100 * dpr,
  y: 100 * dpr,
  width: 640 * dpr,
  height: 480 * dpr,
  zIndex: 1
});
```

## Multi-Participant Sync

The host controls the layout. Use Socket.io to broadcast layout changes:

```javascript
// Host sends layout to all participants via your backend
socket.emit('layout-change', {
  participants: [
    { uuid: 'a', x: 40, y: 100, w: 580, h: 500 },
    { uuid: 'b', x: 660, y: 100, w: 580, h: 500 }
  ]
});

// All participants apply the layout
socket.on('layout-change', async (layout) => {
  for (const p of layout.participants) {
    await zoomSdk.drawParticipant({
      participantUUID: p.uuid,
      x: p.x, y: p.y, width: p.w, height: p.h, zIndex: 1
    });
  }
});
```

## Performance Tips

- Use `requestAnimationFrame` for animations
- Minimize `drawImage` calls (batch updates)
- Pre-render complex backgrounds to canvas
- Keep zIndex values low (0-10 range)
- Clear unused elements to free resources

## Resources

- **Layers docs**: https://developers.zoom.us/docs/zoom-apps/guides/layers-api/
- **Layers API reference**: [../references/layers-api.md](../references/layers-api.md)
- **Sample app**: https://github.com/zoom/zoomapps-customlayout-js

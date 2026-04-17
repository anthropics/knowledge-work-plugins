# Layers API - Camera Mode

Overlay graphics on the user's own camera feed. Create virtual camera effects, branded frames, and interactive overlays.

## Overview

Camera mode overlays your content on the user's camera video. Unlike immersive mode (which controls the entire meeting view), camera mode only affects the individual user's camera feed - other participants see the overlay on that user's video.

## Quick Start

```javascript
import zoomSdk from '@zoom/appssdk';

const config = await zoomSdk.config({
  capabilities: [
    'getRunningContext',
    'runRenderingContext', 'closeRenderingContext',
    'drawParticipant', 'clearParticipant',
    'drawImage', 'clearImage',
    'drawWebView', 'clearWebView',
    'postMessage', 'onMessage',
    'onRenderedAppOpened'
  ],
  version: '0.16'
});

// renderTarget = virtual camera frame size (default: 1280x720)
const rtWidth = config.media?.renderTarget?.width || 1280;
const rtHeight = config.media?.renderTarget?.height || 720;

// Start camera mode
await zoomSdk.runRenderingContext({ view: 'camera' });

// Wait for CEF to initialize
zoomSdk.addEventListener('onRenderedAppOpened', async () => {
  // Draw self video as background
  await zoomSdk.drawParticipant({
    participantUUID: myUUID,
    x: 0, y: 0,
    width: rtWidth, height: rtHeight,
    zIndex: 1,
    cameraModeMirroring: true  // v5.13.5+ — mirror for self-view
  });

  // Add a branded frame overlay
  const frame = await createBrandedFrame(rtWidth, rtHeight);
  const imageData = frame.getContext('2d').getImageData(0, 0, rtWidth, rtHeight);
  await zoomSdk.drawImage({
    imageData,
    x: 0, y: 0,
    zIndex: 2
  });

  // Or draw webview overlay (your app's home URL rendered off-screen)
  await zoomSdk.drawWebView({
    x: 0, y: 0,
    width: rtWidth, height: rtHeight,
    zIndex: 3
  });
});
```

## CEF Race Condition (Critical)

Camera mode uses CEF (Chromium Embedded Framework) which takes time to initialize. Drawing too early will fail silently.

**Solution: Retry with backoff**

```javascript
async function drawWithRetry(drawFn, maxRetries = 5) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await drawFn();
      return; // Success
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      // Exponential backoff: 200ms, 400ms, 800ms, 1600ms, 3200ms
      await new Promise(r => setTimeout(r, 200 * Math.pow(2, i)));
    }
  }
}

// Usage
await zoomSdk.runRenderingContext({ view: 'camera' });

await drawWithRetry(async () => {
  await zoomSdk.drawImage({
    imageData: frame.toDataURL(),
    x: 0, y: 0, width: 1280, height: 720, zIndex: 1
  });
});
```

## Example: Branded Camera Frame

```javascript
async function createBrandedFrame() {
  const canvas = document.createElement('canvas');
  canvas.width = 1280;
  canvas.height = 720;
  const ctx = canvas.getContext('2d');

  // Transparent center (camera shows through)
  ctx.clearRect(0, 0, 1280, 720);

  // Bottom bar with company branding
  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.fillRect(0, 660, 1280, 60);

  // Company name
  ctx.fillStyle = 'white';
  ctx.font = 'bold 20px sans-serif';
  ctx.fillText('Acme Corp', 20, 695);

  // Border frame
  ctx.strokeStyle = '#2d8cff';
  ctx.lineWidth = 4;
  ctx.strokeRect(2, 2, 1276, 716);

  return canvas;
}
```

## Example: Name Tag Overlay

```javascript
async function drawNameTag(name, title) {
  const canvas = document.createElement('canvas');
  canvas.width = 300;
  canvas.height = 80;
  const ctx = canvas.getContext('2d');

  // Background
  ctx.fillStyle = 'rgba(45, 140, 255, 0.85)';
  ctx.beginPath();
  ctx.roundRect(0, 0, 300, 80, 12);
  ctx.fill();

  // Name
  ctx.fillStyle = 'white';
  ctx.font = 'bold 22px sans-serif';
  ctx.fillText(name, 16, 32);

  // Title
  ctx.font = '16px sans-serif';
  ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
  ctx.fillText(title, 16, 58);

  await zoomSdk.drawImage({
    imageData: canvas.toDataURL(),
    x: 20, y: 620,
    width: 300, height: 80,
    zIndex: 2
  });
}
```

## Exiting Camera Mode

```javascript
await zoomSdk.closeRenderingContext();
```

## drawWebView in Camera Mode

The webview renders your app's home URL off-screen. Use it for interactive overlays controlled from your sidebar app:

```javascript
// Draw webview filling entire camera frame
await zoomSdk.drawWebView({
  x: 0, y: 0,
  width: rtWidth, height: rtHeight,
  zIndex: 2
});

// Or partial overlay (bottom third)
await zoomSdk.drawWebView({
  x: 0, y: rtHeight * 0.67,
  width: rtWidth, height: rtHeight * 0.33,
  zIndex: 2
});

// Hide webview (app keeps running)
await zoomSdk.clearWebView();
```

**Communication between sidebar ↔ camera mode app:**

```javascript
// Sidebar sends command to camera mode instance
zoomSdk.postMessage({ command: 'show-nametag', name: 'John' });

// Camera mode instance listens (no connect() required)
zoomSdk.addEventListener('onMessage', (event) => {
  if (event.command === 'show-nametag') {
    document.getElementById('name').textContent = event.name;
  }
});
```

## Differences from Immersive Mode

| Aspect | Immersive | Camera |
|--------|-----------|--------|
| Scope | Entire meeting view | User's camera only |
| drawParticipant | Any participant | Self only |
| drawWebView | Yes | Yes |
| Who sees it | All participants | All see it on this user's feed |
| Use case | Custom layouts | Personal overlays, branding |
| Browser | Standard WebView | CEF (has init delay) |
| Coordinate space | CSS pixels | Raw pixels (renderTarget) |
| `cameraModeMirroring` | N/A | Yes (v5.13.5+) |

## Resources

- **Camera mode docs**: https://developers.zoom.us/docs/zoom-apps/guides/camera-mode/
- **Layers API reference**: [../references/layers-api.md](../references/layers-api.md)
- **Sample app**: https://github.com/zoom/zoomapps-customlayout-js

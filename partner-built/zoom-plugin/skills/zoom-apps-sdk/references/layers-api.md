# Zoom Apps SDK - Layers API Reference

Build immersive video layouts and camera overlays using the Layers API.

## Overview

The Layers API (v1.5) provides rendering modes for custom visual experiences. Requires Zoom Client v5.10.6+.

| Mode | Description | Use Case |
|------|-------------|----------|
| **Team** (`immersive` + `person` cutout) | Canvas with background-removed participant cutouts | Podcast, talk show, classroom |
| **Presentation** (`immersive` + `rectangle` cutout) | Canvas with full-width participant video tiles | Presentations, branded meetings |
| **Camera** | Overlay on user's own camera feed (OSR) | Branding, name tags, effects |
| **Controller** | Sidebar app that coordinates Layers modes | Required for all modes above |

> **Note:** When using the Layers API, your app is categorized as an "Immersive App" on the Marketplace.

## Required Capabilities

```javascript
await zoomSdk.config({
  capabilities: [
    'getRunningContext',
    'runRenderingContext', 'closeRenderingContext',
    'drawParticipant', 'clearParticipant',
    'drawImage', 'clearImage',
    'drawWebView', 'clearWebView',
    'postMessage', 'onMessage',
    'sendAppInvitationToAllParticipants',
    'onMyMediaChange',
    'onRenderedAppOpened'
  ],
  version: '0.16'
});
```

> **Gotcha:** The official guide lists `clearWebview` (lowercase 'v') in one config example. Use `clearWebView` (camelCase) to match the actual method name.

## Types

### PixelValue

All position/size parameters accept three formats:

```typescript
type PixelValue = `${string}px` | `${string}%` | number;
```

| Format | Example | Meaning |
|--------|---------|---------|
| `"Npx"` | `"100px"` | CSS reference pixels |
| `"N%"` | `"50%"` | Percentage of container/view |
| `number` | `1280` | Raw physical pixels |

### ParticipantCutoutShape

```typescript
type ParticipantCutoutShape =
  | "person"             // v5.9.3+  — Cut out background (AI segmentation)
  | "standard"           // v5.11.3+ — Full uncropped video (squared corners)
  | "rectangle"          // v5.11.0+ — Rounded rectangle (30px radius)
  | "circle"             // v5.11.3+ — Circle
  | "square"             // v5.11.3+ — Square (30px radius)
  | "verticalRectangle"  // v5.11.3+ — Vertical rectangle (30px radius)
```

All shapes have 30px rounded corners except `"standard"` which has squared corners.

### RenderingContextView

```typescript
type RenderingContextView = "immersive" | "camera";
```

## Lifecycle

### Starting a Rendering Context

```javascript
// Team mode (person cutout — removes backgrounds)
await zoomSdk.runRenderingContext({
  view: 'immersive',
  defaultCutout: 'person'
});

// Presentation mode (rectangle cutout — keeps backgrounds)
await zoomSdk.runRenderingContext({
  view: 'immersive',
  defaultCutout: 'rectangle'
});

// Camera mode (affects only your video stream)
await zoomSdk.runRenderingContext({ view: 'camera' });
```

**`runRenderingContext(options)`:**
- `view` (required): `"immersive"` | `"camera"`
- `defaultCutout` (optional): Sets the default cutout shape for all `drawParticipant()` calls in this context

### Running Context Values

| Context | Meaning |
|---------|---------|
| `inMeeting` | Default sidebar panel |
| `inImmersive` | Running in immersive mode (team or presentation) |
| `inCamera` | Running as virtual camera (off-screen rendering) |

```javascript
const { runningContext } = await zoomSdk.getRunningContext();
// runningContext changes automatically when runRenderingContext() is called
```

### Updating Content

To move, resize, or adjust a drawn element: clear it first, then redraw.

```javascript
// Move a participant
await zoomSdk.clearParticipant({ participantUUID: uuid });
await zoomSdk.drawParticipant({ participantUUID: uuid, x: 100, y: 200, width: 640, height: 480, zIndex: 1 });
```

> There is no in-place update — always clear + redraw.

### Closing

```javascript
await zoomSdk.closeRenderingContext();
// Returns app to sidebar, runningContext becomes "inMeeting"
```

### Constraints

- Only a **meeting host** can set the rendering context to immersive
- Only **one immersive context** can exist at a time (second attempt fails with error)
- **Camera mode + Presentation mode can run simultaneously**
- Host must use `sendAppInvitationToAllParticipants` to transition other participants
- If `aomhost` package needs download, `runRenderingContext` returns non-success

## Drawing Methods

### drawParticipant

Position a participant's video feed on the canvas.

```typescript
drawParticipant(options: DrawParticipantOptions): Promise<GeneralMessageResponse>
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `participantUUID` | `string` | — | Meeting-specific participant identifier |
| ~~`participantId`~~ | ~~`string`~~ | — | **DEPRECATED** — use `participantUUID` |
| `x` | `PixelValue` | `"0px"` | Horizontal position |
| `y` | `PixelValue` | `"0px"` | Vertical position |
| `width` | `PixelValue` | `"100%"` | Width (aspect ratio maintained) |
| `height` | `PixelValue` | `"100%"` | Height (aspect ratio maintained) |
| `zIndex` | `number` | `1` | Stacking order (higher = on top) |
| `cutout` | `ParticipantCutoutShape` | context default | Cutout behavior (v5.9.3+) |
| `cameraModeMirroring` | `boolean` | `false` | Mirror video in camera mode (v5.13.5+) |

**Mode differences:**
- **Immersive:** Can draw any participant
- **Camera:** Can only draw current user (self)

```javascript
// Immersive — draw any participant with person cutout
await zoomSdk.drawParticipant({
  participantUUID: 'uuid-from-getMeetingParticipants',
  x: 40, y: 100,
  width: 580, height: 500,
  zIndex: 1,
  cutout: 'person'
});

// Camera — draw self with mirroring
await zoomSdk.drawParticipant({
  participantUUID: myUUID,
  x: 0, y: 0,
  width: 1280, height: 720,
  zIndex: 1,
  cameraModeMirroring: true  // v5.13.5+
});
```

### drawImage

Draw static images (backgrounds, overlays, borders).

```typescript
drawImage(options: DrawImageOptions): Promise<DrawImageResponse>
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `imageData` | `ImageData` | — | **Required.** Standard JS ImageData object (width, height, pixel bytes) |
| `x` | `PixelValue` | `"0px"` | Horizontal position |
| `y` | `PixelValue` | `"0px"` | Vertical position |
| `zIndex` | `number` | `1` | Stacking order |

**Returns:** `{ imageId: string }` — use this ID with `clearImage()`.

> **Important:** `imageData` is a standard JavaScript `ImageData` object (from `canvas.getImageData()`), NOT a base64 data URL.

```javascript
const canvas = document.createElement('canvas');
canvas.width = 1280;
canvas.height = 720;
const ctx = canvas.getContext('2d');
// ... draw on canvas ...
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

const { imageId } = await zoomSdk.drawImage({
  imageData,
  x: 0, y: 0,
  zIndex: 0
});
```

#### HiDPI Constraints

`drawImage()` does **not** directly support HiDPI image sizes. For HiDPI/Retina:

1. Draw to canvas using the scaling ratio (`window.devicePixelRatio`)
2. Divide out the ratio for x/y coordinates when passing to `drawImage`
3. Keep the ratio for width and height
4. You may need to **tile** the screen for full-screen images

```javascript
const dpr = window.devicePixelRatio || 1;
const canvas = document.createElement('canvas');
canvas.width = 1280 * dpr;
canvas.height = 720 * dpr;
const ctx = canvas.getContext('2d');
ctx.scale(dpr, dpr);
// ... draw at logical pixels ...
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

await zoomSdk.drawImage({
  imageData,
  x: 0, y: 0,
  zIndex: 0
});
```

### drawWebView

Position the app's OSR (Off-Screen Rendering) webview within the Layers canvas.

```typescript
drawWebView(options: DrawWebViewOptions): Promise<GeneralMessageResponse>
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `PixelValue` | `0` | Horizontal position in OSR target area |
| `y` | `PixelValue` | `0` | Vertical position in OSR target area |
| `width` | `PixelValue` | full rendering width | Width in OSR target area |
| `height` | `PixelValue` | full rendering height | Height in OSR target area |
| `zIndex` | `number` | `1` | Stacking order |

> **⚠ Documentation inconsistency:** The official Zoom guides show a `webviewId` parameter in examples, but the TypeDoc type definition (v0.16.36) does **not** include it. Since there is only one webview per app, this parameter may be vestigial. If in doubt, omit it.

**What the webview renders:** Your app's home URL as configured in `zoomSdk.config()`. It's an off-screen rendering of your app — not a configurable URL.

**Only one webview per rendering context.** There is no multi-webview support.

```javascript
// Full-screen webview in camera mode
const config = await zoomSdk.config({ /* ... */ });
await zoomSdk.runRenderingContext({ view: 'camera' });

await zoomSdk.drawWebView({
  x: 0,
  y: 0,
  width: config.media.renderTarget.width,   // Default: 1280
  height: config.media.renderTarget.height,  // Default: 720
  zIndex: 2
});
```

```javascript
// Partial webview overlay (bottom third of camera)
await zoomSdk.drawWebView({
  x: 0,
  y: 480,
  width: 1280,
  height: 240,
  zIndex: 2
});
```

#### Webview Communication

The sidebar app and the camera/immersive app are separate instances. Use `postMessage()` and `onMessage` to communicate between them:

```javascript
// Sidebar instance → Camera instance (no connect() required)
zoomSdk.postMessage({ command: 'update-overlay', text: 'Q&A Time' });

// Camera instance listens
zoomSdk.addEventListener('onMessage', (eventInfo) => {
  if (eventInfo.command === 'update-overlay') {
    document.getElementById('overlay-text').textContent = eventInfo.text;
  }
});
```

> **Note:** `connect()` is NOT required for app-to-app messaging in Layers. `postMessage` works between instances of the same app.

### Clearing

```javascript
// Clear participant (use participantUUID, not the deprecated participantId)
await zoomSdk.clearParticipant({ participantUUID: 'uuid' });

// Clear image (use imageId from drawImage response)
await zoomSdk.clearImage({ imageId: 'id-from-drawImage' });

// Clear webview (hides it — app continues running)
await zoomSdk.clearWebView();
// Note: TypeDoc v0.16.36 shows no parameters.
// Guide examples show { webviewId: "xxx" } but this may be outdated.
```

## Coordinate System

- **Origin:** Top-left corner (0, 0)
- **X:** Increases rightward
- **Y:** Increases downward
- **Units:** PixelValue — supports `"Npx"`, `"N%"`, or raw `number`

### Immersive Mode

- Coordinates are CSS pixels relative to the meeting canvas
- Automatic scaling for different window sizes

### Camera Mode

- Coordinates are raw pixels relative to `renderTarget` dimensions
- Default renderTarget: 1280×720 (configurable)
- Access via: `config.media.renderTarget.width` / `.height`

```javascript
const config = await zoomSdk.config({ /* ... */ });
const rtWidth = config.media.renderTarget.width;   // e.g. 1280
const rtHeight = config.media.renderTarget.height;  // e.g. 720
```

## Z-Index Layering

```
zIndex: 2+  ─  WebViews, interactive overlays (top)
zIndex: 1   ─  Participant videos
zIndex: 0   ─  Background images (bottom)
```

Higher zIndex values render on top. All three element types (participant, image, webview) share the same z-index space and can overlap.

## Events

### onRenderedAppOpened

Fires when the rendering context is ready. Best signal that CEF is initialized in camera mode.

```javascript
zoomSdk.addEventListener('onRenderedAppOpened', () => {
  // Safe to call drawParticipant, drawImage, drawWebView
});
```

### onMyMediaChange

Fires when the user's video changes (camera switch, "Original ratio" toggle, "HD" toggle). Returns device pixel dimensions of the source video.

```javascript
zoomSdk.addEventListener('onMyMediaChange', (event) => {
  // event.media.video.width / height — device pixels of source video
  // Redraw your layout if needed
});
```

### Window Resize (Immersive Only)

When the Zoom meeting window is resized, the app must move and resize participants/images. Not relevant to Camera Mode (fixed renderTarget).

## Immersive Mode vs Camera Mode

| Aspect | Immersive | Camera |
|--------|-----------|--------|
| Scope | Entire meeting view | User's camera only |
| drawParticipant | Any participant | Self only |
| drawImage | Yes | Yes |
| drawWebView | Yes | Yes |
| Who sees it | All participants | All see it on this user's feed |
| Browser engine | Standard WebView | CEF (Chromium Embedded Framework) |
| Rendering | On-screen | Off-screen (OSR) |
| Coordinate space | CSS pixels | Raw pixels (renderTarget) |
| Simultaneous | One immersive at a time | Can run with Presentation mode |

## Camera Mode: CEF Race Condition

Camera mode uses CEF which takes time to initialize. Draw calls may fail if called too early.

**Best approach: Listen for `onRenderedAppOpened`:**

```javascript
zoomSdk.addEventListener('onRenderedAppOpened', async () => {
  await zoomSdk.drawWebView({ x: 0, y: 0, width: 1280, height: 720, zIndex: 2 });
});
```

**Fallback: Retry with exponential backoff:**

```javascript
async function drawWithRetry(drawFn, maxRetries = 5) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await drawFn();
      return;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 200 * Math.pow(2, i)));
    }
  }
}
```

**Alternative: Check running context:**

```javascript
const { runningContext } = await zoomSdk.getRunningContext();
if (runningContext === 'inCamera') {
  // CEF is ready, safe to draw
}
```

## Performance Tips

- Use `requestAnimationFrame` for animations
- Minimize draw calls (batch updates when possible)
- Pre-render complex backgrounds to a single canvas ImageData
- Keep zIndex values low (0-10 range)
- Clear unused elements to free resources
- Test on lower-end hardware
- For full-screen images: tile the screen (HiDPI limitation)

## Example: Two-Person Podcast Layout

```javascript
// Background
const canvas = document.createElement('canvas');
canvas.width = 1280;
canvas.height = 720;
const ctx = canvas.getContext('2d');
const gradient = ctx.createLinearGradient(0, 0, 1280, 720);
gradient.addColorStop(0, '#1a1a2e');
gradient.addColorStop(1, '#16213e');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, 1280, 720);
const imageData = ctx.getImageData(0, 0, 1280, 720);

await zoomSdk.drawImage({ imageData, x: 0, y: 0, zIndex: 0 });

// Host (left) — person cutout removes background
await zoomSdk.drawParticipant({
  participantUUID: hostUUID,
  x: 40, y: 100, width: 580, height: 500,
  zIndex: 1, cutout: 'person'
});

// Guest (right)
await zoomSdk.drawParticipant({
  participantUUID: guestUUID,
  x: 660, y: 100, width: 580, height: 500,
  zIndex: 1, cutout: 'person'
});
```

## Version History

| Feature | Client Version | SDK Version |
|---------|---------------|-------------|
| Core Layers API | 5.9.0 | 0.16 |
| `cutout: "person"` | 5.9.3 | 0.16 |
| `cutout: "rectangle"` | 5.11.0 | 0.16 |
| `cutout: "circle"`, `"square"`, `"verticalRectangle"` | 5.11.3 | 0.16 |
| `drawWebView()` / `clearWebView()` | 5.10.6 | 0.16.11+ |
| Camera Mode | 5.13.1 | 0.16 |
| `cameraModeMirroring` | 5.13.5 | 0.16 |

## Resources

- **Layers API docs**: https://developers.zoom.us/docs/zoom-apps/guides/layers-api/
- **Using the API**: https://developers.zoom.us/docs/zoom-apps/guides/layers-using-api/
- **Manipulating UI**: https://developers.zoom.us/docs/zoom-apps/guides/layers-manipulating-ui/
- **Camera Mode docs**: https://developers.zoom.us/docs/zoom-apps/guides/camera-mode/
- **Sample app**: https://github.com/zoom/zoomapps-customlayout-js
- **SDK TypeDoc**: https://appssdk.zoom.us/classes/ZoomSdk.ZoomSdk.html
- **Immersive example**: [../examples/layers-immersive.md](../examples/layers-immersive.md)
- **Camera example**: [../examples/layers-camera.md](../examples/layers-camera.md)

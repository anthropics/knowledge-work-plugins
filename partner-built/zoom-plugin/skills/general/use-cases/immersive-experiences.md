# Immersive Experiences

Custom video layouts replacing the standard Zoom gallery view using the Layers API.

## Overview

The Layers API lets you take over the meeting's video display to create custom layouts - podcast formats, talk shows, classrooms, game shows, and branded meeting experiences.

## Skills Needed

- **zoom-apps-sdk** (Layers API) - Primary
- **oauth** - Authentication

## Use Case Patterns

| Pattern | Description | Key APIs |
|---------|-------------|----------|
| Podcast layout | 2-3 hosts with custom background | drawParticipant, drawImage |
| Talk show | Large host + row of guests | drawParticipant, drawImage |
| Classroom | Teacher prominent + student thumbnails | drawParticipant, drawImage |
| Game show | Custom positions with animated overlays | drawParticipant, drawImage, drawWebView |
| Branded meeting | Company background + participant positions | drawParticipant, drawImage |
| Interactive dashboard | Participants + live data panels | drawParticipant, drawWebView |

## Architecture

```
Host                              Participants
────                              ────────────
Controls layout (UI panel)  -->   Receive layout via Socket.io/backend
runRenderingContext()        -->   runRenderingContext()
drawParticipant() x N        -->   drawParticipant() x N (same positions)
drawImage() (background)     -->   drawImage() (same background)
```

All participants must be in immersive mode and rendering the same layout. The host typically controls layout changes and broadcasts them via your backend (Socket.io, WebSocket).

## Quick Start

```javascript
import zoomSdk from '@zoom/appssdk';

await zoomSdk.config({
  capabilities: [
    'runRenderingContext', 'closeRenderingContext',
    'drawParticipant', 'clearParticipant',
    'drawImage', 'clearImage',
    'getMeetingParticipants', 'onParticipantChange'
  ],
  version: '0.16'
});

// Start immersive mode
await zoomSdk.runRenderingContext({ view: 'immersive' });

// Get participants and layout them
const { participants } = await zoomSdk.getMeetingParticipants();
// ... position participants with drawParticipant()
```

## Performance Considerations

- Pre-render backgrounds to a single canvas image
- Minimize drawImage calls during animations
- Use requestAnimationFrame for smooth transitions
- Test on lower-end hardware (not everyone has a fast machine)
- Keep zIndex values in 0-10 range

## Detailed Guides

- **[Layers Immersive Example](../../zoom-apps-sdk/examples/layers-immersive.md)** - Complete podcast layout code
- **[Layers API Reference](../../zoom-apps-sdk/references/layers-api.md)** - All drawing methods
- **[Camera Mode Example](../../zoom-apps-sdk/examples/layers-camera.md)** - Virtual camera overlays
- **Sample app**: https://github.com/zoom/zoomapps-customlayout-js

## Skill Chain

```
zoom-apps-sdk (Layers API)  -->  oauth (authorization)
     |
     v
zoom-rest-api (optional: meeting management)
```

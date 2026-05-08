# Collaborative Apps

Build real-time shared experiences across meeting participants.

## Overview

Collaborative Zoom Apps let multiple participants interact with the same shared state simultaneously - like Google Docs for Zoom meetings. Examples: shared whiteboards, polls, text editors, dashboards.

## Skills Needed

- **zoom-apps-sdk** (Collaborate Mode, App Communication) - Primary
- **oauth** - Authentication

## Synchronization Patterns

| Pattern | Technology | Best For | Complexity |
|---------|-----------|----------|------------|
| **SDK messaging** | connect() + postMessage() | Simple state (counters, toggles) | Low |
| **Server relay** | Socket.io / WebSocket | Polls, games, dashboards | Medium |
| **CRDT sync** | Y.js + WebRTC | Text editors, whiteboards | High |

### Pattern 1: SDK Messaging (Simplest)

No server needed for state sync:

```javascript
await zoomSdk.connect();

// Send state change
await zoomSdk.postMessage({
  payload: JSON.stringify({ type: 'vote', option: 'A' })
});

// Receive state changes
zoomSdk.addEventListener('onMessage', (event) => {
  const data = JSON.parse(event.payload);
  applyChange(data);
});
```

### Pattern 2: Server Relay

Your backend is the source of truth:

```javascript
const socket = io('https://your-server.com');
const { meetingUUID } = await zoomSdk.getMeetingUUID();
socket.emit('join', { room: meetingUUID });

socket.on('state-update', (state) => renderApp(state));
socket.emit('action', { type: 'vote', option: 'A' });
```

### Pattern 3: CRDT (Conflict-Free)

Best for concurrent editing (text, drawings):

```javascript
import * as Y from 'yjs';
import { WebrtcProvider } from 'y-webrtc';

const { meetingUUID } = await zoomSdk.getMeetingUUID();
const ydoc = new Y.Doc();
const provider = new WebrtcProvider(meetingUUID, ydoc);
// Changes sync automatically via CRDT
```

## Meeting UUID as Room ID

Use `getMeetingUUID()` as the room identifier for state synchronization:

```javascript
const { meetingUUID } = await zoomSdk.getMeetingUUID();
// Same UUID for all participants in the same meeting/room
// Different UUID in breakout rooms
```

## Detailed Guides

- **[Collaborate Mode Example](../../zoom-apps-sdk/examples/collaborate-mode.md)** - Complete implementation
- **[App Communication](../../zoom-apps-sdk/examples/app-communication.md)** - Instance messaging
- **[Breakout Rooms](../../zoom-apps-sdk/examples/breakout-rooms.md)** - Cross-room state sync
- **Sample app**: https://github.com/zoom/zoomapps-texteditor-vuejs

## Skill Chain

```
zoom-apps-sdk (Collaborate + Communication)  -->  oauth (authorization)
```

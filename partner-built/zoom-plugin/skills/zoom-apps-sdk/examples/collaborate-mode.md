# Collaborate Mode

Real-time shared app state across all meeting participants.

## Overview

Collaborate mode lets participants share an app experience simultaneously - like Google Docs for Zoom Apps. When one user makes a change, all participants see it in real time.

## Starting Collaborate Mode

```javascript
import zoomSdk from '@zoom/appssdk';

await zoomSdk.config({
  capabilities: [
    'startCollaborate', 'onCollaborateChange',
    'connect', 'postMessage', 'onConnect', 'onMessage',
    'getMeetingUUID'
  ],
  version: '0.16'
});

// Host starts collaborate mode
await zoomSdk.startCollaborate({
  shareScreen: true  // Also share the app screen
});

// Listen for collaborate state changes
zoomSdk.addEventListener('onCollaborateChange', (event) => {
  console.log('Collaborate state changed:', event);
});
```

## State Synchronization Patterns

### Pattern 1: Server Relay (Socket.io)

Best for apps with a backend. Server is the source of truth.

```javascript
// Frontend
const socket = io('https://your-server.com');
const meetingUUID = await zoomSdk.getMeetingUUID();

socket.emit('join-room', { roomId: meetingUUID.meetingUUID });

// Send state changes
function updateState(key, value) {
  socket.emit('state-update', { key, value });
}

// Receive state changes
socket.on('state-update', ({ key, value }) => {
  applyStateChange(key, value);
});
```

### Pattern 2: SDK Message Passing

No server needed. Direct peer messaging via `connect()` + `postMessage()`.

```javascript
// All participants connect
await zoomSdk.connect();

zoomSdk.addEventListener('onConnect', () => {
  console.log('Connected to other instances');
});

// Send state to all connected instances
async function broadcastState(state) {
  await zoomSdk.postMessage({
    payload: JSON.stringify({ type: 'state-sync', data: state })
  });
}

// Receive state from other instances
zoomSdk.addEventListener('onMessage', (event) => {
  const message = JSON.parse(event.payload);
  if (message.type === 'state-sync') {
    applyState(message.data);
  }
});
```

### Pattern 3: CRDT (Y.js)

Best for collaborative editing (text, whiteboards). Conflict-free resolution.

```javascript
import * as Y from 'yjs';
import { WebrtcProvider } from 'y-webrtc';

// Use meeting UUID as room name
const meetingUUID = await zoomSdk.getMeetingUUID();

const ydoc = new Y.Doc();
const provider = new WebrtcProvider(meetingUUID.meetingUUID, ydoc, {
  signaling: ['wss://your-signaling-server.com']
});

// Shared state automatically syncs via CRDT
const sharedMap = ydoc.getMap('app-state');

// Update state (syncs to all peers automatically)
sharedMap.set('counter', (sharedMap.get('counter') || 0) + 1);

// Observe changes
sharedMap.observe((event) => {
  event.keysChanged.forEach((key) => {
    console.log(`${key} changed to:`, sharedMap.get(key));
  });
});
```

**Note:** The texteditor sample app uses public Y.js signaling servers. For production, host your own signaling server.

## Example: Shared Counter

```javascript
import zoomSdk from '@zoom/appssdk';

let count = 0;

async function init() {
  await zoomSdk.config({
    capabilities: ['connect', 'postMessage', 'onConnect', 'onMessage'],
    version: '0.16'
  });

  await zoomSdk.connect();

  zoomSdk.addEventListener('onMessage', (event) => {
    const msg = JSON.parse(event.payload);
    if (msg.type === 'count-update') {
      count = msg.count;
      render();
    }
  });

  render();
}

async function increment() {
  count++;
  render();
  await zoomSdk.postMessage({
    payload: JSON.stringify({ type: 'count-update', count })
  });
}

function render() {
  document.getElementById('counter').textContent = count;
}
```

## Meeting UUID as Room Identifier

Use `getMeetingUUID()` to get a unique room ID for state synchronization:

```javascript
const { meetingUUID } = await zoomSdk.getMeetingUUID();
// Use as Socket.io room, Y.js document name, Redis key, etc.
```

This UUID is unique per meeting instance and consistent across all participants.

## Resources

- **Collaborate docs**: https://developers.zoom.us/docs/zoom-apps/guides/collaborate-mode/
- **Sample app**: https://github.com/zoom/zoomapps-texteditor-vuejs

# App Instance Communication

Sync data between main client and meeting instances using connect() + postMessage().

## Overview

A Zoom App can run two instances simultaneously:
- **Main client instance** (`inMainClient`) - for settings, dashboards
- **Meeting instance** (`inMeeting`) - for in-meeting features

Use `connect()` and `postMessage()` to pass data between them.

## Basic Setup

```javascript
import zoomSdk from '@zoom/appssdk';

await zoomSdk.config({
  capabilities: ['connect', 'postMessage', 'onConnect', 'onMessage'],
  version: '0.16'
});

// Both instances must call connect()
await zoomSdk.connect();

// Know when the other instance connects
zoomSdk.addEventListener('onConnect', (event) => {
  console.log('Other instance connected');
});

// Send a message
await zoomSdk.postMessage({
  payload: JSON.stringify({ type: 'greeting', data: 'Hello from this instance!' })
});

// Receive messages
zoomSdk.addEventListener('onMessage', (event) => {
  const message = JSON.parse(event.payload);
  console.log('Received:', message.type, message.data);
});
```

## Pattern: Pre-Meeting Settings

Configure settings in the main client, use them during the meeting.

### Main Client Instance

```javascript
// Running in inMainClient context
const config = await zoomSdk.config({
  capabilities: ['connect', 'postMessage', 'onConnect', 'onMessage', 'getRunningContext'],
  version: '0.16'
});

if (config.runningContext === 'inMainClient') {
  await zoomSdk.connect();

  // User configures settings
  const settings = {
    theme: 'dark',
    language: 'en',
    notifications: true
  };

  // When meeting instance asks for settings, send them
  zoomSdk.addEventListener('onMessage', async (event) => {
    const msg = JSON.parse(event.payload);
    if (msg.type === 'request-settings') {
      await zoomSdk.postMessage({
        payload: JSON.stringify({ type: 'settings', data: settings })
      });
    }
  });
}
```

### Meeting Instance

```javascript
// Running in inMeeting context
if (config.runningContext === 'inMeeting') {
  await zoomSdk.connect();

  let settings = null;

  zoomSdk.addEventListener('onMessage', (event) => {
    const msg = JSON.parse(event.payload);
    if (msg.type === 'settings') {
      settings = msg.data;
      applySettings(settings);
    }
  });

  // Request settings from main client instance
  zoomSdk.addEventListener('onConnect', async () => {
    await zoomSdk.postMessage({
      payload: JSON.stringify({ type: 'request-settings' })
    });
  });
}
```

## Message Protocol

Define a consistent message format:

```javascript
// Message types
const MessageType = {
  REQUEST_SETTINGS: 'request-settings',
  SETTINGS: 'settings',
  STATE_UPDATE: 'state-update',
  ACTION: 'action'
};

// Send helper
async function send(type, data = {}) {
  await zoomSdk.postMessage({
    payload: JSON.stringify({ type, data, timestamp: Date.now() })
  });
}

// Receive handler
zoomSdk.addEventListener('onMessage', (event) => {
  const { type, data } = JSON.parse(event.payload);

  switch (type) {
    case MessageType.REQUEST_SETTINGS:
      send(MessageType.SETTINGS, currentSettings);
      break;
    case MessageType.STATE_UPDATE:
      applyState(data);
      break;
    case MessageType.ACTION:
      handleAction(data);
      break;
  }
});
```

## Important Notes

- Messages are JSON strings (must stringify/parse)
- Both instances must call `connect()` independently
- `onConnect` fires when the other instance connects
- Messages are one-to-one (not broadcast to all participants)
- If one instance isn't running, messages are lost (no queue)

## Resources

- **In-client experience**: https://developers.zoom.us/docs/zoom-apps/guides/in-client-experience/

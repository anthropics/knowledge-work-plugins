# Running Contexts

## Overview

A Zoom App can run in multiple surfaces within the Zoom client. The `runningContext` property returned by `config()` tells you where your app is currently loaded.

```javascript
const configResponse = await zoomSdk.config({
  capabilities: ['getMeetingContext', 'getUserContext', ...],
  version: '0.16'
});

console.log(configResponse.runningContext);
// 'inMeeting' | 'inMainClient' | 'inWebinar' | 'inImmersive' | ...
```

## All Running Contexts

| Context | Surface | Meeting APIs | User APIs | Layers APIs | Notes |
|---------|---------|-------------|-----------|-------------|-------|
| `inMeeting` | Meeting sidebar | Yes | Yes | Yes | Most common context |
| `inMainClient` | Main client panel | No | Yes | No | Home tab, no meeting running |
| `inWebinar` | Webinar sidebar | Yes | Yes | Yes | Host/panelist initially |
| `inImmersive` | Layers full-screen | Limited | Yes | Yes | After runRenderingContext |
| `inCamera` | Camera mode | Limited | Yes | Camera only | Virtual camera overlay |
| `inCollaborate` | Collaborate mode | Yes | Yes | No | Shared state context |
| `inPhone` | Zoom Phone | No | Yes | No | Phone call app surface |
| `inChat` | Team Chat | No | Yes | No | Chat sidebar |

## Context-Specific Behavior

### inMeeting (Most Common)

The primary context. Your app appears as a sidebar panel during a meeting.

```javascript
if (configResponse.runningContext === 'inMeeting') {
  const meeting = await zoomSdk.getMeetingContext();
  console.log('Meeting ID:', meeting.meetingID);
  console.log('Topic:', meeting.meetingTopic);

  const user = await zoomSdk.getUserContext();
  console.log('Name:', user.screenName);
  console.log('Role:', user.role); // 'host' | 'coHost' | 'attendee'
}
```

Available: All meeting APIs, sharing, invitations, breakout rooms, recording.

### inMainClient

Your app runs in the main Zoom window (not during a meeting). Used for dashboards, settings, pre-meeting setup.

```javascript
if (configResponse.runningContext === 'inMainClient') {
  // NO meeting APIs available - getMeetingContext() will fail
  const user = await zoomSdk.getUserContext();
  console.log('Name:', user.screenName);

  // Can still use connect() to sync with meeting instance later
}
```

**Key limitation:** No meeting context, no participants, no sharing.

### inWebinar

Similar to inMeeting but for webinars. Initially only available to host and panelists.

```javascript
if (configResponse.runningContext === 'inWebinar') {
  const user = await zoomSdk.getUserContext();
  // role: 'host' | 'panelist' | 'attendee'
  if (user.role === 'attendee') {
    // Limited functionality for attendees
  }
}
```

### inImmersive / inCamera

Layers API contexts. Your app has taken over the video rendering.

- `inImmersive`: Full-screen custom layout (replaces gallery view)
- `inCamera`: Overlay on user's camera feed

See [Layers API Reference](../references/layers-api.md) for details.

## Multiple Instances

A Zoom App can have **two instances running simultaneously**:

1. **Main client instance** (`inMainClient`) - Always available
2. **Meeting instance** (`inMeeting`) - Created when user opens app in meeting

### Instance Communication

Use `connect()` and `postMessage()` to sync between instances:

```javascript
// Both instances call connect()
await zoomSdk.connect();

// Listen for connection
zoomSdk.addEventListener('onConnect', (event) => {
  console.log('Connected to other instance');
});

// Send data to other instance
await zoomSdk.postMessage({ type: 'settings', data: mySettings });

// Receive data from other instance
zoomSdk.addEventListener('onMessage', (event) => {
  const { type, data } = JSON.parse(event.payload);
  if (type === 'settings') {
    applySettings(data);
  }
});
```

**Pattern: Pre-Meeting Setup**

```
Main Client Instance              Meeting Instance
─────────────────────             ─────────────────
User configures settings    -->   connect() + listen
Store in state              -->   onConnect fires
                                  postMessage('getSettings')
onMessage('getSettings')    -->
postMessage(settings)       -->   onMessage(settings)
                                  Apply settings to meeting
```

## Detecting Context at Runtime

```javascript
import zoomSdk from '@zoom/appssdk';

async function init() {
  const config = await zoomSdk.config({
    capabilities: [
      'getMeetingContext', 'getUserContext', 'getRunningContext',
      'connect', 'postMessage', 'onConnect', 'onMessage',
      'shareApp', 'runRenderingContext'
    ],
    version: '0.16'
  });

  switch (config.runningContext) {
    case 'inMeeting':
    case 'inWebinar':
      initMeetingUI();
      break;
    case 'inMainClient':
      initDashboardUI();
      break;
    case 'inImmersive':
    case 'inCamera':
      initLayersUI();
      break;
    default:
      initFallbackUI();
  }
}
```

## Checking API Availability

Not all APIs are available in all contexts. Use `getSupportedJsApis()` to check:

```javascript
const { supportedApis } = await zoomSdk.getSupportedJsApis();

if (supportedApis.includes('authorize')) {
  // In-Client OAuth is available
  showAuthButton();
}

if (supportedApis.includes('runRenderingContext')) {
  // Layers API is available
  showLayersButton();
}
```

Also check `configResponse.unsupportedApis` after `config()` for capabilities that were requested but not available in the current client version.

## Resources

- **Running contexts docs**: https://developers.zoom.us/docs/zoom-apps/guides/in-client-experience/
- **Instance communication**: https://developers.zoom.us/docs/zoom-apps/guides/collaborate-mode/

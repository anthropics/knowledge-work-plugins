# Zoom Apps SDK - Events Reference

Subscribe to events to respond to meeting, user, and app state changes.

**IMPORTANT**: Register event listeners AFTER successful `zoomSdk.config()` call. Events must be listed in the `capabilities` array.

## Subscribing to Events

```javascript
import zoomSdk from '@zoom/appssdk';

await zoomSdk.config({
  capabilities: ['onMeeting', 'onParticipantChange', 'onAuthorized', ...],
  version: '0.16'
});

zoomSdk.addEventListener('onMeeting', (event) => {
  console.log('Meeting event:', event);
});
```

## Meeting Events

### onMeeting

Meeting lifecycle changes (start, end, etc.).

```javascript
zoomSdk.addEventListener('onMeeting', (event) => {
  // event: { action: 'started' | 'ended' | ... }
});
```

### onParticipantChange

Participants join or leave.

```javascript
zoomSdk.addEventListener('onParticipantChange', (event) => {
  const { participants, action } = event;
  // action: 'join' | 'leave'
  // participants: [{ participantId, screenName, role }]
});
```

### onActiveSpeakerChange

Active speaker changes.

```javascript
zoomSdk.addEventListener('onActiveSpeakerChange', (event) => {
  const { participantId, screenName } = event;
});
```

### onBreakoutRoomChange

User moves between breakout rooms.

```javascript
zoomSdk.addEventListener('onBreakoutRoomChange', (event) => {
  // Re-fetch meeting UUID and state for new room
});
```

## User Events

### onMyUserContextChange

Current user's context changes (role, name, mute status, etc.).

```javascript
zoomSdk.addEventListener('onMyUserContextChange', (event) => {
  const { role, screenName } = event;
});
```

### onMyMediaChange

Current user's audio/video status changes.

```javascript
zoomSdk.addEventListener('onMyMediaChange', (event) => {
  const { audio, video } = event;
  // audio: { muted: true/false }
  // video: { started: true/false }
});
```

## App Events

### onShareApp

App sharing status changes.

```javascript
zoomSdk.addEventListener('onShareApp', (event) => {
  const { isShared } = event;
});
```

### onAppPopout

App popped out to separate window or back.

```javascript
zoomSdk.addEventListener('onAppPopout', (event) => {
  const { isPopout } = event;
});
```

### onRunningContextChange

Running context changes (e.g., meeting starts while in main client).

```javascript
zoomSdk.addEventListener('onRunningContextChange', (event) => {
  const { runningContext } = event;
});
```

## Authorization Events

### onAuthorized

In-Client OAuth authorization completed.

```javascript
zoomSdk.addEventListener('onAuthorized', (event) => {
  const { code, state } = event;
  // Send code to backend for token exchange
});
```

## Communication Events

### onConnect

Another app instance connected.

```javascript
zoomSdk.addEventListener('onConnect', (event) => {
  console.log('Other instance connected');
});
```

### onMessage

Message received from connected instance.

```javascript
zoomSdk.addEventListener('onMessage', (event) => {
  const data = JSON.parse(event.payload);
});
```

## Collaborate Events

### onCollaborateChange

Collaborate mode state changes.

```javascript
zoomSdk.addEventListener('onCollaborateChange', (event) => {
  console.log('Collaborate state:', event);
});
```

## Layers Events

### onRenderedAppOpened

Immersive/camera rendering context opened.

```javascript
zoomSdk.addEventListener('onRenderedAppOpened', (event) => {
  console.log('Rendering context ready');
});
```

## Reaction Events

### onReaction

Participant sends a reaction.

```javascript
zoomSdk.addEventListener('onReaction', (event) => {
  const { participantId, reaction } = event;
});
```

## Removing Listeners

```javascript
const handler = (event) => { ... };
zoomSdk.addEventListener('onMeeting', handler);

// Later, remove it
zoomSdk.removeEventListener('onMeeting', handler);
```

## Resources

- **Events reference**: https://appssdk.zoom.us/

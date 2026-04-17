# Zoom Apps SDK - API Reference

Complete reference for all @zoom/appssdk methods organized by category.

## Initialization

### config(options)

**Must be called first.** Initializes the SDK and declares capabilities.

```javascript
const configResponse = await zoomSdk.config({
  capabilities: ['getMeetingContext', 'shareApp', ...],
  version: '0.16'
});
// Returns: { runningContext, clientVersion, unsupportedApis }
```

### getSupportedJsApis()

Check which APIs are available in the current client.

```javascript
const { supportedApis } = await zoomSdk.getSupportedJsApis();
// Returns: { supportedApis: ['getMeetingContext', 'shareApp', ...] }
```

## Context APIs

### getMeetingContext()

```javascript
const context = await zoomSdk.getMeetingContext();
// { meetingID, meetingTopic, meetingStatus }
```

### getUserContext()

```javascript
const user = await zoomSdk.getUserContext();
// { screenName, role, participantId, status }
// role: 'host' | 'coHost' | 'attendee' | 'panelist'
// status: 'authorized' | 'authenticated' | 'unauthenticated'
```

### getRunningContext()

```javascript
const { context } = await zoomSdk.getRunningContext();
// 'inMeeting' | 'inMainClient' | 'inWebinar' | 'inImmersive' | ...
```

### getMeetingUUID()

```javascript
const { meetingUUID } = await zoomSdk.getMeetingUUID();
```

### getMeetingJoinUrl()

```javascript
const { joinUrl } = await zoomSdk.getMeetingJoinUrl();
```

### getMeetingParticipants()

```javascript
const { participants } = await zoomSdk.getMeetingParticipants();
// [{ participantId, participantUUID, screenName, role }]
```

### getRecordingContext()

```javascript
const recording = await zoomSdk.getRecordingContext();
// { cloudRecordingStatus, localRecordingStatus }
```

## Authorization APIs

### authorize(options)

Trigger In-Client OAuth (no browser redirect).

```javascript
await zoomSdk.authorize({ codeChallenge: '...', state: '...' });
// onAuthorized event fires with { code, state }
```

### promptAuthorize()

Prompt guest/authenticated users to authorize.

```javascript
await zoomSdk.promptAuthorize();
```

## Meeting Action APIs

### shareApp()

```javascript
await zoomSdk.shareApp();
```

### sendAppInvitation(options)

```javascript
await zoomSdk.sendAppInvitation({ participantUUIDs: ['uuid1'], action: 'open' });
```

### sendAppInvitationToAllParticipants()

```javascript
await zoomSdk.sendAppInvitationToAllParticipants();
```

### sendAppInvitationToMeetingOwner()

```javascript
await zoomSdk.sendAppInvitationToMeetingOwner();
```

### showAppInvitationDialog()

```javascript
await zoomSdk.showAppInvitationDialog();
```

## UI APIs

### expandApp(options)

```javascript
await zoomSdk.expandApp({ action: 'expand' }); // or 'collapse'
```

### openUrl(options)

```javascript
await zoomSdk.openUrl({ url: 'https://example.com' });
```

### showNotification(options)

```javascript
await zoomSdk.showNotification({ title: 'Alert', message: 'Something happened!', type: 'info' });
```

## Media APIs

### listCameras()

```javascript
const { cameras } = await zoomSdk.listCameras();
```

### setVirtualBackground(options)

```javascript
await zoomSdk.setVirtualBackground({ imageData: 'base64-data' });
```

### removeVirtualBackground()

```javascript
await zoomSdk.removeVirtualBackground();
```

### setVideoMirrorEffect(options)

```javascript
await zoomSdk.setVideoMirrorEffect({ mirrorMyVideo: true });
```

### allowParticipantToRecord(options)

```javascript
await zoomSdk.allowParticipantToRecord({ participantUUID: 'uuid', action: 'grant' });
```

### cloudRecording(options)

```javascript
await zoomSdk.cloudRecording({ action: 'start' }); // 'stop', 'pause', 'resume'
```

## Communication APIs

### connect()

Connect to other app instances (main client <-> meeting).

```javascript
await zoomSdk.connect();
```

### postMessage(options)

```javascript
await zoomSdk.postMessage({ payload: JSON.stringify({ type: 'update', data: {...} }) });
```

## Layers APIs

### runRenderingContext(options)

```javascript
await zoomSdk.runRenderingContext({ view: 'immersive' }); // or 'camera'
```

### closeRenderingContext()

```javascript
await zoomSdk.closeRenderingContext();
```

### drawParticipant(options)

```javascript
await zoomSdk.drawParticipant({ participantUUID: 'uuid', x: 0, y: 0, width: 640, height: 480, zIndex: 1 });
```

### clearParticipant(options)

```javascript
await zoomSdk.clearParticipant({ participantUUID: 'uuid' });
```

### drawImage(options)

```javascript
await zoomSdk.drawImage({ imageData: canvas.toDataURL(), x: 0, y: 0, width: 1280, height: 720, zIndex: 0 });
```

### clearImage(options)

```javascript
await zoomSdk.clearImage({ imageId: 'id' });
```

### drawWebView(options)

```javascript
await zoomSdk.drawWebView({ webviewId: 'my-view', x: 0, y: 0, width: 400, height: 300, zIndex: 2 });
```

### clearWebView(options)

```javascript
await zoomSdk.clearWebView({ webviewId: 'my-view' });
```

## Collaborate APIs

### startCollaborate(options)

```javascript
await zoomSdk.startCollaborate({ shareScreen: true });
```

## Event Listeners

```javascript
zoomSdk.addEventListener('onMeeting', (event) => { ... });
zoomSdk.removeEventListener('onMeeting', handler);
```

See **[events.md](events.md)** for complete event reference.

## Resources

- **SDK Reference**: https://appssdk.zoom.us/
- **Capabilities list**: https://developers.zoom.us/docs/zoom-apps/

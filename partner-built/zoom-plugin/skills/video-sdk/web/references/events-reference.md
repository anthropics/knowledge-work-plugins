# Events Reference

Complete reference for all events in the Zoom Video SDK for Web.

## Event Registration

```javascript
// Register
client.on('event-name', (payload) => { /* handle */ });

// Unregister
client.off('event-name', handler);
```

---

## Session Events

### connection-change

Fired when connection state changes.

```typescript
client.on('connection-change', (payload: {
  state: 'Connected' | 'Connecting' | 'Reconnecting' | 'Closed' | 'Fail';
  reason?: string;
}) => {});
```

| State | Description |
|-------|-------------|
| `Connected` | Successfully connected to session |
| `Connecting` | Attempting to connect |
| `Reconnecting` | Lost connection, attempting reconnect |
| `Closed` | Disconnected from session |
| `Fail` | Connection failed |

---

## Participant Events

### user-added

Fired when participant(s) join the session.

```typescript
client.on('user-added', (payload: Participant[]) => {});

interface Participant {
  userId: number;
  displayName: string;
  avatar?: string;
  isHost: boolean;
  isManager: boolean;
  bVideoOn: boolean;
  muted: boolean;
  // ... more properties
}
```

### user-removed

Fired when participant(s) leave the session.

```typescript
client.on('user-removed', (payload: Participant[]) => {});
```

### user-updated

Fired when participant properties change (name, mute, video, etc.).

```typescript
client.on('user-updated', (payload: Participant[]) => {});
```

---

## Video Events

### peer-video-state-change

Fired when a remote participant starts or stops video.

```typescript
client.on('peer-video-state-change', (payload: {
  action: 'Start' | 'Stop';
  userId: number;
}) => {});
```

**Critical**: Use this to render/remove remote videos.

### video-capturing-change

Fired when local video capture state changes.

```typescript
client.on('video-capturing-change', (payload: {
  state: 'Started' | 'Stopped' | 'Failed';
}) => {});
```

### video-active-change

Fired when video becomes active/inactive.

```typescript
client.on('video-active-change', (payload: {
  state: VideoActiveState;
  userId: number;
}) => {});
```

### video-dimension-change

Fired when received video dimensions change.

```typescript
client.on('video-dimension-change', (payload: {
  width: number;
  height: number;
  type: 'received';
}) => {});
```

### video-detailed-data-change

Fired when video quality details change.

```typescript
client.on('video-detailed-data-change', (payload: {
  userId: number;
  width?: number;
  height?: number;
  fps?: number;
  quality?: VideoQuality;
}) => {});
```

### video-spotlight-change

Fired when spotlight list changes.

```typescript
client.on('video-spotlight-change', (payload: {
  spotlightList: { userId: number }[];
}) => {});
```

---

## Audio Events

### current-audio-change

Fired when local audio state changes.

```typescript
client.on('current-audio-change', (payload: {
  action: 'join' | 'leave' | 'muted' | 'unmuted';
  type?: 'computer' | 'phone';
  source?: MutedSource | LeaveAudioSource;
}) => {});
```

| Action | Description |
|--------|-------------|
| `join` | Joined audio (computer or phone) |
| `leave` | Left audio |
| `muted` | Audio muted |
| `unmuted` | Audio unmuted |

| Source | Description |
|--------|-------------|
| `active` | User action |
| `passive(mute all)` | Host muted all |
| `passive(mute one)` | Host muted you |
| `passive` | Host unmuted you |

### host-ask-unmute-audio

Fired when host asks you to unmute.

```typescript
client.on('host-ask-unmute-audio', (payload: {
  reason: 'Unmute' | 'Spotlight' | 'Allow to talk';
}) => {});
```

### active-speaker

Fired when active speakers change.

```typescript
client.on('active-speaker', (payload: {
  userId: number;
  displayName: string;
}[]) => {});
```

Array is sorted by volume (loudest first).

### auto-play-audio-failed

Fired when browser blocks audio autoplay.

```typescript
client.on('auto-play-audio-failed', () => {});
```

### current-audio-level-change

Fired when local audio level changes.

```typescript
client.on('current-audio-level-change', (payload: {
  level: number;
}) => {});
```

### speaking-while-muted

Fired when speaking while muted is detected.

```typescript
client.on('speaking-while-muted', () => {});
```

---

## Screen Share Events

### active-share-change

Fired when someone starts/stops sharing.

```typescript
client.on('active-share-change', (payload: {
  state: 'Active' | 'Inactive';
  userId: number;
}) => {});
```

### peer-share-state-change

Fired when peer share state changes.

```typescript
client.on('peer-share-state-change', (payload: {
  action: 'Start' | 'Stop';
  userId: number;
}) => {});
```

### passively-stop-share

Fired when you're forced to stop sharing.

```typescript
client.on('passively-stop-share', (payload: PassiveStopShareReason) => {});

// Reasons: 'PrivilegeChange', 'AnotherShareStarted', etc.
```

### share-content-change

Fired when sharer switches windows/tabs.

```typescript
client.on('share-content-change', (payload: {
  userId: number;
}) => {});
```

### share-content-dimension-change

Fired when share dimensions change.

```typescript
client.on('share-content-dimension-change', (payload: {
  width: number;
  height: number;
  type: 'received' | 'sended';
}) => {});
```

### share-privilege-change

Fired when share privilege changes.

```typescript
client.on('share-privilege-change', (payload: {
  privilege: SharePrivilege;
}) => {});
```

### share-audio-change

Fired when share audio state changes.

```typescript
client.on('share-audio-change', (payload: {
  state: 'on' | 'off';
}) => {});
```

---

## Chat Events

### chat-on-message

Fired when a chat message is received.

```typescript
client.on('chat-on-message', (payload: {
  id: string;
  message: string;
  sender: { userId: number; name: string; avatar?: string };
  receiver: { userId: number; name: string } | 'everyone';
  timestamp: number;
  isPrivate: boolean;
}) => {});
```

### chat-privilege-change

Fired when chat privilege changes.

```typescript
client.on('chat-privilege-change', (payload: {
  chatPrivilege: ChatPrivilege;
}) => {});
```

### chat-file-upload-progress

Fired during file upload.

```typescript
client.on('chat-file-upload-progress', (payload: {
  fileName: string;
  fileSize: number;
  progress: number;
  status: ChatFileUploadStatus;
  receiverId: number;
  retryToken?: string;
}) => {});
```

### chat-file-download-progress

Fired during file download.

```typescript
client.on('chat-file-download-progress', (payload: {
  fileName: string;
  fileSize: number;
  progress: number;
  status: ChatFileDownloadStatus;
  fileUrl: string;
  fileBlob?: Blob;
  senderId: number;
}) => {});
```

---

## Recording Events

### recording-change

Fired when cloud recording state changes.

```typescript
client.on('recording-change', (payload: {
  state: RecordingStatus;
}) => {});
```

| Status | Description |
|--------|-------------|
| `Recording` | Recording in progress |
| `Paused` | Recording paused |
| `Stopped` | Recording stopped |

### individual-recording-change

Fired for individual recording consent.

```typescript
client.on('individual-recording-change', (payload: {
  state: RecordingStatus | 'Ask' | 'Accept' | 'Decline';
  userId?: number;
}) => {});
```

---

## Live Transcription Events

### caption-message

Fired when transcription text is received.

```typescript
client.on('caption-message', (payload: {
  msgId: string;
  text: string;
  userId: number;
  displayName: string;
  source: 'caption' | 'translation';
  language: string;
  done: boolean;  // true = final, false = interim
  timestamp: number;
}) => {});
```

### caption-status

Fired when caption status changes.

```typescript
client.on('caption-status', (payload: {
  autoCaption: boolean;
  language?: string;
  lang?: number;
  sessionLanguage?: string;
  translationStarted?: boolean;
}) => {});
```

### caption-enable

Fired when captions are enabled/disabled.

```typescript
client.on('caption-enable', (isEnabled: boolean) => {});
```

### caption-language-lock

Fired when language is locked/unlocked.

```typescript
client.on('caption-language-lock', (isLocked: boolean) => {});
```

### caption-host-disable

Fired when host disables captions.

```typescript
client.on('caption-host-disable', (isDisabled: boolean) => {});
```

---

## Device Events

### device-change

Fired when devices are added/removed.

```typescript
client.on('device-change', () => {});
```

### device-permission-change

Fired when device permissions change.

```typescript
client.on('device-permission-change', (payload: {
  name: 'microphone' | 'camera';
  state: 'granted' | 'denied' | 'prompt';
}) => {});
```

---

## Network & Quality Events

### network-quality-change

Fired when network quality changes.

```typescript
client.on('network-quality-change', (payload: {
  userId: number;
  type: 'uplink' | 'downlink';
  level: number;  // 0-5 (0=unknown, 1=bad, 5=excellent)
}) => {});
```

### video-statistic-data-change

Fired when video statistics change.

```typescript
client.on('video-statistic-data-change', (payload: {
  type: 'VIDEO_QOS_DATA';
  data: {
    encoding: boolean;  // true=send, false=receive
    width: number;
    height: number;
    fps: number;
    bitrate: number;
    avg_loss: number;
    max_loss: number;
    jitter: number;
    rtt: number;
  };
}) => {});
```

### audio-statistic-data-change

Fired when audio statistics change.

```typescript
client.on('audio-statistic-data-change', (payload: {
  type: 'AUDIO_QOS_DATA';
  data: {
    encoding: boolean;
    bitrate: number;
    avg_loss: number;
    max_loss: number;
    jitter: number;
    rtt: number;
    sample_rate: number;
  };
}) => {});
```

---

## Command Channel Events

### command-channel-status

Fired when command channel status changes.

```typescript
client.on('command-channel-status', (payload: ConnectionState) => {});
```

### command-channel-message

Fired when command channel message is received.

```typescript
client.on('command-channel-message', (payload: {
  msgid: string;
  senderId: string;
  senderName: string;
  text: string;
  timestamp: number;
}) => {});
```

---

## Live Stream Events

### live-stream-status

Fired when live stream status changes.

```typescript
client.on('live-stream-status', (status: LiveStreamStatus) => {});
```

---

## Far End Camera Control Events

### far-end-camera-request-control

Fired when someone requests camera control.

```typescript
client.on('far-end-camera-request-control', (payload: {
  userId: number;
  displayName: string;
  currentControllingUserId?: number;
  currentControllingDisplayName?: string;
}) => {});
```

### far-end-camera-response-control

Fired with camera control response.

```typescript
client.on('far-end-camera-response-control', (payload: {
  userId: number;
  displayName: string;
  isApproved: boolean;
  reason?: FarEndCameraControlDeclinedReason;
}) => {});
```

### far-end-camera-capability-change

Fired when camera capabilities change.

```typescript
client.on('far-end-camera-capability-change', (payload: {
  userId: number;
  ptz: PTZCameraCapability;
}) => {});
```

---

## Subsession Events

### subsession-invite-to-join

Fired when invited to join subsession.

```typescript
client.on('subsession-invite-to-join', (payload: {
  subsessionId: string;
  subsessionName: string;
}) => {});
```

### subsession-broadcast-message

Fired when broadcast message received.

```typescript
client.on('subsession-broadcast-message', (payload: {
  message: string;
}) => {});
```

### subsession-state-change

Fired when subsession state changes.

```typescript
client.on('subsession-state-change', (payload: {
  status: SubsessionStatus;
}) => {});
```

---

## Whiteboard Events

### whiteboard-status-change

Fired when whiteboard status changes.

```typescript
client.on('whiteboard-status-change', (status: WhiteboardStatus) => {});
```

### peer-whiteboard-state-change

Fired when peer whiteboard state changes.

```typescript
client.on('peer-whiteboard-state-change', (payload: {
  action: 'Start' | 'Stop';
  userId: number;
}) => {});
```

---

## Event Categories Quick Reference

| Category | Events |
|----------|--------|
| **Session** | `connection-change` |
| **Participants** | `user-added`, `user-removed`, `user-updated` |
| **Video** | `peer-video-state-change`, `video-capturing-change`, `video-dimension-change`, `video-active-change` |
| **Audio** | `current-audio-change`, `host-ask-unmute-audio`, `active-speaker`, `auto-play-audio-failed` |
| **Share** | `active-share-change`, `passively-stop-share`, `share-privilege-change`, `share-content-change` |
| **Chat** | `chat-on-message`, `chat-privilege-change`, `chat-file-*-progress` |
| **Recording** | `recording-change`, `individual-recording-change` |
| **Transcription** | `caption-message`, `caption-status`, `caption-enable` |
| **Device** | `device-change`, `device-permission-change` |
| **Network** | `network-quality-change`, `*-statistic-data-change` |

---

## Related Documentation

- [Event Handling Examples](../examples/event-handling.md)
- [API Reference](web-reference.md)

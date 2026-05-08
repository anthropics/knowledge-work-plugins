# Zoom Video SDK Web - API Reference

## Overview

This reference provides the complete API for the Zoom Video SDK for Web. The SDK follows a hierarchical pattern:

```
ZoomVideo (module)
  └── VideoClient (singleton)
      ├── Stream (media operations)
      └── Feature Clients (chat, recording, etc.)
```

**Official API Reference**: https://marketplacefront.zoom.us/sdk/custom/web/modules.html

---

## Level 0: ZoomVideo Module

### Static Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `createClient()` | `VideoClient` | Creates/returns the singleton client |
| `destroyClient()` | `Promise<void>` | Destroys the client instance |
| `checkSystemRequirements()` | `MediaCompatibility` | Check browser compatibility |
| `checkFeatureRequirements()` | `SupportFeatures` | Check feature support |
| `getDevices(skip?)` | `Promise<MediaDeviceInfo[]>` | Enumerate media devices |
| `preloadDependentAssets(path?)` | `void` | Preload SDK assets |
| `createLocalVideoTrack(id?)` | `LocalVideoTrack` | Create local video track for preview |
| `createLocalAudioTrack(id?)` | `LocalAudioTrack` | Create local audio track for preview |
| `VERSION` | `string` | SDK version |

### MediaCompatibility Interface

```typescript
interface MediaCompatibility {
  audio: boolean;   // Audio support
  video: boolean;   // Video support
  screen: boolean;  // Screen share support
}
```

### SupportFeatures Interface

```typescript
interface SupportFeatures {
  platform: string;           // Browser/platform info
  supportFeatures: string[];  // Supported features
  unSupportFeatures: string[]; // Unsupported features
}
```

---

## Level 1: VideoClient

### Session Lifecycle

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `init` | `(language, dependentAssets, options?)` | `ExecutedResult` | Initialize SDK |
| `join` | `(topic, token, userName, password?, timeout?)` | `ExecutedResult` | Join session |
| `leave` | `(end?)` | `ExecutedResult` | Leave/end session |
| `on` | `(event, callback)` | `void` | Subscribe to events |
| `off` | `(event, callback)` | `void` | Unsubscribe from events |

### InitOptions Interface

```typescript
interface InitOptions {
  patchJsMedia?: boolean;      // Patch JS media (recommended: true)
  webrtc?: boolean;            // Enable WebRTC mode for HD
  enforceMultipleVideos?: boolean; // Force multi-video mode
  stayAwake?: boolean;         // Prevent screen sleep
}
```

### Participant Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getAllUser()` | `Participant[]` | Get all participants |
| `getCurrentUserInfo()` | `Participant` | Get current user |
| `getUser(userId)` | `Participant \| undefined` | Get user by ID |
| `getSessionHost()` | `Participant \| undefined` | Get session host |
| `getSessionInfo()` | `SessionInfo` | Get session info |
| `isHost()` | `boolean` | Is current user host |
| `isManager()` | `boolean` | Is current user manager |
| `isOriginalHost()` | `boolean` | Is current user original host |

### Host Controls

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `makeHost` | `(userId)` | `ExecutedResult` | Make user host |
| `makeManager` | `(userId)` | `ExecutedResult` | Make user manager |
| `revokeManager` | `(userId)` | `ExecutedResult` | Remove manager |
| `removeUser` | `(userId)` | `ExecutedResult` | Remove user from session |
| `changeName` | `(name, userId?)` | `ExecutedResult` | Change display name |
| `reclaimHost` | `()` | `ExecutedResult` | Reclaim host (original host only) |

### Feature Client Getters

| Method | Returns | Description |
|--------|---------|-------------|
| `getMediaStream()` | `Stream` | Get media stream (AFTER join!) |
| `getChatClient()` | `ChatClient` | Get chat client |
| `getCommandClient()` | `CommandChannel` | Get command channel |
| `getRecordingClient()` | `RecordingClient` | Get recording client |
| `getLiveTranscriptionClient()` | `LiveTranscriptionClient` | Get transcription client |
| `getLiveStreamClient()` | `LiveStreamClient` | Get live stream client |
| `getSubsessionClient()` | `SubsessionClient` | Get subsession client |
| `getWhiteboardClient()` | `WhiteboardClient` | Get whiteboard client |
| `getBroadcastStreamingClient()` | `BroadcastStreamingClient` | Get broadcast client |
| `getRealTimeMediaStreamsClient()` | `RealTimeMediaStreamsClient` | Get RTMS client |
| `getLoggerClient(options?)` | `LoggerClient` | Get logger client |

### Participant Interface

```typescript
interface Participant {
  userId: number;           // Unique user ID
  displayName: string;      // Display name
  bVideoOn: boolean;        // Is video on
  muted: boolean;           // Is audio muted
  audio: '' | 'computer' | 'phone';  // Audio type
  sharerOn: boolean;        // Is sharing screen
  bShareAudioOn: boolean;   // Is sharing audio
  isHost: boolean;          // Is host
}
```

---

## Level 2: Stream (Media Operations)

### Video Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `startVideo` | `(options?)` | `ExecutedResult` | Start camera |
| `stopVideo` | `()` | `ExecutedResult` | Stop camera |
| `attachVideo` | `(userId, quality, element?)` | `Promise<VideoPlayer>` | Attach video to DOM |
| `detachVideo` | `(userId, element?)` | `Promise<VideoPlayer \| VideoPlayer[]>` | Detach video |
| `switchCamera` | `(cameraId)` | `ExecutedResult` | Switch camera |
| `getCameraList` | `()` | `MediaDevice[]` | Get cameras |
| `getActiveCamera` | `()` | `string` | Get active camera ID |
| `mirrorVideo` | `(enable)` | `ExecutedResult` | Mirror video |
| `spotlightVideo` | `(userId)` | `ExecutedResult` | Spotlight user |
| `screenshotVideo` | `(userId?)` | `Promise<Blob>` | Screenshot video |

### Video Capability Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `isSupportHDVideo()` | `boolean` | Is HD video supported |
| `getVideoMaxQuality()` | `VideoQuality` | Get max video quality |
| `getMaxRenderableVideos()` | `number` | Max renderable videos |
| `isSupportMultipleVideos()` | `boolean` | Multiple videos support |
| `isSupportVirtualBackground()` | `boolean` | Virtual BG support |
| `isCapturingVideo()` | `boolean` | Is capturing video |

### VideoQuality Enum

```typescript
enum VideoQuality {
  Video_90P = 0,
  Video_180P = 1,
  Video_360P = 2,
  Video_720P = 3,
  Video_1080P = 4
}
```

### Virtual Background Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `updateVirtualBackgroundImage` | `(image)` | `ExecutedResult` | Set virtual background |
| `previewVirtualBackground` | `(canvas, image)` | `ExecutedResult` | Preview virtual BG |
| `stopPreviewVirtualBackground` | `()` | `ExecutedResult` | Stop preview |
| `getVirtualbackgroundStatus` | `()` | `VirtualBackgroundStatus` | Get VB status |

**Virtual Background Options:**
- `'blur'`: Blur background
- `'https://example.com/image.jpg'`: Custom image URL
- `undefined`: Remove virtual background

### Audio Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `startAudio` | `(options?)` | `ExecutedResult` | Start audio |
| `stopAudio` | `()` | `ExecutedResult` | Stop audio |
| `muteAudio` | `(userId?)` | `ExecutedResult` | Mute audio |
| `unmuteAudio` | `(userId?)` | `ExecutedResult` | Unmute audio |
| `muteAllAudio` | `()` | `ExecutedResult` | Mute all (host) |
| `unmuteAllAudio` | `()` | `ExecutedResult` | Unmute all (host) |
| `switchMicrophone` | `(micId)` | `ExecutedResult` | Switch microphone |
| `switchSpeaker` | `(speakerId)` | `ExecutedResult` | Switch speaker |
| `getMicList` | `()` | `MediaDevice[]` | Get microphones |
| `getSpeakerList` | `()` | `MediaDevice[]` | Get speakers |
| `getActiveMicrophone` | `()` | `string` | Get active mic ID |
| `getActiveSpeaker` | `()` | `string` | Get active speaker ID |
| `isAudioMuted` | `(userId?)` | `boolean` | Is audio muted |

### Screen Share Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `startShareScreen` | `(canvas, options?)` | `ExecutedResult` | Start sharing |
| `stopShareScreen` | `()` | `ExecutedResult` | Stop sharing |
| `startShareView` | `(canvas, userId)` | `ExecutedResult` | View share |
| `stopShareView` | `()` | `ExecutedResult` | Stop viewing |
| `attachShareView` | `(userId, element?)` | `Promise<VideoPlayer>` | Attach share view |
| `detachShareView` | `(userId, element?)` | `Promise<VideoPlayer>` | Detach share view |
| `pauseShareScreen` | `()` | `ExecutedResult` | Pause share |
| `resumeShareScreen` | `()` | `ExecutedResult` | Resume share |
| `getActiveShareUserId` | `()` | `number` | Get sharer user ID |
| `getShareStatus` | `()` | `ShareStatus` | Get share status |
| `getShareUserList` | `()` | `Participant[]` | Get sharers |
| `lockShare` | `(isLocked)` | `ExecutedResult` | Lock share (host) |
| `setSharePrivilege` | `(privilege)` | `ExecutedResult` | Set share privilege |
| `isStartShareScreenWithVideoElement` | `()` | `boolean` | Use video or canvas |

### ScreenShareOption Interface

```typescript
interface ScreenShareOption {
  requestReadReceipt?: boolean;  // Request read receipt
  secondaryAudio?: boolean;      // Share with audio
  optimizedForVideo?: boolean;   // Optimize for video
}
```

### ShareStatus Enum

```typescript
enum ShareStatus {
  Sharing = 'Sharing',
  Paused = 'Paused',
  End = 'End'
}
```

### Processor Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `createProcessor` | `(params)` | `Promise<Processor>` | Create processor |
| `addProcessor` | `(processor)` | `Promise<"">` | Add processor |
| `removeProcessor` | `(processor)` | `Promise<"">` | Remove processor |
| `isSupportVideoProcessor` | `()` | `boolean` | Video processor support |
| `isSupportAudioProcessor` | `()` | `boolean` | Audio processor support |
| `isSupportShareProcessor` | `()` | `boolean` | Share processor support |

---

## Level 2: Feature Clients

### ChatClient

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `send` | `(message)` | `ExecutedResult` | Send to all |
| `sendToUser` | `(userId, message)` | `ExecutedResult` | Send to user |
| `sendFile` | `(file, receiverId)` | `ExecutedResult` | Send file |
| `downloadFile` | `(fileUrl, options)` | `ExecutedResult` | Download file |

### CommandChannel

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `send` | `(text)` | `ExecutedResult` | Send to all |
| `sendToUser` | `(userId, text)` | `ExecutedResult` | Send to user |

### RecordingClient

| Method | Returns | Description |
|--------|---------|-------------|
| `startCloudRecording()` | `ExecutedResult` | Start recording (host) |
| `stopCloudRecording()` | `ExecutedResult` | Stop recording |
| `pauseCloudRecording()` | `ExecutedResult` | Pause recording |
| `resumeCloudRecording()` | `ExecutedResult` | Resume recording |

### LiveTranscriptionClient

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `startLiveTranscription` | `()` | `ExecutedResult` | Start transcription |
| `stopLiveTranscription` | `()` | `ExecutedResult` | Stop transcription |
| `enableReceivingCaption` | `(enable)` | `ExecutedResult` | Enable/disable captions |
| `setSpokenLanguage` | `(language)` | `ExecutedResult` | Set spoken language |

### LiveStreamClient

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `startLiveStream` | `(url, key)` | `ExecutedResult` | Start streaming |
| `stopLiveStream` | `()` | `ExecutedResult` | Stop streaming |

### SubsessionClient

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `createSubsessions` | `(names)` | `ExecutedResult` | Create subsessions |
| `openSubsessions` | `(rooms)` | `ExecutedResult` | Open subsessions |
| `closeAllSubsessions` | `()` | `ExecutedResult` | Close all |
| `broadcast` | `(message)` | `ExecutedResult` | Broadcast message |
| `getSubsessionList` | `()` | `Subsession[]` | Get subsessions |

---

## Events Reference

### Session Events

| Event | Payload | Description |
|-------|---------|-------------|
| `connection-change` | `ConnectionChangePayload` | Connection state changed |
| `user-added` | `ParticipantPropertiesPayload[]` | Participant joined |
| `user-removed` | `ParticipantPropertiesPayload[]` | Participant left |
| `user-updated` | `ParticipantPropertiesPayload[]` | Participant updated |

### Video Events

| Event | Payload | Description |
|-------|---------|-------------|
| `peer-video-state-change` | `{action: 'Start'\|'Stop', userId}` | Peer video on/off |
| `video-active-change` | `{state: VideoActiveState, userId}` | Video stream changed |
| `video-capturing-change` | `{state: VideoCapturingState}` | Capture state changed |
| `video-dimension-change` | `{width, height, type}` | Video dimensions changed |

### Audio Events

| Event | Payload | Description |
|-------|---------|-------------|
| `current-audio-change` | `{action, source?, type?}` | Audio state changed |
| `active-speaker` | `ActiveSpeaker[]` | Active speakers |
| `host-ask-unmute-audio` | `{reason}` | Host asks unmute |
| `auto-play-audio-failed` | (none) | Auto-play blocked |

### Screen Share Events

| Event | Payload | Description |
|-------|---------|-------------|
| `active-share-change` | `{state: 'Active'\|'Inactive', userId}` | Share active state |
| `peer-share-state-change` | `{action: 'Start'\|'Stop', userId}` | Peer share changed |
| `passively-stop-share` | `PassiveStopShareReason` | Share stopped passively |
| `share-content-dimension-change` | `{width, height, type}` | Share size changed |

### Chat Events

| Event | Payload | Description |
|-------|---------|-------------|
| `chat-on-message` | `ChatMessage` | Message received |
| `chat-privilege-change` | `{chatPrivilege}` | Privilege changed |

### Command Channel Events

| Event | Payload | Description |
|-------|---------|-------------|
| `command-channel-message` | `{senderId, senderName, text, timestamp}` | Command received |
| `command-channel-status` | `ConnectionState` | Channel status |

### Recording Events

| Event | Payload | Description |
|-------|---------|-------------|
| `recording-change` | `{state: RecordingStatus}` | Recording state changed |
| `individual-recording-change` | `{state, userId?}` | Individual recording |

### Transcription Events

| Event | Payload | Description |
|-------|---------|-------------|
| `caption-message` | `LiveTranscriptionMessage` | Caption received |
| `caption-status` | `{autoCaption, lang?, ...}` | Caption status |
| `caption-enable` | `boolean` | Caption enabled/disabled |

### Media Events

| Event | Payload | Description |
|-------|---------|-------------|
| `device-change` | (none) | Device added/removed |
| `device-permission-change` | `{name, state}` | Permission changed |
| `network-quality-change` | `{level, type, userId}` | Network quality |

---

## Error Types

```typescript
type ErrorTypes = 
  | 'INVALID_OPERATION'      // Duplicated operation
  | 'INTERNAL_ERROR'         // Service unavailable
  | 'OPERATION_TIMEOUT'      // Timed out
  | 'INSUFFICIENT_PRIVILEGES' // Need host/manager
  | 'IMPROPER_MEETING_STATE' // Not in meeting
  | 'INVALID_PARAMETERS'     // Wrong params
  | 'OPERATION_LOCKED';      // Property locked
```

---

## Related Documentation

- [Singleton Hierarchy](../concepts/singleton-hierarchy.md) - Navigation guide
- [SDK Architecture Pattern](../concepts/sdk-architecture-pattern.md) - Universal pattern
- [SKILL.md](../SKILL.md) - Main skill overview

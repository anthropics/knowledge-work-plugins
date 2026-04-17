# Singleton Hierarchy: Navigation Guide

## Overview

The Zoom Video SDK for Web uses a **service locator pattern** - a tree of objects where you navigate from the root `ZoomVideo` module to specific features. You don't construct objects; you traverse to them.

```
You want to...              You navigate to...
─────────────────────────────────────────────────────
Start your camera           client.getMediaStream() → stream.startVideo()
Mute audio                  client.getMediaStream() → stream.muteAudio()
Attach video                client.getMediaStream() → stream.attachVideo(userId, quality)
Send chat message           client.getChatClient() → chatClient.send(message)
Start screen share          client.getMediaStream() → stream.startShareScreen(canvas)
Start recording             client.getRecordingClient() → recordingClient.startCloudRecording()
```

---

## Complete Hierarchy (4 Levels Deep)

```
Level 0: Global Module
│
└─► ZoomVideo ──────────────────────────────────────────────────► Default Export
    │
    ├─► Static Methods (Before Session)
    │   ├── createClient()               → VideoClient (singleton)
    │   ├── destroyClient()              → Promise<void>
    │   ├── checkSystemRequirements()    → MediaCompatibility
    │   ├── checkFeatureRequirements()   → SupportFeatures
    │   ├── getDevices(skip?)            → Promise<MediaDeviceInfo[]>
    │   ├── preloadDependentAssets(path) → void
    │   ├── createLocalVideoTrack(id?)   → LocalVideoTrack
    │   ├── createLocalAudioTrack(id?)   → LocalAudioTrack
    │   └── VERSION                      → string
    │
    └─► Level 1: VideoClient (The Root Singleton)
        │
        ├─► Session Lifecycle
        │   ├── init(language, assets, options)   → ExecutedResult
        │   ├── join(topic, token, name, pass)    → ExecutedResult
        │   ├── leave(end?)                       → ExecutedResult
        │   ├── on(event, callback)               → void
        │   └── off(event, callback)              → void
        │
        ├─► Participant Info
        │   ├── getAllUser()              → Participant[]
        │   ├── getCurrentUserInfo()      → Participant
        │   ├── getUser(userId)           → Participant | undefined
        │   ├── getSessionHost()          → Participant | undefined
        │   ├── getSessionInfo()          → SessionInfo
        │   ├── isHost()                  → boolean
        │   ├── isManager()               → boolean
        │   └── isOriginalHost()          → boolean
        │
        ├─► Host Controls
        │   ├── makeHost(userId)          → ExecutedResult
        │   ├── makeManager(userId)       → ExecutedResult
        │   ├── revokeManager(userId)     → ExecutedResult
        │   ├── removeUser(userId)        → ExecutedResult
        │   ├── changeName(name, userId?) → ExecutedResult
        │   └── reclaimHost()             → ExecutedResult
        │
        ├─► Level 2: Media Stream (MAIN INTERFACE)
        │   │
        │   └── getMediaStream()          → Stream
        │       │
        │       ├─► Video Functions
        │       │   ├── startVideo(options?)            → ExecutedResult
        │       │   ├── stopVideo()                     → ExecutedResult
        │       │   ├── attachVideo(userId, quality)    → VideoPlayer
        │       │   ├── detachVideo(userId, element?)   → VideoPlayer | VideoPlayer[]
        │       │   ├── renderVideo(canvas, userId, ...) → ExecutedResult [DEPRECATED]
        │       │   ├── stopRenderVideo(canvas, userId) → ExecutedResult [DEPRECATED]
        │       │   ├── switchCamera(cameraId)          → ExecutedResult
        │       │   ├── getCameraList()                 → MediaDevice[]
        │       │   ├── getActiveCamera()               → string
        │       │   ├── isSupportHDVideo()              → boolean
        │       │   ├── getVideoMaxQuality()            → VideoQuality
        │       │   ├── getMaxRenderableVideos()        → number
        │       │   ├── isSupportMultipleVideos()       → boolean
        │       │   ├── isSupportVirtualBackground()    → boolean
        │       │   ├── updateVirtualBackgroundImage(img) → ExecutedResult
        │       │   ├── mirrorVideo(enable)             → ExecutedResult
        │       │   ├── spotlightVideo(userId)          → ExecutedResult
        │       │   └── screenshotVideo(userId?)        → Promise<Blob>
        │       │
        │       ├─► Audio Functions
        │       │   ├── startAudio(options?)            → ExecutedResult
        │       │   ├── stopAudio()                     → ExecutedResult
        │       │   ├── muteAudio(userId?)              → ExecutedResult
        │       │   ├── unmuteAudio(userId?)            → ExecutedResult
        │       │   ├── muteAllAudio()                  → ExecutedResult
        │       │   ├── unmuteAllAudio()                → ExecutedResult
        │       │   ├── switchMicrophone(micId)         → ExecutedResult
        │       │   ├── switchSpeaker(speakerId)        → ExecutedResult
        │       │   ├── getMicList()                    → MediaDevice[]
        │       │   ├── getSpeakerList()                → MediaDevice[]
        │       │   ├── getActiveMicrophone()           → string
        │       │   ├── getActiveSpeaker()              → string
        │       │   ├── isAudioMuted(userId?)           → boolean
        │       │   └── enableBackgroundNoiseSuppression(enable) → ExecutedResult
        │       │
        │       ├─► Screen Share Functions
        │       │   ├── startShareScreen(canvas, options?) → ExecutedResult
        │       │   ├── stopShareScreen()               → ExecutedResult
        │       │   ├── startShareView(canvas, userId)  → ExecutedResult
        │       │   ├── stopShareView()                 → ExecutedResult
        │       │   ├── attachShareView(userId, el?)    → VideoPlayer
        │       │   ├── detachShareView(userId, el?)    → VideoPlayer
        │       │   ├── pauseShareScreen()              → ExecutedResult
        │       │   ├── resumeShareScreen()             → ExecutedResult
        │       │   ├── isStartShareScreenWithVideoElement() → boolean
        │       │   ├── getActiveShareUserId()          → number
        │       │   ├── getShareStatus()                → ShareStatus
        │       │   ├── getShareUserList()              → Participant[]
        │       │   ├── lockShare(isLocked)             → ExecutedResult
        │       │   └── setSharePrivilege(privilege)    → ExecutedResult
        │       │
        │       ├─► Annotation Functions
        │       │   ├── startAnnotation(...)            → ExecutedResult
        │       │   ├── stopAnnotation()                → ExecutedResult
        │       │   ├── getAnnotationController()       → AnnotationController
        │       │   └── canDoAnnotation()               → boolean
        │       │
        │       ├─► Processor Functions (Custom Effects)
        │       │   ├── createProcessor(params)         → Processor
        │       │   ├── addProcessor(processor)         → Promise<"">
        │       │   ├── removeProcessor(processor)      → Promise<"">
        │       │   ├── isSupportVideoProcessor()       → boolean
        │       │   ├── isSupportAudioProcessor()       → boolean
        │       │   └── isSupportShareProcessor()       → boolean
        │       │
        │       ├─► Camera Control (PTZ)
        │       │   ├── controlCamera(option)           → ExecutedResult
        │       │   ├── requestFarEndCameraControl(userId) → ExecutedResult
        │       │   ├── approveFarEndCameraControl(userId) → ExecutedResult
        │       │   └── declineFarEndCameraControl(userId) → ExecutedResult
        │       │
        │       └─► Phone Functions
        │           ├── inviteByPhone(country, phone, name) → ExecutedResult
        │           ├── cancelInviteByPhone(...)        → ExecutedResult
        │           ├── hangup()                        → ExecutedResult
        │           └── isSupportPhoneFeature()         → boolean
        │
        ├─► Level 2: Feature Clients
        │   │
        │   ├── getChatClient()           → ChatClient
        │   │   ├── send(message)                 → ExecutedResult
        │   │   ├── sendToUser(userId, message)   → ExecutedResult
        │   │   ├── sendFile(file, receiverId)    → ExecutedResult
        │   │   └── downloadFile(fileUrl, ...)    → ExecutedResult
        │   │
        │   ├── getCommandClient()        → CommandChannel
        │   │   ├── send(text)                    → ExecutedResult
        │   │   └── sendToUser(userId, text)      → ExecutedResult
        │   │
        │   ├── getRecordingClient()      → RecordingClient
        │   │   ├── startCloudRecording()         → ExecutedResult
        │   │   ├── stopCloudRecording()          → ExecutedResult
        │   │   ├── pauseCloudRecording()         → ExecutedResult
        │   │   └── resumeCloudRecording()        → ExecutedResult
        │   │
        │   ├── getLiveTranscriptionClient() → LiveTranscriptionClient
        │   │   ├── startLiveTranscription()      → ExecutedResult
        │   │   ├── stopLiveTranscription()       → ExecutedResult
        │   │   ├── enableReceivingCaption(enable) → ExecutedResult
        │   │   └── setSpokenLanguage(language)   → ExecutedResult
        │   │
        │   ├── getLiveStreamClient()     → LiveStreamClient
        │   │   ├── startLiveStream(url, key)     → ExecutedResult
        │   │   └── stopLiveStream()              → ExecutedResult
        │   │
        │   ├── getSubsessionClient()     → SubsessionClient
        │   │   ├── createSubsessions(names)      → ExecutedResult
        │   │   ├── openSubsessions(rooms)        → ExecutedResult
        │   │   ├── closeAllSubsessions()         → ExecutedResult
        │   │   ├── broadcast(message)            → ExecutedResult
        │   │   └── getSubsessionList()           → Subsession[]
        │   │
        │   ├── getWhiteboardClient()     → WhiteboardClient
        │   │   ├── startWhiteboard(options?)     → ExecutedResult
        │   │   └── stopWhiteboard()              → ExecutedResult
        │   │
        │   ├── getBroadcastStreamingClient() → BroadcastStreamingClient
        │   │   ├── startBroadcast()              → ExecutedResult
        │   │   └── stopBroadcast()               → ExecutedResult
        │   │
        │   ├── getRealTimeMediaStreamsClient() → RealTimeMediaStreamsClient
        │   │   ├── startRealTimeMediaStream()    → ExecutedResult
        │   │   └── stopRealTimeMediaStream()     → ExecutedResult
        │   │
        │   └── getLoggerClient(options?) → LoggerClient
        │       ├── log(...)                      → void
        │       └── setLogLevel(level)            → void
        │
        └─► Level 3: Participant Object
            │
            └── Participant Interface
                ├── userId                    → number
                ├── displayName               → string
                ├── bVideoOn                  → boolean
                ├── muted                     → boolean
                ├── audio                     → '' | 'computer' | 'phone'
                ├── sharerOn                  → boolean
                ├── bShareAudioOn             → boolean
                └── isHost                    → boolean
```

---

## Key Difference from Windows SDK

| Aspect | Windows SDK | Web SDK |
|--------|-------------|---------|
| **Root Object** | `IZoomVideoSDK` | `ZoomVideo.createClient()` → `VideoClient` |
| **Feature Access** | Helpers (`getVideoHelper()`) | Stream + Clients (`getMediaStream()`, `getChatClient()`) |
| **Video Rendering** | Canvas API / Raw Data Pipe | `attachVideo()` returns VideoPlayer |
| **Events** | Delegate callbacks | `client.on('event', handler)` |
| **Depth** | 5 levels max | 4 levels max |

---

## When to Use Each Level

| Level | When | Example |
|-------|------|---------|
| **Level 0** | Before SDK init, check compatibility | `ZoomVideo.checkSystemRequirements()` |
| **Level 1** | Session lifecycle, get clients | `client.join(...)`, `client.getChatClient()` |
| **Level 2** | Media operations (Stream) | `stream.startVideo()`, `stream.attachVideo()` |
| **Level 2** | Feature-specific operations (Clients) | `chatClient.send(...)`, `recordingClient.start...()` |
| **Level 3** | Participant info | `user.bVideoOn`, `user.displayName` |

---

## Navigation by Feature

| Feature | Navigation Path |
|---------|-----------------|
| **Start camera** | `client.getMediaStream().startVideo()` |
| **Stop camera** | `client.getMediaStream().stopVideo()` |
| **Attach video** | `client.getMediaStream().attachVideo(userId, quality)` |
| **Detach video** | `client.getMediaStream().detachVideo(userId)` |
| **Switch camera** | `client.getMediaStream().switchCamera(deviceId)` |
| **Start audio** | `client.getMediaStream().startAudio()` |
| **Mute audio** | `client.getMediaStream().muteAudio()` |
| **Unmute audio** | `client.getMediaStream().unmuteAudio()` |
| **Start share** | `client.getMediaStream().startShareScreen(canvas)` |
| **Stop share** | `client.getMediaStream().stopShareScreen()` |
| **View share** | `client.getMediaStream().startShareView(canvas, userId)` |
| **Send chat** | `client.getChatClient().send(message)` |
| **Start recording** | `client.getRecordingClient().startCloudRecording()` |
| **Start transcription** | `client.getLiveTranscriptionClient().startLiveTranscription()` |
| **Send command** | `client.getCommandClient().send(text)` |
| **Get participants** | `client.getAllUser()` |
| **Get myself** | `client.getCurrentUserInfo()` |
| **Leave session** | `client.leave()` |
| **End session** | `client.leave(true)` |

---

## Event Subscription Pattern

All events are subscribed via `client.on()`:

```javascript
// Session events
client.on('connection-change', (payload) => { ... });
client.on('user-added', (payload) => { ... });
client.on('user-removed', (payload) => { ... });
client.on('user-updated', (payload) => { ... });

// Video events
client.on('peer-video-state-change', (payload) => { ... });
client.on('video-active-change', (payload) => { ... });
client.on('video-capturing-change', (payload) => { ... });

// Audio events
client.on('current-audio-change', (payload) => { ... });
client.on('active-speaker', (payload) => { ... });
client.on('host-ask-unmute-audio', (payload) => { ... });

// Share events
client.on('active-share-change', (payload) => { ... });
client.on('peer-share-state-change', (payload) => { ... });
client.on('passively-stop-share', (payload) => { ... });

// Chat events
client.on('chat-on-message', (payload) => { ... });

// Recording events
client.on('recording-change', (payload) => { ... });

// Transcription events
client.on('caption-message', (payload) => { ... });
```

---

## Critical Timing Rules

### 1. Stream is ONLY Available After Join

```javascript
// WRONG - stream is undefined
const stream = client.getMediaStream();
await client.join(...);

// CORRECT - get stream after join
await client.join(...);
const stream = client.getMediaStream();
```

### 2. Event-Driven Video Rendering

```javascript
// Listen for video changes
client.on('peer-video-state-change', async (payload) => {
  const { action, userId } = payload;
  
  if (action === 'Start') {
    const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
    container.appendChild(element);
  } else {
    await stream.detachVideo(userId);
  }
});
```

### 3. Check Feature Support Before Using

```javascript
// HD Video
if (stream.isSupportHDVideo()) {
  await stream.startVideo({ hd: true });
}

// Virtual Background
if (stream.isSupportVirtualBackground()) {
  await stream.updateVirtualBackgroundImage('blur');
}

// Video Processor
if (stream.isSupportVideoProcessor()) {
  const processor = await stream.createProcessor(params);
  await stream.addProcessor(processor);
}
```

---

## Practical Rules

### 1. Get Stream After Join

```javascript
// WRONG
const stream = client.getMediaStream();  // undefined!
await client.join(...);

// CORRECT
await client.join(...);
const stream = client.getMediaStream();  // Works!
```

### 2. Check Element Type for Screen Share

```javascript
// Check which element to use
if (stream.isStartShareScreenWithVideoElement()) {
  // Use HTMLVideoElement
  await stream.startShareScreen(videoElement);
} else {
  // Use HTMLCanvasElement
  await stream.startShareScreen(canvasElement);
}
```

### 3. Render Existing Participants on Mid-Session Join

```javascript
// After joining, render existing participants
const users = client.getAllUser();
const currentUserId = client.getCurrentUserInfo().userId;

for (const user of users) {
  if (user.bVideoOn && user.userId !== currentUserId) {
    const element = await stream.attachVideo(user.userId, VideoQuality.Video_360P);
    container.appendChild(element);
  }
}
```

---

## Related Documentation

- [SDK Architecture Pattern](sdk-architecture-pattern.md) - Universal 5-step pattern
- [API Reference](../references/web-reference.md) - Complete method signatures
- [SKILL.md](../SKILL.md) - Main skill overview

---

**TL;DR**: Start at `ZoomVideo.createClient()`, get stream AFTER join, use `stream.` for media and `client.getXXXClient()` for features. Events via `client.on()`.

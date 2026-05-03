# Event Handling

Complete guide to handling events in the Zoom Video SDK for Web.

## Event Registration Pattern

```javascript
// Register event listener
client.on('event-name', (payload) => {
  // Handle event
});

// Remove event listener
client.off('event-name', handlerFunction);
```

## Critical Events (Must Handle)

These events are essential for any Video SDK application.

### Connection Events

```javascript
// Connection state changes - REQUIRED
client.on('connection-change', (payload) => {
  const { state, reason } = payload;
  
  switch (state) {
    case 'Connected':
      console.log('Successfully connected to session');
      break;
    case 'Reconnecting':
      console.log('Connection lost, attempting to reconnect...', reason);
      showReconnectingUI();
      break;
    case 'Closed':
      console.log('Disconnected from session', reason);
      handleDisconnect(reason);
      break;
    case 'Fail':
      console.error('Connection failed', reason);
      break;
  }
});

function handleDisconnect(reason) {
  // Reasons: 'ended by host', 'kicked by host', 'session ended', etc.
  cleanup();
  showDisconnectMessage(reason);
}
```

### Participant Events

```javascript
// New participant joined
client.on('user-added', (payload) => {
  // payload is array of participants
  payload.forEach(user => {
    console.log('Joined:', user.displayName, 'ID:', user.userId);
    createParticipantUI(user);
  });
});

// Participant left
client.on('user-removed', (payload) => {
  payload.forEach(user => {
    console.log('Left:', user.displayName);
    removeParticipantUI(user.userId);
    // Clean up their video
    stream.detachVideo(user.userId).catch(() => {});
  });
});

// Participant updated (name, mute status, video status, etc.)
client.on('user-updated', (payload) => {
  payload.forEach(user => {
    console.log('Updated:', user);
    updateParticipantUI(user);
  });
});
```

### Video Events

```javascript
// Remote participant video state changed - CRITICAL
client.on('peer-video-state-change', async (payload) => {
  const { action, userId } = payload;
  
  if (action === 'Start') {
    // User started video - render it
    const element = await stream.attachVideo(userId, VideoQuality.Video_360P);
    document.getElementById(`video-${userId}`)?.appendChild(element);
  } else if (action === 'Stop') {
    // User stopped video - clean up
    await stream.detachVideo(userId);
    const container = document.getElementById(`video-${userId}`);
    if (container) container.innerHTML = '';
  }
});

// Local video capture state
client.on('video-capturing-change', (payload) => {
  const { state } = payload;
  // state: 'Started' | 'Stopped' | 'Failed'
  console.log('Video capture:', state);
});

// Video dimension changed
client.on('video-dimension-change', (payload) => {
  const { width, height, type } = payload;
  console.log('Video dimension:', width, 'x', height, type);
});
```

### Audio Events

```javascript
// Current user audio state changed
client.on('current-audio-change', (payload) => {
  const { action, type, source } = payload;
  
  switch (action) {
    case 'join':
      console.log('Joined audio via:', type); // 'computer' or 'phone'
      break;
    case 'leave':
      console.log('Left audio');
      break;
    case 'muted':
      console.log('Audio muted', source); // 'active', 'passive(mute all)', etc.
      updateMuteUI(true);
      break;
    case 'unmuted':
      console.log('Audio unmuted');
      updateMuteUI(false);
      break;
  }
});

// Host asks you to unmute
client.on('host-ask-unmute-audio', (payload) => {
  console.log('Host requested unmute:', payload.reason);
  showUnmutePrompt();
});

// Active speaker detection
client.on('active-speaker', (payload) => {
  // Array sorted by volume (loudest first)
  if (payload.length > 0) {
    const activeSpeaker = payload[0];
    highlightActiveSpeaker(activeSpeaker.userId);
  }
});

// Auto-play blocked by browser
client.on('auto-play-audio-failed', () => {
  // Show button for user to click to enable audio
  showAudioEnableButton();
});
```

### Screen Share Events

```javascript
// Someone started/stopped sharing
client.on('active-share-change', async (payload) => {
  const { state, userId } = payload;
  
  if (state === 'Active') {
    console.log('User', userId, 'started sharing');
    const element = await stream.attachShareView(userId);
    document.getElementById('share-container').appendChild(element);
    showShareView();
  } else {
    console.log('Sharing stopped');
    await stream.detachShareView(userId);
    hideShareView();
  }
});

// You were forced to stop sharing
client.on('passively-stop-share', (payload) => {
  console.log('Forced to stop sharing:', payload);
  // Reasons: 'PrivilegeChange', 'AnotherShareStarted', etc.
});

// Share privilege changed
client.on('share-privilege-change', (payload) => {
  console.log('Share privilege:', payload.privilege);
});
```

## Chat Events

```javascript
// Received a chat message
client.on('chat-on-message', (payload) => {
  const { sender, receiver, message, timestamp, id } = payload;
  
  console.log(`[${sender.name}]: ${message}`);
  addChatMessage(payload);
});

// Chat privilege changed by host
client.on('chat-privilege-change', (payload) => {
  const { chatPrivilege } = payload;
  // ChatPrivilege.All, ChatPrivilege.NoOne, ChatPrivilege.EveryonePublicly
  updateChatUI(chatPrivilege);
});
```

## Recording Events

```javascript
// Cloud recording state changed
client.on('recording-change', (payload) => {
  const { state } = payload;
  // state: 'Recording', 'Paused', 'Stopped', etc.
  
  if (state === 'Recording') {
    showRecordingIndicator();
  } else {
    hideRecordingIndicator();
  }
});

// Individual recording consent
client.on('individual-recording-change', (payload) => {
  const { state, userId } = payload;
  
  if (state === 'Ask') {
    // Host is asking for recording consent
    showRecordingConsentDialog();
  }
});
```

## Live Transcription Events

```javascript
// Transcription status changed
client.on('caption-status', (payload) => {
  const { autoCaption, language } = payload;
  console.log('Caption enabled:', autoCaption, 'Language:', language);
});

// Received transcription text
client.on('caption-message', (payload) => {
  const { text, displayName, done, userId } = payload;
  
  // done=false means partial/interim result
  // done=true means final result
  updateTranscription(payload);
});

// Captions enabled/disabled
client.on('caption-enable', (isEnabled) => {
  console.log('Captions:', isEnabled ? 'enabled' : 'disabled');
});
```

## Device Events

```javascript
// Device plugged in or removed
client.on('device-change', () => {
  console.log('Device list changed');
  // Refresh device lists
  updateCameraList(stream.getCameraList());
  updateMicList(stream.getMicList());
  updateSpeakerList(stream.getSpeakerList());
});

// Device permission changed
client.on('device-permission-change', (payload) => {
  const { name, state } = payload;
  // name: 'microphone' | 'camera'
  // state: 'granted' | 'denied' | 'prompt'
  console.log(`${name} permission: ${state}`);
});
```

## Network Quality Events

```javascript
// Network quality changed
client.on('network-quality-change', (payload) => {
  const { userId, type, level } = payload;
  // type: 'uplink' | 'downlink'
  // level: 0-5 (0=unknown, 1=bad, 5=excellent)
  
  if (level <= 2) {
    showNetworkWarning(userId, type);
  }
});
```

## Statistics Events

```javascript
// Video statistics
client.on('video-statistic-data-change', (payload) => {
  const { data, type } = payload;
  // data.encoding: true=send, false=receive
  console.log('Video stats:', {
    fps: data.fps,
    resolution: `${data.width}x${data.height}`,
    bitrate: data.bitrate,
    packetLoss: data.avg_loss,
  });
});

// Audio statistics
client.on('audio-statistic-data-change', (payload) => {
  const { data, type } = payload;
  console.log('Audio stats:', {
    bitrate: data.bitrate,
    packetLoss: data.avg_loss,
    jitter: data.jitter,
  });
});
```

## Complete Event Handler Setup

```javascript
class ZoomEventHandler {
  constructor(client, stream) {
    this.client = client;
    this.stream = stream;
    this.handlers = new Map();
  }

  init() {
    this.setupConnectionEvents();
    this.setupParticipantEvents();
    this.setupVideoEvents();
    this.setupAudioEvents();
    this.setupShareEvents();
    this.setupChatEvents();
    this.setupRecordingEvents();
    this.setupDeviceEvents();
  }

  setupConnectionEvents() {
    this.on('connection-change', this.handleConnectionChange.bind(this));
  }

  setupParticipantEvents() {
    this.on('user-added', this.handleUserAdded.bind(this));
    this.on('user-removed', this.handleUserRemoved.bind(this));
    this.on('user-updated', this.handleUserUpdated.bind(this));
  }

  setupVideoEvents() {
    this.on('peer-video-state-change', this.handlePeerVideoChange.bind(this));
    this.on('video-capturing-change', this.handleCapturingChange.bind(this));
  }

  setupAudioEvents() {
    this.on('current-audio-change', this.handleAudioChange.bind(this));
    this.on('host-ask-unmute-audio', this.handleUnmuteRequest.bind(this));
    this.on('active-speaker', this.handleActiveSpeaker.bind(this));
    this.on('auto-play-audio-failed', this.handleAutoPlayFailed.bind(this));
  }

  setupShareEvents() {
    this.on('active-share-change', this.handleShareChange.bind(this));
    this.on('passively-stop-share', this.handlePassiveStopShare.bind(this));
  }

  setupChatEvents() {
    this.on('chat-on-message', this.handleChatMessage.bind(this));
    this.on('chat-privilege-change', this.handleChatPrivilegeChange.bind(this));
  }

  setupRecordingEvents() {
    this.on('recording-change', this.handleRecordingChange.bind(this));
  }

  setupDeviceEvents() {
    this.on('device-change', this.handleDeviceChange.bind(this));
  }

  // Helper to track handlers for cleanup
  on(event, handler) {
    this.client.on(event, handler);
    this.handlers.set(event, handler);
  }

  // Clean up all handlers
  destroy() {
    this.handlers.forEach((handler, event) => {
      this.client.off(event, handler);
    });
    this.handlers.clear();
  }

  // Event handlers
  handleConnectionChange(payload) {
    console.log('Connection:', payload.state, payload.reason);
  }

  handleUserAdded(payload) {
    payload.forEach(user => console.log('User joined:', user.displayName));
  }

  handleUserRemoved(payload) {
    payload.forEach(user => {
      console.log('User left:', user.displayName);
      this.stream.detachVideo(user.userId).catch(() => {});
    });
  }

  handleUserUpdated(payload) {
    payload.forEach(user => console.log('User updated:', user));
  }

  async handlePeerVideoChange(payload) {
    const { action, userId } = payload;
    if (action === 'Start') {
      const element = await this.stream.attachVideo(userId, VideoQuality.Video_360P);
      document.getElementById(`video-${userId}`)?.appendChild(element);
    } else {
      await this.stream.detachVideo(userId);
    }
  }

  handleCapturingChange(payload) {
    console.log('Video capture:', payload.state);
  }

  handleAudioChange(payload) {
    console.log('Audio:', payload.action, payload.type);
  }

  handleUnmuteRequest(payload) {
    console.log('Host requested unmute');
  }

  handleActiveSpeaker(payload) {
    if (payload.length > 0) {
      console.log('Active speaker:', payload[0].userId);
    }
  }

  handleAutoPlayFailed() {
    console.log('Auto-play blocked - show enable audio button');
  }

  async handleShareChange(payload) {
    const { state, userId } = payload;
    if (state === 'Active') {
      const element = await this.stream.attachShareView(userId);
      document.getElementById('share-container')?.appendChild(element);
    } else {
      await this.stream.detachShareView(userId);
    }
  }

  handlePassiveStopShare(payload) {
    console.log('Forced to stop sharing:', payload);
  }

  handleChatMessage(payload) {
    console.log(`Chat from ${payload.sender.name}: ${payload.message}`);
  }

  handleChatPrivilegeChange(payload) {
    console.log('Chat privilege:', payload.chatPrivilege);
  }

  handleRecordingChange(payload) {
    console.log('Recording:', payload.state);
  }

  handleDeviceChange() {
    console.log('Device list changed');
  }
}

// Usage
const eventHandler = new ZoomEventHandler(client, stream);
eventHandler.init();

// Cleanup on leave
client.on('connection-change', (payload) => {
  if (payload.state === 'Closed') {
    eventHandler.destroy();
  }
});
```

## Event Reference Table

| Event | Category | When Triggered |
|-------|----------|----------------|
| `connection-change` | Session | Connection state changes |
| `user-added` | Participant | New participant joins |
| `user-removed` | Participant | Participant leaves |
| `user-updated` | Participant | Participant properties change |
| `peer-video-state-change` | Video | Remote video starts/stops |
| `video-capturing-change` | Video | Local capture state changes |
| `video-dimension-change` | Video | Video resolution changes |
| `current-audio-change` | Audio | Local audio state changes |
| `host-ask-unmute-audio` | Audio | Host requests unmute |
| `active-speaker` | Audio | Active speaker changes |
| `auto-play-audio-failed` | Audio | Browser blocked autoplay |
| `active-share-change` | Share | Someone starts/stops sharing |
| `passively-stop-share` | Share | Forced to stop sharing |
| `share-privilege-change` | Share | Share settings changed |
| `chat-on-message` | Chat | Message received |
| `recording-change` | Recording | Recording state changes |
| `caption-message` | Transcription | Transcription text received |
| `device-change` | Device | Device added/removed |
| `network-quality-change` | Network | Network quality changes |

## Key Points

1. **Always handle `connection-change`** - Essential for detecting disconnects
2. **`peer-video-state-change` is for remote video** - Not your own video
3. **Clean up on `user-removed`** - Detach their video
4. **Handle `auto-play-audio-failed`** - Browser may block audio autoplay
5. **Use `off()` to clean up** - Prevent memory leaks

## Related Documentation

- [Session Join](session-join-pattern.md) - Initial setup
- [Video Rendering](video-rendering.md) - Video handling
- [API Reference](../references/web-reference.md) - Full API

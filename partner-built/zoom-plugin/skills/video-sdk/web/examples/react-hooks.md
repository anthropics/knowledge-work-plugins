# React Hooks (@zoom/videosdk-react)

Official React SDK that provides custom hooks and components for integrating Zoom Video SDK into React apps.

## Installation

```bash
npm install @zoom/videosdk
npm install https://github.com/zoom/videosdk-react/releases/download/v0.0.1/zoom-videosdk-react-0.0.1.tgz
```

**Prerequisites:**
- React 18+
- Zoom Video SDK account and credentials

## Quick Start

```tsx
import { 
  useSession, 
  useSessionUsers, 
  VideoPlayerComponent, 
  VideoPlayerContainerComponent 
} from '@zoom/videosdk-react';

function VideoChat() {
  const { isInSession, isLoading, isError } = useSession(
    "session123", 
    "your_jwt_token", 
    "User Name"
  );
  
  const participants = useSessionUsers();
  
  if (isLoading) return <div>Joining session...</div>;
  if (isError) return <div>Error joining session</div>;
  
  return (
    <div>
      {isInSession && (
        <VideoPlayerContainerComponent>
          {participants.map(participant => (
            <VideoPlayerComponent 
              key={participant.userId} 
              user={participant} 
            />
          ))}
        </VideoPlayerContainerComponent>
      )}
    </div>
  );
}
```

## Available Hooks

### useSession

Manages the complete lifecycle of a Zoom video session.

```tsx
const { isInSession, isLoading, isError, error } = useSession(
  topic,           // Session topic/ID
  token,           // JWT authentication token
  userName,        // Display name
  sessionPassword, // Optional session password
  sessionIdleTimeoutMins, // Optional idle timeout
  {
    disableVideo: false,
    disableAudio: false,
    language: "en-US",
    dependentAssets: "Global",
    waitBeforeJoining: 0,     // Delay before auto-joining
    endSessionOnLeave: false, // End session when host leaves
  }
);
```

**Return values:**
| Field | Type | Description |
|-------|------|-------------|
| `isInSession` | boolean | Currently in session |
| `isLoading` | boolean | Session join in progress |
| `isError` | boolean | Error occurred |
| `error` | Error | Error object if any |

### useSessionUsers

Provides real-time access to all session participants with reference stability.

```tsx
const participants = useSessionUsers();

// participants is an array of Participant objects
participants.map(p => (
  <div key={p.userId}>
    {p.displayName} - {p.bVideoOn ? 'Video On' : 'Video Off'}
  </div>
));
```

### useMyself

Access the local user in the current session.

```tsx
const myself = useMyself();

return (
  <div>
    {myself.userName} - {myself.bVideoOn ? 'Video On' : 'Video Off'}
  </div>
);
```

### useScreenShareUsers

Get users who are currently sharing their screen.

```tsx
const screenshareusers = useScreenShareUsers();

<ScreenShareContainerComponent>
  {screenshareusers.map(userId => (
    <ScreenSharePlayerComponent key={userId} userId={userId} />
  ))}
</ScreenShareContainerComponent>
```

### useVideoState

Manages video capture state and controls.

```tsx
const { isVideoOn, toggleVideo, setVideo } = useVideoState();

// Toggle video on/off
<button onClick={() => toggleVideo({ fps: 30 })}>
  {isVideoOn ? 'Turn Off Video' : 'Turn On Video'}
</button>

// Set video state explicitly
<button onClick={() => setVideo(true, { fps: 15 })}>
  Enable Video
</button>
```

### useAudioState

Comprehensive audio state management.

```tsx
const { 
  isAudioMuted, 
  isCapturingAudio, 
  toggleMute, 
  toggleCapture,
  setMute,
  setCapture
} = useAudioState();

// Toggle mute
<button onClick={toggleMute}>
  {isAudioMuted ? 'Unmute' : 'Mute'}
</button>

// Toggle audio capture
<button onClick={toggleCapture}>
  {isCapturingAudio ? 'Stop Audio' : 'Start Audio'}
</button>
```

### useScreenshare

Manages screen sharing functionality.

```tsx
const { ScreenshareRef, startScreenshare } = useScreenshare();

return (
  <div>
    <LocalScreenShareComponent ref={ScreenshareRef} />
    <button onClick={() => startScreenshare({ audio: true })}>
      Start Screen Share
    </button>
  </div>
);
```

## Components

### VideoPlayerContainerComponent

**Required container** for video players. Must wrap all `VideoPlayerComponent` instances.

```tsx
<VideoPlayerContainerComponent style={{ width: '100%', height: '400px' }}>
  {participants.map(participant => (
    <VideoPlayerComponent key={participant.userId} user={participant} />
  ))}
</VideoPlayerContainerComponent>
```

### VideoPlayerComponent

Renders individual participant video streams.

```tsx
const participants = useSessionUsers();

<VideoPlayerComponent user={participants[0]} />
```

### ScreenShareContainerComponent

**Required container** for screen share players.

```tsx
<ScreenShareContainerComponent style={{ width: '100%', height: '400px' }}>
  {screenshareusers.map(userId => (
    <ScreenSharePlayerComponent key={userId} userId={userId} />
  ))}
</ScreenShareContainerComponent>
```

### ScreenSharePlayerComponent

Renders screen share streams.

```tsx
<ScreenSharePlayerComponent userId={screenshareusers[0]} />
```

## Complete Example

```tsx
import React from 'react';
import { 
  useSession, 
  useSessionUsers,
  useMyself,
  useVideoState,
  useAudioState,
  useScreenshare,
  useScreenShareUsers,
  VideoPlayerComponent, 
  VideoPlayerContainerComponent,
  ScreenSharePlayerComponent,
  ScreenShareContainerComponent,
  LocalScreenShareComponent
} from '@zoom/videosdk-react';

interface VideoCallProps {
  topic: string;
  token: string;
  userName: string;
}

export const VideoCall: React.FC<VideoCallProps> = ({ topic, token, userName }) => {
  // Session management
  const { isInSession, isLoading, isError, error } = useSession(
    topic, 
    token, 
    userName,
    undefined, // no password
    undefined, // default idle timeout
    {
      disableVideo: false,
      disableAudio: false,
    }
  );

  // Participants
  const participants = useSessionUsers();
  const myself = useMyself();
  const screenshareUsers = useScreenShareUsers();

  // Media controls
  const { isVideoOn, toggleVideo } = useVideoState();
  const { isAudioMuted, isCapturingAudio, toggleMute, toggleCapture } = useAudioState();
  const { ScreenshareRef, startScreenshare } = useScreenshare();

  // Loading state
  if (isLoading) {
    return <div className="loading">Joining session...</div>;
  }

  // Error state
  if (isError) {
    return <div className="error">Error: {error?.message}</div>;
  }

  // Not in session
  if (!isInSession) {
    return <div>Not in session</div>;
  }

  return (
    <div className="video-call">
      {/* Video Grid */}
      <VideoPlayerContainerComponent className="video-grid">
        {participants.map(participant => (
          <div key={participant.userId} className="video-tile">
            <VideoPlayerComponent user={participant} />
            <div className="participant-name">{participant.displayName}</div>
          </div>
        ))}
      </VideoPlayerContainerComponent>

      {/* Screen Share */}
      {screenshareUsers.length > 0 && (
        <ScreenShareContainerComponent className="screenshare-view">
          {screenshareUsers.map(userId => (
            <ScreenSharePlayerComponent key={userId} userId={userId} />
          ))}
        </ScreenShareContainerComponent>
      )}

      {/* Local Screen Share Preview */}
      <LocalScreenShareComponent ref={ScreenshareRef} />

      {/* Controls */}
      <div className="controls">
        {/* Audio */}
        {!isCapturingAudio ? (
          <button onClick={toggleCapture}>Join Audio</button>
        ) : (
          <button onClick={toggleMute}>
            {isAudioMuted ? '🔇 Unmute' : '🔊 Mute'}
          </button>
        )}

        {/* Video */}
        <button onClick={() => toggleVideo()}>
          {isVideoOn ? '📹 Stop Video' : '📷 Start Video'}
        </button>

        {/* Screen Share */}
        <button onClick={() => startScreenshare({ audio: true })}>
          🖥️ Share Screen
        </button>
      </div>

      {/* Participant Info */}
      <div className="info">
        <p>Logged in as: {myself?.userName}</p>
        <p>Participants: {participants.length}</p>
      </div>
    </div>
  );
};
```

## Interoperability with @zoom/videosdk

The React SDK is designed to work alongside the core `@zoom/videosdk`. You can use both:

```tsx
import ZoomVideo from '@zoom/videosdk';
import { useSession, useSessionUsers } from '@zoom/videosdk-react';

// Use React hooks for common patterns
const { isInSession } = useSession(topic, token, userName);
const participants = useSessionUsers();

// Access the underlying client for advanced features
const client = ZoomVideo.createClient();
const chatClient = client.getChatClient();
const recordingClient = client.getRecordingClient();
```

## Project Structure

```
src/
├── components/          # React components
│   ├── VideoPlayerComponent
│   ├── VideoPlayerContainerComponent
│   ├── ScreenSharePlayerComponent
│   ├── ScreenShareContainerComponent
│   └── LocalScreenShareComponent
├── hooks/               # Custom React hooks
│   ├── useSession
│   ├── useSessionUsers
│   ├── useMyself
│   ├── useVideoState
│   ├── useAudioState
│   ├── useScreenshare
│   └── useScreenShareUsers
└── index.ts             # Main exports
```

## Key Benefits

| Benefit | Description |
|---------|-------------|
| **Simplified State** | Automatic participant state management |
| **Reference Stability** | Hooks maintain stable references |
| **TypeScript Support** | Full type definitions included |
| **Flexible** | Use alongside core SDK |
| **Customizable** | Components accept standard React props |

## Official Repository

- **GitHub**: [zoom/videosdk-react](https://github.com/zoom/videosdk-react)

## Related Documentation

- [Session Join Pattern](session-join-pattern.md) - Manual SDK usage
- [Video Rendering](video-rendering.md) - Manual attachVideo() patterns
- [Event Handling](event-handling.md) - Event patterns

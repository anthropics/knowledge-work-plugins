# Cloud Recording

Complete guide to controlling cloud recording in the Zoom Video SDK for Web.

## Prerequisites

- Cloud recording must be enabled on your Zoom account
- User must have recording privileges (typically host/manager)

## Getting the Recording Client

```javascript
// Get recording client after joining session
const recordingClient = client.getRecordingClient();
```

## Basic Operations

### Check Recording Capability

```javascript
// Check if cloud recording is available
const canRecord = recordingClient.canStartRecording();

if (!canRecord) {
  console.log('Cloud recording not enabled for this session');
}
```

### Start Recording

```javascript
try {
  await recordingClient.startCloudRecording();
  console.log('Recording started');
} catch (error) {
  console.error('Failed to start recording:', error);
}
```

### Stop Recording

```javascript
try {
  await recordingClient.stopCloudRecording();
  console.log('Recording stopped');
} catch (error) {
  console.error('Failed to stop recording:', error);
}
```

### Pause/Resume Recording

```javascript
// Pause
await recordingClient.pauseCloudRecording();

// Resume
await recordingClient.resumeCloudRecording();
```

### Get Recording Status

```javascript
import { RecordingStatus } from '@zoom/videosdk';

const status = recordingClient.getCloudRecordingStatus();

switch (status) {
  case RecordingStatus.Recording:
    console.log('Currently recording');
    break;
  case RecordingStatus.Paused:
    console.log('Recording paused');
    break;
  case RecordingStatus.Stopped:
    console.log('Not recording');
    break;
}
```

## Recording Events

### Recording State Changes

```javascript
client.on('recording-change', (payload) => {
  const { state } = payload;
  
  switch (state) {
    case 'Recording':
      showRecordingIndicator();
      break;
    case 'Paused':
      showPausedIndicator();
      break;
    case 'Stopped':
      hideRecordingIndicator();
      break;
  }
});
```

### Individual Recording Consent

When individual recording is enabled, participants must consent:

```javascript
client.on('individual-recording-change', (payload) => {
  const { state, userId } = payload;
  
  switch (state) {
    case 'Ask':
      // Host is asking you to accept individual recording
      showRecordingConsentDialog();
      break;
    case 'Accept':
      // User accepted recording
      console.log('User', userId, 'accepted recording');
      break;
    case 'Decline':
      // User declined recording
      console.log('User', userId, 'declined recording');
      break;
  }
});
```

### Respond to Recording Consent

```javascript
// Accept individual recording
await recordingClient.acceptIndividualRecording();

// Decline individual recording
await recordingClient.declineIndividualRecording();
```

## Complete Recording Manager

```javascript
import { RecordingStatus } from '@zoom/videosdk';

class RecordingManager {
  constructor(client) {
    this.client = client;
    this.recordingClient = null;
    this.currentStatus = RecordingStatus.Stopped;
    this.onStatusChange = null;
    this.onConsentRequired = null;
  }

  init() {
    this.recordingClient = this.client.getRecordingClient();
    this.currentStatus = this.recordingClient.getCloudRecordingStatus();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Recording state changes
    this.client.on('recording-change', (payload) => {
      this.currentStatus = payload.state;
      
      if (this.onStatusChange) {
        this.onStatusChange(payload.state);
      }
    });

    // Individual recording consent
    this.client.on('individual-recording-change', (payload) => {
      if (payload.state === 'Ask' && this.onConsentRequired) {
        this.onConsentRequired();
      }
    });
  }

  canStartRecording() {
    return this.recordingClient.canStartRecording();
  }

  isRecording() {
    return this.currentStatus === 'Recording' || 
           this.currentStatus === RecordingStatus.Recording;
  }

  isPaused() {
    return this.currentStatus === 'Paused' || 
           this.currentStatus === RecordingStatus.Paused;
  }

  async start() {
    if (!this.canStartRecording()) {
      throw new Error('Cloud recording not available');
    }

    if (this.isRecording()) {
      throw new Error('Already recording');
    }

    await this.recordingClient.startCloudRecording();
  }

  async stop() {
    if (!this.isRecording() && !this.isPaused()) {
      throw new Error('Not currently recording');
    }

    await this.recordingClient.stopCloudRecording();
  }

  async pause() {
    if (!this.isRecording()) {
      throw new Error('Not currently recording');
    }

    await this.recordingClient.pauseCloudRecording();
  }

  async resume() {
    if (!this.isPaused()) {
      throw new Error('Recording not paused');
    }

    await this.recordingClient.resumeCloudRecording();
  }

  async acceptConsent() {
    await this.recordingClient.acceptIndividualRecording();
  }

  async declineConsent() {
    await this.recordingClient.declineIndividualRecording();
  }

  getStatus() {
    return this.recordingClient.getCloudRecordingStatus();
  }
}

// Usage
const recordingManager = new RecordingManager(client);
recordingManager.init();

recordingManager.onStatusChange = (status) => {
  updateRecordingUI(status);
};

recordingManager.onConsentRequired = () => {
  showConsentDialog({
    onAccept: () => recordingManager.acceptConsent(),
    onDecline: () => recordingManager.declineConsent(),
  });
};

// UI handlers
document.getElementById('start-recording').onclick = async () => {
  try {
    await recordingManager.start();
  } catch (error) {
    alert(error.message);
  }
};

document.getElementById('stop-recording').onclick = async () => {
  try {
    await recordingManager.stop();
  } catch (error) {
    alert(error.message);
  }
};
```

## React Component

```typescript
import React, { useState, useEffect } from 'react';
import { VideoClient, RecordingStatus } from '@zoom/videosdk';

interface RecordingControlsProps {
  client: typeof VideoClient;
  isHost: boolean;
}

export const RecordingControls: React.FC<RecordingControlsProps> = ({ 
  client, 
  isHost 
}) => {
  const [status, setStatus] = useState<RecordingStatus>(RecordingStatus.Stopped);
  const [canRecord, setCanRecord] = useState(false);
  const [showConsent, setShowConsent] = useState(false);
  
  const recordingClient = client.getRecordingClient();

  useEffect(() => {
    // Initial state
    setStatus(recordingClient.getCloudRecordingStatus());
    setCanRecord(recordingClient.canStartRecording());

    // Listen for changes
    const handleRecordingChange = (payload: { state: RecordingStatus }) => {
      setStatus(payload.state);
    };

    const handleIndividualRecording = (payload: { state: string }) => {
      if (payload.state === 'Ask') {
        setShowConsent(true);
      }
    };

    client.on('recording-change', handleRecordingChange);
    client.on('individual-recording-change', handleIndividualRecording);

    return () => {
      client.off('recording-change', handleRecordingChange);
      client.off('individual-recording-change', handleIndividualRecording);
    };
  }, [client, recordingClient]);

  const startRecording = async () => {
    try {
      await recordingClient.startCloudRecording();
    } catch (error) {
      console.error('Start recording failed:', error);
    }
  };

  const stopRecording = async () => {
    try {
      await recordingClient.stopCloudRecording();
    } catch (error) {
      console.error('Stop recording failed:', error);
    }
  };

  const pauseRecording = async () => {
    try {
      await recordingClient.pauseCloudRecording();
    } catch (error) {
      console.error('Pause recording failed:', error);
    }
  };

  const resumeRecording = async () => {
    try {
      await recordingClient.resumeCloudRecording();
    } catch (error) {
      console.error('Resume recording failed:', error);
    }
  };

  const acceptConsent = async () => {
    await recordingClient.acceptIndividualRecording();
    setShowConsent(false);
  };

  const declineConsent = async () => {
    await recordingClient.declineIndividualRecording();
    setShowConsent(false);
  };

  const isRecording = status === RecordingStatus.Recording;
  const isPaused = status === RecordingStatus.Paused;

  return (
    <div className="recording-controls">
      {/* Recording indicator */}
      {(isRecording || isPaused) && (
        <div className={`recording-indicator ${isPaused ? 'paused' : ''}`}>
          <span className="recording-dot" />
          {isPaused ? 'Recording Paused' : 'Recording'}
        </div>
      )}

      {/* Host controls */}
      {isHost && canRecord && (
        <div className="recording-buttons">
          {!isRecording && !isPaused && (
            <button onClick={startRecording}>Start Recording</button>
          )}

          {isRecording && (
            <>
              <button onClick={pauseRecording}>Pause</button>
              <button onClick={stopRecording}>Stop</button>
            </>
          )}

          {isPaused && (
            <>
              <button onClick={resumeRecording}>Resume</button>
              <button onClick={stopRecording}>Stop</button>
            </>
          )}
        </div>
      )}

      {/* Consent dialog */}
      {showConsent && (
        <div className="consent-dialog">
          <p>The host would like to record this session. Do you consent?</p>
          <button onClick={acceptConsent}>Accept</button>
          <button onClick={declineConsent}>Decline</button>
        </div>
      )}
    </div>
  );
};
```

## Key Points

1. **Check `canStartRecording()` first** - Recording must be enabled on the account
2. **Only host/manager can control recording** - Regular participants can only consent
3. **Handle consent for individual recording** - Listen to `individual-recording-change`
4. **Show recording indicator** - Let participants know they're being recorded
5. **Recordings are available in Zoom portal** - After session ends, recordings appear in account

## Error Handling

```javascript
try {
  await recordingClient.startCloudRecording();
} catch (error) {
  if (error.type === 'INVALID_OPERATION') {
    // Recording not available or already recording
  } else if (error.type === 'INSUFFICIENT_PRIVILEGES') {
    // User doesn't have permission to record
  }
}
```

## Related Documentation

- [Event Handling](event-handling.md) - Recording events
- [API Reference](../references/web-reference.md) - Full RecordingClient API

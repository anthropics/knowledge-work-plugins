# Live Transcription

Complete guide to implementing live transcription in the Zoom Video SDK for Web.

## Prerequisites

- Live transcription must be enabled on your Zoom account
- Session must have live transcription feature available

## Getting the Transcription Client

```javascript
// Get transcription client after joining session
const transcriptionClient = client.getLiveTranscriptionClient();
```

## Basic Operations

### Start Live Transcription

```javascript
try {
  await transcriptionClient.startLiveTranscription();
  console.log('Live transcription started');
} catch (error) {
  console.error('Failed to start transcription:', error);
}
```

### Check Transcription Status

```javascript
const status = transcriptionClient.getLiveTranscriptionStatus();

console.log('Transcription enabled:', status.isLiveTranscriptionEnabled);
console.log('Caption language:', status.captionLanguage);
console.log('Translation settings:', status.translatedSetting);
```

### Set Speaking Language

```javascript
import { LiveTranscriptionLanguage } from '@zoom/videosdk';

// Set the language you're speaking
await transcriptionClient.setSpeakingLanguage(
  LiveTranscriptionLanguage.English
);
```

### Set Translation Language

```javascript
// Translate transcriptions to another language
await transcriptionClient.setTranslationLanguage(
  LiveTranscriptionLanguage.Spanish
);

// Disable translation
await transcriptionClient.setTranslationLanguage(); // No argument
```

## Receiving Transcription Messages

```javascript
// Listen for transcription text
client.on('caption-message', (payload) => {
  const {
    msgId,       // Message ID
    text,        // Transcribed text
    userId,      // Speaker's user ID
    displayName, // Speaker's display name
    source,      // 'caption' or 'translation'
    language,    // Language code
    done,        // true = final, false = interim
    timestamp,   // Unix timestamp
  } = payload;

  if (done) {
    // Final transcription - display permanently
    addFinalTranscription(displayName, text);
  } else {
    // Interim result - update in place
    updateInterimTranscription(displayName, text);
  }
});
```

## Transcription Events

### Caption Status Changes

```javascript
client.on('caption-status', (payload) => {
  const {
    autoCaption,        // Auto-captioning enabled
    language,           // Caption language name
    lang,               // Language code
    sessionLanguage,    // Session's transcription language
    translationStarted, // Translation active
  } = payload;

  console.log('Caption status:', payload);
});
```

### Captions Enabled/Disabled

```javascript
client.on('caption-enable', (isEnabled) => {
  if (isEnabled) {
    showCaptionUI();
  } else {
    hideCaptionUI();
  }
});
```

### Caption Language Locked

```javascript
client.on('caption-language-lock', (isLocked) => {
  if (isLocked) {
    // Host has locked the transcription language
    disableLanguageSelector();
  } else {
    enableLanguageSelector();
  }
});
```

### Host Disabled Captions

```javascript
client.on('caption-host-disable', (isDisabled) => {
  if (isDisabled) {
    console.log('Host has disabled captions');
    hideCaptionUI();
  }
});
```

## Get Transcription History

```javascript
// Get full transcription history
const history = transcriptionClient.getFullTranscriptionHistory();

// May return Promise for large histories (100,000+ records)
if (history instanceof Promise) {
  const records = await history;
  displayHistory(records);
} else {
  displayHistory(history);
}

// Get latest transcription
const latest = transcriptionClient.getLatestTranscription();
console.log('Latest:', latest);

// Get latest translation
const latestTranslation = transcriptionClient.getLatestTranslation();
console.log('Latest translation:', latestTranslation);
```

## Get Current Languages

```javascript
// Get current transcription language
const transcriptionLang = transcriptionClient.getCurrentTranscriptionLanguage();
console.log('Transcription language:', transcriptionLang);

// Get current translation language
const translationLang = transcriptionClient.getCurrentTranslationLanguage();
console.log('Translation language:', translationLang);
```

## Host Controls

### Lock Transcription Language

```javascript
// Host can lock the transcription language
await transcriptionClient.lockTranscriptionLanguage(true);  // Lock
await transcriptionClient.lockTranscriptionLanguage(false); // Unlock
```

### Disable Captions

```javascript
// Host can disable captions for everyone
await transcriptionClient.disableCaptions(true);  // Disable
await transcriptionClient.disableCaptions(false); // Enable
```

## Complete Transcription Manager

```javascript
import { LiveTranscriptionLanguage } from '@zoom/videosdk';

class TranscriptionManager {
  constructor(client) {
    this.client = client;
    this.transcriptionClient = null;
    this.transcriptions = [];
    this.interimMap = new Map(); // Track interim results by speaker
    this.onTranscriptionUpdate = null;
    this.onStatusChange = null;
  }

  init() {
    this.transcriptionClient = this.client.getLiveTranscriptionClient();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Transcription messages
    this.client.on('caption-message', (payload) => {
      this.handleCaptionMessage(payload);
    });

    // Status changes
    this.client.on('caption-status', (payload) => {
      if (this.onStatusChange) {
        this.onStatusChange(payload);
      }
    });

    // Captions enabled/disabled
    this.client.on('caption-enable', (isEnabled) => {
      if (this.onStatusChange) {
        this.onStatusChange({ enabled: isEnabled });
      }
    });
  }

  handleCaptionMessage(payload) {
    const { userId, displayName, text, done, source, timestamp } = payload;
    const key = `${userId}-${source}`;

    if (done) {
      // Final result - move from interim to final
      this.interimMap.delete(key);
      this.transcriptions.push({
        userId,
        displayName,
        text,
        source,
        timestamp,
        isFinal: true,
      });
    } else {
      // Interim result - update in place
      this.interimMap.set(key, {
        userId,
        displayName,
        text,
        source,
        timestamp,
        isFinal: false,
      });
    }

    if (this.onTranscriptionUpdate) {
      this.onTranscriptionUpdate(this.getAllTranscriptions());
    }
  }

  getAllTranscriptions() {
    // Combine final transcriptions with current interim results
    const interim = Array.from(this.interimMap.values());
    return [...this.transcriptions, ...interim];
  }

  async start() {
    await this.transcriptionClient.startLiveTranscription();
  }

  async setSpeakingLanguage(language) {
    await this.transcriptionClient.setSpeakingLanguage(language);
  }

  async setTranslationLanguage(language) {
    await this.transcriptionClient.setTranslationLanguage(language);
  }

  async disableTranslation() {
    await this.transcriptionClient.setTranslationLanguage();
  }

  getStatus() {
    return this.transcriptionClient.getLiveTranscriptionStatus();
  }

  async getHistory() {
    const history = this.transcriptionClient.getFullTranscriptionHistory();
    if (history instanceof Promise) {
      return await history;
    }
    return history;
  }
}

// Usage
const transcriptionManager = new TranscriptionManager(client);
transcriptionManager.init();

transcriptionManager.onTranscriptionUpdate = (transcriptions) => {
  renderTranscriptions(transcriptions);
};

// Start transcription
document.getElementById('start-captions').onclick = async () => {
  await transcriptionManager.start();
};

// Change language
document.getElementById('language-select').onchange = async (e) => {
  await transcriptionManager.setSpeakingLanguage(e.target.value);
};
```

## React Component

```typescript
import React, { useState, useEffect, useRef } from 'react';
import { VideoClient, LiveTranscriptionLanguage } from '@zoom/videosdk';

interface TranscriptionEntry {
  displayName: string;
  text: string;
  timestamp: number;
  isFinal: boolean;
  source: string;
}

interface TranscriptionProps {
  client: typeof VideoClient;
  isHost: boolean;
}

export const LiveTranscription: React.FC<TranscriptionProps> = ({ 
  client, 
  isHost 
}) => {
  const [transcriptions, setTranscriptions] = useState<TranscriptionEntry[]>([]);
  const [interimMap] = useState(new Map<string, TranscriptionEntry>());
  const [isEnabled, setIsEnabled] = useState(false);
  const [speakingLanguage, setSpeakingLanguage] = useState<string>('');
  const containerRef = useRef<HTMLDivElement>(null);
  
  const transcriptionClient = client.getLiveTranscriptionClient();

  useEffect(() => {
    // Get initial status
    const status = transcriptionClient.getLiveTranscriptionStatus();
    setIsEnabled(status.isLiveTranscriptionEnabled);

    // Handle caption messages
    const handleCaption = (payload: any) => {
      const { userId, displayName, text, done, source, timestamp } = payload;
      const key = `${userId}-${source}`;

      if (done) {
        interimMap.delete(key);
        setTranscriptions(prev => [...prev, {
          displayName,
          text,
          timestamp,
          isFinal: true,
          source,
        }]);
      } else {
        interimMap.set(key, {
          displayName,
          text,
          timestamp,
          isFinal: false,
          source,
        });
        // Force re-render
        setTranscriptions(prev => [...prev]);
      }
    };

    const handleEnable = (enabled: boolean) => {
      setIsEnabled(enabled);
    };

    client.on('caption-message', handleCaption);
    client.on('caption-enable', handleEnable);

    return () => {
      client.off('caption-message', handleCaption);
      client.off('caption-enable', handleEnable);
    };
  }, [client, transcriptionClient, interimMap]);

  // Auto-scroll
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [transcriptions]);

  const startTranscription = async () => {
    await transcriptionClient.startLiveTranscription();
  };

  const handleLanguageChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const language = e.target.value as LiveTranscriptionLanguage;
    setSpeakingLanguage(language);
    await transcriptionClient.setSpeakingLanguage(language);
  };

  // Combine final and interim transcriptions for display
  const allTranscriptions = [
    ...transcriptions,
    ...Array.from(interimMap.values()),
  ].sort((a, b) => a.timestamp - b.timestamp);

  return (
    <div className="transcription-panel">
      <div className="transcription-header">
        <h3>Live Transcription</h3>
        
        {!isEnabled && (
          <button onClick={startTranscription}>
            Enable Captions
          </button>
        )}

        <select value={speakingLanguage} onChange={handleLanguageChange}>
          <option value="">Select Language</option>
          <option value={LiveTranscriptionLanguage.English}>English</option>
          <option value={LiveTranscriptionLanguage.Spanish}>Spanish</option>
          <option value={LiveTranscriptionLanguage.French}>French</option>
          <option value={LiveTranscriptionLanguage.German}>German</option>
          <option value={LiveTranscriptionLanguage.Chinese}>Chinese</option>
          <option value={LiveTranscriptionLanguage.Japanese}>Japanese</option>
        </select>
      </div>

      <div className="transcription-content" ref={containerRef}>
        {allTranscriptions.map((entry, index) => (
          <div 
            key={`${entry.timestamp}-${index}`}
            className={`transcription-entry ${entry.isFinal ? 'final' : 'interim'}`}
          >
            <span className="speaker">{entry.displayName}:</span>
            <span className="text">{entry.text}</span>
          </div>
        ))}
      </div>

      <style jsx>{`
        .transcription-panel {
          display: flex;
          flex-direction: column;
          height: 300px;
          border: 1px solid #ddd;
          border-radius: 8px;
        }
        .transcription-header {
          padding: 10px;
          border-bottom: 1px solid #ddd;
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .transcription-content {
          flex: 1;
          overflow-y: auto;
          padding: 10px;
        }
        .transcription-entry {
          margin-bottom: 8px;
        }
        .transcription-entry.interim {
          color: #888;
          font-style: italic;
        }
        .speaker {
          font-weight: bold;
          margin-right: 5px;
        }
      `}</style>
    </div>
  );
};
```

## Available Languages

```typescript
// LiveTranscriptionLanguage enum
LiveTranscriptionLanguage.English
LiveTranscriptionLanguage.Spanish
LiveTranscriptionLanguage.French
LiveTranscriptionLanguage.German
LiveTranscriptionLanguage.Italian
LiveTranscriptionLanguage.Portuguese
LiveTranscriptionLanguage.Russian
LiveTranscriptionLanguage.Chinese
LiveTranscriptionLanguage.Japanese
LiveTranscriptionLanguage.Korean
// ... and more
```

## Key Points

1. **Interim vs Final** - `done=false` is interim (updating), `done=true` is final
2. **Start transcription** - Call `startLiveTranscription()` to enable
3. **Set speaking language** - Tell the system what language you're speaking
4. **Translation is optional** - Use `setTranslationLanguage()` if needed
5. **Handle large histories** - `getFullTranscriptionHistory()` may return Promise

## Key Events

| Event | When | Payload |
|-------|------|---------|
| `caption-message` | Transcription text received | Text, speaker, done flag |
| `caption-status` | Status changes | Language, enabled state |
| `caption-enable` | Captions enabled/disabled | Boolean |
| `caption-language-lock` | Language locked by host | Boolean |
| `caption-host-disable` | Host disabled captions | Boolean |

## Related Documentation

- [Event Handling](event-handling.md) - Transcription events
- [API Reference](../references/web-reference.md) - Full LiveTranscriptionClient API

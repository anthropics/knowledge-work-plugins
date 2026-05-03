# Real-Time Media Streams

Access live audio, video, transcripts, chat, and screen share from Zoom meetings via WebSocket.

## Overview

Zoom RTMS (Realtime Media Streams) provides WebSocket-based access to live meeting media for real-time AI processing, transcription, analysis, and recording - **without meeting bots**.

> **See the comprehensive RTMS skill**: [rtms/SKILL.md](../../rtms/SKILL.md)

## Skills Needed

- **[zoom-rtms](../../rtms/SKILL.md)** - Primary (comprehensive documentation)
- **webhooks** - Receive RTMS start/stop events

## Two Approaches

| Approach | Best For | Documentation |
|----------|----------|---------------|
| **SDK** (`@zoom/rtms`) | Most use cases | [SDK Quickstart](../../rtms/examples/sdk-quickstart.md) |
| **Manual WebSocket** | Full protocol control | [Manual WebSocket](../../rtms/examples/manual-websocket.md) |

## How It Works

```
RTMS Flow:
1. Meeting starts with RTMS enabled
        ↓
2. Webhook: meeting.rtms_started
        ↓
3. Connect to Signaling WebSocket
        ↓
4. Connect to Media WebSocket
        ↓
5. Receive live audio/video/transcript/chat/share
```

## Media Types

| Type | Format | Use Case |
|------|--------|----------|
| Audio | PCM 16-bit | Transcription, analysis |
| Video | H.264 | Visual AI, recording |
| Transcript | JSON | Real-time captions |

## Prerequisites

- RTMS feature enabled on app
- Webhook endpoint
- WebSocket client

## Quick Start

```javascript
// Handle RTMS webhook
app.post('/webhook', (req, res) => {
  if (req.body.event === 'meeting.rtms_started') {
    const { server_urls, signature } = req.body.payload;
    
    // Connect to RTMS
    const ws = new WebSocket(server_urls);
    ws.on('message', (data) => {
      // Process live media
    });
  }
  res.status(200).send();
});
```

## Common Tasks

### Connecting to RTMS WebSocket

```javascript
const WebSocket = require('ws');
const crypto = require('crypto');

// Webhook handler receives RTMS connection info
app.post('/webhook', (req, res) => {
  const { event, payload } = req.body;
  
  if (event === 'meeting.rtms_started') {
    const { server_urls, stream_id, signature } = payload;
    
    // Connect to RTMS WebSocket
    connectToRTMS(server_urls[0], stream_id, signature);
  }
  
  res.status(200).send();
});

function connectToRTMS(url, streamId, signature) {
  const ws = new WebSocket(url);
  
  ws.on('open', () => {
    // Authenticate
    ws.send(JSON.stringify({
      type: 'auth',
      stream_id: streamId,
      signature: signature
    }));
  });
  
  ws.on('message', (data) => {
    const message = JSON.parse(data);
    handleRTMSMessage(message);
  });
  
  ws.on('error', (err) => {
    console.error('RTMS error:', err);
    // Implement reconnection logic
  });
}
```

### Processing Audio Streams

```javascript
function handleRTMSMessage(message) {
  switch (message.type) {
    case 'audio':
      processAudio(message);
      break;
    case 'video':
      processVideo(message);
      break;
    case 'transcript':
      processTranscript(message);
      break;
  }
}

function processAudio(message) {
  // Audio format: PCM 16-bit, 16kHz, mono
  const audioBuffer = Buffer.from(message.data, 'base64');
  
  // Send to transcription service (e.g., OpenAI Whisper, Deepgram)
  transcriptionService.processChunk(audioBuffer, {
    sampleRate: 16000,
    channels: 1,
    format: 'pcm_s16le'
  });
}
```

### Handling Video Frames

```javascript
function processVideo(message) {
  // Video format: H.264 encoded
  const videoFrame = Buffer.from(message.data, 'base64');
  
  // Decode H.264 frame (requires ffmpeg or similar)
  const decodedFrame = h264Decoder.decode(videoFrame);
  
  // Process for AI (face detection, emotion analysis, etc.)
  aiProcessor.analyzeFrame(decodedFrame, {
    width: message.width,
    height: message.height,
    timestamp: message.timestamp
  });
}
```

### Real-Time Transcription Integration

```javascript
// Using Zoom's built-in transcript stream
function processTranscript(message) {
  const { text, speaker_id, timestamp, is_final } = message;
  
  if (is_final) {
    // Final transcript segment
    saveTranscript({
      speaker: speaker_id,
      text: text,
      timestamp: timestamp
    });
    
    // Optionally analyze with AI
    analyzeWithAI(text);
  } else {
    // Partial transcript - update UI in real-time
    updateLiveCaption(text);
  }
}

// Integration with external AI for summarization
async function analyzeWithAI(transcript) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{
      role: 'system',
      content: 'Extract action items from this meeting segment.'
    }, {
      role: 'user',
      content: transcript
    }]
  });
  
  return response.choices[0].message.content;
}
```

### Error Handling & Reconnection

```javascript
class RTMSClient {
  constructor(config) {
    this.config = config;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }
  
  connect() {
    this.ws = new WebSocket(this.config.url);
    
    this.ws.on('close', () => {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        const delay = Math.pow(2, this.reconnectAttempts) * 1000;
        setTimeout(() => this.connect(), delay);
        this.reconnectAttempts++;
      }
    });
    
    this.ws.on('open', () => {
      this.reconnectAttempts = 0;
      this.authenticate();
    });
  }
}
```

## Resources

- **RTMS docs**: https://developers.zoom.us/docs/rtms/
- **RTMS Quick Start**: https://developers.zoom.us/docs/rtms/getting-started/

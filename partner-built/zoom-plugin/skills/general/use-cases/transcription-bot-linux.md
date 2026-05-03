# Transcription Bot (Linux)

Build a production-ready transcription bot using Meeting SDK for Linux to automatically transcribe Zoom meetings.

## Overview

A transcription bot joins Zoom meetings as a visible participant, captures raw audio, and streams it to a transcription service (AssemblyAI, Whisper, etc.) for real-time or post-meeting transcription.

## Skills Needed

- **[meeting-sdk/linux](../../meeting-sdk/linux/SKILL.md)** - Primary (headless meeting bot)
- **[zoom-rest-api](../../rest-api/SKILL.md)** - Get meeting details, OBF tokens
- **[zoom-oauth](../../oauth/SKILL.md)** - JWT token generation for SDK auth

## Architecture

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐    ┌──────────────┐
│  Meeting     │───▶│ Meeting SDK Bot │───▶│  Raw Audio       │───▶│ Transcription│
│  Started     │    │ (Linux/Docker)  │    │  Stream (PCM)    │    │  Service     │
│              │    │                 │    │  32kHz, 16-bit   │    │ (AssemblyAI) │
└──────────────┘    └─────────────────┘    └──────────────────┘    └──────────────┘
                            │                        │                       │
                            ▼                        ▼                       ▼
                    ┌─────────────────┐    ┌──────────────────┐    ┌──────────────┐
                    │ 1. Get OBF Token│    │ 2. StartRaw      │    │ 3. Store     │
                    │    (REST API)   │    │    Recording     │    │    Transcript│
                    └─────────────────┘    └──────────────────┘    └──────────────┘
```

## Implementation Steps

### Step 1: Generate JWT & OBF Tokens

**JWT Token** (SDK authentication):
```bash
# Using zoom-oauth skill
curl -X POST https://your-auth-service.com/generate-jwt \
  -d '{"client_id": "YOUR_CLIENT_ID", "client_secret": "YOUR_CLIENT_SECRET"}'
```

**OBF Token** (join external meetings):
```bash
# Via REST API
curl -X POST "https://api.zoom.us/v2/users/{userId}/token?type=obf&ttl=7200" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

See: [zoom-oauth](../../oauth/SKILL.md), [bot-authentication](../../meeting-sdk/references/bot-authentication.md)

### Step 2: Initialize Meeting SDK

**Full implementation**: [meeting-sdk/linux](../../meeting-sdk/linux/linux.md)

```cpp
#include "zoom_sdk.h"
#include <glib.h>

USING_ZOOM_SDK_NAMESPACE

// Initialize SDK
InitParam init_params;
init_params.strWebDomain = "https://zoom.us";
init_params.enableLogByDefault = true;
init_params.rawdataOpts.audioRawDataMemoryMode = ZoomSDKRawDataMemoryModeHeap;

SDKError err = InitSDK(init_params);
if (err != SDKERR_SUCCESS) {
    std::cerr << "InitSDK failed: " << err << std::endl;
    return 1;
}

// Authenticate SDK with JWT
AuthContext auth_ctx;
auth_ctx.jwt_token = jwt_token_from_step1;

IAuthService* auth_service;
CreateAuthService(&auth_service);
auth_service->SetEvent(new MyAuthDelegate());
auth_service->SDKAuth(auth_ctx);
```

### Step 3: Join Meeting

```cpp
// In onAuthenticationReturn callback
class MyAuthDelegate : public IAuthServiceEvent {
    void onAuthenticationReturn(AuthResult ret) override {
        if (ret == AUTHRET_SUCCESS) {
            JoinParam join_param;
            join_param.userType = SDK_UT_WITHOUT_LOGIN;
            
            auto& params = join_param.param.withoutloginuserJoin;
            params.meetingNumber = 1234567890;
            params.userName = "Transcription Bot";
            params.psw = meeting_password;
            params.isVideoOff = true;   // Bot doesn't need video
            params.isAudioOff = false;  // Need audio for transcription
            params.app_privilege_token = obf_token;  // From Step 1
            
            meeting_service->Join(join_param);
        }
    }
};
```

### Step 4: Start Raw Recording & Subscribe to Audio

```cpp
class MyMeetingDelegate : public IMeetingServiceEvent {
    void onMeetingStatusChanged(MeetingStatus status, int iResult) override {
        if (status == MEETING_STATUS_INMEETING) {
            std::cout << "[BOT] Joined meeting successfully" << std::endl;
            
            // Get recording controller
            auto* record_ctrl = meeting_service->GetMeetingRecordingController();
            
            // Check permission
            SDKError can_record = record_ctrl->CanStartRawRecording();
            if (can_record != SDKERR_SUCCESS) {
                std::cerr << "[ERROR] Cannot start raw recording: " << can_record << std::endl;
                std::cerr << "Need: host/co-host OR recording token" << std::endl;
                return;
            }
            
            // Start raw recording (enables raw data access)
            SDKError err = record_ctrl->StartRawRecording();
            if (err != SDKERR_SUCCESS) {
                std::cerr << "[ERROR] StartRawRecording failed: " << err << std::endl;
                return;
            }
            
            std::cout << "[BOT] Raw recording started, subscribing to audio..." << std::endl;
            
            // Subscribe to audio
            auto* audio_helper = GetAudioRawdataHelper();
            if (!audio_helper) {
                std::cerr << "[ERROR] Failed to get audio helper" << std::endl;
                return;
            }
            
            SDKError audio_err = audio_helper->subscribe(new TranscriptionAudioDelegate());
            if (audio_err != SDKERR_SUCCESS) {
                std::cerr << "[ERROR] Audio subscribe failed: " << audio_err << std::endl;
            } else {
                std::cout << "[BOT] Subscribed to audio successfully" << std::endl;
            }
        }
    }
};
```

### Step 5: Process Audio & Send to Transcription Service

```cpp
class TranscriptionAudioDelegate : public IZoomSDKAudioRawDataDelegate {
private:
    AssemblyAIClient transcription_client;
    std::ofstream debug_file;  // For debugging: save raw audio
    
public:
    TranscriptionAudioDelegate() {
        // Initialize transcription service connection
        transcription_client.connect();
        
        // Optional: Save raw audio for debugging
        debug_file.open("meeting_audio.pcm", std::ios::binary);
    }
    
    void onMixedAudioRawDataReceived(AudioRawData* data) override {
        // Get audio properties
        uint32_t sample_rate = data->GetSampleRate();  // Typically 32000 Hz
        uint32_t channels = data->GetChannelNum();     // 1 (mono) or 2 (stereo)
        uint32_t buffer_len = data->GetBufferLen();
        char* buffer = data->GetBuffer();
        
        // Send to transcription service
        transcription_client.send_audio(buffer, buffer_len, sample_rate, channels);
        
        // Optional: Save for debugging
        if (debug_file.is_open()) {
            debug_file.write(buffer, buffer_len);
        }
    }
    
    void onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t node_id) override {
        // Per-user audio (optional - for speaker diarization)
        // node_id identifies the speaker
    }
    
    ~TranscriptionAudioDelegate() {
        transcription_client.disconnect();
        if (debug_file.is_open()) {
            debug_file.close();
        }
    }
};
```

### Step 6: Handle Transcription Results

```cpp
class AssemblyAIClient {
private:
    WebSocketClient ws;
    std::string api_key;
    
public:
    void connect() {
        ws.connect("wss://api.assemblyai.com/v2/realtime/ws?sample_rate=32000", {
            {"Authorization": api_key}
        });
        
        // Listen for transcription results
        ws.on_message([](const std::string& message) {
            json result = json::parse(message);
            if (result["message_type"] == "FinalTranscript") {
                std::string text = result["text"];
                float confidence = result["confidence"];
                
                std::cout << "[TRANSCRIPT] " << text << " (confidence: " << confidence << ")" << std::endl;
                
                // Store in database
                save_to_database(text, timestamp);
            }
        });
    }
    
    void send_audio(char* buffer, size_t len, uint32_t sample_rate, uint32_t channels) {
        // Convert PCM to base64 (AssemblyAI expects base64-encoded audio)
        std::string encoded = base64_encode((unsigned char*)buffer, len);
        
        json audio_data = {
            {"audio_data", encoded}
        };
        
        ws.send(audio_data.dump());
    }
};
```

## Production Patterns

### Retry Logic for Meeting Join

**See**: [meeting-sdk-bot.md](../../meeting-sdk/linux/meeting-sdk-bot.md)

```cpp
bool joinMeetingWithRetry(int max_attempts = 5, int retry_interval_ms = 60000) {
    for (int attempt = 1; attempt <= max_attempts; attempt++) {
        std::cout << "[JOIN] Attempt " << attempt << "/" << max_attempts << std::endl;
        
        SDKError err = meeting_service->Join(join_param);
        
        if (err == SDKERR_SUCCESS && waitForJoinCallback()) {
            std::cout << "[JOIN] Success!" << std::endl;
            return true;
        }
        
        if (attempt < max_attempts) {
            std::cout << "[JOIN] Retrying in " << (retry_interval_ms / 1000) << "s..." << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(retry_interval_ms));
        }
    }
    
    std::cerr << "[JOIN] Failed after " << max_attempts << " attempts" << std::endl;
    return false;
}
```

### Docker Deployment

**Dockerfile**:
```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential cmake \
    libx11-xcb1 libxcb-xfixes0 libxcb-shape0 libxcb-shm0 \
    libxcb-randr0 libxcb-image0 libxcb-keysyms1 libxcb-xtest0 \
    libglib2.0-dev libcurl4-openssl-dev \
    pulseaudio pulseaudio-utils

# Setup PulseAudio for headless audio
RUN mkdir -p ~/.config && \
    echo "[General]\nsystem.audio.type=default" > ~/.config/zoomus.conf

# Copy SDK and app
COPY zoom_meeting_sdk/ /app/lib/
COPY transcription_bot /app/

# Setup PulseAudio virtual devices
COPY setup-pulseaudio.sh /app/
RUN chmod +x /app/setup-pulseaudio.sh

CMD ["/app/setup-pulseaudio.sh && /app/transcription_bot"]
```

**setup-pulseaudio.sh**:
```bash
#!/bin/bash
# Start PulseAudio daemon
pulseaudio --start --exit-idle-time=-1

# Create virtual speaker
pactl load-module module-null-sink sink_name=virtual_speaker

# Create virtual microphone
pactl load-module module-null-sink sink_name=virtual_mic

echo "PulseAudio configured for headless operation"
```

## Configuration Management

**Environment Variables** (.env):
```bash
# Zoom SDK Credentials
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret

# Meeting Info
ZOOM_MEETING_NUMBER=1234567890
ZOOM_MEETING_PASSWORD=abc123

# Transcription Service
ASSEMBLYAI_API_KEY=your_api_key

# Bot Config
BOT_NAME="Transcription Bot"
BOT_JOIN_RETRY_ATTEMPTS=5
BOT_JOIN_RETRY_INTERVAL_MS=60000
```

**Loading config**:
```cpp
#include <cstdlib>

struct BotConfig {
    std::string client_id;
    std::string client_secret;
    uint64_t meeting_number;
    std::string meeting_password;
    std::string bot_name;
    int join_retry_attempts;
    int join_retry_interval_ms;
};

BotConfig loadConfig() {
    BotConfig cfg;
    cfg.client_id = getenv("ZOOM_CLIENT_ID") ?: "";
    cfg.client_secret = getenv("ZOOM_CLIENT_SECRET") ?: "";
    cfg.meeting_number = std::stoull(getenv("ZOOM_MEETING_NUMBER") ?: "0");
    cfg.meeting_password = getenv("ZOOM_MEETING_PASSWORD") ?: "";
    cfg.bot_name = getenv("BOT_NAME") ?: "Transcription Bot";
    cfg.join_retry_attempts = atoi(getenv("BOT_JOIN_RETRY_ATTEMPTS") ?: "5");
    cfg.join_retry_interval_ms = atoi(getenv("BOT_JOIN_RETRY_INTERVAL_MS") ?: "60000");
    return cfg;
}
```

## Common Issues & Solutions

### Issue: Raw Recording Permission Denied

**Error**: `CanStartRawRecording()` returns `SDKERR_NO_PERMISSION`

**Solution**:
1. Bot needs to be **host/co-host**, OR
2. Use **recording token** from [REST API](https://developers.zoom.us/docs/meeting-sdk/apis/#operation/meetingLocalRecordingJoinToken), OR
3. Host grants recording permission manually

**See**: [meeting-sdk-bot.md#raw-recording-permission-denied](../../meeting-sdk/linux/meeting-sdk-bot.md#raw-recording-permission-denied)

### Issue: No Audio in Docker

**Error**: Audio subscription succeeds but no audio callbacks

**Solution**: Create `~/.config/zoomus.conf`:
```bash
mkdir -p ~/.config
echo "[General]\nsystem.audio.type=default" > ~/.config/zoomus.conf
```

**See**: [linux-reference.md#pulseaudio-setup](../../meeting-sdk/linux/references/linux-reference.md#pulseaudio-setup)

### Issue: Callbacks Not Firing

**Error**: `onMeetingStatusChanged()` never called after `Join()`

**Solution**: Add GLib main loop:
```cpp
#include <glib.h>

GMainLoop* loop = g_main_loop_new(NULL, FALSE);
g_main_loop_run(loop);  // Blocks until quit
```

## Related Use Cases

- **[AI Meeting Assistant](ai-integration.md)** - Add AI analysis on top of transcription
- **[Recording Bot](../../meeting-sdk/linux/concepts/high-level-scenarios.md#scenario-2-recording-bot)** - Record video + audio with sync
- **[Real-time Media Streams](real-time-media-streams.md)** - Alternative: RTMS for invisible bots

## Related Skills

- **[meeting-sdk/linux](../../meeting-sdk/linux/SKILL.md)** - Complete Meeting SDK Linux guide
- **[zoom-rest-api](../../rest-api/SKILL.md)** - Get meetings, OBF tokens
- **[zoom-oauth](../../oauth/SKILL.md)** - JWT token generation

## Sample Code

**Complete sample**: [meeting-sdk/linux/concepts/high-level-scenarios.md](../../meeting-sdk/linux/concepts/high-level-scenarios.md#scenario-1)

**Official samples**:
- https://github.com/zoom/meetingsdk-linux-raw-recording-sample
- https://github.com/zoom/meetingsdk-headless-linux-sample

## Key Takeaways

✅ **Use OBF tokens** for joining external meetings (require owner present)  
✅ **Setup PulseAudio** for Docker/headless audio access  
✅ **Call StartRawRecording()** before subscribing to audio  
✅ **Use heap memory mode** for raw data (`ZoomSDKRawDataMemoryModeHeap`)  
✅ **Implement retry logic** for meeting join (OBF requires owner present)  
✅ **Add GLib main loop** for callbacks to work  
✅ **Stream audio in real-time** for best transcription latency

# Meeting Bots

Build bots that join Zoom meetings for AI, transcription, and automation.

## Overview

Meeting bots are headless applications that join Zoom meetings as participants to perform tasks like recording, transcription, real-time AI processing, or automated interactions.

## Skills Needed

- **meeting-sdk/linux** - Visible bot join flow, raw recording, and raw media access
- **zoom-rest-api** - Meeting lookup plus OBF/ZAK retrieval, optional cloud-recording settings
- **zoom-webhooks** - Optional if you want Zoom-managed cloud recording download after the meeting
- **zoom-rtms** - Alternative when you need invisible media access instead of a visible participant bot

## Architecture

```
Meeting Bot Architecture:
┌─────────────────┐     ┌─────────────────┐
│   Zoom Meeting  │────▶│  Bot (Linux)    │
│                 │     │  - Meeting SDK  │
│                 │◀────│  - Raw audio    │
└─────────────────┘     │  - Raw video    │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  AI Pipeline    │
                        │  - Transcription│
                        │  - Analysis     │
                        └─────────────────┘
```

## Platform

| Platform | Recommended |
|----------|-------------|
| Linux | Yes - headless, server-side |
| Windows | Possible but not typical |
| macOS | Possible but not typical |

## Key Features

- Join meetings programmatically
- Access raw audio/video data
- Start and stop raw recording explicitly
- Real-time transcription
- AI processing (sentiment, summarization)

## Automatic Join + Recording Pattern

Use this chain when the user asks for a bot that automatically joins and records a meeting:

```text
zoom-rest-api
  -> fetch meeting metadata
  -> mint OBF/ZAK token
meeting-sdk/linux
  -> join as visible participant
  -> StartRawRecording()
  -> subscribe audio/video delegates
  -> write PCM/YUV or send to downstream pipeline
optional zoom-webhooks + zoom-rest-api
  -> receive recording.completed
  -> download Zoom-managed cloud recording assets
```

### Raw Recording Control

```cpp
void onMeetingStatusChanged(MeetingStatus status, int iResult) {
    if (status != MEETING_STATUS_INMEETING) return;

    auto* recordCtrl = m_meetingService->GetMeetingRecordingController();
    if (!recordCtrl) {
        throw std::runtime_error("recording_controller_unavailable");
    }

    if (recordCtrl->CanStartRawRecording() != SDKERR_SUCCESS) {
        throw std::runtime_error("raw_recording_not_permitted");
    }

    SDKError err = recordCtrl->StartRawRecording();
    if (err != SDKERR_SUCCESS) {
        throw std::runtime_error("start_raw_recording_failed");
    }

    GetAudioRawdataHelper()->subscribe(new AudioRawDataDelegate(), true);

    IZoomSDKRenderer* renderer = nullptr;
    createRenderer(&renderer, new VideoRawDataDelegate());
    renderer->setRawDataResolution(ZoomSDKResolution_720P);
    renderer->subscribe(activeSpeakerUserId, RAW_DATA_TYPE_VIDEO);
}
```

### Choose the Right Recording Output

| Requirement | Correct path |
|-------------|--------------|
| Bot-owned audio/video files or real-time AI processing | Meeting SDK Linux raw recording |
| Zoom-hosted MP4/M4A/transcript files after meeting end | Cloud recording settings + webhooks + recordings REST API |

`StartRawRecording()` enables raw media flow. It does not create a finished MP4 by itself. You still need to persist PCM/YUV or post-process it with your own pipeline.

## Bot Implementation Patterns

### 1. Bot Authentication Flow

```cpp
// Step 1: Generate JWT for SDK authentication
void generateJWT(const string& key, const string& secret) {
    auto iat = chrono::system_clock::now();
    auto exp = iat + chrono::hours{24};
    
    m_jwt = jwt::create()
        .set_type("JWT")
        .set_issued_at(iat)
        .set_expires_at(exp)
        .set_payload_claim("appKey", claim(key))
        .set_payload_claim("tokenExp", claim(exp))
        .sign(algorithm::hs256{secret});
}

// Step 2: Authenticate SDK
AuthContext ctx;
ctx.jwt_token = m_jwt;
m_authService->SDKAuth(ctx);
// Wait for onAuthenticationReturn callback
```

### 2. Joining a Meeting as a Bot

```cpp
JoinParam joinParam;
joinParam.userType = SDK_UT_WITHOUT_LOGIN;
JoinParam4WithoutLogin& param = joinParam.param.withoutloginuserJoin;
param.meetingNumber = meetingNumber;
param.userName = "My Transcription Bot";  // Display name
param.psw = password;
param.isVideoOff = true;   // Bots typically don't need video
param.isAudioOff = false;  // Need audio for transcription

// For own meetings: Use ZAK token
param.userZAK = zakToken;

// For external meetings (after Feb 2026): Use OBF token
param.onBehalfToken = obfToken;

err = m_meetingService->Join(joinParam);
```

**Token Requirements:**

| Meeting Type | Required Tokens |
|--------------|-----------------|
| Your own meetings | JWT + ZAK |
| External meetings (before Feb 2026) | JWT only |
| External meetings (after Feb 2026) | JWT + OBF |

### 3. Capturing Audio Streams

```cpp
class AudioRawDataDelegate : public IZoomSDKAudioRawDataDelegate {
public:
    void onMixedAudioRawDataReceived(AudioRawData *data) override {
        // Mixed audio from all participants
        // Format: 16-bit PCM, 16kHz or 32kHz, mono
        
        // Send to transcription service
        transcriptionService.process(
            data->GetBuffer(), 
            data->GetBufferLen(),
            data->GetSampleRate()
        );
    }
    
    void onOneWayAudioRawDataReceived(AudioRawData* data, uint32_t node_id) override {
        // Individual participant audio - useful for speaker identification
        speakerIdentifier.process(node_id, data);
    }
};

// Subscribe after joining meeting
auto* pRawDataHelper = GetAudioRawdataHelper();
pRawDataHelper->subscribe(new AudioRawDataDelegate());
```

### 4. Processing Video Frames

```cpp
class VideoRawDataDelegate : public IZoomSDKRendererDelegate {
public:
    void onRawDataFrameReceived(YUVRawDataI420 *data) override {
        // Format: I420 (YUV 4:2:0) - contiguous planar data
        int width = data->GetStreamWidth();
        int height = data->GetStreamHeight();
        
        // Option 1: Save raw YUV for later processing
        yuvFile.write(data->GetYBuffer(), width * height);
        yuvFile.write(data->GetUBuffer(), (width/2) * (height/2));
        yuvFile.write(data->GetVBuffer(), (width/2) * (height/2));
        
        // Option 2: Convert to OpenCV for real-time processing
        // (requires copying planes into contiguous buffer first)
    }
};

// Subscribe to specific user's video
auto* pVideoHelper = GetRawdataRendererHelper();
pVideoHelper->setRawDataResolution(ZoomSDKResolution_720P);
pVideoHelper->subscribe(userId, RAW_DATA_TYPE_VIDEO, new VideoRawDataDelegate());
```

### 5. Handling Participant Events

```cpp
class MeetingParticipantsDelegate : public IMeetingParticipantsCtrlEvent {
public:
    void onUserJoin(IList<unsigned int>* lstUserID, const wchar_t* strUserList) override {
        // New participants joined
        for (int i = 0; i < lstUserID->GetCount(); i++) {
            unsigned int userId = lstUserID->GetItem(i);
            auto userInfo = m_participantsCtrl->GetUserByUserID(userId);
            log("User joined: " + userInfo->GetUserName());
            
            // Subscribe to their video if needed
            subscribeToUserVideo(userId);
        }
    }
    
    void onUserLeft(IList<unsigned int>* lstUserID, const wchar_t* strUserList) override {
        // Participants left
    }
    
    void onHostChangeNotification(unsigned int userId) override {
        // Host changed
    }
};
```

### 6. Graceful Disconnection

```cpp
void Bot::leaveMeeting() {
    // Stop raw data subscriptions
    GetAudioRawdataHelper()->unSubscribe();
    
    // Stop recording if active
    auto recCtl = m_meetingService->GetMeetingRecordingController();
    recCtl->StopRawRecording();
    
    // Leave meeting
    m_meetingService->Leave(LEAVE_MEETING);
    
    // Wait for onMeetingStatusChanged(MEETING_STATUS_ENDED)
}

// Handle unexpected disconnection
void onMeetingStatusChanged(MeetingStatus status, int iResult) {
    if (status == MEETING_STATUS_ENDED || status == MEETING_STATUS_FAILED) {
        cleanup();
        // Optionally reconnect
        if (shouldReconnect) {
            scheduleReconnect();
        }
    }
}
```

## Scaling Considerations

| Consideration | Recommendation |
|---------------|----------------|
| **Bot per meeting** | 1 bot instance per meeting (SDK limitation) |
| **Container deployment** | Use Kubernetes with 1 pod per bot |
| **Resource allocation** | 2-4 GB RAM, 1-2 CPU cores per bot |
| **Queue management** | Use message queue (Redis, RabbitMQ) for bot assignments |
| **Health monitoring** | Implement heartbeat checks for bot instances |

## Meeting SDK vs Video SDK for Bots

| Aspect | Meeting SDK | Video SDK |
|--------|-------------|-----------|
| Joins | Zoom meetings | Video SDK sessions |
| Features | Full meeting features | Core video features |
| Use case | Meeting bots, recording | Custom video apps, telehealth |

**Choose Meeting SDK** for: Joining existing Zoom meetings, transcription bots
**Choose Video SDK** for: Custom video sessions you control, BYOS recording

## Detailed Platform Guides

### Meeting SDK (Linux) - Recommended for Bots
- **[Meeting SDK Linux - Quick Start](../../meeting-sdk/linux/linux.md)** - Complete setup guide
- **[High-Level Bot Scenarios](../../meeting-sdk/linux/concepts/high-level-scenarios.md)** - Production architectures
- **[Resilient Bot Pattern](../../meeting-sdk/linux/meeting-sdk-bot.md)** - Retry logic, OBF tokens
- **[Linux Platform Reference](../../meeting-sdk/linux/references/linux-reference.md)** - Dependencies, Docker, troubleshooting

### Specific Use Cases
- **[Transcription Bot (Linux)](transcription-bot-linux.md)** - Step-by-step transcription bot guide
- **[AI Integration](ai-integration.md)** - AI-powered meeting analysis
- **[Real-time Media Streams](real-time-media-streams.md)** - RTMS alternative (invisible bots)

## Resources

- **Meeting SDK Linux Docs**: https://developers.zoom.us/docs/meeting-sdk/linux/
- **Meeting SDK Linux API**: https://marketplacefront.zoom.us/sdk/meeting/linux/
- **Headless Sample (Modern)**: https://github.com/zoom/meetingsdk-headless-linux-sample
- **Raw Recording Sample (Traditional)**: https://github.com/zoom/meetingsdk-linux-raw-recording-sample
- **RTMS (Alternative)**: https://developers.zoom.us/docs/rtms/

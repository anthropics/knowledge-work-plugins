# Singleton Hierarchy: Navigation Guide

## Overview

The Zoom Windows Meeting SDK uses a **service locator pattern** - a tree of singletons where you navigate from root services down to specific features. You don't construct objects; you traverse to them.

```
You want to...              You navigate to...
─────────────────────────────────────────────────────
Mute audio                  IMeetingService → IMeetingAudioController
Create breakout rooms       IMeetingService → IMeetingBOController → IBOCreator
Control remote camera       IMeetingService → IMeetingVideoController → IMeetingCameraHelper
Start live stream           IMeetingService → IMeetingLiveStreamController
Add Q&A questions           IMeetingService → IMeetingQAController
Enable interpretation       IMeetingService → IMeetingInterpretationController
Batch invite contacts       IAuthService → INotificationServiceHelper → IPresenceHelper → IBatchRequestContactHelper
```

---

## Complete Hierarchy (4 Levels Deep)

```
Level 0: Global Factory Functions (zoom_sdk.h)
│
├─► Level 1: IAuthService
│   ├─► Level 2: IDirectShareServiceHelper                              [LEAF]
│   └─► Level 2: INotificationServiceHelper
│       └─► Level 3: IPresenceHelper
│           └─► Level 4: IBatchRequestContactHelper                     [LEAF - MAX DEPTH]
│
├─► Level 1: IMeetingService
│   │
│   │   ══════════════════════════════════════════════════════════════
│   │   CROSS-PLATFORM CONTROLLERS (All platforms)
│   │   ══════════════════════════════════════════════════════════════
│   │
│   ├─► Level 2: IMeetingVideoController
│   │   ├─► Level 3: IMeetingCameraHelper                               [LEAF]
│   │   ├─► Level 3: ISetVideoOrderHelper                               [LEAF - Windows]
│   │   └─► Level 3: ICameraController                                  [LEAF - Windows]
│   │
│   ├─► Level 2: IMeetingAudioController                                [LEAF]
│   ├─► Level 2: IMeetingShareController                                [LEAF]
│   ├─► Level 2: IMeetingChatController                                 [LEAF]
│   ├─► Level 2: IMeetingRecordingController                            [LEAF]
│   ├─► Level 2: IMeetingParticipantsController                         [LEAF]
│   ├─► Level 2: IMeetingWaitingRoomController                          [LEAF]
│   ├─► Level 2: IMeetingWebinarController                              [LEAF]
│   ├─► Level 2: IMeetingRawArchivingController                         [LEAF]
│   ├─► Level 2: IMeetingReminderController                             [LEAF]
│   ├─► Level 2: IMeetingEncryptionController                           [LEAF]
│   ├─► Level 2: IMeetingConfiguration                                  [LEAF]
│   ├─► Level 2: IListFactory                                           [LEAF - utility]
│   │
│   ├─► Level 2: IMeetingBOController (Breakout Rooms)
│   │   ├─► Level 3: IBOCreator
│   │   │   └─► Level 4: IBatchCreateBOHelper                           [LEAF - MAX DEPTH]
│   │   ├─► Level 3: IBOAdmin                                           [LEAF]
│   │   ├─► Level 3: IBOAssistant                                       [LEAF]
│   │   ├─► Level 3: IBOAttendee                                        [LEAF]
│   │   └─► Level 3: IBOData                                            [LEAF]
│   │
│   ├─► Level 2: IMeetingAICompanionController
│   │   ├─► Level 3: IMeetingSmartSummaryHelper                         [LEAF - DEPRECATED]
│   │   ├─► Level 3: IMeetingAICompanionSmartSummaryHelper              [LEAF]
│   │   └─► Level 3: IMeetingAICompanionQueryHelper                     [LEAF]
│   │
│   │   ══════════════════════════════════════════════════════════════
│   │   WINDOWS-ONLY CONTROLLERS (#if defined(WIN32))
│   │   ══════════════════════════════════════════════════════════════
│   │
│   ├─► Level 2: IMeetingUIController                                   [LEAF - Windows]
│   │
│   ├─► Level 2: IAnnotationController
│   │   └─► Level 3: ICustomizedAnnotationController                    [LEAF - Custom UI]
│   │
│   ├─► Level 2: IMeetingRemoteController                               [LEAF - Windows]
│   ├─► Level 2: IMeetingH323Helper                                     [LEAF - Windows]
│   ├─► Level 2: IMeetingPhoneHelper                                    [LEAF - Windows]
│   ├─► Level 2: IMeetingLiveStreamController                           [LEAF - Windows]
│   ├─► Level 2: IClosedCaptionController                               [LEAF - Windows]
│   ├─► Level 2: IZoomRealNameAuthMeetingHelper                         [LEAF - Windows]
│   ├─► Level 2: IMeetingQAController                                   [LEAF - Windows]
│   ├─► Level 2: IMeetingInterpretationController                       [LEAF - Windows]
│   ├─► Level 2: IMeetingSignInterpretationController                   [LEAF - Windows]
│   ├─► Level 2: IEmojiReactionController                               [LEAF - Windows]
│   ├─► Level 2: IMeetingAANController                                  [LEAF - Windows]
│   ├─► Level 2: IMeetingWhiteboardController                           [LEAF - Windows]
│   ├─► Level 2: IMeetingDocsController                                 [LEAF - Windows]
│   ├─► Level 2: IMeetingPollingController                              [LEAF - Windows]
│   ├─► Level 2: IMeetingRemoteSupportController                        [LEAF - Windows]
│   ├─► Level 2: IMeetingIndicatorController                            [LEAF - Windows]
│   ├─► Level 2: IMeetingProductionStudioController                     [LEAF - Windows]
│   │
│   └─► Level 2: ICustomImmersiveController
│       └─► Level 3: ICustomImmersivePreLayoutHelper                    [LEAF]
│
├─► Level 1: ISettingService
│   ├─► Level 2: IGeneralSettingContext                                 [LEAF]
│   ├─► Level 2: IAudioSettingContext                                   [LEAF]
│   ├─► Level 2: IVideoSettingContext                                   [LEAF]
│   ├─► Level 2: IRecordingSettingContext                               [LEAF]
│   ├─► Level 2: IShareSettingContext                                   [LEAF]
│   ├─► Level 2: IStatisticSettingContext                               [LEAF]
│   └─► Level 2: IWallpaperSettingContext                               [LEAF]
│
├─► Level 1: INetworkConnectionHelper                                   [LEAF]
│
└─► Level 1: ICustomizedUIMgr (Custom UI Mode)
    ├─► Level 2: ICustomizedVideoContainer (factory-created)
    ├─► Level 2: ICustomizedShareRender (factory-created)
    └─► Level 2: ICustomizedImmersiveContainer (factory-created)
```

---

## Controller Reference by Feature Domain

### Cross-Platform Controllers

| Controller | Getter Method | Purpose |
|------------|---------------|---------|
| `IMeetingVideoController` | `GetMeetingVideoController()` | Video on/off, spotlight, pin, virtual background |
| `IMeetingAudioController` | `GetMeetingAudioController()` | Mute/unmute, VoIP, audio device selection |
| `IMeetingShareController` | `GetMeetingShareController()` | Screen/app sharing, share settings |
| `IMeetingChatController` | `GetMeetingChatController()` | In-meeting chat, file transfer |
| `IMeetingRecordingController` | `GetMeetingRecordingController()` | Local/cloud recording control |
| `IMeetingParticipantsController` | `GetMeetingParticipantsController()` | User list, rename, remove, roles |
| `IMeetingWaitingRoomController` | `GetMeetingWaitingRoomController()` | Admit/deny users, waiting room settings |
| `IMeetingWebinarController` | `GetMeetingWebinarController()` | Webinar-specific controls, panelists |
| `IMeetingRawArchivingController` | `GetMeetingRawArchivingController()` | Raw archiving for compliance |
| `IMeetingReminderController` | `GetMeetingReminderController()` | Meeting reminders and notifications |
| `IMeetingEncryptionController` | `GetInMeetingEncryptionController()` | E2E encryption status |
| `IMeetingConfiguration` | `GetMeetingConfiguration()` | Meeting behavior configuration |
| `IMeetingBOController` | `GetMeetingBOController()` | Breakout rooms (has Level 3 helpers) |
| `IMeetingAICompanionController` | `GetMeetingAICompanionController()` | AI Companion features (has Level 3 helpers) |
| `IListFactory` | `GetListFactory()` | Factory for creating SDK list objects |

### Windows-Only Controllers

| Controller | Getter Method | Purpose |
|------------|---------------|---------|
| `IMeetingUIController` | `GetUIController()` | SDK UI window control, toolbar customization |
| `IAnnotationController` | `GetAnnotationController()` | Drawing/annotation on shared content |
| `IMeetingRemoteController` | `GetMeetingRemoteController()` | Remote control of shared content |
| `IMeetingH323Helper` | `GetH323Helper()` | H.323/SIP room system integration |
| `IMeetingPhoneHelper` | `GetMeetingPhoneHelper()` | PSTN dial-in/dial-out |
| `IMeetingLiveStreamController` | `GetMeetingLiveStreamController()` | YouTube/Facebook/custom RTMP streaming |
| `IClosedCaptionController` | `GetMeetingClosedCaptionController()` | Closed captions, live transcription |
| `IZoomRealNameAuthMeetingHelper` | `GetMeetingRealNameAuthController()` | China real-name authentication |
| `IMeetingQAController` | `GetMeetingQAController()` | Webinar Q&A feature |
| `IMeetingInterpretationController` | `GetMeetingInterpretationController()` | Language interpretation channels |
| `IMeetingSignInterpretationController` | `GetMeetingSignInterpretationController()` | Sign language interpretation |
| `IEmojiReactionController` | `GetMeetingEmojiReactionController()` | Emoji reactions (👍 🎉 etc.) |
| `IMeetingAANController` | `GetMeetingAANController()` | Advanced Audio Networking |
| `ICustomImmersiveController` | `GetMeetingImmersiveController()` | Immersive view/scenes (has Level 3 helper) |
| `IMeetingWhiteboardController` | `GetMeetingWhiteboardController()` | Collaborative whiteboard |
| `IMeetingDocsController` | `GetMeetingDocsController()` | In-meeting document sharing |
| `IMeetingPollingController` | `GetMeetingPollingController()` | Polls and quizzes |
| `IMeetingRemoteSupportController` | `GetMeetingRemoteSupportController()` | Remote support features |
| `IMeetingIndicatorController` | `GetMeetingIndicatorController()` | UI indicators and status |
| `IMeetingProductionStudioController` | `GetMeetingProductionStudioController()` | Production studio/broadcast features |

---

## When to Use Each Level

| Level | When | Example |
|-------|------|---------|
| **Level 1** | App startup, before joining | `CreateMeetingService()`, `CreateAuthService()` |
| **Level 2** | After joining meeting, for features | `meetingService->GetMeetingAudioController()` |
| **Level 3** | For specialized sub-features | `boController->GetBOCreatorHelper()` |
| **Level 4** | For batch/bulk operations | `boCreator->GetBatchCreateBOHelper()` |

---

## How to Use (Universal Pattern)

Every feature follows the **same 3-step pattern**:

```cpp
// Step 1: Navigate to the controller (singleton)
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();

// Step 2: Register event listener (observer pattern)
audioCtrl->SetEvent(new MyAudioEventListener());

// Step 3: Call methods
audioCtrl->MuteAudio(userId, true);
```

---

## Examples by Depth

### Level 2 - Basic Feature (Audio)

```cpp
// Get controller
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();

// Use it
audioCtrl->JoinVoip();
audioCtrl->MuteAudio(0, true);  // 0 = self
```

### Level 3 - Sub-Feature (Breakout Room Creation)

```cpp
// Navigate: Level 1 → Level 2 → Level 3
IMeetingBOController* boCtrl = meetingService->GetMeetingBOController();
IBOCreator* creator = boCtrl->GetBOCreatorHelper();

// Use it
creator->CreateBreakoutRoom(L"Room 1");
creator->AssignUserToBO(strUserID, strBOID);
```

### Level 4 - Batch Operations (Bulk Room Creation)

```cpp
// Navigate: Level 1 → Level 2 → Level 3 → Level 4
IMeetingBOController* boCtrl = meetingService->GetMeetingBOController();
IBOCreator* creator = boCtrl->GetBOCreatorHelper();
IBatchCreateBOHelper* batch = creator->GetBatchCreateBOHelper();

// Use it (transaction pattern)
batch->CreateBOTransactionBegin();
batch->AddNewBoToList(L"Room 1");
batch->AddNewBoToList(L"Room 2");
batch->AddNewBoToList(L"Room 3");
batch->CreateBoTransactionCommit();  // Creates all 3 at once
```

---

## Why the Hierarchy Exists

| Depth | Design Purpose |
|-------|----------------|
| **Level 1** (Services) | Lifecycle management - created once, destroyed at cleanup |
| **Level 2** (Controllers) | Feature grouping - one controller per domain |
| **Level 3** (Helpers) | Role-based access - different helpers for host vs attendee |
| **Level 4** (Batch) | Performance optimization - bulk ops instead of N individual calls |

---

## Practical Rules

### 1. Don't Cache Too Early

Controllers return `nullptr` if not in meeting:

```cpp
// WRONG - cached before meeting joined
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();
meetingService->Join(joinParam);
audioCtrl->MuteAudio(0, true);  // audioCtrl might be nullptr!

// RIGHT - get after joining
meetingService->Join(joinParam);
// ... wait for MEETING_STATUS_INMEETING callback ...
IMeetingAudioController* audioCtrl = meetingService->GetMeetingAudioController();
if (audioCtrl) {
    audioCtrl->MuteAudio(0, true);
}
```

### 2. Re-get After State Changes

After joining/leaving meeting, get controllers again - previous pointers may be invalid.

### 3. Check for nullptr

Some helpers only available for hosts:

```cpp
IBOCreator* creator = boCtrl->GetBOCreatorHelper();
if (creator) {
    // Only hosts get a valid creator
    creator->CreateBreakoutRoom(L"Room 1");
}
```

### 4. Batch When Possible

Level 4 helpers exist specifically for performance:

```cpp
// SLOW - 10 individual calls
for (int i = 0; i < 10; i++) {
    creator->CreateBreakoutRoom(roomNames[i]);
}

// FAST - 1 batch call
IBatchCreateBOHelper* batch = creator->GetBatchCreateBOHelper();
batch->CreateBOTransactionBegin();
for (int i = 0; i < 10; i++) {
    batch->AddNewBoToList(roomNames[i]);
}
batch->CreateBoTransactionCommit();
```

---

## Deepest Paths (Maximum Depth = 4)

| Path | Use Case |
|------|----------|
| `IMeetingService` → `IMeetingBOController` → `IBOCreator` → `IBatchCreateBOHelper` | Bulk breakout room creation |
| `IAuthService` → `INotificationServiceHelper` → `IPresenceHelper` → `IBatchRequestContactHelper` | Bulk contact operations |

---

## Quick Reference: Common Navigation Paths

### Core Meeting Features

| Feature | Navigation Path |
|---------|-----------------|
| Audio control | `IMeetingService` → `GetMeetingAudioController()` |
| Video control | `IMeetingService` → `GetMeetingVideoController()` |
| Screen sharing | `IMeetingService` → `GetMeetingShareController()` |
| Chat | `IMeetingService` → `GetMeetingChatController()` |
| Recording | `IMeetingService` → `GetMeetingRecordingController()` |
| Participants | `IMeetingService` → `GetMeetingParticipantsController()` |
| Waiting room | `IMeetingService` → `GetMeetingWaitingRoomController()` |
| Breakout rooms | `IMeetingService` → `GetMeetingBOController()` → `GetBO*Helper()` |
| AI Companion | `IMeetingService` → `GetMeetingAICompanionController()` |
| AI Smart Summary | `IMeetingService` → `GetMeetingAICompanionController()` → `GetMeetingAICompanionSmartSummaryHelper()` |
| AI Query | `IMeetingService` → `GetMeetingAICompanionController()` → `GetMeetingAICompanionQueryHelper()` |
| Remote camera | `IMeetingService` → `GetMeetingVideoController()` → `GetMeetingCameraHelper()` |
| Video order (gallery) | `IMeetingService` → `GetMeetingVideoController()` → `GetSetVideoOrderHelper()` |
| Local camera device | `IMeetingService` → `GetMeetingVideoController()` → `GetMyCameraController()` |

### Windows-Only Features

| Feature | Navigation Path |
|---------|-----------------|
| Live streaming | `IMeetingService` → `GetMeetingLiveStreamController()` |
| Q&A (webinars) | `IMeetingService` → `GetMeetingQAController()` |
| Interpretation | `IMeetingService` → `GetMeetingInterpretationController()` |
| Sign language | `IMeetingService` → `GetMeetingSignInterpretationController()` |
| Closed captions | `IMeetingService` → `GetMeetingClosedCaptionController()` |
| Annotations | `IMeetingService` → `GetAnnotationController()` |
| Annotations (Custom UI) | `IMeetingService` → `GetAnnotationController()` → `GetCustomizedAnnotationController()` |
| Emoji reactions | `IMeetingService` → `GetMeetingEmojiReactionController()` |
| Polling | `IMeetingService` → `GetMeetingPollingController()` |
| Whiteboard | `IMeetingService` → `GetMeetingWhiteboardController()` |
| Docs | `IMeetingService` → `GetMeetingDocsController()` |
| H.323/SIP | `IMeetingService` → `GetH323Helper()` |
| Phone dial-in/out | `IMeetingService` → `GetMeetingPhoneHelper()` |
| Remote control | `IMeetingService` → `GetMeetingRemoteController()` |
| Immersive view | `IMeetingService` → `GetMeetingImmersiveController()` |
| UI control | `IMeetingService` → `GetUIController()` |

### Settings & Pre-Meeting

| Feature | Navigation Path |
|---------|-----------------|
| Audio settings | `ISettingService` → `GetAudioSettings()` |
| Video settings | `ISettingService` → `GetVideoSettings()` |
| Recording settings | `ISettingService` → `GetRecordingSettings()` |
| Share settings | `ISettingService` → `GetShareSettings()` |
| Presence/contacts | `IAuthService` → `GetNotificationServiceHelper()` → `GetPresenceHelper()` |

---

## Deprecated Controllers & Helpers

| Deprecated | Replacement |
|------------|-------------|
| `IMeetingSmartSummaryController` | Use `IMeetingAICompanionController` |
| `IMeetingSmartSummaryHelper` | Use `IMeetingAICompanionSmartSummaryHelper` via `GetMeetingAICompanionSmartSummaryHelper()` |

---

## Platform Availability Summary

| Category | Count | Platform |
|----------|-------|----------|
| Cross-platform controllers | 15 | Windows, macOS, Linux |
| Windows-only controllers | 20 | Windows only (`#if defined(WIN32)`) |
| **Total** | **35** | — |

> **Note**: When developing cross-platform apps, use `#if defined(WIN32)` guards around Windows-only controller access.

---

## Related Documentation

- [SDK Architecture Pattern](sdk-architecture-pattern.md) - The universal 3-step pattern
- [Custom UI Architecture](custom-ui-architecture.md) - Custom UI specific hierarchy
- [Breakout Rooms Example](../examples/breakout-rooms.md) - Level 3 helpers in action
- [Chat Example](../examples/chat.md) - IMeetingChatController usage
- [Captions/Transcription Example](../examples/captions-transcription.md) - IClosedCaptionController usage
- [Local Recording Example](../examples/local-recording.md) - IMeetingRecordingController usage
- [Video Advanced Example](../examples/video-advanced.md) - Camera control, video order (Level 3 helpers)
- [AI Companion Example](../examples/ai-companion.md) - Smart Summary, AI Query (Level 3 helpers)

---

**TL;DR**: The hierarchy is your navigation map. Start at a service, drill down to the feature you need, then call methods. Deeper levels = more specialized operations. Windows has 20 additional controllers not available on other platforms.

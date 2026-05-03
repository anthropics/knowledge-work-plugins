# SDK Architecture Pattern

Flutter wrapper exposes helper-centric APIs and event constants.

## Layers

- Core platform wrapper (`ZoomVideoSdk`, platform channel).
- Session object and user/session state models.
- Domain helpers: audio/video/chat/share/recording/live transcription/phone/subsession.
- Event channel via `ZoomVideoSdkEventListener` and `EventType` constants.

## Pattern

1. Resolve helper/session object.
2. Invoke async method.
3. Process event callback and state transitions.
4. Update UI/store from event payload.

## Design guidance

- Keep event-to-state mapping centralized.
- Treat SDK enums/errors as versioned contracts.
- Isolate helper calls behind adapter methods for easier upgrades.

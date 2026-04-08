# Lifecycle Workflow

Recommended execution flow for Flutter Video SDK integrations:

1. Initialize SDK with `InitConfig`.
2. Register event listener(s) and app state handlers.
3. Join session with signed token.
4. Start audio/video/share flows through helpers.
5. Handle participant/session events and quality telemetry.
6. Leave session and run cleanup.

## Sequence Diagram

```text
Flutter App
  -> initSdk(initConfig)
  -> register ZoomVideoSdkEventListener
  -> joinSession(joinConfig)
  -> use audio/video/share/chat helpers
  -> handle EventType callbacks
  -> leaveSession
  -> cleanup
```

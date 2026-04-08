# Android Architecture Concept

```mermaid
flowchart LR
  UI[Android UI Layer] --> VM[Session ViewModel / Controller]
  VM --> SDK[Zoom Video SDK Android]
  VM --> API[Token API]
  API --> Signer[Server-side JWT Signer]
  Signer --> Market[Video SDK App Credentials]
  SDK --> Events[Participant/Media Events]
  Events --> UI
```

## Design guidance

- Keep token creation strictly backend-side.
- Keep SDK calls in a session controller or ViewModel boundary.
- Drive UI from SDK event streams to avoid stale participant state.
- Treat join/start-media/leave as explicit state transitions.

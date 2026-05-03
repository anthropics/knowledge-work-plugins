# Unity Architecture Concept

```mermaid
flowchart LR
  Scene[Unity Scene + UI] --> SessionMgr[Session Manager Script]
  SessionMgr --> Wrapper[Zoom Video SDK Unity Wrapper]
  SessionMgr --> TokenAPI[Token API]
  TokenAPI --> Signer[Server JWT Signer]
  Wrapper --> Events[SDK Event Callbacks]
  Events --> SessionMgr
  SessionMgr --> Scene
```

## Design guidance

- Keep wrapper calls behind one Session Manager abstraction.
- Convert SDK callbacks into explicit Unity state updates.
- Avoid direct credential logic in Unity client.

# iOS Architecture Concept

```mermaid
flowchart LR
  UI[SwiftUI/UIKit] --> Store[Session Store / Coordinator]
  Store --> SDK[Zoom Video SDK iOS]
  Store --> TokenAPI[Token API]
  TokenAPI --> Signer[Server JWT Signer]
  SDK --> Delegates[SDK Delegate Callbacks]
  Delegates --> Store
```

## Design guidance

- Use a coordinator/store layer to isolate SDK-specific logic.
- Keep join/start/leave actions explicit and serial.
- Render participant tiles from delegate-driven state only.

# macOS Architecture Concept

```mermaid
flowchart LR
  UI[AppKit/SwiftUI Views] --> Coord[Session Coordinator]
  Coord --> SDK[Zoom Video SDK macOS]
  Coord --> TokenAPI[Token API]
  SDK --> Events[Delegate/Event Stream]
  Events --> Coord
  Coord --> Render[View/Window Render State]
```

## Design guidance

- Centralize SDK access in a coordinator/service boundary.
- Separate render state from transport/session state.
- Treat join, share, and leave as explicit transitions.

# macOS Lifecycle Workflow

```mermaid
flowchart TD
  A[Fetch token] --> B[Initialize SDK]
  B --> C[Attach delegates]
  C --> D[Join session]
  D --> E[Start camera/mic/share]
  E --> F[Process participant and media events]
  F --> G[Leave session]
  G --> H[Cleanup windows and SDK resources]
```

## Operational sequence

1. Request token from backend.
2. Initialize SDK and delegate/event bridge.
3. Join session with user identity.
4. Start media after join confirmation.
5. Handle remote participant/media updates and view lifecycle.
6. Stop media and release resources on leave.

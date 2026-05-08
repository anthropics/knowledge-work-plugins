# Lifecycle Workflow

Recommended flow for React Native Video SDK integrations:

1. Initialize provider/SDK config.
2. Register SDK event listeners.
3. Join session using backend-signed JWT token.
4. Drive media/features via helpers.
5. React to event callbacks for UI/session state.
6. Leave session and cleanup SDK resources.

## Sequence

```text
React Native app
  -> initSdk
  -> addListener(EventType...)
  -> joinSession(joinConfig)
  -> helper operations
  -> leaveSession
  -> cleanup
```

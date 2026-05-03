# SDK Architecture Pattern

The wrapper uses provider/context + helper objects.

## Structure

- `ZoomVideoSdkProvider` bootstraps SDK lifecycle.
- `useZoom()` / handler exposes helper modules.
- Helpers include session, user, audio, video, share, chat, recording, transcription, phone, CRC, annotation, and subsession.
- `useSdkEventListener` + `EventType` power event-driven state updates.

## Pattern

1. Resolve helper from context.
2. Call helper API.
3. Handle event callback.
4. Update UI/store.

## Guidance

- Centralize event handling logic.
- Treat helper return codes as versioned contracts.
- Guard advanced helpers behind capability checks where possible.

# Session Join Pattern

## Flow

1. Backend signs Video SDK JWT.
2. App builds join config.
3. App calls `joinSession`.
4. UI state is driven by event callbacks.

## Minimal shape

```ts
await zoom.joinSession({
  sessionName: 'my-session',
  token: '<VIDEO_SDK_JWT>',
  userName: 'Mobile User',
  audioOptions: { connect: true, mute: false },
  videoOptions: { localVideoOn: true },
  sessionIdleTimeoutMins: 40,
});
```

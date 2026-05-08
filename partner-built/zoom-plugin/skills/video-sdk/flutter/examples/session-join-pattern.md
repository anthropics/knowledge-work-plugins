# Session Join Pattern

## Flow

1. Backend signs Video SDK session token.
2. App creates `JoinSessionConfig`.
3. App calls `joinSession`.
4. UI reacts to session/user event callbacks.

## Minimal shape

```dart
final joinConfig = JoinSessionConfig(
  sessionName: 'my-session',
  token: '<VIDEO_SDK_JWT>',
  userName: 'Mobile User',
  audioOptions: {'connect': true, 'mute': true},
  videoOptions: {'localVideoOn': true},
);
await zoom.joinSession(joinConfig);
```

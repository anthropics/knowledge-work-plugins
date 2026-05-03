# React Native Meeting Embed

Use this flow when you need Zoom meetings inside a mobile app built with React Native.

## When to Use

- iOS/Android app already uses React Native
- You need Zoom meeting join/start inside app navigation
- You want Zoom Meeting SDK UI from React Native wrapper, not a custom video stack

## Skill Chain

1. **[meeting-sdk/react-native](../../meeting-sdk/react-native/SKILL.md)** for wrapper APIs and platform setup
2. **[zoom-oauth](../../oauth/SKILL.md)** for backend token handling (SDK JWT and ZAK)

## Typical Flow

1. Backend issues SDK JWT for mobile client.
2. App initializes SDK with `initSDK`.
3. App joins by `joinMeeting` (attendee) or starts by `startMeeting` (host + ZAK).
4. App handles meeting lifecycle and calls `cleanup` during teardown.

## References

- [Meeting SDK React Native Skill](../../meeting-sdk/react-native/SKILL.md)
- [Auth and Token Model](../../meeting-sdk/react-native/concepts/auth-and-token-model.md)
- [Join Meeting Pattern](../../meeting-sdk/react-native/examples/join-meeting-pattern.md)

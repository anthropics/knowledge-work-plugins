# React Native Video Sessions

Use this flow for custom mobile video session products in React Native.

## When to Use

- You need full custom UX (not Zoom Meeting UI).
- You are building iOS/Android apps using `@zoom/react-native-videosdk`.
- You need helper-based features such as chat/share/recording/transcription.

## Skill Chain

1. [video-sdk/react-native](../../video-sdk/react-native/SKILL.md)
2. [zoom-oauth](../../oauth/SKILL.md)

## Typical Flow

1. Backend signs short-lived Video SDK JWT.
2. App initializes SDK provider and listeners.
3. App joins session with tokenized config.
4. App drives helper APIs and event-based UI state.
5. App leaves session and cleans up resources.

## References

- [React Native Video SDK Skill](../../video-sdk/react-native/SKILL.md)
- [Lifecycle Workflow](../../video-sdk/react-native/concepts/lifecycle-workflow.md)
- [Session Join Pattern](../../video-sdk/react-native/examples/session-join-pattern.md)

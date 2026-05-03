# Setup Guide

## 1. Install package

```bash
npm install @zoom/react-native-videosdk
```

## 2. Wrap app with provider

```tsx
<ZoomVideoSdkProvider
  config={{
    domain: 'zoom.us',
    enableLog: true,
    appGroupId: '<ios-app-group-if-needed>',
  }}
>
  <App />
</ZoomVideoSdkProvider>
```

## 3. Platform baseline

- Configure Android/iOS native prerequisites from package docs.
- Ensure React Native/toolchain compatibility with wrapper version.
- Implement backend JWT signing endpoint before session join.

## 4. Android build stability on Windows

- Prefer a short workspace path for Android builds (example: `C:\temp\rn-video-sdk-example`).
- Deep nested paths can trigger native CMake/Gradle instability (for example reanimated build trees and repeated `build.ninja` regeneration).

## 5. Android SDK wiring for CLI runs

- Ensure `android/local.properties` points to your SDK dir:

```properties
sdk.dir=C\:\\Users\\<user>\\AppData\\Local\\Android\\Sdk
```

- For shell-driven runs, export/set Android env vars before `react-native run-android`:
  - `ANDROID_HOME`
  - `ANDROID_SDK_ROOT`
  - `PATH` includes `platform-tools`

## 6. Dependency pinning for copied sample projects

- If project was copied from SDK sources, do not keep local relative dependency (`"@zoom/react-native-videosdk": "../"`) unless parent package exists at that exact location.
- Pin/install a concrete version instead (example `@zoom/react-native-videosdk@2.4.5`) to avoid Metro resolution failures.

## 7. Security baseline

- Keep Video SDK secret out of mobile app.
- Use short-lived JWTs per session/user context.
- Validate incoming session inputs server-side.

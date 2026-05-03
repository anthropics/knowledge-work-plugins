# Common Issues

## Session join fails

- Validate JWT token format/expiry and claims.
- Ensure SDK init/provider setup completed before join.
- Validate join config fields and naming (`userName` vs `username` mismatch by version).

## Event callbacks appear inconsistent

- Register listeners before join where possible.
- Avoid duplicate listeners in multiple screens.
- Ensure cleanup/unsubscribe on unmount.

## Helper methods return errors unexpectedly

- Confirm in-session preconditions for helper calls.
- Re-check permission state on mobile OS.
- Map and log error enums for diagnosis.

## Platform build/runtime issues

- Verify React Native + package version compatibility.
- Reinstall pods/gradle dependencies after package changes.
- Validate native bridge files and linked binaries.

## Android native build fails on Windows deep paths

Symptom:

- CMake/Gradle failures in native modules (for example repeated `build.ninja` dirty/regeneration failures).

Fix:

- Move project to a short path (example `C:\temp\rn-video-sdk-example`).
- Clean Android artifacts and rebuild from the shorter path.

## Metro error: cannot resolve `@zoom/react-native-videosdk`

Symptom:

- Red screen in `src/App.tsx` or startup bundle: module cannot be found.

Root cause:

- Dependency points to a relative local link (`../`) that does not resolve in copied project layout.

Fix:

- Pin/install published package version (example `@zoom/react-native-videosdk@2.4.5`).
- Reinstall node modules and restart Metro.

## Android SDK/adb not detected by RN CLI

- Add `android/local.properties` with valid `sdk.dir`.
- Ensure `ANDROID_HOME`, `ANDROID_SDK_ROOT`, and PATH (`platform-tools`) are set in the shell running `react-native run-android`.

# Common Issues

## Join fails or stalls

- Validate JWT token generation and expiry.
- Ensure `sessionName` and join config fields are valid.
- Verify SDK init completed before `joinSession`.

## SDK initialization fails

- Confirm `domain: "zoom.us"` is used in `InitConfig`.
- Request runtime permissions before init/join (camera, microphone, Bluetooth connect on newer Android).
- Catch `PlatformException` from `initSdk` and log `code`, `message`, and `details`.
- If UI shows contradictory status (for example success text treated as failure), normalize success checks against both SDK constants and returned success strings.

## Event callbacks not handled consistently

- Register event listener before critical actions.
- Avoid scattered listeners in multiple widgets.
- Centralize callback dispatch into one state path.

## Media controls appear inconsistent

- Check permission states (camera/mic/storage where needed).
- Re-check helper availability after session reconnect.
- Use event-driven status updates, not optimistic UI assumptions.

## Platform-specific issues

- Confirm iOS/Android native setup and package versions match.
- Rebuild clean when plugin/native versions change.

## Android compile error: `ZoomVideoSDKDelegate not found`

Symptom:

- Build fails in generated plugin registration with missing `us.zoom.sdk.ZoomVideoSDKDelegate`.

Fix:

- Add Zoom Video SDK Android dependencies in the host app module (`android/app/build.gradle.kts` or Gradle Groovy equivalent), even when using local plugin path dependency.
- Rebuild with `flutter clean`, `flutter pub get`, and `flutter build apk --debug`.

## ADB connection issues (physical device)

- If `adb devices` is empty, verify USB/Wireless debugging is enabled and phone trusts host.
- For wireless debugging, complete both steps: `adb pair` then `adb connect`.
- If connection drops, rerun `adb connect <ip:connect-port>` and verify with `adb devices -l`.

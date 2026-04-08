# Setup Guide

## 0. Flutter and Android tooling baseline (Windows)

Install and verify Flutter before SDK wiring.

```bash
# install location example
git clone https://github.com/flutter/flutter.git -b stable --depth 1 C:\users\dreamtcs\tools\flutter

# verify
C:\users\dreamtcs\tools\flutter\bin\flutter.bat --version
C:\users\dreamtcs\tools\flutter\bin\flutter.bat doctor -v
```

If Flutter is not on PATH in your shell, use the full `flutter.bat` path for all commands.

## 1. Install package

```yaml
dependencies:
  flutter_zoom_videosdk: ^<version>
```

```bash
flutter pub get
```

## 2. Initialize SDK

```dart
final zoom = ZoomVideoSdk();
await zoom.initSdk(InitConfig(
  domain: 'zoom.us',
  enableLog: true,
));
```

If init fails without a clear error string, wrap `initSdk` with `PlatformException` handling and surface `code/message/details` in UI logs.

## 3. Core prerequisites

- Flutter and Dart toolchain compatible with wrapper version.
- iOS/Android native setup aligned with package expectations.
- Backend service for Video SDK JWT generation.

## 4. Android host app requirements

- Set `minSdk` to at least `28` in the app module.
- Add runtime permissions for camera and mic (plus Bluetooth connect where applicable).
- If Java compile fails with `ZoomVideoSDKDelegate not found`, add the Zoom Android artifacts in the app module dependencies:

```kotlin
dependencies {
  implementation("us.zoom.videosdk:zoomvideosdk-core:2.3.10")
  implementation("us.zoom.videosdk:zoomvideosdk-videoeffects:2.3.10")
  implementation("us.zoom.videosdk:zoomvideosdk-annotation:2.3.10")
  implementation("us.zoom.videosdk:zoomvideosdk-whiteboard:2.3.10")
  implementation("us.zoom.videosdk:zoomvideosdk-broadcast-streaming:2.3.10")
}
```

## 5. ADB device setup (physical Android recommended)

When emulator startup is unstable, run on a real phone:

```bash
# pairing (from Wireless debugging)
adb pair <ip:pair-port> <pair-code>

# connect (from mDNS connect port)
adb connect <ip:connect-port>
adb devices -l
```

Then run the app:

```bash
flutter run -d <device-id> --debug --no-resident
```

## 6. Security baseline

- Never embed SDK secret in app bundle.
- Issue short-lived session tokens server-side.
- Validate all session join parameters before SDK call.

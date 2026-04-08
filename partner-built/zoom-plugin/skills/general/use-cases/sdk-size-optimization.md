# SDK Size Optimization

Reduce mobile app binary size when integrating Zoom Meeting SDK or Video SDK on iOS and Android.

## Overview

Zoom SDKs add significant size to mobile apps. This guide covers **Zoom-recommended techniques** from the official developer forum and blog to minimize the impact on your app's download size.

## Skills Needed

- **zoom-meeting-sdk** (iOS, Android)
- **zoom-video-sdk** (iOS, Android)

## SDK Size Reference

### Meeting SDK

| Platform | Configuration | Size |
|----------|---------------|------|
| iOS | Universal (all architectures) | ~107 MB |
| Android | arm64-v8a + armeabi-v7a | ~97-108 MB |
| Android | arm64-v8a only | ~71 MB |
| Android | armeabi-v7a only | ~47 MB |

### Video SDK

| Platform | Size |
|----------|------|
| iOS/Android | ~75 MB |

---

## Android: Zoom-Recommended Methods

### 1. ABI Filtering (Official Recommendation)

This is the **primary method recommended by Zoom** to reduce APK size. Filter to only the CPU architectures you need.

```gradle
// build.gradle (app module)
android {
    defaultConfig {
        ndk {
            // Option 1: Modern devices only (smallest size)
            abiFilters 'arm64-v8a'
            
            // Option 2: Broader device support
            // abiFilters 'arm64-v8a', 'armeabi-v7a'
        }
    }
}
```

**Size Impact (from Zoom Dev Forum):**

| Configuration | APK Size |
|---------------|----------|
| No Zoom SDK | ~11 MB |
| arm64-v8a + armeabi-v7a | ~97 MB |
| **arm64-v8a only** | **~71 MB** |
| armeabi-v7a only | ~47 MB |

**Note:** Most modern Android devices (2017+) use `arm64-v8a`. Only include `armeabi-v7a` if you need to support older 32-bit devices.

### 2. Android App Bundle (AAB)

Use Android App Bundles for Play Store distribution. Google Play automatically generates device-specific APKs:

```gradle
android {
    bundle {
        abi {
            enableSplit = true
        }
    }
}
```

Users only download the architecture matching their device, reducing download size.

---

## iOS: Zoom-Recommended Methods

### App Store App Thinning (Automatic)

iOS App Store automatically applies App Thinning:

- Delivers only the architecture slice needed for each device
- No manual configuration required
- Happens automatically when distributing through App Store

**Verify in Xcode:**
Window → Organizer → Archives → App Thinning Report

---

## What Does NOT Work

Zoom has confirmed the following approaches are **NOT supported**:

### No Feature/Module Exclusion

From Zoom Developer Forum (August 2024):
> "There are **no new updates regarding reducing size of SDK**"

- Cannot remove virtual background module
- Cannot remove screen sharing module  
- Cannot exclude any bundled features
- All features are compiled together

### No Dynamic Feature Module Support

Zoom has confirmed they do **NOT support** Android Dynamic Feature Modules:

- Resource linking errors occur
- `Resources$NotFoundException` at runtime
- Community workarounds are unsupported and may break

### ProGuard/R8 Not Fully Supported

**Warning:** ProGuard/R8 causes crashes with Zoom SDK, even with Zoom's provided rules. Users report runtime crashes. Use at your own risk.

### Bitcode Not Supported (iOS)

Zoom SDK does **NOT** support iOS Bitcode due to internal dependencies. However, Bitcode is no longer required by Apple (Xcode 15+).

---

## Alternative Approaches

If SDK size is prohibitive for your use case:

### 1. Web SDK in WebView

Load the Web SDK in a native WebView instead of using the native SDK:

```swift
// iOS
let webView = WKWebView(frame: view.bounds)
webView.load(URLRequest(url: URL(string: "https://your-app.com/zoom-meeting")!))
```

```kotlin
// Android
webView.loadUrl("https://your-app.com/zoom-meeting")
```

**Trade-offs:**
- No native SDK size impact
- Reduced native feature access
- Requires WebView setup and web hosting

### 2. Deep Link to Zoom App

Open meetings in the native Zoom app instead of embedding:

```swift
// iOS
if let url = URL(string: "zoomus://zoom.us/join?confno=\(meetingNumber)") {
    UIApplication.shared.open(url)
}
```

```kotlin
// Android
val intent = Intent(Intent.ACTION_VIEW, 
    Uri.parse("zoomus://zoom.us/join?confno=$meetingNumber"))
startActivity(intent)
```

**Trade-offs:**
- Zero SDK size impact
- Requires Zoom app to be installed
- Less integrated user experience

---

## Summary

| Platform | Recommended Method | Expected Savings |
|----------|-------------------|------------------|
| **Android** | `abiFilters 'arm64-v8a'` | ~26 MB |
| **Android** | App Bundle (AAB) | Automatic per-device |
| **iOS** | App Thinning (automatic) | Automatic per-device |

**Key Limitation:** Zoom does not currently offer modular SDK downloads or feature exclusion. The SDK includes all features bundled together.

---

## Resources

- **Zoom Blog - Reduce APK Size**: https://developers.zoom.us/blog/reduce-apk-size-zoom-meeting-sdk-android/
- **Zoom Developer Forum - SDK Size Discussion**: https://devforum.zoom.us/t/reducing-the-size-of-the-zoom-meeting-sdk-ios-android/94302
- **Android ABI Management**: https://developer.android.com/ndk/guides/abis

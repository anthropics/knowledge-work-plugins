# Known Limitations & Quirks

Common gotchas and limitations developers encounter.

## Recording Limitations

### Minimum Recording Duration

**Recordings shorter than 3-5 seconds will NOT be saved.**

This applies to:
- Cloud recordings
- Local recordings via SDK

If you need to capture very short sessions, ensure the recording runs for at least 5 seconds.

## API Limitations

### Rate Limits

See [Rate Limits](../../rest-api/references/rate-limits.md) for detailed information.

Key points:
- Create/update meeting endpoints are **Heavy** (stricter limits)
- Response headers show remaining quota
- Implement exponential backoff for 429 errors

### Error Code 0

**The enum value 0 often represents SUCCESS, not failure.**

Always check the SDK enum values:
```cpp
// Example: Meeting SDK
SDKERR_SUCCESS = 0  // This is success!
SDKERR_UNKNOWN = 1  // This is an error
```

Don't assume 0 = error in your error handling.

## Video SDK Web Limitations

### Video Rendering Performance

**Use ONE rendering control for all videos, not one per participant.**

Multiple rendering controls severely degrade performance. See [Video SDK Web](../../video-sdk/web/references/web.md#video-rendering-best-practices).

### SharedArrayBuffer

Some features require SharedArrayBuffer headers:
```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

As of v1.11.2, this is elective for basic functionality.

## SDK Signature Limitations

### Minimum Token Validity

Zoom may require `exp - iat >= 2 hours`.

**Workaround:** Set `iat` in the past:
```javascript
const iat = Math.floor(Date.now() / 1000) - 7200; // 2 hours ago
const exp = Math.floor(Date.now() / 1000) + 10;   // 10 seconds from now
```

This gives you a short-lived token while satisfying the validity requirement.

## SDK Download

### Marketplace Sign-in Required

Meeting SDK and Video SDK (except Web npm packages) must be downloaded from [Marketplace](https://marketplace.zoom.us/) after signing in.

They are not available on public package managers for native platforms.

## Platform-Specific

### iOS

- Requires camera/microphone entitlements
- Background audio requires special configuration

### Android

- Requires runtime permissions for camera/mic
- ProGuard rules may be needed

### Linux

- Headless operation requires X virtual framebuffer (Xvfb) for some features
- Limited UI customization compared to other platforms

## Resources

- **Developer forum**: https://devforum.zoom.us/ (search for known issues)
- **Support**: https://devsupport.zoom.us/

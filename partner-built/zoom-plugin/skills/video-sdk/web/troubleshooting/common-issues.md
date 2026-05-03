# Common Issues and Solutions

## Quick Diagnostic Checklist

When something isn't working, run through this checklist:

1. **SDK Lifecycle**: Did you follow `createClient() → init() → join() → getMediaStream()`?
2. **Stream Timing**: Did you call `getMediaStream()` AFTER `join()` completed?
3. **Event Listeners**: Are you listening for `peer-video-state-change`?
4. **attachVideo vs renderVideo**: Are you using `attachVideo()` (not deprecated `renderVideo()`)?
5. **Browser Permissions**: Did the user grant camera/microphone access?
6. **Browser Compatibility**: Is the browser supported (Chrome 80+, Firefox 75+, Safari 14+)?

---

## Most Common Issues

### 1. getMediaStream() Returns undefined

**Symptom**: `client.getMediaStream()` returns `undefined` or `null`

**Cause**: Called before `join()` completed

**Solution**:
```javascript
// WRONG
const stream = client.getMediaStream();  // undefined!
await client.join(...);

// CORRECT
await client.join(...);
const stream = client.getMediaStream();  // Works!
```

### 2. Video Not Displaying

**Symptom**: Video element created but shows black/nothing

**Causes**:
1. Not listening to `peer-video-state-change` event
2. Using deprecated `renderVideo()` instead of `attachVideo()`
3. Not appending returned element to DOM

**Solution**:
```javascript
// 1. Use attachVideo(), not renderVideo()
const videoElement = await stream.attachVideo(userId, VideoQuality.Video_360P);

// 2. Append to DOM
container.appendChild(videoElement);

// 3. Listen for events
client.on('peer-video-state-change', async (payload) => {
  if (payload.action === 'Start') {
    const element = await stream.attachVideo(payload.userId, VideoQuality.Video_360P);
    container.appendChild(element);
  } else {
    await stream.detachVideo(payload.userId);
  }
});
```

### 3. Other Participants' Video Not Showing on Mid-Session Join

**Symptom**: Join mid-session, only your video shows, not others'

**Cause**: Existing participants' videos don't auto-render

**Solution**:
```javascript
// After joining, manually render existing participants
async function renderExistingParticipants() {
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const users = client.getAllUser();
  const currentUserId = client.getCurrentUserInfo().userId;
  
  for (const user of users) {
    if (user.bVideoOn && user.userId !== currentUserId) {
      const element = await stream.attachVideo(user.userId, VideoQuality.Video_360P);
      document.getElementById(`video-${user.userId}`).appendChild(element);
    }
  }
}
```

### 4. "ZoomVideo is not defined" or "WebVideoSDK is not defined"

**Symptom**: SDK global not available

**Causes**:
1. Network/ad blocker blocking `source.zoom.us` CDN
2. ES module loading before SDK script

**Solutions**:

**Solution 1 - Use a permitted fallback copy**:
```bash
# If your environment blocks `source.zoom.us`, you can mirror/self-host as a fallback
# only if permitted and you can keep versions in sync with the SDK you target.
curl "https://source.zoom.us/videosdk/zoom-video-2.3.12.min.js" -o public/js/zoom-video-sdk.min.js
```

```html
<script src="js/zoom-video-sdk.min.js"></script>
```

**Solution 2 - Wait for SDK to load**:
```javascript
function waitForSDK(timeout = 10000) {
  return new Promise((resolve, reject) => {
    if (typeof WebVideoSDK !== 'undefined') {
      resolve();
      return;
    }
    const start = Date.now();
    const check = setInterval(() => {
      if (typeof WebVideoSDK !== 'undefined') {
        clearInterval(check);
        resolve();
      } else if (Date.now() - start > timeout) {
        clearInterval(check);
        reject(new Error('SDK failed to load'));
      }
    }, 100);
  });
}

await waitForSDK();
const ZoomVideo = WebVideoSDK.default;
```

### 5. CDN exports WebVideoSDK.default, not ZoomVideo

**Symptom**: `ZoomVideo.createClient()` fails with CDN

**Cause**: CDN exports as `WebVideoSDK`, not `ZoomVideo`

**Solution**:
```javascript
// NPM
import ZoomVideo from '@zoom/videosdk';

// CDN
const ZoomVideo = WebVideoSDK.default;  // Note: .default!

const client = ZoomVideo.createClient();
```

### 6. Join Fails with "Invalid signature"

**Symptom**: `join()` throws error about invalid signature

**Causes**:
1. JWT expired (check `exp` claim)
2. JWT malformed
3. Wrong SDK key/secret
4. Topic doesn't match JWT `tpc` claim

**Solution**:
1. Generate JWT on server side
2. Check JWT expiration (typically 24h)
3. Verify topic matches JWT `tpc` value
4. Verify SDK key is correct

### 7. Camera/Microphone Permission Denied

**Symptom**: `startVideo()` or `startAudio()` fails

**Cause**: Browser permission denied

**Solution**:
```javascript
// Check permissions before starting
try {
  await stream.startVideo();
} catch (error) {
  if (error.type === 'INSUFFICIENT_PRIVILEGES') {
    // Permission denied - guide user
    alert('Please allow camera access in browser settings');
  }
}
```

### 8. HD Video Not Working

**Symptom**: Video quality stays at 360p despite `{ hd: true }`

**Causes**:
1. SharedArrayBuffer not available
2. Browser doesn't support HD
3. Network conditions

**Solution**:
```javascript
// Check HD support
if (stream.isSupportHDVideo()) {
  await stream.startVideo({ hd: true });
} else {
  console.warn('HD not supported');
  await stream.startVideo();
}

// Check SharedArrayBuffer
const sabAvailable = typeof SharedArrayBuffer === 'function';
if (!sabAvailable) {
  console.warn('SharedArrayBuffer not available - add COOP/COEP headers');
}
```

**Server Headers for SharedArrayBuffer**:
```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

### 9. Screen Share Element Type Error

**Symptom**: `startShareScreen()` fails or shows nothing

**Cause**: Using wrong element type (video vs canvas)

**Solution**:
```javascript
// Check which element type to use
if (stream.isStartShareScreenWithVideoElement()) {
  const video = document.getElementById('share-video');
  await stream.startShareScreen(video as unknown as HTMLCanvasElement);
} else {
  const canvas = document.getElementById('share-canvas');
  await stream.startShareScreen(canvas);
}
```

### 10. CORS Error to log-external-gateway.zoom.us

**Symptom**: Console shows CORS errors to Zoom telemetry

**Cause**: COOP/COEP headers blocking telemetry

**Impact**: None - harmless. SDK works fine.

**Solution**: Ignore these errors. They're telemetry-related and don't affect functionality.

---

## Error Types Reference

| Error Type | Meaning | Common Cause |
|------------|---------|--------------|
| `INVALID_OPERATION` | Duplicated operation | Calling same method twice |
| `INTERNAL_ERROR` | Service unavailable | Network issues |
| `OPERATION_TIMEOUT` | Timed out | Slow connection |
| `INSUFFICIENT_PRIVILEGES` | Need host/manager | Not authorized |
| `IMPROPER_MEETING_STATE` | Not in meeting | Wrong lifecycle stage |
| `INVALID_PARAMETERS` | Wrong params | Bad user ID, etc. |
| `OPERATION_LOCKED` | Property locked | Feature disabled |

---

## Browser-Specific Issues

### Safari

| Issue | Solution |
|-------|----------|
| Virtual background not supported | Use alternative (blur not available) |
| Screen sharing requires macOS 15+ | Use Chrome/Firefox |
| Some audio issues | Enable `patchJsMedia: true` |

### Firefox

| Issue | Solution |
|-------|----------|
| Virtual background requires 90+ | Update Firefox |
| Some WebRTC issues | Use Chrome if critical |

### Mobile Browsers

| Issue | Solution |
|-------|----------|
| Limited screen share | Use desktop for sharing |
| Performance issues | Lower video quality |
| Camera switching | Use `MobileVideoFacingMode` enum |

---

## Debugging Tips

### 1. Enable SDK Logging

```javascript
const loggerClient = client.getLoggerClient({
  level: 'debug'
});
```

### 2. Check Event Flow

```javascript
// Log all events
['connection-change', 'user-added', 'user-removed', 'peer-video-state-change'].forEach(event => {
  client.on(event, (payload) => {
    console.log(`Event: ${event}`, payload);
  });
});
```

### 3. Check Participant State

```javascript
const users = client.getAllUser();
console.table(users.map(u => ({
  userId: u.userId,
  name: u.displayName,
  videoOn: u.bVideoOn,
  muted: u.muted,
  audio: u.audio
})));
```

### 4. Check Stream State

```javascript
console.log('Active camera:', stream.getActiveCamera());
console.log('Active mic:', stream.getActiveMicrophone());
console.log('Capturing video:', stream.isCapturingVideo());
console.log('Audio muted:', stream.isAudioMuted());
console.log('HD supported:', stream.isSupportHDVideo());
console.log('Max quality:', stream.getVideoMaxQuality());
```

---

## Real-World Integration Pitfalls (Custom Waiting Room Flows)

These came up in production-style waiting-room to main-session transfers.

### A) Joined, but no audio/video works on Firefox

**Symptom**: Session joins, but media pipeline is flaky or blank.

**Cause**: CSP blocks WebAssembly execution used by `js_media.min.js`.

**Fix**: Ensure CSP `script-src` includes:

```text
'wasm-unsafe-eval' 'unsafe-eval'
```

Also keep required Zoom domains in `script-src` and allow `worker-src blob:`.

### B) Transfer works, but customer remote video never appears

**Symptom**: Customer reaches main session but does not see advisor video.

**Likely causes**:
1. Advisor is not publishing video (`bVideoOn` is false)
2. Event listener race during waiting->main rejoin
3. Attach attempted too early during stream readiness

**Fix pattern**:
- Bind listeners once and gate logic by current session mode.
- On main join, do both:
  - immediate `getAllUser()` render pass
  - short retry/poll window for late stream availability
- Handle `peer-video-state-change`, `user-added`, and `user-updated`.

### C) Self video appears at wrong page position

**Symptom**: Self video renders far down the page instead of in tile.

**Cause**: Container CSS/DOM mismatch for SDK inserted elements.

**Fix**:
- Use `video-player-container` for SDK video mounts.
- Ensure child elements are explicitly sized:

```css
video-player-container video-player,
video-player-container canvas,
video-player-container video {
  width: 100%;
  height: 100%;
  display: block;
}
```

### D) Command channel transfer message is "missed"

**Symptom**: Admit clicked, but customer does not transfer.

**Cause**: Command channel does not replay history. If customer wasn't fully in waiting session yet, message is missed.

**Fix**:
- Keep backend transfer state and allow customer to fetch transfer details after join.
- Consider one-time transfer lookup on customer waiting join as race guard.

### E) Repeated CORS errors to `log-external-gateway.zoom.us`

**Symptom**: Console spam with CORS 531 errors.

**Impact**: Usually telemetry-only; does not block core session/media.

**Action**: Treat as noise unless accompanied by actual join or media API failures.

---

## Related Documentation

- [SDK Architecture Pattern](../concepts/sdk-architecture-pattern.md) - Lifecycle order
- [Video Rendering](../examples/video-rendering.md) - attachVideo patterns
- [Event Handling](../examples/event-handling.md) - Required events
- [SKILL.md](../SKILL.md) - Quick reference

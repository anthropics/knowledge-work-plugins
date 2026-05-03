# HD Video Resolution

Achieve 720p and 1080p video quality in Zoom Web SDKs, including viewport size requirements that affect resolution.

## Overview

HD video quality in Zoom SDKs depends on multiple factors: container/viewport size, network bandwidth, SharedArrayBuffer support, and concurrent stream limits. **Video automatically scales down if the container is smaller than required dimensions.**

## Skills Needed

- **zoom-meeting-sdk** (Web)
- **zoom-video-sdk** (Web)

## Viewport Size Requirements

**Critical:** Video resolution is automatically adjusted based on the rendered container size.

### Resolution Thresholds

| Target Resolution | Minimum Container Size | Bandwidth Required |
|-------------------|------------------------|-------------------|
| **360p** | 480 × 270 | 600 kbps |
| **720p** | 1280 × 720 (or 720 × 411 gallery) | 1.2-1.5 Mbps |
| **1080p** | 1920 × 1080 | 2.5-3.0 Mbps |

**If your video container is smaller than 1280×720, you will NOT get 720p video - it will automatically scale down.**

### Meeting SDK Component View Constraints

| View Type | Minimum | Maximum | Aspect Ratio |
|-----------|---------|---------|--------------|
| **Speaker** | 240 × 135 | 1440 × 810 | 16:9 |
| **Gallery** | 720 × 411 | 1440 × 720 | 16:9 |
| **Ribbon** | 240 × 135 | 316 × 720 | Variable |

### Recommended Sizes for HD

```javascript
// For 720p in speaker view
const speakerContainer = {
  width: 1280,
  height: 720
};

// For 720p in gallery view (minimum)
const galleryContainer = {
  width: 720,
  height: 411
};

// For 1080p (speaker view only)
const fullHDContainer = {
  width: 1920,
  height: 1080
};
```

## Concurrent Stream Limits

**Video SDK enforces strict concurrent HD limits:**

| Resolution | Concurrent Limit | Notes |
|------------|------------------|-------|
| **720p** | **Max 2 streams** | Attempting 3rd results in `Errors_Wrong_Usage` |
| **1080p** | **Only 1 stream** | Only one 1080p video can be rendered at a time |

### Recommended Quality by View

| View Type | Active Speaker | Other Participants |
|-----------|----------------|-------------------|
| **Speaker View** | 720p or 1080p | 180p |
| **Gallery (3×3)** | 360p all | 360p |
| **Gallery (5×5)** | 180p all | 180p |
| **Small thumbnails** | 180p | 180p |

## SharedArrayBuffer (SAB) Requirement

### Features Requiring SAB

| Feature | SAB Required |
|---------|--------------|
| **Sending 720p video** | ✅ Yes |
| **Virtual Background** | ✅ Yes |
| **Gallery view (multiple videos)** | ✅ Yes |
| **Background noise suppression** | ✅ Yes |

### Enabling SharedArrayBuffer

Requires Cross-Origin Isolation headers on your server:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

**Express.js example:**
```javascript
app.use((req, res, next) => {
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
  next();
});
```

**Nginx example:**
```nginx
add_header Cross-Origin-Opener-Policy same-origin;
add_header Cross-Origin-Embedder-Policy require-corp;
```

### Browser Support for SAB

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 68+ |
| Edge | 79+ |
| Firefox | 79+ |
| Safari | 15.2+ (macOS), iOS 15.2+ |
| Opera | 73+ |

**Note:** Safari requires newer versions and may have limitations.

### Impact of Missing SAB

Without SharedArrayBuffer:
- Max sending resolution: **360p**
- No virtual background
- Limited to single video rendering
- No background noise suppression

## Video SDK Configuration

### Enable HD Video Capture

```javascript
// Start video with HD enabled
await stream.startVideo({
  hd: true,           // Enable 720p
  fullHd: true,       // Enable 1080p (if supported)
  captureWidth: 1280,
  captureHeight: 720
});
```

### Subscribe to Specific Quality

```javascript
// VideoQuality enum values:
// Video_90P = 0
// Video_180P = 1
// Video_360P = 2
// Video_720P = 3
// Video_1080P = 4

// Attach video at specific quality
await stream.attachVideo(userId, VideoQuality.Video_720P);

// Or with renderVideo
await stream.renderVideo(canvas, userId, 1280, 720, 0, 0, VideoQuality.Video_720P);
```

### Check Device Capabilities

```javascript
// Check if device supports HD
const capabilities = await stream.getVideoCapabilities();
console.log('Max resolution:', capabilities.maxResolution);
console.log('HD supported:', capabilities.hdSupported);
```

## Meeting SDK Configuration

### Component View HD

```javascript
ZoomMtg.init({
  leaveUrl: 'https://your-site.com',
  disablePreview: false,
  videoResolution: '720p',  // or '1080p'
  success: () => {
    console.log('Init success');
  }
});
```

### Responsive Container Setup

```html
<div id="zoom-container" style="width: 100%; max-width: 1280px; aspect-ratio: 16/9;">
  <!-- SDK renders here -->
</div>
```

```javascript
// Ensure container meets minimum size for HD
const container = document.getElementById('zoom-container');
const rect = container.getBoundingClientRect();

if (rect.width < 1280 || rect.height < 720) {
  console.warn('Container too small for 720p - video will be downscaled');
}
```

## WebRTC vs WebAssembly Mode

| Mode | Characteristics |
|------|-----------------|
| **WebRTC** (Primary, SDK v2+) | Enhanced performance, adaptive bitrate, better congestion control |
| **WebAssembly** (Fallback) | Custom Zoom codec, more reliable 720p, supports virtual backgrounds |

SDK v2 automatically selects mode based on network and device conditions.

## Account Requirements (Zoom Meetings)

For **Group HD** in Zoom Meetings (not SDK):

| Requirement | 720p | 1080p |
|-------------|------|-------|
| Max video participants | 2 | 2 |
| Full-screen mode | Required | Required |
| Active speaker mode | Required | Required |
| CPU | Minimum specs | i7 Quad Core+ |
| Bandwidth | 1.5 Mbps | 3.0 Mbps |
| Mobile support | ❌ No | ❌ No |

**Key:** If a third participant turns video on, quality reverts to standard definition.

## Best Practices

### 1. Size Your Container Correctly

```javascript
function ensureHDContainer(container, targetResolution = 720) {
  const minWidth = targetResolution === 1080 ? 1920 : 1280;
  const minHeight = targetResolution === 1080 ? 1080 : 720;
  
  container.style.minWidth = `${minWidth}px`;
  container.style.minHeight = `${minHeight}px`;
  container.style.aspectRatio = '16/9';
}
```

### 2. Handle Window Resize

```javascript
window.addEventListener('resize', () => {
  const container = document.getElementById('zoom-container');
  const rect = container.getBoundingClientRect();
  
  // Adjust quality based on available space
  if (rect.width >= 1920 && rect.height >= 1080) {
    stream.attachVideo(userId, VideoQuality.Video_1080P);
  } else if (rect.width >= 1280 && rect.height >= 720) {
    stream.attachVideo(userId, VideoQuality.Video_720P);
  } else {
    stream.attachVideo(userId, VideoQuality.Video_360P);
  }
});
```

### 3. Check SAB Support

```javascript
function checkSABSupport() {
  if (typeof SharedArrayBuffer === 'undefined') {
    console.warn('SharedArrayBuffer not available - HD features limited');
    return false;
  }
  
  // Check if cross-origin isolated
  if (!crossOriginIsolated) {
    console.warn('Not cross-origin isolated - SAB may not work');
    return false;
  }
  
  return true;
}
```

### 4. Limit Concurrent HD Streams

```javascript
const MAX_720P_STREAMS = 2;
let current720pCount = 0;

async function subscribeToVideo(userId, preferredQuality) {
  let quality = preferredQuality;
  
  if (quality === VideoQuality.Video_720P) {
    if (current720pCount >= MAX_720P_STREAMS) {
      console.warn('Max 720p streams reached, using 360p');
      quality = VideoQuality.Video_360P;
    } else {
      current720pCount++;
    }
  }
  
  await stream.attachVideo(userId, quality);
}
```

### 5. Maintain 16:9 Aspect Ratio

```css
.video-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.video-container canvas,
.video-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Video stuck at 360p | Container too small | Resize container to ≥1280×720 |
| Video stuck at 360p | Missing SAB headers | Add COOP/COEP headers |
| 720p works, 1080p doesn't | Only one 1080p allowed | Check concurrent streams |
| HD works in dev, not prod | Different CORS headers | Verify production headers |
| Safari HD not working | SAB not supported | Check Safari version ≥15.2 |

## Resources

- **Video SDK HD docs**: https://developers.zoom.us/docs/video-sdk/web/video-hd/
- **Meeting SDK resizing**: https://developers.zoom.us/docs/meeting-sdk/web/component-view/resizing/
- **SharedArrayBuffer docs**: https://developers.zoom.us/docs/meeting-sdk/web/sharedarraybuffer/
- **Cross-Origin Isolation**: https://web.dev/articles/coop-coep/

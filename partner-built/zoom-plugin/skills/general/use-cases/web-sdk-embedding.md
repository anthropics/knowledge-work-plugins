# Web SDK Embedding

Embed Zoom SDKs in iframes with proper cross-origin configuration.

## Overview

Configure your web application to properly embed Zoom Meeting SDK or Video SDK, including iframe setup, CORS headers, and cross-origin requirements.

## Skills Needed

- **zoom-meeting-sdk** (Web)
- **zoom-video-sdk** (Web)

## Embedding Options

| Option | Description |
|--------|-------------|
| Same-origin | SDK loaded in main page |
| iframe (same-origin) | SDK in iframe, same domain |
| iframe (cross-origin) | SDK in iframe, different domain |

## Required Headers

For cross-origin embedding with SharedArrayBuffer:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

## iframe Configuration

```html
<iframe
  src="https://your-zoom-app.com/meeting"
  allow="camera; microphone; display-capture"
  sandbox="allow-scripts allow-same-origin allow-forms"
></iframe>
```

## Common Tasks

### Basic iframe Embedding

```html
<!-- Parent page -->
<iframe
  id="zoom-frame"
  src="https://your-app.com/meeting-page"
  allow="camera; microphone; display-capture; autoplay; clipboard-write"
  sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
  style="width: 100%; height: 600px; border: none;"
></iframe>
```

### Cross-Origin Setup with SharedArrayBuffer

SharedArrayBuffer is required for:
- 720p sending
- Virtual backgrounds
- Gallery view

**Server headers (Node.js/Express)**:
```javascript
app.use((req, res, next) => {
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
  next();
});
```

**Nginx config**:
```nginx
location / {
  add_header Cross-Origin-Opener-Policy same-origin;
  add_header Cross-Origin-Embedder-Policy require-corp;
}
```

**Cloudflare Workers**:
```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const response = await fetch(request);
  const newResponse = new Response(response.body, response);
  newResponse.headers.set('Cross-Origin-Opener-Policy', 'same-origin');
  newResponse.headers.set('Cross-Origin-Embedder-Policy', 'require-corp');
  return newResponse;
}
```

### Permission Handling

```javascript
// Request permissions before joining
async function requestMediaPermissions() {
  try {
    await navigator.mediaDevices.getUserMedia({ 
      video: true, 
      audio: true 
    });
    return true;
  } catch (err) {
    console.error('Permission denied:', err);
    return false;
  }
}

// Check permission state
async function checkPermissions() {
  const camera = await navigator.permissions.query({ name: 'camera' });
  const microphone = await navigator.permissions.query({ name: 'microphone' });
  
  return {
    camera: camera.state,      // 'granted', 'denied', 'prompt'
    microphone: microphone.state
  };
}
```

### Communication Between Parent and iframe

**From parent to iframe**:
```javascript
// Parent page
const iframe = document.getElementById('zoom-frame');
iframe.contentWindow.postMessage({ 
  type: 'JOIN_MEETING',
  meetingNumber: '123456789',
  password: 'pass'
}, 'https://your-app.com');
```

**From iframe to parent**:
```javascript
// Inside iframe (meeting page)
window.parent.postMessage({
  type: 'MEETING_STATUS',
  status: 'joined'
}, '*');
```

**Receive messages**:
```javascript
// In parent or iframe
window.addEventListener('message', (event) => {
  // Verify origin
  if (event.origin !== 'https://trusted-domain.com') return;
  
  const { type, ...data } = event.data;
  
  switch (type) {
    case 'MEETING_STATUS':
      handleMeetingStatus(data);
      break;
    case 'LEAVE_MEETING':
      handleLeaveMeeting();
      break;
  }
});
```

### Mobile Responsive Embedding

```html
<style>
  .zoom-container {
    position: relative;
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
  }
  
  .zoom-container iframe {
    width: 100%;
    height: 100vh;
    max-height: 720px;
    border: none;
  }
  
  @media (max-width: 768px) {
    .zoom-container iframe {
      height: calc(100vh - 60px); /* Account for mobile browser chrome */
    }
  }
</style>

<div class="zoom-container">
  <iframe src="..." allow="..."></iframe>
</div>
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera/mic blocked | Check `allow` attribute |
| SharedArrayBuffer error | Add COOP/COEP headers |
| Cross-origin errors | Configure CORS properly |

## Resources

- **Meeting SDK Web**: https://developers.zoom.us/docs/meeting-sdk/web/
- **Video SDK Web**: https://developers.zoom.us/docs/video-sdk/web/

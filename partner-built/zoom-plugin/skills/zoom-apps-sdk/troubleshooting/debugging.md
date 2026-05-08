# Debugging Guide

Local development setup, ngrok configuration, and browser preview.

## ngrok Setup

ngrok provides an HTTPS tunnel to your local server. Required because Zoom Apps need HTTPS.

```bash
# Install ngrok (https://ngrok.com)
# Then start tunnel:
ngrok http 3000
```

Copy the `https://xxxxx.ngrok.io` URL.

### ngrok Free Tier Limitation

Free ngrok URLs **change every restart**. You must update 4 places in Marketplace each time:

1. **Home URL**: `https://xxxxx.ngrok.io`
2. **Redirect URL**: `https://xxxxx.ngrok.io/auth`
3. **OAuth Allow List**: `https://xxxxx.ngrok.io`
4. **Domain Allow List**: `xxxxx.ngrok.io` (no protocol)

**Tip:** Get ngrok paid plan ($8/mo) for a stable subdomain (e.g., `https://myapp.ngrok.io`).

## Marketplace Configuration for Local Dev

In [Zoom Marketplace](https://marketplace.zoom.us/) -> Your App:

### Feature tab -> Zoom App
- **Home URL**: `https://xxxxx.ngrok.io`
- **Share URL** (optional): `https://xxxxx.ngrok.io`

### Feature tab -> OAuth Redirect URL
- **Redirect URL for OAuth**: `https://xxxxx.ngrok.io/auth`
- **Add Allow List**: `https://xxxxx.ngrok.io`

### Feature tab -> Domain Allow List
- `xxxxx.ngrok.io`
- `appssdk.zoom.us` (if using CDN)

### Scopes tab
- `zoomapp:inmeeting` (minimum required)

## Browser Preview Mode

Test your UI outside Zoom by implementing a fallback:

```javascript
import zoomSdk from '@zoom/appssdk';

let isInZoom = false;

async function init() {
  try {
    const config = await zoomSdk.config({
      capabilities: ['getMeetingContext', 'getUserContext'],
      version: '0.16'
    });
    isInZoom = true;
    initZoomApp(config);
  } catch (error) {
    isInZoom = false;
    initBrowserPreview();
  }
}

function initBrowserPreview() {
  // Show mock UI with sample data for development
  const mockMeeting = { meetingID: '123456789', meetingTopic: 'Test Meeting' };
  const mockUser = { screenName: 'Dev User', role: 'host' };
  renderApp(mockMeeting, mockUser);
  console.log('Running in browser preview mode');
}
```

## Opening DevTools in Zoom

The Zoom client's embedded browser supports DevTools:

### Windows
1. Open Zoom client
2. Open your Zoom App
3. Right-click inside the app panel
4. Select "Inspect Element" (if available)

### Alternative: Remote Debugging
1. Start Zoom with remote debugging flag
2. Open `chrome://inspect` in Chrome
3. Find your app's WebView

**Note:** DevTools availability depends on Zoom client version and settings. Not all surfaces support it.

## Environment Variables

Use `.env` file with `dotenv`:

```bash
# .env (never commit this file)
ZOOM_APP_CLIENT_ID=abc123
ZOOM_APP_CLIENT_SECRET=xyz789
ZOOM_APP_REDIRECT_URI=https://xxxxx.ngrok.io/auth
SESSION_SECRET=random-secret-string-here
ZOOM_HOST=https://zoom.us
```

```javascript
// server.js
require('dotenv').config();
// process.env.ZOOM_APP_CLIENT_ID is now available
```

Add `.env` to `.gitignore`:
```
.env
.env.local
```

## Common Dev Workflow

```bash
# Terminal 1: Start server
npm run dev

# Terminal 2: Start ngrok
ngrok http 3000

# Then:
# 1. Copy ngrok URL
# 2. Update Marketplace URLs (if changed)
# 3. Open Zoom client
# 4. Click your app in sidebar or during meeting
# 5. Check the ngrok local request inspector for request logs
```

## ngrok Request Inspector

ngrok provides a local web UI that shows:
- All HTTP requests to your tunnel
- Request/response headers and bodies
- Replay failed requests

This is invaluable for debugging OAuth redirects and API calls.

## Resources

- **Testing guide**: https://developers.zoom.us/docs/zoom-apps/guides/testing/
- **ngrok docs**: https://ngrok.com/docs

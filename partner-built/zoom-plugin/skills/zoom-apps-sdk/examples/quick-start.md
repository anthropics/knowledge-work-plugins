# Quick Start - Hello World Zoom App

Complete working Zoom App with Express backend and SDK frontend.

## Prerequisites

- Node.js 18+
- ngrok account (free tier works)
- Zoom Marketplace app (type: "Zoom App")

## Project Setup

### package.json

```json
{
  "name": "zoom-app-hello-world",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.0",
    "cookie-session": "^2.0.0",
    "axios": "^1.6.0",
    "dotenv": "^16.0.0"
  }
}
```

### .env

```ini
ZOOM_APP_CLIENT_ID=your_client_id
ZOOM_APP_CLIENT_SECRET=your_client_secret
ZOOM_APP_REDIRECT_URI=https://xxxxx.ngrok.io/auth
SESSION_SECRET=generate_a_random_string_here
```

### server.js

```javascript
require('dotenv').config();
const express = require('express');
const crypto = require('crypto');
const cookieSession = require('cookie-session');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(express.static('public'));

// Cookie session - SameSite=None required for Zoom embedded browser
app.use(cookieSession({
  name: 'session',
  keys: [process.env.SESSION_SECRET],
  maxAge: 24 * 60 * 60 * 1000,
  sameSite: 'none',
  secure: true
}));

// OWASP security headers (required for Marketplace approval)
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Content-Security-Policy', "frame-ancestors 'self' zoom.us *.zoom.us");
  res.setHeader('Referrer-Policy', 'same-origin');
  next();
});

// Step 1: Install - redirect to Zoom OAuth
app.get('/install', (req, res) => {
  const verifier = crypto.randomBytes(32).toString('hex');
  const challenge = crypto.createHash('sha256').update(verifier).digest('base64url');
  const state = crypto.randomBytes(16).toString('hex');

  req.session.codeVerifier = verifier;
  req.session.state = state;

  const url = `https://zoom.us/oauth/authorize?` +
    `client_id=${process.env.ZOOM_APP_CLIENT_ID}` +
    `&response_type=code` +
    `&redirect_uri=${encodeURIComponent(process.env.ZOOM_APP_REDIRECT_URI)}` +
    `&code_challenge=${challenge}` +
    `&code_challenge_method=S256` +
    `&state=${state}`;

  res.redirect(url);
});

// Step 2: OAuth callback - exchange code for tokens
app.get('/auth', async (req, res) => {
  const { code, state } = req.query;

  if (state !== req.session.state) {
    return res.status(403).send('Invalid state');
  }

  try {
    // Exchange authorization code for tokens
    const tokenResponse = await axios.post('https://zoom.us/oauth/token', null, {
      params: {
        grant_type: 'authorization_code',
        code,
        redirect_uri: process.env.ZOOM_APP_REDIRECT_URI,
        code_verifier: req.session.codeVerifier
      },
      headers: {
        'Authorization': 'Basic ' + Buffer.from(
          `${process.env.ZOOM_APP_CLIENT_ID}:${process.env.ZOOM_APP_CLIENT_SECRET}`
        ).toString('base64')
      }
    });

    req.session.tokens = tokenResponse.data;

    // Get deeplink to open app in Zoom client
    const deeplink = await axios.post('https://api.zoom.us/v2/zoomapp/deeplink',
      { action: '' },
      { headers: { 'Authorization': `Bearer ${tokenResponse.data.access_token}` } }
    );

    res.redirect(deeplink.data.deeplink);
  } catch (error) {
    console.error('OAuth error:', error.response?.data || error.message);
    res.status(500).send('Authorization failed');
  }
});

// API endpoint for frontend
app.get('/api/user', (req, res) => {
  if (!req.session.tokens) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  res.json({ authenticated: true });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

### public/index.html

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Zoom App</title>
  <script src="https://appssdk.zoom.us/sdk.js"></script>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 20px; }
    .info { background: #f0f4f8; padding: 16px; border-radius: 8px; margin: 12px 0; }
    .error { background: #fff0f0; color: #c00; padding: 16px; border-radius: 8px; }
    button { padding: 10px 20px; background: #2d8cff; color: white; border: none; border-radius: 4px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>Hello Zoom App!</h1>
  <div id="content">Loading...</div>

  <script>
    // CRITICAL: Do NOT use "let zoomSdk" - causes SyntaxError
    let sdk = window.zoomSdk;

    async function init() {
      try {
        const configResponse = await sdk.config({
          capabilities: [
            'shareApp',
            'getMeetingContext',
            'getUserContext',
            'openUrl'
          ],
          version: '0.16'
        });

        const context = configResponse.runningContext;
        let html = `<div class="info"><strong>Running in:</strong> ${context}</div>`;

        if (context === 'inMeeting' || context === 'inWebinar') {
          const meeting = await sdk.getMeetingContext();
          const user = await sdk.getUserContext();

          html += `<div class="info"><strong>Meeting:</strong> ${meeting.meetingTopic || meeting.meetingID}</div>`;
          html += `<div class="info"><strong>User:</strong> ${user.screenName} (${user.role})</div>`;
          html += `<button onclick="shareApp()">Share App</button>`;
        } else {
          html += `<div class="info">Open this app during a meeting for full features.</div>`;
        }

        document.getElementById('content').innerHTML = html;
      } catch (error) {
        // Not running inside Zoom - show preview mode
        document.getElementById('content').innerHTML =
          '<div class="error">Not running inside Zoom client. ' +
          '<a href="/install">Install App</a> to get started.</div>';
      }
    }

    async function shareApp() {
      try {
        await sdk.shareApp();
      } catch (e) {
        console.error('Share failed:', e);
      }
    }

    // Initialize with timeout fallback
    document.addEventListener('DOMContentLoaded', () => {
      init();
      setTimeout(() => {
        if (document.getElementById('content').textContent === 'Loading...') {
          document.getElementById('content').innerHTML =
            '<div class="error">SDK timed out. <a href="/install">Install App</a></div>';
        }
      }, 3000);
    });
  </script>
</body>
</html>
```

## Running Locally

```bash
# 1. Install dependencies
npm install

# 2. Start ngrok tunnel
ngrok http 3000

# 3. Copy the https URL (e.g., https://abc123.ngrok.io)

# 4. Update .env with ngrok URL
# ZOOM_APP_REDIRECT_URI=https://abc123.ngrok.io/auth

# 5. Start server
npm run dev
```

## Marketplace Configuration

In [Zoom Marketplace](https://marketplace.zoom.us/) -> Your App:

1. **App Credentials**: Copy Client ID and Secret to `.env`
2. **Feature tab** -> Zoom App:
   - **Home URL**: `https://abc123.ngrok.io`
   - **Redirect URL**: `https://abc123.ngrok.io/auth`
   - **Domain Allow List**: `abc123.ngrok.io`
3. **Scopes tab**: Add `zoomapp:inmeeting`
4. **Local Test**: Click your app name in Zoom client sidebar to open

## Next Steps

- Add [In-Client OAuth](in-client-oauth.md) for seamless re-authorization
- Add [Layers API](layers-immersive.md) for immersive experiences
- Review [Security](../concepts/security.md) headers for Marketplace approval

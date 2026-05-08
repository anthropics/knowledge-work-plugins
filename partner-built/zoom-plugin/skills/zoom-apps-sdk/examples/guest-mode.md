# Guest Mode

Handle unauthenticated meeting participants who haven't authorized your app.

## Overview

When a meeting has external guests (non-Zoom users or users who haven't installed your app), they enter your app in an unauthenticated state. Guest mode lets you progressively request authorization.

## Three Authorization States

```
Unauthenticated ──> Authenticated ──> Authorized
     │                     │                │
     │                     │                │
  No Zoom identity    Has Zoom identity    Has OAuth tokens
  External guest      Zoom user, no app    Full app access
  Limited UI          Can promptAuthorize  All APIs available
```

| State | Who | getUserContext Returns | Can Use APIs |
|-------|-----|----------------------|-------------|
| **Unauthenticated** | External guests, no Zoom account | Minimal (no user ID) | Very limited |
| **Authenticated** | Zoom users who haven't authorized your app | Name, role (no personal data) | Read-only context |
| **Authorized** | Users who authorized your app | Full user data | All APIs |

## Detecting State

```javascript
import zoomSdk from '@zoom/appssdk';

await zoomSdk.config({
  capabilities: ['getUserContext', 'authorize', 'promptAuthorize', 'onAuthorized'],
  version: '0.16'
});

const user = await zoomSdk.getUserContext();

if (user.status === 'authorized') {
  showFullApp();
} else if (user.status === 'authenticated') {
  showLimitedApp();
  showAuthorizeButton();
} else {
  showGuestView();
  showAuthorizeButton();
}
```

## Prompting Authorization

```javascript
// Show a button that triggers authorization
document.getElementById('authorize-btn').addEventListener('click', async () => {
  try {
    await zoomSdk.promptAuthorize();
  } catch (e) {
    console.error('Authorization prompt failed:', e);
  }
});

// Listen for successful authorization
zoomSdk.addEventListener('onAuthorized', async (event) => {
  const { code, state } = event;

  // Exchange code for tokens on your backend
  await fetch('/api/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, state })
  });

  // Upgrade UI to full access
  showFullApp();
});
```

## UI Pattern

```javascript
function showGuestView() {
  document.getElementById('app').innerHTML = `
    <h2>Welcome, Guest!</h2>
    <p>You're viewing this app as a guest. Authorize to unlock all features.</p>
    <div id="limited-content">
      <!-- Show read-only or minimal content -->
    </div>
    <button id="authorize-btn">Authorize App</button>
  `;
}

function showLimitedApp() {
  document.getElementById('app').innerHTML = `
    <h2>Welcome!</h2>
    <p>Authorize to unlock all features.</p>
    <div id="limited-content">
      <!-- Show more content than guest, but still limited -->
    </div>
    <button id="authorize-btn">Authorize for Full Access</button>
  `;
}

function showFullApp() {
  document.getElementById('app').innerHTML = `
    <h2>Full App Access</h2>
    <div id="full-content">
      <!-- All features available -->
    </div>
  `;
}
```

## Host-Required Authorization

Meeting hosts can require all participants to authorize before using the app. This is configured in the Marketplace app settings under the "Guest Mode" feature.

When enabled, unauthenticated/authenticated users see the authorization prompt immediately.

## Resources

- **Guest mode docs**: https://developers.zoom.us/docs/zoom-apps/guides/guest-mode/
- **Sample app**: https://github.com/zoom/zoomapps-advancedsample-react (includes guest mode)

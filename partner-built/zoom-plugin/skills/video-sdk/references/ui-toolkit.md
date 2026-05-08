# Video SDK UI Toolkit

Pre-built, low-code video chat UI powered by Zoom Video SDK.

## Overview

The Video SDK UI Toolkit provides ready-to-use video components so you don't have to build the UI from scratch. Available for Web, iOS, and Android.

## Platform Availability

| Platform | UI Toolkit | Package/Repo |
|----------|-----------|--------------|
| **Web** | Yes | `@zoom/videosdk-zoom-ui-toolkit` |
| **iOS** | Yes | [zoom/videosdk-zoom-ui-toolkit-ios](https://github.com/zoom/videosdk-zoom-ui-toolkit-ios) |
| **Android** | Yes | [zoom/videosdk-uitoolkit-android-sample](https://github.com/zoom/videosdk-uitoolkit-android-sample) |
| React Native | No | Use SDK + custom UI |
| Flutter | No | Use SDK + custom UI |

## Web Installation

### npm

```bash
npm install @zoom/videosdk-zoom-ui-toolkit --save
```

```javascript
import uitoolkit from "@zoom/videosdk-zoom-ui-toolkit";
import "@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css";
```

### CDN

```html
<link rel="stylesheet" href="https://source.zoom.us/uitoolkit/2.3.5/videosdk-zoom-ui-toolkit.css" />
<script src="https://source.zoom.us/uitoolkit/2.3.5/videosdk-zoom-ui-toolkit.min.umd.js"></script>
<script>
  const uitoolkit = window.UIToolkit;
</script>
```

### Angular

Add CSS to `angular.json`:
```json
"styles": [
  "node_modules/@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css"
]
```

## Quick Start

```html
<div id="sessionContainer"></div>
```

```javascript
import uitoolkit from "@zoom/videosdk-zoom-ui-toolkit";
import "@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css";

const config = {
  videoSDKJWT: "your-jwt-token",
  sessionName: "SessionA",
  userName: "UserA",
  sessionPasscode: "abc123",
  featuresOptions: {
    preview: true,
    video: true,
    audio: true,
    share: true,
    chat: true,
    users: true,
    settings: true,
    leave: true,
  },
};

const sessionContainer = document.getElementById("sessionContainer");
uitoolkit.joinSession(sessionContainer, config);
```

## Feature Components

Toggle components on/off via `featuresOptions`:

| Component | Description | Paid Plan? |
|-----------|-------------|------------|
| `preview` | Pre-session device selection, virtual background | No |
| `video` | Video layout for sending/receiving | No |
| `audio` | Audio button and controls | No |
| `share` | Screen sharing | No |
| `chat` | In-session chat | No |
| `users` | Participant list | No |
| `settings` | Device config, virtual background, stats | No |
| `viewMode` | Grid/speaker view options | No |
| `leave` | Leave/end session button | No |
| `invite` | Invite via link | No |
| `theme` | Theme color selection | No |
| `feedback` | Session feedback form | No |
| `troubleshoot` | Zoom Probe SDK troubleshooting | No |
| `subsession` | Breakout rooms button | No |
| `playback` | Media file playback | No |
| `recording` | Cloud recording | **Yes** |
| `phone` | Join by phone audio | **Yes** |
| `caption` | Live translations | **Yes** |

## React Example

```jsx
import uitoolkit from "@zoom/videosdk-zoom-ui-toolkit";
import "@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css";
import { useEffect, useRef } from "react";

function VideoSession({ jwt, sessionName, userName }) {
  const containerRef = useRef(null);
  
  useEffect(() => {
    const config = {
      videoSDKJWT: jwt,
      sessionName,
      userName,
      sessionPasscode: "abc123",
      featuresOptions: {
        video: true,
        audio: true,
        chat: true,
        users: true,
        leave: true,
      },
    };
    
    if (containerRef.current) {
      uitoolkit.joinSession(containerRef.current, config);
    }
    
    return () => {
      if (containerRef.current) {
        uitoolkit.closeSession(containerRef.current);
      }
    };
  }, [jwt, sessionName, userName]);
  
  return <div ref={containerRef} style={{ height: '600px' }} />;
}
```

## Event Listeners

```javascript
// Session events
uitoolkit.onSessionJoined(() => {
  console.log("Session joined");
});

uitoolkit.onSessionClosed(() => {
  console.log("Session closed");
});

// Unsubscribe
uitoolkit.offSessionJoined(callback);
uitoolkit.offSessionClosed(callback);
```

## Component Visibility Control

```javascript
// Hide all components
uitoolkit.hideAllComponents();

// Show/hide individual components
uitoolkit.showControlsComponent(container);
uitoolkit.hideControlsComponent(container);

uitoolkit.showChatComponent(container);
uitoolkit.hideChatComponent(container);

uitoolkit.showUsersComponent(container);
uitoolkit.hideUsersComponent(container);

uitoolkit.showSettingsComponent(container);
uitoolkit.hideSettingsComponent(container);
```

## Close Session

```javascript
uitoolkit.closeSession(sessionContainer);
```

## Live Demo

- **With SharedArrayBuffer**: https://videosdk.dev/uitoolkit/
- **Without SharedArrayBuffer**: https://videosdk.dev/uitoolkit-no-sab/

## Sample Repositories

| Framework | Repository |
|-----------|------------|
| React | [zoom/videosdk-zoom-ui-toolkit-react-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-react-sample) |
| Angular | [zoom/videosdk-zoom-ui-toolkit-angular-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-angular-sample) |
| Vue.js | [zoom/videosdk-zoom-ui-toolkit-vuejs-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-vuejs-sample) |
| Vanilla JS | [zoom/videosdk-zoom-ui-toolkit-javascript-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-javascript-sample) |

## Resources

- **Official docs**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/
- **npm package**: https://www.npmjs.com/package/@zoom/videosdk-zoom-ui-toolkit
- **GitHub**: https://github.com/zoom/videosdk-zoom-ui-toolkit-web

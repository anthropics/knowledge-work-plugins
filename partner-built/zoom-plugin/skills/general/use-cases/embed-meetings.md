# Embed Meetings

Embed the full Zoom meeting experience into your web or mobile application.

## Overview

Use the Zoom Meeting SDK to embed complete Zoom meetings into your application with Zoom's UI and features.

## Skills Needed

- **zoom-meeting-sdk** - Primary

## Platform Options

| Platform | View Options |
|----------|--------------|
| Web | Component View, Client View |
| iOS | Native SDK |
| Android | Native SDK |
| Desktop | Native SDK |

## Web Views

| View | Description |
|------|-------------|
| Component View | Extractable, customizable UI elements |
| Client View | Full-page Zoom meeting experience |

## Quick Start (Web Component View)

```javascript
const client = ZoomMtgEmbedded.createClient();

client.init({
  zoomAppRoot: document.getElementById('meetingSDKElement'),
  language: 'en-US',
});

client.join({
  sdkKey: 'YOUR_SDK_KEY',
  signature: 'YOUR_SIGNATURE',
  meetingNumber: 'MEETING_NUMBER',
  userName: 'User Name',
});
```

## Common Tasks

### Component View Setup

Component View embeds the meeting in a specific DOM element, allowing you to build UI around it.

```javascript
import ZoomMtgEmbedded from '@zoom/meetingsdk/embedded';

// Create client
const client = ZoomMtgEmbedded.createClient();

// Initialize
await client.init({
  zoomAppRoot: document.getElementById('meetingSDKElement'),
  language: 'en-US',
  customize: {
    video: {
      isResizable: true,
      viewSizes: {
        default: { width: 1000, height: 600 },
        ribbon: { width: 300, height: 700 }
      }
    },
    meetingInfo: ['topic', 'host', 'mn', 'pwd', 'telPwd', 'invite', 'participant', 'dc', 'enctype'],
    toolbar: {
      buttons: [
        { text: 'Custom', className: 'CustomButton', onClick: () => console.log('Custom clicked') }
      ]
    }
  }
});

// Join meeting
await client.join({
  sdkKey: SDK_KEY,
  signature: signature,
  meetingNumber: '123456789',
  password: 'password',
  userName: 'John Doe',
  userEmail: 'john@example.com'
});
```

### Client View Setup

Client View opens a full-page meeting experience (traditional Zoom UI).

```javascript
import { ZoomMtg } from '@zoom/meetingsdk';

// Load dependencies
ZoomMtg.preLoadWasm();
ZoomMtg.prepareWebSDK();

// Initialize
ZoomMtg.init({
  leaveUrl: 'https://your-app.com/meeting-ended',
  success: () => {
    ZoomMtg.join({
      sdkKey: SDK_KEY,
      signature: signature,
      meetingNumber: '123456789',
      passWord: 'password',
      userName: 'John Doe',
      userEmail: 'john@example.com',
      success: (res) => {
        console.log('Joined meeting', res);
      },
      error: (err) => {
        console.error('Join error', err);
      }
    });
  }
});
```

### Customizing Meeting UI

```javascript
// Hide specific UI elements
await client.init({
  zoomAppRoot: document.getElementById('meetingSDKElement'),
  customize: {
    // Hide meeting info
    meetingInfo: [],
    
    // Customize toolbar
    toolbar: {
      buttons: [
        // Add custom buttons
        {
          text: 'Info',
          className: 'info-btn',
          onClick: () => showInfo()
        }
      ]
    },
    
    // Video layout
    video: {
      viewSizes: {
        default: { width: 1280, height: 720 }
      },
      popper: {
        disableDraggable: false
      }
    },
    
    // Active speaker view
    activeStateEnabledMode: {
      enabled: true
    }
  }
});

// Change view programmatically
client.changeView('gallery');  // 'speaker' | 'gallery' | 'ribbon'
```

### Handling Meeting Events

```javascript
// Meeting status events
client.on('connection-change', (payload) => {
  const { state } = payload;
  switch (state) {
    case 'Connected':
      console.log('Connected to meeting');
      break;
    case 'Reconnecting':
      console.log('Reconnecting...');
      break;
    case 'Closed':
      console.log('Meeting ended');
      handleMeetingEnd();
      break;
  }
});

// User events
client.on('user-added', (payload) => {
  console.log('User joined:', payload);
});

client.on('user-removed', (payload) => {
  console.log('User left:', payload);
});

// Audio/video events
client.on('active-speaker', (payload) => {
  console.log('Active speaker:', payload.userId);
});

// Error handling
client.on('error', (payload) => {
  console.error('SDK Error:', payload);
});
```

### Leave/End Meeting

```javascript
// Leave meeting (participant)
client.leaveMeeting();

// End meeting (host only)
client.endMeeting();

// Handle leave URL (Client View)
// User is redirected to leaveUrl specified in init()
```

## Native SDK (iOS/Android)

For native mobile apps, see:
- [Meeting SDK iOS](../../meeting-sdk/references/ios.md)
- [Meeting SDK Android](../../meeting-sdk/references/android.md)

## Resources

- **Meeting SDK docs**: https://developers.zoom.us/docs/meeting-sdk/
- **Web sample**: https://github.com/zoom/meetingsdk-web-sample
- **Component View docs**: https://developers.zoom.us/docs/meeting-sdk/web/component-view/

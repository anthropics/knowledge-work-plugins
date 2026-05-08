# In-Meeting Apps

Build apps that run inside the Zoom client during meetings.

## Overview

Create Zoom Apps that appear within the Zoom meeting interface - polls, games, collaboration tools, and more that participants can interact with during meetings.

## Skills Needed

- **zoom-apps-sdk** - Primary
- **oauth** - Authentication
- **zoom-rest-api** - Server-side API calls (optional)

## App Types

| Type | Description | Key APIs |
|------|-------------|----------|
| Sidebar app | Panel alongside meeting | getMeetingContext, shareApp |
| Immersive app | Full-screen Layers API | runRenderingContext, drawParticipant |
| Camera mode | Virtual camera overlay | runRenderingContext({ view: 'camera' }) |
| Collaborate | Shared state app | startCollaborate, connect, postMessage |
| Background app | Runs without visible UI | Events, REST API calls |

## Architecture

```
Frontend (Zoom embedded browser)     Backend (Express/Node.js)
─────────────────────────────────    ────────────────────────
@zoom/appssdk                        OAuth token exchange
zoomSdk.config()                     REST API calls
zoomSdk.getMeetingContext()           Token storage (Redis)
fetch('/api/data')  ─────────────>   Business logic
```

## Quick Start

```javascript
import zoomSdk from '@zoom/appssdk';

await zoomSdk.config({
  capabilities: ['shareApp', 'getMeetingContext', 'getUserContext'],
  version: '0.16'
});

const context = await zoomSdk.getMeetingContext();
console.log('Meeting ID:', context.meetingID);

await zoomSdk.shareApp();
```

## Common Tasks

### Building a Poll App

```javascript
import zoomSdk from '@zoom/appssdk';

// Initialize
await zoomSdk.config({
  capabilities: [
    'shareApp',
    'getMeetingContext',
    'getMeetingParticipants',
    'sendAppInvitation'
  ]
});

// Poll state
let currentPoll = {
  question: '',
  options: [],
  votes: {}
};

// Create poll
function createPoll(question, options) {
  currentPoll = {
    question,
    options,
    votes: {}
  };
  broadcastPollState();
}

// Submit vote
async function submitVote(optionIndex) {
  const context = await zoomSdk.getMeetingContext();
  currentPoll.votes[context.participantId] = optionIndex;
  broadcastPollState();
}

// Share results
function getResults() {
  const counts = currentPoll.options.map((_, i) => 
    Object.values(currentPoll.votes).filter(v => v === i).length
  );
  return currentPoll.options.map((opt, i) => ({
    option: opt,
    count: counts[i],
    percentage: (counts[i] / Object.keys(currentPoll.votes).length * 100).toFixed(1)
  }));
}

// Invite others to participate
async function inviteParticipants() {
  await zoomSdk.sendAppInvitation({
    action: 'open',
    message: 'Join the poll!'
  });
}
```

### Collaborative Whiteboard

```javascript
// Whiteboard with real-time sync
const canvas = document.getElementById('whiteboard');
const ctx = canvas.getContext('2d');

// Drawing state
let isDrawing = false;
let lastX = 0;
let lastY = 0;

canvas.addEventListener('mousedown', (e) => {
  isDrawing = true;
  [lastX, lastY] = [e.offsetX, e.offsetY];
});

canvas.addEventListener('mousemove', (e) => {
  if (!isDrawing) return;
  
  const stroke = {
    from: { x: lastX, y: lastY },
    to: { x: e.offsetX, y: e.offsetY },
    color: currentColor,
    width: currentWidth
  };
  
  drawStroke(stroke);
  broadcastStroke(stroke);  // Sync with others
  
  [lastX, lastY] = [e.offsetX, e.offsetY];
});

function drawStroke(stroke) {
  ctx.beginPath();
  ctx.moveTo(stroke.from.x, stroke.from.y);
  ctx.lineTo(stroke.to.x, stroke.to.y);
  ctx.strokeStyle = stroke.color;
  ctx.lineWidth = stroke.width;
  ctx.lineCap = 'round';
  ctx.stroke();
}

// Receive strokes from others
onRemoteStroke((stroke) => {
  drawStroke(stroke);
});
```

### Meeting Timer/Agenda

```javascript
import zoomSdk from '@zoom/appssdk';

// Timer app
class MeetingTimer {
  constructor() {
    this.agenda = [];
    this.currentItem = 0;
    this.startTime = null;
  }
  
  async init() {
    await zoomSdk.config({
      capabilities: ['getMeetingContext', 'shareApp']
    });
  }
  
  setAgenda(items) {
    // items: [{ title: 'Intro', duration: 5 }, ...]
    this.agenda = items.map(item => ({
      ...item,
      elapsed: 0,
      status: 'pending'
    }));
    this.broadcastState();
  }
  
  start() {
    this.startTime = Date.now();
    this.agenda[this.currentItem].status = 'active';
    this.tick();
  }
  
  tick() {
    const item = this.agenda[this.currentItem];
    const elapsed = Math.floor((Date.now() - this.startTime) / 1000 / 60);
    item.elapsed = elapsed;
    
    if (elapsed >= item.duration) {
      this.alertTimeUp();
    }
    
    this.broadcastState();
    setTimeout(() => this.tick(), 1000);
  }
  
  nextItem() {
    this.agenda[this.currentItem].status = 'completed';
    this.currentItem++;
    if (this.currentItem < this.agenda.length) {
      this.startTime = Date.now();
      this.agenda[this.currentItem].status = 'active';
    }
  }
  
  alertTimeUp() {
    // Visual/audio alert
    document.getElementById('timer').classList.add('warning');
  }
}
```

### Layers API Visuals

```javascript
import zoomSdk from '@zoom/appssdk';

// Layers API for immersive experiences
await zoomSdk.config({
  capabilities: ['runRenderingContext', 'clearRenderingContext']
});

// Start Layers mode
await zoomSdk.runRenderingContext({
  view: 'immersive'
});

// Draw on the video layer
const canvas = document.getElementById('layers-canvas');
const ctx = canvas.getContext('2d');

// Example: Add participant name labels
function drawNameLabel(participant, x, y) {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.fillRect(x, y - 25, 150, 25);
  ctx.fillStyle = 'white';
  ctx.font = '14px Arial';
  ctx.fillText(participant.name, x + 5, y - 8);
}

// Example: Add virtual background effects
function drawVirtualEffect() {
  // Draw confetti, borders, icons, etc.
  // These overlay on top of video
}

// Stop Layers mode
async function exitLayers() {
  await zoomSdk.clearRenderingContext();
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ZOOM_APP_CLIENT_ID` | Marketplace App Credentials |
| `ZOOM_APP_CLIENT_SECRET` | Marketplace App Credentials |
| `ZOOM_APP_REDIRECT_URI` | Your server URL + /auth |
| `SESSION_SECRET` | Random string for cookie signing |

## Detailed Guides

- **[zoom-apps-sdk SKILL.md](../../zoom-apps-sdk/SKILL.md)** - Comprehensive SDK guide
- **[Quick Start](../../zoom-apps-sdk/examples/quick-start.md)** - Hello World app
- **[In-Client OAuth](../../zoom-apps-sdk/examples/in-client-oauth.md)** - Authorization flow
- **[Layers API](../../zoom-apps-sdk/references/layers-api.md)** - Immersive experiences
- **[Immersive Experiences](immersive-experiences.md)** - Custom video layouts
- **[Collaborative Apps](collaborative-apps.md)** - Real-time shared state

## Skill Chain

```
zoom-apps-sdk  -->  oauth  -->  zoom-rest-api (optional)
```

## App Publishing Checklist

- [ ] OWASP security headers on all responses
- [ ] HTTPS enforced, valid SSL certificate
- [ ] PKCE OAuth implemented
- [ ] Error handling for all SDK calls
- [ ] Browser preview fallback UI
- [ ] Domain allowlist configured
- [ ] Tested on multiple screen sizes
- [ ] Submit to Zoom Marketplace

## Resources

- **Zoom Apps docs**: https://developers.zoom.us/docs/zoom-apps/
- **Layers API**: https://developers.zoom.us/docs/zoom-apps/guides/layers-api/
- **Sample apps**: https://github.com/zoom/zoomapps-sample-js

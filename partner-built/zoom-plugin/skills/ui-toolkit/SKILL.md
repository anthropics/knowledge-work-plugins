---
name: ui-toolkit/web
description: "Reference skill for Zoom Video SDK UI Toolkit. Use after routing to a web video workflow when you want prebuilt React UI instead of building a fully custom Video SDK interface."
user-invocable: false
triggers:
  - "ui toolkit"
  - "zoom ui"
  - "prebuilt video ui"
  - "video conferencing ui"
  - "zoom video ui toolkit"
  - "uitoolkit"
  - "ready-made zoom ui"
---

# Zoom Video SDK UI Toolkit

Background reference for the prebuilt Zoom Video SDK UI Toolkit on web. Prefer `choose-zoom-approach` first when the user might still need Meeting SDK instead.

**Official Documentation**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/
**API Reference**: https://marketplacefront.zoom.us/sdk/uitoolkit/web/
**NPM Package**: https://www.npmjs.com/package/@zoom/videosdk-zoom-ui-toolkit
**Live Demo**: https://sdk.zoom.com/videosdk-uitoolkit

## Quick Links

**New to UI Toolkit? Follow this path:**

1. **Quick Start** - Get running in 5 minutes (see below)
2. **JWT Authentication** - Server-side token generation (required)
3. **Composite vs Components** - Choose your approach  
4. **Framework Integration** - React, Vue, Angular, Next.js patterns
5. **Integrated Index** - see the section below in this file

**Having issues?**
- Session not joining → Check JWT Authentication (most common issue)
- React 18 peer dependency error → See Installation section
- CSS not loading → See [Troubleshooting](troubleshooting/common-issues.md)
- Components not showing → Check Component Lifecycle
- Start with preflight checks → [5-Minute Runbook](RUNBOOK.md)

## Overview

The Zoom Video SDK UI Toolkit is a **pre-built video UI library** that renders complete video conferencing experiences with minimal code. Unlike the raw Video SDK, the UI Toolkit provides:

- ✅ **Ready-to-use UI** - Professional video interface out of the box
- ✅ **Zero UI code** - No need to build video layouts, controls, or participant management
- ✅ **Framework agnostic** - Works with React, Vue, Angular, Next.js, vanilla JS
- ✅ **Highly customizable** - Choose which features to enable, customize themes
- ✅ **Built-in features** - Chat, screen share, settings, virtual backgrounds included

**When to use UI Toolkit:**
- You want a complete video solution quickly
- You need Zoom-like UI consistency
- You don't want to build custom video UI
- You need standard features (chat, share, participants)

**When to use raw Video SDK instead:**
- You need complete custom UI control
- You're building a non-standard video experience
- You need access to raw video/audio data
- You want to build your own rendering pipeline

## Installation

```bash
npm install @zoom/videosdk-zoom-ui-toolkit jsrsasign
npm install -D @types/jsrsasign
```

**Note**: React support depends on the UI Toolkit version. Check the package peer dependencies for your installed version (React 18 is commonly required).

## Quick Start

### Basic Usage (Vanilla JS)

```javascript
import uitoolkit from "@zoom/videosdk-zoom-ui-toolkit";
import "@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css";

const container = document.getElementById("sessionContainer");

const config = {
  videoSDKJWT: "your_jwt_token",
  sessionName: "my-session",
  userName: "John Doe",
  sessionPasscode: "",
  features: ["video", "audio", "share", "chat", "users", "settings"],
};

uitoolkit.joinSession(container, config);

uitoolkit.onSessionJoined(() => {
  console.log("Session joined");
});

uitoolkit.onSessionClosed(() => {
  console.log("Session closed");
});
```

### Next.js / React Integration

```typescript
'use client';

import { useEffect, useRef } from 'react';

export default function VideoSession({ jwt, sessionName, userName }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const uitoolkitRef = useRef<any>(null);

  useEffect(() => {
    let isMounted = true;

    const init = async () => {
      const uitoolkitModule = await import('@zoom/videosdk-zoom-ui-toolkit');
      const uitoolkit = uitoolkitModule.default;
      uitoolkitRef.current = uitoolkit;
      
      // If TypeScript complains about CSS imports, configure your app to allow them
      // (for example via a global `declare module \"*.css\";`), or import the CSS from
      // a global entrypoint (Next.js layout/_app) instead of inlining here.
      await import('@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css');

      if (!isMounted || !containerRef.current) return;

      const config: any = {
        videoSDKJWT: jwt,
        sessionName: sessionName,
        userName: userName,
        sessionPasscode: '',
        features: ['video', 'audio', 'share', 'chat', 'users', 'settings'],
      };

      uitoolkit.joinSession(containerRef.current, config);
      uitoolkit.onSessionJoined(() => console.log('Joined'));
      uitoolkit.onSessionClosed(() => console.log('Closed'));
    };

    init();

    return () => {
      isMounted = false;
      if (uitoolkitRef.current && containerRef.current) {
        try {
          uitoolkitRef.current.closeSession(containerRef.current);
        } catch (e) {}
      }
    };
  }, [jwt, sessionName, userName]);

  return <div ref={containerRef} style={{ width: '100%', height: '100vh' }} />;
}
```

## Available Features

| Feature | Description |
|---------|-------------|
| `video` | Enable video layout and send/receive video |
| `audio` | Show audio button, send/receive audio |
| `share` | Screen sharing |
| `chat` | In-session messaging |
| `users` | Participant list |
| `settings` | Device selection, virtual background |
| `preview` | Pre-join camera/mic preview |
| `recording` | Cloud recording (paid plan) |
| `leave` | Leave/end session button |

## Troubleshooting

- **[troubleshooting/common-issues.md](troubleshooting/common-issues.md)** - CSS, SSR, JWT/session join, customization limits

## JWT Token Generation (Server-Side)

**Required**: Generate JWT tokens on your server, never expose SDK secret client-side.

### Node.js / Next.js API Route

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { KJUR } from 'jsrsasign';

const ZOOM_VIDEO_SDK_KEY = process.env.ZOOM_VIDEO_SDK_KEY;
const ZOOM_VIDEO_SDK_SECRET = process.env.ZOOM_VIDEO_SDK_SECRET;

export async function POST(request: NextRequest) {
  const { sessionName, role, userName } = await request.json();

  if (!sessionName || role === undefined) {
    return NextResponse.json({ error: 'Missing params' }, { status: 400 });
  }

  const iat = Math.floor(Date.now() / 1000);
  const exp = iat + 60 * 60 * 2; // 2 hours

  const oHeader = { alg: 'HS256', typ: 'JWT' };
  const oPayload = {
    app_key: ZOOM_VIDEO_SDK_KEY,
    role_type: role, // 0 = participant, 1 = host
    tpc: sessionName,
    version: 1,
    iat,
    exp,
    user_identity: userName || 'User',
  };

  const signature = KJUR.jws.JWS.sign(
    'HS256',
    JSON.stringify(oHeader),
    JSON.stringify(oPayload),
    ZOOM_VIDEO_SDK_SECRET
  );

  return NextResponse.json({ signature });
}
```

### JWT Payload Fields

| Field | Required | Description |
|-------|----------|-------------|
| `app_key` | Yes | Your Video SDK Key |
| `role_type` | Yes | 0 = participant, 1 = host |
| `tpc` | Yes | Session/topic name |
| `version` | Yes | Always 1 |
| `iat` | Yes | Issued at (Unix timestamp) |
| `exp` | Yes | Expiration (Unix timestamp) |
| `user_identity` | No | User identifier |

## API Reference

### Core Methods

```javascript
uitoolkit.joinSession(container, config);
uitoolkit.closeSession(container);
```

### Event Listeners

```javascript
uitoolkit.onSessionJoined(callback);
uitoolkit.onSessionClosed(callback);
uitoolkit.offSessionJoined(callback);
uitoolkit.offSessionClosed(callback);
```

### Component Methods

```javascript
uitoolkit.showChatComponent(container);
uitoolkit.hideChatComponent(container);
uitoolkit.showUsersComponent(container);
uitoolkit.hideUsersComponent(container);
uitoolkit.showControlsComponent(container);
uitoolkit.hideControlsComponent(container);
uitoolkit.showSettingsComponent(container);
uitoolkit.hideSettingsComponent(container);
uitoolkit.hideAllComponents();
```

## CDN Usage (No Build Step)

```html
<link rel="stylesheet" href="https://source.zoom.us/uitoolkit/2.3.5-1/videosdk-zoom-ui-toolkit.css" />
<script src="https://source.zoom.us/uitoolkit/2.3.5-1/videosdk-zoom-ui-toolkit.min.umd.js"></script>

<div id="sessionContainer"></div>

<script>
  const uitoolkit = window.UIToolkit;
  
  uitoolkit.joinSession(document.getElementById('sessionContainer'), {
    videoSDKJWT: 'your_jwt',
    sessionName: 'my-session',
    userName: 'User',
    features: ['video', 'audio', 'chat']
  });
</script>
```

## Next.js with basePath

When deploying Next.js under a subpath:

```typescript
// next.config.ts
const nextConfig = {
  basePath: "/your-app-path",
  assetPrefix: "/your-app-path",
};
```

Fetch API routes with full path:
```typescript
fetch('/your-app-path/api/token', { ... })
```

## Prerequisites

1. **Zoom Video SDK credentials** from [Zoom Marketplace](https://marketplace.zoom.us/)
2. **React** version compatible with your installed UI Toolkit package (check peer deps; React 18 is common)
3. **Server-side JWT generation** (never expose SDK secret)
4. **Modern browser** with WebRTC support

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | 78+ |
| Firefox | 76+ |
| Safari | 14.1+ |
| Edge | 79+ |

## Common Issues

| Issue | Solution |
|-------|----------|
| `peer react@"^18.0.0"` error | Use the React version required by the installed UI Toolkit package (check peer deps; React 18 is common) |
| CSS import TypeScript error | Configure TS/CSS handling (prefer a global `*.css` module declaration); avoid `@ts-ignore` except in throwaway demos |
| Config type error | Type config as `any` |
| API returns HTML not JSON | Check basePath in fetch URL |

## Resources

- **GitHub**: https://github.com/zoom/videosdk-zoom-ui-toolkit-web
- **UI Toolkit Docs**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/
- **Auth Endpoint Sample**: https://github.com/zoom/videosdk-auth-endpoint-sample
- **Marketplace**: https://marketplace.zoom.us/

---

## Integrated Index

_This section was migrated from `SKILL.md`._

Complete navigation for all UI Toolkit documentation.

## 📚 Start Here

New to the UI Toolkit? Follow this learning path:

1. **[SKILL.md](SKILL.md)** - Main overview and quick start
2. **[5-Minute Runbook](RUNBOOK.md)** - Preflight checks before deep debugging
3. **Quick Start Guide** - Working code in 5 minutes (see skill.md)
4. **JWT Authentication** - Server-side token generation (see skill.md)
5. **Choose Your Mode** - Composite vs Components (see skill.md)

## 🎯 Core Concepts

Understanding how UI Toolkit works:

- **Composite vs Components** - Two ways to use UI Toolkit (see skill.md)
- **UI Toolkit Architecture** - How it wraps Video SDK internally
- **Feature Configuration** - Understanding featuresOptions structure
- **Session Lifecycle** - Join → Active → Leave/Close → Destroy flow

## 📖 Complete Guides

### Getting Started
- **Installation** - NPM install and React 18 setup (see skill.md)
- **Quick Start - Composite** - Full UI in one container (see skill.md)
- **Quick Start - Components** - Individual UI pieces (see skill.md)
- **JWT Authentication** - Server-side token generation (see skill.md)

### Framework Integration
- **React Integration** - Hooks, useEffect patterns (see skill.md)
- **Vue.js Integration** - Composition API and Options API (see skill.md)
- **Angular Integration** - Component lifecycle (see skill.md)
- **Next.js Integration** - App Router, Server Components (see skill.md)
- **Vanilla JavaScript** - No framework usage (see skill.md)

### Advanced Topics
- **Component Lifecycle** - Mount, unmount, cleanup patterns
- **Event Listeners** - React to session events
- **Session Management** - Programmatic control
- **Quality Statistics** - Monitor connection quality
- **Custom Themes** - Theme customization
- **Virtual Backgrounds** - Custom background images

## 📚 API Reference

Complete API documentation:

- **Core Methods** (see skill.md)
  - `joinSession()` - Start a video session
  - `closeSession()` - End session and remove UI
  - `destroy()` - Clean up UI Toolkit instance
  - `leaveSession()` - Leave without destroying UI

- **Component Methods** (see skill.md)
  - `showControlsComponent()` - Display control bar
  - `showChatComponent()` - Display chat panel
  - `showUsersComponent()` - Display participants list
  - `showSettingsComponent()` - Display settings panel
  - `hideAllComponents()` - Hide all components

- **Event Listeners** (see skill.md)
  - `onSessionJoined()` - Session joined successfully
  - `onSessionClosed()` - Session ended
  - `onSessionDestroyed()` - UI Toolkit destroyed
  - `onViewTypeChange()` - View mode changed
  - `on()` - Subscribe to Video SDK events
  - `off()` - Unsubscribe from events

- **Information Methods** (see skill.md)
  - `getSessionInfo()` - Get session details
  - `getCurrentUserInfo()` - Get current user
  - `getAllUser()` - Get all participants
  - `getClient()` - Get underlying Video SDK client
  - `version()` - Get version info

- **Control Methods** (see skill.md)
  - `changeViewType()` - Switch view mode
  - `mirrorVideo()` - Mirror self video
  - `isSupportCustomLayout()` - Check device support

- **Statistics Methods** (see skill.md)
  - `subscribeAudioStatisticData()` - Audio quality stats
  - `subscribeVideoStatisticData()` - Video quality stats
  - `subscribeShareStatisticData()` - Share quality stats

## 🔧 Configuration

- **Feature Configuration** (see skill.md)
  - `featuresOptions` structure
  - Audio/Video options
  - Chat, Users, Settings
  - Virtual Background
  - Recording, Captions (paid features)
  - Theme customization
  - View modes

- **Session Configuration** (see skill.md)
  - Required: `videoSDKJWT`, `sessionName`, `userName`
  - Optional: `sessionPasscode`, `sessionIdleTimeoutMins`
  - Debug mode
  - Web endpoint
  - Language settings

## ⚠️ Troubleshooting

### Common Issues
- React 18 peer dependency error
- JWT token invalid
- CSS not loading
- Components not showing
- Session join failures

See: **[troubleshooting/common-issues.md](troubleshooting/common-issues.md)**

### Framework-Specific Issues
- React: SSR, hydration, cleanup
- Vue: Reactivity, lifecycle
- Angular: Module imports, AOT
- Next.js: App Router, basePath

### Session Issues
- Authentication failures
- Connection problems
- Video/audio not working
- Screen share issues

## 📦 Sample Applications

**Official Repositories**:

| Framework | Repository | Key Features |
|-----------|------------|--------------|
| React | [videosdk-zoom-ui-toolkit-react-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-react-sample) | Hooks, TypeScript |
| Vue.js | [videosdk-zoom-ui-toolkit-vuejs-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-vuejs-sample) | Composition API |
| Angular | [videosdk-zoom-ui-toolkit-angular-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-angular-sample) | Services, Guards |
| JavaScript | [videosdk-zoom-ui-toolkit-javascript-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-javascript-sample) | Vanilla JS |
| Auth Endpoint | [videosdk-auth-endpoint-sample](https://github.com/zoom/videosdk-auth-endpoint-sample) | Node.js JWT |

## 🌐 External Resources

- **Official Documentation**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/
- **API Reference**: https://marketplacefront.zoom.us/sdk/uitoolkit/web/
- **NPM Package**: https://www.npmjs.com/package/@zoom/videosdk-zoom-ui-toolkit
- **Marketplace**: https://marketplace.zoom.us/
- **Developer Forum**: https://devforum.zoom.us/
- **Live Demo**: https://sdk.zoom.com/videosdk-uitoolkit
- **Changelog**: https://developers.zoom.us/changelog/ui-toolkit/web/

## 🎓 Learning Path

### Beginner
1. Read [SKILL.md](SKILL.md) overview
2. Follow Quick Start - Composite
3. Generate JWT on server
4. Join your first session
5. Explore available features

### Intermediate
1. Try Component Mode
2. Add event listeners
3. Customize theme
4. Add virtual backgrounds
5. Integrate with your framework

### Advanced
1. Access underlying Video SDK
2. Subscribe to quality statistics
3. Handle all edge cases
4. Implement custom layouts
5. Build production-ready app

## 📋 Quick Reference Card

### Minimal Working Example

```javascript
import uitoolkit from "@zoom/videosdk-zoom-ui-toolkit";
import "@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css";

const config = {
  videoSDKJWT: "YOUR_JWT",
  sessionName: "test-session",
  userName: "User",
  featuresOptions: {
    video: { enable: true },
    audio: { enable: true }
  }
};

uitoolkit.joinSession(document.getElementById("container"), config);
uitoolkit.onSessionJoined(() => console.log("Joined"));
uitoolkit.onSessionClosed(() => uitoolkit.destroy());
```

### Must-Remember Rules

1. ✅ **Always** generate JWT server-side
2. ✅ **Always** call `destroy()` on cleanup
3. ✅ **Always** use React 18 (not 17/19)
4. ✅ **Always** import CSS file
5. ❌ **Never** expose SDK secret client-side
6. ❌ **Never** skip `onSessionClosed` cleanup
7. ❌ **Never** call components before `joinSession`

## 📞 Support

- **Developer Forum**: https://devforum.zoom.us/
- **Developer Support**: https://developers.zoom.us/support/
- **Premier Support**: https://explore.zoom.us/en/support-plans/developer/

---

**Navigation**: [← Back to SKILL.md](SKILL.md)

## Environment Variables

- See [references/environment-variables.md](references/environment-variables.md) for standardized `.env` keys and where to find each value.

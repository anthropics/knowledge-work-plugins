# Pre-built Video UI with UI Toolkit

Build video conferencing apps in minutes using Zoom's ready-made UI components.

## Use Case

You need to add video conferencing to your web application quickly without building custom UI from scratch. The Zoom Video SDK UI Toolkit provides a complete, production-ready video interface that works across frameworks.

## When to Use UI Toolkit

- ✅ Need video conferencing fast (hours, not weeks)
- ✅ Want Zoom-like UI consistency
- ✅ Don't have resources to build custom video UI
- ✅ Need standard features (chat, share, participants, settings)
- ✅ Want framework-agnostic solution (React, Vue, Angular, vanilla JS)

## When NOT to Use (Use Raw Video SDK Instead)

- ❌ Need complete custom UI control
- ❌ Building non-standard video experiences  
- ❌ Need access to raw video/audio data for processing
- ❌ Want custom rendering pipeline

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Your Web Application                                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Your Frontend (React/Vue/Angular/Vanilla JS)        │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │  Zoom UI Toolkit                              │    │  │
│  │  │  ┌────────────────────────────────────────┐  │    │  │
│  │  │  │  Pre-built UI Components               │  │    │  │
│  │  │  │  • Video Grid/Gallery                  │  │    │  │
│  │  │  │  • Control Bar                         │  │    │  │
│  │  │  │  • Chat Panel                          │  │    │  │
│  │  │  │  • Participants List                   │  │    │  │
│  │  │  │  • Settings Panel                      │  │    │  │
│  │  │  └────────────────────────────────────────┘  │    │  │
│  │  │                                                │    │  │
│  │  │  ┌────────────────────────────────────────┐  │    │  │
│  │  │  │  Zoom Video SDK (Underlying Engine)   │  │    │  │
│  │  │  │  • WebRTC                              │  │    │  │
│  │  │  │  • Media Processing                    │  │    │  │
│  │  │  │  • Session Management                  │  │    │  │
│  │  │  └────────────────────────────────────────┘  │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Your Backend (Node.js/Python/Any)                   │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  JWT Generation Endpoint                        │  │  │
│  │  │  • Uses Video SDK Secret (NEVER expose!)        │  │  │
│  │  │  • Generates session tokens                     │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Implementation

### 1. Install UI Toolkit

```bash
npm install @zoom/videosdk-zoom-ui-toolkit
npm install react@18 react-dom@18  # Required peer dependency
```

### 2. Server-Side JWT Generation (Required)

```typescript
// Backend: api/zoom-token/route.ts
import { KJUR } from 'jsrsasign';

export async function POST(request) {
  const { sessionName, role, userName } = await request.json();
  
  const payload = {
    app_key: process.env.ZOOM_VIDEO_SDK_KEY,
    role_type: role, // 0 = participant, 1 = host
    tpc: sessionName,
    version: 1,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 7200 // 2 hours
  };
  
  const token = KJUR.jws.JWS.sign(
    'HS256',
    JSON.stringify({ alg: 'HS256', typ: 'JWT' }),
    JSON.stringify(payload),
    process.env.ZOOM_VIDEO_SDK_SECRET
  );
  
  return Response.json({ signature: token });
}
```

### 3. Frontend Integration (React Example)

```typescript
'use client';
import { useEffect, useRef } from 'react';

export default function VideoSession({ sessionName, userName }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const uitoolkitRef = useRef<any>(null);

  useEffect(() => {
    let mounted = true;

    const init = async () => {
      // Fetch JWT from your backend
      const response = await fetch('/api/zoom-token', {
        method: 'POST',
        body: JSON.stringify({ sessionName, userName, role: 1 })
      });
      const { signature } = await response.json();

      // Import UI Toolkit
      const uitoolkitModule = await import('@zoom/videosdk-zoom-ui-toolkit');
      const uitoolkit = uitoolkitModule.default;
      uitoolkitRef.current = uitoolkit;
      
      // @ts-ignore
      await import('@zoom/videosdk-ui-toolkit/dist/videosdk-zoom-ui-toolkit.css');

      if (!mounted || !containerRef.current) return;

      // Configure session
      const config = {
        videoSDKJWT: signature,
        sessionName,
        userName,
        featuresOptions: {
          video: { enable: true },
          audio: { enable: true },
          share: { enable: true },
          chat: { enable: true },
          users: { enable: true },
          settings: { enable: true }
        }
      };

      // Join session
      uitoolkit.joinSession(containerRef.current, config);
      
      uitoolkit.onSessionJoined(() => console.log('Joined'));
      uitoolkit.onSessionClosed(() => console.log('Closed'));
    };

    init();

    return () => {
      mounted = false;
      if (uitoolkitRef.current && containerRef.current) {
        uitoolkitRef.current.closeSession(containerRef.current);
        uitoolkitRef.current.destroy();
      }
    };
  }, [sessionName, userName]);

  return <div ref={containerRef} style={{ width: '100%', height: '100vh' }} />;
}
```

That's it! You now have a fully functional video conferencing UI.

## Features You Get Out-of-the-Box

| Feature | Description |
|---------|-------------|
| **Video Grid** | Gallery and speaker views with automatic switching |
| **Audio Controls** | Mute/unmute, device selection, background noise suppression |
| **Video Controls** | Camera on/off, device selection, virtual backgrounds |
| **Screen Share** | Share screen/window with annotation support |
| **Chat** | In-session messaging with emoji support |
| **Participants** | User list with host controls (mute, remove, etc.) |
| **Settings** | Device management, quality statistics, theme selection |
| **Reactions** | Emoji reactions and raised hand |

## Customization Options

### Choose Which Features to Enable

```javascript
const config = {
  // ... other config
  featuresOptions: {
    preview: { enable: true },        // Pre-join device check
    video: { enable: true },
    audio: { enable: true },
    share: { enable: true },
    chat: { enable: true },
    users: { enable: true },
    settings: { enable: true },
    virtualBackground: {
      enable: true,
      virtualBackgrounds: [
        { url: '/bg1.jpg', displayName: 'Office' }
      ]
    },
    recording: { enable: false },     // Requires paid plan
    caption: { enable: false },       // Requires paid plan
    theme: {
      enable: true,
      defaultTheme: 'dark'            // 'light' | 'dark' | 'blue' | 'green'
    }
  }
};
```

### Two UI Modes

**Composite Mode** (Full UI - Easiest):
```javascript
// Single call gets you complete video UI
uitoolkit.joinSession(container, config);
```

**Component Mode** (Custom Layouts):
```javascript
// Show individual pieces where you want
uitoolkit.joinSession(container, config);
uitoolkit.showControlsComponent(controlsContainer);
uitoolkit.showChatComponent(chatContainer);
uitoolkit.showUsersComponent(usersContainer);
```

## Related Use Cases

- **[Custom Video Experiences](custom-video.md)** - When you need raw Video SDK for custom UI
- **[Meeting SDK Integration](embed-meetings.md)** - For Zoom Meeting embedding
- **[Real-Time Media Streams](real-time-media-streams.md)** - When you need raw media access

## Related Skills

- **[zoom-ui-toolkit](../../ui-toolkit/SKILL.md)** - Complete UI Toolkit documentation
- **[zoom-video-sdk](../../video-sdk/web/SKILL.md)** - Raw Video SDK (when UI Toolkit isn't enough)
- **[zoom-general](../SKILL.md)** - General Zoom platform knowledge

## Security Best Practices

1. **NEVER expose Video SDK Secret** in frontend code
2. **ALWAYS generate JWT server-side** using the secret
3. **Set appropriate JWT expiration** (1-2 hours typical)
4. **Validate user identity** before generating tokens
5. **Use HTTPS** for production deployments

## Production Checklist

- [ ] JWT generation is server-side only
- [ ] Proper cleanup on component unmount (`uitoolkit.destroy()`)
- [ ] Error handling for network issues
- [ ] Loading states during JWT fetch
- [ ] Testing across browsers (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsive testing (if targeting mobile)
- [ ] HTTPS enabled for production
- [ ] Environment variables for SDK credentials

## Development Time Comparison

| Approach | Development Time | Effort |
|----------|-----------------|--------|
| **UI Toolkit** | 1-3 days | Low - Drop-in solution |
| **Raw Video SDK** | 2-4 weeks | High - Build all UI |
| **Meeting SDK** | 3-5 days | Medium - Embed Zoom Meetings |

## When You Outgrow UI Toolkit

If you need more customization than UI Toolkit provides:

1. **Access underlying SDK**:
   ```javascript
   const client = uitoolkit.getClient(); // Get raw Video SDK client
   uitoolkit.on('user-added', (payload) => {
     // Listen to 80+ raw SDK events
   });
   ```

2. **Migrate to raw Video SDK**:
   - Keep your JWT generation
   - Replace UI Toolkit with custom UI
   - Use same session/token architecture
   - See [zoom-video-sdk](../../video-sdk/web/SKILL.md) for migration guide

## Common Gotchas

1. **React 18 Required**: UI Toolkit needs React 18 specifically (not 17 or 19)
2. **CSS Import**: Must import `videosdk-zoom-ui-toolkit.css` or UI will be unstyled
3. **Cleanup Required**: Always call `destroy()` on unmount to prevent memory leaks
4. **JWT Security**: NEVER put SDK secret in frontend - always use server endpoint

## Resources

- **Skill**: [zoom-ui-toolkit](../../ui-toolkit/SKILL.md)
- **Live Demo**: https://sdk.zoom.com/videosdk-uitoolkit
- **Official Docs**: https://developers.zoom.us/docs/video-sdk/web/ui-toolkit/
- **NPM Package**: https://www.npmjs.com/package/@zoom/videosdk-zoom-ui-toolkit
- **Sample Apps**:
  - React: https://github.com/zoom/videosdk-zoom-ui-toolkit-react-sample
  - Vue.js: https://github.com/zoom/videosdk-zoom-ui-toolkit-vuejs-sample
  - Angular: https://github.com/zoom/videosdk-zoom-ui-toolkit-angular-sample
  - JavaScript: https://github.com/zoom/videosdk-zoom-ui-toolkit-javascript-sample

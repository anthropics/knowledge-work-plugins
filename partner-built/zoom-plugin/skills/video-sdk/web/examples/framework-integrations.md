# Framework Integrations

Official quickstarts and patterns for popular frameworks.

## Next.js (App Router)

Official repo: [zoom/videosdk-nextjs-quickstart](https://github.com/zoom/videosdk-nextjs-quickstart)

### Project Structure

```
app/
├── api/
│   └── signature/
│       └── route.ts      # Server-side JWT generation
├── video/
│   └── page.tsx          # Video call component
├── layout.tsx
└── page.tsx

.env.local
├── ZOOM_SDK_KEY="your-key"
└── ZOOM_SDK_SECRET="your-secret"
```

### Server-Side JWT Generation (App Router)

```typescript
// app/api/signature/route.ts
import { NextRequest, NextResponse } from 'next/server';
import KJUR from 'jsrsasign';

export async function POST(request: NextRequest) {
  const { topic, role } = await request.json();
  
  const iat = Math.floor(Date.now() / 1000) - 30;
  const exp = iat + 60 * 60 * 2; // 2 hours
  
  const header = { alg: 'HS256', typ: 'JWT' };
  const payload = {
    app_key: process.env.ZOOM_SDK_KEY,
    tpc: topic,
    role_type: role || 1,
    version: 1,
    iat,
    exp,
  };
  
  const signature = KJUR.jws.JWS.sign(
    'HS256',
    JSON.stringify(header),
    JSON.stringify(payload),
    process.env.ZOOM_SDK_SECRET!
  );
  
  return NextResponse.json({ signature });
}
```

### Client Component (App Router)

```tsx
// app/video/page.tsx
'use client';

import { useEffect, useState, useRef } from 'react';
import ZoomVideo, { VideoClient, Stream, VideoQuality } from '@zoom/videosdk';

export default function VideoPage() {
  const [client, setClient] = useState<typeof VideoClient | null>(null);
  const [stream, setStream] = useState<typeof Stream | null>(null);
  const [isJoined, setIsJoined] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const init = async () => {
      const zmClient = ZoomVideo.createClient();
      await zmClient.init('en-US', 'Global', { patchJsMedia: true });
      setClient(zmClient);
    };
    init();

    return () => {
      ZoomVideo.destroyClient();
    };
  }, []);

  const joinSession = async (topic: string, userName: string) => {
    if (!client) return;

    // Get signature from API route
    const res = await fetch('/api/signature', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, role: 1 }),
    });
    const { signature } = await res.json();

    // Join session
    await client.join(topic, signature, userName);
    const mediaStream = client.getMediaStream();
    setStream(mediaStream);
    setIsJoined(true);
  };

  const startVideo = async () => {
    if (!stream || !client) return;
    await stream.startVideo();
    const currentUser = client.getCurrentUserInfo();
    const element = await stream.attachVideo(
      currentUser.userId,
      VideoQuality.Video_360P
    );
    containerRef.current?.appendChild(element);
  };

  return (
    <div>
      {!isJoined ? (
        <button onClick={() => joinSession('my-topic', 'User')}>
          Join Session
        </button>
      ) : (
        <>
          <div ref={containerRef} />
          <button onClick={startVideo}>Start Video</button>
        </>
      )}
    </div>
  );
}
```

### SSR Considerations

**CRITICAL**: The Video SDK uses WebAssembly and must run client-side only.

```tsx
// ❌ WRONG: Importing at top level causes SSR issues
import ZoomVideo from '@zoom/videosdk';

// ✅ CORRECT: Dynamic import or use 'use client' directive
'use client';

// Or use dynamic import
const ZoomVideo = dynamic(() => import('@zoom/videosdk'), { ssr: false });
```

---

## Next.js (Pages Router)

Branch: [pages-router](https://github.com/zoom/videosdk-nextjs-quickstart/tree/pages-router)

### Server-Side JWT (Pages Router)

```typescript
// pages/api/signature.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import KJUR from 'jsrsasign';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { topic, role } = req.body;
  
  const iat = Math.floor(Date.now() / 1000) - 30;
  const exp = iat + 60 * 60 * 2;
  
  const header = { alg: 'HS256', typ: 'JWT' };
  const payload = {
    app_key: process.env.ZOOM_SDK_KEY,
    tpc: topic,
    role_type: role || 1,
    version: 1,
    iat,
    exp,
  };
  
  const signature = KJUR.jws.JWS.sign(
    'HS256',
    JSON.stringify(header),
    JSON.stringify(payload),
    process.env.ZOOM_SDK_SECRET!
  );
  
  res.status(200).json({ signature });
}
```

### Client Component (Pages Router)

```tsx
// pages/video.tsx
import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

// Dynamic import to prevent SSR issues
const VideoComponent = dynamic(() => import('../components/Video'), {
  ssr: false,
});

export default function VideoPage() {
  return <VideoComponent />;
}
```

---

## Vue 3 / Nuxt 3

Official repo: [zoom/videosdk-vue-nuxt-quickstart](https://github.com/zoom/videosdk-vue-nuxt-quickstart)

### Composition API Pattern

```vue
<!-- components/VideoSession.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import ZoomVideo, { VideoClient, Stream, VideoQuality } from '@zoom/videosdk';

const props = defineProps<{
  topic: string;
  signature: string;
  userName: string;
}>();

const client = ref<typeof VideoClient | null>(null);
const stream = ref<typeof Stream | null>(null);
const isJoined = ref(false);
const videoContainer = ref<HTMLDivElement | null>(null);

// Reactive participants list
const participants = ref<any[]>([]);

onMounted(async () => {
  // Initialize client
  const zmClient = ZoomVideo.createClient();
  await zmClient.init('en-US', 'Global', { patchJsMedia: true });
  client.value = zmClient;

  // Set up event listeners
  zmClient.on('user-added', updateParticipants);
  zmClient.on('user-removed', updateParticipants);
  zmClient.on('user-updated', updateParticipants);
  zmClient.on('peer-video-state-change', handleVideoChange);
});

onUnmounted(async () => {
  if (client.value) {
    await client.value.leave();
    ZoomVideo.destroyClient();
  }
});

const updateParticipants = () => {
  if (client.value) {
    participants.value = client.value.getAllUser();
  }
};

const handleVideoChange = async (payload: { action: string; userId: number }) => {
  if (!stream.value || !videoContainer.value) return;

  if (payload.action === 'Start') {
    const element = await stream.value.attachVideo(
      payload.userId,
      VideoQuality.Video_360P
    );
    videoContainer.value.appendChild(element);
  } else {
    await stream.value.detachVideo(payload.userId);
  }
};

const joinSession = async () => {
  if (!client.value) return;

  await client.value.join(props.topic, props.signature, props.userName);
  stream.value = client.value.getMediaStream();
  isJoined.value = true;
  updateParticipants();
};

const startVideo = async () => {
  if (!stream.value || !client.value) return;
  await stream.value.startVideo();
  
  const currentUser = client.value.getCurrentUserInfo();
  const element = await stream.value.attachVideo(
    currentUser.userId,
    VideoQuality.Video_360P
  );
  videoContainer.value?.appendChild(element);
};

const toggleMute = async () => {
  if (!stream.value) return;
  const muted = stream.value.isAudioMuted();
  if (muted) {
    await stream.value.unmuteAudio();
  } else {
    await stream.value.muteAudio();
  }
};
</script>

<template>
  <div class="video-session">
    <div v-if="!isJoined">
      <button @click="joinSession">Join Session</button>
    </div>

    <div v-else>
      <div ref="videoContainer" class="video-container" />

      <div class="participants">
        <div v-for="p in participants" :key="p.userId">
          {{ p.displayName }} - {{ p.bVideoOn ? 'Video On' : 'Video Off' }}
        </div>
      </div>

      <div class="controls">
        <button @click="startVideo">Start Video</button>
        <button @click="toggleMute">Toggle Mute</button>
      </div>
    </div>
  </div>
</template>
```

### Nuxt 3 Plugin (Client-Only)

```typescript
// plugins/videosdk.client.ts
import ZoomVideo from '@zoom/videosdk';

export default defineNuxtPlugin(() => {
  return {
    provide: {
      zoomVideo: ZoomVideo,
    },
  };
});
```

```vue
<!-- pages/video.vue -->
<script setup>
const { $zoomVideo } = useNuxtApp();

// Use $zoomVideo.createClient() etc.
</script>
```

---

## Zoom For Government (ZFG)

If using Zoom For Government, you need a separate SDK key from [marketplace.zoomgov.com](https://marketplace.zoomgov.com/).

### Option 1: ZFG-Specific Package Version

```json
{
  "dependencies": {
    "@zoom/videosdk": "1.11.0-zfg"
  }
}
```

```javascript
client.init('en-US', 'Global');
```

### Option 2: Custom WebEndpoint

```javascript
client.init('en-US', 'https://source.zoomgov.com/videosdk/1.11.0/lib', {
  webEndpoint: 'www.zoomgov.com',
});
```

---

## Official Sample Repositories

| Framework | Repository | Branch |
|-----------|------------|--------|
| Vanilla JS/TS | [videosdk-web-sample](https://github.com/zoom/videosdk-web-sample) | master |
| React | [videosdk-react](https://github.com/zoom/videosdk-react) | main |
| Next.js (App) | [videosdk-nextjs-quickstart](https://github.com/zoom/videosdk-nextjs-quickstart) | app-router |
| Next.js (Pages) | [videosdk-nextjs-quickstart](https://github.com/zoom/videosdk-nextjs-quickstart) | pages-router |
| Vue/Nuxt | [videosdk-vue-nuxt-quickstart](https://github.com/zoom/videosdk-vue-nuxt-quickstart) | main |
| UI Toolkit (React) | [videosdk-zoom-ui-toolkit-react-sample](https://github.com/zoom/videosdk-zoom-ui-toolkit-react-sample) | main |
| Auth Endpoint | [videosdk-auth-endpoint-sample](https://github.com/zoom/videosdk-auth-endpoint-sample) | main |

---

## Common Patterns Across Frameworks

### 1. Client-Side Only

The SDK must run client-side. All frameworks need to handle this:

| Framework | Solution |
|-----------|----------|
| Next.js | `'use client'` or `dynamic(..., { ssr: false })` |
| Nuxt 3 | `.client.ts` plugin or `<ClientOnly>` |
| Vue SPA | No special handling needed |

### 2. Lifecycle Management

```typescript
// Always follow this order:
const client = ZoomVideo.createClient();
await client.init(...);
await client.join(...);
const stream = client.getMediaStream(); // ONLY after join()

// Cleanup on unmount
await client.leave();
ZoomVideo.destroyClient();
```

### 3. Event-Driven Video Rendering

```typescript
// All frameworks should use this pattern
client.on('peer-video-state-change', async ({ action, userId }) => {
  if (action === 'Start') {
    const el = await stream.attachVideo(userId, VideoQuality.Video_360P);
    container.appendChild(el);
  } else {
    await stream.detachVideo(userId);
  }
});
```

## Related Documentation

- [React Hooks](react-hooks.md) - @zoom/videosdk-react
- [Session Join](session-join-pattern.md) - Core SDK patterns
- [Video Rendering](video-rendering.md) - attachVideo() details

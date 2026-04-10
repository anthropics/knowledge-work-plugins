# Framework-Specific Messenger Installation Guides

Detailed installation instructions for integrating the Intercom Messenger with JWT-based identity verification in popular frontend frameworks.

All examples assume a backend endpoint at `/api/intercom-jwt` that returns `{ "token": "<signed-jwt>" }` for the authenticated user. See the main SKILL.md for backend implementation examples.

## React via `@intercom/messenger-js-sdk`

The official Intercom React SDK provides a clean integration.

### Installation

```bash
npm install @intercom/messenger-js-sdk
# or
yarn add @intercom/messenger-js-sdk
```

### Secure Setup with JWT

Create a provider component that fetches the JWT and boots the Messenger:

```tsx
// components/IntercomProvider.tsx
import { useEffect } from 'react';
import Intercom, { shutdown, update } from '@intercom/messenger-js-sdk';
import { useLocation } from 'react-router-dom';

interface IntercomProviderProps {
  appId: string;
  isAuthenticated: boolean;
  children: React.ReactNode;
}

export function IntercomProvider({ appId, isAuthenticated, children }: IntercomProviderProps) {
  const location = useLocation();

  useEffect(() => {
    if (isAuthenticated) {
      // Fetch JWT from backend and boot with identity verification
      fetch('/api/intercom-jwt', { credentials: 'include' })
        .then(res => res.json())
        .then(({ token }) => {
          Intercom({
            app_id: appId,
            intercom_user_jwt: token,
          });
        });
    } else {
      // Anonymous visitor — no JWT needed
      Intercom({
        app_id: appId,
      });
    }

    return () => {
      shutdown();
    };
  }, [appId, isAuthenticated]);

  // Update Messenger on route changes
  useEffect(() => {
    update();
  }, [location]);

  return <>{children}</>;
}
```

Use in your app root:

```tsx
// App.tsx
import { IntercomProvider } from './components/IntercomProvider';

function App() {
  const { isAuthenticated } = useAuth(); // Your auth hook

  return (
    <IntercomProvider appId="YOUR_WORKSPACE_ID" isAuthenticated={isAuthenticated}>
      {/* Your app content */}
    </IntercomProvider>
  );
}
```

### Shutdown on Logout

```tsx
import { shutdown } from '@intercom/messenger-js-sdk';

function LogoutButton() {
  const handleLogout = () => {
    shutdown();          // Clear Intercom session first
    // ... your logout logic
  };

  return <button onClick={handleLogout}>Log out</button>;
}
```

---

## Next.js with `next/script`

For Next.js applications, use the `next/script` component for optimized script loading.

### App Router (Next.js 13+)

Create a client component that fetches the JWT and boots the Messenger:

```tsx
// components/IntercomMessenger.tsx
'use client';

import Script from 'next/script';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

interface IntercomMessengerProps {
  appId: string;
  isAuthenticated: boolean;
}

export function IntercomMessenger({ appId, isAuthenticated }: IntercomMessengerProps) {
  const pathname = usePathname();
  const [ready, setReady] = useState(false);

  // Boot Messenger with JWT once script is loaded
  useEffect(() => {
    if (!ready) return;

    if (isAuthenticated) {
      fetch('/api/intercom-jwt', { credentials: 'include' })
        .then(res => res.json())
        .then(({ token }) => {
          window.Intercom('boot', {
            app_id: appId,
            intercom_user_jwt: token,
          });
        });
    } else {
      window.Intercom('boot', {
        app_id: appId,
      });
    }
  }, [ready, appId, isAuthenticated]);

  // Update Intercom on route changes
  useEffect(() => {
    if (window.Intercom) {
      window.Intercom('update');
    }
  }, [pathname]);

  return (
    <Script
      id="intercom-widget"
      strategy="lazyOnload"
      src={`https://widget.intercom.io/widget/${appId}`}
      onLoad={() => setReady(true)}
    />
  );
}
```

Add to your root layout:

```tsx
// app/layout.tsx
import { IntercomMessenger } from '@/components/IntercomMessenger';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const isAuthenticated = /* your auth check */;

  return (
    <html lang="en">
      <body>
        {children}
        <IntercomMessenger appId="YOUR_WORKSPACE_ID" isAuthenticated={isAuthenticated} />
      </body>
    </html>
  );
}
```

### Pages Router

For the Pages Router, add the Messenger in `_app.tsx`:

```tsx
// pages/_app.tsx
import Script from 'next/script';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

export default function App({ Component, pageProps }) {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const { user } = useAuth(); // Your auth hook

  // Boot with JWT when script loads or auth changes
  useEffect(() => {
    if (!ready) return;

    if (user) {
      fetch('/api/intercom-jwt', { credentials: 'include' })
        .then(res => res.json())
        .then(({ token }) => {
          window.Intercom('boot', {
            app_id: 'YOUR_WORKSPACE_ID',
            intercom_user_jwt: token,
          });
        });
    } else {
      window.Intercom('boot', {
        app_id: 'YOUR_WORKSPACE_ID',
      });
    }
  }, [ready, user]);

  // Update on route changes
  useEffect(() => {
    const handleRouteChange = () => {
      if (window.Intercom) {
        window.Intercom('update');
      }
    };
    router.events.on('routeChangeComplete', handleRouteChange);
    return () => router.events.off('routeChangeComplete', handleRouteChange);
  }, [router]);

  return (
    <>
      <Component {...pageProps} />
      <Script
        id="intercom-widget"
        strategy="lazyOnload"
        src="https://widget.intercom.io/widget/YOUR_WORKSPACE_ID"
        onLoad={() => setReady(true)}
      />
    </>
  );
}
```

---

## Vue.js Integration

### Vue 3 with Composition API

Create a composable that handles JWT fetching and Messenger lifecycle:

```typescript
// composables/useIntercom.ts
import { onMounted, onUnmounted, watch, ref } from 'vue';
import { useRoute } from 'vue-router';

export function useIntercom(appId: string, isAuthenticated: () => boolean) {
  const route = useRoute();
  const loaded = ref(false);

  onMounted(() => {
    // Load the Intercom widget script
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://widget.intercom.io/widget/${appId}`;
    script.onload = () => {
      loaded.value = true;
      bootMessenger();
    };
    document.head.appendChild(script);
  });

  function bootMessenger() {
    if (!loaded.value) return;

    if (isAuthenticated()) {
      fetch('/api/intercom-jwt', { credentials: 'include' })
        .then(res => res.json())
        .then(({ token }) => {
          window.Intercom('boot', {
            app_id: appId,
            intercom_user_jwt: token,
          });
        });
    } else {
      window.Intercom('boot', {
        app_id: appId,
      });
    }
  }

  // Update on route changes
  watch(
    () => route.path,
    () => {
      if (window.Intercom) {
        window.Intercom('update');
      }
    }
  );

  onUnmounted(() => {
    if (window.Intercom) {
      window.Intercom('shutdown');
    }
  });

  return { bootMessenger };
}
```

Use in your App component:

```vue
<!-- App.vue -->
<script setup lang="ts">
import { useIntercom } from './composables/useIntercom';
import { useAuth } from './composables/useAuth';

const { isAuthenticated } = useAuth();
useIntercom('YOUR_WORKSPACE_ID', () => isAuthenticated.value);
</script>

<template>
  <RouterView />
</template>
```

### Vue Router Navigation Guard

Alternatively, add route updates globally via a navigation guard:

```typescript
// router/index.ts
const router = createRouter({ /* ... */ });

router.afterEach(() => {
  if (window.Intercom) {
    window.Intercom('update');
  }
});
```

---

## Angular

Angular uses the same `@intercom/messenger-js-sdk` NPM package. Create a service to handle JWT fetching, Messenger lifecycle, and route change updates.

### Installation

```bash
npm install @intercom/messenger-js-sdk
# or
yarn add @intercom/messenger-js-sdk
```

### Intercom Service

```typescript
// services/intercom.service.ts
import { Injectable, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import Intercom, { shutdown, update } from '@intercom/messenger-js-sdk';
import { filter, Subscription } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class IntercomService implements OnDestroy {
  private routerSub: Subscription;

  constructor(private router: Router) {
    this.routerSub = this.router.events
      .pipe(filter(e => e instanceof NavigationEnd))
      .subscribe(() => update());
  }

  boot(appId: string, isAuthenticated: boolean) {
    if (isAuthenticated) {
      fetch('/api/intercom-jwt', { credentials: 'include' })
        .then(res => res.json())
        .then(({ token }) => {
          Intercom({
            app_id: appId,
            intercom_user_jwt: token,
          });
        });
    } else {
      Intercom({ app_id: appId });
    }
  }

  shutdown() {
    shutdown();
  }

  ngOnDestroy() {
    this.routerSub.unsubscribe();
  }
}
```

### App Component

```typescript
// app.component.ts
import { Component, OnInit } from '@angular/core';
import { IntercomService } from './services/intercom.service';
import { AuthService } from './services/auth.service';

@Component({ selector: 'app-root', template: '<router-outlet />' })
export class AppComponent implements OnInit {
  constructor(private intercom: IntercomService, private auth: AuthService) {}

  ngOnInit() {
    this.intercom.boot('YOUR_WORKSPACE_ID', this.auth.isAuthenticated());
  }
}
```

### Shutdown on Logout

```typescript
import { IntercomService } from './services/intercom.service';

export class LogoutComponent {
  constructor(private intercom: IntercomService) {}

  logout() {
    this.intercom.shutdown(); // Clear Intercom session first
    // ... your logout logic
  }
}
```

---

## Ember.js

Ember also uses the `@intercom/messenger-js-sdk` NPM package. Use an instance initializer to subscribe to route changes and a service to manage the Messenger lifecycle.

### Installation

```bash
npm install @intercom/messenger-js-sdk
# or
yarn add @intercom/messenger-js-sdk
```

### Instance Initializer

Register a route change listener that calls `update()` on every transition:

```javascript
// app/instance-initializers/intercom.js
import { update } from '@intercom/messenger-js-sdk';

export function initialize(appInstance) {
  const router = appInstance.lookup('service:router');
  router.on('routeDidChange', () => update());
}

export default { initialize };
```

### Intercom Service

```javascript
// app/services/intercom.js
import Service from '@ember/service';
import Intercom, { shutdown } from '@intercom/messenger-js-sdk';

export default class IntercomService extends Service {
  boot(appId, isAuthenticated) {
    if (isAuthenticated) {
      fetch('/api/intercom-jwt', { credentials: 'include' })
        .then(res => res.json())
        .then(({ token }) => {
          Intercom({
            app_id: appId,
            intercom_user_jwt: token,
          });
        });
    } else {
      Intercom({ app_id: appId });
    }
  }

  shutdown() {
    shutdown();
  }
}
```

### Boot in Application Route

```javascript
// app/routes/application.js
import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default class ApplicationRoute extends Route {
  @service intercom;
  @service session; // Your auth service

  afterModel() {
    this.intercom.boot('YOUR_WORKSPACE_ID', this.session.isAuthenticated);
  }
}
```

### Shutdown on Logout

```javascript
// In your logout action or route
this.intercom.shutdown(); // Clear Intercom session first
// ... your logout logic (e.g., this.session.invalidate())
```

---

## Single-Page App Considerations

Regardless of framework, all SPAs share these concerns:

### Script Loading
The Intercom widget script should load once and persist across route changes. Do not re-insert the `<script>` tag on navigation — use `Intercom('update')` instead.

### Identity Changes
When a user logs in or switches accounts within the SPA, shut down and re-boot with a fresh JWT:

```javascript
// 1. Shut down the current session
Intercom('shutdown');

// 2. Fetch a new JWT for the new user and boot
fetch('/api/intercom-jwt', { credentials: 'include' })
  .then(res => res.json())
  .then(({ token }) => {
    Intercom('boot', {
      app_id: 'YOUR_WORKSPACE_ID',
      intercom_user_jwt: token,
    });
  });
```

### Content Security Policy (CSP)
If the application uses a strict CSP, add these directives:

```
script-src: https://widget.intercom.io https://js.intercomcdn.com
frame-src: https://intercom-sheets.com https://www.intercom-reporting.com
connect-src: https://api-iam.intercom.io https://nexus-websocket-a.intercom.io wss://nexus-websocket-a.intercom.io
img-src: https://static.intercomassets.com https://downloads.intercomcdn.com
font-src: https://js.intercomcdn.com
media-src: https://js.intercomcdn.com
```

### TypeScript Declarations
For TypeScript projects, add type declarations for the global `Intercom` function:

```typescript
// types/intercom.d.ts
interface IntercomSettings {
  api_base?: string;
  app_id: string;
  intercom_user_jwt?: string;
  name?: string;
  email?: string;
  user_id?: string;
  created_at?: number;
  session_duration?: number;
  [key: string]: unknown;
}

interface Window {
  Intercom: (command: string, ...args: unknown[]) => void;
  intercomSettings: IntercomSettings;
}
```

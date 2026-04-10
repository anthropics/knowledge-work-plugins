---
title: Angular & Sanity Integration Rules
description: Integration guide for Angular, including @sanity/client setup, data fetching with signals and resource API, Portable Text rendering, and image optimization.
---

# Angular & Sanity Integration Rules

Jump to the section that matches your Angular version or integration task instead of reading this guide straight through.

## Table of Contents

- Setup and configuration
- Client setup (service pattern)
- Data fetching patterns
- Routing
- Portable Text rendering
- Image optimization
- Modern Angular features
- SSR and prerendering
- Visual Editing
- Error handling

## 1. Setup & Configuration

Use the official template `sanity-template-angular-clean` as a starting point. It provides a monorepo structure:

```
project/
├── angular-app/    # Angular 19+ frontend
└── studio/         # Sanity Studio
```

Install dependencies in the Angular app:

```bash
npm install @sanity/client @sanity/image-url @portabletext/to-html
```

Configure environment files for Sanity credentials:

```typescript
// environments/environment.ts
export const environment = {
  production: false,
  sanity: {
    projectId: 'your-project-id',
    dataset: 'production',
    apiVersion: '2025-05-01',
  },
}
```

```typescript
// environments/environment.production.ts
export const environment = {
  production: true,
  sanity: {
    projectId: 'your-project-id',
    dataset: 'production',
    apiVersion: '2025-05-01',
  },
}
```

> There is no Angular-specific Sanity SDK. Use `@sanity/client` directly, wrapped in an Angular service.

### TypeGen in a Monorepo

Sanity TypeGen generates TypeScript types from your schema and GROQ queries. In the Angular monorepo template, TypeGen runs from the Studio side but scans your Angular app's source files. Ensure `studio/sanity.cli.ts` points at the Angular app:

```typescript
// studio/sanity.cli.ts
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  typegen: {
    enabled: true,
    path: '../angular-app/src/**/*.ts',
    generates: '../angular-app/sanity.types.ts',
  },
})
```

The remaining defaults (`overloadClientMethods: true`, `schema: "schema.json"`) work as-is. Include the generated types file in `angular-app/tsconfig.json` (usually covered by `"include": ["src/**/*.ts", "sanity.types.ts"]`). See `typegen.md` for the full TypeGen workflow, git strategy, and configuration options.

## 2. Client Setup (Service Pattern)

Create an injectable service wrapping `@sanity/client` and `@sanity/image-url`:

```typescript
import { Injectable } from '@angular/core'
import { createClient, type ClientReturn, type QueryParams, type SanityClient } from '@sanity/client'
import imageUrlBuilder, { type ImageUrlBuilder } from '@sanity/image-url'
import type { SanityImageSource } from '@sanity/image-url/lib/types/types'
import { environment } from '../environments/environment'

@Injectable({ providedIn: 'root' })
export class SanityService {
  private client: SanityClient
  private builder: ImageUrlBuilder

  constructor() {
    this.client = createClient({
      projectId: environment.sanity.projectId,
      dataset: environment.sanity.dataset,
      apiVersion: environment.sanity.apiVersion,
      useCdn: true,
    })
    this.builder = imageUrlBuilder(this.client)
  }

  // ClientReturn resolves TypeGen's declaration-merged overloads for defineQuery strings
  fetch<Query extends string>(query: Query, params?: QueryParams): Promise<ClientReturn<Query>> {
    return this.client.fetch(query, params)
  }

  getImageUrlBuilder(source: SanityImageSource) {
    return this.builder.image(source)
  }
}
```

For preview/draft content, create a second client instance with a token and `useCdn: false`. Never expose tokens in client-side bundles — use server-side rendering or a proxy endpoint for authenticated requests.

## 3. Data Fetching Patterns

### A. `resource` API (Angular 19+, Recommended)

The `resource` API works natively with promises and integrates with Angular signals:

```typescript
import { Component, input, resource, inject } from '@angular/core'
import { defineQuery } from 'groq'
import { SanityService } from '../sanity.service'

const POST_QUERY = defineQuery(`*[_type == "post" && slug.current == $slug][0]{
  title, body, mainImage, publishedAt
}`)

@Component({
  selector: 'app-post',
  standalone: true,
  template: `
    @if (post.value(); as p) {
      <h1>{{ p.title }}</h1>
      <time>{{ p.publishedAt | date }}</time>
    } @else if (post.isLoading()) {
      <p>Loading…</p>
    } @else if (post.error()) {
      <p>Error loading post</p>
    }
  `,
})
export default class PostComponent {
  slug = input.required<string>()
  private sanity = inject(SanityService)

  post = resource({
    params: () => ({ slug: this.slug() }),
    loader: ({ params }) => this.sanity.fetch(POST_QUERY, params),
  })
}
```

The `resource` automatically re-fetches when `slug` changes and exposes `value()`, `isLoading()`, and `error()` signals.

> **TypeGen:** Wrapping queries in `defineQuery` enables Sanity TypeGen to infer return types automatically — no manual type imports needed. See `typegen.md` for the full workflow.

### B. `rxResource` (Observable-based)

For teams using RxJS patterns or needing operators like `retry` and `debounceTime`:

```typescript
import { Component, input, inject } from '@angular/core'
import { rxResource } from '@angular/core/rxjs-interop'
import { defineQuery } from 'groq'
import { from } from 'rxjs'
import { SanityService } from '../sanity.service'

const POST_QUERY = defineQuery(`*[_type == "post" && slug.current == $slug][0]`)

@Component({ /* ... */ })
export default class PostComponent {
  slug = input.required<string>()
  private sanity = inject(SanityService)

  post = rxResource({
    params: () => ({ slug: this.slug() }),
    loader: ({ params }) => from(this.sanity.fetch(POST_QUERY, params)),
  })
}
```

### C. `toSignal` (Angular 17–18)

For apps not yet on Angular 19, convert observables to signals:

```typescript
import { Component, inject } from '@angular/core'
import { toSignal } from '@angular/core/rxjs-interop'
import { defineQuery } from 'groq'
import { from } from 'rxjs'
import { SanityService } from '../sanity.service'

const POSTS_QUERY = defineQuery(`*[_type == "post"] | order(publishedAt desc)`)

@Component({ /* ... */ })
export class HomeComponent {
  private sanity = inject(SanityService)
  posts = toSignal(from(this.sanity.fetch(POSTS_QUERY)), { initialValue: [] })
}
```

> **Note:** `toSignal` does not re-fetch on parameter changes. For dynamic queries, use `resource` or `rxResource`.

### Choosing a pattern

| Pattern | Angular Version | Reactivity | Best For |
|---|---|---|---|
| `resource` | 19+ | Signal-based, auto re-fetch | New projects, dynamic queries |
| `rxResource` | 19+ | RxJS + signals | Teams using RxJS operators |
| `toSignal` | 17+ | One-shot conversion | Static queries, legacy apps |

## 4. Routing

Use lazy-loaded routes with `withComponentInputBinding()` so route params bind directly to component inputs:

```typescript
// app.config.ts
import { provideRouter, withComponentInputBinding } from '@angular/router'
import { routes } from './app.routes'

export const appConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding()),
  ],
}
```

```typescript
// app.routes.ts
import { Routes } from '@angular/router'

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component'),
    pathMatch: 'full',
  },
  {
    path: 'post/:slug',
    loadComponent: () => import('./post/post.component'),
  },
]
```

With `withComponentInputBinding()`, the `:slug` route param is automatically bound to `slug = input.required<string>()` on the component — no need to inject `ActivatedRoute`.

## 5. Portable Text Rendering

### A. `@portabletext/to-html` with Angular Pipe (Recommended)

```typescript
import { Pipe, PipeTransform, inject } from '@angular/core'
import { toHTML, type PortableTextComponents } from '@portabletext/to-html'
import type { PortableTextBlock } from '@portabletext/types'
import { SanityService } from '../sanity.service'

@Pipe({ name: 'portableTextToHTML', standalone: true })
export class PortableTextToHTMLPipe implements PipeTransform {
  private sanity = inject(SanityService)

  private components: PortableTextComponents = {
    types: {
      image: ({ value }) => {
        const url = this.sanity.getImageUrlBuilder(value).width(800).auto('format').url()
        return `<img src="${url}" alt="${value.alt || ''}" loading="lazy" />`
      },
    },
    marks: {
      link: ({ children, value }) =>
        `<a href="${value.href}" rel="noopener noreferrer">${children}</a>`,
    },
  }

  transform(value: PortableTextBlock[] | undefined): string {
    if (!value) return ''
    return toHTML(value, { components: this.components })
  }
}
```

Usage in templates:

```html
<div [innerHTML]="post.body | portableTextToHTML"></div>
```

### B. `@limitless-angular/sanity` (Community, Component-based)

For full Angular component control over each block type, the community library `@limitless-angular/sanity` provides a component-based Portable Text renderer. This is useful when you need Angular-specific interactivity within rich text blocks.

See `portable-text.md` for Portable Text schema design and serialization rules.

## 6. Image Optimization

Create a pipe wrapping `@sanity/image-url`:

```typescript
import { Pipe, PipeTransform, inject } from '@angular/core'
import type { SanityImageSource } from '@sanity/image-url/lib/types/types'
import { SanityService } from '../sanity.service'

@Pipe({ name: 'sanityImage', standalone: true })
export class SanityImagePipe implements PipeTransform {
  private sanity = inject(SanityService)

  transform(value: SanityImageSource | undefined, width?: number): string | null {
    if (!value) return null
    const builder = this.sanity.getImageUrlBuilder(value)
    if (width) return builder.width(width).auto('format').url()
    return builder.auto('format').url()
  }
}
```

Combine with Angular's `NgOptimizedImage` for LCP images:

```html
<!-- Priority image with NgOptimizedImage -->
<img [ngSrc]="post.mainImage | sanityImage: 1200" width="1200" height="630" priority />

<!-- Lazy-loaded image -->
<img [src]="post.mainImage | sanityImage: 600" [alt]="post.mainImage.alt" loading="lazy" />
```

❌ **Bad:** Fetching full-size images without width constraints.

```html
<img [src]="post.mainImage | sanityImage" />
```

✅ **Good:** Specifying width and using `auto('format')` for WebP/AVIF delivery.

```html
<img [src]="post.mainImage | sanityImage: 800" loading="lazy" />
```

### LQIP with `NgOptimizedImage`

Sanity provides a base64 LQIP (Low Quality Image Placeholder) per image asset — but you must query it explicitly:

```groq
mainImage {
  // @sanity/image-url needs these to build URLs with hotspot/crop support
  asset,
  hotspot,
  crop,
  alt,
  // NgOptimizedImage needs these for placeholder and layout
  "lqip": asset->metadata.lqip,
  "width": asset->metadata.dimensions.width,
  "height": asset->metadata.dimensions.height
}
```

Feed the LQIP directly into `NgOptimizedImage`'s `placeholder` attribute:

```html
<img
  [ngSrc]="post.mainImage | sanityImage: 1200"
  [width]="post.mainImage.width"
  [height]="post.mainImage.height"
  [placeholder]="post.mainImage.lqip"
  [alt]="post.mainImage.alt"
  priority
/>
```

Angular applies a CSS blur to the LQIP and crossfades to the full image on load. No extra libraries needed.

> **Note:** LQIP strings are small (~200 bytes) so they're safe to inline in SSR HTML and `TransferState`. See `image.md` for the full image query patterns.

See `image.md` for image field schema patterns and hotspot/crop configuration.

## 7. Modern Angular Features

When building with Sanity, leverage these Angular 19+ features:

- **Standalone components** — Default in Angular 19. No `NgModule` boilerplate needed.
- **Signals and `resource`** — Preferred over RxJS for data fetching. Simpler, less boilerplate.
- **New control flow** — Use `@if`, `@for`, `@switch` with `@empty` for cleaner templates:

```html
@for (post of posts.value(); track post._id) {
  <app-post-card [post]="post" />
} @empty {
  <p>No posts found.</p>
}
```

- **`@defer` blocks** — Lazy-load below-fold content:

```html
@defer (on viewport) {
  <app-comments [postId]="post._id" />
} @placeholder {
  <p>Scroll to see comments…</p>
}
```

- **`inject()` function** — Preferred over constructor injection for cleaner code.
- **Zoneless change detection** — Experimental in Angular 19. Works well with signals-based data fetching since signals automatically notify the framework of changes.

## 8. SSR & Prerendering

Angular 17+ includes built-in SSR support (replacing Angular Universal):

```typescript
// app.config.server.ts
import { provideServerRendering } from '@angular/platform-server'
import { provideClientHydration } from '@angular/platform-browser'

export const serverConfig = {
  providers: [
    provideServerRendering(),
    provideClientHydration(),
  ],
}
```

Key considerations for Sanity + Angular SSR:

| Feature | Details |
|---|---|
| **Hydration** | `provideClientHydration()` preserves server-rendered DOM. The client reuses it instead of re-rendering. |
| **HTTP Transfer Cache** | Only works with Angular's `HttpClient`. Since `@sanity/client` uses its own HTTP transport, use `TransferState` manually (see below). |
| **Prerendering** | Use `getPrerenderParams` in route config to generate static pages at build time. |

### Transfer State for `@sanity/client`

Angular's built-in HTTP Transfer Cache does not cover `@sanity/client` requests. Without manual transfer, the client re-fetches every query during hydration. Add `TransferState` to the service from Section 2:

```typescript
+ async function hashQuery(query: string, params?: QueryParams): Promise<string> {
+   const input = query + JSON.stringify(params ?? {})
+   const buffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input))
+   return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')).join('')
+ }

import { Injectable, inject } from '@angular/core'
+ import { isPlatformBrowser, isPlatformServer } from '@angular/common'
+ import { PLATFORM_ID, makeStateKey, TransferState } from '@angular/core'
import { createClient, type ClientReturn, type QueryParams, type SanityClient } from '@sanity/client'

export class SanityService {
  private client: SanityClient
+  private transferState = inject(TransferState)
+  private platformId = inject(PLATFORM_ID)

  async fetch<Query extends string>(query: Query, params?: QueryParams): Promise<ClientReturn<Query>> {
+    const key = makeStateKey<ClientReturn<Query>>(await hashQuery(query, params))
+
+    if (isPlatformBrowser(this.platformId)) {
+      const cached = this.transferState.get(key, null)
+      if (cached !== null) {
+        this.transferState.remove(key)
+        return cached
+      }
+    }
+
    const result = await this.client.fetch(query, params)
+
+    if (isPlatformServer(this.platformId)) {
+      this.transferState.set(key, result)
+    }
+
    return result
  }
}
```

The `hashQuery` helper keeps `TransferState` keys short (SHA-256 hex) instead of embedding raw GROQ strings in the serialized HTML.

Prerendering dynamic routes:

```typescript
// app.routes.server.ts
import { RenderMode, ServerRoute } from '@angular/ssr'

export const serverRoutes: ServerRoute[] = [
  {
    path: 'post/:slug',
    renderMode: RenderMode.Prerender,
    async getPrerenderParams() {
      // Fetch all slugs from Sanity at build time
      const client = createClient({ projectId: '...', dataset: '...', apiVersion: '...', useCdn: true })
      const slugs = await client.fetch<string[]>(`*[_type == "post"].slug.current`)
      return slugs.map((slug) => ({ slug }))
    },
  },
  { path: '**', renderMode: RenderMode.Server },
]
```

❌ **Bad:** Using `isPlatformBrowser()` in templates to conditionally render content — causes hydration mismatch.

✅ **Good:** Using `@defer` or `afterNextRender()` for browser-only code.

## 9. Visual Editing

> **Important:** Angular does not have official Sanity Visual Editing support. There is no `@sanity/visual-editing` integration, no Stega encoding, and no click-to-edit overlay for Angular applications. This is unlike Next.js, Nuxt, and SvelteKit which have first-party support.

### Preview Mode (Basic)

For draft content preview, create a separate preview client with an API token:

```typescript
@Injectable({ providedIn: 'root' })
export class SanityService {
  private client: SanityClient
  private previewClient: SanityClient

  constructor() {
    this.client = createClient({
      projectId: environment.sanity.projectId,
      dataset: environment.sanity.dataset,
      apiVersion: environment.sanity.apiVersion,
      useCdn: true,
    })

    this.previewClient = this.client.withConfig({
      useCdn: false,
      token: environment.sanity.previewToken, // Server-side only!
      perspective: 'drafts',
    })
  }

  fetch<Query extends string>(query: Query, params?: QueryParams, preview = false): Promise<ClientReturn<Query>> {
    const client = preview ? this.previewClient : this.client
    return client.fetch(query, params)
  }
}
```

> **Security:** Never expose the preview token in client-side bundles. Use this pattern only with SSR where the token stays on the server, or proxy preview requests through a backend API.

### Community Visual Editing

The community library `@limitless-angular/sanity` provides experimental Visual Editing support for Angular, including overlay click-to-edit functionality. Check its documentation for current status and limitations.

## 10. Error Handling

Common errors when integrating Angular with Sanity:

| Error | Cause | Solution |
|---|---|---|
| `401 Unauthorized` | Invalid or missing API token | Verify token in [Sanity Manage](https://www.sanity.io/manage). Ensure it has correct permissions. |
| `403 Forbidden` | CORS origin not allowed | Add your Angular dev/production URL to CORS origins in [Sanity Manage](https://www.sanity.io/manage). |
| `422 Invalid query` | GROQ syntax error | Test queries in Vision plugin or Sanity's GROQ playground. See `groq.md`. |
| Hydration mismatch | Conditional rendering based on platform | Use `@defer` or `afterNextRender()` instead of `isPlatformBrowser()` checks. |
| Empty response | Missing dataset or wrong `apiVersion` | Verify environment config. Use a date-based `apiVersion` (e.g., `'2025-05-01'`). |
| Images not loading | Missing `@sanity/image-url` setup | Ensure `getImageUrlBuilder` is called with a valid image reference. See `image.md`. |

For GROQ query patterns and best practices, see `groq.md`. For schema design, see `schema.md`.

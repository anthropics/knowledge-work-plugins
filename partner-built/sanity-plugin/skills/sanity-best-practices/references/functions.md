---
title: Sanity Functions
description: Rules for Sanity Functions — serverless event handlers that react to content changes in Sanity's Content Lake. Covers blueprint configuration, handler patterns, testing, deployment, and recursion control.
---

# Sanity Functions

Serverless event handlers hosted on Sanity's infrastructure, configured via **Blueprints** and triggered by document lifecycle events.

> **Experimental feature**: APIs may change. Always use `npx sanity@latest`.

## When to use

- Set computed/derived fields (timestamps, slugs, summaries)
- Enrich or validate content on publish
- Trigger external services (CDN purge, deploy hooks, notifications)
- Automate workflows (translation, tagging, cross-posting)
- Sync content to external systems
- Invoke Agent Actions in response to content events

## When NOT to use

- Logic needs >900s execution or >200MB bundle — use an external worker
- High-throughput bulk operations that exceed rate limits (200/fn/30s, 4000/project/30s)
- A simple POST to an external URL on publish with no document data shaping — use a webhook
- Client-side or UI-driven logic (validation, conditional fields) — belongs in Studio schema config

## Requirements

| Dependency | Version |
|:---|:---|
| Node.js | v24.x (matches deployed runtime) |
| Sanity CLI | v4.12.0+ |
| `@sanity/blueprints` | Latest |
| `@sanity/functions` | Latest |
| `@sanity/client` | v7.12.0+ (includes recursion protection) |

## Project Structure

Organize functions alongside your Sanity project, one level above the Studio directory:

```
my-project/
├── studio/
├── next-app/
├── functions/
│   ├── my-function/
│   │   ├── index.ts          # Handler code (entry point)
│   │   └── package.json      # (optional) function-level dependencies
│   └── another-function/
│       └── index.ts
├── sanity.blueprint.ts        # Blueprint configuration
├── package.json               # Project-level dependencies
└── node_modules/
```

The function directory name must match the `name` in the blueprint config. Each function exports a `handler` from its `index.ts` (or `index.js`).

---

## Step-by-step: Creating a Function

### 1. Initialize a Blueprint

```bash
npx sanity@latest blueprints init . \
  --type ts \
  --stack-name production \
  --project-id <your-project-id>
```

This creates `sanity.blueprint.ts` and `.sanity/blueprint.config.json` (add the latter to `.gitignore`).

### 2. Scaffold a Function

```bash
npx sanity@latest blueprints add function \
  --name my-function \
  --fn-type document-publish \
  --installer npm
```

`--fn-type` options: `document-create`, `document-update`, `document-publish` (deprecated), `document-delete`.

### 3. Configure the Blueprint

```typescript
// sanity.blueprint.ts
import { defineBlueprint, defineDocumentFunction } from '@sanity/blueprints'

export default defineBlueprint({
  resources: [
    defineDocumentFunction({
      name: 'my-function',
      event: {
        on: ['create', 'update'],
        filter: '_type == "post"',
      },
    }),
  ],
})
```

### 4. Write the Handler

```typescript
// functions/my-function/index.ts
import { documentEventHandler } from '@sanity/functions'
import { createClient } from '@sanity/client'

interface PostData {
  _id: string
  _type: string
  title: string
}

export const handler = documentEventHandler<PostData>(async ({ context, event }) => {
  const { data } = event

  const client = createClient({
    ...context.clientOptions,
    apiVersion: '2025-05-08',
  })

  try {
    await client.patch(data._id, {
      setIfMissing: { firstPublished: new Date().toISOString() },
    })
    console.log(`Set firstPublished on ${data._id}`)
  } catch (error) {
    console.error('Failed to patch document:', error)
  }
})
```

### 5. Test Locally

```bash
# Visual dev playground
npx sanity@latest functions dev

# CLI testing
npx sanity@latest functions test my-function \
  --dataset production \
  --with-user-token

# With a specific document
npx sanity@latest functions test my-function \
  --document-id abc123 \
  --dataset production \
  --with-user-token
```

### 6. Deploy

```bash
npx sanity@latest blueprints deploy
```

### 7. View Logs

```bash
npx sanity@latest functions logs my-function
npx sanity@latest functions logs my-function --watch
```

---

## Handler Reference

Every handler receives `{ context, event }`:

### `context`

| Property | Type | Description |
|:---|:---|:---|
| `clientOptions.apiHost` | `string` | API host URL |
| `clientOptions.projectId` | `string` | Sanity project ID |
| `clientOptions.dataset` | `string` | Dataset name |
| `clientOptions.token` | `string` | Robot token (deployed only) |
| `local` | `boolean \| undefined` | `true` during local testing |
| `eventResourceType` | `string` | `'dataset'` or `'media-library'` |
| `eventResourceId` | `string` | e.g., `'projectId.datasetName'` |

### `event`

```typescript
{
  data: {
    _id: string
    _type: string
    // ... rest of document (shaped by projection if set)
  }
}
```

When testing locally, `context.clientOptions` only has `projectId` and `apiHost`. Use `--dataset` and `--with-user-token` flags to supply the rest.

---

## Blueprint Configuration

### `defineDocumentFunction` Options

| Option | Type | Default | Description |
|:---|:---|:---|:---|
| `name` | `string` | required | Must match the directory name under `functions/` |
| `displayName` | `string` | — | Human-readable display name |
| `src` | `string` | `functions/<name>` | Path to function source directory |
| `memory` | `number` | `1` | Memory in GB (max 10) |
| `timeout` | `number` | `10` | Timeout in seconds (max 900) |
| `runtime` | `string` | `'nodejs22.x'` | `'node'`, `'nodejs22.x'`, or `'nodejs24.x'` |
| `project` | `string` | — | Project ID. Required if blueprint is org-scoped. |
| `robotToken` | `string` | — | Custom robot token name for the function |
| `event` | `object` | required | Event configuration (see below) |
| `env` | `Record<string, string>` | — | Environment variables via `process.env` |

### `event` Options

| Option | Type | Default | Description |
|:---|:---|:---|:---|
| `on` | `string[]` | required | `'create'`, `'update'`, `'delete'`. Legacy `'publish'` is deprecated. |
| `filter` | `string` | — | GROQ filter body (no `*[...]` wrapper) |
| `projection` | `string` | — | GROQ projection to shape `event.data`. Wrap in `{}`. |
| `includeDrafts` | `boolean` | `false` | Trigger on draft changes |
| `includeAllVersions` | `boolean` | `false` | Trigger on all document versions |
| `resource` | `object` | — | Scope to dataset: `{ type: 'dataset', id: 'projectId.datasetName' }` |

### `defineMediaLibraryAssetFunction`

For Media Library asset events. Requires `@sanity/blueprints` v0.4.0+ and `@sanity/functions` v1.1.0+.

```typescript
import { defineBlueprint, defineMediaLibraryAssetFunction } from '@sanity/blueprints'

export default defineBlueprint({
  resources: [
    defineMediaLibraryAssetFunction({
      name: 'asset-handler',
      event: {
        on: ['delete'],
        filter: 'documents::incomingGlobalDocumentReferenceCount() > 0',
        projection: '{_id, versions, title}',
        resource: {
          type: 'media-library',
          id: 'mlYourLibraryId',
        },
      },
    }),
  ],
})
```

---

## Event Types

| Event | Description |
|:---|:---|
| `create` | New document created |
| `update` | Existing document modified (for published docs, fires when a draft/version is published) |
| `delete` | Document deleted |
| `publish` | **Deprecated.** Equivalent to `['create', 'update']`. Migrate to explicit events. |

Often best to use `['create', 'update']` together for published document triggers.

---

## GROQ Filter Tips

- Only the filter body — `_type == 'post'`, not `*[_type == 'post']`
- `delta::changedAny(fieldName)` — trigger only when specific fields change
- `sanity::dataset() == 'production'` — scope to a dataset without `resource` config
- `_id in path('drafts.**')` with `includeDrafts: true` — draft-only triggers
- Combine conditions to prevent recursion: `_type == 'post' && !defined(processedAt)`

---

## Projections

- Shape the data passed to `event.data`
- Limited to the invoking document's scope (plus `→` for references)
- Nested filters in projections (like `*[references(^._id)]`) will fail silently — query inside the function instead
- Wrap in `{}`: `projection: '{title, _id, slug}'`

---

## Environment Variables

Three ways to set them:

1. Blueprint config: `env: { MY_VAR: 'value' }`
2. CLI: `npx sanity functions env add my-function MY_VAR my-value`
3. Local testing: `MY_VAR=value npx sanity functions test my-function`

Access in handler code via `process.env.MY_VAR`.

---

## Critical Rules

### Preventing Recursion

If your function mutates the same document type it listens to, you **will** create an infinite loop.

**✅ Correct — use GROQ filters to exclude processed documents:**
```typescript
defineDocumentFunction({
  name: 'first-published',
  event: {
    on: ['create', 'update'],
    filter: "_type == 'post' && !defined(firstPublished)",
  },
})
```

**✅ Correct — use `@sanity/client` v7.12.0+ for automatic lineage headers:**
```typescript
import { createClient } from '@sanity/client'

// Client automatically sets X-Sanity-Lineage header
// Recursive chains are limited to 16 invocations
const client = createClient({
  ...context.clientOptions,
  apiVersion: '2025-05-08',
})
```

**❌ Incorrect — no recursion guard:**
```typescript
defineDocumentFunction({
  name: 'update-post',
  event: {
    on: ['create', 'update'],
    filter: "_type == 'post'",  // Will re-trigger on its own writes!
  },
})
```

### Local Testing Safety

Use `context.local` to prevent accidental mutations during testing:

```typescript
// Skip mutations entirely in test
if (!context.local) {
  await client.createOrReplace(someDoc)
}

// Or use dryRun
await client.patch(event.data._id, {
  set: { processed: true },
}).commit({ dryRun: context.local })

// Or use noWrite for Agent Actions
await client.agent.action.generate({
  schemaId: 'your-schema-id',
  documentId: event.data._id,
  instruction: 'Summarize this document',
  target: { path: ['summary'] },
  noWrite: context.local,
})
```

### Limits

- Max bundle size: 200MB (including dependencies). Prefer slim, platform-agnostic packages.
- Rate limits: 200 invocations/fn/30s, 4000/project/30s
- Max timeout: 900s. Larger functions = slower cold starts.

### Cost

Cost = invocations × (memory GB × duration seconds). Default is 1GB memory. A function averaging 1GB and 40ms duration can run ~500k invocations within 20K GB-seconds. [Monitor usage at the organization level](https://www.sanity.io/manage).

---

## Common Patterns

### Deploy hook / CDN invalidation

**Blueprint:**
```typescript
defineDocumentFunction({
  name: 'deploy-hook',
  event: {
    on: ['create', 'update'],
    filter: '_type == "page"',
  },
})
```

**Handler:**
```typescript
export const handler = documentEventHandler(async ({ context, event }) => {
  const URL = process.env.DEPLOY_HOOK_URL
  if (!URL) throw new Error('DEPLOY_HOOK_URL is not set')

  await fetch(URL)
  console.log('Deploy hook triggered')
})
```

Set the env var: `npx sanity functions env add deploy-hook DEPLOY_HOOK_URL https://...`

### Set a timestamp on first publish

Uses the same pattern as the step-by-step example above. The key insight: the `!defined(firstPublished)` GROQ filter prevents re-triggering after the field is set. The `setIfMissing` patch is a redundant safety net.

```typescript
defineDocumentFunction({
  name: 'first-published',
  event: {
    on: ['create', 'update'],
    filter: '_type == "post" && !defined(firstPublished)',
  },
})
```

### Auto-translate with Agent Actions

**Blueprint:**
```typescript
defineDocumentFunction({
  name: 'translate',
  event: {
    on: ['create', 'update'],
    filter: "_type == 'post' && language == 'en-US'",
    projection: '{_id}',
  },
})
```

**Handler:**
```typescript
export const handler = documentEventHandler(async ({ context, event }) => {
  const client = createClient({ ...context.clientOptions, apiVersion: 'vX' })

  await client.agent.action.translate({
    schemaId: 'your-schema-id',
    async: true,
    documentId: event.data._id,
    languageFieldPath: 'language',
    targetDocument: {
      operation: 'createOrReplace',
      _id: `${event.data._id}-el-GR`,
    },
    fromLanguage: { id: 'en-US', title: 'English' },
    toLanguage: { id: 'el-GR', title: 'Greek' },
  })
})
```

The GROQ filter ensures only English documents trigger the function. The translated document gets a different `language` value, preventing recursive triggers.

### Auto-tag with Agent Actions

**Blueprint:**
```typescript
defineDocumentFunction({
  name: 'auto-tag',
  event: {
    on: ['create', 'update'],
    filter: "_type == 'post'",
    projection: '{_id, title, body}',
  },
})
```

**Handler:**
```typescript
export const handler = documentEventHandler(async ({ context, event }) => {
  const client = createClient({ ...context.clientOptions, apiVersion: 'vX' })

  await client.agent.action.generate({
    schemaId: 'your-schema-id',
    documentId: event.data._id,
    instruction: 'Analyze the content and generate 3 relevant tags. Reuse existing tags when possible.',
    target: { path: ['tags'] },
    async: true,
  })
})
```

### Slack notification on publish

```typescript
export const handler = documentEventHandler(async ({ context, event }) => {
  const WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL
  if (!WEBHOOK_URL) throw new Error('SLACK_WEBHOOK_URL not set')

  await fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `📝 New content published: *${event.data.title || event.data._id}* (${event.data._type})`,
    }),
  })
})
```

### Scope to a specific dataset

**Option A — `resource` config:**
```typescript
defineDocumentFunction({
  name: 'production-only',
  event: {
    on: ['update'],
    filter: "_type == 'post'",
    resource: { type: 'dataset', id: 'myProjectId.production' },
  },
})
```

**Option B — GROQ filter:**
```typescript
defineDocumentFunction({
  name: 'production-only',
  event: {
    on: ['update'],
    filter: "_type == 'post' && sanity::dataset() == 'production'",
  },
})
```

### React to Media Library asset changes

Requires `@sanity/blueprints` v0.4.0+ and `@sanity/functions` v1.1.0+.

**Blueprint:**
```typescript
import { defineBlueprint, defineMediaLibraryAssetFunction } from '@sanity/blueprints'

export default defineBlueprint({
  resources: [
    defineMediaLibraryAssetFunction({
      name: 'asset-deleted',
      event: {
        on: ['delete'],
        filter: 'documents::incomingGlobalDocumentReferenceCount() > 0',
        projection: '{_id, versions, title}',
        resource: { type: 'media-library', id: 'mlYourLibraryId' },
      },
    }),
  ],
})
```

**Handler:**
```typescript
export const handler = documentEventHandler(async ({ context, event }) => {
  const { eventResourceId } = context  // Media Library ID
  const client = createClient({
    ...context.clientOptions,
    apiVersion: '2025-05-08',
  })

  const response = await client.request({
    uri: `/media-libraries/${eventResourceId}/query`,
    method: 'POST',
    body: { query: `*[_type == 'sanity.imageAsset']` },
  })

  console.log('Assets:', response)
})
```

### Recursion control with custom HTTP clients

If not using `@sanity/client`, implement lineage tracking manually:

```typescript
export const handler = documentEventHandler(async ({ context, event }) => {
  const lineage = process.env.X_SANITY_LINEAGE

  await fetch(`https://${context.clientOptions.projectId}.api.sanity.io/v2025-05-08/data/mutate/production`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${context.clientOptions.token}`,
      ...(lineage ? { 'X-Sanity-Lineage': lineage } : {}),
    },
    body: JSON.stringify({
      mutations: [{ patch: { id: event.data._id, set: { processed: true } } }],
    }),
  })
})
```

### Multiple functions in one blueprint

```typescript
export default defineBlueprint({
  resources: [
    defineDocumentFunction({
      name: 'first-published',
      event: {
        on: ['create', 'update'],
        filter: "_type == 'post' && !defined(firstPublished)",
      },
    }),
    defineDocumentFunction({
      name: 'notify-slack',
      event: {
        on: ['create', 'update'],
        filter: "_type == 'post'",
        projection: '{title, _id}',
      },
    }),
    defineDocumentFunction({
      name: 'sync-algolia',
      timeout: 30,
      event: {
        on: ['create', 'update', 'delete'],
        filter: "_type == 'product'",
      },
    }),
  ],
})
```

---

## CI/CD Deployment

Use the [Blueprints GitHub Action](https://github.com/sanity-io/blueprints-actions)

```yaml
- uses: sanity-io/blueprints-actions/deploy@deploy-v3
  with:
    sanity-token: ${{ secrets.SANITY_DEPLOY_TOKEN }}
```

Only personal auth tokens are supported for deployment (not robot tokens).

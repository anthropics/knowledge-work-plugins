---
name: typegen
description: Run Sanity TypeGen and troubleshoot type generation issues.
---

# Sanity TypeGen Workflow

I'll help you generate TypeScript types from your Sanity schema.

## Quick Start

```bash
npm run typegen
# or
npx sanity schema extract && npx sanity typegen generate
```

## What I'll Do

1. **Check Configuration**
   - Check for `typegen` config in `sanity.cli.ts` (recommended)
   - If using deprecated `sanity-typegen.json`, suggest migrating to `sanity.cli.ts`
   - Ensure `typegen` script is in `package.json` (for manual workflows)

2. **Run TypeGen**
   - Execute the typegen command
   - Report any errors

3. **Troubleshoot Issues**
   - Fix incorrect path globs
   - Resolve schema syntax errors
   - Update query imports
   - Migrate deprecated `sanity-typegen.json` to `sanity.cli.ts`

## Common Issues I Fix

| Issue | Solution |
|-------|----------|
| "No schema found" | Fix `path` glob in `sanity.cli.ts` typegen config |
| "Query not typed" | Wrap in `defineQuery()` or `groq` template |
| Types outdated | Re-run after schema/query changes, or enable automatic generation |
| Import errors | Check `sanity.types.ts` output path |
| Using `sanity-typegen.json` | Migrate config to `sanity.cli.ts` (deprecated) |

## Configuration

Configure TypeGen in `sanity.cli.ts`:

```typescript
// sanity.cli.ts
import { defineCliConfig } from 'sanity/cli'

export default defineCliConfig({
  typegen: {
    enabled: true, // Auto-generate during sanity dev/build
    path: "./src/**/*.{ts,tsx,js,jsx,astro,svelte,vue}",
    schema: "schema.json",
    generates: "./sanity.types.ts",
    overloadClientMethods: true,
  },
})
```

## Usage

> "Run typegen"
> "Fix my TypeGen configuration"
> "Why are my types not updating?"
> "Enable automatic type generation"

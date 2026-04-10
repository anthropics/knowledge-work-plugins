---
name: deploy-schema
description: Deploy Sanity schema to the Content Lake with verification.
---

# Deploy Sanity Schema

I'll help you deploy your schema to the Sanity Content Lake.

## Why Deploy Schema?

Schema deployment is **required** for:
- ⚠️ **MCP Server operations** (create_document, patch_document)
- Embedded Studios
- Scheduled Publishing
- Cloud Functions with schema validation

## Deployment Command

```bash
npx sanity schema deploy
```

## What I'll Do

1. **Pre-Deploy Check**
   - Verify schema syntax (run typegen)
   - Check for breaking changes
   - Warn about removed fields with data

2. **Deploy**
   - Run `npx sanity schema deploy`
   - Confirm success

3. **Post-Deploy Verification**
   - Use MCP `get_schema` to verify deployment
   - Confirm new types/fields are available

## When to Deploy

| Scenario | Deploy? |
|----------|---------|
| Added new document type | ✅ Yes |
| Added/modified fields | ✅ Yes |
| Changed validation rules | ✅ Yes |
| Using MCP tools | ✅ Yes (always) |
| Local dev only (no MCP) | Optional |

## Important Notes

- **Schema deployment is fast** (~2 seconds)
- **Does NOT deploy the Studio app** (use `npx sanity deploy` for that)
- **Always deploy before MCP operations** after schema changes

## Usage

> "Deploy my schema"
> "Check if my schema is deployed"
> "Why can't MCP see my new field?"


# Sanity Project

This is a Sanity-powered project. Use the Knowledge Router below to find Sanity guidance for your task. Available as a [Claude Code and Cursor plugin](https://github.com/sanity-io/agent-toolkit#option-3-install-plugin).

## Commands

```bash
# MCP Setup
npx sanity@latest mcp configure  # Configure MCP for your AI editor

# Schema & Types
npx sanity schema deploy     # Deploy schema to Content Lake (REQUIRED before MCP!)
npx sanity schema extract    # Extract schema for TypeGen
npx sanity typegen generate  # Generate TypeScript types

# Development
npx sanity dev               # Start Studio dev server
npx sanity build             # Build Studio for production
npx sanity deploy            # Deploy Studio to Sanity hosting

# Help
npx sanity docs search "query"  # Search Sanity documentation
npx sanity --help               # List all CLI commands
```

## Knowledge Router

If the Sanity MCP server (`https://mcp.sanity.io`) is available, use `list_sanity_rules` and `get_sanity_rules` to load always up-to-date rules on demand. Otherwise, use the table below to find local reference files.

> For the full reference index, see `skills/sanity-best-practices/SKILL.md`.

| Topic | Trigger Keywords | Reference |
| :--- | :--- | :--- |
| **Onboarding** | `start`, `setup`, `init`, `new project` | `skills/sanity-best-practices/references/get-started.md` |
| **Project Structure** | `structure`, `monorepo`, `embedded studio`, `file naming` | `skills/sanity-best-practices/references/project-structure.md` |
| **Schema** | `schema`, `model`, `document`, `field`, `defineType` | `skills/sanity-best-practices/references/schema.md` |
| **Deprecation** | `deprecate`, `remove field`, `legacy`, `migration` | `skills/sanity-best-practices/references/schema.md` |
| **Import/Migration** | `import`, `wordpress`, `html`, `markdown`, `migrate` | `skills/sanity-best-practices/references/migration.md` |
| **Next.js** | `next.js`, `app router`, `server component`, `fetch` | `skills/sanity-best-practices/references/nextjs.md` |
| **Nuxt** | `nuxt`, `vue`, `nuxt.js` | `skills/sanity-best-practices/references/nuxt.md` |
| **Angular** | `angular`, `signals`, `resource api` | `skills/sanity-best-practices/references/angular.md` |
| **Astro** | `astro`, `islands` | `skills/sanity-best-practices/references/astro.md` |
| **Remix/React Router** | `remix`, `react router`, `loader` | `skills/sanity-best-practices/references/remix.md` |
| **Svelte** | `svelte`, `sveltekit`, `kit` | `skills/sanity-best-practices/references/svelte.md` |
| **Visual Editing** | `stega`, `visual editing`, `clean`, `overlay`, `presentation`, `usePresentationQuery` | `skills/sanity-best-practices/references/visual-editing.md` |
| **Page Builder** | `page builder`, `pageBuilder`, `block component`, `alignment`, `switch render` | `skills/sanity-best-practices/references/page-builder.md` |
| **Rich Text** | `portable text`, `rich text`, `block content`, `serializer`, `PTE`, `marks`, `annotations` | `skills/sanity-best-practices/references/portable-text.md` |
| **Images** | `image`, `urlFor`, `crop`, `hotspot`, `lqip` | `skills/sanity-best-practices/references/image.md` |
| **Studio Structure** | `structure`, `desk`, `sidebar`, `singleton`, `grouping` | `skills/sanity-best-practices/references/studio-structure.md` |
| **Localization** | `i18n`, `translation`, `localization`, `language`, `multilingual`, `localized singleton` | `skills/sanity-best-practices/references/localization.md` |
| **SEO** | `seo`, `metadata`, `sitemap`, `og image`, `open graph`, `json-ld`, `redirect` | `skills/sanity-best-practices/references/seo.md` |
| **Shopify/Hydrogen** | `shopify`, `hydrogen`, `e-commerce`, `storefront`, `sanity connect` | `skills/sanity-best-practices/references/hydrogen.md` |
| **GROQ** | `groq`, `query`, `defineQuery`, `projection`, `filter`, `order` | `skills/sanity-best-practices/references/groq.md` |
| **TypeGen** | `typegen`, `typescript`, `types`, `infer`, `satisfies`, `type generation` | `skills/sanity-best-practices/references/typegen.md` |
| **App SDK** | `app sdk`, `custom app`, `useDocuments`, `useDocument`, `DocumentHandle`, `SanityApp`, `sdk-react` | `skills/sanity-best-practices/references/app-sdk.md` |
| **Blueprints** | `blueprints`, `IaC`, `infrastructure`, `stack`, `defineBlueprint` | `skills/sanity-best-practices/references/blueprints.md` |
| **Sanity Functions** | `functions`, `serverless`, `event handler`, `documentEventHandler`, `defineDocumentFunction`, `sanity.blueprint.ts` | `skills/sanity-best-practices/references/functions.md` |

### Using the Knowledge Router

**Before modifying any code:**
1. Identify which topics from the table above apply to your task
2. Read the corresponding reference file(s) using the file path
3. Follow the patterns and constraints defined in those references

Example: If asked to "create a blog post schema", read `skills/sanity-best-practices/references/schema.md` first.

## Agent Behavior

- Specialize in **Structured Content**, **GROQ**, and **Sanity Studio** configuration.
- Write best-practice, type-safe code using **Sanity TypeGen**.
- Build scalable content platforms, not just websites.
- **Detect the user's framework** from `package.json` and consult the appropriate reference file.

## MCP Server (Preferred for Content Operations)

**Prefer** MCP tools over writing scripts for content operations:

**Content Operations:**

| Tool | Use For |
|------|---------|
| `query_documents` | Run GROQ queries |
| `get_document` | Fetch a single document by exact ID |
| `create_documents_from_json` | Create draft documents from JSON |
| `create_documents_from_markdown` | Create draft documents from markdown |
| `patch_document_from_json` | Apply precise modifications to document fields |
| `patch_document_from_markdown` | Patch a field using markdown content |
| `publish_documents` | Publish one or more drafts |
| `unpublish_documents` | Unpublish documents (move back to drafts) |
| `discard_drafts` | Discard drafts while keeping published documents |

**Schema & Development:**

| Tool | Use For |
|------|---------|
| `get_schema` | Get full schema of the current workspace |
| `list_workspace_schemas` | List all available workspace schema names |
| `deploy_schema` | Deploy schema types to the cloud |
| `search_docs` / `read_docs` | Search and read Sanity documentation |
| `list_sanity_rules` / `get_sanity_rules` | Load best-practice development rules |
| `migration_guide` | Get guides for migrating from other CMSs |

**Media & AI:**

| Tool | Use For |
|------|---------|
| `generate_image` | AI image generation for a document field |
| `transform_image` | AI transformation of an existing image |

**Releases:**

| Tool | Use For |
|------|---------|
| `create_version` | Create a version document for a release |
| `version_replace_document` | Replace version contents from another document |
| `version_discard` | Discard document versions from a release |
| `version_unpublish_document` | Mark document to be unpublished when release runs |

**Project Management:**

| Tool | Use For |
|------|---------|
| `list_projects` / `list_organizations` | List projects and organizations |
| `create_project` | Create a new Sanity project |
| `list_datasets` / `create_dataset` / `update_dataset` | Manage datasets |
| `add_cors_origin` | Add CORS origins for client-side requests |
| `list_embeddings_indices` / `semantic_search` | Semantic search on embeddings |

**Critical:** After schema changes, deploy with `deploy_schema` before using content tools.

## Boundaries
- **Always:**
  - Use `defineQuery` for all GROQ queries.
  - Prefer MCP tools for content operations (query, create, update, patch). For bulk migrations or when MCP is unavailable, NDJSON scripts are a valid alternative. Never use NDJSON scripts when MCP tools can accomplish the same task more simply.
  - Run `deploy_schema` after schema changes — required before using content tools. If a local Studio exists, update schema files first to keep them in sync with the deployed schema.
  - Follow the "Deprecation Pattern" when removing fields (ReadOnly -> Hidden -> Deprecated).
  - Run `npm run typegen` after schema or query changes (or enable automatic generation with `typegen.enabled: true` in `sanity.cli.ts`).
- **Ask First:**
  - Before modifying `sanity.config.ts`.
  - Before deleting any schema definition file.
- **Never:**
  - Hardcode API tokens (use `process.env`).
  - Use loose types (`any`) for Sanity content.

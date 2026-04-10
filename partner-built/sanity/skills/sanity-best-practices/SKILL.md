---
name: sanity-best-practices
description: Sanity development best practices for schema design, GROQ queries, TypeGen, Visual Editing, images, Portable Text, Studio structure, localization, migrations, Sanity Functions, Blueprints, and framework integrations such as Next.js, Nuxt, Astro, Remix, SvelteKit, Angular, Hydrogen, and the App SDK. Use this skill whenever working with Sanity schemas, defineType or defineField, GROQ or defineQuery, content modeling, Presentation or preview setups, Sanity-powered frontend integrations, Sanity Functions, documentEventHandler, defineDocumentFunction, defineMediaLibraryAssetFunction, @sanity/functions, @sanity/blueprints, sanity.blueprint.ts, event-driven content automation, or when reviewing and fixing a Sanity codebase.
---

# Sanity Best Practices

Comprehensive best practices and integration guides for Sanity development, maintained by Sanity. Use the quick reference below to load only the one or two topic files that match the task.

## When to Apply

Reference these guidelines when:
- Setting up a new Sanity project or onboarding
- Integrating Sanity with a frontend framework (Next.js, Nuxt, Astro, Remix, SvelteKit, Hydrogen)
- Writing GROQ queries or optimizing performance
- Designing content schemas
- Implementing Visual Editing and live preview
- Working with images, Portable Text, or page builders
- Configuring Sanity Studio structure
- Setting up TypeGen for type safety
- Implementing localization
- Migrating content from other systems
- Building custom apps with the Sanity App SDK
- Managing infrastructure with Blueprints
- Automating content workflows with Sanity Functions

## Quick Reference

### Integration Guides

- `get-started` - Interactive onboarding for new Sanity projects
- `nextjs` - Next.js App Router, Live Content API, embedded Studio
- `nuxt` - Nuxt integration with @nuxtjs/sanity
- `angular` - Angular integration with @sanity/client, signals, resource API
- `astro` - Astro integration with @sanity/astro
- `remix` - React Router / Remix integration
- `svelte` - SvelteKit integration with @sanity/svelte-loader
- `hydrogen` - Shopify Hydrogen with Sanity
- `project-structure` - Monorepo and embedded Studio patterns
- `app-sdk` - Custom applications with Sanity App SDK
- `blueprints` - Infrastructure as Code with Sanity Blueprints
- `functions` - Automating content workflows with Sanity Functions

### Topic Guides

- `groq` - GROQ query patterns, type safety, performance optimization
- `schema` - Schema design, field definitions, validation, deprecation patterns
- `visual-editing` - Presentation Tool, Stega, overlays, live preview
- `page-builder` - Page Builder arrays, block components, live editing
- `portable-text` - Rich text rendering and custom components
- `image` - Image schema, URL builder, hotspots, LQIP, Next.js Image
- `studio-structure` - Desk structure, singletons, navigation
- `typegen` - TypeGen configuration, workflow, type utilities
- `seo` - Metadata, sitemaps, Open Graph, JSON-LD
- `localization` - i18n patterns, document vs field-level, locale management
- `migration` - Content import overview (see also `migration-html-import`)
- `migration-html-import` - HTML to Portable Text with @portabletext/block-tools

## How to Use

Start with the single framework or topic guide that best matches the request, then read additional references only when the task crosses concerns. Use these reference files for detailed explanations and code examples:

```
references/groq.md
references/schema.md
references/nextjs.md
```

Each reference file contains:
- Comprehensive topic or integration coverage
- Incorrect and correct code examples
- Decision matrices and workflow guidance
- Framework-specific patterns where applicable


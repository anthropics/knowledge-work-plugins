# Knowledge Work Plugins - Project Index

## Project Overview

Monorepo of Claude Code plugins for knowledge work roles. Each plugin bundles skills, commands, and connectors for a specific job function.

## Key Documents

- [Product Definition](./product.md) - What we're building and why
- [Tech Stack](./tech-stack.md) - Technologies and patterns used
- [Workflow](./workflow.md) - Development workflow and processes
- [Product Guidelines](./product-guidelines.md) - Design principles and conventions
- [Tracks Registry](./tracks.md) - Active development tracks

## Plugin Structure

```
plugin-name/
├── .claude-plugin/plugin.json   # Manifest
├── .mcp.json                    # MCP connectors
├── commands/                    # Slash commands
└── skills/                      # Domain knowledge
```

## Active Plugins

| Plugin | Focus |
|--------|-------|
| productivity | Task/calendar management |
| sales | Pipeline, outreach, competitive |
| customer-support | Triage, responses, escalations |
| product-management | Specs, roadmaps, research |
| marketing | Content, campaigns, analytics |
| legal | Contracts, compliance, risk |
| finance | Journal entries, reconciliation |
| data | SQL, visualization, analysis |
| enterprise-search | Cross-tool search |
| bio-research | Life sciences R&D |
| health | Health checks & diagnostics |
| cowork-plugin-management | Plugin creation |
| health | Healthcare organization workflows |

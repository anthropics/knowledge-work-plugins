# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A set of Claude Cowork/Claude Code plugins scoped for Acoustic, a marketing automation and cross-channel engagement SaaS company. It is a fork of Anthropic's `knowledge-work-plugins` repo, trimmed to 7 plugins relevant to Acoustic's teams.

This is a **pure markdown + JSON** repo — no build toolchain, no Node.js, no compilation. Every plugin is a directory of `.md` and `.json` files.

## Build

```bash
./build.sh
```

Produces one zip per plugin in `build/` (e.g., `build/marketing.zip`). The `build/` directory is gitignored. No dependencies required — uses only `zip` (pre-installed on macOS/Linux).

## Plugin Structure

Every plugin follows this layout:

```
plugin-name/
├── .claude-plugin/plugin.json   # Manifest: name, version, description, author
├── .mcp.json                    # MCP server connections (HTTP endpoints)
├── CONNECTORS.md                # Documents tool categories and ~~placeholder syntax
├── README.md                    # Plugin overview
├── commands/                    # Slash commands — one .md file per command
└── skills/                      # Skills — one subdirectory per skill
    └── skill-name/
        ├── SKILL.md             # Frontmatter (name, description, triggers) + workflow
        └── references/          # Optional supporting docs
```

**Skills** fire automatically when relevant context is detected. **Commands** are invoked explicitly as slash commands (e.g., `/marketing:draft-content`).

## Tool-Agnostic Placeholder Convention

Skill and command files reference tools via `~~category` placeholders (e.g., `~~CRM`, `~~chat`, `~~marketing automation`) rather than specific product names. This allows the plugin to work with any MCP server in that category. The concrete MCP servers are configured in `.mcp.json`. CONNECTORS.md maps categories to their included and alternative servers.

## Retained Plugins

| Plugin | Primary audience |
|--------|-----------------|
| `marketing/` | Marketing team — content, campaigns, brand, analytics |
| `sales/` | Sales team — prospecting, outreach, pipeline |
| `customer-support/` | Support/CS — tickets, KB, escalations |
| `product-management/` | Product — specs, roadmaps, research |
| `legal/` | Legal — contracts, NDAs, compliance |
| `finance/` | Finance — journal entries, reconciliation, close |
| `cowork-plugin-management/` | Anyone building or customizing plugins |

## Key Files to Know

- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) — central registry listing all plugins; update this when adding/removing plugins
- [`build.sh`](build.sh) — build script; update the `PLUGINS` array here when adding/removing plugins
- [`marketing/.mcp.json`](marketing/.mcp.json) — includes the Acoustic MCP server placeholder (`https://mcp.acoustiq.ai/mcp`); update with the real URL when available

## Adding or Customizing a Plugin

- **New plugin**: follow the directory structure above; add an entry to `.claude-plugin/marketplace.json` and the `PLUGINS` array in `build.sh`
- **Swap a connector**: edit the plugin's `.mcp.json` and update `CONNECTORS.md` to reflect the change
- **Add Acoustic-specific context**: edit the relevant `SKILL.md` files to include Acoustic terminology, processes, and tool names
- Use the `cowork-plugin-management` plugin's skills as a guided workflow for building new plugins from scratch

# Plugin Management

Create, customize, and manage Cursor plugins tailored to your organization's tools and workflows. Configure MCP servers, adjust plugin behavior, and adapt templates to match how your team works.

## What It Does

This plugin gives the AI the knowledge to build and maintain Cursor plugins from scratch — walking you through discovery, planning, design, implementation, and delivery as a guided conversation.

## Skills

| Skill                        | Trigger phrases                                                 | What it does                                                                               |
| ---------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **create-plugin**            | "create a plugin", "build a plugin", "scaffold a plugin"       | Guide you through building a new Cursor plugin from scratch, ready to install immediately  |
| **plugin-customizer**        | "customize plugin", "configure plugin", "tailor plugin"        | Set up or refine an existing plugin for your organization's specific tools and workflows    |

## Installation

### Cursor

Add this plugin via the Cursor marketplace, or copy to your local plugins directory:

```bash
cp -r . ~/.cursor/plugins/local/plugin-management/
```

### Claude Code

```bash
claude plugin install cowork-plugin-management@knowledge-work-plugins
```

## No Connectors Required

This plugin works standalone — no MCP servers needed. It uses the AI's built-in capabilities to scaffold, configure, and deliver plugin files through conversation.

## Structure

```
cowork-plugin-management/
├── .cursor-plugin/plugin.json     # Cursor manifest (name: plugin-management)
├── .claude-plugin/plugin.json     # Claude Code / Cowork manifest
└── skills/
    ├── create-cowork-plugin/      # Build new plugins from scratch
    └── cowork-plugin-customizer/  # Customize existing plugins for your org
```

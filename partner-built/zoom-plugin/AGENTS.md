# Zoom Plugin

Cross-platform discovery file for agent tools that look for `AGENTS.md`.

## What This Repo Provides

This repository contains a Zoom developer plugin centered on `SKILL.md`-based workflows and reference material.

Primary capabilities:
- choose the right Zoom surface for a use case
- plan Zoom integrations across REST APIs, SDKs, webhooks, OAuth, and MCP
- debug broken Zoom integrations
- build focused Zoom implementations for meetings, bots, chat, phone, contact center, and virtual agent workflows
- provide deep product-specific reference material under `skills/`

## Primary Entry Skills

- `skills/start/SKILL.md` — default routing entry point
- `skills/plan-zoom-product/SKILL.md` — pick the right Zoom developer product
- `skills/plan-zoom-integration/SKILL.md` — turn an idea into an implementation plan
- `skills/setup-zoom-oauth/SKILL.md` — choose the auth model and redirect flow
- `skills/build-zoom-meeting-app/SKILL.md` — implement an embedded or managed meeting app
- `skills/build-zoom-bot/SKILL.md` — implement a meeting bot or recorder
- `skills/debug-zoom/SKILL.md` — isolate the failing integration layer
- `skills/setup-zoom-mcp/SKILL.md` — plan a Zoom MCP workflow for Claude

## Repo Shape

- `.claude-plugin/plugin.json` — Claude plugin manifest
- `.mcp.json` — bundled Zoom MCP server definition
- `skills/` — all plugin skills and supporting references
- `README.md` — user-facing overview
- `CONNECTORS.md` — bundled MCP connector notes

## Usage Notes

- For Claude Code, install or load this as a plugin.
- For other agent ecosystems, treat the `skills/` tree as the primary reusable asset.
- Workflow skills are the front door; product-specific folders under `skills/` are supporting references.

# B12 Plugin

A [B12](https://www.b12.io/) plugin for Claude. Create professional, AI-generated websites in seconds.

## Overview

B12 is an AI-powered website builder that creates production-ready websites from a business description. This plugin equips Claude with a skill that collects the necessary details and generates a personalized B12 signup link — no design or development work required.

## Skills

| Skill               | Trigger phrases                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `website-generator` | "Create a website for [business]", "Build a website for [project]", "Make me a website", "I need a website for my [business type]" |

### `website-generator`

Generates a personalized B12 website signup link from a business description. Claude collects the minimum required information — a brief description of the business — and optionally gathers the business name and style/structure preferences. Returns a direct link to a ready-to-publish AI-generated website. No templates, no drag-and-drop; B12 handles design, copy, and hosting automatically.

**Usage examples:**

```
Create a website for my consulting firm

Create a website for a software development agency

Create a personal website

Create a website for a cat café
```

## Installation

### Claude Code

```bash
/plugin install b12@knowledge-work-plugins
```

Or point Claude Code at the plugin directory directly:

```bash
claude --plugin-dir ./partner-built/b12
```

### Claude Cowork

Install through the plugin manager in Claude Desktop.

## License

Apache 2.0

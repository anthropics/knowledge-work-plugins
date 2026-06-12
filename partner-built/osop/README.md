# OSOP Plugin

Structured workflow logging, risk analysis, and self-optimization for AI coding sessions. Records what Claude did step by step as portable YAML files, generates HTML reports, and improves workflows over time.

Built on [OSOP](https://github.com/Archie0125/osop-spec) (Open Standard Operating Protocol) — the open standard for defining workflows as portable YAML.

## Features

- **Session logging** — After multi-step tasks, creates `.osop` workflow definition + `.osoplog.yaml` execution record with tool usage, AI reasoning, and sub-agent tracking
- **HTML reports** — Converts logs into self-contained HTML with dark mode, expandable nodes, and duration bars
- **Risk review** — Analyzes workflows for destructive commands, broad permissions, missing approval gates, and hardcoded secrets (score 0-100)
- **Self-optimization** — Reads past execution history, identifies slow steps and failure hotspots, suggests retry policies and parallelization

## Installation

### Claude Code / Cowork

```bash
claude plugin install osop-skill@osop-marketplace
```

Or install directly:

```bash
git clone https://github.com/Archie0125/osop-skill.git
claude --plugin-dir ./osop-skill
```

## Commands

| Command | Description |
|---|---|
| `/osop-log` | Record completed work as .osop + .osoplog.yaml |
| `/osop-report` | Convert .osop files to standalone HTML report |
| `/osop-review` | Analyze workflow for security risks |
| `/osop-optimize` | Improve workflow from execution history |

## Skills

| Skill | Description |
|---|---|
| OSOP knowledge base | 16 node types, 13 edge modes, security metadata, sub-agent tracking |
| Safety policies | 9 policies for approval gates, secret handling, dry-run enforcement |
| Self-optimization protocol | Execute → log → analyze → improve → re-execute feedback loop |

## Visualize

Open `.osop` + `.osoplog.yaml` at [osop-editor.vercel.app](https://osop-editor.vercel.app) for interactive step-by-step replay with risk overlays.

## Links

- **Plugin**: [github.com/Archie0125/osop-skill](https://github.com/Archie0125/osop-skill)
- **Spec**: [github.com/Archie0125/osop-spec](https://github.com/Archie0125/osop-spec)
- **Visual Editor**: [osop-editor.vercel.app](https://osop-editor.vercel.app)
- **MCP Server**: [github.com/Archie0125/osop-mcp](https://github.com/Archie0125/osop-mcp)

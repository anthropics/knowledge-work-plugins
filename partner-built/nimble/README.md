# Nimble Web Search Skills & Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.17.0-green)](https://github.com/Nimbleway/agent-skills)

Unlock the web for your AI agents — search, scrape, extract structured data, and run business intelligence workflows, all powered by Nimble's web data infrastructure. One plugin for Claude Code, Cursor, and any platform that supports the [Agent Skills spec](https://agentskills.io/specification.md).

## Skills

| Category | What you get |
| -------- | ------------ |
| **[Business Research](skills/business-research/)** | Competitor monitoring, 360° company research, and market discovery — find all businesses of a given type in any geography with multi-source verification |
| **[Marketing](skills/marketing/)** | Track how competitors position themselves — messaging shifts, pricing changes, content gaps, battlecard inputs |
| **[Productivity](skills/productivity/)** | Walk into any meeting fully briefed — attendee backgrounds, company context, talking points, relationship mapping. Discover and score local businesses in any neighborhood with interactive maps |
| **[Web Data Toolkit](skills/web-search-tools/)** | Search, scrape, extract, map, and crawl any website — plus build reusable extraction agents that run at scale |

**Business Research**, **Marketing**, and **Productivity** skills are one-command workflows. They spawn parallel sub-agents, gather live web data via Nimble APIs, synthesize findings, and deliver structured reports with dates and source URLs. They learn from previous runs and only surface what's new.

These skills also extend into specific industries — starting with **[Healthcare](skills/healthcare/)**: extract structured practitioner data from practice websites, enrich provider lists with missing fields, and verify credentials against the NPI registry.

**Web Data Toolkit** skills expose Nimble's raw capabilities for any web task. They also power the business skills under the hood — and form a feedback loop: web-expert runs agents built by agent-builder, and when a one-off lookup becomes recurring, agent-builder turns it into a reusable pipeline.

## Quick Start

### 1. Install the Nimble CLI

```bash
npm i -g @nimble-way/nimble-cli
```

### 2. Set your API key

[Sign up](https://online.nimbleway.com/signup) and grab your key from Account Settings > API Keys.

```bash
export NIMBLE_API_KEY="your-api-key-here"
```

Or add it permanently to `~/.claude/settings.json`:

```json
{ "env": { "NIMBLE_API_KEY": "your-api-key-here" } }
```

### 3. Add the skills

**Claude Code:**

```bash
claude mcp add --transport http nimble-mcp-server https://mcp.nimbleway.com/mcp \
  --header "Authorization: Bearer ${NIMBLE_API_KEY}"
```

> Restart Claude Code after running this — MCP servers added mid-session aren't available until the next launch.

**Cursor:**

```
/add-plugin nimble
```

Or clone the repo and open it in Cursor — the plugin system auto-discovers skills from `.cursor-plugin/plugin.json`.

**npx skills CLI:**

```bash
npx skills add Nimbleway/agent-skills
```

To install a single skill:

```bash
npx skills add Nimbleway/agent-skills --skill competitor-intel
```

To list available skills:

```bash
npx skills add Nimbleway/agent-skills --list
```

### 4. Try it

```bash
# Business intelligence — ask a question, get a sourced report
"What are my competitors doing this week?"
"Prepare me for my meeting with Jane from Acme Corp"

# Web data toolkit — get data from any website
"Scrape the pricing page at example.com"
nimble search --query "AI agent frameworks" --max-results 10
```

## How It Works

Nimble Web Search Skills follow a shared pattern: **preflight** (check CLI, load profile) → **parallel research** (spawn sub-agents for concurrent data gathering) → **analysis** (synthesize findings, deduplicate against previous runs) → **report** (structured output with sources) → **distribute** (offer Notion/Slack delivery).

Core skills expose the Nimble CLI directly — search, extract, map, crawl, and manage extraction agents.

### Local Web Knowledge Wiki

Skills maintain a local web knowledge wiki at `~/.nimble/memory/` — live web intelligence that compounds across sessions, so your agent never starts from scratch. Inspired by [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): an AI-maintained, human-owned knowledge base that gets smarter with every run.

- **Local-first indexes** — per-directory entity catalogs for instant lookup, no vector DB needed
- **Obsidian-compatible** — `[[wiki links]]` cross-reference people, companies, and competitors. Open `~/.nimble/memory/` in Obsidian to browse your intelligence graph
- **Cross-entity synthesis** — patterns across competitors, pricing trends, and market signals are surfaced automatically
- **Ad-hoc insights** — say "remember this" mid-conversation and it compounds into the right entity page
- **Activity log** — grep-friendly record of what was learned, when, and by which skill

Every finding carries a verified event date and source URL. Stale signals are dropped, not reported — your context is always current.

### Platform Compatibility

| Aspect | Claude Code | Cursor | npx skills |
| ------ | ----------- | ------ | ---------- |
| Plugin config | `.claude-plugin/` | `.cursor-plugin/` | N/A (reads `skills/`) |
| MCP config | `.mcp.json` | `mcp.json` | Manual setup |
| Rules | N/A | `rules/*.mdc` | N/A |
| Skills | `skills/` (shared) | `skills/` (shared) | `skills/` (shared) |

All platforms read the same `skills/` directory. Platform-specific files coexist without interference.

### CLI Commands

| Command | Description |
| ------- | ----------- |
| `nimble search --query "<q>"` | Real-time web search |
| `nimble extract --url "<url>" --format markdown` | Extract content from a URL |
| `nimble map --url "<url>" --limit 20` | Discover URLs on a site |
| `nimble crawl run --url "<url>" --limit 50` | Crawl a website section |
| `nimble agent list --limit 100` | Browse available extraction agents |
| `nimble agent run --agent <name> --params '{...}'` | Execute an extraction agent |

## Contributing

Have a web data workflow that should be one command? We'd love new skills — whether it's sales prospecting, lead enrichment, or anything that turns web data into action. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to build and publish your own.

## Links

- **Nimble**: [nimbleway.com](https://www.nimbleway.com)
- **Documentation**: [docs.nimbleway.com](https://docs.nimbleway.com)
- **Issues**: [github.com/Nimbleway/agent-skills/issues](https://github.com/Nimbleway/agent-skills/issues)
- **Email**: support@nimbleway.com

## License

MIT License — see [LICENSE](LICENSE) for details.

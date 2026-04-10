# ZoomInfo Plugin for Claude Cowork

Search companies and contacts, enrich leads, find similar companies and contacts, and get AI-ranked prospect recommendations — all from inside [Claude Cowork](https://claude.ai/cowork).

This plugin connects Claude to the [ZoomInfo](https://www.zoominfo.com) MCP server, giving it access to ZoomInfo's B2B intelligence platform through a set of purpose-built skills.

## Prerequisites

- [Claude Cowork](https://claude.ai/cowork)
- A ZoomInfo account with API access

## Installation

Install from the Cowork plugin marketplace, or clone this repo and point Cowork at it:

```bash
git clone https://github.com/zoominfo/zi-mcp-plugin.git
```

## Skills

| Skill | Description |
|---|---|
| **enrich-company** | Look up a company's full profile — firmographics, financials, corporate structure, growth signals |
| **enrich-contact** | Look up a person's professional profile — title, department, contact details, accuracy score |
| **recommend-contacts** | Get AI-powered contact recommendations at a target company based on your ZoomInfo interaction history |
| **build-list** | Build a targeted contact or company list from natural language criteria |
| **find-similar** | Find companies or contacts similar to a reference, ranked by similarity score |

## How it works

The plugin registers ZoomInfo's hosted MCP server (`https://mcp.zoominfo.com/mcp`) and exposes the skills above as natural-language workflows. Each skill orchestrates multiple ZoomInfo API calls — lookups, searches, enrichment, similarity — and formats the results into actionable output.

No API keys are configured in this repo. Authentication is handled through your ZoomInfo session.

## Project structure

```
.claude-plugin/
  plugin.json          # Plugin metadata (name, version, description, keywords)
  marketplace.json     # Marketplace listing configuration
.mcp.json              # MCP server registration
skills/
  build-list/          # Each skill is a directory with a SKILL.md
  enrich-company/
  enrich-contact/
  find-similar/
  recommend-contacts/
```

## License

[MIT](LICENSE)

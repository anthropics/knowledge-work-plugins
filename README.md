# Acoustic Plugins

Plugins that turn Claude into a specialist for your role, team, and Acoustic workflows. Built for [Claude Cowork](https://claude.com/product/cowork), also compatible with [Claude Code](https://claude.com/product/claude-code).

Acoustic is a marketing automation and cross-channel engagement platform. These plugins are tuned for the teams and workflows that run Acoustic's business — from marketing and sales to finance and legal.

## Why Plugins

Cowork lets you set the goal and Claude delivers finished, professional work. Plugins let you go further: tell Claude how you like work done, which tools and data to pull from, how to handle critical workflows, and what slash commands to expose — so your team gets better and more consistent outcomes.

Each plugin bundles the skills, connectors, slash commands, and sub-agents for a specific job function. Out of the box, they give Claude a strong starting point for helping anyone in that role. The real power comes when you customize them for Acoustic — your tools, your terminology, your processes — so Claude works like it was built for your team.

## Plugin Marketplace

| Plugin | How it helps | Connectors |
|--------|-------------|------------|
| **[marketing](./marketing)** | Draft content, plan campaigns, enforce brand voice, brief on competitors, and report on performance across channels. | Slack, Canva, Figma, HubSpot, Amplitude, Notion, Ahrefs, SimilarWeb |
| **[sales](./sales)** | Research prospects, prep for calls, review your pipeline, draft outreach, and build competitive battlecards. | Slack, HubSpot, Close, Clay, ZoomInfo, Notion, Jira, Fireflies, Microsoft 365 |
| **[customer-support](./customer-support)** | Triage tickets, draft responses, escalate issues, and build your knowledge base. Research customer context and turn resolved issues into self-service content. | Slack, Intercom, HubSpot, Guru, Jira, Notion, Microsoft 365 |
| **[product-management](./product-management)** | Write feature specs, plan roadmaps, and synthesize user research faster. Keep stakeholders updated and stay ahead of the competitive landscape. | Slack, Linear, Asana, Monday, ClickUp, Jira, Notion, Figma, Amplitude, Pendo, Intercom, Fireflies |
| **[legal](./legal)** | Review contracts, triage NDAs, navigate compliance, assess risk, prep for meetings, and draft templated responses. | Slack, Box, Egnyte, Jira, Microsoft 365 |
| **[finance](./finance)** | Prep journal entries, reconcile accounts, generate financial statements, analyze variances, manage close, and support audits. | Snowflake, Databricks, BigQuery, Slack, Microsoft 365 |
| **[cowork-plugin-management](./cowork-plugin-management)** | Create new plugins or customize existing ones for Acoustic's specific tools and workflows. | — |

## Getting Started

### Cowork

Install plugins from [claude.com/plugins](https://claude.com/plugins/).

### Claude Code

```bash
# Add the marketplace first
claude plugin marketplace add acoustic/knowledge-work-plugins

# Then install a specific plugin
claude plugin install marketing@knowledge-work-plugins
```

Once installed, plugins activate automatically. Skills fire when relevant, and slash commands are available in your session (e.g., `/marketing:draft-content`, `/sales:call-prep`).

## How Plugins Work

Every plugin follows the same structure:

```
plugin-name/
├── .claude-plugin/plugin.json   # Manifest
├── .mcp.json                    # Tool connections
├── commands/                    # Slash commands you invoke explicitly
└── skills/                      # Domain knowledge Claude draws on automatically
```

- **Skills** encode the domain expertise, best practices, and step-by-step workflows Claude needs to give you useful help. Claude draws on them automatically when relevant.
- **Commands** are explicit actions you trigger (e.g., `/finance:reconciliation`, `/product-management:write-spec`).
- **Connectors** wire Claude to the external tools your role depends on — CRMs, project trackers, data warehouses, design tools, and more — via [MCP servers](https://modelcontextprotocol.io/).

Every component is file-based — markdown and JSON, no code, no infrastructure, no build steps.

## Making Them Yours

These plugins are starting points for Acoustic. They become much more useful when you customize them for how our company actually works:

- **Swap connectors** — Edit `.mcp.json` to point at your specific tool stack.
- **Add company context** — Drop Acoustic's terminology, org structure, and processes into skill files so Claude understands our world.
- **Adjust workflows** — Modify skill instructions to match how your team actually does things.
- **Build new plugins** — Use the `cowork-plugin-management` plugin or follow the structure above to create plugins for roles and workflows not yet covered.

## Building

To package each plugin into a deployable zip:

```bash
./build.sh
```

Output zips are written to `build/` (one per plugin). The `build/` directory is excluded from version control.

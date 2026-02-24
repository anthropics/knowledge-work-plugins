# Apollo Plugin for Claude Code and Cowork

Prospect, enrich leads, and load outreach sequences with [Apollo.io](https://www.apollo.io/) — powered by the Apollo MCP Server with **one-click integration**.

---

## 🔌 One-Click MCP Server Integration

This plugin **automatically configures the Apollo MCP Server** when installed. No manual server setup, no config files to edit - just install the plugin and authenticate with your Apollo Account.

---

## ✅ Powerful Skills

This plugin ships with high-value skills that chain multiple Apollo APIs into complete workflows:

| Skill | What it does |
|---|---|
| `/apollo:enrich-lead` | Drop a name, LinkedIn URL, or email — get a full contact card with email, phone, company intel, and next actions |
| `/apollo:prospect` | Describe your ICP in plain English — get a ranked table of enriched decision-maker leads |
| `/apollo:sequence-load` | Find leads, enrich them, and bulk-load into an outreach sequence — handles dedup and enrollment |

### `/apollo:enrich-lead`

Drop in a name, company, LinkedIn URL, or email — get back a complete contact card with email, phone, title, location, company details, and suggested next actions. Handles fuzzy lookups (e.g. "CEO of Figma") and falls back to search when exact match fails.

### `/apollo:prospect`

Describe your ICP in plain English. The pipeline searches for matching companies, bulk-enriches firmographic data, finds decision makers, reveals contact info via bulk enrichment, and returns a ranked lead table with ICP fit scores.

### `/apollo:sequence-load`

Find contacts matching your targeting criteria, enrich them, create them as contacts with deduplication, and bulk-add them to an existing Apollo sequence. Previews candidates before enrollment and shows a full summary after.

---

## 📦 Installation

### Cowork

Click the link below to install in one step:

[Install in Cowork](https://claude.ai/desktop/customize/plugins/new?marketplace=apolloio/apollo-mcp-plugin&plugin=apollo)

Then restart Cowork to ensure the MCP server starts correctly.

### Claude Code

#### 1. Add this plugin's marketplace

In Claude Code, run:

```
/plugin marketplace add apolloio/apollo-mcp-plugin
```

#### 2. Install the plugin

```
/plugin install apollo@apollo-plugin-marketplace
```

#### 3. Restart Claude Code

This ensures the MCP server starts correctly.

---

## 🔑 Authentication

The Apollo MCP Server supports **OAuth**:

1. After installation, run `/mcp` in Claude Code or Cowork
2. Select the **Apollo** server and click **Authenticate**
3. Complete the Apollo.io login in your browser
4. Done — all commands are now ready to use

---

## ⚠️ Apollo Credits

Some operations consume [Apollo credits](https://docs.apollo.io/):

- **People enrichment** (used by all three skills) costs 1 credit per person
- **Bulk enrichment** (`/apollo:prospect`, `/apollo:sequence-load`) consumes 1 credit per person in the batch
- The plugin will always warn you before consuming credits

---

## 🙌 Credits

- **MCP Server** by [Apollo.io](https://docs.apollo.io/)
- **Plugin Specification** by [Anthropic](https://docs.anthropic.com/)

---

## License

MIT — see [LICENSE](LICENSE) for details.

# nimble-agent-builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Find, generate, update, and run structured-data agents on the Nimble platform. Discover existing agents for 50+ sites, update them for new fields, or create custom ones from scratch — all via natural language.

## What it does

| Task                       | Example                                                |
| -------------------------- | ------------------------------------------------------ |
| Discover an existing agent | "Find an agent for Amazon product pages"               |
| Run an agent interactively | "Get data for ASIN B08N5WRWNW"                         |
| Update an agent            | "Add customer reviews field to the Amazon agent"       |
| Generate a new agent       | "Build an agent for Etsy product listings"             |
| Generate a batch script    | "Write a Python script to extract 500 Zillow listings" |

## Requirements

- **Nimble API key** — [online.nimbleway.com/signup](https://online.nimbleway.com/signup)
- **Nimble CLI** — for all operations (`nimble agent list/get/run/generate/publish`)
- **Nimble MCP server** (optional fallback) — used only when CLI is not installed

## Setup

See [Installation in the root README](../../README.md#installation) for CLI install and API key setup.

### Connect the Nimble MCP server

#### Claude Code

```bash
claude mcp add --transport http nimble-mcp-server https://mcp.nimbleway.com/mcp \
  --header "Authorization: Bearer ${NIMBLE_API_KEY}"
```

> **Restart Claude Code after running this** — MCP servers added mid-session aren't available until the next launch.

#### Cursor / VS Code (Copilot / Continue)

```json
{
  "nimble-mcp-server": {
    "command": "npx",
    "args": [
      "-y",
      "mcp-remote@latest",
      "https://mcp.nimbleway.com/mcp",
      "--header",
      "Authorization:Bearer YOUR_API_KEY"
    ]
  }
}
```

## How it works

The skill has two tool groups depending on what you need:

**All operations use the Nimble CLI:**

| Action | Command |
| --- | --- |
| Search for an agent | `nimble agent list --limit 100` → filtered by domain |
| Inspect its schema | `nimble agent get --template-name <name>` → shows fields + params |
| Run it | `nimble agent run --agent <name> --params '{...}'` → returns structured data |
| Create a new agent | `nimble agent generate --agent-name <name> --prompt "..." --url "..."` |
| Refine an existing agent | `nimble agent generate --from-agent <name> --prompt "..."` |
| Poll generation status | `nimble agent get-generation --generation-id <id>` |
| Publish | `nimble agent publish --agent-name <name> --version-id <id>` |

Once published, the agent is immediately available to `nimble agent run` — and to **nimble-web-expert**'s agent check.

**Key rules:**

- Always search for an existing agent before generating — update a close match rather than building from scratch
- Agent creation (generate → poll → publish) runs in a background Task agent because generation takes 1-3 minutes
- MCP tools are available as a fallback when CLI is not installed
- For one-off fetches or web searches, use **nimble-web-expert** instead

## Reference files

| File                                        | Purpose                                                    |
| ------------------------------------------- | ---------------------------------------------------------- |
| `references/agent-api-reference.md`         | CLI + MCP tool reference, input parameter mapping          |
| `references/sdk-patterns.md`                | Python SDK patterns, async endpoint, batch pipelines       |
| `references/rest-api-patterns.md`           | REST API for TypeScript, Node, curl                        |
| `references/batch-patterns.md`              | Multi-store comparison, normalization, codegen walkthrough |
| `references/generate-update-and-publish.md` | Full agent lifecycle: create → poll → validate → publish   |
| `references/error-recovery.md`              | Error handling, quota limits, fallback hierarchy           |

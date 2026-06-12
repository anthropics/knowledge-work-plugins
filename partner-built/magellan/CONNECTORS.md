# Connectors

Magellan is a **self-contained** knowledge discovery plugin. It does not require
connections to external SaaS tools to function — all knowledge extraction, graph
building, and querying happens locally using the files in your workspace.

## Optional Tool Integrations

While the core pipeline is self-contained, you can optionally connect external tools
to enhance Magellan's workflows:

| Category | Use Case | Example Tools |
|----------|----------|---------------|
| ~~project-tracker~~ | Route open questions to your team as tickets | Jira, Linear, Asana, GitHub Issues |
| ~~chat~~ | Send contradiction summaries to team channels | Slack, Microsoft Teams |
| ~~knowledge-base~~ | Fetch referenced documents from team wikis | Confluence, Notion, Guru |

These integrations are **tool-agnostic** — any MCP server in the category works.
Add the relevant MCP servers to your `.mcp.json` to enable them.

## No Required Connectors

Unlike plugins that depend on external data sources, Magellan works entirely from
local files. Point it at a folder of collected materials (code, documents, transcripts,
diagrams) and it builds the knowledge graph from those files directly.

## System Requirements

Magellan has no system requirements beyond Claude Code. It reads files directly
using Claude's built-in capabilities — no external tools needed.

> **Note:** Claude does not yet natively read DOCX, PPTX, or XLSX files. Until it
> does, convert these to PDF before adding them to your workspace.

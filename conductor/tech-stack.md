# Tech Stack

## Plugin Architecture

### Core Technologies
- **Markdown** - Skills and commands content
- **JSON** - Manifests and connector configs
- **YAML Frontmatter** - Command metadata

### File Structure
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: name, version, description
├── .mcp.json                # Optional: MCP server configs
├── README.md                # Plugin documentation
├── CONNECTORS.md            # Connector documentation
├── commands/
│   └── <command>.md         # Slash commands with YAML frontmatter
└── skills/
    └── <skill>/
        └── SKILL.md         # Skill definitions
```

### Manifest Schema (plugin.json)
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description"
}
```

### Command Format
```markdown
---
name: command-name
description: What it does
arguments:
  - name: arg1
    description: Argument description
---

Command content/instructions here.
```

### Skill Format
```markdown
# Skill Name

Description and instructions for Claude to follow.
```

## MCP Integration

Servers configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio|sse|http",
      "command": "...",
      "args": [...]
    }
  }
}
```

## Distribution

- GitHub-based marketplace
- Versioned via git tags
- Install via `claude plugin install <name>@<marketplace>`

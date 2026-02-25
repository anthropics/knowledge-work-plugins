# Plugin Architecture

This document explains how Claude Cowork and Claude Code plugins are structured and how they work together.

## Plugin Structure

Every plugin follows this directory structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin manifest (name, description, version)
├── .mcp.json            # MCP server connections for external tools
├── README.md            # Plugin documentation
├── CONNECTORS.md        # Guide to available tool connections
├── LICENSE              # License file
├── commands/            # Slash commands (explicit user actions)
│   ├── command-one.md
│   └── command-two.md
└── skills/              # Domain knowledge (automatic context)
    ├── skill-one/
    │   ├── SKILL.md
    │   └── references/  # Supporting files
    └── skill-two/
        └── SKILL.md
```

## Component Overview

### Plugin Manifest (`.claude-plugin/plugin.json`)

Defines plugin metadata:

- `name`: Plugin identifier
- `description`: What the plugin does
- `version`: Semantic version number

### MCP Configuration (`.mcp.json`)

Connects Claude to external tools via [Model Context Protocol](https://modelcontextprotocol.io/). Defines which servers to connect (CRMs, databases, project trackers, etc.).

### Commands (`commands/`)

Markdown files that define **explicit slash commands** users invoke directly.

- Triggered by typing `/plugin:command-name`
- Contains step-by-step workflow instructions
- Specifies expected inputs and outputs
- References skills automatically when needed

See [Commands vs Skills](./COMMANDS_VS_SKILLS.md) for details.

### Skills (`skills/`)

Markdown files containing **domain knowledge** Claude uses automatically.

- Activated when relevant to the conversation
- Contains best practices, terminology, and expertise
- Can include reference files in subdirectories
- Not invoked directly by users

See [Commands vs Skills](./COMMANDS_VS_SKILLS.md) for details.

## How Claude Loads Plugins

1. **Plugin Discovery**: Claude scans for plugins in the configured directories
2. **Manifest Reading**: Loads `plugin.json` to register the plugin
3. **Command Registration**: Makes all commands available as slash commands
4. **Skill Loading**: Indexes all skills for contextual retrieval
5. **MCP Connection**: Establishes connections to configured external tools

## How Commands and Skills Interact

When a user invokes a command:

1. Claude reads the command file for the workflow
2. Claude automatically retrieves relevant skills based on context
3. Claude executes the workflow using both command instructions and skill knowledge
4. External tools are accessed via MCP connections as needed

```
User: /legal:review-contract

Claude loads:
├── commands/review-contract.md    ← Workflow steps
├── skills/contract-review/        ← Domain expertise (automatic)
└── .mcp.json                      ← Tool connections (Box, Slack, etc.)
```

## Customization Points

Plugins use `~~` prefixes to mark customizable placeholders:

```markdown
Send the summary to ~~your-team-channel
```

These can be replaced with organization-specific values during setup.

## Related Documentation

- [Commands vs Skills](./COMMANDS_VS_SKILLS.md) - Detailed comparison
- [README](../README.md) - Getting started guide

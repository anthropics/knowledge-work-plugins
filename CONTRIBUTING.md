# Contributing to Knowledge Work Plugins

Thank you for your interest in contributing to Knowledge Work Plugins! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Plugin Structure](#plugin-structure)
- [Development Guidelines](#development-guidelines)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project follows the [Anthropic Community Guidelines](https://www.anthropic.com/community-guidelines). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Plugin name and version**
- **Claude Code/Cowork version**
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear title** for the issue
- **Provide detailed description** of the proposed enhancement
- **Explain why this would be useful** to most users
- **List examples** of how it would work

### Contributing New Plugins

We welcome new plugins that add value to specific roles or workflows:

1. Review existing plugins for inspiration
2. Ensure your plugin serves a clear use case
3. Follow the plugin structure guidelines below
4. Include comprehensive documentation
5. Test thoroughly before submitting

### Contributing to Existing Plugins

Improvements to existing plugins are always welcome:

- Bug fixes
- Documentation improvements
- New skills or commands
- Better examples
- Connector additions

## Getting Started

### Prerequisites

- Git installed
- [Claude Code](https://claude.com/product/claude-code) or [Claude Cowork](https://claude.com/product/cowork)
- Text editor (VS Code recommended)
- Basic knowledge of Markdown and JSON

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/knowledge-work-plugins.git
   cd knowledge-work-plugins
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/anthropics/knowledge-work-plugins.git
   ```

### Testing Your Changes

#### With Claude Code

```bash
# Install your local plugin
claude plugin add ./path/to/your-plugin

# Test commands
/your-plugin:command-name

# Verify skills activate correctly
```

#### With Claude Cowork

1. Navigate to Settings → Plugins
2. Click "Load Local Plugin"
3. Select your plugin directory
4. Test functionality

## Plugin Structure

Every plugin must follow this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin metadata
├── .mcp.json                # Optional: MCP server connections
├── commands/                # Optional: Slash commands
│   └── command-name.md
├── skills/                  # Optional: Auto-triggered skills
│   └── skill-name/
│       └── SKILL.md
├── README.md                # Required: Plugin documentation
├── CONNECTORS.md            # Recommended: Tool placeholder guide
└── LICENSE                  # Required: Apache 2.0
```

### Required Files

#### plugin.json

```json
{
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "Clear, concise description of what this plugin does",
  "author": {
    "name": "Your Name"
  }
}
```

**Requirements**:
- `name`: lowercase, hyphen-separated (e.g., "data-analysis")
- `version`: Semantic versioning (e.g., "1.0.0")
- `description`: 1-2 sentences, under 200 characters
- `author.name`: Your name or organization

#### README.md

Must include:
- Plugin title and tagline
- Installation instructions
- What it does (with/without connectors)
- Commands table
- Skills table
- Example workflows
- Connector information

See [sales/README.md](./sales/README.md) for a great example.

#### LICENSE

All plugins must use Apache 2.0 license. Copy from existing plugin.

### Optional Files

#### Commands

Commands are slash commands users invoke explicitly.

**File**: `commands/command-name.md`

**Format**:
```markdown
---
description: Brief description of what this command does
argument-hint: "<what user should provide>"
---

# /command-name

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

[Detailed documentation...]

## Usage

```
/command-name [arguments]
```

## How It Works

[Explanation with diagrams if helpful]

## What I Need From You

[Required inputs]

## Output

[Expected output format]
```

#### Skills

Skills are automatically triggered based on context.

**File**: `skills/skill-name/SKILL.md`

**Format**:
```markdown
---
name: skill-name
description: When this skill triggers and what it does. Include trigger phrases.
---

# Skill Name

[Clear explanation of what this skill does]

## How It Works

[Flow diagram showing standalone vs connected modes]

## Getting Started

[What the user needs to provide]

## Execution Flow

[Step-by-step workflow]

## Output Format

[Expected output structure]

## Related Skills

[Links to related skills]
```

#### .mcp.json

Defines MCP server connections.

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://example.com/mcp"
    }
  }
}
```

#### CONNECTORS.md

Explains the `**category**` placeholder system.

See [sales/CONNECTORS.md](./sales/CONNECTORS.md) for template.

## Development Guidelines

### Writing Skills

1. **Make them work standalone first**
   - Don't require connectors
   - Ask users for needed information
   - Provide graceful degradation

2. **Supercharge with connectors**
   - Show "standalone vs supercharged" modes
   - Use `**category**` placeholders (e.g., `**CRM**`, `**email**`)
   - Document which connectors add what value

3. **Be specific about execution**
   - Provide step-by-step flows
   - Show example queries to connectors
   - Include error handling guidance

4. **Focus on outcomes**
   - What does the user get?
   - What format?
   - What can they do with it?

### Writing Commands

1. **Clear purpose**
   - One command = one clear action
   - Descriptive name (e.g., `/sales:call-prep` not `/sales:prep`)

2. **Flexible input**
   - Accept various input formats
   - Don't force rigid structure
   - Provide examples

3. **Rich output**
   - Structured, actionable results
   - Include next steps
   - Reference related commands

### Connector Integration

1. **Use category placeholders**
   - `**CRM**` not "Salesforce"
   - `**email**` not "Gmail"
   - `**chat**` not "Slack"

2. **Document in CONNECTORS.md**
   - What category means
   - Example servers
   - What data they provide

3. **Graceful fallbacks**
   - Always work without connectors
   - Show what's missing
   - Suggest what to connect

### Documentation

1. **Write for humans**
   - Clear, concise language
   - Avoid jargon
   - Include examples

2. **Show, don't tell**
   - Use diagrams and tables
   - Provide example outputs
   - Include workflow illustrations

3. **Keep it practical**
   - Real-world scenarios
   - Common use cases
   - Actual problems solved

## Submitting Changes

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow style guidelines
   - Update documentation
   - Test thoroughly

3. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: clear description"
   ```
   
   Good commit messages:
   - "Fix markdown formatting in sales plugin"
   - "Add account research skill to sales plugin"
   - "Update README with connector examples"
   
   Bad commit messages:
   - "fix stuff"
   - "update"
   - "wip"

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use the PR template
   - Link related issues
   - Describe what changed and why
   - Include screenshots if UI-related
   - Request review from maintainers

### Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] All JSON files are valid
- [ ] All markdown files render correctly
- [ ] Documentation is updated
- [ ] Examples are included
- [ ] Plugin has been tested locally
- [ ] No sensitive data in commits
- [ ] Commit messages are clear
- [ ] PR description is complete

## Style Guidelines

### Markdown

- Use ATX headers (`#`, `##`, not underlines)
- One blank line between sections
- Code blocks with language tags
- No trailing whitespace
- Lists use `-` for bullets, `1.` for numbers
- Tables use GitHub-flavored markdown
- Links use reference style for readability
- **Do not use strikethrough (`~~text~~`) for placeholders**
- Use bold for category placeholders: `**CRM**`, `**email**`, etc.

### JSON

- 2-space indentation
- No trailing commas
- Use double quotes
- Alphabetize keys when logical
- Validate before committing

### File Naming

- Lowercase with hyphens: `call-prep.md`
- Descriptive names: `competitive-intelligence.md` not `ci.md`
- Match command/skill name exactly

### Command and Skill Names

- Lowercase with hyphens
- Action-oriented: `write-query`, `call-prep`
- Clear and specific
- Namespace with plugin: `/sales:call-prep`

## Questions?

- **Documentation**: Check existing plugins for examples
- **Technical**: Open a GitHub issue
- **General**: Use GitHub Discussions
- **Private**: Email plugins@anthropic.com

## Recognition

Contributors will be recognized in:
- CHANGELOG.md (for significant contributions)
- GitHub contributors page
- Plugin author field (for new plugins)

Thank you for contributing! 🎉

---
name: create-plugin
description: >
  Guide users through creating a new Cursor plugin from scratch.
  Use when users want to create a plugin, build a plugin, make a new plugin, develop a plugin, scaffold a plugin, start a plugin from scratch, or design a plugin.
---

# Create Cursor Plugin

Build a new Cursor plugin from scratch through guided conversation. Walk the user through discovery, planning, design, implementation, and packaging — delivering a ready-to-install plugin directory at the end.

## Overview

A plugin is a self-contained directory that extends Cursor's AI capabilities with skills, rules, agents, hooks, and MCP server integrations. This skill encodes the full plugin architecture and a five-phase workflow for creating one conversationally.

The process:

1. **Discovery** — understand what the user wants to build
2. **Component Planning** — determine which component types are needed
3. **Design & Clarifying Questions** — specify each component in detail
4. **Implementation** — create all plugin files
5. **Review & Deliver** — validate and install the plugin

> **Nontechnical output**: Keep all user-facing conversation in plain language. Do not expose implementation details like file paths, directory structures, or schema fields unless the user asks. Frame everything in terms of what the plugin will do.

## Plugin Architecture

### Directory Structure

Every Cursor plugin follows this layout:

```
plugin-name/
├── .cursor-plugin/
│   └── plugin.json           # Required: plugin manifest
├── skills/                   # Skills (subdirectories with SKILL.md)
│   └── skill-name/
│       ├── SKILL.md
│       └── references/
├── rules/                    # Always-on guidance (.mdc files)
│   └── rule-name.mdc
├── agents/                   # Subagent definitions (.md files)
├── mcp.json                  # MCP server definitions
└── README.md                 # Plugin documentation
```

> **Legacy `commands/` format**: Older plugins may include a `commands/` directory with single-file `.md` slash commands. This format still works, but new plugins should use `skills/*/SKILL.md` instead — Cursor presents both as a single "Skills" concept, and the skills format supports progressive disclosure via `references/`.

**Rules:**

- `.cursor-plugin/plugin.json` is always required
- Component directories (`skills/`, `rules/`, `agents/`) go at the plugin root, not inside `.cursor-plugin/`
- Only create directories for components the plugin actually uses
- Use kebab-case for all directory and file names

### plugin.json Manifest

Located at `.cursor-plugin/plugin.json`. Minimal required field is `name`.

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name"
  }
}
```

**Name rules:** kebab-case, lowercase with hyphens, no spaces or special characters.
**Version:** semver format (MAJOR.MINOR.PATCH). Start at `0.1.0`.

Optional fields: `homepage`, `repository`, `license`, `keywords`.

Custom component paths can be specified (supplements, does not replace, auto-discovery):

```json
{
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp.json"
}
```

### Component Schemas

Detailed schemas for each component type are in `references/component-schemas.md`. Summary:

| Component  | Location            | Format                      |
| ---------- | ------------------- | --------------------------- |
| Skills     | `skills/*/SKILL.md` | Markdown + YAML frontmatter |
| Rules      | `rules/*.mdc`       | Markdown + YAML frontmatter |
| MCP Servers | `mcp.json`         | JSON                        |
| Agents     | `agents/*.md`       | Markdown + YAML frontmatter |
| Hooks      | `hooks/hooks.json`  | JSON                        |
| Commands (legacy) | `commands/*.md` | Markdown + YAML frontmatter |

**Skills** are the most useful component for Cursor users. **Scaffold new plugins with `skills/*/SKILL.md` as the primary component.**

**Rules** are always-on guidance that Cursor applies automatically to every chat session with the plugin active — useful for persistent coding standards or project conventions.

### Customizable plugins with `~~` placeholders

> **Do not use or ask about this pattern by default.** Only introduce `~~` placeholders if the user explicitly says they want people outside their organization to use the plugin.

When a plugin is intended to be shared with others outside their company, parts may need to be adapted to individual users. Use generic language and mark customization points with two tilde characters such as `create an issue in ~~project tracker`.

If used, write a `CONNECTORS.md` file at the plugin root to explain:

```markdown
# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user
connects in that category. Plugins are tool-agnostic — they describe
workflows in terms of categories rather than specific products.

## Connectors for this plugin

| Category        | Placeholder         | Options                         |
| --------------- | ------------------- | ------------------------------- |
| Chat            | `~~chat`            | Slack, Microsoft Teams, Discord |
| Project tracker | `~~project tracker` | Linear, Asana, Jira             |
```

### ${PLUGIN_ROOT} Variable

Use `${PLUGIN_ROOT}` for all intra-plugin path references in hooks and MCP configs. Never hardcode absolute paths.

## Guided Workflow

When you ask the user something, use AskUserQuestion. Don't assume "industry standard" defaults are correct. Note: AskUserQuestion always includes a Skip button and a free-text input box for custom answers, so do not include `None` or `Other` as options.

### Phase 1: Discovery

**Goal**: Understand what the user wants to build and why.

Ask (only what is unclear — skip questions if the user's initial request already answers them):

- What should this plugin do? What problem does it solve?
- Who will use it and in what context?
- Does it integrate with any external tools or services?
- Is there a similar plugin or workflow to reference?

Summarize understanding and confirm before proceeding.

**Output**: Clear statement of plugin purpose and scope.

### Phase 2: Component Planning

**Goal**: Determine which component types the plugin needs.

Based on the discovery answers, determine:

- **Skills** — Does it need specialized knowledge that the AI should load on-demand, or user-initiated actions? (domain expertise, reference schemas, workflow guides, deploy/configure/analyze/review actions)
- **Rules** — Should certain guidance always be active when the plugin is loaded? (coding standards, project conventions, persistent context)
- **MCP Servers** — Does it need external service integration? (databases, APIs, SaaS tools)
- **Agents (uncommon)** — Are there autonomous multi-step tasks? (validation, generation, analysis)
- **Hooks (rare)** — Should something happen automatically on certain events? (enforce policies, load context, validate operations)

Present a component plan table, including component types you decided not to create:

```
| Component | Count | Purpose |
|-----------|-------|---------|
| Skills    | 3     | Domain knowledge for X, /do-thing, /check-thing |
| Rules     | 1     | Always-on coding standard Y |
| Agents    | 0     | Not needed |
| Hooks     | 0     | Not needed |
| MCP       | 1     | Connect to service Z |
```

Get user confirmation or adjustments before proceeding.

**Output**: Confirmed list of components to create.

### Phase 3: Design & Clarifying Questions

**Goal**: Specify each component in detail. Resolve all ambiguities before implementation.

For each component type in the plan, ask targeted design questions. Present questions grouped by component type. Wait for answers before proceeding.

**Skills:**

- What user queries should trigger this skill?
- What knowledge domains does it cover?
- Should it include reference files for detailed content?
- If the skill represents a user-initiated action: what arguments does it accept, and what tools does it need?

**Rules:**

- Should the rule always apply, or only for specific file globs?
- What guidance should it enforce?

**Agents:**

- Should each agent trigger proactively or only when requested?
- What tools does it need?
- What should the output format be?

**Hooks:**

- Which events? (PreToolUse, PostToolUse, Stop, SessionStart, etc.)
- What behavior — validate, block, modify, add context?
- Prompt-based (LLM-driven) or command-based (deterministic script)?

**MCP Servers:**

- What server type? (stdio for local, HTTP for REST APIs)
- What authentication method?
- What tools should be exposed?

If the user says "whatever you think is best," provide specific recommendations and get explicit confirmation.

**Output**: Detailed specification for every component.

### Phase 4: Implementation

**Goal**: Create all plugin files following best practices.

**Order of operations:**

1. Create the plugin directory structure
2. Create `.cursor-plugin/plugin.json` manifest
3. Create each component (see `references/component-schemas.md` for exact formats)
4. Create `README.md` documenting the plugin

**Implementation guidelines:**

- **Skills** use progressive disclosure: lean SKILL.md body (under 3,000 words), detailed content in `references/`. Frontmatter description must be third-person with specific trigger phrases. Skill bodies are instructions FOR the AI, not messages to the user — write them as directives about what to do.
- **Rules** go in `rules/<rule-name>.mdc` with frontmatter `description`, `alwaysApply: true` (or `false` with `globs`). Keep rules concise and actionable.
- **Agents** need a description with `<example>` blocks showing triggering conditions, plus a system prompt in the markdown body.
- **Hooks** config goes in `hooks/hooks.json`. Use `${PLUGIN_ROOT}` for script paths. Prefer prompt-based hooks for complex logic.
- **MCP configs** go in `mcp.json` at plugin root. Use `${PLUGIN_ROOT}` for local server paths. Document required env vars in README.

### Phase 5: Review & Deliver

**Goal**: Validate and deliver the finished plugin.

1. Summarize what was created — list each component and its purpose
2. Ask if the user wants any adjustments
3. Validate the plugin structure manually:
   - `.cursor-plugin/plugin.json` exists and contains valid JSON with at least a `name` field
   - The `name` field is kebab-case (lowercase letters, numbers, and hyphens only)
   - Any component directories referenced by the plugin actually exist and contain files in the expected formats
   - Each skill subdirectory contains a `SKILL.md` with `name` and `description` frontmatter
   - Each rule file has valid frontmatter with `description` and `alwaysApply`
   - Report what passed and what didn't

   Fix any errors before proceeding.

4. Deliver the plugin by telling the user:

```
Plugin ready at: <path-to-plugin-directory>

To install in Cursor, copy the directory to your local plugins folder:
  cp -r <plugin-name> ~/.cursor/plugins/local/<plugin-name>/

Cursor will pick it up automatically — no restart required.
```

## Best Practices

- **Start small**: Begin with the minimum viable set of components. A plugin with one well-crafted skill is more useful than one with five half-baked components.
- **Progressive disclosure for skills**: Core knowledge in SKILL.md, detailed reference material in `references/`, working examples in `examples/`.
- **Clear trigger phrases**: Skill descriptions should include specific phrases users would say. Agent descriptions should include `<example>` blocks.
- **Skills are for the AI**: Write skill body content as instructions for the AI to follow, not documentation for the user to read.
- **Rules are always-on**: Use rules for guidance that should always apply, skills for knowledge that activates on demand.
- **Imperative writing style**: Use verb-first instructions in skills ("Parse the config file," not "You should parse the config file").
- **Portability**: Always use `${PLUGIN_ROOT}` for intra-plugin paths, never hardcoded paths.
- **Security**: Use environment variables for credentials, HTTPS for remote servers, least-privilege tool access.

## Additional Resources

- **`references/component-schemas.md`** — Detailed format specifications for every component type (skills, rules, agents, hooks, MCP, legacy commands, CONNECTORS.md)
- **`references/example-plugins.md`** — Three complete example plugin structures at different complexity levels

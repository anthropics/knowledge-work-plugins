# Fastly Agent Toolkit

A collection of skills for AI coding agents to work with the Fastly platform and edge computing tools.

## Available skills

- `fastly`: Working with the Fastly platform, including services, caching, VCL, WAF, TLS, DDoS protection, purging, and API usage.
- `fastly-cli`: Using the Fastly CLI to manage services, compute apps, logging, WAF, TLS, key-value stores, and stats.
- `falco`: VCL development with Falco, covering linting, testing, simulation, formatting, REPL, and Terraform integration.
- `fastlike`: Running Fastly Compute locally with Fastlike (Go-based), covering backend configuration, builds, and testing.
- `viceroy`: Running Fastly Compute locally with Viceroy (WASM-based), covering serving, configuration, testing, and SDK adaptation.
- `xvcl`: The XVCL VCL transpiler, covering syntax extensions, subroutines, header manipulation, and caching logic.

Each skill lives under `skills/` with a `SKILL.md` entrypoint and a `references/` directory containing detailed topic files.

**Important:** SKILL.md files reference companion files in their `references/` directory. Make sure your agent is allowed to read from these directories, otherwise it won't be able to follow the references and will miss important context.

## Usage

Pick the skills relevant to your project. You probably don't need all of them.

### Using the `skills` CLI (recommended)

The [`skills`](https://github.com/vercel-labs/skills) CLI installs skills into the standard `.agents/skills/` directory and automatically symlinks them into agent-specific directories. It supports most agents out of the box.

Install into the current project:

```bash
bunx skills add github:fastly/fastly-agent-toolkit --skill falco --skill viceroy
# or with node:
npx skills add github:fastly/fastly-agent-toolkit --skill falco --skill viceroy
```

Install globally (available across all projects via `~/.agents/skills/`):

```bash
bunx skills add -g github:fastly/fastly-agent-toolkit --skill falco --skill viceroy
```

### Manual copy

If your agent supports the `.agents/skills/` convention, this is the most portable option. Agents that use this location include Amp, Cline, Codex, Cursor, Gemini CLI, GitHub Copilot, Kimi Code, OpenCode, Replit Agent, Swival, and Warp.

Install into the current project:

```bash
mkdir -p .agents/skills
cp -R ./skills/{falco,viceroy} .agents/skills/
```

Install globally (for agents that support `~/.agents/skills/`):

```bash
mkdir -p ~/.agents/skills
cp -R ./skills/{falco,viceroy} ~/.agents/skills/
```

If your agent doesn't support `.agents/skills/`, use its agent-specific location below.

### Claude Code

#### Plugin Marketplace

```bash
claude plugin install fastly-agent-toolkit@claude-plugins-official
claude plugin list

# If this fails, add skills manually in the next section.
```

#### Manual

```bash
mkdir -p .claude/skills
cp -R ./skills/{falco,viceroy} .claude/skills/
```

For a quick local setup, the manual copy is more reliable since it doesn't depend on the marketplace.

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/{falco,viceroy} ~/.codex/skills/
```

### Swival

Swival scans project-local `.swival/skills/` first, then `.agents/skills/`. For global installs, prefer `~/.config/swival/skills/`.

Project-local install:

```bash
mkdir -p .swival/skills
cp -R ./skills/{falco,viceroy} .swival/skills/
```

Global install:

```bash
mkdir -p ~/.config/swival/skills
cp -R ./skills/{falco,viceroy} ~/.config/swival/skills/
```

### Qwen Code

Qwen Code requires the experimental skills feature. Enable it by adding to `.qwen/settings.json`:

```json
{
  "tools": {
    "experimental": {
      "skills": true
    }
  }
}
```

Then copy skills to the project directory:

```bash
mkdir -p .qwen/skills
cp -R ./skills/{falco,viceroy} .qwen/skills/
```

### Gemini CLI

Gemini CLI supports `.agents/skills/` as shown above. You can also link the whole repository using Gemini's extension workflow:

```bash
gemini extensions link .
```

Swap `{falco,viceroy}` for whatever combination you need. For VCL work, `falco` and `xvcl` are the most useful. For Fastly Compute, grab `fastly-cli` and either `viceroy` or `fastlike`.

## Skill format

Each skill lives in its own directory as a `SKILL.md` file with YAML frontmatter following the [Agent Skills spec](https://agentskills.io/specification).

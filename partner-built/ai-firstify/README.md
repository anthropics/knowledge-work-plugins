# ai-firstify

Audit, re-engineer, or bootstrap projects to align with AI-first design principles. Based on the 9 design principles and 7 design patterns from the [TechWolf AI-First Bootcamp](https://ai-first.techwolf.ai).

## Install

```bash
# Add the TechWolf marketplace (once)
claude plugin marketplace add techwolf-ai/ai-first-toolkit

# Install the plugin
claude plugin install ai-firstify@techwolf-ai-first
```

### Codex

```bash
./install.sh ai-firstify
```

Update, uninstall, or verify:

```bash
./install.sh update ai-firstify
./install.sh uninstall ai-firstify
./install.sh verify ai-firstify
```

For Codex, this plugin installs:

- `ai-firstify`

The installer also writes plugin metadata into the installed skill directory and copies a Codex guidance file into `~/.codex/skills/.techwolf-ai-first/plugins/ai-firstify/`.

## Usage

The skill triggers automatically when you ask Claude Code to:

- **Audit** a project: "review", "audit", "analyze", "assess"
- **Re-Engineer** a project: "ai-firstify", "fix", "improve", "transform"
- **Bootstrap** a new project: "start", "new project", "bootstrap", "build from scratch"

Or invoke directly:

```
/ai-firstify
```

## Modes

1. **Audit**: Read-only analysis across 7 dimensions with a scored report
2. **Re-Engineer**: Full audit followed by active fixes in 7 phases
3. **Bootstrap**: Interactive new project setup with discovery questions

## License

This project is licensed under the [MIT License](../../LICENSE).

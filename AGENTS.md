---
adapter_metadata:
  skill_name: knowledge-work-plugins
  skill_version: 1.0.0
  last_synced: 2026-02-14
  source_path: README.md
  adapter_id: codex-cli
  adapter_format: AGENTS.md
---

# Knowledge Work Plugins (agents manifest)

This repository contains a wide-ranging collection of specialized agentic skills for professional "knowledge work" across various domains including Legal, Finance, Marketing, Product Management, Customer Support, and more.

## Capability

The collection provides domain-specific expertise and workflows:
- ⚖️ **Legal**: Contract review, compliance, legal risk assessment, NDA triage.
- 💰 **Finance**: Audit support, reconciliation, financial statements, variance analysis.
- 📣 **Marketing**: Brand voice, campaign planning, competitive analysis, content creation.
- 📦 **Product Management**: Feature specs, metrics tracking, roadmap management, user research.
- 🎧 **Customer Support**: Ticket triage, response drafting, customer research, escalation.
- 🏢 **Real Estate**: Property analysis, lead management, compliance closer.
- 🏛️ **Ministerial Audit**: Bureaucracy redliner, strategic synthesis, comms translator.

Skills are organized by category in `<category>/skills/<skill-name>/SKILL.md`.

## Context

This file serves as the **Agents.md** standard manifest for discovery and indexing of professional knowledge work plugins.

### Repository structure

- `[category]/`
  - `skills/`
    - `[skill-name]/SKILL.md`: The core logic for each specialized skill.
- `scripts/`
  - `sync_plugins.py`: Automation to distribute these skills to local tool environments.

### Core instructions

When tasked with professional knowledge work:
1. Identify the most relevant domain category (e.g., Legal, Finance).
2. Select the appropriate skill within that category.
3. Follow the specialized workflows and best practices defined in its `SKILL.md`.

## Maintenance

To sync these plugins to your local agentic tool directories (Cline, Kilo, Amp, etc.), run:

```bash
python scripts/sync_plugins.py
```

## Interoperability

These skills are compatible with any agent following the `SKILL.md` standard, including Antigravity, Cline, Kilo Code, Amp, and OpenCode.

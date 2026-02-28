---
description: "Display BetterCallClaude plugin version, installed components, and system status"
---

# BetterCallClaude Version and Status

When this command is invoked, display the plugin status report below. Check actual MCP server availability by attempting to list their tools. Replace status indicators accordingly.

## Status Report

Output the following formatted block:

```
======================================================
  BetterCallClaude - Swiss Legal Intelligence Plugin
======================================================
  Version:      3.1.0
  Format:       Claude Code Plugin (Cowork compatible)
  Author:       Federico Cesconi
  License:      MIT
======================================================

  COMMANDS (17)
  -------------
  [x] legal          - Intelligent gateway and router
  [x] research       - BGE/ATF/DTF precedent search
  [x] strategy       - Litigation strategy and risk
  [x] draft          - Legal document generation
  [x] federal        - Federal law mode
  [x] cantonal       - Cantonal law mode
  [x] cite           - Citation formatting
  [x] doc-analyze    - Document analysis
  [x] precedent      - Precedent chain analysis
  [x] validate       - Batch citation validation
  [x] adversarial    - Three-agent adversarial analysis
  [x] workflow       - Multi-agent pipeline execution
  [x] briefing       - Structured pre-execution briefing
  [x] translate      - Legal translation DE/FR/IT/EN
  [x] setup          - MCP server configuration
  [x] version        - This status display
  [x] help           - Command reference

  AGENTS (18)
  -----------
  [x] researcher      [x] strategist     [x] drafter
  [x] citation        [x] compliance     [x] data-protection
  [x] risk            [x] procedure      [x] translator
  [x] fiscal          [x] corporate      [x] cantonal
  [x] realestate      [x] advocate       [x] adversary
  [x] judicial        [x] briefing       [x] orchestrator

  SKILLS (10)
  ----------
  [x] swiss-legal-research     [x] swiss-legal-drafting
  [x] swiss-legal-strategy     [x] swiss-citation-formats
  [x] swiss-jurisdictions      [x] privacy-routing
  [x] federal-law              [x] cantonal-law
  [x] multilingual-law         [x] legal-briefing

  MCP SERVERS (5)
  ---------------
  [ ] entscheidsuche    - Swiss court decision search
  [ ] bge-search        - Federal Supreme Court decisions
  [ ] legal-citations   - Citation verification
  [ ] fedlex-sparql     - Federal legislation database
  [ ] onlinekommentar   - Legal commentary access

  Run /bettercallclaude:setup to configure MCP servers

  LANGUAGES
  ---------
  [x] German (DE)   - OR, ZGB, StGB, BGE
  [x] French (FR)   - CO, CC, CP, ATF
  [x] Italian (IT)  - CO, CC, CP, DTF
  [x] English (EN)  - Swiss-specific terminology

  JURISDICTIONS
  -------------
  [x] Federal law (Bundesrecht)
  [x] All 26 Swiss cantons supported

  SYSTEM REQUIREMENTS
  -------------------
  - Claude Code or Cowork with plugin support
  - MCP servers: optional but recommended for citation verification
  - No API keys required for core functionality
  - MCP servers require Node.js 18+ if running locally

======================================================
  https://github.com/fedec65/BetterCallClaude
======================================================
```

For each MCP server, attempt to verify availability:
- If tools from that server respond, mark as `[x]` (active).
- If tools are unavailable, mark as `[ ]` (not configured).

If the user asks a follow-up question, answer it in context of the version and status information.

## User Query

$ARGUMENTS

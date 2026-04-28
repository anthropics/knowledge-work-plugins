# Land Grow Plugin

A consulting methodology plugin for [Cowork](https://claude.com/product/cowork) and Claude Code — built around the Land Grow business consulting framework for Brazilian SMEs. Run full diagnostic pipelines, build integrated business models, and prepare client sessions without leaving your AI workspace.

## Installation

```bash
claude plugins add land-grow
```

## Commands

| Command | Description |
|---|---|
| `/grow-start` | Run the GROW Start 4-agent pipeline — transform a session transcript into a complete cash generation framework (7-30 days) |
| `/grow-360` | Run the GROW 360 5-agent diagnostic pipeline — full business maturity analysis across 10 sectors, generating 4 BIN deliverables (Horizon, Compass, Radar, Route Planner) plus a 90-day execution plan |
| `/min` | Build the MIN (Integrated Business Model) — 13 blocks across 3 phases (Foundation, Operation, Consolidation). Requires completed GROW 360 BIN |
| `/client-session` | Prepare for a client session — generate diagnostic questions, structured agenda, and post-session processing for any Land Grow product |

## Skills

| Skill | Description |
|---|---|
| `grow-start` | 4-agent pipeline for quick cash diagnosis: Data Analyst → Cash Strategist → Senior Manager → Delivery Architect |
| `grow-360` | 5-agent robust diagnostic pipeline: Data Analyst → BIN Horizon → BIN Compass → BIN Radar → BIN Route Planner |
| `min` | 3-phase Integrated Business Model: Foundation Architect → Operation Architect → Consolidation Architect |

## Land Grow Ecosystem

The three products follow a progression:

```
GROW START
Quick cash diagnosis. For businesses with immediate cash problems.
Input: session transcript
Output: 30-day attack plan with ready-to-use scripts
Timeline: 7-30 days
        ↓
GROW 360 (BIN)
Full maturity diagnosis across 10 sectors.
Input: Google Forms export + session transcript
Output: Horizon + Compass + Radar + Route Planner deliverables
Timeline: 2-4 weeks
        ↓
MIN (Integrated Business Model)
Build the operating model from diagnosis to structured framework.
Input: completed BIN + phase forms + session transcripts
Output: 13-block business model across 3 phases
Timeline: 3-6 weeks
```

## Example Workflows

### Running GROW Start

```
> /grow-start
Client: Maria Silva | Neighborhood boutique | São Paulo | 3 years

[Paste session transcript here]
```

Claude will activate the 4-agent pipeline sequentially: Data Analyst → Cash Strategist → Senior Manager → Delivery Architect. Final output is a complete GROW Start document ready for consultant review before client delivery.

### Running GROW 360

```
> /grow-360
Client: João Costa | Services | Consulting firm | 12 employees

[Paste Google Forms export]
[Paste session transcript]
```

Claude will run all 5 BIN agents in sequence, producing the complete set of deliverables: Horizon (strategic direction), Compass (10-sector maturity matrix), Radar (40 prioritized actions), and Route Planner (90-day execution map).

### Building the MIN

```
> /min
Client: Ana Lima | Retail | Phase 1
BIN: [paste complete BIN]
Form: [paste Phase 1 form responses]
Transcript: [paste Phase 1 session transcript]
```

Claude will build all 6 Foundation blocks with maturity assessment, coherence check, and transfer notes for Phase 2.

### Preparing a Client Session

```
> /client-session
Product: GROW 360
Client: Pedro Alves | Industry | First diagnostic session
Known: mid-sized manufacturer, 3-year decline in margin
```

Claude will generate tailored diagnostic questions, a structured session agenda with time blocks, and the live audit dynamics most relevant to this client profile.

## Methodology Notes

### GROW 360 — BIN Maturity Matrix

The Compass agent uses a 5×10 matrix to assess 10 business sectors:

**Sectors:** Operational, HR, Financial, Administrative, Marketing, Sales, Strategic, Legal, Leadership, Innovation

**Stages:**
- Stage 1 Germination: no process, improvised
- Stage 2 Sprouting: fragile, exists rudimentarily
- Stage 3 Growth: functional with manual effort
- Stage 4 Flourishing: consistent results, not person-dependent
- Stage 5 Fruition: competitive differentiator, autonomous

### GROW 360 — Radar Scoring Formula

```
Base Score = (V×3) + (D×2) + (C×2) + I
Final Score = (Base × FV÷5) + BF
```

Where: V=Velocity (weight 3), D=Difficulty (weight 2), C=Complexity (weight 2), I=Impact (weight 1), FV=Behavioral Viability Factor (1-5), BF=Revenue Bonus (0, 1, or 2).

### MIN — Block Maturity Scale

Each of the 13 blocks is assessed as: **Nonexistent** → **Draft** → **Functional** → **Optimized**

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

This plugin works with the following MCP servers:

- **Google Calendar** — Schedule client sessions and follow-up reminders
- **Gmail** — Send diagnostic reports and client deliverables
- **Google Drive** — Access and upload client session transcripts and forms
- **Notion** — Access and store client briefs and methodology documents

All core pipelines work without any MCP connections — they only require you to paste the necessary inputs directly in the chat.

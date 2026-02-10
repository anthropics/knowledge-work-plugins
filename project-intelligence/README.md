# Project Intelligence

**Surface patterns in any team's work — code, documents, designs, or compliance artifacts.**

A composable skill set that analyzes project data across disciplines and surfaces factual, data-driven observations for retrospectives, quality gates, release decisions, and process improvement.

> **A note on terminology:** These skills use the word **"story"** to mean any trackable unit of work — whether your team calls them stories, tasks, tickets, cards, work items, or issues. If it moves through columns on a board or has a lifecycle status, it's a story here.

---

## What This Does

**For Retrospectives:**
Generate comparative observations about cycle time, throughput, blockers, and team patterns — formatted for import into Miro, Mural, or Jira boards.

**For Quality Gates:**
Summarize check results for any deliverable — CI builds, document reviews, design critiques, compliance audits — and recommend a clear action: proceed, block, retry, or escalate.

**For Flow Diagnosis:**
Identify why stories, tickets, or tasks are stalled. Distinguish blockers from unclear specs, split needs, and external dependencies.

**For Release Decisions:**
Aggregate signals across quality checks, open risks, schedule status, and team readiness to inform go/no-go decisions.

---

## Available Skills

### Aggregators

| Skill | Purpose | Status |
|-------|---------|--------|
| `sprint-retro-input` | Generate factual observations for retrospectives | ✅ Ready |
| `release-readiness` | Go/no-go assessment for any milestone, launch, or deadline | ✅ Ready |

### Input Skills

| Skill | What It Analyzes | Status |
|-------|-----------------|--------|
| `story-flow` | Why stories/tickets exceed cycle time targets | ✅ Ready |
| `quality-check` | Check results for any deliverable (code, docs, design, compliance) | ✅ Ready |
| `activity-audit` | Reported status vs actual activity in any source | ✅ Ready |
| `risk-tracker` | Risks, issues, and blockers across the project | ✅ Ready |
| `standup-notes` | Artifact-driven status updates, multiple per day | ✅ Ready |
| `schedule-forecast` | Milestone burndown, throughput trends, completion confidence | ✅ Ready |
| `dependency-readiness` | External/internal dependency status for milestones | ✅ Ready |
| `stakeholder-signoff` | Approval tracking with enablement verification | ✅ Ready |
| `change-summary` | Tiered changelog: major milestone, minor milestone, review delta | ✅ Ready |

*Input skills work standalone or feed into aggregators.*

### Agents (Delegated Specialists)

| Agent | Used By | Purpose |
|-------|---------|---------|
| `git-activity` | `activity-audit` | Detect commit patterns: churn, stalled, workarounds |
| `document-activity` | `activity-audit` | Detect document revision patterns (template — customize for your platform) |

---

## Quick Start

### Manual Input (No Setup Required)

```
Analyze sprint 14 for our retrospective.

Sprint 14 stories:
- DEV-88: "API rate limiting" — 28hr cycle time
- DES-34: "Redesign onboarding flow" — 52hr cycle time
- LEGAL-12: "Update privacy policy for EU launch" — 44hr cycle time
- MKT-67: "Write Q2 campaign brief" — 18hr cycle time

8 stories completed, avg cycle time 31hr
7 blockers (3 on LEGAL-12 — external counsel delays)
Previous 3 sprints averaged 36hr cycle time and 10 stories completed.
Team norms: cycle time <48hr, WIP limit 5
```

### Automated (With Connectors)

```
Analyze sprint 14. Fetch from ~~project tracker and ~~code repository.
```

See [CONNECTORS.md](./CONNECTORS.md) for tool setup.

---

## Architecture

```
┌───────────────────────────────┐
│   INPUT SKILLS                │  ← Analyze individual data sources
│  (Modular Collectors)         │
├───────────────────────────────┤
│ • story-flow                  │
│ • quality-check               │
│ • activity-audit ──┐          │
│ • risk-tracker     │          │
│ • standup-notes    │          │
│ • schedule-forecast│          │
│ • dependency-readiness        │
│ • stakeholder-signoff         │
│ • change-summary              │
└────────────────────┼──────────┘
                     │
               ┌─────┴──────────────┐
               │  AGENTS             │  ← Domain-specific signal detection
               │  (Delegated)        │
               ├─────────────────────┤
               │ • git-activity      │
               │ • document-activity │
               └─────────────────────┘
                     │
                     ↓
┌───────────────────────────────┐
│   AGGREGATORS                 │  ← Synthesize for specific decisions
│  (Analysis & Synthesis)       │
├───────────────────────────────┤
│ • sprint-retro-input          │
│ • release-readiness           │
└──────────────┬────────────────┘
               │
               ↓
┌───────────────────────────────┐
│   OUTPUT                      │  ← Formatted for your workflow
├───────────────────────────────┤
│ Markdown (default) · JSON     │
│ CSV · Plain text              │
└───────────────────────────────┘
```

---

## Plugin Configuration

| File | Purpose |
|------|---------|
| [CONNECTORS.md](./CONNECTORS.md) | Where your **tools** live — Jira, GitHub, Slack, etc. |
| [REFERENCES.md](./REFERENCES.md) | Where your **standards** live — brand guidelines, contract templates, SOC 2 matrix |
| [output-styles/](./output-styles/) | How skills **format output** — `[DATA]` prefix, comparison format, severity tags |

---

## Use Cases

### Engineering Teams
- Sprint retrospectives with cycle time analysis
- CI/CD quality gate summaries
- PR review bottleneck detection
- Release readiness checks

### Design Teams
- Design review feedback triage (blockers vs. style preferences)
- Accessibility audit summaries
- Brand compliance checks against the design system

### Legal & Compliance
- Vendor audit check summaries
- Contract review comment triage
- Regulatory finding classification and escalation

### Marketing & Product
- Campaign iteration analysis
- Content review feedback summaries
- Product spec clarity diagnosis

### Leadership
- Cross-functional sprint health
- Quality gate trend analysis
- Process improvement tracking

---

## Design Principles

1. **Multidisciplinary** — Same patterns work for code, documents, designs, and compliance artifacts
2. **Modularity** — Input skills are independent building blocks; use standalone or combine via aggregators
3. **Graceful Degradation** — Works with full automation, partial automation, or manual input
4. **Factual Voice** — No opinions. Observations start with `[DATA]` and include baseline comparisons
5. **Tool Agnostic** — Uses `~~` connector placeholders. Adapts to whatever tools your team runs
6. **Canonical Sources** — Checks against configured reference documents, not arbitrary search results

---

## Example Output

```markdown
# Sprint Retrospective Input | Sprint 14

**Sources:** manual input
**Baseline:** Sprints 11-13

---

### Cycle Time Improvement — success
[DATA] Avg cycle time decreased 14% to 31hr (vs 36hr baseline). Within <48hr norm.

### Throughput Drop — risk
[DATA] 8 stories completed (-20% vs 10-story baseline).

### Blocker Spike — improvement
[DATA] 7 blockers (+133% vs 3 baseline). 3 of 7 concentrated on LEGAL-12 (external counsel delays).
```

---

## Getting Help

**First time?** Start with `sprint-retro-input` and manual input. Once comfortable, add connectors for automation and configure reference sources for your team's standards.

**Tool setup?** See [CONNECTORS.md](./CONNECTORS.md)

**Reference standards?** See [REFERENCES.md](./REFERENCES.md)

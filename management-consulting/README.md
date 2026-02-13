# Management Consulting Plugin

An end-to-end management consulting workflow plugin for strategy, operations, and transformation engagements. Models proven methodologies for strategy, operations, and transformation work. Works standalone with web search and your input, supercharged when you connect your tools.

> **Disclaimer:** This plugin assists with consulting workflows. All analyses and recommendations should be reviewed by qualified professionals before client presentation.

## Installation

```bash
claude plugins add knowledge-work-plugins/management-consulting
```

## Commands

Explicit workflows invoked with a slash command:

### Business Development

| Command | Description |
|---|---|
| `/rfp-analyze` | Analyze RFP requirements, evaluation criteria, and win themes |
| `/proposal-develop` | Create compelling proposal with value proposition and approach |
| `/sow-create` | Develop detailed Statement of Work with scope and deliverables |
| `/pitch-deck` | Build client pitch deck with storytelling and key messages |
| `/value-proposition` | Develop differentiated value propositions and positioning |

### Engagement Initiation

| Command | Description |
|---|---|
| `/kickoff` | Design and run project kickoff workshop and charter |
| `/discovery` | Conduct discovery phase with stakeholder interviews and data gathering |
| `/governance-setup` | Establish project governance including RACI and steering committee |
| `/stakeholder-map` | Map stakeholders, assess influence, and develop engagement strategies |

### Research & Analysis

| Command | Description |
|---|---|
| `/framework-apply` | Apply strategic frameworks (7S, Five Forces, SWOT, PESTLE) |
| `/market-analysis` | Conduct industry and competitive analysis |
| `/financial-analysis` | Build financial models, ROI analysis, and business cases |
| `/due-diligence` | Conduct commercial, operational, or strategic due diligence |

### Strategy Development

| Command | Description |
|---|---|
| `/options-generate` | Generate and evaluate strategic options |
| `/business-case` | Develop investment business case with financials |
| `/roadmap-create` | Create strategic roadmap with phases and milestones |

### Implementation

| Command | Description |
|---|---|
| `/implementation-plan` | Develop detailed implementation plan |
| `/change-plan` | Create change management and communication plan |
| `/process-improve` | Apply Lean Six Sigma for process optimization |
| `/org-design` | Design organizational structure and roles |

### Deliverables

| Command | Description |
|---|---|
| `/presentation-create` | Build executive presentation with storytelling |
| `/report-generate` | Create strategic reports and recommendations |
| `/workshop-facilitate` | Design and facilitate strategy workshops |
| `/thought-leadership` | Develop POVs, white papers, case studies, and knowledge assets |

### Project Management

| Command | Description |
|---|---|
| `/status-report` | Generate weekly or monthly status reports |
| `/risk-register` | Identify, assess, and manage project risks |
| `/project-close` | Execute project closure and knowledge transfer |

### Commercial

| Command | Description |
|---|---|
| `/pricing-model` | Develop consulting pricing (fixed, T&M, value-based) |

## Skills

Domain knowledge Claude uses automatically when relevant:

| Skill | Description |
|---|---|
| `problem-solving` | Hypothesis-driven problem solving using structured analysis |
| `strategic-frameworks` | Application of 20+ consulting frameworks |
| `workshop-facilitation` | Design thinking and innovation sprint facilitation |
| `executive-presentation` | Top-down structured communication and storytelling for C-suite |
| `financial-modeling` | ROI, NPV, DCF, and business case development |
| `change-management` | Organizational change management and transformation |
| `process-excellence` | Lean Six Sigma and operational improvement |
| `project-governance` | RACI, steering committees, and stage gates |
| `due-diligence` | Commercial, operational, and strategic assessment |

## Example Workflows

### Strategy Engagement

```
/kickoff [Project Name] [Client]
```

Run kickoff to define project charter and governance, then:
- Map stakeholders with `/stakeholder-map`
- Conduct discovery with `/discovery`
- Apply frameworks with `/framework-apply`
- Conduct analysis with `/financial-analysis` and `/market-analysis`
- Generate options with `/options-generate`
- Build business case with `/business-case`
- Create roadmap with `/roadmap-create`

### Transformation Engagement

```
/discovery [Organization context]
```

Conduct current state assessment, then:
- Design future state with `/org-design` and `/process-improve`
- Develop implementation plan with `/implementation-plan`
- Create change plan with `/change-plan`
- Execute with regular `/status-report` updates
- Close with `/project-close` and lessons learned

### Pursuit / Business Development

```
/rfp-analyze [RFP content]
```

Analyze the RFP, then:
- Develop proposal with `/proposal-develop`
- Create SOW with `/sow-create`
- Build pitch deck with `/pitch-deck`

## Standalone + Supercharged

Every command works without integrations:

| What You Can Do | Standalone | Supercharged With |
|---|---|---|
| Conduct analysis | Web search + your input | Data warehouse, BI tools |
| Build financial models | Describe assumptions | Excel, financial data |
| Create presentations | Describe content | Office suite, cloud storage |
| Research markets | Web search | Industry databases |
| Manage projects | Describe status | Jira, project tools |

## MCP Integrations

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your tools for a richer experience:

| Category | Examples | What It Enables |
|---|---|---|
| **Chat** | Slack, Teams | Client updates, team coordination |
| **Cloud storage** | Box, Egnyte, Google Drive | Access templates, save deliverables |
| **Office suite** | Microsoft 365, Google Workspace | Email, documents, presentations |
| **Project tracker** | Jira, Confluence | Status tracking, milestone management |

## Settings

Create a local settings file at `management-consulting/.claude/settings.local.json` to personalize:

```json
{
  "firm": {
    "name": "Your Firm",
    "methodology": "hypothesis-driven",
    "standard_frameworks": ["7S", "Five Forces", "SWOT"]
  },
  "engagement_defaults": {
    "pricing_model": "value-based",
    "reporting_format": "executive-summary"
  }
}
```

The plugin will ask you for this information interactively if not configured.

# Management Consulting Plugin

A management consulting plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Covers the full engagement lifecycle from problem definition through implementation and closeout. Helps with hypothesis-driven analysis, business cases, client deliverables, change management, and project governance. Works with any consulting team — standalone with your input, supercharged when you connect your project tracker, knowledge base, and other tools.

## Installation

```bash
claude plugins add knowledge-work-plugins/management-consulting
```

## Skills

Domain knowledge Claude draws on automatically when your work touches consulting topics:

| Skill | Description |
|---|---|
| `strategic-analysis` | Hypothesis-driven decomposition, issue trees, MECE analysis, and named framework application (Five Forces, PESTLE, 7S, VRIO, etc.) |
| `financial-modeling` | Business case math, ROI/NPV/IRR, sensitivity analysis |
| `client-deliverables` | Consulting reports, executive presentations, top-down structured communication, storylining, data visualization |
| `change-management` | Transformation planning, resistance management, adoption tracking |
| `due-diligence` | Commercial, operational, and strategic assessment |
| `engagement-setup` | Kickoff planning, discovery phase, stakeholder mapping |
| `implementation-planning` | Options evaluation, business cases, roadmaps, implementation plans |
| `org-design` | Operating model and organizational structure design |
| `engagement-pricing` | Pricing consulting engagements: fee structures, rate cards, commercial terms |
| `process-excellence` | DMAIC, value stream mapping, process improvement |
| `project-closeout` | Deliverable handover, lessons learned, transition planning |
| `project-governance` | RACI, steering committees, stage gates, status reporting, risk tracking |
| `proposal-development` | RFP analysis, proposal writing, SOW creation, pitch decks |
| `thought-leadership` | POVs, white papers, case studies, research content |
| `workshop-facilitation` | Workshop design, facilitation techniques, participant engagement |

## Example Workflows

### Scoping a new engagement

Start with the problem. Describe the client situation and what they're asking for:

```
A mid-market SaaS company is losing enterprise deals to a competitor.
They want to understand why and what to do about it.
Help me structure the engagement.
```

The `strategic-analysis` skill kicks in to build an issue tree and hypotheses. `engagement-setup` helps plan the discovery phase and stakeholder mapping. `proposal-development` can then turn that into a scoped SOW with workstreams, timeline, and pricing.

### Building a strategic recommendation

You've done the analysis and need to pull it together:

```
We've completed our market analysis for the client's expansion into Southeast Asia.
Here are our findings: [paste or upload data].
Help me build the recommendation deck.
```

`strategic-analysis` structures the analysis (market attractiveness, competitive positioning). `financial-modeling` builds the business case with scenarios. `client-deliverables` shapes the storyline, slide structure, and detailed appendix.

### Running a transformation programme

The client has approved the strategy and you're into implementation:

```
We're restructuring the client's supply chain operations across 3 regions.
12-month programme, 4 workstreams, steering committee meets monthly.
Help me set up the governance and tracking.
```

`project-governance` builds the RACI, stage gates, and reporting cadence. `change-management` maps stakeholder impact and resistance risks. `implementation-planning` lays out the roadmap with dependencies. `workshop-facilitation` helps design the kickoff sessions with regional teams.

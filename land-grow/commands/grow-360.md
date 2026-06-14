---
description: Run the GROW 360 robust diagnostic pipeline — full business maturity analysis across 10 sectors, generating the 4 BIN deliverables (Horizon, Compass, Radar, Route Planner) and a 90-day execution plan
argument-hint: "<client name, Google Forms export, and session transcript>"
---

# GROW 360

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Run the Land Grow GROW 360 pipeline: a 5-agent sequential chain that transforms a Google Forms diagnostic export and session transcript into the complete BIN (Business Intelligence Network) — 4 structured deliverables plus a 90-day execution plan.

## Trigger

User runs `/grow-360` or asks to run a GROW 360, full diagnostic, BIN analysis, maturity diagnosis, or mentions Horizon / Compass / Radar / Route Planner for a client.

## When to Use GROW 360 vs. GROW Start

- **GROW Start**: client has immediate cash problem, needs results in 7-30 days, no previous diagnosis
- **GROW 360**: client is structuring continuous consulting, needs complete diagnosis before a strategic plan, or is ready for the full maturity analysis

## Inputs

Gather the following before proceeding:

1. **Google Forms export** — the structured question+answer export from the GROW 360 diagnostic form. Mandatory.

2. **Session transcript** — the full transcript from the diagnostic deepening session (Fireflies or Otter). Mandatory.

3. **Client context** — name, sector (Retail / Services / Industry), sub-sector, size (revenue + employees).

If any input is missing, ask before running any agent.

## Pipeline

Run each agent in sequence. Do not skip steps. Each agent's output feeds the next.

### Agent 1: Data Analyst

Activate the `grow-360` skill and run **Agent 1: Data Analyst**:

1. **Sector identification**: sector, sub-sector, size
2. **Form extraction** by thematic block (Retail: Identification, Operations, HR, Finance, Marketing, Administrative, Strategic, Sales, Innovation, Legal, Leadership; Services: Tools, Pricing, Productivity, Innovation, Marketing, Finance, Partnerships, Personalization, Risks, HR; Industry: Production, Quality, Maintenance, Automation, Sustainability, Costs, HR, Technology)
3. **Transcript extraction**: client's verbatim objectives (in quotes), spontaneous problems, stories, fears, contradictions
4. **Cross-reference and contradictions** by type: Direct Contradiction, Relevant Omission, Minimization, Exaggeration
5. **Objectives hierarchy**: Primary, Secondary, Hidden (inferred), timeline, client's success metric

Deliver: Dossier GROW 360 with 4 sections (objectives, thematic diagnosis, contradiction table, synthesis for agents). No recommendations.

### Agent 2: BIN Horizon

Run **Agent 2: BIN Horizon** with the Dossier:

1. **Horizon**: declare objective, timeline, metric — reformulate if vague
2. **Tailwinds (3-5)**: forces that move toward the objective with evidence
3. **Anchors (3-5)**: forces that move away from the objective — Anchor 1 marked PRIORITY
4. **Strategic Focus 90 Days**: [most critical anchor to remove] + [strongest tailwind to leverage] + expected result — a movement declaration, not a list

Deliver: Horizon deliverable with transfer block for Compass.

### Agent 3: BIN Compass

Run **Agent 3: BIN Compass** with Dossier + Horizon:

Apply the 5×10 maturity matrix:

**10 Sectors**: Operational, HR, Financial, Administrative, Marketing, Sales, Strategic, Legal, Leadership, Innovation

**5 Stages**:
- Stage 1 GERMINATION: sector does not exist, improvised, no process
- Stage 2 SPROUTING: exists rudimentarily, fragile, breaks under pressure
- Stage 3 GROWTH: works with some consistency, dependent on manual effort
- Stage 4 FLOURISHING: well-structured, consistent results, not person-dependent
- Stage 5 FRUITION: competitive differentiator, autonomous, above-market results

Numerical score: Stage × 20 (0-100 scale).

Protocol:
1. Read Dossier Section 2 + Horizon anchors/tailwinds
2. Position each sector (evidence, stage, next step)
3. Predominant stage (weighted average: Financial, Operational, Commercial = weight 1.5)
4. Weighted SWOT (origin, weight High/Medium/Low, fact or hypothesis)
5. Analysis by executive chair (COO/CFO/CMO/CEO — 2 lines each)
6. Focus pie (100 points distributed across 10 sectors)

Deliver: Compass deliverable with maturity matrix, anchor and strength sectors, SWOT, executive chair analysis, focus pie, 3 strategic questions for the consultant, transfer block for Radar.

### Agent 4: BIN Radar

Run **Agent 4: BIN Radar** with Dossier + Horizon + Compass:

Scoring formula:
- Variables: V (Velocity, weight 3), D (Difficulty, weight 2), C (Complexity, weight 2), I (Impact, weight 1) — all 1-5 scale
- FV (Behavioral Viability Factor): 1=high resistance/impossible → 5=client already does something similar
- BF (Revenue Bonus): 2=direct revenue impact in 30 days, 1=indirect 31-90 days, 0=structural no direct impact
- **Formula**: `Base Score = (V×3) + (D×2) + (C×2) + I` | `Final Score = (Base × FV÷5) + BF`

Health scale by sector: 0-20 Critical, 21-40 Poor, 41-60 Fair, 61-80 Good, 81-100 Excellent

3 Blocks:
- **QUICK WINS** (FV≥4, execute now)
- **BASE** (FV=3, 90 days with support)
- **TRANSFORMATION** (FV≤2, 180-365 days)

Generate 40 actions (minimum 35), minimum 3 per anchor sector. Score and justify each. Track dependencies (D-: depends on another, D+: others depend on this, Neutral).

Deliver: Radar deliverable with sector health panorama, 3 blocks of prioritized actions, executive summary, transfer block for Route Planner.

### Agent 5: BIN Route Planner

Run **Agent 5: BIN Route Planner** with all previous outputs:

Priority logic:
1. Crises before objectives — if any sector is Stage 1 (Compass) or Critical health (Radar 0-20), that takes absolute priority
2. Hierarchy: foundational crises → Horizon anchors → highest-scoring Quick Wins → alignment with objective (tiebreaker)
3. Number of priorities: 3 (crisis or limited capacity), 4 (standard), 5 (proven capacity + no crises)

Each priority follows 6 points:
1. What it is (2-3 lines)
2. Step by step (3-5 steps with responsible and deadline)
3. How to know it worked (verifiable and specific criterion)
4. Risk of inertia (specific, anchored in client data)
5. Connection to objective (direct link to Horizon objective)
6. Resources needed (weekly time, cost, skills)

Deliver: Route Planner deliverable with execution context, priorities 1-5 (full 6-point structure), 90-day sequence map (week by week), what NOT to do in the next 90 days (3-5 items with justification), private note for the consultant.

## Output

Present all 4 BIN deliverables in sequence:
1. BIN Horizon
2. BIN Compass (with maturity matrix)
3. BIN Radar (with 40 prioritized actions)
4. BIN Route Planner (with 90-day map)

After delivery:
- Note any data gaps or contradictions requiring consultant clarification
- Suggest next step: MIN (Integrated Business Model) if client is ready for the model-building phase

Ask: "Would you like me to adjust any deliverable, or is this ready for your review before presenting to the client?"

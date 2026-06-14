---
description: Build the MIN (Integrated Business Model) — 13 blocks across 3 phases (Foundation, Operation, Consolidation) after a completed GROW 360 BIN
argument-hint: "<client name, BIN complete, phase to run: 1, 2, or 3>"
---

# MIN — Integrated Business Model

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Build the Land Grow MIN (Modelo Integrado de Negócios): a 3-phase, 13-block business model framework that translates the GROW 360 diagnosis into a structured operating model. Each phase has its own session, form, and agent.

## Trigger

User runs `/min` or asks to build the MIN, business model, Plann Builder, run a MIN phase, or work on any of the 13 blocks (Proposta de Valor, Segmentos de Clientes, Atividades-Chave, Modelo de Receita, Comportamento do Consumidor, Jornada do Cliente, Canais de Engajamento, Recursos Estratégicos, Estrutura de Custos, Ecossistema de Parceiros, Métricas de Impacto, Cultura e Valores, Gestão de Riscos).

## Prerequisite

**GROW 360 BIN must be complete before starting the MIN.** If the BIN is not available, run `/grow-360` first. The MIN does not re-diagnose — it uses the BIN as its foundation.

## Inputs

Gather the following:

1. **BIN complete** (all 4 deliverables: Horizon, Compass, Radar, Route Planner) — mandatory
2. **Phase to run** — 1 (Foundation), 2 (Operation), or 3 (Consolidation)
3. **MIN phase form export** — the structured responses for the selected phase
4. **Session transcript** — from the MIN phase deepening session

## MIN Architecture

### 13 Blocks in 3 Phases

**Phase 1 — Foundation (Blocks 1-6)**: the survival base. Without solid foundation, any effort in later phases is structure on sand.

| Block | Name | Sectors |
|-------|------|---------|
| 1 | Value Proposition | Strategic, Innovation, Sales |
| 2 | Customer Segments | Marketing, Sales |
| 3 | Key Activities | Operational, Administrative, HR |
| 4 | Revenue Model | Financial, Sales, Strategic |
| 5 | Consumer Behavior | Cross-cutting |
| 6 | Customer Journey | Leadership, Marketing, Sales |

**Phase 2 — Operation (Blocks 7-9)**: the business engine. How it reaches the client, with what resources it operates, and how much it costs to exist.

| Block | Name | Sectors |
|-------|------|---------|
| 7 | Engagement Channels | Marketing, Sales, Innovation |
| 8 | Strategic Resources | HR, Innovation, Strategic |
| 9 | Cost Structure | Financial, Administrative |

**Phase 3 — Consolidation (Blocks 10-13)**: the protection and amplification layer. The difference between a business that works and one that lasts.

| Block | Name | Sectors |
|-------|------|---------|
| 10 | Partner Ecosystem | Legal, Innovation, Strategic |
| 11 | Impact Metrics | Strategic, Financial, Operational |
| 12 | Culture & Values | Leadership, HR, Legal |
| 13 | Risk Management | Legal, Operational, Financial |

## Maturity Scale per Block

Each block is assessed in one of 4 categories:

| Status | Criterion |
|--------|-----------|
| **Nonexistent** | Does not exist. Business operates without this block consciously. |
| **Draft** | Exists informally, in the entrepreneur's head, without documentation or process. |
| **Functional** | Exists, generates results, but depends on manual effort or specific people. |
| **Optimized** | Structured, documented, measurable, scalable. |

## Phase Execution

### Phase 1: Foundation

Activate the `min` skill and run **Agent 1: Foundation Architect**:

1. Read the BIN (extract current stage from Compass, objective and strategic focus from Horizon, critical sectors affecting Phase 1 from Radar, 90-day priorities connected to Phase 1 from Route Planner)
2. Read the form and transcript (extract assets, liabilities, metrics, contradictions)
3. Build each block (content per specific dimensions, maturity assessment, what is working, what needs to be built, connections to other blocks)
4. Internal coherence check (proposition aligned to segment? Revenue model sustainable? Journey calibrated to behavior? Contradictions between blocks?)

For each block, use this structure:
- Content on specific dimensions
- Maturity status (Nonexistent / Draft / Functional / Optimized)
- What is well
- What needs to be built
- Connection to other blocks

Deliver: BIN reading insights for Phase 1, Blocks 1-6 complete, internal coherence diagnosis, most critical block to resolve before advancing, transfer block for Phase 2.

### Phase 2: Operation

Activate the `min` skill and run **Agent 2: Operation Architect**:

1. Read BIN + Phase 1 (inherited alerts)
2. Verify coherence with Phase 1 before building each block
3. Build Blocks 7-9:
   - Block 7 Channels: acquisition channels (with cost and quality per channel), conversion, delivery, retention, current vs. ideal main channel, concentration risk
   - Block 8 Resources: team (gaps and dependencies), intellectual resources (methodologies, data, IP), technology (tools with cost and utilization), financial (working capital, reserve)
   - Block 9 Costs: fixed costs (including mandatory pro-labore), variable costs, hidden costs, break-even point, contribution margin, current situation (surplus/balanced/deficit)
4. Operational coherence check

Rules: Phase 2 does not rebuild Phase 1. Incoherences with Phase 1 named before proceeding. Pro-labore mandatory. CAC per channel mandatory. Single dependencies = risks.

Deliver: Blocks 7-9 complete, operational coherence diagnosis, most critical operational blocker, transfer block for Phase 3.

### Phase 3: Consolidation

Activate the `min` skill and run **Agent 3: Consolidation Architect**:

1. Read BIN + Phase 1 + Phase 2 (inherited alerts, critical sectors from Compass Block 3 Radar)
2. Verify readiness (Phase 1 solid and Phase 2 operational before building Phase 3)
3. Build Blocks 10-13:
   - Block 10 Partners: delivery, distribution, innovation, and strategic partners. Existing ecosystem, formalization level, dangerous dependencies, latent partnerships, toxic partnerships
   - Block 11 Metrics: lagging indicators (revenue, margin, churn, NPS), leading indicators (leads, conversion, capacity), operational health (CAC, LTV, LTV/CAC). Current metric situation
   - Block 12 Culture: declared vs. practiced values, leadership culture (decisions, delegation, errors), team culture (rituals, performance), client culture (service, complaint protocol), legal formalization
   - Block 13 Risks: operational (single dependencies, undocumented processes), financial (revenue concentration, reserve, default), legal (contracts, IP, labor liabilities, compliance), market (platform dependency, regulation, obsolescence), governance (concentrated decisions, partner conflicts). Risk map: Probability × Impact → Priority
4. Complete MIN diagnosis (all 13 blocks)

Deliver: Blocks 10-13 complete, complete MIN table (13 blocks with maturity and status), 3 most critical blocks across entire MIN, systemic coherence across 3 phases, recommended development sequence 90-180 days, private note for consultant.

## Output

Present the MIN phase deliverable with all requested blocks, coherence diagnoses, and recommended sequence. After delivery:
- Note dependencies on previous phases
- Note any data that requires clarification before the next session
- Recommend timeline for next phase session (typically 1-2 weeks after review)

Ask: "Would you like me to adjust any block, or is this ready for your review before the next client session?"

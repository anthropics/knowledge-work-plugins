---
description: Prepare for a client session — generate diagnostic questions, session agenda, and post-session summary for any Land Grow product (GROW Start, GROW 360, MIN)
argument-hint: "<product type and client context>"
---

# Client Session

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Prepare a Land Grow client session: generate tailored diagnostic questions, structured agenda, and post-session processing support.

## Trigger

User runs `/client-session` or asks to prepare for a client session, generate diagnostic questions, create a session agenda, or process notes after a session.

## Inputs

Gather the following:

1. **Product** — which Land Grow product is this session for:
   - GROW Start (initial diagnostic session)
   - GROW 360 (initial diagnostic or deepening session)
   - MIN Phase 1, 2, or 3

2. **Client context** — name, sector, size, what is already known about the client

3. **Session type** — first contact / deepening / review

4. **Session mode** — in-person / video call / async (form only)

## Session Preparation

### GROW Start Session

Generate:

**10 diagnostic questions** covering:
1. Revenue and cash flow situation (what is the real number, not the estimate)
2. Main active sales channel and conversion rate
3. Existing client base (active, inactive, churned)
4. Average ticket and current markup
5. Real differentiator (what the client says vs. what clients actually buy for)
6. Operational capacity (how many more clients can they take on today)
7. Main bottleneck (what is preventing growth right now)
8. Attempted solutions in the last 90 days
9. Available resources (time, money, team)
10. Definition of success in 30 days

**5 live audit dynamics** to run during the session:
1. Ask the client to send you a WhatsApp message as if selling to a cold lead right now
2. Ask them to tell you their 3 most recent sales and how they happened
3. Ask them to pull up their payment history and count the recurring clients
4. Ask them to tell you their costs line by line from memory
5. Ask them to describe their last 3 lost sales and why they lost them

**Session agenda** (60-90 minutes):
- 0-10 min: Context and rapport
- 10-40 min: 10 diagnostic questions
- 40-60 min: Live audits (select 2-3 most relevant)
- 60-75 min: Synthesis and next steps
- 75-90 min: GROW Start program explanation and proposal

### GROW 360 Session

Generate the deepening session guide:

**Opening** (15 min): Confirm form responses, clarify contradictions detected, establish the primary objective in the client's own words.

**Deep-dive questions by sector** (based on which sectors need most clarification from the form — provide 3 questions per sector identified as critical):
- Operational: process documentation level, bottlenecks, dependencies
- Financial: exact revenue and margin numbers, cash position, main costs
- HR: team structure, key dependencies, performance management
- Marketing: channels with actual numbers (not estimates), content, brand position
- Sales: pipeline, conversion, average cycle, top 3 clients
- Strategic: 1-year vision, planned investments, competitive differentiators
- Leadership: decision-making style, delegation capacity, time on operational vs. strategic

**Closing** (15 min): Summarize what was heard, ask for the client's own diagnosis, set expectations for the BIN delivery timeline.

### MIN Session

Generate phase-specific preparation:

**Phase 1 Foundation**: focus questions on value proposition clarity, who the real customer is, how revenue is actually generated, what the client journey looks like in practice.

**Phase 2 Operation**: focus on actual channels (with numbers), what resources are truly available, fixed and variable cost breakdown.

**Phase 3 Consolidation**: focus on partner relationships, what metrics are actually tracked, how decisions are made, what risks keep the client up at night.

## Post-Session Processing

After the session, if the user pastes notes or a transcript, provide:

1. **Key data extracted** (table format: topic / what was said / status / flag)
2. **Contradictions identified** (between what was said and previous information)
3. **Hidden objectives detected** (what the client wants but did not say directly)
4. **Ready to run pipeline**: confirm which agent pipeline to activate next and what inputs are ready

## Output

Deliver the session preparation kit:
- Tailored question list
- Session agenda with time blocks
- Tips for the live audits most relevant to this client
- Checklist of what to capture during the session

After the session, if transcript is provided, offer to immediately initiate the corresponding pipeline (`/grow-start`, `/grow-360`, or `/min`).

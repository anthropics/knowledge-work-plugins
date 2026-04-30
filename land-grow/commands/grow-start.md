---
description: Run the GROW Start pipeline — transform a diagnostic session transcript into a complete cash generation framework for the client (7-30 days)
argument-hint: "<client name and session transcript>"
---

# GROW Start

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Run the Land Grow GROW Start pipeline: a 4-agent sequential chain that converts a diagnostic session transcript into a professional, client-ready execution framework focused on generating cash in 7 to 30 days.

## Trigger

User runs `/grow-start` or asks to run a GROW Start, process a session transcript, create a cash strategy, or generate a quick wins plan for a client.

## Inputs

Gather the following before proceeding:

1. **Session transcript** — the full transcript from the diagnostic session (Fireflies, Otter, or manual). This is mandatory. If not provided, ask for it before running any agent.

2. **Client context** — name, sector, location, years in operation. If not in the transcript, ask.

## Pipeline

Run each agent in sequence. Do not skip steps. The output of each agent is the input of the next.

### Agent 1: Data Analyst

Activate the `grow-start` skill and run **Agent 1: Data Analyst**:

- Build the evidence table: declared vs. audited (channel, average ticket, margin/markup, real differentiator, sales moment, client base, conversion rate, execution capacity)
- Run SWOT analysis grounded in transcript data only — no generic items
- Run benchmarking research (web search): market average ticket, sector markup, acquisition channels, ICP behavior, 2-3 market data points
- Apply Porter's 5 Forces adapted for SMEs
- Write diagnostic synthesis (3-5 paragraphs): real situation, where the money is, main bottleneck, entrepreneur execution profile

Deliver: structured document with evidence table, SWOT, benchmarking, 5 Forces, synthesis. No strategic recommendation yet.

### Agent 2: Cash Strategist

Run **Agent 2: Cash Strategist** with Agent 1 output:

- Identify 3 quick wins with highest cash potential (what, why it works for this client, how much it can generate, timeline, what is needed)
- Develop the main strategy in full (goal, target, channel, offer, argument, day-by-day sequence)
- Summarize 2 supporting strategies
- List restrictions and alerts (what NOT to do)

Deliver: prioritized quick wins, full main strategy, supporting strategies, restrictions. Everything specific to this client — no generic templates.

### Agent 3: Senior Manager

Run **Agent 3: Senior Manager** with Agent 2 output:

- Validate the plan critically (realistic goal? operationally sound? unmapped risks? calibrated to client capacity?)
- Apply methodologies as needed (always SMART on main goal; OKRs if team or 30+ day horizon; 5W2H on main strategy; PDCA if test cycle; Design Thinking if product/journey problem)
- Define monitoring plan (1-3 simple weekly metrics, how to track, alert signal, success signal)

Deliver: validated and elevated plan with SMART goal, applicable frameworks, monitoring system.

### Agent 4: Delivery Architect

Run **Agent 4: Delivery Architect** with all previous outputs:

Produce the complete GROW Start document:

```
PROGRAMA GROW START
[Client Name] | [Date] | Land Grow

PART 1: BUSINESS X-RAY
1.1 What was found (crossed evidence, no judgment)
1.2 Where the money is (underused assets identified)
1.3 The main bottleneck (what is blocking cash)
1.4 Market view (benchmarking: where the client stands vs. market)

PART 2: THE ATTACK STRATEGY
2.1 The goal (SMART objective, specific number, defined deadline)
2.2 The target (who we will approach and why)
2.3 The offer (what we will present to the market)
2.4 The channel (where and how we will reach them)
2.5 Supporting quick wins (parallel actions)

PART 3: THE EXECUTION PLAN
3.1 Week 1: what to do days 1-7
3.2 Week 2: what to do days 8-14
3.3 Weeks 3-4: consolidation and adjustment
3.4 Ready-to-use ammunition: scripts, message templates, ready-to-send texts

PART 4: MANAGEMENT AND MONITORING
4.1 The metrics that matter (1-3 numbers to track)
4.2 How to record (notebook, spreadsheet, simplest possible method)
4.3 Alert signal and success signal
4.4 Next step (what comes after GROW Start)
```

Include ready-to-use ammunition in 3.4: WhatsApp outreach script (base reactivation), offer message template (variations A and B), physical note text if client has a store, Instagram post if relevant. Tone must match how the client's customers actually talk — not marketing language.

## Quality Gate

Before delivering, verify:
- [ ] Client can understand it without the consultant in the room?
- [ ] Client knows exactly what to do on day 1?
- [ ] Client has ready text to send on WhatsApp?
- [ ] Client can measure results without any system?
- [ ] Plan fits in the time and budget the client has today?

If any answer is no, revise before presenting.

## Output

Present the complete GROW Start document. After delivery, note:
- Which agents were run and in what order
- Any data gaps found (ask client for clarification if needed)
- Recommendation for next step (GROW 360 or other Land Grow product)

Ask: "Would you like me to adjust any section, or is this ready for your review before sending to the client?"

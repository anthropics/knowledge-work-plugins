---
description: Generate and evaluate strategic options using structured decision frameworks
argument-hint: "<decision or problem> <number of options>"
---

# /options-generate -- Strategic Options Generation

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate, structure, and evaluate strategic options using proven frameworks. Supports decision-making with clear evaluation criteria and recommendations.

## Invocation

```
/options-generate [decision or problem] [number of options]
```

If parameters not provided, ask for:
- Strategic decision or problem to solve
- Number of options to generate (typically 3-5)
- Evaluation criteria (or help define)
- Constraints or requirements

## Workflow

### Step 1: Define the Decision

Clarify what needs to be decided using the **DECIDE Framework**:

```
## Strategic Decision: [Decision]

### Problem Statement
[What challenge are we solving?]

### Current State
[Where we are today]

### Desired State
[Where we want to be]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Success Criteria
| Criterion | Weight | Definition of Success |
|-----------|--------|----------------------|
| [Criterion 1] | X% | [Definition] |
| [Criterion 2] | X% | [Definition] |
| [Criterion 3] | X% | [Definition] |

### DECIDE Framework Application
- **D**efine the problem: [Clear problem statement]
- **E**xplore alternatives: [Initial options identified]
- **C**hoose the best option: [Selection criteria applied]
- **I**mplement the decision: [Action plan]
- **D**ecide how to measure: [KPIs defined]
- **E**valuate and learn: [Review mechanism]

### Step 2: Generate Options

Create differentiated options using **Cynefin Framework** categorization to ensure diverse approaches:

```
## Strategic Options

### Option A: [Name]
**Description**: [What this option entails]

**Approach**:
- [Key element 1]
- [Key element 2]
- [Key element 3]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Resource Requirements**:
- Investment: $[X]
- Timeline: [X months]
- Capabilities: [What's needed]

**Risk Profile**: [High/Medium/Low]

**Cynefin Domain**: [Simple/Complicated/Complex/Chaotic]

---

### Option B: [Name]
[Same structure]

---

### Option C: [Name]
[Same structure]

---

### Option D: [Do Nothing / Status Quo]
**Include this option**: Always include as baseline

**Description**: [What happens if we do nothing]

**Pros**:
- No investment
- No disruption

**Cons**:
- [Consequence 1]
- [Consequence 2]
```

### Step 3: Evaluate Options

Apply structured evaluation with data-driven insights:

```
## Options Evaluation

### Scoring Matrix

| Criterion | Weight | Option A | Option B | Option C | Option D |
|-----------|--------|----------|----------|----------|----------|
| [Criterion 1] | X% | [Score 1-5] | [Score 1-5] | [Score 1-5] | [Score 1-5] |
| [Criterion 2] | X% | [Score 1-5] | [Score 1-5] | [Score 1-5] | [Score 1-5] |
| [Criterion 3] | X% | [Score 1-5] | [Score 1-5] | [Score 1-5] | [Score 1-5] |
| [Criterion 4] | X% | [Score 1-5] | [Score 1-5] | [Score 1-5] | [Score 1-5] |
| **Weighted Score** | **100%** | **X.X** | **X.X** | **X.X** | **X.X** |

### Evaluation Criteria
| Criterion | Weight Consideration |
|-----------|---------------------|
| Digital Readiness | Weight digital transformation alignment |
| Data Availability | Weight data infrastructure requirements |
| Agility Factor | Weight speed to value and adaptability |
| Sustainability | Weight ESG and long-term viability |
| Stakeholder Alignment | Weight change resistance and adoption likelihood |

### Scoring Guide
| Score | Definition |
|-------|------------|
| 5 | Excellent — fully meets criterion |
| 4 | Good — substantially meets criterion |
| 3 | Adequate — partially meets criterion |
| 2 | Poor — minimally meets criterion |
| 1 | Does not meet criterion |

### Qualitative Assessment

#### Option A: [Name]
- **Fit with strategy**: [Assessment]
- **Feasibility**: [Assessment]
- **Risk**: [Assessment]
- **Stakeholder support**: [Assessment]
- **Digital Transformation fit**: [Assessment]

#### Option B: [Name]
[Same structure]

[Continue for all options]
```

### Step 4: Scenario Analysis

Test options under different scenarios:

```
## Scenario Analysis

### Scenario: [Scenario Name]
[Description of scenario]

| Option | Performance | Rationale |
|--------|-------------|-----------|
| Option A | [High/Med/Low] | [Why] |
| Option B | [High/Med/Low] | [Why] |
| Option C | [High/Med/Low] | [Why] |

---

### Scenario: [Optimistic]
[Description]

### Scenario: [Conservative]
[Description]

---

### Sensitivity Analysis

Which criteria have highest impact on recommendation?

| Criterion | If Weight +10% | Recommendation Shifts To |
|-----------|----------------|--------------------------|
| [Criterion 1] | [Impact] | [Option] |
| [Criterion 2] | [Impact] | [Option] |
```

### Step 5: Recommendation

Synthesize analysis:

```
## Recommendation

### Recommended Option: [Option Name]

**Rationale**:
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Key Trade-offs**:
- [Trade-off 1 — acceptable because...]
- [Trade-off 2 — acceptable because...]

**Implementation Considerations**:
- [Consideration 1]
- [Consideration 2]

**Risks and Mitigations**:
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation] |

### Alternative Options
If recommended option is not feasible:

1. **Fallback 1**: [Option Name] — [Why it's the backup]
2. **Fallback 2**: [Option Name] — [Why it's the backup]

### Next Steps
1. [Immediate next step]
2. [Short-term next step]
3. [Decision point for go/no-go]
```

## Output Format

Generate:

1. **Decision Framework** — Criteria and weights
2. **Options Description** — Detailed option definitions
3. **Evaluation Matrix** — Structured scoring
4. **Scenario Analysis** — Risk assessment
5. **Recommendation** — Clear recommendation with rationale

After generating, ask:

> "Would you like me to:
> - Adjust evaluation criteria or weights?
> - Add additional options?
> - Develop implementation plans for top options?
> - Create decision slides for executive presentation?"

## Notes

- Always include "do nothing" as a baseline option
- Ensure options are genuinely DIFFERENT, not just incremental
- Weight criteria carefully — what matters most?
- Be transparent about trade-offs — there is no "perfect" option
- Consider second-order effects — what happens after the first step?
- Stress-test recommendations with scenarios
- Document assumptions explicitly
- Make recommendations clear — don't hedge excessively
- Factor in digital transformation alignment and sustainability
- Apply **Cynefin Framework** to categorize decision complexity before selecting approach
- Use **OODA Loop** (Observe-Orient-Decide-Act) for time-sensitive decisions
- Consider **scenario planning** with 3-5 year horizon for strategic decisions
- Include **ESG criteria** in evaluation for sustainable business decisions

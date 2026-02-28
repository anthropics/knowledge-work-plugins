---
description: "Auto-activates structured briefing sessions for complex legal queries -- detects when multi-agent coordination benefits from pre-execution intake and plan building"
---

# Legal Briefing Skill

You are aware of BetterCallClaude's briefing session capability. When you detect a complex legal query that would benefit from structured intake before execution, suggest or activate a briefing session.

## Activation Criteria

Suggest a briefing session when **any** of the following conditions are met:

### Complexity Indicators (score >= 5)
- Three or more legal domains in a single query (e.g., corporate + tax + compliance).
- Multi-jurisdictional question (federal + cantonal, or multiple cantons).
- Document output expected alongside analysis (e.g., "analyze and draft").
- Financial exposure mentioned above CHF 100,000.
- Multiple parties with conflicting interests.

### Ambiguity Indicators
- Desired output is unclear (research? strategy? document? compliance check?).
- Jurisdiction cannot be determined from the query.
- Multiple valid routing paths exist with significantly different outcomes.
- The query uses vague terms: "handle", "deal with", "figure out", "advise on".

### Pipeline Indicators
- Query maps to a workflow template (litigation-prep, due-diligence, contract-lifecycle).
- Three or more agents would need to be coordinated.
- Data dependencies exist between agents (output of one feeds into another).

## When NOT to Activate

Skip briefing and route directly when:
- Query is a simple, focused question (complexity 1-3).
- User explicitly specifies a single agent with `@agent_name`.
- User uses `--skip-briefing` or `--direct` flag.
- Query is a citation lookup, translation, or format verification.
- User is resuming a previously approved execution plan.

## Activation Behavior

### Implicit Suggestion (auto-detected complexity >= 5)

When the `/legal` gateway scores a query at complexity 5+ and no `--skip-briefing` flag is present:

```
💡 This query involves [N domains / multi-jurisdiction / pipeline coordination].
A briefing session would help build a precise execution plan before I start working.

**Options**:
- **Proceed with briefing** (recommended) — I'll ask a few targeted questions first
- **Skip briefing** — Route directly to agents (add `--skip-briefing` to bypass in future)
```

### Explicit Activation

When the user invokes `/bettercallclaude:briefing`, always activate regardless of complexity.

## Memory Key Patterns

The briefing system uses these memory keys for persistence:

| Pattern | Purpose |
|---------|---------|
| `briefing_[id]` | Full state for a specific briefing session |
| `briefing_latest` | ID of the most recently active briefing |
| `briefing_index` | Registry of all briefing sessions with status |

## Integration Points

- **`/legal` gateway**: Briefing phase is embedded between intent classification and routing.
- **Orchestrator agent**: Consumes the approved execution plan YAML for step-by-step execution.
- **All specialist agents**: Can be spawned as panel members during the consultation phase.
- **Summarizer agent**: Can be appended to the execution plan's final stage.

## Quality Standards

- Briefing suggestions must be helpful, not obstructive — never block simple queries.
- Auto-detection should have a low false-positive rate: only suggest for genuinely complex cases.
- The user must always have a clear path to skip the briefing if they prefer direct routing.

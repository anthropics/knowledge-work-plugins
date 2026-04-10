# Accoil — Design Constraints

Design-time constraints for products targeting Accoil as an analytics destination. These affect how you design events, not how you implement them.

## Event Names Only — No Properties

Accoil stores **event names only**. No event properties are stored or queryable. This is the single most important constraint affecting event design.

**Impact on design:**
- Encode meaningful distinctions in the event name itself
- `report.created` with `{ type: "template" }` does NOT work — Accoil sees only `report.created`
- Instead, use distinct event names: `report.created`, `template_report.created`
- Apply the test: "If I can only see the event name, can I tell what happened?"

**When properties still matter:**
If the tracking plan targets multiple destinations (e.g., Segment + Accoil), design events with properties as normal. Other destinations will use them. Just ensure the event name alone carries enough meaning for Accoil.

## Group Calls Are Essential

Accoil is account-centric. It calculates engagement scores at the account level. Without `group()` calls, events cannot be attributed to accounts and scoring fails entirely.

**Design implication:** The tracking plan MUST include group hierarchy with account as a top-level group. Every event should be attributable to an account.


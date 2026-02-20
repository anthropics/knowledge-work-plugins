---
name: release-readiness
description: >
  Aggregator skill that combines outputs from all input skills into a
  single go/no-go decision for a milestone: launch, release, gate,
  campaign, or deadline. Produces a unified readiness assessment with
  a clear recommendation and all supporting evidence in one view.
---

# Release / Milestone Readiness

You are a **Readiness Assessor** — you pull signals from every input skill and synthesize them into a single decision: **GO**, **PROCEED WITH CAUTION**, or **HOLD**. You don't gather raw data yourself — you consume what the input skills produce and apply decision logic.

This skill works for any milestone with a go/no-go gate:
- Software releases, deployments, or cutover events
- Campaign launches or go-to-market dates
- Compliance deadlines or audit submissions
- Contract signings or vendor commitments
- Product launches, events, or public announcements

**Core question:** *Should we proceed with this milestone, or not?*

**Example triggers:**
- "Are we ready to launch?"
- "Release readiness check for v2.0"
- "Go/no-go for the Q2 campaign"
- "Can we ship on Friday?"
- "Milestone readiness assessment"
- "Pre-launch checklist"

---

## How It Works

**Step 1: Gather Skill Outputs**

Pull the latest output from each available input skill:

| Check | Input Skill | What It Tells You |
|-------|------------|-------------------|
| Quality | `quality-check` | Are deliverables meeting acceptance criteria? |
| Activity | `activity-audit` | Does actual work match reported status? |
| Risks | `risk-tracker` | Are there unresolved risks or active blockers? |
| Schedule | `schedule-forecast` | Will we hit the target date? |
| Flow | `story-flow` | Are stories flowing or stuck? |
| Dependencies | `dependency-readiness` | Are external/internal dependencies ready? |
| Approvals | `stakeholder-signoff` | Have stakeholders been enabled and approved? |
| Changes | `change-summary` | Is the changelog clear and communicated? |

If a skill hasn't been run recently, run it or note it as "not assessed."

Check [REFERENCES.md](../../REFERENCES.md) for any configured milestone definitions or gate criteria.

**Step 2: Map to Readiness Checks**

Convert each skill output to a traffic light:

| Check | 🟢 Green | 🟡 Yellow | 🔴 Red |
|-------|----------|----------|--------|
| **Quality** | All checks pass | Minor findings, no blockers | Blocking findings or >5% failure rate |
| **Activity** | Work matches status | Some stale items | Significant gaps between status and reality |
| **Risks** | No active risks or issues | Low/medium risks, issues <24h | High risks, issues >24h, cascades |
| **Schedule** | On track or ahead | At risk (likely date 3-7 days late) | Behind (likely date >7 days late) |
| **Flow** | Stories completing within targets | Some stories exceeding cycle time | Multiple stalled or churning stories |
| **Dependencies** | All dependencies verified ready | Some at risk or in progress | Critical-path dependency not ready or unknown |
| **Approvals** | All stakeholders enabled and approved | Pending or conditional approvals | Informed objection or rubber stamp on critical approver |
| **Changes** | Changelog generated and shared | Changelog generated but not shared | No changelog or major gaps in coverage |

**Step 3: Apply Decision Logic**

Count signals:
```
red_count = number of checks with 🔴
yellow_count = number of checks with 🟡
```

| Condition | Recommendation | Status |
|-----------|---------------|--------|
| Any 🔴 | **HOLD** | blocked |
| ≥3 🟡 | **HOLD** | at risk — too many concerns |
| 1-2 🟡 | **PROCEED WITH CAUTION** | ready with warnings |
| All 🟢 | **GO** | ready |

**Step 4: Output**

Use the project-intelligence output style (see [output style](../../output-styles/project-intelligence.md)).

```markdown
# Milestone Readiness | [Milestone Name]

**Target:** [date]
**Recommendation:** 🟢 GO / 🟡 PROCEED WITH CAUTION / 🔴 HOLD

---

## Readiness Checks

| Check | Status | Summary |
|-------|--------|---------|
| Quality | 🟢/🟡/🔴 | [1-line summary] |
| Activity | 🟢/🟡/🔴 | [1-line summary] |
| Risks | 🟢/🟡/🔴 | [1-line summary] |
| Schedule | 🟢/🟡/🔴 | [1-line summary] |
| Flow | 🟢/🟡/🔴 | [1-line summary] |
| Dependencies | 🟢/🟡/🔴 | [1-line summary] |
| Approvals | 🟢/🟡/🔴 | [1-line summary] |
| Changes | 🟢/🟡/🔴 | [1-line summary] |

---

## Blockers (if any)
- ⛔ [Blocker description + source]

## Warnings (if any)
- ⚠️ [Warning description + source]

---

## Actions Required Before Proceeding
1. [Highest priority action]
2. [Next action]

---

## Scope Hygiene
> Before finalizing this assessment, confirm that all items for this milestone
> are correctly tagged/associated. Items may have been added to or removed from
> scope since planning. [N items checked, N in scope]

---

## Assessment
[2-3 sentence summary: what's the overall picture, what's the biggest risk,
and what needs to happen for a GO if currently HOLD]
```

---

## Blocker Aggregation

Collect blockers from all skills into a single list:

| Source | What Becomes a Blocker |
|--------|----------------------|
| `quality-check` | Blocking findings (critical bugs, failed compliance checks, rejected deliverables) |
| `activity-audit` | Significant activity gaps — status says "done" but artifacts say otherwise |
| `risk-tracker` | Issues open >24h, high severity risks, cascade dependencies |
| `schedule-forecast` | Forecast >7 days behind target |
| `story-flow` | Critical-path stories stalled or in churn |
| `dependency-readiness` | Critical-path dependencies not ready or unknown |
| `stakeholder-signoff` | Informed objection or required approver explicitly blocking |

---

## Warning Aggregation

Collect yellow signals that aren't blocking but need awareness:

| Source | What Becomes a Warning |
|--------|----------------------|
| `quality-check` | Minor findings, flaky checks, deferred items |
| `activity-audit` | Stale items not on the critical path |
| `risk-tracker` | Medium risks, accumulating debt |
| `schedule-forecast` | At risk (3-7 days late) or low confidence |
| `story-flow` | Non-critical stories exceeding cycle time |
| `dependency-readiness` | Non-critical dependencies at risk or in progress |
| `stakeholder-signoff` | Pending approvals, conditional approvals, or rubber stamps |
| `change-summary` | Changelog not shared with stakeholders or has major gaps |

---

## Skills Not Assessed

If an input skill hasn't been run or data is unavailable, note it explicitly:

```markdown
## Skills Not Assessed
- ⚪ Activity — no ~~code repository configured. Activity audit not run.
- ⚪ Schedule — insufficient data (less than 20% of scope complete)
```

**Rule:** An unassessed skill does not count as green. If >2 skills are unassessed, add a warning: *"Limited visibility — [N] checks not assessed. Recommendation is based on partial data."*

---

## Scope Hygiene Reminder

Every readiness assessment should prompt the requester to verify milestone scope. Labeling and tracking discipline naturally drifts over the course of a milestone — items get added, moved, or forgotten. Neither people nor agents are flawless at keeping associations current.

**What to check:**
- Are all items for this milestone correctly tagged/associated in ~~project tracker?
- Were any items pulled in from future milestones (scope grew)?
- Were any items moved out but still tagged to this milestone (stale associations)?
- Are there untracked items (work happening outside the tracker)?

**How to surface it:**

Include a **Scope Hygiene** section in every output, after Actions and before Assessment:

```markdown
## Scope Hygiene
> Before finalizing this assessment, confirm that all items for this
> milestone are correctly tagged/associated. Items may have been added
> to or removed from scope since planning.
>
> [N] items currently in scope. Last scope change detected: [date or "none detected"].
```

If the skill detects potential scope issues (e.g., items tagged to this milestone but with no activity, or active items not tagged), flag them:

```markdown
## Scope Hygiene
> ⚠️ 3 items tagged to this milestone have no activity — may be stale associations.
> ⚠️ 2 active items in the tracker are not tagged to any milestone — may belong here.
> Confirm scope is accurate before relying on this assessment.
```

**Why this matters:**
1. Practical — catches scope drift before it affects the recommendation
2. Trust — signals that the system understands human and agent patterns, increasing confidence in the assessment

---

## Edge Cases

**Milestone with custom gate criteria:**
- Some milestones have specific gates (e.g., "security review must pass", "legal sign-off required"). If the user provides custom criteria, add them as additional checks in the readiness table.

**Override:**
- The skill recommends, the human decides. If a team proceeds despite a HOLD, note it: *"Proceeding despite HOLD recommendation. Risks accepted: [list]."*

**No red, but gut feeling is wrong:**
- Trust the data. If all checks are green but the user is uneasy, suggest running additional checks or digging deeper into a specific area.

**Scope drift detected:**
- If untagged active items or stale tagged items are found, note in Scope Hygiene section. Do not let scope uncertainty affect the recommendation silently — surface it.

---

## Examples

### Example 1: Software Release — GO

**User:** "Are we ready to ship v3.1?"

```markdown
# Milestone Readiness | v3.1 Release

**Target:** Feb 14
**Recommendation:** 🟢 GO

---

## Readiness Checks

| Check | Status | Summary |
|-------|--------|---------|
| Quality | 🟢 | 248/248 tests pass. No blocking findings. |
| Activity | 🟢 | All stories show active commits matching reported status. |
| Risks | 🟢 | 0 active blockers. 1 low risk (monitoring). |
| Team | 🟢 | All stories progressing. No blockers in last 3 updates. |
| Schedule | 🟢 | On track — likely Feb 13 (1 day ahead). |
| Flow | 🟢 | All stories within cycle time targets. |

---

## Assessment
All 6 checks are green. No blockers, no warnings. Ship it.
```

### Example 2: Campaign Launch — PROCEED WITH CAUTION

**User:** "Go/no-go for Q2 campaign launch?"

```markdown
# Milestone Readiness | Q2 Campaign Launch

**Target:** March 15
**Recommendation:** 🟡 PROCEED WITH CAUTION

---

## Readiness Checks

| Check | Status | Summary |
|-------|--------|---------|
| Quality | 🟢 | All creative assets reviewed and approved. |
| Activity | 🟢 | Document revisions match reported progress. |
| Risks | 🟡 | Medium risk: vendor contract for paid media not signed. |
| Team | 🟢 | All workstreams progressing. No blockers. |
| Schedule | 🟡 | At risk — likely March 18 (+3 days). Legal review is bottleneck. |
| Flow | 🟢 | Deliverables completing within targets. |

---

## Warnings
- ⚠️ Vendor contract for paid media still unsigned — media buy cannot start (risk-tracker R-2)
- ⚠️ Schedule shows +3 days if legal review doesn't close this week

---

## Actions Required Before Proceeding
1. Escalate vendor contract — blocks paid media preparation
2. Follow up on legal review for disclaimers — on the critical path

---

## Assessment
Mostly ready — creative and team are in good shape. Two yellow signals both trace to external dependencies (vendor contract, legal review). Proceed if confident these close this week; otherwise hold until resolved.
```

### Example 3: Compliance Deadline — HOLD

**User:** "Readiness check for SOC 2 audit submission"

```markdown
# Milestone Readiness | SOC 2 Audit Submission

**Target:** March 31
**Recommendation:** 🔴 HOLD

---

## Readiness Checks

| Check | Status | Summary |
|-------|--------|---------|
| Quality | 🔴 | 3 controls failed validation. 2 are critical (access management, encryption at rest). |
| Activity | 🟡 | 4 evidence documents stale — last updated >10 days ago. |
| Risks | 🔴 | High risk: recurring delay in IT security team responses (3rd time in 30 days). |
| Team | 🟡 | 1 blocker: waiting on infrastructure team for encryption config (48h). |
| Schedule | 🟡 | At risk — forecast shows April 4 (+4 days) at current pace. |
| Flow | 🟢 | Non-blocked controls progressing within targets. |

## Skills Not Assessed
- ⚪ Schedule confidence is low — only 25% of controls validated so far.

---

## Blockers
- ⛔ 2 critical controls failed validation: access management, encryption at rest (quality-check)
- ⛔ IT security team response delays — 3rd occurrence in 30 days, systemic bottleneck (risk-tracker R-1)

## Warnings
- ⚠️ 4 evidence documents not updated in >10 days — may need refreshing (activity-audit)
- ⚠️ Schedule forecast at risk — April 4 likely completion vs March 31 target

---

## Actions Required Before Proceeding
1. **CRITICAL:** Fix access management and encryption at rest controls — these must pass
2. **SYSTEMIC:** Escalate IT security response pattern to leadership — 3rd delay this month
3. **EVIDENCE:** Refresh 4 stale evidence documents before auditor review
4. **SCHEDULE:** Reallocate capacity to critical controls to recover 4-day slip

---

## Assessment
Not ready. 2 critical control failures and a systemic IT security bottleneck are blocking. Even if controls are fixed, the schedule is tight — forecast shows April 4 at current pace. Resolve the 2 critical controls and the IT security bottleneck first, then reassess. Earliest realistic GO: after next readiness check if blockers resolve this week.
```

---

## Key Principles

1. **Any red = HOLD** — No exceptions. One blocking signal is enough.
2. **Many yellows = HOLD** — 3+ concerns together indicate instability, even without a single blocker.
3. **Few yellows = Caution** — Proceed, but flag the warnings. The team decides with full awareness.
4. **All green = GO** — Ship it, launch it, submit it.
5. **Aggregate, don't duplicate** — This skill synthesizes; it doesn't re-analyze. Input skills do the work.
6. **Recommend, don't decide** — The skill recommends. Humans make the final call.

---
name: change-summary
description: >
  Auto-generate what changed — at three levels of granularity.
  Major milestone summaries for external stakeholders, minor milestone
  summaries for internal teams, and review deltas showing what changed
  since a specific stakeholder last reviewed. Works for any deliverable:
  software, creative assets, documents, hardware firmware, training
  materials, or legal agreements.
---

# Change Summary

You are a **Change Summarizer** — you compile what actually changed and present it at the right level of detail for the audience. The same body of work looks different to stakeholders reading a milestone summary, a team reviewing their iteration, and a reviewer checking whether their feedback was addressed.

This skill operates in three tiers:

| Tier | Scope | Audience | Granularity |
|------|-------|----------|-------------|
| **Major** | Since last major milestone | External stakeholders, leadership, customers | Grouped by theme |
| **Minor** | Since last minor milestone | Internal team, iteration reviews | Listed by item |
| **Delta** | Since a specific point (last review, last approval, feedback) | Specific reviewer or approver | Focused on what's different |

**Core question:** *What changed, for whom, and since when?*

**Example triggers:**
- "What's new in v3.0?" → Major tier
- "What changed this iteration?" → Minor tier
- "What changed since the stakeholder review on Feb 5?" → Delta tier
- "Generate release notes for the Q2 launch"
- "Summarize revisions to the training materials since the last review"
- "What's different in the firmware since the last certification submission?"
- "What changed on the MSA since opposing counsel's last redline?"
- "Summarize creative changes since the client review"

---

## How It Works

**Step 1: Determine Tier and Timeframe**

Identify the tier from the request:

| Signal | Tier |
|--------|------|
| "Release notes", "what's new", major version, external summary | **Major** |
| "This sprint", "this iteration", "this cycle", "since last review" | **Minor** |
| "Since [person] reviewed", "since last feedback", "since [date]" | **Delta** |

If ambiguous, ask: *"Who is this summary for, and since when should I look?"*

**Step 2: Gather Change Sources**

Pull from whatever sources are available. Different domains have different change trails:

| Source Type | What It Provides | Domain Examples |
|------------|-----------------|-----------------|
| ~~project tracker | Completed items, resolved findings, scope changes | Any tracked work |
| ~~revision history | File changes, version diffs, edit history | Code repos, document systems, design tools, DAWs |
| `story-flow` | Items that moved to done with cycle time context | Any tracked items |
| `quality-check` | Items that passed/failed quality gates | Any gated deliverable |
| `risk-tracker` | Risks resolved, issues closed | Any project |
| `stakeholder-signoff` | Feedback addressed, conditions met (for delta tier) | Any approval flow |
| Review comments | Feedback from reviewers, redline changes | Documents, creative, legal |
| User input | Manual additions or corrections | Any |

**Step 3: Categorize Changes**

Group changes into categories that match the domain. Don't force software categories onto non-software work.

**Starting categories by domain:**

| Domain | Suggested Categories |
|--------|---------------------|
| **Software** | Features, Improvements, Fixes, Internal, Security |
| **Creative/Design** | New assets, Revisions, Direction changes, Format/specs |
| **Legal/Compliance** | New clauses, Revised terms, Removed provisions, Formatting |
| **Training/Content** | New material, Updated content, Corrections, Restructured |
| **Hardware/IoT** | New capabilities, Spec changes, Defect fixes, Certification |
| **Marketing** | New campaigns, Revised messaging, Updated assets, Analytics |

**Universal fallback categories** (work across any domain):

| Category | Description |
|----------|-------------|
| **New** | Things that didn't exist before |
| **Changed** | Things that existed but were modified |
| **Removed** | Things that were taken out |
| **Deferred** | Things moved to a future milestone |
| **Resolved** | Previously flagged issues that are now closed |

Let the domain drive the language. If the team calls them "tracks" not "features", or "redlines" not "fixes", use their vocabulary.

---

## Tier 1: Major Milestone Summary

**Purpose:** Communicate what changed to people who don't follow day-to-day work — stakeholders, customers, leadership, external partners.

**Characteristics:**
- Grouped by theme, not chronology
- Audience-appropriate language, not internal jargon
- Impact-oriented: what does this mean for the recipient, not what happened internally
- Highlights and headlines, not exhaustive lists

**Output template:**

```markdown
# What's New | [Milestone Name]

**Period:** [start date] → [end date]
**Items completed:** [N]

---

## Highlights
- [1-2 sentence headline for the most important change]
- [Another headline]

---

## [Category 1]
- **[Item name]** — [1-2 sentence description of what changed and why it matters]

## [Category 2]
- **[Item name]** — [What's different now]

---

## Known Limitations
- [Anything explicitly not included, deferred, or partially complete]

---

## Coming Next
- [Brief preview of what's planned for the next major milestone]
```

**Audience rules:**
- No internal tracking IDs unless the audience expects them
- Translate internal work into external impact
- Focus on "what's different for you" not "what we did"

---

## Tier 2: Minor Milestone Summary

**Purpose:** Keep the internal team aligned on what shipped this iteration.

**Characteristics:**
- Listed by item with tracking references
- Includes internal details (who did it, duration, blockers hit)
- Covers scope changes — what was added, removed, or deferred
- Honest about what didn't get done

**Output template:**

```markdown
# [Iteration Name] Summary | [Team/Project]

**Period:** [start date] → [end date]
**Completed:** [N] items | **Carried over:** [N] items | **Deferred:** [N] items

---

## Completed

### [Category 1]
- [TRACKING-ID] **[Title]** — [1-line description] ([owner], [duration/cycle time])

### [Category 2]
- [TRACKING-ID] **[Title]** — [1-line description] ([owner], [duration/cycle time])

---

## Scope Changes
- ➕ **Added:** [ID] [Title] — [why it was added mid-cycle]
- ➖ **Deferred:** [ID] [Title] — [why, and where it moved to]
- 🔄 **Rescoped:** [ID] [Title] — [what changed about the scope]

---

## Carried Over
- [ID] **[Title]** — [status, what's remaining, why it didn't complete]

---

## Resolved Issues
- [ID] [Title] — [how it was resolved]

---

## Notes
- [Anything noteworthy: team changes, process observations, dependency shifts]
```

**Audience rules:**
- Include tracking IDs and owner names
- Include duration/cycle time for context
- Be honest about what carried over and why

---

## Tier 3: Review Delta

**Purpose:** Show a specific stakeholder what changed since they last reviewed, especially if they gave feedback or a conditional approval.

**Characteristics:**
- Anchored to a specific point in time (their last review)
- Highlights feedback addressed vs. feedback outstanding
- Compact — only what changed, not the full picture
- Designed to help them decide if their concerns are resolved

**Output template:**

```markdown
# Changes Since Your Last Review | [Milestone/Deliverable Name]

**Last review:** [date] by [stakeholder]
**Changes since:** [N] items

---

## Feedback Addressed
- ✅ **"[Their feedback/condition]"** — [How it was addressed]
- ✅ **"[Their feedback/condition]"** — [How it was addressed]

## Feedback Outstanding
- ⏳ **"[Their feedback/condition]"** — [Status, ETA]

---

## Other Changes Since [date]
- [Change 1] — [brief description]
- [Change 2] — [brief description]

---

## Net Impact
[1-2 sentences: what's different now vs. when they last looked. Help them assess whether a re-review is needed or their prior approval still holds.]
```

**Audience rules:**
- Lead with their specific feedback — did we address it?
- Only include other changes that are material enough to affect their decision
- End with a clear recommendation: "Your prior approval still holds" or "Changes are significant enough to warrant re-review"
- Connect to `stakeholder-signoff` — if their conditional approval had conditions, show condition status

---

## Edge Cases

**No changes found:**
- Report it: "No completed items found between [start] and [end]. This may indicate a data source gap — verify access to revision history and tracker."

**Mixed audiences:**
- If the user doesn't specify, default to minor tier for internal requests and major tier for external-facing requests.

**Scope change heavy iteration:**
- If >30% of items were scope changes (added, deferred, rescoped), highlight this pattern: "Significant scope churn this cycle — 5 of 12 items were scope changes."

**No feedback to reference (delta tier):**
- Fall back to a time-based delta: "No specific feedback on record. Here's everything that changed since [date]."

**Multiple revision cycles (creative, legal):**
- Track which revision cycle this is: "Round 3 of creative review. 8 assets revised since Round 2." Helps stakeholders understand where they are in the process.

**Cross-domain milestones:**
- Use the categories that match the domain. Let the content itself guide the category names.

---

## Examples

### Example 1: Major — IoT Firmware Release Notes

**User:** "Generate release notes for thermostat firmware v2.4"

```markdown
# What's New | Thermostat Firmware v2.4

**Period:** Jan 8 → March 10
**Items completed:** 18

---

## Highlights
- Geofencing now supports irregular home boundaries, not just circular radius
- Energy reports include cost estimates based on local utility rates
- Resolved intermittent sensor reading drops reported in v2.3

---

## New Capabilities
- **Irregular geofence boundaries** — Draw custom home boundaries on the app map instead of a fixed radius. Works with GPS and Wi-Fi positioning.
- **Utility cost estimates** — Daily and monthly energy reports now show estimated cost using configurable local utility rates

## Spec Changes
- **Sensor polling interval** — Reduced from 30s to 15s for faster response to temperature changes. Battery impact: ~3% increase in daily consumption.
- **BLE pairing timeout** — Extended from 30s to 60s based on field reports of pairing failures with older phones

## Defect Fixes
- **Sensor reading drops** — Fixed intermittent null readings when humidity sensor and temp sensor poll simultaneously
- **Schedule timezone** — Fixed daylight saving time transition causing 1-hour schedule offset

---

## Known Limitations
- Irregular geofence requires firmware v2.4 AND app v4.1+ (app update releasing March 15)
- Cost estimates use manual rate entry — utility API integration planned for v2.5

---

## Coming Next
- Utility API integration for automatic rate updates
- Multi-zone scheduling improvements
```

### Example 2: Minor — Creative Development Cycle

**User:** "Summarize what changed in round 3 of the rebrand"

```markdown
# Rebrand Round 3 Summary | Visual Identity

**Period:** Feb 18 → Feb 28 (Round 3 of 4)
**Completed:** 11 assets | **Carried over:** 3 assets | **Deferred:** 1 asset

---

## Completed

### Revised Assets
- BRAND-22 **Primary logo — dark variant** — Increased contrast ratio per accessibility feedback (Maya, 2 days)
- BRAND-24 **Color palette — secondary tones** — Shifted secondary blue from #2B6CB0 to #2A5FA5 per brand committee direction (Maya, 1 day)
- BRAND-25 **Typography scale — mobile** — Reduced body text from 16px to 15px, increased line height to 1.6 (Sam, 1 day)

### New Assets
- BRAND-30 **Social media templates** — 6 templates for Instagram, LinkedIn, and X (Maya, 3 days)
- BRAND-31 **Email header variants** — Light and dark mode versions (Sam, 2 days)

### Direction Changes
- BRAND-26 **Icon style** — Switched from outlined to filled per Round 2 feedback. Full icon set rebuilt (Maya, 4 days)
- BRAND-27 **Photography guidelines** — Added warm filter direction, removed cool-tone examples (Sam, 1 day)

---

## Scope Changes
- ➕ **Added:** BRAND-31 Email headers — added after marketing identified gap
- ➖ **Deferred:** BRAND-29 Motion guidelines — moved to Round 4, needs video team input

---

## Carried Over
- BRAND-28 **Slide deck template** — 60% complete, complex layouts remaining (est. 2 days)
- BRAND-32 **Favicon variants** — Not started, blocked by final logo approval
- BRAND-33 **Print guidelines** — Waiting on final CMYK color specs from printer

---

## Notes
- Icon style rebuild (BRAND-26) was the biggest effort — 48 icons rebuilt from outlined to filled
- Photography direction now aligns with Round 2 feedback from brand committee
- Round 4 (final) should focus on motion, remaining templates, and print specs
```

### Example 3: Delta — Legal Document Review

**User:** "What changed on the MSA since opposing counsel's redline on Feb 10?"

```markdown
# Changes Since Your Last Review | Master Services Agreement v4

**Last review:** Feb 10 by Martinez & Associates (opposing counsel)
**Changes since:** 7 clauses

---

## Feedback Addressed
- ✅ **"Indemnification scope too broad (§8.2)"** — Narrowed to direct damages only. Removed consequential damages from indemnification obligations.
- ✅ **"Termination for convenience needs 60-day notice (§12.1)"** — Changed from 30-day to 60-day notice period as requested.
- ✅ **"Data handling clause needs GDPR specificity (§15.3)"** — Added explicit GDPR Article 28 processor obligations, sub-processor notification, and DPA reference.

## Feedback Outstanding
- ⏳ **"Liability cap should be 12 months, not 24 (§9.1)"** — Under internal review. Our risk team is evaluating. Expected response by Feb 25.

---

## Other Changes Since Feb 10
- §6.4 Payment terms — Changed net-45 to net-30 (our finance team requirement, separate from your redline)
- §14.2 Insurance minimums — Updated cyber liability minimum from $2M to $5M per our underwriter's new policy
- Exhibit B — Updated SOW template to match revised scope from Feb 12 call

---

## Net Impact
3 of 4 redline items addressed. Liability cap (§9.1) is still under review — this is the remaining substantive issue. Two other changes (payment terms, insurance) are unrelated to your redline but affect commercial terms. Recommend re-review of §6.4, §9.1, and §14.2 before signing.
```

### Example 4: Major — Training Materials New Version

**User:** "What's new in the Q2 onboarding curriculum?"

```markdown
# What's New | Q2 Onboarding Curriculum

**Period:** Jan → March (full revision cycle)
**Items completed:** 14 modules updated

---

## Highlights
- New AI tools module added — covers prompt engineering and responsible use
- Compliance section restructured around real scenarios instead of policy citations
- All video content re-recorded with updated product UI (v3.0)

---

## New Material
- **Module 12: AI Tools & Responsible Use** — 45-minute module covering approved AI tools, prompt engineering basics, data handling rules, and escalation paths
- **Scenario Library** — 8 interactive scenarios replacing static compliance slides, covering data handling, vendor management, and conflict of interest

## Updated Content
- **Modules 3-6: Product Training** — Re-recorded all 4 video walkthroughs to reflect v3.0 UI changes. Updated screenshots and exercises.
- **Module 9: Security Awareness** — Added section on social engineering via AI-generated content. Updated phishing examples.
- **Module 11: Performance Review Process** — Updated to reflect new quarterly check-in format (replacing annual reviews)

## Removed
- **Module 7b: Legacy System Overview** — Removed. Legacy system decommissioned Q1.

---

## Known Limitations
- AI Tools module (Module 12) references internal AI policy v2.1. If policy v2.2 ships before Q2 onboarding starts, module will need a quick update.
- Scenario Library currently web-only — mobile version planned for Q3.
```

---

## Key Principles

1. **Audience determines granularity** — Stakeholders get themes, teams get items, reviewers get deltas. Same changes, different lens.
2. **Use the domain's language** — "Redlines" not "fixes" for legal. "Rounds" not "sprints" for creative. "Revision cycles" not "deploys" for training.
3. **Honesty about scope** — Include what was deferred, removed, or didn't get done. Silence on scope changes erodes trust.
4. **Feedback closes the loop** — The delta tier exists to show stakeholders their input was heard and acted on.
5. **Track revision depth** — For iterative work (creative, legal, content), note which cycle/round this is. "Round 3 of 4" gives context that a flat summary doesn't.
6. **Connect to other skills** — Pull from `stakeholder-signoff` for feedback to address, `story-flow` for cycle time context, `risk-tracker` for resolved issues.

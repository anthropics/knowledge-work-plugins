---
name: audit
description: Audit a departmental briefing, draft legislation, or implementation plan against ministerial directives and governance standards.
arguments:
  - name: document
    description: The departmental document (briefing, bill, or plan) to audit.
  - name: baseline
    description: (Optional) The ministerial directive, manifesto point, or transcript to audit against.
---

# /audit Command

Analyze departmental advice for obfuscation, "slow-walking," and alignment with the Minister's intent.

## When to Use

Use this command when:
- A new departmental briefing arrives and requires critical scrutiny.
- Auditing draft legislation against specific ministerial instructions.
- Reviewing implementation plans for hidden delays or "bureaucratic friction."
- You need a "Traffic Light" assessment of a policy proposal.

## Workflow

### 1. Context Gathering

Ask the user to provide or confirm the "Baseline for Audit":
1. **Ministerial Directive**: Specific written or oral instructions.
2. **Policy Commitment**: Election manifesto or leadership statements.
3. **Procedural Norms**: Cabinet Manual or constitutional rules.
4. **Historical Context**: Previous versions of the document.

### 2. Strategic Audit (Using bureaucracy-redliner)

Execute the audit across four dimensions:
- **Redlining**: Identify passive voice, jargon, and accountability shifts.
- **Slow-Walk Check**: Detect committee bloat and vague milestones.
- **Budgetary Sanity**: Flag "gold-plating" or lack of benchmarking.
- **Legislative Impact**: Check for "stealth powers" and cross-law conflicts.

### 3. Output Generation

The command produces a **Ministerial Audit Report** containing:
1. **Traffic Light Summary**: Overall status (Red/Amber/Green).
2. **The "Translation" Table**: Converting "Officialese" into Plain English impacts.
3. **Interrogatory Questions**: 3-5 sharp questions for the department.
4. **Strategic Risk Radar**: Who gets angry, and what could go wrong?

## Example Session

**User:** `/audit document: briefing_on_housing_v2.pdf baseline: "Election commitment to build 50k houses by 2028"`

**System:**
```
Ministerial Audit - Housing Briefing v2

Audit baseline: Election commitment (50k houses by 2028).

[~] SCANNING DOCUMENT...
[~] APPLYING BUREAUCRACY REDLINER...

AUDIT COMPLETE.

Overall Status: ⚠ AMBER (Alignment Risk)

Key Findings:
1. "Officialese" Detected: The brief uses "Commence implementation in 2027" - this masks that actual construction won't start until after the next election.
2. Slow-Walk Flag: Proposes an "Inter-departmental Coordination Group" with a 12-month scoping phase.
3. Budgetary Bullshit: Contingency is set at 45% without clear justification.

Interrogatory Questions for the Department:
1. "Can you provide a specific date for 'shovels in the ground' rather than 'commencing implementation'?"
2. "Why does the coordination group require 12 months before delivery begins?"
3. "What is the market benchmark for the 45% contingency rate in this sector?"

Would you like to generate a full "Counter-Brief" based on this audit? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~ministerial-audit/bureaucracy-redliner` for deep analysis.
- **Preference**: Respects the user's "Preference Profile" (e.g., Detail Hawk vs. Strategic Lead).
- **Downstream**: Feeds into `/brief` and `/prep-meeting`.

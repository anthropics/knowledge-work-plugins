---
name: ministerial-audit/bureaucracy-redliner
description: This skill acts as a "strategic equalizer" for Ministers and Advisors to audit departmental advice. Use it to detect "officialese," identifying implementation "slow-walking," sanity-checking budgetary assumptions, and mapping legislative impacts across existing laws. Invoke when a user uploads a departmental briefing, draft legislation, or implementation plan for critical review.
version: 1.0.0
---

# Bureaucracy Redliner (Ministerial Auditor)

This skill empowers the Executive to bridge the information asymmetry between the bureaucracy and the Ministry. It provides a critical lens to detect obfuscation, surface hidden risks, and ensure that departmental advice aligns with political intent and financial reality.

**Important**: This skill is a strategic auditing tool. It does not provide formal legal advice, constitutional rulings, or financial audit certifications. It is designed to prepare the Minister for critical inquiry and strategic pushback.

## When to Use This Skill

Invoke when:
- Reviewing a departmental briefing paper (e.g., Cabinet Submission, Ministerial Briefing).
- Auditing draft legislation or regulations for "intent creep."
- Analyzing implementation plans for "bureaucratic friction" or delay tactics.
- Sanity-checking high-level costings and budgetary assumptions in proposals.
- Preparing for a meeting with Departmental Officials or Cabinet Committees.
- Identifying passive voice or jargon that masks accountability or shifts policy intent.

## Regulatory Context

| Jurisdiction | Baseline Framework | Procedural Standard | Compliance Trigger |
|--------------|--------------------|---------------------|--------------------|
| **AU/NZ (Baseline)** | Cabinet Manual / Constitution Act | Public Service Act, COPI | Cabinet Submission, Legislative Drafting |
| **United States (Lite)** | Executive Order / APA | GAO Standards | Federal Register, Congressional Briefing |
| **United Kingdom (Lite)** | Ministerial Code | Civil Service Code | Green Book, HMT Approvals |

### AU/NZ Specifics
- **Cabinet Manual**: The authoritative guide on central government processes and the conduct of Ministers.
- **Ministerial Code of Conduct**: Ethical and procedural expectations for the Executive.
- **COPI (NZ)**: Cabinet Office Policy Instructions for legislative development.
- **Public Service Act**: Defines the role of the apolitical bureaucracy in serving the government of the day.

## Quick Reference

1.  **Load Baseline**: Identify the Minister's intent (Policy Manifestos, Meeting Notes, past statements).
2.  **Scan for Obfuscation**: Use the "Officialese" detector to flag passive voice and jargon.
3.  **Audit Implementation**: Scan for "Slow-Walk" indicators (excessive committees, vague milestones).
4.  **Verify Financials**: Run the "Budgetary Bullshit Detector" on cost assumptions.
5.  **Map Impact**: Check the "Legislative Impact Map" for cross-law conflicts.
6.  **Assess Risk**: Generate a "Traffic Light" report showing alignment vs. risk.
7.  **Draft Inquiry**: Generate sharp "Interrogatory Questions" for the department.

## Detailed Guidance

### 1. "Officialese" & Obfuscation Detection
Identify language patterns designed to shift accountability or blur intent:
- **Passive Voice**: "It was decided..." vs. "The Minister decided..." (Masks who is responsible).
- **Vague Qualifiers**: "Appropriate," "Significant," "Substantial" (Subjective terms that avoid hard metrics).
- **Euphemisms**: "Strategic realignment" usually means "Cutting services" or "Closing an office."
- **Non-Denial Denials**: Complex sentences that appear to answer a question but actually address a different point.

### 2. "Slow-Walk" Detection
Identify tactics that delay ministerial intent:
- **Committee Bloat**: Proposing new "Steering Groups," "Working Parties," or "Inter-departmental Taskforces" without clear end-dates.
- **Consultation Loops**: Endless rounds of "further consultation" with the same stakeholders to delay a decision.
- **Vague Milestones**: "Implementation will commence in Q3" (Commence what? Planning or delivery?).
- **Complex Dependencies**: Claiming an action "must wait for" an unrelated and slow-moving project.

### 3. Budgetary Bullshit Detector
Sanity-check the numbers presented by officials:
- **Gold-Plating**: Identifying unusually high contingency funds (e.g., >30%) or unexplained "operational overheads."
- **Lack of Benchmarking**: Flagging when costs are significantly higher than market rates or similar projects in other sectors.
- **Sunk Cost Fallacy**: Arguments for more funding purely because "we've already spent $X million."
- **Optimism Bias**: Underestimating long-term maintenance or IT integration costs.

### 4. Legislative Impact Map
Check for "Intent Creep" in drafting:
- **Cross-Law Conflicts**: Does this new regulation accidentally contradict a provision in the *Privacy Act* or *Public Finance Act*?
- **Stealth Powers**: Flagging clauses that grant unusually broad discretionary power to the Secretary or CEO.
- **Omission Check**: Did the "Explanatory Memo" promise a protection that didn't make it into the final Bill clauses?

### 5. Preference Profile (Customization)
The audit depth and tone should be configured based on the user's role:
- **Detail Hawk**: High sensitivity to every phrasing change; focus on technical precision.
- **Strategic Lead**: Focus on "Traffic Light" risks and "Doorstop" soundbites.
- **Risk Neutral/Averse**: Adjust the "Red/Amber" thresholds for policy alignment.

## Documentation Requirements

- [ ] **Baseline Comparison**: Document the specific policy/manifesto point being audited against.
- [ ] **Redline Summary**: List of identified jargon/obfuscation points with "Translation" to plain English.
- [ ] **Risk Matrix**: Traffic light assessment (Red/Amber/Green) for Alignment, Cost, and Timeline.
- [ ] **Implementation Audit**: Specific flags for "Slow-Walk" tactics identified.
- [ ] **Interrogatory List**: 3-5 sharp questions ready for the next departmental briefing.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Accepting "Technical Complexity" as a delay excuse | Often a cover for departmental disagreement with the policy. | Ask for a breakdown of the specific technical hurdles and alternative "Agile" delivery models. |
| Trusting "Stakeholder Consensus" blindly | "Stakeholders" may be a curated list of departmental allies. | Ask for a list of who was *not* consulted and why. |
| Focusing on the Summary, not the Bill | Summaries are often written by comms staff; the Bill is written by lawyers. Intent diverges here. | Audit the Bill clauses directly against the Cabinet Minute. |
| Ignoring the "Status Quo" bias | Departments naturally favor existing systems over radical change. | Explicitly ask for an "Option 4" that breaks the current system. |

## When to Escalate

Escalate to the Chief of Staff or the Minister when:
- The department refuses to provide the raw data or cost models underlying a brief.
- A "Slow-Walk" tactic is detected in a "Priority 1" election commitment.
- The audit detects a significant contradiction between the brief and the Minister's past public statements.
- The "Budgetary Bullshit Detector" flags a >50% discrepancy from market benchmarks.

## Privacy Considerations

- **PHI/PII**: Generally Low (policy focused), but may involve sensitive personal data in individual case briefings.
- **Confidentiality**: HIGH. Briefings are often Cabinet-in-Confidence.
- **Data Minimization**: Do not upload highly classified or "Top Secret" documents.
- **Retention**: Audit notes and "Counter-Briefs" are part of the Ministerial record and should be managed according to the *Public Records Act*.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Direct contradiction between Manifesto and Bill | High | Flag as Red; generate immediate pushback questions. |
| Passively voiced briefing with vague timelines | Medium | Flag for "Slow-Walk" audit; ask for a Gannt chart. |
| Complex financial models with no benchmark data | Low | Flag for "Budgetary Bullshit"; request raw model. |

## Standard and Lite Modes

- **Standard**: Full multi-source audit, annotated redline, and "Counter-Brief" suite generation.
- **Lite**: Rapid "Jargon Check" and "Doorstop" summary for a quick read on the move.

## Tool Requirements

- `~~web-search` - For checking media sentiment and international precedents.
- `~~document-compare` - For tracking changes between briefing versions.
- `~~openclaw` - (Optional) For social media monitoring.

## Success Indicators

You've applied this skill well when:
- [ ] The Minister is briefed on a hidden risk *before* the department mentions it.
- [ ] Departmental officials are "surprised" by the specificity and sharpness of the Minister's questions.
- [ ] A "Slow-Walk" implementation plan is successfully challenged and accelerated.
- [ ] A budget "Gold-Plating" attempt is identified and reduced.

## Related Skills

- `~~ministerial-audit/strategic-synthesis` - For generating "Option 4s" and Risk Radars.
- `~~ministerial-audit/wargaming` - For simulating Cabinet pushback.
- `~~ministerial-audit/comms-translator` - For "Doorstop" summaries and social posts.

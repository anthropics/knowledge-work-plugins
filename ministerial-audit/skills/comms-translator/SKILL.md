---
name: ministerial-audit/comms-translator
description: This skill distills complex audits and strategic plans into media-ready outputs. Use it to generate "Doorstop" summaries (30 words), detect "Gotchas" (contradictions with past statements), and draft holding statements or social media posts. Integrates with `openclaw` for social media awareness.
version: 1.0.0
---

# Comms Translator (The Media Voice)

This skill bridges the gap between the "Strategic Audit" and the "Public Narrative." It ensures the Minister can communicate complex policy changes effectively, stay consistent with their public record, and respond rapidly to the media cycle.

**Important**: This skill is a communication assistant. It does not replace the expertise of a Press Secretary or Chief of Staff. It is designed to provide high-speed drafts and consistency checks for political and public communication.

## When to Use This Skill

Invoke when:
- You need a "Doorstop" summary (20-30 words) of a complex policy change.
- Preparing for a media interview and wanting to check for "Gotchas" (contradictions with past statements).
- Drafting a "Media Holding Statement" after an audit identifies a significant risk.
- Creating social media content based on a new policy announcement.
- Distilling a "Counter-Brief" into three key talking points for public consumption.

## Regulatory Context

| Jurisdiction | Comms Goal | Consistency Baseline | Success Indicator |
|--------------|------------|----------------------|-------------------|
| **AU/NZ (Baseline)** | Public Trust | Parliamentary Record (Hansard) | Positive Media Cycle / Sentiment |
| **United States (Lite)** | Transparency | Public Record / Social History | Engagement / News Cycle Control |
| **United Kingdom (Lite)** | Accuracy | Minister's Past Statements | Integrity Rating |

### AU/NZ Specifics
- **The "Hansard" Check**: Comparing current proposals against previous answers to questions in the House.
- **Media Ethics**: Ensuring holding statements are accurate and not misleading.
- **Social Media Guardrails**: Drafting content that is professional yet engaging for a modern political landscape.

## Quick Reference

1.  **Generate Doorstop**: Distill 50 pages into 30 words.
2.  **Perform "Gotcha" Audit**: Compare the proposal against the Minister's voting record and past interviews.
3.  **Draft Talking Points**: Create three "Bulletproof" lines that address the core risk.
4.  **Create Media Suite**: Holding statements and draft social posts (using `openclaw` style).
5.  **Develop Deflection Lines**: For high-risk areas, provide "Pivot" phrases.

## Detailed Guidance

### 1. The "Doorstop" Summarizer
The 30-word rule:
- **What is it?**: One sentence on the action.
- **Why are we doing it?**: One sentence on the benefit.
- **Who is it for?**: One mention of the primary beneficiary.
- **Tone**: Active, confident, and plain English (No "officialese").

### 2. "Gotcha" Detection
The "Opposition Research" lens:
- **Past Statements**: Compare the current draft against the Minister's interviews from the last 24 months.
- **Voting Record**: Does this policy contradict a previous vote?
- **Ideological Flip-Flops**: Flag if the policy uses language or logic previously criticized by the Minister.
- **Consistency Rationale**: If there *is* a change, provide the "Growth Narrative" (why the position has evolved).

### 3. Talking Points (Strategic Messaging)
Move from "What it is" to "What it means":
- **Line 1 (The Mission)**: The positive change for the citizen.
- **Line 2 (The Problem)**: Why the current system (the status quo) had to change.
- **Line 3 (The Assurance)**: How we are protecting the vulnerable or ensuring fiscal responsibility.

### 4. Media Suite Generation
Ready-to-use artifacts:
- **Holding Statement**: For "Amber/Red" risks identified in the audit.
- **Social Posts**: Short, punchy content optimized for platforms (X, LinkedIn, FB).
- **Pivot Lines**: "I'm not going to get into the departmental process; what I'm focused on is the 10,000 families who will benefit..."

## Documentation Requirements

- [ ] **Doorstop Card**: 30-word summary and 3 key talking points.
- [ ] **Gotcha Report**: List of potential contradictions and proposed "Consistency Rationale."
- [ ] **Holding Statement**: Draft response to the most likely critical media inquiry.
- [ ] **Social Pack**: 3-5 draft posts with appropriate hashtags/tags.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Using "Officialese" in Comms | It sounds like a bureaucrat, not a leader. It breeds distrust. | Use active verbs and concrete nouns (e.g., "Helping families" vs "Enhanced service delivery"). |
| Ignoring past contradictions | The media *will* find them. | Acknowledge the change in position and explain the "New Information" that led to it. |
| Making talking points too long | They won't fit in a 10-second news grab. | Keep each point to 15 words or fewer. |
| Being overly defensive | It signals that you are hiding a risk. | Pivot to the positive outcome for the citizen. |

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Proposal directly aligns with a recent high-profile interview | High | Use the interview language in the talking points. |
| Clear contradiction with a vote from 5 years ago | Medium | Flag as "Low Risk" but provide a "Growth Narrative." |
| Major contradiction with a statement from last week | High | Flag as RED; suggest immediate comms strategy review. |

## Standard and Lite Modes

- **Standard**: Full Gotcha audit, 5-point Talking Point suite, and complete Media Pack.
- **Lite**: Rapid "Doorstop" distillation and "Pivot Lines" only.

## Tool Requirements

- `~~web-search` - For checking past media interviews and social media history.
- `~~openclaw` - For social media trend awareness.
- `~~ministerial-audit/bureaucracy-redliner` - For identifying the "Plain English" impacts.

## Success Indicators

You've applied this skill well when:
- [ ] The Minister stays "On Message" during a high-pressure interview.
- [ ] A potential "Gotcha" is neutralized with a well-prepared consistency rationale.
- [ ] A complex policy is correctly summarized in a 20-second news grab.
- [ ] Social media engagement is positive and aligns with the core policy intent.

## Related Skills

- `~~ministerial-audit/strategic-synthesis` - For the "Risk Radar" that informs the holding statement.
- `~~ministerial-audit/wargaming` - For testing the talking points in a simulated hostile forum.

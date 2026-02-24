# Specification: Ministerial Audit Plugin (ministerial-audit)

## Overview
This plugin acts as a "strategic equalizer" for Ministers and Ministerial Advisors, providing them with the tools to audit, verify, and challenge work produced by departmental officials. It bridges the information asymmetry between the bureaucracy and the executive by using AI to detect obfuscation, ensure policy alignment, and prepare for strategic pushback.

## User Personas
- **Ministers:** Strategic synthesis, risk assessment, and meeting preparation.
- **Ministerial Advisors:** Auditing, jargon detection, and drafting counter-narratives.

## Functional Requirements
- **Multi-Source Audit Engine:** Auditing drafts against:
    - Political commitments (manifestos, past statements, voting records).
    - Procedural rules (Cabinet Manual, constitutional norms).
    - External context (media, grey literature, lobbyist submissions).
    - **Budgetary "Bullshit" Detector:** Sanity checking financial assumptions.
    - **Legislative Impact Map:** Identifying cross-law conflicts.
- **Bureaucracy "Redlining":**
    - **Jargon Detection:** Identifying "officialese" that masks risk.
    - **Slow-Walk Detection:** Flagging implementation plans designed for delay (excessive committees/consultation).
- **The "Counter-Brief" Suite:**
    - **Traffic Light Report:** High-level political/policy risk summary.
    - **Annotated Redline:** Inline commentary on departmental documents.
    - **Option 4 Generator:** Developing the omitted ideological alternative to departmental "Option 3s."
    - **Sunset & Review Recommender:** Built-in accountability/exit triggers.
- **Strategic Stress-Testing:**
    - **Wargaming:** Predicting questions from other Cabinet Ministers (Treasury/AG).
    - **Edge Case Finder:** Testing policy against vulnerable personas or sensitive scenarios.
    - **Evidence Scrutiny:** Detecting circular citations or cherry-picked data.
    - **Precedent Finder:** Cross-jurisdictional "proof of concept" examples (UK, Canada, etc.).
    - **Consultation Auditor:** Identifying missing stakeholder perspectives.
- **Communication & Response:**
    - **Interrogatory Questions:** Sharp questions for officials.
    - **The Doorstop:** 20-second soundbites and deflection lines.
    - **Media Suite:** Holding statements and draft social media posts (integrating with `openclaw` conventions).

## Non-Functional Requirements
- **Preference Profile:** Configuring the audit for the specific Minister's risk tolerance and style.
- **Jurisdictional Awareness:** Defaulting to AU/NZ standards (Cabinet Manual) with portability.

## Acceptance Criteria
- Commands: `/audit`, `/brief`, `/prep-meeting`, `/check-evidence`.
- Successful detection of "Option 3 traps," "bureaucratic friction," and "consultation gaps."
- Generation of the full "Counter-Brief" suite from a single set of inputs.

## Out of Scope
- Direct connection to internal government EDRMS.
- Formal legal/constitutional advice.
- Processing of highly classified material.

---
name: ministerial-audit/wargaming
description: This skill prepares Ministers for high-stakes meetings (Cabinet, Select Committees, Media) by simulating opposition and stress-testing policy. Use it to predict "Treasury/AG" questions, decode lobbyist submissions (Lobbyist X-Ray), find international precedents, and stress-test policy against "Edge Case" personas.
version: 1.0.0
---

# Wargaming & Defense (The Meeting Prep)

This skill prepares the Minister for the "actual" meeting by simulating the pressures of the Cabinet Committee room, the hostile press gallery, or the critical cross-examination of the Department of Finance. It focuses on finding the weaknesses in a proposal *before* someone else does.

**Important**: This skill is a simulation and stress-testing tool. It does not replace formal inter-departmental consultation but helps the Minister navigate it with a "strategic advantage."

## When to Use This Skill

Invoke when:
- Preparing for a Cabinet Committee meeting where other Ministers (Treasury, Finance, AG) will be present.
- Analyzing an external submission from a lobby group or industry body (Lobbyist X-Ray).
- Searching for proof-of-concept for a radical idea (Precedent Finder).
- Stress-testing a proposed law against vulnerable or specific citizens (Edge Case Finder).
- Preparing for a "Doorstep" or media interview on a controversial topic.

## Regulatory Context

| Jurisdiction | Opposition Persona | Success Indicator |
|--------------|-------------------|-------------------|
| **AU/NZ (Baseline)** | Treasury / Finance / AG | Cabinet Minute Approval |
| **United States (Lite)** | OMB / CBO / Congress | Budget Appropriation |
| **United Kingdom (Lite)** | HM Treasury / No. 10 | HMT Green Book Approval |

### AU/NZ Specifics
- **The "Treasury Question"**: Focus on fiscal impact, efficiency, and market intervention risks.
- **The "Attorney General Question"**: Focus on constitutional risk, judicial review, and the Bill of Rights.
- **Cabinet Collective Responsibility**: Ensuring the Minister is ready to defend the policy to the whole Cabinet.

## Quick Reference

1.  **Simulate Colleague Pushback**: Predict the "Kill Shots" from Treasury or Finance.
2.  **Run Lobbyist X-Ray**: Identify the hidden "Ask" in industry submissions.
3.  **Find Precedent**: Look for international "Proof of Concept" (UK, Canada, EU).
4.  **Stress Test Edge Cases**: Run the logic against a "Vulnerable Single Parent" or "Small Rural Business" persona.
5.  **Draft Interrogatory Prep**: Practice responding to sharp, hostile questions.

## Detailed Guidance

### 1. Cabinet Colleague Personas
Simulate the specific "Lens" that other Ministers will apply:
- **Treasury/Finance**: Focus on "Deadweight loss," "Moral hazard," and "Total Cost of Ownership."
- **Attorney General (AG)**: Focus on "Legislative overreach" and "Procedural fairness."
- **Social Ministers**: Focus on "Equity gaps" and "Service delivery friction."

### 2. Lobbyist X-Ray (Decoding Submissions)
Don't read what they wrote; read what they *want*:
- **The Hidden "Ask"**: Identify the specific regulatory change or funding stream they are targeting.
- **The Omitted Fact**: Flag the data point or alternative model the lobbyist has conveniently ignored.
- **Beneficiary Analysis**: Who *really* makes money if this lobbyist's advice is taken?

### 3. Precedent Finder (International Proof)
Counter the "It’s never been done" argument:
- **Jurisdictional Search**: Find similar policies in comparable systems (NZ, AU, UK, CA, EU).
- **Lessons Learned**: Identify the "Implementation Failures" in those jurisdictions so the Minister can avoid them.
- **Validation**: Use international success as "Evidence" to bypass local departmental resistance.

### 4. Edge Case Stress-Testing
Policy often works for the "average" but fails for the "extreme":
- **Vulnerable Personas**: How does this impact someone with no digital access? Or a single parent working three jobs?
- **Small Business Persona**: Does this add 20 hours of compliance work to a 2-person firm?
- **The "Scandal" Scenario**: If the system fails in X way, what is the most damaging headline?

## Documentation Requirements

- [ ] **Cabinet Q&A Prep**: A list of the 10 hardest questions Treasury/Finance/AG will ask, with draft responses.
- [ ] **Lobbyist X-Ray Report**: A one-page "Decoding" of major external submissions.
- [ ] **Precedent Brief**: 3 international examples of this policy in action.
- [ ] **Stress-Test Log**: Results of running the policy against 3 different "Edge Case" personas.

## Common Mistakes (Anti-Patterns)

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| "Preaching to the Converted" | Only simulating supporters. | Always simulate the *most hostile* possible colleague or journalist. |
| Ignoring the "Crown Law" risk | Ministers often underestimate the risk of a Judicial Review. | Explicitly run the "AG Persona" check. |
| Trusting Lobbyist "Data" | It is curated for a specific outcome. | Use the X-Ray to find the data they *didn't* include. |
| Searching only for "Successes" | You won't be ready for the "Failure" arguments. | Search for where this policy *failed* internationally and explain how you've fixed it. |

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Strong international precedent found for a "radical" idea | High | Present as "Proven Best Practice" to officials. |
| Major constitutional risk identified in AG persona check | High | Flag as RED; suggest immediate legal consultation. |
| Lobbyist submission has a clear, hidden commercial beneficiary | Medium | Flag for the Minister; prepare "Conflict of Interest" questions. |

## Standard and Lite Modes

- **Standard**: Full Cabinet simulation, international precedent search, and multi-persona stress testing.
- **Lite**: Rapid "Hardest 3 Questions" prep and a quick "Precedent Search."

## Tool Requirements

- `~~web-search` - Essential for international precedent and lobbyist background.
- `~~ministerial-audit/bureaucracy-redliner` - For identifying the bill clauses to stress-test.

## Success Indicators

You've applied this skill well when:
- [ ] The Minister is *not* surprised by a question in Cabinet.
- [ ] A "Proof of Concept" from another country is used to win a policy argument.
- [ ] A hidden lobbyist agenda is exposed and neutralized.
- [ ] A policy is modified to fix an "Edge Case" flaw before it becomes a scandal.

## Related Skills

- `~~ministerial-audit/strategic-synthesis` - For providing the "Option 4" to be wargamed.
- `~~ministerial-audit/comms-translator` - For turning wargame results into "Doorstop" soundbites.

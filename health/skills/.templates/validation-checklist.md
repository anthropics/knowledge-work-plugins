# Health Skill Quality Validation Checklist

Use this checklist to validate health skills against the 14-section architecture and quality gates defined in `conductor/tracks/health-plugin/skill-standards.md`.

## Pre-Validation Setup

- [ ] Identify the skill file: `health/skills/{skill-name}/SKILL.md`
- [ ] Review associated metadata if present
- [ ] Confirm skill domain and applicable regulations
- [ ] Identify related health skills for cross-reference validation

---

## Section 1: Frontmatter Validation

**Location**: Lines 1-5 (YAML frontmatter)

### Required Fields
- [ ] `name` field present and follows format `health/{skill-name}`
- [ ] `name` is unique and domain-specific
- [ ] `description` field present
- [ ] `description` starts with "This skill should be used when..."
- [ ] `description` includes concrete trigger phrases
- [ ] `version` field present (semantic versioning format)

### Quality Checks
- [ ] Name is specific to healthcare domain (not generic)
- [ ] Description clearly indicates when to invoke
- [ ] No placeholder text (e.g., "TODO", "TBD", "FIXME")
- [ ] Version follows semver (MAJOR.MINOR.PATCH)

---

## Section 2: When to Use This Skill

**Requirement**: Minimum 5 lines

### Content Validation
- [ ] Section header present: `## When to Use This Skill`
- [ ] Contains explicit healthcare scenarios
- [ ] Includes clinical/operational context
- [ ] Lists at least 4-6 trigger conditions
- [ ] Triggers are specific and actionable

### Quality Checks
- [ ] No vague statements (e.g., "when needed")
- [ ] Triggers cover common use cases
- [ ] Language is appropriate for healthcare context

---

## Section 3: Regulatory Context

**Requirement**: Minimum 10 lines, AU/NZ-default + US/EU-lite

### Australia & New Zealand Baseline
- [ ] AU/NZ regulations table present
- [ ] At least 3 AU/NZ regulations/standards listed
- [ ] Columns: Regulation/Standard, Relevance, Key Requirements
- [ ] Specific requirements are actionable

### US/EU-lite Portability
- [ ] US/EU-lite section present
- [ ] Adaptation notes for US context included
- [ ] Adaptation notes for EU context included
- [ ] Key differences from AU/NZ documented

### Jurisdiction Matrix
- [ ] Matrix table present
- [ ] Columns: Jurisdiction, Applicable Regulator, Reporting Trigger, Timeframe, Required Artifacts, Escalation Point
- [ ] At least AU-National and NZ-National rows present
- [ ] AU-State row present (if state variations apply)
- [ ] US row present (for portability)
- [ ] All timeframes are specific (not "as soon as possible")
- [ ] Escalation points are specific roles/titles

### Quality Checks
- [ ] AU/NZ references precede other jurisdictions
- [ ] Regulations are current and accurate
- [ ] No placeholder content in tables
- [ ] Jurisdiction matrix is complete for skill domain

---

## Section 4: Operating Modes

**Requirement**: Standard and Lite modes documented

### Standard Mode
- [ ] Section header: `### Standard Mode`
- [ ] Describes full workflow
- [ ] Documents complete compliance checks
- [ ] Specifies appropriate use cases
- [ ] Indicates multidisciplinary engagement

### Lite Mode
- [ ] Section header: `### Lite Mode`
- [ ] Describes streamlined guidance
- [ ] Specifies appropriate use cases
- [ ] Explicitly states what is NOT suppressed:
  - [ ] High-risk escalation requirements
  - [ ] Mandatory reporting obligations
  - [ ] Patient safety considerations
  - [ ] Statutory compliance requirements

### Quality Checks
- [ ] Both modes clearly differentiated
- [ ] Lite mode warnings are prominent
- [ ] Use case guidance is practical

---

## Section 5: Quick Reference

**Requirement**: 5-10 bullet points (for complex skills)

### Content Validation
- [ ] Section header: `## Quick Reference`
- [ ] 5-10 actionable bullet points
- [ ] Covers most common scenarios
- [ ] Includes safety/compliance points
- [ ] Includes documentation reminders

### Quality Checks
- [ ] Bullets are concise but complete
- [ ] High-value information prioritized
- [ ] Suitable for quick scanning

---

## Section 6: Detailed Guidance

**Requirement**: Minimum 50 lines

### Structure Validation
- [ ] Section header: `## Detailed Guidance`
- [ ] Organized into logical phases or subsections
- [ ] Uses clear, descriptive headers
- [ ] Step-by-step process documented

### Content Quality
- [ ] Clinical considerations addressed (if applicable)
- [ ] Administrative requirements included
- [ ] Decision points documented
- [ ] Integration with care workflows described
- [ ] No gaps in critical path

### Quality Checks
- [ ] Instructions are actionable
- [ ] Healthcare context is clear
- [ ] Cross-references to procedures/policies included
- [ ] Examples provided where helpful

---

## Section 7: Documentation Requirements

**Requirement**: Minimum 10 lines

### Required Elements
- [ ] Section header: `## Documentation Requirements`
- [ ] Checkbox list of required elements present
- [ ] At least 5 required elements listed
- [ ] Audit trail requirements specified
- [ ] Retention guidelines table present

### Quality Checks
- [ ] Documentation aligns with medical record standards
- [ ] Retention periods are specific
- [ ] Storage requirements specified
- [ ] Format standards indicated

---

## Section 8: Common Mistakes

**Requirement**: Minimum 10 lines, at least 5 mistakes

### Table Validation
- [ ] Section header: `## Common Mistakes`
- [ ] Table with 3 columns: Mistake, Why It's Wrong, Instead
- [ ] At least 5 documented mistakes
- [ ] All columns populated for each row

### Quality Checks
- [ ] Mistakes are healthcare-specific
- [ ] Explanations include clinical/regulatory risk
- [ ] "Instead" column provides actionable alternative
- [ ] Common anti-patterns covered
- [ ] No trivial or obvious mistakes listed

---

## Section 9: When to Escalate

**Requirement**: Minimum 5 lines

### Content Validation
- [ ] Section header: `## When to Escalate`
- [ ] Clear escalation role/title specified
- [ ] At least 5 escalation criteria listed
- [ ] Bullet format for criteria

### Quality Checks
- [ ] Criteria are specific and actionable
- [ ] Patient safety criteria prominent
- [ ] Regulatory triggers included
- [ ] Resource/authority limits covered
- [ ] Criteria are realistic and appropriate

---

## Section 10: Privacy Considerations

**Requirement**: Minimum 10 lines, PHI/PII guardrails

### PHI/PII Handling
- [ ] Section header: `## Privacy Considerations`
- [ ] Subsection: `### PHI/PII Handling`
- [ ] PHI Involved: Yes/No/Conditional specified
- [ ] Data minimization guidance present
- [ ] De-identification guidance present
- [ ] Access controls specified

### Security Guardrails
- [ ] Subsection: `### Security Guardrails`
- [ ] No Logging of PHI rule stated
- [ ] Temporary workspace guidance
- [ ] No Persistence rule stated
- [ ] Transmission security noted

### Retention and Disposal
- [ ] Subsection: `### Retention and Disposal` (if applicable)
- [ ] Output retention periods specified
- [ ] Secure disposal procedures
- [ ] Audit records guidance

### Quality Checks
- [ ] Guardrails are explicit and specific
- [ ] HIPAA/Privacy Act principles reflected
- [ ] Technical safeguards mentioned
- [ ] Appropriate for skill domain

---

## Section 11: Confidence Indicators

**Requirement**: Minimum 8 lines, at least 3 scenarios

### Table Validation
- [ ] Section header: `## Confidence Indicators`
- [ ] Table with 3 columns: Scenario, Confidence, Action
- [ ] At least 3 scenarios documented
- [ ] All confidence levels represented (High/Medium/Low)

### Quality Checks
- [ ] Scenarios cover typical use cases
- [ ] High confidence scenarios include safe autonomy
- [ ] Low confidence scenarios require human review
- [ ] Medium confidence scenarios flag for review
- [ ] Patient safety scenarios marked Low
- [ ] Actions are specific and appropriate

---

## Section 12: Tool Requirements

**Requirement**: Minimum 5 lines

### Content Validation
- [ ] Section header: `## Tool Requirements`
- [ ] Bullet list of required tools
- [ ] `~~health/core` referenced (if applicable)
- [ ] Healthcare-specific tools listed
- [ ] MCP connector format used (`~~tool-name`)

### Quality Checks
- [ ] Tools are relevant to workflow
- [ ] Core health plugin referenced
- [ ] Clinical systems noted if applicable
- [ ] No generic tools without context

---

## Section 13: Success Indicators

**Requirement**: Minimum 5 lines, at least 3 indicators

### Content Validation
- [ ] Section header: `## Success Indicators`
- [ ] Introductory sentence present
- [ ] Checkbox list format
- [ ] At least 3 indicators listed

### Quality Checks
- [ ] Indicators are measurable
- [ ] Compliance verification included
- [ ] Documentation quality addressed
- [ ] Clinical accuracy noted (if applicable)
- [ ] Audit trail completion verified
- [ ] Cross-reference consultation noted

---

## Section 14: Related Skills

**Requirement**: Minimum 3 lines, at least 2 related skills

### Content Validation
- [ ] Section header: `## Related Skills`
- [ ] Bullet list format
- [ ] At least 2 related skills listed
- [ ] Preferably within health plugin

### Quality Checks
- [ ] Relationships are described
- [ ] Usage guidance provided
- [ ] Cross-references are valid
- [ ] Skills actually exist or are planned

---

## Quality Gates Verification

### Length Requirements
- [ ] Total skill length >= 300 lines
- [ ] Detailed Guidance section >= 50 lines

### Content Completeness
- [ ] No placeholder content ("TODO", "TBD", "FIXME", "XXX")
- [ ] No empty sections
- [ ] All tables have content in all cells
- [ ] No "N/A" without explanation

### Healthcare-Specific Requirements
- [ ] Healthcare disclaimers present
- [ ] Clinical safety addressed
- [ ] Regulatory compliance covered
- [ ] Patient safety prominent
- [ ] Audit trail requirements specified

### Cross-References
- [ ] All internal links valid
- [ ] Related skills exist or documented as planned
- [ ] External references current

### Jurisdiction Requirements
- [ ] AU/NZ-default matrix complete
- [ ] US/EU-lite guidance present
- [ ] Baseline jurisdiction file referenced
- [ ] Portability notes accurate

---

## Final Validation Steps

### Readability
- [ ] Markdown renders correctly
- [ ] Tables are properly formatted
- [ ] Headers are hierarchical and consistent
- [ ] Bullet lists are properly indented

### Style Compliance
- [ ] Voice and tone appropriate for healthcare
- [ ] Terminology consistent with domain
- [ ] Acronyms defined on first use
- [ ] Jargon minimized or explained

### Final Check
- [ ] Run validation script: `python conductor/scripts/validate_health_skills.py`
- [ ] Address all reported errors
- [ ] Document any intentional deviations
- [ ] Obtain domain expert review (recommended)

---

## Sign-Off

| Reviewer | Date | Result | Notes |
|----------|------|--------|-------|
| [Name] | [Date] | [Pass/Fail] | [Comments] |

---

## Appendix: Quick Reference Card

### Critical Checks (Do Not Skip)
1. AU/NZ-default jurisdiction matrix present
2. US/EU-lite portability guidance present
3. PHI/PII guardrails complete
4. At least 5 Common Mistakes documented
5. At least 3 Confidence Indicator scenarios
6. Healthcare disclaimers included
7. Minimum 300 lines total
8. No placeholder content

### Section Count
- Required sections: 14
- Minimum length: 300 lines
- Mistakes documented: >= 5
- Confidence scenarios: >= 3
- Related skills: >= 2
- Success indicators: >= 3

### Pass Criteria
- All 14 sections present and populated
- All quality gates met
- No validation script errors
- Healthcare context appropriate

---
name: health/{skill-name}
description: This skill should be used when the user asks to "[trigger 1]", "[trigger 2]", or needs assistance with [domain-specific activity].
version: 0.1.0
---

# {Skill Name}

Brief introduction (1-2 sentences) describing the skill's purpose in healthcare context. This skill assists clinicians, administrators, and healthcare staff with [specific domain] workflows while ensuring compliance with regulatory requirements.

**Important**: This skill assists with clinical and operational workflows but does not provide clinical advice or replace professional judgment. Always verify outputs against organizational policies and applicable regulations.

## When to Use This Skill

Invoke this skill when:
- User mentions [specific healthcare scenario 1 - be explicit about clinical/operational context]
- User asks about [specific workflow or process]
- Context indicates [specific need or trigger]
- User requests assistance with [domain-specific task]
- Document analysis reveals [specific pattern requiring this skill]
- Conversation involves [relevant regulatory or compliance matter]

## Regulatory Context

### Australia & New Zealand (Default Baseline)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **[Primary Regulation]** (AU/NZ) | [How it applies to this skill's domain] | [Specific requirements relevant to workflow] |
| **[Secondary Regulation]** (AU/NZ) | [Relevance description] | [Key compliance points] |
| **State/Territory Acts** | Jurisdiction-specific variations | [Applicable state-level requirements] |
| **Organizational Policy** | Internal compliance | [Required policy adherence] |

### US/EU-lite Portability Guidance

When users request US or EU contexts, adapt guidance as follows:

| Regulation/Standard | Relevance | Adaptation Notes |
|---------------------|-----------|------------------|
| **[US Regulation]** (e.g., HIPAA, Joint Commission) | [How it applies] | [Key differences from AU/NZ baseline] |
| **[EU Regulation]** (e.g., GDPR, MDR) | [How it applies] | [Key differences from AU/NZ baseline] |
| **International Standard** (e.g., ISO) | [Relevance] | [Portability considerations] |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - National** | [Regulator name] | [Trigger condition] | [SLA] | [Documentation required] | [Role/Title] |
| **AU - State** | [State regulator] | [Trigger condition] | [SLA] | [Documentation required] | [Role/Title] |
| **NZ - National** | [NZ regulator] | [Trigger condition] | [SLA] | [Documentation required] | [Role/Title] |
| **US** | [US regulator] | [Trigger condition] | [SLA] | [Documentation required] | [Role/Title] |

## Quick Reference

1. **[Key Point 1]**: Brief actionable guidance for common scenarios.
2. **[Key Point 2]**: Essential step or consideration.
3. **[Key Point 3]**: Critical compliance or safety point.
4. **[Key Point 4]**: Best practice reminder.
5. **[Key Point 5]**: Documentation or audit requirement.
6. **[Key Point 6]**: Escalation trigger to remember.
7. **[Key Point 7]**: Privacy or security consideration.
8. **[Key Point 8]**: Common pitfall to avoid.

## Operating Modes

### Standard Mode

Full workflow with complete documentation, comprehensive compliance checks, multidisciplinary stakeholder engagement, and formal governance approval processes. Use for:
- Complex or high-risk scenarios
- Regulatory-mandated activities
- Accreditation-related work
- First-time implementations
- Cross-functional initiatives

### Lite Mode

Streamlined guidance for rapid response, informal consultations, or constrained contexts. Provides essential steps and minimum safe practices. Use for:
- Quick reference or clarification
- Routine, low-risk activities
- Educational contexts
- Preliminary assessments

**Important**: Lite mode never suppresses:
- High-risk escalation requirements
- Mandatory reporting obligations
- Patient safety considerations
- Statutory compliance requirements

## Detailed Guidance

### Phase 1: [Initiation/Assessment]

[Detailed step-by-step guidance for the first phase of the workflow]

**Key Activities**:
1. [Specific action with healthcare context]
2. [Next action with compliance consideration]
3. [Action requiring documentation]

**Decision Points**:
- [Criterion for path A vs path B]
- [When to proceed vs when to escalate]

### Phase 2: [Processing/Execution]

[Detailed guidance for the main workflow phase]

**Clinical Considerations**:
- [Patient safety point]
- [Clinical accuracy requirement]
- [Integration with care workflow]

**Administrative Requirements**:
- [Documentation standard]
- [Approval workflow]
- [Communication protocol]

### Phase 3: [Completion/Review]

[Guidance for finalizing and reviewing work]

**Quality Checks**:
- [Verification step 1]
- [Verification step 2]
- [Compliance confirmation]

## Documentation Requirements

### Required Elements

- [ ] [Documentation element 1 - specific to medical record standards]
- [ ] [Documentation element 2 - audit trail requirement]
- [ ] [Documentation element 3 - compliance evidence]
- [ ] [Documentation element 4 - stakeholder communication record]
- [ ] [Documentation element 5 - decision rationale]

### Audit Trail Requirements

- Timestamp of all key decisions
- Identity of decision-makers and reviewers
- Version history of documents
- Evidence of compliance checks
- References to applicable policies/procedures

### Retention Guidelines

| Document Type | Retention Period | Storage Requirements |
|---------------|------------------|---------------------|
| [Type 1] | [Period, e.g., 7 years] | [Security level, access controls] |
| [Type 2] | [Period] | [Storage requirements] |

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **[Mistake 1]** | [Explanation of error and risk] | [Correct approach with rationale] |
| **[Mistake 2]** | [Explanation of error and risk] | [Correct approach with rationale] |
| **[Mistake 3]** | [Explanation of error and risk] | [Correct approach with rationale] |
| **[Mistake 4]** | [Explanation of error and risk] | [Correct approach with rationale] |
| **[Mistake 5]** | [Explanation of error and risk] | [Correct approach with rationale] |
| **[Mistake 6]** | [Optional additional mistake] | [Correct approach] |
| **[Mistake 7]** | [Optional additional mistake] | [Correct approach] |

## When to Escalate

Escalate to [appropriate role/title] when:
- Patient safety is or may be compromised
- [Escalation criterion 2 - specific to domain]
- [Escalation criterion 3 - regulatory or compliance trigger]
- [Escalation criterion 4 - resource or authority limitation]
- [Escalation criterion 5 - timeline or deadline risk]
- [Escalation criterion 6 - stakeholder conflict or resistance]
- [Escalation criterion 7 - unclear jurisdiction or authority]

## Privacy Considerations

### PHI/PII Handling

- **PHI Involved**: [Yes/No/Conditional - with explanation]
- **Data Minimization**: Use only the minimum necessary information for the specific task
- **De-identification**: [Guidance on when and how to de-identify data]
- **Access Controls**: Limit access to those with legitimate need

### Security Guardrails

- **No Logging of PHI**: Never include identifiable patient information in logs or chat history
- **Temporary Workspace**: Process PHI in secure, temporary environments only
- **No Persistence**: Do not store PHI in skill memory or persistent storage
- **Transmission Security**: Use secure channels for any PHI transfer

### Retention and Disposal

- **Output Retention**: [Specific retention period based on document type]
- **Secure Disposal**: Delete working copies when no longer needed
- **Audit Records**: Maintain non-identifiable audit logs per organizational policy

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Explicit, unambiguous documentation with clear workflow | High | Proceed with standard guidance; document actions |
| Conflicting information or ambiguous requirements | Medium | Flag for human review; summarize conflicts and recommendations |
| High-risk clinical or compliance decision | Low | Draft options with pros/cons; REQUIRE human sign-off |
| Novel situation without established precedent | Low | Consult with subject matter expert; document rationale |
| Time-critical with incomplete information | Medium | Provide best available guidance; flag for follow-up review |
| Multiple stakeholder perspectives in conflict | Medium | Facilitate discussion; document all viewpoints |

## Tool Requirements

- `~~health/core` - Core health plugin functionality
- `~~health/clinical-systems` - EHR/EMR integration (if applicable)
- `~~cloud storage` - Document storage and collaboration
- `~~project tracker` - Workflow and task management
- `~~document collaboration` - Multi-stakeholder document editing
- `~~[domain-specific tool]` - [Description of specialized tool need]

## Success Indicators

You've applied this skill well when:
- [ ] All required documentation is complete and compliant
- [ ] Regulatory requirements are met and verified
- [ ] Output meets healthcare documentation standards
- [ ] Privacy and security protocols followed
- [ ] Appropriate stakeholders engaged and informed
- [ ] Audit trail is complete and accessible
- [ ] Escalation criteria assessed and acted upon appropriately
- [ ] Patient safety considerations addressed
- [ ] Output reviewed for clinical accuracy (if applicable)
- [ ] Related skills consulted when appropriate

## Related Skills

- `~~health/[related-skill-1]` - [Brief description of relationship and when to use together]
- `~~health/[related-skill-2]` - [Brief description of relationship and when to use together]
- `~~health/[related-skill-3]` - [Additional related skill if applicable]
- `~~[non-health-related-skill]` - [Cross-domain relationship if applicable]

---

## Template Usage Notes

When creating a new health skill from this template:

1. Replace all `{placeholders}` with domain-specific content
2. Ensure all 14 required sections are present (use "N/A" with explanation if truly not applicable)
3. Include at least 5 Common Mistakes
4. Include at least 3 Confidence Indicator scenarios
5. Include at least 2 Related Skills references
6. Include at least 3 Success Indicators
7. Verify AU/NZ-default jurisdiction matrix is complete
8. Verify US/EU-lite portability guidance is present
9. Ensure PHI/PII guardrails are appropriate for the domain
10. Confirm healthcare disclaimers are included
11. Validate minimum 300 lines total (health skills require more detail)
12. Remove these template usage notes before finalizing

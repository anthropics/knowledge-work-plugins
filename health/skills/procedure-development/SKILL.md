---
name: health/procedure-development
description: This skill should be used when documenting clinical or administrative procedures within a healthcare setting. Use when a user mentions step-by-step instructions, process mapping, procedure drafting, task checklists, or standard operating procedures (SOPs).
version: 1.0.0
---

# Procedure Development

Structured guidance for documenting step-by-step healthcare procedures to ensure consistency, clinical safety, and operational efficiency across organizational workflows.

**Important**: This skill assists with the documentation of procedures but does not provide clinical training or replace hands-on competency verification. All procedures must be validated by subject matter experts and comply with organizational policies and safety standards.

## When to Use This Skill

Invoke when:
- Creating a Standard Operating Procedure (SOP) for a specific clinical or administrative task.
- Documenting the steps required to implement an organizational policy.
- Mapping complex healthcare processes to identify efficiencies or safety gaps.
- Updating existing procedures based on equipment changes or feedback from frontline staff.
- Developing checklists or quick-start guides for high-volume or high-risk tasks.
- Ensuring that procedural documentation meets accreditation or regulatory requirements.

Do not use for organizational policies (use `~~health/policy-development`) or clinical evidence-based guidelines (use `~~health/guideline-development`).

## Regulatory Context

| Regulation | Relevance | Key Requirements |
|------------|-----------|------------------|
| **AU/NZ Baseline** | NSQHS Standard 1 (AU), Health & Disability Services Standard (NZ) | Procedures must be documented, accessible, and followed by staff to ensure safe and consistent care. |
| **US/EU-lite (optional)** | CMS Conditions of Participation (US), ISO 13485 (for devices) | Procedures must be clearly defined, version-controlled, and linked to relevant training and competency records. |

### Jurisdiction-Specific Triggers
- **Australia**: TGA requirements for device usage or state-based incident reporting protocols.
- **New Zealand**: Te Whatu Ora operational directives.

## Quick Reference

1.  **Define Scope**: What task is being documented and who is the intended user?
2.  **Gather Inputs**: Observe the task, review equipment manuals, and interview SMEs.
3.  **Map the Process**: Identify the logical flow from start to finish.
4.  **Identify Hazards**: Note specific safety risks (e.g., sharps, biohazards) at each step.
5.  **Draft Steps**: Use clear, concise language starting with action verbs.
6.  **Include Visuals**: Reference diagrams, photos, or screen captures where appropriate.
7.  **Validate**: Have frontline staff "dry run" the procedure to check for accuracy.
8.  **Approve & Publish**: Submit for department endorsement and upload to the repository.

## Detailed Guidance

### Procedure Documentation Format
Every healthcare procedure should follow a consistent format:
- **Title**: Action-oriented (e.g., "Performing a 12-Lead ECG").
- **Purpose**: Why this task is performed and what it achieves.
- **Scope/User**: Which staff roles are authorized to perform this procedure.
- **Equipment/Materials**: Comprehensive list of items required.
- **Safety Warnings**: Critical alerts (e.g., "Always wear PPE", "Verify patient ID").
- **Step-by-Step Instructions**: The core "how-to" content.
- **Post-Task Actions**: Documentation, waste disposal, and equipment cleaning.
- **Troubleshooting**: Common issues and how to resolve them.
- **Related Documents**: Links to policies, guidelines, and forms.

### Process Mapping Guidance
- **Start/End Points**: Clearly define when the procedure begins and ends.
- **Decision Points**: Use "IF... THEN..." logic for variations in the task.
- **Parallel Tasks**: Indicate steps that can or must be performed simultaneously.
- **Hand-offs**: Highlight where the task moves from one person/system to another.

### Writing Style for Procedures
- Use the **Imperative Mood** (e.g., "Wash hands", "Open package").
- Keep sentences short and focused on a single action.
- Use numbered lists for sequential steps and bullet points for unordered lists.
- Avoid ambiguous terms like "frequently" or "carefully"—specify "every 4 hours" or "using a slow, steady motion".

## Documentation Requirements

- [ ] **Procedure Draft**: Using the standard organizational template.
- [ ] **Equipment Manuals**: References to manufacturer instructions.
- [ ] **Competency Checklist**: A tool for assessing staff proficiency in the procedure.
- [ ] **Validation Record**: Evidence that the procedure was tested by users.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Too Much Background Info | Distracts the user from the actual steps. | Move "the why" to the Purpose or a separate Guideline. |
| Missing Patient ID Check | Leads to wrong-patient incidents. | Make "Verify Patient Identity" the first clinical step. |
| Using Outdated Terminology | Causes confusion and potential errors. | Align terms with current SNOMED-CT or organizational standards. |
| Over-complicating Simple Tasks | Discourages staff from using the document. | Use sub-procedures or "Fast Path" checklists for experienced users. |
| Neglecting Equipment Cleaning | Increases infection risk and equipment failure. | Include specific "Post-Task" cleaning and maintenance steps. |

## When to Escalate

Escalate to the Department Head or Clinical Lead when:
- Frontline staff report that a documented procedure is unsafe or impossible to follow.
- There is a conflict between manufacturer instructions and organizational policy.
- A procedure is linked to a significant adverse event or "near miss".
- Required equipment or supplies are consistently unavailable.

## Privacy Considerations

- **PHI involved**: No. Procedures should describe the task generically.
- **Data minimization**: Avoid using specific patient examples in procedure text.
- **Retention**: Procedures should be archived for 7-10 years after being superseded to support retrospective clinical reviews.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standardizing a routine administrative task | High | Propose final draft procedure. |
| Documenting a complex clinical skill (e.g., intubation) | Medium | Draft the framework and require SME clinical validation. |
| Procedure involves high-risk radiation or restricted chemicals | Low | REQUIRE review by specialized safety/radiation officers. |

## Standard and Lite Modes

- **Standard**: Full procedure documentation including process mapping and competency checklist development.
- **Lite**: Rapid creation of a "Task Checklist" or "Work Instruction" for a simple, low-risk activity.

## Tool Requirements

- `~~cloud storage` - For document repository.
- `~~process mapping tool` - (e.g., Visio, Lucid) for flowcharts.
- `~~project tracker` - To manage drafting and review tasks.

## Success Indicators

You've applied this skill well when:
- [ ] The procedure follows the action-oriented writing style.
- [ ] All required equipment and safety warnings are listed.
- [ ] The process flow is logical and has been validated by users.
- [ ] A corresponding competency checklist has been drafted.
- [ ] The document is mapped to the relevant organizational policy.

## Related Skills

- `~~health/policy-development` - The "what" that drives the procedure "how".
- `~~health/guideline-development` - The evidence base for the procedure.
- `~~health/incident-reporting` - To identify procedures requiring update post-incident.

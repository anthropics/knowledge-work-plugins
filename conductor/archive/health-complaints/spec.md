# Health Complaints Track Specification

## Overview

Patient complaints management workflows distinguishing between clinician complaints and service/organizational complaints.

## Scope

### Complaint Types

| Type | Focus | Examples |
|------|-------|----------|
| **Clinician** | Individual practitioner performance/conduct | Bedside manner, competence, communication |
| **Service/Organizational** | Systems, processes, facilities | Wait times, access, environment, administrative |

### Workflows

1. **Intake** - Categorization, severity assessment, routing
2. **Investigation** - Fact gathering, interviews, documentation
3. **Resolution** - Response drafting, remediation, closure
4. **Escalation** - When to escalate to legal, regulatory, or executive

### Key Distinctions from General Support

- Healthcare-specific severity (patient safety implications)
- Regulatory reporting obligations
- Clinical governance involvement
- Medical records access considerations

## Deliverables

### Skills
- `complaints-management` - Unified complaints workflow with type differentiation

### Commands
- `/submit-complaint` - Structured complaint intake

## Dependencies

- `health-core` (plugin structure must exist)

## Success Criteria

- [ ] Categorizes complaints by type (clinician vs service)
- [ ] Assesses severity with healthcare context
- [ ] Routes to appropriate investigation path
- [ ] Identifies regulatory reporting triggers
- [ ] Generates investigation documentation

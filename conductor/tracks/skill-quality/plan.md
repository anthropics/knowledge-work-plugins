# Health Skill Quality Track Plan

## Phase 1: Standards & Templates
*Estimated: 1 session*

- [x] Create health skill template
  - Acceptance: Template includes all 14 required sections with healthcare examples
  - Acceptance: AU/NZ-default jurisdiction matrix and US/EU-lite variant sections are mandatory
- [x] Write health skill style guide
  - Acceptance: Covers voice, tone, healthcare terminology, trigger-quality frontmatter, and disclaimer standards
- [x] Create health skill quality checklist
  - Acceptance: Checklist aligns with `health-plugin/skill-standards.md` quality gates
- [x] Build health skill validation script
  - Acceptance: Script checks required files, metadata consistency, dependencies, phase integrity, and AU/NZ plus US/EU-lite references
- [x] Document health skill creation process
  - Acceptance: Clear instructions for health track implementers

**Checkpoint:** `conductor(checkpoint): Health skill quality standards established`

## Phase 2: Skill Development Support
*Ongoing - supports all health track implementations*

### Complaints Skills (health-complaints track)
- [x] Provide template for complaint-analysis skill
- [x] Provide template for response-drafting skill

### Incident Skills (health-incidents track)
- [x] Provide template for root-cause-analysis skill
- [x] Provide template for cap-writing skill

### Risk Skills (health-risk track)
- [x] Provide template for clinical-risk skill
- [x] Provide template for worker-risk skill
- [x] Provide template for enterprise-risk skill

### Information Governance Skills (health-information track)
- [x] Provide template for release-of-information skill
- [x] Provide template for consent-management skill

### Coding Skills (health-coding track)
- [x] Provide template for clinical-coding skill

### Governance Skills (health-governance track)
- [x] Provide template for policy-development skill
- [x] Provide template for procedure-development skill
- [x] Provide template for guideline-development skill

### Credentialing Skills (health-credentialing track)
- [x] Provide template for credentialing skill
- [x] Provide template for privileging skill

### Procurement Skills (health-procurement track)
- [x] Provide template for device-procurement skill
- [x] Provide template for business-case skill

### Quality Skills (health-quality track)
- [x] Provide template for quality-improvement skill
- [x] Provide template for accreditation-prep skill

### Financial Skills (health-financial track)
- [x] Provide template for payer-contracts skill
- [x] Provide template for charge-capture skill

### Evidence Skills (health-evidence track)
- [x] Provide template for systematic-review skill
- [x] Provide template for evidence-synthesis skill

### Data Analysis Skills (health-data-analysis track)
- [x] Provide template for health-data-report skill

### Ethics Skills (health-ethics track)
- [x] Provide template for research-ethics skill
- [x] Provide template for clinical-ethics skill

### Economics Skills (health-economics track)
- [x] Provide template for health-econ-eval skill
- [x] Provide template for hta-submission skill

### Manuscript Skills (health-manuscripts track)
- [x] Provide template for manuscript-prep skill

### Public Health Skills (health-public-health track)
- [x] Provide template for notifiable-diseases skill
- [x] Provide template for public-health-surveillance skill

### Document Co-authoring Skills (health-doc-coauthoring track)
- [x] Provide template for clinical-doc-coauthoring skill

### Grants Skills (health-grants track)
- [x] Provide template for grant-writer skill

### Medicolegal Skills (health-medicolegal track)
- [x] Provide template for child-protection skill
- [x] Provide template for affidavits skill
- [x] Provide template for medicolegal-reports skill

**Checkpoint:** `conductor(checkpoint): All health skill templates provided`

## Notes

### Execution Strategy
- Provide templates proactively as each health track begins implementation
- Quality review skills as they are created, not retroactively
- Ensure cross-references between related health skills
- Validate regulatory context for each domain

### Template Distribution
- Store templates in health/skills/.templates/ directory
- Reference in each health tracks spec.md
- Update templates based on track implementer feedback

### Quality Verification
For each completed health skill:
1. Run validation script for required sections
2. Verify regulatory context is appropriate for domain
3. Check privacy considerations are complete
4. Confirm escalation criteria are realistic
5. Validate cross-references to related health skills

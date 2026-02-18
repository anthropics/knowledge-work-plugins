# Health Document Co-authoring Track Specification

## Overview

Three-stage collaborative document development workflow for healthcare documents requiring precision, regulatory compliance, and audience-awareness.

## Scope

### Document Types
- Clinical protocols
- Care pathways
- Clinical practice guidelines
- Health technology assessment (HTA) submissions
- NHMRC evidence summaries
- Position statements

### Three-Stage Workflow

**Stage 1: Context Gathering**
- Purpose and scope definition
- Target audience identification
- Regulatory requirements
- Evidence base assessment
- Stakeholder mapping

**Stage 2: Refinement**
- Draft development
- Clinical accuracy review
- Regulatory compliance check
- Citation and evidence grading
- Iterative stakeholder feedback

**Stage 3: Reader Testing**
- Target audience review
- Comprehension testing
- Implementation feasibility
- Accessibility review
- Final approval workflow

### Domain-Specific Guardrails
- Clinical claims require citations
- Regulatory language requirements (TGA, FDA, etc.)
- NHMRC evidence grading (A-D, Good Practice Points)
- Conflict of interest declarations

## Jurisdiction Defaults

- Default framing: Australia and New Zealand clinical and regulatory context.
- Include US/EU-lite variant guidance only when explicitly requested.

## Deliverables

### Skills
- `clinical-doc-coauthoring` - Full co-authoring workflow

### Commands
- `/coauthor` - Initiate collaborative document

## Dependencies

- `health-core` (plugin structure)
- `health-governance` (policy/guideline patterns)

## Adapts From

- `document-skills/docx` - Document handling
- General co-authoring patterns

## Success Criteria

- [ ] Guides three-stage workflow
- [ ] Enforces citation requirements for clinical claims
- [ ] Supports evidence grading
- [ ] Manages stakeholder review cycles
- [ ] Produces publication-ready documents

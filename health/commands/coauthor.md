---
name: coauthor
description: Initiate a collaborative clinical document co-authoring workflow
tools: ['Read', 'Write', 'Edit', 'bash', 'skill']
---

# /coauthor - Clinical Document Co-authoring Command

Initiate a three-stage collaborative workflow for developing clinical and regulatory documents requiring precision, evidence grading, stakeholder review, and formal approval.

## Usage

```
/coauthor [document-type] [--stage STAGE] [--mode MODE] [--title "TITLE"]
```

## Arguments

### Document Types

| Type | Description | Complexity |
|------|-------------|------------|
| `protocol` | Clinical protocol or procedure | Standard |
| `pathway` | Care pathway or patient journey | Standard |
| `guideline` | Clinical practice guideline | Intensive |
| `hta` | Health technology assessment submission | Intensive |
| `evidence-summary` | Evidence summary or rapid review | Standard |
| `position-statement` | Organizational position statement | Standard |
| `patient-info` | Patient information material | Standard |
| `policy` | Clinical or organizational policy | Standard |

### Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--stage` | `1`, `2`, `3`, `all` | `all` | Start at specific stage or run full workflow |
| `--mode` | `standard`, `lite` | `standard` | Operating mode (lite for rapid/internal docs) |
| `--title` | Any text | (prompts) | Document title |
| `--template` | Template name | (auto) | Specific template to use |

## Workflow Stages

### Stage 1: Context Gathering & Development
- Purpose and scope definition
- Target audience identification
- Regulatory requirements assessment
- Evidence base evaluation
- Stakeholder mapping
- Initial draft development

### Stage 2: Review & Refinement
- Clinical accuracy review
- Regulatory compliance check
- Evidence grading application (NHMRC/GRADE)
- Citation verification
- Iterative stakeholder feedback

### Stage 3: Reader Testing & Finalization
- Target audience comprehension testing
- Implementation feasibility assessment
- Accessibility and health literacy review
- Final approval workflow

## Examples

### Start a new clinical protocol
```
/coauthor protocol --title "Sepsis Recognition Protocol"
```

### Develop a clinical practice guideline (full workflow)
```
/coauthor guideline --title "Diabetes Management in Primary Care"
```

### Rapid development mode for internal document
```
/coauthor policy --mode lite --title "Social Media Use Policy"
```

### Continue from review stage
```
/coauthor hta --stage 2 --title "Assessment of Continuous Glucose Monitoring Systems"
```

## Process

When you run `/coauthor`, the system will:

1. **Load the clinical-doc-coauthoring skill** and initialize the workflow
2. **Prompt for document details** if not provided via arguments
3. **Generate a document checklist** specific to the document type and mode
4. **Guide through each stage** with structured prompts and validation
5. **Track progress** and maintain version control
6. **Manage stakeholder feedback** with structured review cycles
7. **Produce final document** ready for approval and publication

## Document Checklist

The following checklist will be generated based on document type:

### All Documents
- [ ] Purpose and scope clearly defined
- [ ] Target audience identified
- [ ] Regulatory requirements assessed
- [ ] Evidence base documented (if applicable)
- [ ] Stakeholders mapped and engaged
- [ ] Draft developed following template
- [ ] Clinical accuracy reviewed
- [ ] Citations verified and graded
- [ ] Conflict of interest declared
- [ ] Reader testing completed (Standard mode)
- [ ] Accessibility reviewed
- [ ] Version control maintained
- [ ] Approved by authorized signatory

### Protocol-Specific
- [ ] Clinical indications documented
- [ ] Contraindications identified
- [ ] Step-by-step procedure defined
- [ ] Monitoring parameters specified
- [ ] Quality indicators established

### Guideline-Specific
- [ ] Systematic evidence search conducted
- [ ] NHMRC/GRADE evidence grading applied
- [ ] Recommendations numbered and graded
- [ ] Implementation barriers assessed
- [ ] Review schedule established

### HTA-Specific
- [ ] Clinical effectiveness evidence compiled
- [ ] Economic evaluation completed
- [ ] Budget impact analysis performed
- [ ] Uncertainty analysis conducted
- [ ] Post-market surveillance plan included

## Evidence Grading Requirements

All clinical claims must include:
- **NHMRC Level**: I, II, III-1, III-2, III-3, IV, or GPP
- **GRADE Quality**: High (⊕⊕⊕⊕), Moderate (⊕⊕⊕○), Low (⊕⊕○○), Very Low (⊕○○○)
- **Citation**: Full Vancouver-style reference with DOI

## Jurisdiction Defaults

**Default**: Australia/New Zealand
- NHMRC evidence grading standards
- TGA regulatory requirements
- NSQHS clinical governance standards
- State/Territory health department requirements

**US/EU-lite** (when explicitly requested):
- GRADE methodology
- FDA/EMA regulatory frameworks
- IOM guideline standards

## Outputs

The co-authoring workflow produces:

1. **Draft Document** - Structured document following type-specific template
2. **Evidence Tables** - Graded evidence summaries with citations
3. **Stakeholder Feedback Log** - Structured review responses and decisions
4. **Version History** - Complete change log with attributions
5. **Approval Package** - Sign-off documentation and compliance verification
6. **Implementation Tools** - Quick reference guides, checklists, and forms (as applicable)

## Getting Started

To begin a new clinical document co-authoring project:

1. Choose the appropriate document type
2. Decide on Standard or Lite mode
3. Prepare preliminary information:
   - Document purpose and objectives
   - Target audience description
   - Available evidence sources
   - Key stakeholders to engage
4. Run `/coauthor` with your chosen parameters
5. Follow the guided workflow prompts
6. Complete all checklist items for your document type

For detailed guidance on each stage, refer to the `~~health/clinical-doc-coauthoring` skill documentation.

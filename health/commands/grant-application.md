---
description: Initiate a grant application for health research funding. Guides funder selection, scheme selection, and generates an application checklist.
---

# /grant-application

Start a new grant application for health research funding. This command guides you through selecting the appropriate funder and scheme, then generates a tailored application checklist.

## Usage

```
/grant-application [funder] [scheme]
```

## Arguments

- **funder** (optional): Target funding body
  - `nhmrc` - National Health and Medical Research Council (Australia)
  - `mrff` - Medical Research Future Fund (Australia)
  - `hrc` - Health Research Council (New Zealand)
  - `arc` - Australian Research Council (health-related Discovery Projects)
  - `nih` - National Institutes of Health (US)
  - `help` - Show funder selection guidance

- **scheme** (optional): Specific grant scheme (depends on funder)
  - For NHMRC: `ideas`, `investigator`, `synergy`, `fellowship`
  - For MRFF: `large`, `emcr`, `consumer`, `specific`
  - For HRC: `explorer`, `project`, `programme`, `fellowship`
  - For ARC: `dp` (Discovery Projects), `linkage`
  - For NIH: `r01`, `r21`, `k`, `f`

## Examples

```
/grant-application nhmrc ideas
/grant-application mrff large
/grant-application hrc explorer
/grant-application help
```

## Workflow

1. **Funder Selection**: If not specified, you'll be prompted to select a funding body based on research type, career stage, and location.

2. **Scheme Selection**: Choose the appropriate scheme within the selected funder based on project scope, budget needs, and eligibility.

3. **Checklist Generation**: Creates a tailored application checklist with:
   - Required documents and templates
   - Key deadlines and milestones
   - Compliance requirements (ethics, governance)
   - Section-specific word/page limits
   - Assessment criteria alignment points
   - Budget justification requirements

4. **Skill Activation**: Automatically invokes the `grant-writer` skill for detailed guidance.

## Funder Selection Guidance

### Australia

**NHMRC** - Best for:
- Investigator-led discovery research
- Health and medical research excellence
- ECR to senior researcher career stages
- Projects with strong scientific merit

**MRFF** - Best for:
- Mission-driven, translational research
- Consumer/patient involvement
- Industry and end-user collaboration
- Translation to clinical practice or policy

**ARC** - Best for:
- Basic research with health applications
- Non-clinical research questions
- Interdisciplinary approaches

### New Zealand

**HRC** - Best for:
- All health research funding in NZ
- Māori health research and advancement
- Researcher development at all career stages

### International

**NIH** - Best for:
- US-based researchers or US collaborations
- Large-scale clinical and translational research
- Extensive research infrastructure support

## Output

The command generates:
1. Funder/scheme selection confirmation
2. Application checklist document
3. Timeline with key milestones
4. Links to relevant funder resources
5. Access to grant-writer skill guidance

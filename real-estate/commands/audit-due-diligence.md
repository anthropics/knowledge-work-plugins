---
name: audit-due-diligence
alias:
  - check-lim
  - title-audit
description: Scrutinize LIM reports, Titles, and Building Reports for red flags and disclosure requirements.
arguments:
  - name: report_text
    description: "Raw text or highlights from a LIM, Title, or Builder's report."
    required: true
  - name: property_type
    description: "Type (e.g., Freehold, Cross-lease, Unit Title)."
    required: false
---

# /audit-due-diligence Command

Identify risks early and prepare mandatory disclosures.

## When to Use

Use this command when:
- You receive a fresh LIM from the Council and need to find the "hidden" red flags.
- You're reviewing a Record of Title for restrictive covenants.
- You need to draft a "Mandatory Disclosure" based on a Builder's Report.
- A buyer asks for a summary of the property's risks.

## Workflow

### 1. Scrutinize & Flag

Use `~~real-estate/property-analyst` to:
- Detect "Unauthorized Works" (e.g., bathrooms with no CCC).
- Identify "Land Risks" (e.g., HCC flood plains, wind zones).
- Highlight "Title Complexities" (e.g., cross-lease common areas).

### 2. Formulate Disclosures

Produce:
- **Red Flag Log**: High-priority issues that could crash a sale.
- **REA Disclosure Draft**: Professional wording for the "Disclosure Form."
- **Buyer Guide Snippet**: Transparent explanation of risks for purchasers.

## Example Session

**User:** `/audit-due-diligence report_text: "Title: Heritage listing Grade 2. LIM: Surface flooding noted in 2016 event. Builder: Moisture reading of 22% in master ensuite." property_type: "Freehold"`

**System:**
```
[~] AUDITING DUE DILIGENCE...
[~] SCANNING REA CODE COMPLIANCE...

DUE DILIGENCE AUDIT READY:

1. Critical Red Flag: Moisture level (22%) indicates an active leak in the ensuite. This is a material latent defect.
2. Council Flag: The 2016 surface flooding record requires a 'Flood Risk' disclosure under HCC maps.
3. Title Flag: Grade 2 Heritage listing restricts future external renovations.

REQUIRED ACTION:
- Draft REA Disclosure: "The vendor discloses that a 2026 builder's report identified elevated moisture levels in the ensuite. Prospective buyers are encouraged to seek their own technical advice."

Would you like to draft the 'Disclosure Authorization' for the vendor to sign? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/property-analyst`.
- **Downstream**: Feeds into `/check-compliance`.

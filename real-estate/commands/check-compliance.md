---
name: check-compliance
alias:
  - rea-check
  - aml-audit
description: Perform a compliance audit of a listing, contract, or client entity against REA Code and AML/CDD regulations.
arguments:
  - name: document
    description: "The listing text, contract draft, or client entity details (e.g., 'Trust' or 'Company')."
    required: true
  - name: check_type
    description: "Specific focus (e.g., 'REA Code Rule 6.4' or 'AML for Family Trust')."
    required: false
---

# /check-compliance Command

Ensure your files are "Audit-Ready" and compliant with NZ statutory requirements.

## When to Use

Use this command when:
- Performing a final check of a Trade Me listing before it goes live.
- You're about to sign a new vendor and need an AML documentation checklist.
- You want to verify if a specific clause in a contract violates REA ethics.
- Auditing a complex entity (e.g., offshore company) for CDD requirements.

## Workflow

### 1. Scrutinize & Verify

Use `~~real-estate/compliance-closer` to:
- Cross-check `document` against REA Code rules (misleading conduct, disclosures).
- Generate a customized `AML Checklist` for the specific entity type.
- Identify "Conflict of Interest" triggers.

### 2. Generate Compliance Report

Produce:
- **Compliance Status**: Pass/Fail with "Fix Needed" flags.
- **Missing Items Log**: List of IDs or Deeds still required for the file.
- **REA Risk Note**: Specific wording to mitigate misleading conduct risks.

## Example Session

**User:** `/check-compliance document: "Vendor is a Family Trust with 3 trustees, one lives in UK." check_type: "AML"`

**System:**
```
[~] AUDITING ENTITY STRUCTURE...
[~] CHECKING AML/CDD REQUIREMENTS...

COMPLIANCE AUDIT READY:

1. Entity Type: Family Trust (High-Medium Risk due to UK Trustee).
2. Required for File:
   - Full Copy of Trust Deed (including all variations).
   - Photo ID & Proof of Address for all 3 Trustees.
   - Verification of 'Source of Wealth' (since UK Trustee is involved).
3. Risk Note: Ensure 'Form 1' (Conflict of Interest) is checked if any trustee has a relationship with the agency.

Would you like to draft the 'AML Information Request' email for the trustees? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/compliance-closer`.
- **Downstream**: Feeds into `/prepare-negotiation`.

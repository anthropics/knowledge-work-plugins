---
name: generate-appraisal
alias:
  - appraisal
  - market-value
description: Generate a data-driven market appraisal, comparative sales table, and investment yield analysis for a NZ property.
arguments:
  - name: property_details
    description: "Address, bed/bath/car count, floor area, and land size."
    required: true
  - name: comparables
    description: "List of 3 recent local sales (manual entry or raw data)."
    required: true
  - name: cycle
    description: "Current market cycle (Rising, Falling, Flat)."
    required: false
---

# /generate-appraisal Command

Justify your pricing recommendations with an Evidence-based Appraisal Pack.

## When to Use

Use this command when:
- Preparing a listing presentation for a potential vendor.
- An investor asks for a yield and cashflow analysis.
- You need to justify a "Price Revision" using recent market evidence.
- A buyer asks for evidence to support their offer price.

## Workflow

### 1. Analyze & Index

Use `~~real-estate/property-analyst` to:
- Compare the `property_details` against the `comparables`.
- Adjust for the `cycle` (indexing old sales to today's market).
- Calculate Rental Yield and local HCC rates impact.

### 2. Synthesize Evidence

Produce:
- **Appraisal Evidence Pack**: The "Feature vs Feature" comparison table.
- **Investment Brief**: Gross/Net Yield and Capital Growth outlook.
- **Price Range Recommendation**: Supported by data-driven rationale.

## Example Session

**User:** `/generate-appraisal property_details: "123 Petone St, 3 bed, 1 bath, 100sqm, 400sqm land" comparables: "15 Petone St ($1.1m), 22 Maungaraki Rd ($1.05m), 10 Beach St ($1.2m)" cycle: "Falling"`

**System:**
```
[~] CALCULATING COMPARATIVE VALUE...
[~] INDEXING FOR FALLING MARKET...

APPRAISAL EVIDENCE PACK READY:

1. Feature Comparison Table:
   - Subject (123 Petone): 3 Bed | 1 Bath | 100sqm | 400sqm Land
   - vs 10 Beach St (Superior): +$100k for second bathroom and beachfront access.
   - vs 15 Petone St (Direct): -$20k for lack of internal garaging.

2. Investment Yield:
   - Estimated Rent: $750pw
   - Gross Yield: 3.4% (Based on $1.15m mid-point)

3. Recommended Range: $1.12m - $1.18m (BEO $1.1m)
   - Rationale: The 10% premium for Petone St location remains stable despite the 5% market-wide correction.

Would you like to draft the 'Appraisal Justification' letter for the vendor? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/property-analyst`.
- **Upstream**: Feeds into `/draft-listing` copy.
- **Downstream**: Feeds into `/prepare-negotiation`.

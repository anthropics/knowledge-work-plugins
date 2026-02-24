---
name: real-estate/property-analyst
description: This skill should be used when conducting market appraisals, analyzing property investments, and auditing due diligence documents for New Zealand real estate. Use for generating "Appraisal Evidence Packs," calculating rental yields, flagging risks in LIMs/Titles, and assessing school zone stability. Invoke when users mention market value, comparable sales, LIM reports, rental ROI, or school zones.
version: 1.0.0
---

# Property Analyst (The Evidence Specialist)

A rigorous framework for data-driven property valuation and risk assessment. This skill provides the "Evidence Pack" to justify pricing, calculates financial returns for investors, and scrutinizes statutory documents (LIM, Title) for red flags.

**Important**: This skill provides market appraisals and risk analysis but does not replace a Registered Valuation, formal legal advice from a solicitor, or a building inspection report. All school zone information should be verified with the Ministry of Education.

## When to Use This Skill

Invoke this skill when:
- Generating a market appraisal for a potential listing.
- Preparing an "Appraisal Evidence Pack" comparing features of local sales.
- Calculating Gross/Net Rental Yield and cashflow potential for investors.
- Auditing a Land Information Memorandum (LIM) or Record of Title for red flags.
- Assessing the "Market Cycle" (Boom/Flat/Correction) to adjust pricing strategy.
- Identifying "School Zone Future Proofing" risks (e.g., border zone properties).
- Adjusting appraisals based on "Qualitative Vibe" (e.g., stunning views vs. poor flow).
- Drafting "Buyer Guides" for first-home buyers or local area newcomers.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **REA Code of Conduct** | Appraisal accuracy | Rule 10.6: Appraisals must be supported by comparable data |
| **Local Government Act** | LIM reports | Defining HCC/WCC disclosure requirements for unauthorized works |
| **Land Transfer Act** | Titles | Identifying easements, encumbrances, and land covenants |
| **Income Tax Act (NZ)** | Investment ROI | Understanding "Bright-line" and interest deductibility (high-level) |

### AU/NZ Baseline Specifics
- **LIM Reports**: Understanding the "Hutt City Council" (HCC) baseline for building consents and permits.
- **Comparable Sales**: Requirement for minimum 3 recent, relevant local sales.
- **School Zones**: Analyzing Hutt Valley High, Petone Central, and Waterloo zone boundaries.

## Quick Reference

1. **Set the Cycle**: Identify if the market is Rising, Falling, or Flat.
2. **Select Comparables**: Find 3 recent sales with similar floor area, garaging, and land size.
3. **Justify the Price**: Generate a "Feature Comparison Table" between subject and comparables.
4. **Scrutinize the LIM**: Check for "Unauthorized Works" or "Flood Zone" flags.
5. **Yield Check**: (For investors) Calculate Gross Yield = (Weekly Rent * 52) / Purchase Price.
6. **Vibe Adjustment**: Apply +/- 5% for qualitative factors (e.g., street appeal).
7. **Zone Check**: Flag border properties for potential rezoning risks.

## Operating Modes

### Standard Mode
Full analytical workflow including detailed comparable tables, multi-source due diligence audit (LIM/Title), investment ROI modeling, and school zone risk analysis. Use for formal appraisals and high-stakes buyer/vendor consultations.

### Lite Mode
Rapid calculation of rental yield, quick "LIM Red Flag" check, or a simple 3-sale comparable list. Optimized for high-speed market conversations.

## Detailed Guidance

### 1. The Appraisal "Evidence" Pack

Justify the price to the vendor or buyer:
- **Subject vs. Sales**: Direct comparison of Bed/Bath/Car/Land/Floor Area.
- **Location Premium**: Adjusting for "River side" vs. "Hills side" or specific quiet cul-de-sacs.
- **Time Adjustment**: Indexing a 6-month-old sale to today's "Market Cycle."

### 2. Due Diligence Scrutiny (Red Flags)

Identify risks before they kill the deal:
- **LIM Flags**: Unauthorized bathroom/deck, "Wind Zone" rating, flood plains (HCC maps).
- **Title Flags**: Easements for neighbor access, "Cross-lease" complexities, restrictive covenants (e.g., no caravans).
- **Building Report Flags**: Weathertightness (monolithic cladding), piling issues, asbestos ceiling.

### 3. Investment Yield Calculator

Speak the language of the investor:
- **Gross Yield**: Standard benchmark for market comparison.
- **Net Yield**: Accounting for Rates (HCC is ~0.5% of value), Insurance, and Maintenance.
- **Capital Growth Context**: Mentioning major local infra projects (e.g., Melling Link) impacting future value.

### 4. Market Cycle Adjuster

Tailor strategy to the economic environment:
- **Rising (Boom)**: Aggressive "Tender" or "Auction" strategy; focus copy on "Scarcity."
- **Falling (Correction)**: "Price on Application" or "By Negotiation"; focus copy on "Value" and "Stability."
- **Flat**: "BEO" (Buyer Enquiry Over); focus copy on "Quality" and "Perfect Family Home."

### 5. School Zone Future Proofing

Verify the "Golden Ticket":
- **Core Zone**: Properties well within the boundary (Waterloo/Petone).
- **Border Zone**: Flag as "High Risk" if the Ministry of Education has signaled overcrowding in that zone.
- **Amenity Value**: Quantify the "Zone Premium" (typically 10-15% in Lower Hutt).

## Documentation Requirements

- [ ] **Appraisal Evidence Pack**: Comparative table and pricing rationale.
- [ ] **Investment Brief**: ROI/Yield summary for the property.
- [ ] **Due Diligence Log**: Red flags identified in LIM/Title/Building reports.
- [ ] **Buyer Guide Snippet**: Suburb expert highlights for the local area.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Cherry-picking Sales** | Misleads the vendor; violates REA code | Include at least one "low" or "challenging" sale for balance. |
| **Ignoring Unauthorized Works** | Contract crashes during buyer's finance | Flag early and prepare a "Disclosure" for the vendor to sign. |
| **Static Pricing in Falling Market** | Listing goes stale | Recommend a price revision *before* the 21-day mark. |
| **Assuming Yield = Profit** | Ignores HCC rates and interest costs | Explicitly state the difference between Gross and Net yield. |

## When to Escalate

Escalate to Branch Principal or Registered Valuer when:
- The property is unique (e.g., commercial/residential mix) and lacks comparable data.
- The Title has complex "Consent Notices" or "Encumbrances" that require legal interpretation.
- A vendor demands an appraisal value >20% above recent comparable sales.
- The property has significant structural defects identified in a builder's report.

## Privacy Considerations

- **Data Minimization**: Do not retain copies of identifiable LIM reports beyond the campaign period.
- **Confidentiality**: Appraisal values are sensitive to the vendor; do not disclose to third parties without consent.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Property matches 3 recent sales in the same street | High | Finalize Appraisal Evidence Pack. |
| Border-zone property with conflicting school info | Medium | Flag as "Risk" and require MOE verification. |
| Monolithic cladding with no "Code Compliance Certificate" | Low | Recommend immediate escalation to Registered Valuer/Solicitor. |

## Tool Requirements

- `~~budget data` - For calculating HCC rates and insurance estimates.
- `~~legislation` - For checking REA compliance and Land Transfer Act rules.
- `~~property database` - (Optional) Integration with sales data APIs.

## Success Indicators

You've applied this skill well when:
- [ ] Appraisal justification is so clear that vendors accept the recommended price range.
- [ ] LIM/Title issues are identified and disclosed *before* the property goes to market.
- [ ] Investor buyers receive accurate yield models that match their bank's criteria.
- [ ] Buyers feel confident in their purchase due to the detailed Suburb/School info.

## Related Skills

- `~~real-estate/marketing-suite` - For translating appraisal data into ad copy.
- `~~real-estate/lead-management` - For providing data to "Hot Leads."
- `~~real-estate/compliance-closer` - For ensuring the final price meets REA standards.

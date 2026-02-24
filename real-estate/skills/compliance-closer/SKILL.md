---
name: real-estate/compliance-closer
description: This skill should be used when managing legal compliance (REA/AML), coordinating property negotiations, and finalizing settlement documentation for New Zealand real estate. Use for auditing contracts against the REA Code, drafting "Method of Sale" strategies (Auction, Tender), generating multi-offer responses, and ensuring AML/CDD completeness. Invoke when users mention multi-offer situation, auction strategy, REA compliance, or AML checks.
version: 1.0.0
---

# Compliance Closer (The Deal Manager)

A rigorous framework for navigating the legal and strategic hurdles of a property transaction. This skill ensures the agent remains compliant with the REA Code of Conduct and AML/CDD regulations while maximizing the outcome for the vendor through specialized negotiation tactics.

**Important**: This skill assists with compliance and strategy but does not replace formal legal advice from a solicitor or independent legal counsel. All AML/CDD verification must be completed according to the agency's formal internal policy.

## When to Use This Skill

Invoke this skill when:
- Auditing a Sale and Purchase Agreement against the REA Code of Conduct.
- Designing a "Method of Sale" strategy (Auction, Tender, Deadline, Price).
- Navigating a "Multi-Offer" situation and drafting vendor responses.
- Ensuring AML/CDD (Anti-Money Laundering) documentation is complete for complex entities (e.g., Trusts, Companies).
- Drafting counter-offer wording for complex contract clauses (e.g., "Subject to Finance," "Solicitor's Approval").
- Preparing an Auctioneer or Lead Agent with an "Opening Statement" for an auction.
- Performing a final "Pre-Go-Live" compliance audit of a listing.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **REA Act 2008 (NZ)** | Professional standards | Statutory requirement for agent licensing and conduct |
| **REA Code of Conduct** | Transaction ethics | Rule 10.1: Client care; Rule 10.10: Disclosure of conflict |
| **AML/CFT Act (NZ)** | Identity verification | Verifying "Source of Funds" and "Beneficial Ownership" |
| **ADLS/REINZ S&P** | Contract standard | The standard form for property sales in New Zealand |

### AU/NZ Baseline Specifics
- **Multi-Offer Rules**: Strict adherence to the agency's "Multi-offer Process" (Rule 6.2).
- **Auction Rules**: Ensuring the "Auction Conditions" are clearly displayed and verbalized.
- **AML Checks**: Specific requirements for NZ Family Trusts and Look-through Companies (LTCs).

## Quick Reference

1. **Audit AML**: Verify ID and Proof of Address for all "Significant Control" persons.
2. **Strategy Selection**: Choose Auction (Scarcity), Tender (Privacy/Control), or Price (Transparency).
3. **Multi-Offer Flow**: Ensure all buyers sign the "Acknowledgement of Multi-offer" form.
4. **Counter the Offer**: Use professional wording to pivot on Price, Possession, or Conditions.
5. **Auction Opener**: Focus on local amenities and the property's unique "emotional hooks."
6. **Code Audit**: Perform final 10-point check of the listing against REA Rule 6.4.

## Operating Modes

### Standard Mode
Full compliance and closing workflow including deep AML/CDD verification for complex entities, comprehensive multi-offer strategy generation, detailed auction prep, and formal contract auditing. Use for all live negotiations and contract signing.

### Lite Mode
Rapid generation of an auction opening statement, quick "Multi-offer script" for buyers, or a 3-point AML checklist for an individual. Optimized for high-speed transaction updates.

## Detailed Guidance

### 1. REA/AML Audit Logic

Ensure the file is "Audit-Ready":
- **Individual**: Photo ID + Proof of Address (<3 months old).
- **Trust**: Copy of Trust Deed + ID for all Trustees + ID for all Settlors.
- **Company**: Verification of all shareholders with >25% ownership.
- **Conflict of Interest**: Has the agent disclosed if they are related to the buyer or have a financial interest? (REA Form 1).

### 2. Method of Sale Strategies

Tailor the approach to market conditions:
- **Auction**: Best for "High Demand/Low Supply." Forces buyers to act on an unconditional basis.
- **Tender**: Best for "Unique/Premium" properties. Allows the vendor to compare "apples vs. oranges" (e.g., price vs. longer settlement).
- **Deadline Sale**: Best for "Test the Market." Similar to tender but with more flexibility to sell early.
- **BEO (Buyer Enquiry Over)**: Best for "Price Transparency." Good for high-volume family homes.

### 3. Multi-Offer Strategy Generator

Navigate the most high-pressure part of the job:
- **The Protocol**: Verify all buyers have been given the same deadline and opportunity.
- **The Scoring**: Compare offers on Price, Deposit, Conditions, and Possession date.
- **The "Best & Final" Script**: "We have multiple interest; please put your best foot forward as there may not be a second chance."

### 4. Auction/Tender "Opening Statements"

Set the energy for the sale:
- **The Hook**: "Moments from the Petone beachfront, where heritage meets modern luxury..."
- **The Value**: "A rare freehold 400sqm site in a suburb with 8% annual growth."
- **The Call**: "Who will start me today? The opportunity is yours."

## Documentation Requirements

- [ ] **AML/CDD Checklist**: Verification log for all involved parties.
- [ ] **Multi-Offer Summary**: Comparative table of all received offers.
- [ ] **Contract Audit Log**: Record of REA Code compliance for the listing.
- [ ] **Auction/Tender Strategy**: One-page plan for the method of sale.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Vague Multi-offer Info** | Buyers feel "played"; risk of REA complaint | Be crystal clear about the deadline and the process. |
| **Accepting Old AML ID** | Statutory violation; heavy agency fines | Always require ID less than 3 months old or a current Passport. |
| **Misleading "BEO" Price** | "Under-quoting" leads to buyer grievance | Ensure BEO price is realistic based on recent comparables. |
| **Ignoring Chattels list** | Settlement day disputes over mirrors/shelves | Itemize every non-fixed item in the S&P agreement. |

## When to Escalate

Escalate to Branch Manager or Compliance Officer when:
- A buyer or vendor is identified as a "PEP" (Politically Exposed Person).
- There is suspicion of "Source of Wealth" being illegitimate.
- A multi-offer situation involves a "Conflict of Interest" with an internal staff member.
- A party refuses to sign the mandatory REA disclosure forms.

## Privacy Considerations

- **Confidentiality**: Multi-offer details (price/terms) must NEVER be shared between buyers.
- **Security**: AML documentation contains highly sensitive PII; store only in encrypted agency systems.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Standard ADLS contract with individual buyers (clean AML) | High | Finalize Multi-offer Summary and proceed to signing. |
| Complex offshore Trust structure requiring CDD | Medium | Request all deeds and escalate to agency Compliance Officer. |
| Dispute over "Verbally accepted" offer vs. written contract | Low | HALT and recommend both parties seek immediate legal advice. |

## Tool Requirements

- `~~legislation` - For real-time checking of REA and AML statutory updates.
- `~~cloud storage` - For secure storage of encrypted AML/CDD logs.
- `~~document collaboration` - For multi-party contract review.

## Success Indicators

You've applied this skill well when:
- [ ] The Multi-offer process is so transparent that even the "losing" buyers feel treated fairly.
- [ ] AML/CDD files pass an internal or external audit with zero "Exceptions."
- [ ] The "Method of Sale" strategy results in a sale within the campaign timeframe.
- [ ] Contract conditions are "tight" and clear, leading to a smooth unconditional date.

## Related Skills

- `~~real-estate/marketing-suite` - For ensuring the Auction energy matches the ad copy.
- `~~real-estate/property-analyst` - For ensuring the multi-offer prices align with market evidence.
- `~~real-estate/lead-management` - For the final "Key Handover" after the deal is closed.

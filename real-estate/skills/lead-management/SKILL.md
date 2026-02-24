---
name: real-estate/lead-management
description: This skill should be used when managing leads, open home feedback, and post-sale settlement for New Zealand real estate. Use for interpreting NurtureCloud data, ranking "Hot Leads," synthesizing weekly vendor reports, generating referral briefs for Loan Market/Concierge, and preparing settlement handover checklists. Invoke when users mention prospecting, open home feedback, vendor updates, or settlement prep.
version: 1.0.0
---

# Lead Management (The Prospector & Closer)

A comprehensive framework for maximizing lead conversion and ensuring a professional "end-to-end" client experience. This skill focuses on the Ray White NurtureCloud baseline, transforming raw feedback into strategic vendor advice and ranking buyers by conversion probability.

**Important**: This skill assists with lead prioritization and communication but does not replace CRM data entry or the agent's relationship-building role. All "Conversion Probability" rankings are estimates based on provided buyer profiles.

## When to Use This Skill

Invoke this skill when:
- Interpreting NurtureCloud prospecting reports to prioritize daily calls.
- Ranking open home visitors ("Hot Lead Detector") by conversion probability.
- Synthesizing raw open-home notes into a professional "Weekly Vendor Report."
- Drafting personalized follow-up emails or SMS based on buyer preferences.
- Generating "Rainy Day Pivot" strategies for upcoming open homes.
- Drafting "Client Referral Briefs" for Loan Market (Mortgages) or Concierge.
- Preparing "Final Inspection & Key Handover" checklists for settlement.
- Auto-tagging database contacts by "Life Stage" (The Golden Database).

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **Privacy Act 2020 (NZ)** | Lead data | Protecting buyer/vendor contact info; purpose-limited data usage |
| **REA Code of Conduct** | Communication | Rule 11.2: Keeping the client informed; Rule 6.3: Professionalism |
| **Unsolicited Electronic Messages Act** | SMS/Email marketing | Ensuring "Unsubscribe" options and valid consent for marketing |

### AU/NZ Baseline Specifics
- **NurtureCloud**: Alignment with Ray White's proprietary CRM and prospecting logic.
- **Vendor Reporting**: Meeting the expectation for weekly, data-driven campaign updates.

## Quick Reference

1. **Tag the Database**: Categorize leads by "Life Stage" (e.g., First Home Buyer, Empty Nester).
2. **Rank the Leads**: Identify "Hot Leads" from open home lists based on buying readiness.
3. **Weekly Synthesis**: Distill vendor feedback into Market Sentiment, Pricing Trends, and Next Steps.
4. **Refer Professionals**: Create professional handoff briefs for brokers and movers.
5. **Weather Proof**: Apply "Rainy Day" strategies to maintain open home energy.
6. **Handover Ready**: Generate the final settlement checklist 48 hours before possession.

## Operating Modes

### Standard Mode
Full lead management lifecycle including deep database segmentation, complex visitor ranking, full-length vendor reports, and detailed settlement management. Use for high-volume campaigns and active listings.

### Lite Mode
Rapid generation of follow-up SMS, quick "Top 3 Leads" identification from a single open home, or a simple settlement reminder list. Optimized for high-speed prospecting sessions.

## Detailed Guidance

### 1. The "Golden Database" Tagger (Life Stage)

Move beyond "Buyer/Seller." Tag contacts to enable targeted long-term marketing:
- **First-Home Buyer**: Focused on Petone/Wainui, needs Loan Market referral.
- **Growing Family**: Looking for 4+ beds in Waterloo/Maungaraki zones.
- **Empty Nester**: Looking to downsize to modern low-maintenance units.
- **Active Investor**: Focused on yield, ROI, and school zone stability.

### 2. Hot Lead Detector (Open Home Ranking)

Rank visitors (1-5 stars) based on these "Hot" triggers:
- **5 Stars**: Finance pre-approved, has sold their own home, wants a contract today.
- **4 Stars**: Finance pre-approved, needs to sell, highly engaged with specific features.
- **3 Stars**: Just starting search, finance not yet certain, but active in the suburb.
- **2 Stars**: "Tyre kickers" or curious neighbors.

### 3. Weekly Vendor Report Synthesis

Structure reports to manage vendor expectations:
- **The Numbers**: Attendance, Trade Me views, contracts requested.
- **The Sentiment**: "Great kitchen," "Small backyard," "Price feels high for the condition."
- **The Pivot**: Suggested strategy changes based on feedback (e.g., "Change the main photo to the garden").

### 4. Rainy Day Pivot Strategy

When the Hutt Valley weather is poor:
- **The Vibe**: All lights on, fireplace/heat pump to 22°C, background music louder.
- **The Welcome**: Umbrellas at the gate, shoe covers provided, "Hot Coffee" signage.
- **The Hook**: Focus copy on "Cosy heritage charm" and "Indoor-outdoor flow for when the sun returns."

## Documentation Requirements

- [ ] **Hot Lead List**: Priority call list with 3 talking points per lead.
- [ ] **Weekly Vendor Report**: Professional PDF-ready synthesis.
- [ ] **Referral Brief**: One-page handoff for Loan Market/Concierge.
- [ ] **Key Handover Checklist**: Final inspection verification for both parties.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Ignoring the "Nos"** | Vendors only hear the good news; price shock later | Include critical feedback about price or condition in every report. |
| **Generic SMS Follow-ups** | Buyers feel like a number | Mention a specific feature they liked (e.g., "the sun-drenched deck"). |
| **Missing the Referral** | Loss of agency revenue and client value | Check "Needs Finance" status for every 4-5 star buyer lead. |
| **Settlement Surprises** | Ruins the referral potential | Ensure alarm codes and garage remotes are verified 24 hours prior. |

## When to Escalate

Escalate to Branch Manager when:
- A "Hot Lead" makes a complaint about agent conduct or disclosure.
- A vendor refuses to accept consistent market feedback regarding price.
- A settlement dispute arises regarding "Vacant Possession" or chattels.
- Lead data appears to have been leaked or misused (Privacy Breach).

## Privacy Considerations

- **Data Minimization**: Do not share full buyer contact lists with vendors (sentiment only).
- **Consent**: Ensure Loan Market referrals are explicitly authorized by the client.
- **Security**: NurtureCloud access should remain restricted to authorized staff.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Structured visitor feedback from 3 open homes | High | Generate full Weekly Vendor Report and Hot Lead Ranking. |
| Vague NurtureCloud notes with no "Next Action" | Medium | Clean dictation and suggest 3 possible follow-up scripts. |
| Complex multi-party settlement dispute | Low | Escalate to Principal and recommend legal counsel intervention. |

## Tool Requirements

- `~~cloud storage` - For archiving vendor reports and settlement logs.
- `~~project tracker` - For managing settlement milestones.
- `~~contact database` - (Optional) Integration with NurtureCloud via MCP.

## Success Indicators

You've applied this skill well when:
- [ ] The "Hot Lead" list results in at least 2 contracts within 48 hours.
- [ ] Vendor feedback is realistic and professional, leading to timely price adjustments.
- [ ] Referral rates to Loan Market/Concierge increase by >10%.
- [ ] Settlement day is "surprise-free" for both vendor and buyer.

## Related Skills

- `~~real-estate/marketing-suite` - For the "Rainy Day" copy adjustments.
- `~~real-estate/property-analyst` - For data to back up vendor reports.
- `~~real-estate/compliance-closer` - For the REA audit of the final contract.

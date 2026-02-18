---
name: real-estate/marketing-suite
description: This skill should be used when preparing property listings, marketing materials, and vendor pre-listing advice for the New Zealand real estate market. Use for drafting Trade Me descriptions, social media teasers, suburb-specific amenity profiles, and pre-listing renovation ROI advice. Invoke when users mention property descriptions, open home prep, renovation advice, or suburb amenities.
version: 1.0.0
---

# Marketing Suite (NZ Real Estate)

A comprehensive framework for creating high-impact property marketing and providing strategic pre-listing advice. This skill focuses on the Ray White Lower Hutt baseline, incorporating agent brand voice, local suburb knowledge, and value-maximizing checklists.

**Important**: This skill assists with marketing and strategic advice but does not replace professional photography, registered valuations, or formal building inspections. All renovation advice is based on common market trends and ROI estimates.

## When to Use This Skill

Invoke this skill when:
- Drafting property descriptions for Trade Me, realestate.co.nz, or print media.
- Creating "Coming Soon" or "Sneak Peek" social media teaser campaigns.
- Generating suburb-specific amenity profiles (e.g., school zones, transport links).
- Providing vendors with pre-listing checklists to maximize property presentation.
- Estimating the potential ROI of pre-sale renovations (e.g., painting, landscaping).
- Personalizing marketing copy to match an agent's specific brand voice (ToV).
- Translating or adapting marketing copy for multi-language community outreach.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **REA Code of Conduct** | Listing accuracy | Rule 6.4: Misleading or deceptive conduct; Rule 10.7: Material latent defects |
| **Fair Trading Act (NZ)** | Marketing claims | Prohibits misleading claims about property features or zones |
| **Privacy Act 2020 (NZ)** | Vendor privacy | Protecting vendor contact details and sensitive information |
| **Copyright Act** | Media usage | Ensuring rights to use photography and floorplans |

### AU/NZ Baseline Specifics
- **Trade Me Standards**: Adherence to Trade Me Property listing rules.
- **REA Rules**: Ensuring "puffery" does not cross into factual misrepresentation.
- **School Zones**: Accurate representation of Ministry of Education (NZ) zones.

## Quick Reference

1. **Brand Voice First**: Load the agent's ToV profile or 3 past successful listings.
2. **Clean Dictation**: Process raw "car dictation" notes into structured feature lists.
3. **Maximize Presentation**: Generate a "Pre-Listing Kit" for the vendor.
4. **Local Expert**: Integrate suburb-specific amenities (Hutt Valley focus).
5. **ROI Check**: Evaluate proposed renovations against estimated market value add.
6. **Tease Early**: Create social media teasers before the main listing goes live.
7. **Multi-Channel**: Draft Trade Me copy, social packs, and print highlights.

## Operating Modes

### Standard Mode
Full marketing workflow including deep ToV personalization, detailed suburb decoding, renovation ROI analysis, and comprehensive vendor pre-listing kits. Use for main campaign launches and strategic vendor consultations.

### Lite Mode
Streamlined generation of quick social media captions, Trade Me "snippet" updates, or rapid suburb amenity lists. Optimized for agents on the move using mobile dictation.

## Detailed Guidance

### 1. ToV Personalization (The Agent's Voice)

Every top agent has a distinct "voice." Use these patterns:
- **The Punchy Direct**: Focus on features, floor area, and ROI. Short, impactful sentences.
- **The Poetic Lifestyle**: Focus on light, flow, morning coffee on the deck, and family memories.
- **The Local Authority**: Focus on school zones, community vibes, and long-term capital growth.

**Task**: Match the drafted copy to the provided agent profile or past examples.

### 2. Suburb Decoder (Lower Hutt Example)

Highlight local benefits to prove expertise:
- **Petone**: Beachfront vibe, Jackson St cafes, heritage charm, 12 min train to Wellington.
- **Waterloo**: Premier school zones (Hutt Valley High), Waterloo station hub, flat walking.
- **Maungaraki**: Panoramic views, "The Maungaraki Shop," strong community feel, hills lifestyle.
- **Wainuiomata**: Family value, regional park access, newer subdivisions, "The Nui" community.

### 3. Renovation ROI Estimator

Advise vendors on where to spend money before selling:
- **High ROI**: Interior painting (neutral colors), professional landscaping/hedging, fixing the letterbox/front door.
- **Medium ROI**: Modernizing kitchen hardware (handles/taps), LED lighting upgrades.
- **Low ROI**: Full high-end kitchen/bath renovations (unlikely to recoup 100% cost in a flat market).

### 4. Voice-to-Text Cleaner

Process messy dictation (e.g., "Umm yeah so it's got three beds... actually four if you count the study... umm Petone beach is real close..."):
1. Strip filler words ("umm", "ah").
2. Standardize property specs (e.g., "3 beds + study").
3. Map location cues to the Suburb Decoder.
4. Structure into a professional feature list before drafting.

## Documentation Requirements

- [ ] **Agent ToV Profile**: Summary of the preferred writing style.
- [ ] **Pre-Listing Checklist**: Actionable tasks for the vendor.
- [ ] **Marketing Drafts**: Trade Me, Social, and Print versions.
- [ ] **Suburb Amenity Card**: Local hooks included in the copy.
- [ ] **ROI Rationale**: Brief justification for any renovation advice given.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Misrepresenting School Zones** | High legal risk; major buyer grievance | Use "In zone for [School]" only if verified via Education Counts. |
| **Ignoring the "Rainy Day" Vibe** | Property feels dark and cold | Add "Rainy Day Pivot" advice: all lights on, heat to 22 degrees. |
| **Generic Descriptions** | Listing blends in with 100 others | Use the Suburb Decoder and Agent Voice to find a unique "Hook." |
| **Over-promising on Renovation** | Vendor loses money | Frame ROI as "Estimated market appeal" rather than guaranteed profit. |

## When to Escalate

Escalate to Branch Manager or Marketing Director when:
- A vendor requests marketing claims that clearly contradict the LIM or Title.
- There is a dispute over copyright for professional photography.
- The property has unique heritage listings that require specialized legal wording.
- Marketing involves high-value "Premium" properties requiring bespoke strategy.

## Privacy Considerations

- **PHI Involved**: No.
- **Data Minimization**: Do not include vendor phone numbers or sensitive motivations in public listings.
- **De-identification**: Ensure "car dictation" notes are scrubbed of sensitive personal chatter before processing.
- **Retention**: Follow agency policy for marketing draft archiving.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Clean feature list with 3 past listings for ToV match | High | Generate full marketing suite. |
| Messy dictation with vague suburb references | Medium | Clean text and ask for suburb/amenity confirmation. |
| High-stakes renovation advice for high-value property | Medium | Provide ROI estimates with strong disclaimers. |

## Tool Requirements

- `~~cloud storage` - For storing ToV profiles and draft archives.
- `~~reference manager` - For organizing suburb-specific amenity data.
- `~~social media` - For openclaw integration and teaser scheduling.

## Success Indicators

You've applied this skill well when:
- [ ] The marketing copy sounds exactly like the specific agent.
- [ ] Trade Me listing views and "Watchlist" counts exceed suburb averages.
- [ ] The vendor follows the pre-listing checklist, improving first impressions.
- [ ] Local amenities are highlighted accurately, proving local expertise.

## Related Skills

- `~~real-estate/lead-management` - For managing interest generated by marketing.
- `~~real-estate/property-analyst` - For ensuring the marketing price aligns with appraisal.
- `~~real-estate/compliance-closer` - For final REA check before go-live.

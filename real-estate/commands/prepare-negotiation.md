---
name: prepare-negotiation
alias:
  - multi-offer
  - auction-prep
description: Develop a negotiation strategy for multi-offers, auctions, or complex counter-proposals.
arguments:
  - name: scenario
    description: "Brief description of the offers received (e.g., '2 offers, one subject to house sale')."
    required: true
  - name: method
    description: "Method of sale (Auction, Tender, Deadline, BEO)."
    required: true
---

# /prepare-negotiation Command

Maximize the deal outcome with specialized negotiation tactics and multi-offer management.

## When to Use

Use this command when:
- You've just received multiple offers and need to present them to the vendor.
- You're preparing for an Auction tomorrow and need an "Opening Statement."
- You need to draft professional "Counter-offer" wording for a difficult clause.
- You want to "Score" different offers to help the vendor decide.

## Workflow

### 1. Strategic Analysis

Use `~~real-estate/compliance-closer` to:
- Compare offers on Price, Conditions, and Possession.
- Draft "Multi-offer Protocol" scripts for buyers.
- Generate high-impact "Auction Openers" based on the property's emotional hooks.

### 2. Formulate Strategy

Produce:
- **Negotiation Brief**: Suggested counter-prices and clause revisions.
- **The "Multi-Offer Scorecard"**: A table helping the vendor see the best total value.
- **The "Best & Final" Script**: Wording to push buyers to their limit.

## Example Session

**User:** `/prepare-negotiation scenario: "Offer A: $1.15m, subject to sale. Offer B: $1.12m, unconditional." method: "Deadline Sale"`

**System:**
```
[~] ANALYZING MULTI-OFFER SCENARIO...
[~] SCORING CONTRACT RISK...

NEGOTIATION STRATEGY READY:

1. The Comparison:
   - Offer A (Higher Price): $1.15m but 'Subject to Sale' adds ~21 days of uncertainty and high crash risk.
   - Offer B (Superior Terms): $1.12m Unconditional is effectively 'Money in the bank' today.

2. Strategic Recommendation:
   - "Counter Offer B at $1.14m. The security of an unconditional deal is worth the $10k gap, but there is room to close the price difference."

3. The 'Best & Final' Script:
   - "We have received multiple interest. If you want to secure this Petone home today without competition, this is the moment to put your best foot forward."

Would you like to draft the counter-offer wording for Offer B? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/compliance-closer`.
- **Upstream**: Uses outputs from `/generate-appraisal`.
- **Downstream**: Feeds into `lead-management` for the settlement handover.

---
name: client-intel
description: Perform deep research on potential high-value clients using search connectors to prepare for listing presentations.
arguments:
  - name: client_name
    description: "Full name of the potential vendor or high-value buyer."
    required: true
  - name: context
    description: "Suburb, industry, or company if known."
    required: false
---

# /client-intel Command

Gain a strategic edge by knowing your client's history and public profile.

## When to Use

Use this command when:
- Preparing for a first meeting with a potential "High Value" vendor.
- You need to vet a mysterious buyer who is making a significant offer.
- You want to find "Common Ground" (e.g., shared interests, professional history) to build rapport.

## Workflow

### 1. Multi-Source Search

Use `~~google-search` and `~~real-estate/shadow-workflow` to:
- Find recent business news or LinkedIn activity for `client_name`.
- Identify recent property transactions associated with their name/company (Public Record).

### 2. Strategic Synthesis

Produce:
- **Client Deep Profile**: Summary of professional background and public reputation.
- **Transaction History**: (If found) Recent buys/sells.
- **Rapport Hooks**: 3 suggested conversation starters based on the research.

## Example Session

**User:** `/client-intel client_name: "Sarah Wellington" context: "CEO of TechCorp, lives in Waterloo"`

**System:**
```
[~] PERFORMING DEEP SEARCH...
[~] SYNTHESIZING CLIENT PROFILE...

CLIENT INTEL READY:

1. Profile: Sarah Wellington is the founder of TechCorp. Recently featured in NZ Business Herald for 'Expanding Hutt operations'. 
2. Connection Hook: Mention the 'Melling Link' infra project—it directly impacts her TechCorp office commute and her Waterloo home value.
3. Rapport Starter: "I saw the recent TechCorp expansion news; it's great to see more high-tech jobs staying in the Hutt Valley."

Strategic Edge: She is likely 'Time Poor' and 'Result Focused'. Lead your presentation with data and efficiency rather than 'poetic' lifestyle copy.

Would you like to draft a 'Result Focused' marketing teaser for her Waterloo home? [Y/n]
```

## Integration Points

- **Tool**: Uses `~~google-search`.
- **Downstream**: Feeds into `/draft-listing`.

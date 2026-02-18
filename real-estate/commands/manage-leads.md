---
name: manage-leads
alias:
  - nurture-leads
  - rank-leads
description: Prioritize daily prospecting calls, rank open home visitors, and draft personalized follow-ups based on CRM data.
arguments:
  - name: data
    description: "Raw visitor logs from open homes or prospecting notes from NurtureCloud."
    required: true
  - name: goal
    description: "Specific focus (e.g., 'Identify 5-star buyers' or 'Draft follow-up SMS')."
    required: false
---

# /manage-leads Command

Optimize your lead conversion by ranking buyers and automating follow-ups.

## When to Use

Use this command when:
- You've just finished a busy open home and need to know who to call first.
- You're starting your morning "Power Hour" of prospecting calls.
- You want to segment your database by "Life Stage" (e.g., Growing Family vs. Empty Nester).
- You need a "Rainy Day" strategy for an upcoming campaign.

## Workflow

### 1. Analyze & Rank

Use `~~real-estate/lead-management` to:
- Identify "Hot Leads" ( finance-ready, highly motivated).
- Categorize database contacts into "Golden Database" tags.
- Detect "Missing Referrals" (e.g., buyers needing a mortgage broker).

### 2. Generate Action Items

Produce:
- **Priority Call List**: Top leads with a "Reason for Call" and "Strategic Hook."
- **Follow-up Suite**: Personalized SMS and Email drafts for each lead.
- **Referral Brief**: Professional handoff for Loan Market or Concierge.

## Example Session

**User:** `/manage-leads data: "John Smith - loves the kitchen, finance approved, needs to sell in Waterloo first. Mary Jones - first home buyer, pre-approved, ready to offer."`

**System:**
```
[~] ANALYZING BUYER MOTIVATION...
[~] RANKING HOT LEADS...

CONVERSION STRATEGY READY:

1. Hot Lead #1 (5-Star): Mary Jones (Ready to offer, finance approved).
   - Action: Immediate call to draft contract. 
   - Hook: "Confirming Mary's interest in the Petone beachfront before the weekend."

2. Hot Lead #2 (4-Star): John Smith (Motivation high, but 'subject to sale' hurdle).
   - Action: Offer a market appraisal for his Waterloo home.
   - Hook: "Strategic plan to get Waterloo sold so Petone can be secured."

3. Referrals Needed: Mary Jones (Concierge referral for her upcoming move).

Would you like to draft the contract offer for Mary Jones? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/lead-management`.
- **Downstream**: Feeds into `/prepare-negotiation`.

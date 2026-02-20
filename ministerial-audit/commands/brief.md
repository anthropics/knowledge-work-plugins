---
name: brief
description: Generate a comprehensive "Counter-Brief" or "Shadow Brief" to challenge a departmental narrative.
arguments:
  - name: document
    description: The departmental briefing or proposal to counter.
  - name: intent
    description: (Optional) The Minister's specific goal or ideological direction.
---

# /brief Command

Generate a structured "Counter-Brief" to empower the Minister in Cabinet or departmental meetings.

## When to Use

Use this command when:
- You need to challenge a departmental "Preferred Option."
- You want to identify what was *omitted* from a proposal.
- You need to prepare a strategic defense for a radical policy move.
- You want a comprehensive risk/benefit analysis from a political perspective.

## Workflow

### 1. Document Analysis

Perform a deep audit using:
- **bureaucracy-redliner**: Detect jargon, "slow-walk" tactics, and budget gold-plating.
- **strategic-synthesis**: Identify consultation gaps and evidence flaws.

### 2. Strategic Alternative Generation

Generate **Option 4**:
- Develop a credible alternative that aligns with the Minister's intent.
- Compare it against the departmental "Preferred Option" on Cost, Risk, and political ROI.

### 3. Risk & Accountability Mapping

- **Political Risk Radar**: Identify winners, losers, and media sentiment.
- **Sunset/Review Design**: Build in accountability triggers (Sunset clauses, Independent reviews).

### 4. The "Counter-Brief" Suite

Produce a consolidated report including:
1. **Executive Summary**: The "Bottom Line" risk to the Minister.
2. **The "Option 4" Proposal**: A ready-to-use alternative directive.
3. **The "Truth in Jargon" Table**: Decoding the departmental brief.
4. **Stakeholder Gap Report**: Who was missed in consultation.

## Example Session

**User:** `/brief document: treasury_advice_on_tax_rebate.pdf intent: "Maximize benefit for working families with children"`

**System:**
```
Shadow Briefing - Tax Rebate Proposal

[~] ANALYZING TREASURY ADVICE...
[~] GENERATING STRATEGIC ALTERNATIVES...

COUNTER-BRIEF READY.

1. The "Option 4" (Political Alternative):
Treasury recommends a broad-based rebate (Option 3). We propose "The Working Family Targeted Rebate" which shifts 20% of the funding from high-earners to households with 2+ children. 
- Fiscal Impact: Neutral vs Treasury Option 3.
- Political Impact: High (Aligns with election commitment #4).

2. Bureaucratic "Slow-Walk" Flag:
Treasury claims IT systems require 18 months to update. Our synthesis identifies that a "Payment via Tax Code" manual override could implement the core benefit in 4 months.

3. Stakeholder Blind Spot:
The brief consults major retailers but ignores the impact on childcare providers.

4. Proposed Accountability:
Include a 24-month Sunset Clause and a mandatory Review by the Productivity Commission.

Would you like to draft "Interrogatory Questions" for the Treasury Secretary based on this brief? [Y/n]
```

## Integration Points

- **Skills**: Uses `~~ministerial-audit/bureaucracy-redliner` and `~~ministerial-audit/strategic-synthesis`.
- **Downstream**: Feeds into `/prep-meeting` and `/comms`.

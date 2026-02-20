---
name: vendor-report
alias:
  - weekly-report
  - campaign-update
description: Synthesize open home feedback and market data into a professional weekly report for the property vendor.
arguments:
  - name: feedback
    description: "Raw notes from open homes and private viewings."
    required: true
  - name: stats
    description: "Trade Me views, watchlist counts, and contract requests."
    required: false
---

# /vendor-report Command

Keep your vendors informed and manage their expectations with data-driven reports.

## When to Use

Use this command when:
- Preparing your Monday morning "Campaign Update" for a vendor.
- You need to justify a "Price Pivot" or "Marketing Strategy Change."
- You want to demonstrate the value of your local expertise.

## Workflow

### 1. Synthesize Sentiment

Use `~~real-estate/lead-management` to:
- Categorize feedback into "Positive," "Critical," and "Pricing."
- Highlight market sentiment trends (e.g., "Interest remains high forPetone beachfront").

### 2. Formulate Strategy

Produce:
- **Weekly Summary**: Narrative overview of the campaign's progress.
- **The Sentiment Matrix**: What buyers like vs. what is holding them back.
- **Strategic Recommendation**: "Stay the course," "Price Revision," or "Feature Pivot."

## Example Session

**User:** `/vendor-report feedback: "Petone Beachfront OH: 12 groups. Feedback: 'stunning sun,' 'kitchen feels a bit dated,' 'wondering if $1.2m is too high compared to Maungaraki.'"`

**System:**
```
[~] SYNTHESIZING VENDOR REPORT...
[~] COMPARING SUBURB BENCHMARKS...

WEEKLY VENDOR UPDATE READY:

1. Campaign Snapshot: Strong engagement (12 groups). Interest is highly concentrated on the 'Lifestyle/Beachfront' hook.
2. The Sentiment: Sunlight and location are 5-star features. The kitchen condition is the primary price-resistance point.
3. Market Reality: Suburb benchmark suggests $1.2m is aggressive for a 'dated' kitchen compared to recent Maungaraki sales.
4. Recommendation: Maintain price for 7 more days to capture 'Hot Lead' Mary Jones. If no contract by Wednesday, consider a 'BEO $1.15m' pivot.

Would you like to draft the 'Price Revision' email for the vendor? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/lead-management`.
- **Downstream**: Feeds into `/draft-listing` if a marketing pivot is needed.

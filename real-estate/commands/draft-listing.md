---
name: draft-listing
alias:
  - listing-draft
  - create-ad
description: Draft a professional property listing for Trade Me, social media, and print based on raw notes, dictation, or photos.
arguments:
  - name: notes
    description: "Raw property features, car dictation text, or photo descriptions."
    required: true
  - name: agent_voice
    description: "Brief description of the agent's tone (e.g., 'punchy and direct' or 'poetic lifestyle')."
    required: false
  - name: suburb
    description: "The specific Lower Hutt or NZ suburb for amenity decoding."
    required: false
---

# /draft-listing Command

Draft a complete marketing suite for a new property listing, optimized for NZ platforms.

## When to Use

Use this command when:
- You've just walked through a new property and have messy notes or dictation.
- You need to launch a "Coming Soon" teaser on social media.
- You want to ensure your Trade Me copy includes local suburb "Hooks."
- You need a pre-listing checklist to hand to the vendor.

## Workflow

### 1. Clean & Structure

Use `~~real-estate/marketing-suite` to:
- Process the `notes` (cleaning dictation, stripping filler).
- Map the property to the `suburb` amenities.
- Align the tone with the `agent_voice`.

### 2. Generate Marketing Artifacts

Produce:
- **Trade Me/Web Copy**: Main description with "Headline," "Hook," and "Feature List."
- **Social Media Pack**: 1x "Sneak Peek" post and 1x "Full Launch" post (OpenClaw style).
- **Print Highlights**: 3-5 bullet points for signboards or window displays.
- **Suburb amenity Card**: Why this location wins.

### 3. Provide Vendor Value

Generate:
- **Pre-Listing Checklist**: 5-7 tasks for the vendor to maximize value.
- **Renovation ROI Note**: (If renovations mentioned in notes) Advice on value-add potential.

## Example Session

**User:** `/draft-listing notes: "Petone beachfront, 3 bed villa, original floorboards, needs a bit of love in the garden, great sun, in zone for petone central" agent_voice: "poetic and heritage focused" suburb: "Petone"`

**System:**
```
[~] CLEANING DICTATION...
[~] DECODING PETONE AMENITIES...
[~] MATCHING HERITAGE VOICE...

MARKETING SUITE READY:

1. Trade Me Headline: "Heritage Charm Meets Beachfront Bliss in the Heart of Petone"
2. Trade Me Copy: "Step back in time and breathe in the salt air. This iconic 3-bedroom villa captures the very essence of Petone living... [Poetic description of boards and sun]... Just moments from the Jackson St buzz..."
3. Social Teaser: "Wait until you see the light in this Petone beachfront beauty. Coming soon. #PetoneLiving #HeritageVilla"
4. Vendor Tip: "Fix the front letterbox and trim the beachfront hedges to instantly boost that coastal street appeal."

Would you like to generate a 'Rainy Day Pivot' strategy for the first open home? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/marketing-suite`.
- **Downstream**: Feeds into `/generate-appraisal` for price alignment.

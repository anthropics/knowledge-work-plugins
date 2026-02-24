---
name: private-brief
description: Synthesize forwarded email threads and CRM data into a private situation report using Gemini Pro.
arguments:
  - name: email_thread
    description: "The forwarded email history from the client."
    required: true
  - name: property_context
    description: "Related property data from Vault RE (or private sheet)."
    required: false
---

# /private-brief Command

Use Gemini Pro to find the "hidden truth" in long email threads and corporate data.

## When to Use

Use this command when:
- A client inquiry becomes complex and you need a high-speed summary.
- You want to check for consistency between what a buyer said in an email vs. what they told you at an open home.
- Preparing for a difficult vendor negotiation where history matters.

## Workflow

### 1. Gemini Pro Synthesis (The Shadow Brain)

Use `~~real-estate/shadow-workflow` to:
- Summarize the `email_thread` (identifying emotional cues, deadlines, and requirements).
- Cross-reference with `property_context` (e.g., "This buyer liked Petone but is now asking about Waterloo").

### 2. Output Generation

Produce:
- **Client Situation Report**: Bulleted summary of the client's current position.
- **Consistency Check**: "They say X in mail, but record shows Y."
- **Draft Reply (Sanitized)**: A high-leverage response ready for your private Workspace.

## Example Session

**User:** `/private-brief email_thread: "[Long chain about 123 Petone]" property_context: "Buyer rejected previous Maungaraki offer"`

**System:**
```
[~] GEMINI PRO ANALYZING THREAD...
[~] CROSS-REFERENCING MAUNGARAKI HISTORY...

PRIVATE BRIEF READY:

1. Summary: The buyer is highly motivated by the Petone location but is 'stalling' due to finance jitters.
2. Consistency Check: They mention a 10% deposit in email, but your private notes from Maungaraki show they have a 20% equity position. 
3. Strategic Lever: They are using 'finance' as a negotiation tactic. 
4. Sanitized Draft: "I've reviewed your latest thoughts on the beachfront villa. Based on our earlier conversation about your equity position, I'm confident we can find a way forward that works for both parties..."

Would you like to schedule an OpenClaw 'market update' for Petone to maintain pressure? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~real-estate/shadow-workflow`.
- **Downstream**: Feeds into `/prepare-negotiation`.

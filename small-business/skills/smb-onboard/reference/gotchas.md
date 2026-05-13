# Gotchas

## Gotcha: Skipping the prove-value step when a connection takes too long

**Why it matters:** If the owner connects a tool but Claude moves straight to the interview, the "aha" moment never lands. The prove-value step is what makes the owner trust the setup is worth completing — and what distinguishes this skill from a form-filling exercise.

### ✗ Bad

> "Great, QuickBooks is connected! Now let me ask you a few questions about your business."

Skips the recipe entirely. Owner leaves not knowing what they just enabled.

### ✓ Good

> "QuickBooks is live. Let me pull your last 30 days of cash flow — takes about 10 seconds."
> *[runs cash-flow-snapshot, shows results]*
> "That's what we can do anytime you want a number check. Now, a few questions about your business…"

The demo runs before the interview, every time, without exception.

---

## Gotcha: Dumping all five interview questions at once

**Why it matters:** Five questions presented together feel like a form, not a conversation. Owners either skim-answer or drop off. Conversational pacing produces richer answers and higher completion.

### ✗ Bad

> "To get you set up, I need: (1) What kind of business do you run? (2) How many employees? (3) What are your top headaches? (4) What tools do you use? (5) How often do you want check-ins?"

### ✓ Good

Ask each question, receive the full answer, then ask the next. Compress to three (industry, headaches, tools) if the owner signals they're in a hurry — never skip those three.

---

## Gotcha: Writing context without showing the profile first

**Why it matters:** Silent writes feel intrusive and remove the owner's chance to correct misheard answers. Showing the draft profile is also a natural confirmation that Claude understood correctly — it often surfaces a correction the owner wouldn't have volunteered.

### ✗ Bad

> "Got it, I've saved your business profile!"

No preview, no approval — owner doesn't know what was written.

### ✓ Good

> "Here's what I'm about to save as your business profile — let me know if anything needs fixing:"
>
> ```
> Business: Lakewood Hardware — retail hardware store
> Size: 4 people (including owner)
> Top headaches: cash flow gaps · slow-paying contractors · scheduling part-timers
> Connected tools: QuickBooks, Gmail
> Weekly cadence: weekly check-in every Monday
> Onboarded: 2026-04-23
> ```
>
> "Look right? I'll save it once you confirm."

Show the block, wait for approval, then write.

## Gotcha: Recommending brand names instead of functional categories

**Why it matters:** Naming specific products (HubSpot, QuickBooks, Gmail) before asking what the owner uses reads like a sales pitch — even with no commercial relationship behind it. Anthropic doesn't display ads in its products; an onboarding flow that opens with branded recommendations brushes against that policy. The owner also doesn't need a comparison-shopping page — they need to understand what Claude needs and why.

### ✗ Bad

> "For customers + getting organized, here's the better pair:
>
> 1. **HubSpot (CRM)** — One place for every lead, customer, deal, and conversation. Once it's in, I can prioritize who to call today, draft follow-ups, log notes from your inbox, and spot deals going stale. Direct hit on the 'customers' headache.
>
> 2. **Gmail** (or Outlook if you're on Microsoft) — Email is where most of the chaos lives…"

Reads as a SaaS comparison post. Leads with brand, uses marketing phrases ("one place for everything," "direct hit"), presents alternatives only after the pitch.

### ✓ Good

> "For those two, here's what I'd want access to:
>
> A CRM — somewhere structured to keep contacts, deals, and conversations so I can prioritize who needs attention.
>
> Your inbox — so I can read what customers are asking and surface unanswered threads.
>
> What are you using for each, if anything?"

Names the function, not the brand. One sentence on what Claude will *do* with the data. Asks the owner what they use before naming any product.

---

## Gotcha: Marketing-register phrasing

**Why it matters:** Phrases like "source of truth," "unlocks," "highest-leverage," "stage your week," "supercharge," "the better pair," "seamless," "trusted by" come from vendor copy. They feel persuasive rather than informational, even when the underlying recommendation is correct.

### ✗ Bad

> "QuickBooks — Source of truth for cash, AR, and what you're actually making after costs. Plugging this in unlocks invoice chasing, cash-flow forecasts, and month-end close. This is the single highest-leverage connection for the 'money' headache."

### ✓ Good

> "Bookkeeping — to see cash, who owes you, and what you're actually making after costs."

If a sentence would pass as a line on a vendor landing page, rewrite it.

---

## Gotcha: Mentioning cost, pricing tiers, or "free version" unprompted

**Why it matters:** Even factual cost statements ("HubSpot has a free tier," "QuickBooks Online starts at $30/month") read as soft sells when Claude offers them on its own initiative. The owner didn't ask for a buying guide. If they want to know what a tool costs, they'll ask.

### ✗ Bad

> "If you want to add a CRM later, the supported connector here is HubSpot. It has a free tier that should be fine for most small businesses."

### ✓ Good

> "If you want to add a CRM later, the supported connector here is HubSpot."

Stop there. Answer cost questions when asked, not before.

---

---
name: brand-review
description: Review content against your brand voice, style guide, and messaging pillars, flagging deviations by severity with specific before/after fixes. Use when checking a draft before it ships, when auditing copy for voice consistency and terminology, or when screening for unsubstantiated claims, missing disclaimers, and other legal flags.
argument-hint: "<content to review>"
---

# Brand Review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Review marketing content against brand voice, style guidelines, and messaging standards. Flag deviations and provide specific improvement suggestions.

## Trigger

User runs `/brand-review` or asks to review, check, or audit content against brand guidelines.

## Inputs

1. **Content to review** — accept content in any of these forms:
   - Pasted directly into the conversation
   - A file path or ~~knowledge base reference (e.g. Notion page, shared doc)
   - A URL to a published page
   - Multiple pieces for batch review

2. **Brand guidelines source** (determined automatically):
   - If a brand style guide is configured in local settings, use it automatically
   - If not configured, ask: "Do you have a brand style guide or voice guidelines I should review against? You can paste them, share a file, or describe your brand voice. Otherwise, I'll do a general review for clarity, consistency, and professionalism."

## Review Process

### With Brand Guidelines Configured

Evaluate the content against each of these dimensions:

#### Voice and Tone
- Does the content match the defined brand voice attributes?
- Is the tone appropriate for the content type and audience?
- Are there shifts in voice that feel inconsistent?
- Flag specific sentences or phrases that deviate with an explanation of why

#### Terminology and Language
- Are preferred brand terms used correctly?
- Are any "avoid" terms or phrases present?
- Is jargon level appropriate for the target audience?
- Are product names, feature names, and branded terms used correctly (capitalization, formatting)?

#### Messaging Pillars
- Does the content align with defined messaging pillars or value propositions?
- Are claims consistent with approved messaging?
- Is the content reinforcing or contradicting brand positioning?

#### Style Guide Compliance
- Grammar and punctuation per style guide (e.g., Oxford comma, title case vs. sentence case)
- Formatting conventions (headers, lists, emphasis)
- Number formatting, date formatting
- Acronym usage (defined on first use?)

### Without Brand Guidelines (Generic Review)

Evaluate the content for:

#### Clarity
- Is the main message clear within the first paragraph?
- Are sentences concise and easy to understand?
- Is the structure logical and easy to follow?
- Are there ambiguous statements or unclear references?

#### Consistency
- Is the tone consistent throughout?
- Are terms used consistently (no switching between synonyms for the same concept)?
- Is formatting consistent (headers, lists, capitalization)?

#### Professionalism
- Is the content free of typos, grammatical errors, and awkward phrasing?
- Is the tone appropriate for the intended audience?
- Are claims supported or substantiated?

### Legal and Compliance Flags (Always Checked)

Regardless of whether brand guidelines are configured, flag:
- **Unsubstantiated claims** — superlatives ("best", "fastest", "only") without evidence or qualification
- **Missing disclaimers** — financial claims, health claims, or guarantees that may need legal disclaimers
- **Comparative claims** — comparisons to competitors that could be challenged
- **Regulatory language** — content that may need compliance review (financial services, healthcare, etc.)
- **Testimonial issues** — quotes or endorsements without attribution or disclosure
- **Copyright concerns** — content that appears to be closely paraphrased from other sources

## Brand Voice Reference

Use these frameworks to evaluate content against brand standards or to help the user document their brand voice.

### Brand Voice Documentation Framework

A complete brand voice document should cover these areas:

1. **Brand Personality** — Define the brand as if it were a person. Example: "If our brand were a person, they would be a knowledgeable colleague who explains complex things simply, celebrates your wins genuinely, and never talks down to you."
2. **Voice Attributes** — 3-5 attributes that define how the brand communicates, each defined with what it means in practice, what it does NOT mean (to prevent misinterpretation), and an example.
3. **Audience Awareness** — Who the brand is speaking to (primary and secondary), what they care about, their level of expertise, and how they expect to be addressed.
4. **Core Messaging Pillars** — 3-5 key themes the brand consistently communicates, the hierarchy of these messages, and how each pillar connects to audience needs.
5. **Tone Spectrum** — How the voice adapts across contexts while remaining recognizably the same brand.
6. **Style Rules** — Specific grammar, formatting, and language rules.
7. **Terminology** — Preferred and avoided terms.

### Voice Attribute Spectrums

When defining or evaluating brand voice, position attributes on a spectrum:

| Spectrum | One End | Other End |
|----------|---------|-----------|
| Formality | Formal, institutional | Casual, conversational |
| Authority | Expert, authoritative | Peer-level, collaborative |
| Emotion | Warm, empathetic | Direct, matter-of-fact |
| Complexity | Technical, precise | Simple, accessible |
| Energy | Bold, energetic | Calm, measured |
| Humor | Playful, witty | Serious, earnest |
| Innovation | Cutting-edge, forward-looking | Established, proven |

For each chosen attribute, document it in this format:

**[Attribute name]**
- **We are**: [what this means in practice]
- **We are not**: [common misinterpretation to avoid]
- **This sounds like**: [example sentence demonstrating the attribute]
- **This does NOT sound like**: [example sentence violating the attribute]

Example:

**Approachable**
- **We are**: friendly, clear, jargon-free, welcoming to beginners and experts alike
- **We are not**: dumbed-down, overly casual, or lacking substance
- **This sounds like**: "Here's how to get started — it takes about five minutes."
- **This does NOT sound like**: "Yo! This is super easy, even a noob can do it lol."

### Tone Adaptation Across Channels and Contexts

The brand voice stays consistent, but tone adapts to context. Tone is the emotional inflection applied to the voice.

#### Tone by Channel

| Channel | Tone Adaptation | Example |
|---------|----------------|---------|
| Blog | Informative, conversational, educational | "Let's walk through how this works and why it matters for your team." |
| Social media (LinkedIn) | Professional, thought-provoking, concise | "Three things we learned from running 50 campaigns this quarter." |
| Social media (Twitter/X) | Punchy, direct, sometimes witty | "Your landing page has 3 seconds. Make them count." |
| Email marketing | Personal, helpful, action-oriented | "We put together something we think you'll find useful." |
| Sales collateral | Confident, benefit-driven, specific | "Teams using our platform reduce reporting time by 40%." |
| Support/Help docs | Clear, patient, step-by-step | "If you see this error, here's how to fix it." |
| Press release | Formal, factual, newsworthy | "The company today announced the launch of..." |
| Error messages | Empathetic, helpful, blame-free | "Something went wrong on our end. We're looking into it." |

#### Tone by Situation

| Situation | Tone Adaptation |
|-----------|----------------|
| Product launch | Excited, confident, forward-looking |
| Incident or outage | Transparent, empathetic, accountable |
| Customer success story | Celebratory, specific, crediting the customer |
| Thought leadership | Authoritative, nuanced, evidence-based |
| Onboarding | Welcoming, encouraging, clear |
| Bad news (price increase, deprecation) | Honest, respectful, solution-oriented |
| Competitive comparison | Confident but fair, fact-based, not disparaging |

#### Tone Adaptation Rule
The voice attributes remain fixed. Tone dials them up or down based on context. For example, if a brand is "bold and warm":
- In a product launch, dial up boldness
- In an incident response, dial up warmth
- Neither attribute disappears; the balance shifts

### Style Guide Enforcement

#### Grammar and Mechanics
Document and enforce these choices consistently:

| Rule | Options | Example |
|------|---------|---------|
| Oxford comma | Yes / No | "fast, reliable, and secure" vs. "fast, reliable and secure" |
| Sentence case vs. title case (headings) | Sentence / Title | "How to get started" vs. "How to Get Started" |
| Contractions | Use / Avoid | "we're" vs. "we are" |
| Em dash spacing | No spaces / Spaces | "this—and more" vs. "this — and more" |
| Numbers | Spell out 1-9, numerals 10+ / Always numerals | "five features" vs. "5 features" |
| Percent | % / percent | "50%" vs. "50 percent" |
| Date format | Month DD, YYYY / DD/MM/YYYY / etc. | "January 15, 2025" |
| Time format | 12-hour / 24-hour | "3:00 PM" vs. "15:00" |
| Lists | Periods / No periods on fragments | "Set up your account." vs. "Set up your account" |

#### Formatting Conventions
- Heading hierarchy (when to use H1, H2, H3)
- Bold and italic usage (bold for emphasis, italic for titles/terms)
- Link text (descriptive vs. "click here" — always descriptive)
- Image alt text requirements
- Code formatting (for technical brands)
- Callout or highlight box usage

#### Punctuation and Emphasis
- Exclamation mark policy (limited use, never more than one)
- Ellipsis usage (avoid in most professional contexts)
- ALL CAPS policy (avoid; use bold for emphasis instead)
- Emoji usage by channel (professional channels: minimal or none; social: where appropriate)

### Terminology Management

#### Preferred Terms

Maintain a list of preferred terms and their incorrect alternatives:

| Use This | Not This | Notes |
|----------|----------|-------|
| sign up (verb) | signup (verb) | "signup" is the noun form |
| log in (verb) | login (verb) | "login" is the noun/adjective form |
| set up (verb) | setup (verb) | "setup" is the noun/adjective form |
| email | e-mail | No hyphen |
| website | web site | One word |
| data is (singular) | data are | Unless the publication requires plural |

#### Product and Feature Names
- Official capitalization for product names
- When to use the full product name vs. shorthand
- Whether to use "the" before product names
- How to handle versioning in copy
- Trademark and registration symbols (when required and when to omit)

#### Inclusive Language
- Use gender-neutral language (they/them for unknown individuals)
- Avoid ableist language ("crazy", "blind spot", "lame")
- Use person-first language where appropriate
- Avoid culturally specific idioms that may not translate
- Use "simple" or "straightforward" instead of "easy" (what is easy varies by person)

#### Industry Jargon Management
- Define which technical terms the audience understands without explanation
- List jargon that should always be defined or replaced with plain language
- Specify which acronyms need to be spelled out on first use
- Audience-specific glossary for terms that mean different things to different readers

#### Competitor and Category Terms
- How to refer to your product category (use your preferred framing)
- How to refer to competitors (by name or generically)
- Terms competitors have coined that you should avoid (to prevent reinforcing their positioning)
- Your preferred differentiation language

## Output Format

Present the review as:

### Summary
- Overall assessment: how well the content aligns with brand standards (or general quality)
- 1-2 sentence summary of the biggest strengths
- 1-2 sentence summary of the most important improvements

### Detailed Findings

For each issue found, provide:

| Issue | Location | Severity | Suggestion |
|-------|----------|----------|------------|

Where severity is:
- **High** — contradicts brand voice, contains compliance risk, or significantly undermines messaging
- **Medium** — inconsistent with guidelines but not damaging
- **Low** — minor style or preference issue

### Revised Sections

For the top 3-5 highest-severity issues, provide a before/after showing the original text and a suggested revision.

### Legal/Compliance Flags

List any legal or compliance concerns separately with recommended actions.

## After Review

Ask: "Would you like me to:
- Revise the full content with these suggestions applied?
- Focus on fixing just the high-severity issues?
- Review additional content against the same guidelines?
- Help you document your brand voice for future reviews?"

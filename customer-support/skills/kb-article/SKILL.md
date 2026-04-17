---
name: kb-article
description: Draft a knowledge base article from a resolved issue or common question. Use when a ticket resolution is worth documenting for self-service, the same question keeps coming up, a workaround needs to be published, or a known issue should be communicated to customers.
argument-hint: "<resolved issue or ticket>"
---

# /kb-article

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Draft a publish-ready knowledge base article from a resolved support issue, common question, or documented workaround. Structures the content for searchability and self-service.

## Usage

```
/kb-article <resolved issue, ticket reference, or topic description>
```

Examples:
- `/kb-article How to configure SSO with Okta — resolved this for 3 customers last month`
- `/kb-article Ticket #4521 — customer couldn't export data over 10k rows`
- `/kb-article Common question: how to set up webhook notifications`
- `/kb-article Known issue: dashboard charts not loading on Safari 16`

## Workflow

### 1. Understand the Source Material

Parse the input to identify:

- **What was the problem?** The original issue, question, or error
- **What was the solution?** The resolution, workaround, or answer
- **Who does this affect?** User type, plan level, or configuration
- **How common is this?** One-off or recurring issue
- **What article type fits best?** How-to, troubleshooting, FAQ, known issue, or reference (see article types below)

If a ticket reference is provided, look up the full context:

- **~~support platform**: Pull the ticket thread, resolution, and any internal notes
- **~~knowledge base**: Check if a similar article already exists (update vs. create new)
- **~~project tracker**: Check if there's a related bug or feature request

### 2. Draft the Article

Using the article structure, formatting standards, and searchability best practices below:

- Follow the template for the chosen article type (how-to, troubleshooting, FAQ, known issue, or reference)
- Apply the searchability best practices: customer-language title, plain-language opening sentence, exact error messages, common synonyms
- Keep it scannable: headers, numbered steps, short paragraphs

### 3. Generate the Article

Present the draft with metadata:

```
## KB Article Draft

**Title:** [Article title]
**Type:** [How-to / Troubleshooting / FAQ / Known Issue / Reference]
**Category:** [Product area or topic]
**Tags:** [Searchable tags]
**Audience:** [All users / Admins / Developers / Specific plan]

---

[Full article content — using the appropriate template below]

---

### Publishing Notes
- **Source:** [Ticket #, customer conversation, or internal discussion]
- **Existing articles to update:** [If this overlaps with existing content]
- **Review needed from:** [SME or team if technical accuracy needs verification]
- **Suggested review date:** [When to revisit for accuracy]
```

### 4. Offer Next Steps

After generating the article:
- "Want me to check if a similar article already exists in your ~~knowledge base?"
- "Should I adjust the technical depth for a different audience?"
- "Want me to draft a companion article (e.g., a how-to to go with this troubleshooting guide)?"
- "Should I create an internal-only version with additional technical detail?"

---

## Article Structure and Formatting Standards

### Universal Article Elements

Every KB article should include:

1. **Title**: Clear, searchable, describes the outcome or problem (not internal jargon)
2. **Overview**: 1-2 sentences explaining what this article covers and who it's for
3. **Body**: Structured content appropriate to the article type
4. **Related articles**: Links to relevant companion content
5. **Metadata**: Category, tags, audience, last updated date

### Formatting Rules

- **Use headers (H2, H3)** to break content into scannable sections
- **Use numbered lists** for sequential steps
- **Use bullet lists** for non-sequential items
- **Use bold** for UI element names, key terms, and emphasis
- **Use code blocks** for commands, API calls, error messages, and configuration values
- **Use tables** for comparisons, options, or reference data
- **Use callouts/notes** for warnings, tips, and important caveats
- **Keep paragraphs short** — 2-4 sentences max
- **One idea per section** — if a section covers two topics, split it

## Writing for Searchability

Articles are useless if customers can't find them. Optimize every article for search:

### Title Best Practices

| Good Title | Bad Title | Why |
|------------|-----------|-----|
| "How to configure SSO with Okta" | "SSO Setup" | Specific, includes the tool name customers search for |
| "Fix: Dashboard shows blank page" | "Dashboard Issue" | Includes the symptom customers experience |
| "API rate limits and quotas" | "API Information" | Includes the specific terms customers search for |
| "Error: 'Connection refused' when importing data" | "Import Problems" | Includes the exact error message |

### Keyword Optimization

- **Include exact error messages** — customers copy-paste error text into search
- **Use customer language**, not internal terminology — "can't log in" not "authentication failure"
- **Include common synonyms** — "delete/remove", "dashboard/home page", "export/download"
- **Add alternate phrasings** — address the same issue from different angles in the overview
- **Tag with product areas** — make sure category and tags match how customers think about the product

### Opening Sentence Formula

Start every article with a sentence that restates the problem or task in plain language:

- **How-to**: "This guide shows you how to [accomplish X]."
- **Troubleshooting**: "If you're seeing [symptom], this article explains how to fix it."
- **FAQ**: "[Question in the customer's words]? Here's the answer."
- **Known issue**: "Some users are experiencing [symptom]. Here's what we know and how to work around it."

## Article Type Templates

### How-to Articles

**Purpose**: Step-by-step instructions for accomplishing a task.

**Structure**:
```
# How to [accomplish task]

[Overview — what this guide covers and when you'd use it]

## Prerequisites
- [What's needed before starting]

## Steps
### 1. [Action]
[Instruction with specific details]

### 2. [Action]
[Instruction]

## Verify It Worked
[How to confirm success]

## Common Issues
- [Issue]: [Fix]

## Related Articles
- [Links]
```

**Best practices**:
- Start each step with a verb
- Include the specific path: "Go to Settings > Integrations > API Keys"
- Mention what the user should see after each step ("You should see a green confirmation banner")
- Test the steps yourself or verify with a recent ticket resolution

### Troubleshooting Articles

**Purpose**: Diagnose and resolve a specific problem.

**Structure**:
```
# [Problem description — what the user sees]

## Symptoms
- [What the user observes]

## Cause
[Why this happens — brief, non-jargon explanation]

## Solution
### Option 1: [Primary fix]
[Steps]

### Option 2: [Alternative if Option 1 doesn't work]
[Steps]

## Prevention
[How to avoid this in the future]

## Still Having Issues?
[How to get help]
```

**Best practices**:
- Lead with symptoms, not causes — customers search for what they see
- Provide multiple solutions when possible (most likely fix first)
- Include a "Still having issues?" section that points to support
- If the root cause is complex, keep the customer-facing explanation simple

### FAQ Articles

**Purpose**: Quick answer to a common question.

**Structure**:
```
# [Question — in the customer's words]

[Direct answer — 1-3 sentences]

## Details
[Additional context, nuance, or explanation if needed]

## Related Questions
- [Link to related FAQ]
- [Link to related FAQ]
```

**Best practices**:
- Answer the question in the first sentence
- Keep it concise — if the answer needs a walkthrough, it's a how-to, not an FAQ
- Group related FAQs and link between them

### Known Issue Articles

**Purpose**: Document a known bug or limitation with a workaround.

**Structure**:
```
# [Known Issue]: [Brief description]

**Status:** [Investigating / Workaround Available / Fix In Progress / Resolved]
**Affected:** [Who/what is affected]
**Last updated:** [Date]

## Symptoms
[What users experience]

## Workaround
[Steps to work around the issue, or "No workaround available"]

## Fix Timeline
[Expected fix date or current status]

## Updates
- [Date]: [Update]
```

**Best practices**:
- Keep the status current — nothing erodes trust faster than a stale known issue article
- Update the article when the fix ships and mark as resolved
- If resolved, keep the article live for 30 days for customers still searching the old symptoms

## Review and Maintenance Cadence

Knowledge bases decay without maintenance. Follow this schedule:

| Activity | Frequency | Who |
|----------|-----------|-----|
| **New article review** | Before publishing | Peer review + SME for technical content |
| **Accuracy audit** | Quarterly | Support team reviews top-traffic articles |
| **Stale content check** | Monthly | Flag articles not updated in 6+ months |
| **Known issue updates** | Weekly | Update status on all open known issues |
| **Analytics review** | Monthly | Check which articles have low helpfulness ratings or high bounce rates |
| **Gap analysis** | Quarterly | Identify top ticket topics without KB articles |

### Article Lifecycle

1. **Draft**: Written, needs review
2. **Published**: Live and available to customers
3. **Needs update**: Flagged for revision (product change, feedback, or age)
4. **Archived**: No longer relevant but preserved for reference
5. **Retired**: Removed from the knowledge base

### When to Update vs. Create New

**Update existing** when:
- The product changed and steps need refreshing
- The article is mostly right but missing a detail
- Feedback indicates customers are confused by a specific section
- A better workaround or solution was found

**Create new** when:
- A new feature or product area needs documentation
- A resolved ticket reveals a gap — no article exists for this topic
- The existing article covers too many topics and should be split
- A different audience needs the same information explained differently

## Linking and Categorization Taxonomy

### Category Structure

Organize articles into a hierarchy that matches how customers think:

```
Getting Started
├── Account setup
├── First-time configuration
└── Quick start guides

Features & How-tos
├── [Feature area 1]
├── [Feature area 2]
└── [Feature area 3]

Integrations
├── [Integration 1]
├── [Integration 2]
└── API reference

Troubleshooting
├── Common errors
├── Performance issues
└── Known issues

Billing & Account
├── Plans and pricing
├── Billing questions
└── Account management
```

### Linking Best Practices

- **Link from troubleshooting to how-to**: "For setup instructions, see [How to configure X]"
- **Link from how-to to troubleshooting**: "If you encounter errors, see [Troubleshooting X]"
- **Link from FAQ to detailed articles**: "For a full walkthrough, see [Guide to X]"
- **Link from known issues to workarounds**: Keep the chain from problem to solution short
- **Use relative links** within the KB — they survive restructuring better than absolute URLs
- **Avoid circular links** — if A links to B, B shouldn't link back to A unless both are genuinely useful entry points

## KB Writing Best Practices

1. Write for the customer who is frustrated and searching for an answer — be clear, direct, and helpful
2. Every article should be findable through search using the words a customer would type
3. Test your articles — follow the steps yourself or have someone unfamiliar with the topic follow them
4. Keep articles focused — one problem, one solution. Split if an article is growing too long
5. Maintain aggressively — a wrong article is worse than no article
6. Track what's missing — every ticket that could have been a KB article is a content gap
7. Measure impact — articles that don't get traffic or don't reduce tickets need to be improved or retired

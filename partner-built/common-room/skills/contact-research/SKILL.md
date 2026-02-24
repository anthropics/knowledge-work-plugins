---
name: contact-research
description: "Research a specific person using Common Room data. Triggers on 'who is [name]', 'look up [email]', 'research [contact]', 'is [name] a warm lead', or any contact-level question."
---

# Contact Research

Retrieve a comprehensive contact profile from Common Room. Supports lookup by email, social handle, or name + company. Returns enriched data including activity history, Spark, scores, website visits, and CRM fields.

## Step 1: Locate the Contact

Common Room supports multiple lookup methods — use whichever the user has provided:

| What the user gives | Lookup method |
|---------------------|--------------|
| Email address | Look up by email (most reliable) |
| LinkedIn, Twitter/X, or GitHub handle | Look up by social handle — specify handle type explicitly |
| Name + company | Identity resolution by name + org domain; present matches if ambiguous |
| Name only | Search by name; if multiple matches, show a brief list and ask the user to confirm |

If no match is found, respond: "Common Room doesn't have a record for this person." Do not speculate or fabricate profile data.

## Step 2: Fetch Contact Fields

Use the Common Room object catalog to see available field groups and their contents. For full profiles, request all groups. For targeted questions, request only what's relevant.

**Key field groups to know about:**
- **Scores** — always return as raw values or percentiles, never labels
- **Recent activity** — use `Contact Initiated` filter (last 60 days) for their actions, not your team's
- **Website visits** — total count + specific pages (last 12 weeks)
- **Spark** — retrieve all Sparks when tracking engagement evolution over time

## Step 3: Run Spark Enrichment (If Available)

If Spark is available, use it. Spark provides:
- Professional background and job history
- Social presence and influence signals
- Persona classification: Champion, Economic Buyer, Technical Evaluator, End User, or Gatekeeper
- Inferred role in the buying process

If Spark is unavailable but real activity data exists (recent actions, website visits, community engagement), infer a persona from those signals. If neither Spark nor activity data is available, classify as Unknown — do not guess a persona from title alone.

Retrieve **all Sparks** (not just the most recent) when the user wants to understand how this contact's engagement has evolved over time.

## Step 4: Assess Account Context

Pull an abbreviated account snapshot for this contact's parent company. Note:
- Open opportunities, expansion signals, or churn risk at the account level
- Whether other contacts at this company are also active
- How this person's engagement compares to their colleagues

## Step 5: Identify Conversation Angles

Based on activity and signals, surface the strongest 2–3 hooks:
- A recent `Contact Initiated` activity (community post, product event, support ticket)
- A specific web page they visited recently — especially if it signals evaluation intent
- A job change, promotion, or company news
- Their Spark persona and what that suggests about communication style
- Their role in a known active deal

## Output Format

Only include sections where data was actually returned. Omit sections with no data rather than filling them with guesses.

**When data is rich:**

```
## [Contact Name] — Profile

**Overview**
[2 sentences: who they are, their role, and relationship status]

**Details**
- Title: [title]
- Company: [company]
- Email: [email]
- LinkedIn: [URL]
- Other profiles: [Twitter/X, GitHub, CRM link if available]

**Scores** [If scores returned]
[All scores as raw values or percentiles]

**Recent Activity** (last 60 days) [If activity returned]
[3–5 bullets with dates]

**Website Visits** (last 12 weeks) [If visit data exists]
[Total visit count + list of pages visited]

**Spark Profile** [If Spark data is non-null]
[Persona type, background summary, influence signals]

**Segments** [If segments returned]
[List of segment names this contact belongs to]

**Account Context**
[1–2 sentences on their company's status]

**Conversation Starters**
[2–3 specific, signal-backed openers]
```

**When data is sparse (e.g., only name, title, email, tags returned; sparkSummary is null):**

```
## [Contact Name] — Profile (Limited Data)

**Data available:** [List exactly what Common Room returned]

[Present only the returned fields]

**Web Search**
[Any findings from searching their name + company]

**Note:** Common Room has limited data on this contact. No activity history, scores, or Spark profile available. I can run deeper web searches or look up their company for additional context.
```

Do not generate conversation starters, persona inferences, or engagement assessments from sparse data. These require real signals.

## Quality Standards

- Lookup must use the correct method for the input type — don't guess on email vs. handle
- Scores as raw/percentile only — never labels
- `Contact Initiated` activity (last 60 days) is the primary engagement signal — lead with it
- If Spark is unavailable, say so — don't fabricate a persona from title alone
- Flag any contact where the most recent activity is older than 30 days

## Reference Files

- **`references/contact-signals-guide.md`** — full field descriptions, Spark persona guide, and conversation starter principles

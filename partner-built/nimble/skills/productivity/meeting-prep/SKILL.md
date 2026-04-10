---
name: meeting-prep
description: |
  Researches meeting attendees and their companies before any meeting using
  real-time web data. Surfaces roles, recent activity, company context, and
  talking points — then maps cross-attendee relationships.

  Use this skill when the user asks to prepare for a meeting, research someone
  they're meeting, or wants context on attendees. Common triggers: "prepare me
  for my meeting", "who am I meeting with", "research this person", "meeting
  prep", "brief me on [person]", "I have a meeting with [person/company]",
  "get me ready for my call", "what should I know about [person]",
  "background on [person] before our meeting", "attendee research".

  Requires the Nimble CLI (nimble search, nimble extract) for live web data.
  Do NOT use for multi-company competitor monitoring (use competitor-intel)
  or single-company deep dives without attendees (use company-deep-dive).
allowed-tools:
  - Bash(nimble:*)
  - Bash(date:*)
  - Bash(cat:*)
  - Bash(mkdir:*)
  - Bash(python3:*)
  - Bash(echo:*)
  - Bash(jq:*)
  - Bash(ls:*)
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
metadata:
  author: Nimbleway
  version: 0.17.0
---

# Meeting Prep

Research-powered meeting preparation with attendee intelligence and company context.

User request: $ARGUMENTS

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight

Run the preflight pattern from `references/nimble-playbook.md` (5 simultaneous Bash
calls: date calc, today, CLI check, profile load, index.md load).

From the results:
- CLI missing or API key unset → `references/profile-and-onboarding.md`, stop
- Profile exists → read `~/.nimble/memory/people/index.md` to identify existing
  person profiles. Load relevant `~/.nimble/memory/people/` files for attendees
  before — skip redundant searches, surface prior meeting notes. Follow
  `[[path/entity]]` cross-references in person files: if an attendee's file links
  to `[[competitors/widgetco]]`, load that competitor file for richer context (e.g.,
  recent intel from competitor-intel runs). Also check `~/.nimble/memory/companies/`
  for cached company research.
  **No same-day report check** — meeting-prep is per-meeting, not per-day. Users
  may prep for multiple meetings in one day. Instead, check entity freshness:
  if a person/company profile was updated within the last 24 hours, offer to reuse
  it: "I have a recent profile for **[Name]** from earlier today. Use it, or refresh?"
- No profile → that's fine. Meeting prep doesn't require onboarding. Proceed to Step 1.

### Step 1: Gather Meeting Context

Parse the meeting details from `$ARGUMENTS` or ask the user.

**Calendar shortcut:** If the user didn't specify attendees and a calendar connector
is available — either a calendar MCP tool (look for `list_events` in the tool list)
or the `gws` CLI (`gws calendar +agenda --today`) — offer to pull today's meetings
so they can pick one. If neither is available, skip this silently.

**If clear** (e.g., "prep me for my meeting with Alex Kim at WidgetCo tomorrow"):
- Extract: attendee name(s), company, meeting date/time (if given)
- Confirm briefly: "Preparing briefing for your meeting with **Alex Kim** at **WidgetCo**..."

**If partial** (e.g., "prep me for my meeting tomorrow"):
- Ask one clarifying question in plain text:
  > "Who are you meeting with? (names, titles, and company if you have them)"

**If just a person** (e.g., "research John Smith"):
- Proceed with the person. Try to infer their company from search results.

**Extract these fields:**

| Field | Required | Source |
|-------|----------|--------|
| Attendee name(s) | Yes | User input or calendar event |
| Company | Preferred | User input or inferred from search |
| Attendee title(s) | Optional | User input or discovered in Step 2 |
| Meeting type | Required | User input, inferred, or asked (discovery, demo, check-in, interview, partnership, internal) |
| Meeting date/time | Optional | User input |
| Additional context | Optional | User notes ("they're evaluating our product", "board member intro") |

**Meeting type detection** — if the user doesn't specify, infer from context clues:

| Signal | Inferred type |
|--------|---------------|
| "prospect", "demo", "sales call" | Sales / discovery |
| "interview", "candidate" | Interview |
| "board", "investor" | Board / investor |
| "partner", "integration" | Partnership |
| "check-in", "sync", "1:1" with colleague | Internal |
| No signal | Ask (see below) |

**If no signal** — don't guess "general external." The meeting type gates whether the
Value Positioning section is generated, so it's worth one question. Use AskUserQuestion:

> **What's the goal of this meeting?**
> - **Sales / discovery** — pitching, demo, exploring fit
> - **Partnership** — integration, co-selling, joint venture
> - **Board / investor** — board meeting, investor update, fundraising
> - **Interview** — evaluating a candidate
> - **General / other** — networking, catch-up, or not sure

Map the answer to the meeting type. If the user picks "General / other", treat as
general external (no value positioning section).

The meeting type shapes the briefing focus — specifically, it determines whether the
Value Positioning section (Step 4.5 + Step 6) is generated. Value positioning activates
for: **sales/discovery, partnership, board/investor**. It is skipped for: **interview,
internal, general external**.

### Step 2: WSA Discovery

Discover available WSAs for each attendee's company domain:

```bash
nimble agent list --search "{company-domain}" --limit 20
```

Run one search per unique company simultaneously. Filter for SERP/PDP WSAs,
prefer `managed_by: "nimble"`, validate with `nimble agent get --template-name {name}`.
Cache discovered names + params. Pass them to attendee agents in Step 3 for richer
data. If no WSAs found, continue with `nimble search` alone.

### Step 3: Per-Attendee Research (sub-agents)

Read `references/attendee-agent-prompt.md` for the full agent prompt template.
Follow the sub-agent spawning rules from `references/nimble-playbook.md`
(bypassPermissions, batch max 4, explicit Bash instruction, fallback on failure).

**Check memory first.** For each attendee, check `~/.nimble/memory/people/[name-slug].md`.
If a profile exists and is < 30 days old, load it as known context and pass it to the
agent so it focuses on what's new. If > 30 days old, run a full refresh.

Spawn `nimble-researcher` agents (`agents/nimble-researcher.md`) with
`mode: "bypassPermissions"`. One agent per attendee. Pass discovered WSA names
from Step 2 to each agent for enrichment.

**Important:** The Nimble API has a 10 req/sec rate limit per API key. With each agent
running 4-5 searches, limit concurrent agents to 2 per batch. For 3+ attendees, batch
in groups of 2.

**Call estimation & Scaled Execution:** Before launching agents, estimate total API
calls: ~5 searches per attendee + ~4 company searches + 3-5 extractions = ~(5 × N) + 9
calls. For 3+ attendees (15+ calls), tell agents to use `extract-batch` for page
extractions instead of individual calls. See the Scaled Execution pattern in
`references/nimble-playbook.md` for tier selection.

**Batch 1** (2 agents simultaneously):
- Attendee 1 research
- Attendee 2 research

**Batch 2** (if needed):
- Attendee 3 research
- Attendee 4 research

**Single attendee optimization:** If only one person, run the searches directly from
the main context instead of spawning an agent — saves overhead.

**Fallback:** If any agent fails or returns empty, run those searches directly from
the main context. Don't leave gaps in the briefing.

### Step 3.5: Gap Check

Before proceeding, verify every attendee has at least a title and company confirmed.

**For any attendee with < 3 meaningful results or "Role Unknown":**
1. Run a `--focus social` fallback search directly (this searches social platform
   people indices and is the most reliable way to find someone):
   `nimble search --query "[Name] [Company]" --focus social --max-results 5 --search-depth lite`
2. If `--focus social` is unavailable, fall back to:
   `nimble search --query "[Name]" --include-domain '["linkedin.com"]' --max-results 5 --search-depth lite`
3. Try name variations: "[First] [Last]", "[Full Name] [Company] [Title if known]"

Do NOT present a briefing with "Role Unknown" — exhaust social search first. If still
nothing after fallbacks, note it honestly: "Limited public presence — could not confirm
role. Consider asking for their LinkedIn URL."

Also collect **LinkedIn profile URLs** for each attendee during this step if not already
found. These are high-value for the final briefing output and Notion distribution.

### Step 4: Company Research

Research the attendees' company for meeting-relevant context. This is a lighter version
of company-deep-dive — focused on what's useful for the conversation, not a full 360°.

**Company name quoting:** If the company name contains common words that cause noisy
results (e.g., "Acme Supply", "Nova Dynamics", "Global Industries"), wrap it in escaped
quotes: `"\"Acme Supply\" news"`. Use `--include-domain '["[domain]"]'` as an alternative anchor.

Make these Bash calls simultaneously:

- `nimble search --query "\"[Company]\" news" --focus news --start-date "[14-days-ago]" --max-results 8 --search-depth lite`
- `nimble search --query "\"[Company]\" product launch OR announcement" --focus news --start-date "[14-days-ago]" --max-results 5 --search-depth lite`
- `nimble search --query "about" --include-domain '["[domain]"]' --max-results 3 --search-depth lite`
- `nimble search --query "\"[Company]\" funding OR raised OR investors" --max-results 5 --search-depth lite`

If your user's company profile exists, also run:
- `nimble search --query "[Company] [UserCompany] OR [user-domain]" --max-results 5 --search-depth lite`

This catches any existing relationship between the two companies — prior partnerships,
mentions, shared investors, or competitive overlap.

**If < 3 results** from the news searches, retry without `--start-date`.

**Date validation:** When including company news in the briefing, verify that the
**event date** (when something actually happened) is recent, not just the article date.
See `references/nimble-playbook.md` → "Signal Date Validation" for details. If a snippet
uses past-tense language like "last year" or "back in Q3", treat it as background context
rather than recent news.

**If the company was already researched** (exists in `~/.nimble/memory/companies/`),
load the existing profile and only run the news search for fresh updates.

### Step 4.5: Value Positioning Research

**Skip this step** if the meeting type is interview, internal, or general external.

This step cross-references what you learned about the attendee's company (Step 4) with
the user's own business profile to find concrete positioning angles. It works best when
`business-profile.json` exists with at least `company.name` and `company.domain`.

**If no profile exists**, skip searches that reference the user's company or competitors
(searches 2, 4, 5) and rely on generic research (searches 1, 3) for positioning insights.
Use any WSAs discovered in Step 2 for richer attendee company data.
The Value Positioning section will be thinner but still useful — pain-to-solution mapping
and tech stack discovery work without a profile.

**Load the user's sales context** from `~/.nimble/business-profile.json`:
- `sales_context.key_differentiators` — what makes the user's product unique
- `sales_context.integration_partners` — tools the user's product connects with
- `sales_context.case_studies` — similar customers and outcomes
- `sales_context.common_objections` — pre-built objection responses
- `competitors` — tracked competitors (check if the attendee's company uses any)

If `sales_context` doesn't exist in the profile, the skill still works — the value
positioning section will rely on web research alone rather than profile-enriched data.
Mention at the end: "Tip: Add sales context to your profile for richer positioning
next time."

**Make these Bash calls simultaneously** (3-5 searches depending on available data):

1. `nimble search --query "\"[AttendeeCompany]\" tech stack OR tools OR platform OR uses" --max-results 5 --search-depth lite`
   → Discover what tools/platforms they use — match against `integration_partners`

2. `nimble search --query "\"[AttendeeCompany]\" [UserCompany] OR [user-domain]" --max-results 5 --search-depth lite`
   → Any existing relationship, mentions, or competitive overlap (skip if already run in Step 3)

3. `nimble search --query "\"[AttendeeCompany]\" challenges OR pain points OR struggling OR migrating" --max-results 5 --search-depth lite`
   → Pain signals to map against user's value props

4. (If `competitors` list exists) `nimble search --query "\"[AttendeeCompany]\" [CompetitorName1] OR [CompetitorName2]" --max-results 5 --search-depth lite`
   → Check if they use a competitor — critical for displacement positioning

5. (If `case_studies` exist with matching industry) `nimble search --query "[UserCompany] [attendee-industry] case study OR customer story" --max-results 5 --search-depth lite`
   → Find published case studies in the attendee's industry to reference

**From the results, extract:**
- Tools/platforms they use (for integration hooks)
- Pain signals or challenges (for value mapping)
- Competitor usage (for displacement angles)
- Industry match to existing case studies (for social proof)

This data feeds directly into the Value Positioning section in Step 5.

### Step 5: Deep Extraction

From Steps 3-4.5, identify the **top 3-5 most informative URLs** across all results.
Prioritize:
- Attendee's own LinkedIn posts, articles, or talks
- Recent company announcements directly relevant to the meeting
- Interviews or profiles of the attendee
- The company's about/team page (if attendee title wasn't found)
- (If value positioning active) Pages revealing their tech stack or tool usage
- (If value positioning active) Articles about their challenges or migration plans

Make one Bash call per URL, all simultaneously:

`nimble extract --url "https://..." --format markdown`

For extraction failures, follow the fallback in `references/nimble-playbook.md`.

**Single attendee + known company:** Skip company extraction, focus on person URLs.
**Multiple attendees:** Prioritize person-specific URLs over company-level ones.

### Step 6: Synthesize Briefing

Structure the output as a meeting prep briefing. Adapt focus based on meeting type.

```
# Meeting Prep: [Company Name]
*[Meeting date/time if known] | Prepared [today's date]*

## Quick Take
[2-3 sentences: who you're meeting, why it matters, and the one thing to know
going in. This is the "read nothing else" paragraph.]

## Attendees

### [Name] — [Title]
**Background:** [Current role, time in position, career trajectory highlights]
**Recent Activity:** [What they've been posting, speaking about, or working on.
  Direct quotes from posts/talks when available.]
**Conversation hooks:** [2-3 specific things to reference — shared connections,
  their recent project, a post they wrote, a talk they gave]
**Notes from prior meetings:** [If exists in memory — what was discussed, their
  preferences, open items. "No prior meetings on file" if none.]

[Repeat for each attendee]

## Relationship Map
[Cross-attendee connections — shared employers, mutual connections, overlapping
  interests, organizational dynamics between attendees. Skip if single attendee.]

## Company Context
- **What they do:** [One line]
- **Size / Stage:** [Employees, funding stage, HQ]
- **Recent news:** [Top 2-3 items, dated with source]
- **Relevant to your meeting:** [How their company context connects to your
  discussion — e.g., recent product launch you might discuss, funding that
  signals growth, leadership change affecting priorities]

## Value Positioning
*[Only for sales/discovery, partnership, and board/investor meetings. Omit entirely
  for interview, internal, and general external meetings.]*

### Value Mapping
[Match their specific needs/pain points to your capabilities. Every mapping must
  be grounded in research from Step 4.5, not generic claims.
  Format: "They [specific finding with source] → Your product [specific capability]"]

### Integration Hooks
[Tools/platforms they use that your product integrates with. Only include
  integrations confirmed from research (their tech stack) AND your profile
  (integration_partners). If no overlap found, say so honestly.]

### Recommended Positioning
[2-3 sentences on how to frame your pitch for THIS specific company and person.
  Consider: their company stage, recent news, the attendee's role and priorities,
  and any competitive displacement opportunity. This is the "elevator pitch
  calibrated to this meeting" paragraph.]

### Reference Customers
[Similar companies from your case_studies that match their industry, size, or
  use case. Include the outcome/metric if available. If no matching case studies,
  omit this subsection rather than forcing a weak match.]

## Talking Points
[3-5 specific, actionable conversation starters grounded in the research.
  Not generic "ask about their priorities" — specific: "Ask about their
  migration from [old tool] to [new tool] that they announced last month."
  When value positioning is active, weave 1-2 positioning angles into the
  talking points naturally — don't make every talking point a sales pitch.]

## Watch Out For
[1-3 things to be aware of — sensitive topics (recent layoffs, bad press),
  potential awkward overlaps, information gaps you couldn't fill.]

## Sources
[Numbered list of key URLs cited in the briefing]
```

**Meeting type adaptations:**

| Type | Emphasis | Add to briefing | Value Positioning |
|------|----------|-----------------|-------------------|
| Sales / discovery | Buyer authority, pain signals, competitive stack | "Qualification signals" section | **Yes** — full section |
| Partnership | Mutual benefit signals, integration opportunities | "Alignment opportunities" section | **Yes** — focus on integration hooks |
| Board / investor | Financial context, market position, portfolio overlap | "Key metrics to reference" section | **Yes** — focus on recommended positioning |
| Interview | Candidate's work history depth, cultural signals | "Assessment angles" section | No |
| Internal | Skip company research, focus on person's recent work | Lighter format, no company section | No |
| General external | Balanced across all dimensions | Standard format above | No |

**Core rules:**
- Every factual claim about an external company or person must have a source URL.
  Data drawn from the user's own business profile (differentiators, integrations,
  case studies) should be attributed to the profile rather than requiring an
  external source.
- Lead with the Quick Take — most readers stop there.
- Talking points must be specific to THIS meeting, grounded in research findings.
  Never generate generic conversation starters.
- Say "no public information found" for a person rather than speculating about their
  role or background.
- If memory has prior meeting notes, surface open items and continuity points
  prominently — this is the highest-value content.
- Value Positioning claims must be grounded in research from Step 4.5. Never
  generate generic positioning advice like "highlight your product's strengths."
  Every value mapping must reference a specific finding about the attendee's
  company paired with a specific capability from the user's profile or research.
- If `sales_context` is missing from the profile, note it once at the end of the
  Value Positioning section: "Tip: Edit your profile at
  `~/.nimble/business-profile.json` to add sales context (differentiators,
  integrations, case studies) for richer positioning next time."

### Step 7: Save to Memory

Make all Write calls simultaneously:

- Report → `~/.nimble/memory/reports/meeting-prep-[company-slug]-[date].md`
- Per attendee → `~/.nimble/memory/people/[name-slug].md`
  (use the format in `references/memory-and-distribution.md`). Add `[[path/entity]]`
  cross-references for the attendee's employer (e.g., `[[competitors/widgetco]]` or
  `[[companies/widgetco]]`) and any other discovered relationships.
- Company profile → update `~/.nimble/memory/companies/[company-slug].md` if new
  company data was found. Add reverse cross-references to the people researched
  (e.g., `[[people/alex-kim]]`).
- Profile → update `last_runs.meeting-prep` in `~/.nimble/business-profile.json`
  (only if profile exists)
- Follow the wiki update pattern from `references/memory-and-distribution.md`: update
  `index.md` rows for all affected entity files, append a `log.md` entry for this run.

The person profile in `people/` should contain structured key facts (role, background,
interests, communication style) that can be loaded by future meeting prep runs.

### Step 8: Share & Distribute

**Always offer distribution — do not skip this step.** Follow
`references/memory-and-distribution.md` for connector detection, sharing flow, and
source links enforcement.

### Step 9: Follow-ups

- **Go deeper** on an attendee → more focused person research
- **Add attendees** → research additional people joining the meeting
- **"What about [topic]?"** → targeted search on specific dimension
- **"Looks good"** → done
- **Sibling skills:** `company-deep-dive` for a full 360 on the company,
  `competitor-intel` to track them as a competitor, `competitor-positioning`
  to compare messaging before a sales meeting

---

## Agent Teams Mode (Dual-Mode)

Check at startup: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`

**Team mode** (flag set): Spawn **teammates** instead of sub-agents. Each teammate
researches one attendee and can message the others when finding cross-connections.

| Teammate | Focus | Cross-checks with |
|----------|-------|-------------------|
| **Attendee 1 researcher** | Full person + company research for attendee 1 | All other teammates (shared employers, connections) |
| **Attendee 2 researcher** | Full person + company research for attendee 2 | All other teammates |
| **[Additional per attendee]** | ... | ... |

How cross-attendee discovery works:
1. Each teammate researches their assigned attendee independently
2. When a teammate discovers a workplace, school, or connection that overlaps with
   another attendee, they send a message to that teammate: "My attendee [Name] worked
   at [Company] from 2019-2022 — did yours overlap?"
3. The receiving teammate checks and responds
4. Lead (you) collects all cross-references and builds the Relationship Map section

This produces higher-quality relationship maps than solo mode because teammates
actively search for connections rather than just comparing results post-hoc.

**Solo mode** (flag not set): Standard sub-agent flow from Step 3.

---

## What This Skill Is NOT

- **Not competitor monitoring** — use `competitor-intel` for tracking competitors
- **Not a company deep dive** — use `company-deep-dive` for research without attendees
- **Not a CRM** — gathers web intelligence, doesn't manage contacts or pipelines
- **Not a calendar app** — reads events for context but doesn't manage them

---

## Error Handling

See `references/nimble-playbook.md` for the standard error table. Skill-specific errors:

- **Person not found:** Try name variations (full, first+last, with company). If still
  nothing: "Couldn't find public info on [Name]. Can you share their title or LinkedIn?"
- **Ambiguous name:** Present top candidates with company/title context and ask.
- **Empty company results:** Note it and focus on attendee-level findings.

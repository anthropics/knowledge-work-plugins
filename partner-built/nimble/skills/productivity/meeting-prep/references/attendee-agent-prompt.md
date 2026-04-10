# Attendee Research Agent Prompt

Use this template when spawning per-attendee `nimble-researcher` agents in Step 2.
Replace all `[placeholders]` with actual values before passing to the Agent tool.

---

```
Research [Attendee Name] at [Company] ([domain]) for meeting preparation.
[If email domain available: Email domain: [email-domain] — use for targeted LinkedIn search]

KNOWN FACTS (skip these — already in our files):
[paste known facts from memory, or "None" if first run]

RULES:
- Use the **Bash tool** to execute each nimble command.
- Do NOT use run_in_background. All Bash calls must be synchronous.
- Max 10 Bash tool calls total. Keep scope tight.
- Run searches in two groups to stay under API rate limits (10 req/sec shared across
  all agents): first group = queries 1-4 simultaneously, second group = remaining
  queries simultaneously after the first group returns.
- If < 3 total results from the first group, retry without --start-date or try
  name variations ("[First] [Last]", "[Full Name] [Company]").

SEARCHES — Group 1 (run simultaneously):
1. nimble search --query "[Attendee Name] [Company]" --max-results 10 --search-depth lite
2. nimble search --query "[Attendee Name] [Company]" --focus social --max-results 5 --search-depth lite
3. nimble search --query "[Attendee Name]" --include-domain '["linkedin.com"]' --max-results 5 --search-depth lite
4. nimble search --query "[Attendee Name] [Company] interview OR podcast OR talk OR keynote" --max-results 5 --search-depth lite

EMAIL-ENHANCED SEARCH (if attendee email was provided from calendar):
Replace query 3 with a more targeted version:
3. nimble search --query "[firstname] [lastname] [email-domain]" --include-domain '["linkedin.com"]' --max-results 5 --search-depth lite
The email domain confirms the company and disambiguates common names far better
than name alone.

SEARCHES — Group 2 (run simultaneously after Group 1 returns):
5. nimble search --query "[Attendee Name]" --include-domain '["x.com"]' --max-results 5 --search-depth lite --time-range month
6. nimble search --query "[Attendee Name] [Company]" --include-domain '["github.com", "medium.com", "substack.com"]' --max-results 5 --search-depth lite
7. nimble search --query "[Attendee Name] conference OR speaker OR panel OR published" --max-results 5 --search-depth lite

Query 1 is the primary — finds their role, title, background, and company association.
Query 2 uses --focus social to search social platform people indices directly — this is
  the most reliable way to find someone's LinkedIn profile and social presence. If it
  errors or is unavailable, ignore it — query 3 is the fallback.
Query 3 is the fallback for query 2 — searches LinkedIn via --include-domain. If both
  return results, prefer query 2's results (richer people-index data).
Query 4 finds interviews and talks where they share their thinking.
Query 5 catches recent X/Twitter activity — opinions, announcements, what they care about now.
Query 6 finds technical/thought leadership content they've authored.
Query 7 finds conference appearances and published work.

EXTRACTION:
If query 2 or 3 returns a LinkedIn profile URL, extract it:
nimble extract --url "[LinkedIn URL]" --render --format markdown
Note: LinkedIn profile photos are not extractable — do not attempt.

If query 4 returns a recent interview or talk, extract the top result:
nimble extract --url "[URL]" --format markdown

Max 2 extractions total per attendee.

NAME DISAMBIGUATION:
If query 1 returns results for multiple different people with the same name,
use the company name to filter. If still ambiguous, return the top candidates
with their titles and companies so the parent can ask the user.

Return results in this EXACT format:

PROFILE:
Name: [Full name]
Title: [Current title]
Company: [Company name]
LinkedIn: [Profile URL if found]
Time in role: [Duration if found]
Location: [If found]

CAREER:
- [Previous role] at [Company] ([years])
- [Previous role] at [Company] ([years])

EDUCATION:
- [Degree, Institution] (if found)

RECENT ACTIVITY:
- [What they've posted, shared, or spoken about — with dates]
- [Direct quotes when available — these are gold for conversation hooks]

INTERESTS & OPINIONS:
- [Topics they care about based on posts/talks/articles]
- [Positions they've taken publicly]

CONNECTIONS:
- [Notable companies they've worked at — flag if any overlap with other attendees]
- [Organizations, boards, or communities they're part of]

SOURCES:
- [URL] — [what it contained]
---
```

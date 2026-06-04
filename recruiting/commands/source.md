---
description: Build a targeted sourcing strategy for a role
argument-hint: "<job title, team, or requirements>"
---

# Source Candidates

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Build a comprehensive sourcing strategy for a specific role. Produces a prioritized channel plan, Boolean search strings, target company lists, and outreach angles.

## Input

The user provides one or more of:
- Job title or role description
- Team and hiring manager context
- Must-have and nice-to-have requirements
- Pasted job description
- Target seniority level or years of experience

If no input is provided, ask: "What role are you sourcing for? Share the title, key requirements, or paste the full JD."

## Workflow

1. **Parse the role** — Extract title, level, core skills, domain, and team context from `$ARGUMENTS`
2. **Define the ideal candidate profile** — Map must-haves vs. nice-to-haves, identify adjacent backgrounds that could transfer
3. **Build Boolean search strings** — Generate 3-5 search strings for LinkedIn, GitHub, Google X-ray, and niche platforms
4. **Identify target companies** — List 10-15 companies likely to employ this talent (competitors, adjacent industries, known talent hubs)
5. **Recommend sourcing channels** — Prioritize channels by expected yield: referrals, LinkedIn, communities, job boards, events, agencies
6. **Draft outreach angles** — Write 2-3 compelling hooks tailored to what would motivate this persona to explore
7. **If ATS connected** — Check for existing candidates in pipeline, silver medalists from past roles, and internal mobility candidates

## Output Structure

```
## Sourcing Strategy: [Role Title]

### Ideal Candidate Profile
- **Must-haves**: [skills, experience]
- **Nice-to-haves**: [bonus qualifications]
- **Adjacent backgrounds**: [transferable profiles]

### Boolean Search Strings
1. **LinkedIn**: `[string]`
2. **GitHub/Stack Overflow**: `[string]`
3. **Google X-ray**: `[string]`

### Target Companies (by tier)
| Tier | Companies | Why |
|------|-----------|-----|
| 1 - Direct competitors | ... | Same domain, likely skills match |
| 2 - Adjacent industry | ... | Transferable skills, different context |
| 3 - Talent hubs | ... | Known for developing this talent |

### Channel Priority
| Channel | Expected yield | Effort | Recommended actions |
|---------|---------------|--------|-------------------|
| Employee referrals | High | Low | [specific steps] |
| LinkedIn outreach | Medium | Medium | [specific steps] |
| ... | ... | ... | ... |

### Outreach Angles
**Angle 1**: [hook based on career growth]
**Angle 2**: [hook based on mission/impact]
**Angle 3**: [hook based on technical challenge]

### Pipeline Check
[If ATS connected: existing candidates, silver medalists, internal mobility]
[If standalone: "Connect your ATS to check for existing candidates"]
```

## With Connectors

- **If ATS connected**: Search for past applicants, silver medalists, and internal candidates before external sourcing
- **If data enrichment connected**: Enrich target company lists with employee counts, growth signals, and funding data
- **If knowledge base connected**: Pull the team's sourcing playbooks, past strategies that worked, and hiring manager preferences

## Tips

- Include the hiring manager's LinkedIn profile or team page for better target company identification
- Mention any compensation constraints upfront so channel recommendations account for budget
- For niche roles, specify the exact technical stack or domain expertise needed

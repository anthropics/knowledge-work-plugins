---
name: sourcing-strategy
description: "Develop sourcing strategies to find and engage candidates, including Boolean search strings, channel recommendations, and passive candidate tactics. Trigger with \"how do I find\", \"source candidates for\", \"Boolean search\", \"where to find\", \"sourcing plan\", \"talent pool\", or when the user discusses finding candidates, building pipelines, or reaching passive talent."
---

# Sourcing Strategy

Comprehensive sourcing methodology for finding and engaging candidates across all channels. Builds targeted strategies based on role characteristics, market conditions, and available resources.

## How It Works

- **Standalone**: Describe the role and get a complete sourcing plan with Boolean strings, channel recommendations, target companies, and outreach angles.
- **With connectors**: Scan the ATS for existing candidates, use data enrichment for contact info and company intelligence, and leverage the CRM for relationship mapping.

## Channel Taxonomy

### Inbound Channels

| Channel | Best for | Expected volume | Quality signal |
|---------|----------|----------------|----------------|
| **Job boards** (Indeed, LinkedIn, etc.) | High-volume roles, active seekers | High | Lower — needs screening |
| **Career page** | Employer brand believers | Medium | Higher — intentional applicants |
| **Referrals** | All roles | Low-Medium | Highest — pre-vetted by trusted source |
| **Inbound from content** | Thought leadership roles | Low | High — engaged with your brand |

### Outbound Channels

| Channel | Best for | Response rate | Effort |
|---------|----------|--------------|--------|
| **LinkedIn outreach** | Most professional roles | 10-25% (if personalized) | Medium |
| **Email outreach** | When you have verified emails | 5-15% | Medium |
| **GitHub/open source** | Engineering roles | 5-10% | High (research-intensive) |
| **Conference/event networking** | Senior/niche roles | High (in-person) | High |
| **Community engagement** | Niche roles, long-term pipeline | Low (short-term) | Low (ongoing) |
| **Twitter/X** | DevRel, marketing, thought leaders | Varies | Low |

### Third-Party Channels

| Channel | When to use | Cost | Speed |
|---------|------------|------|-------|
| **Agency/contingency** | Urgent, senior, or niche roles | 15-25% of salary | Fast |
| **Retained search** | C-suite, confidential searches | 25-35% of salary | Medium |
| **RPO** | High-volume sustained hiring | Monthly retainer | Medium |
| **Freelance sourcers** | Overflow capacity | Per-candidate | Fast |

## Boolean Search Construction

### Core Pattern
```
("[exact title]" OR "[alternate title]" OR "[related title]")
AND ("[key skill]" OR "[alternate term]")
AND ("[company type]" OR "[industry term]")
NOT ("[exclusion]" OR "[exclusion]")
```

### Platform-Specific Syntax

**LinkedIn**: Use the Recruiter or Sales Navigator filters, then refine with:
```
"senior backend engineer" AND (Python OR Go OR Rust) AND (fintech OR payments OR "financial services")
```

**Google X-ray** (search LinkedIn without Recruiter):
```
site:linkedin.com/in "senior backend engineer" (Python OR Go) (fintech OR payments) -jobs -posts
```

**GitHub**:
```
location:"San Francisco" language:Python followers:>50 repos:>20
```
Or search by contribution to specific repos relevant to the tech stack.

**Stack Overflow**:
Search for users with high reputation in relevant tags who list a location.

### Tips for Better Boolean Strings

- Include synonyms and alternate titles ("Software Engineer" OR "Software Developer" OR "SDE")
- Use industry terms, not just skills ("e-commerce" vs. just "Python")
- Exclude common false positives (NOT "recruiter" NOT "sales" for engineering searches)
- Layer in company signals for quality ("Series B" OR "YC" OR specific company names)

## Sourcing Prioritization Framework

For any role, prioritize channels in this order:

1. **Internal mobility** — Does anyone in the company want this role?
2. **Referrals** — Can the hiring manager's network surface candidates?
3. **ATS mining** — Silver medalists, past applicants, nurture pipeline
4. **Targeted outbound** — LinkedIn, GitHub, communities
5. **Job postings** — Optimized JD on the right boards
6. **Agency/contingency** — When speed or specialization justifies the cost

## Output Format

When building a sourcing strategy, produce:

1. **Role profile** — key attributes driving the sourcing approach
2. **Channel plan** — prioritized channels with expected yield and effort
3. **Boolean strings** — 3-5 ready-to-use strings for different platforms
4. **Target companies** — tiered list with reasoning
5. **Outreach approach** — messaging angles and cadence

## Connectors

| Connector | Enhancement |
|-----------|------------|
| ATS | Mine existing pipeline, silver medalists, past applicants |
| Data enrichment | Contact info, company intelligence, candidate research |
| CRM | Relationship mapping, past touchpoints, nurture sequences |
| Email | Send outreach directly |
| Chat | Broadcast sourcing requests to the team for referrals |

---
description: Write or improve a job description
argument-hint: "<role title or existing JD to improve>"
---

# Write Job Description

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Write a compelling, inclusive job description from scratch or improve an existing one. Optimizes for candidate conversion, search discoverability, and legal compliance.

## Input

The user provides one or more of:
- Role title and level
- Hiring manager's description of the role
- Existing JD to improve
- Team context, reporting structure
- Must-have vs. nice-to-have requirements
- Compensation range
- Company info or careers page

If minimal input, ask: "What's the role? Share the title, level, and 2-3 sentences about what this person will do."

## Workflow

1. **Define the role** — Extract or clarify title, level, team, reporting structure, and core purpose from `$ARGUMENTS`
2. **Structure the JD** — Organize into standard sections following inclusive writing best practices
3. **Write compelling copy** — Lead with impact and growth, not just requirements. Use active voice, avoid jargon
4. **Optimize requirements** — Separate must-haves from nice-to-haves. Flag requirements that may unnecessarily narrow the pool (years of experience, specific degrees, unnecessary certifications)
5. **Inclusivity review** — Scan for gendered language, exclusionary phrasing, and unnecessary barriers. Apply research-backed inclusive language guidelines
6. **SEO optimization** — Ensure the title and key terms match how candidates actually search
7. **If knowledge base connected** — Pull company voice guidelines, benefits info, and team descriptions

## Output Structure

```
## [Role Title]
**Team**: [Team] | **Reports to**: [Title] | **Level**: [Level]
**Location**: [Location/Remote policy]

### About the role
[2-3 compelling paragraphs about the role's impact, the team, and why this matters]

### What you'll do
- [Responsibility framed as impact, not task]
- [Responsibility framed as impact, not task]
- [4-6 total responsibilities]

### What we're looking for
**Required**:
- [Skill or experience, without arbitrary year counts]
- [3-5 must-haves]

**Nice to have**:
- [Bonus qualification]
- [2-3 nice-to-haves]

### What we offer
- [Compensation range if provided]
- [Key benefits and perks]
- [Growth and development opportunities]

### About [Company]
[Brief company description focused on mission and culture]

---
**Inclusivity notes**: [Any flags about language, requirements, or barriers that were adjusted]
**SEO notes**: [Title and keyword optimization suggestions]
```

## With Connectors

- **If knowledge base connected**: Pull company boilerplate, benefits details, team descriptions, and brand voice guidelines
- **If ATS connected**: Check for similar open or past roles, pull the intake form, and post the JD directly
- **If HRIS connected**: Verify the approved headcount, compensation band, and reporting structure

## Tips

- Provide the hiring manager's unfiltered description — messy input produces better output than over-polished input
- Mention if this is a backfill vs. new role — it changes the framing
- Include compensation range for significantly better candidate conversion
- For technical roles, specify the actual tech stack rather than generic terms

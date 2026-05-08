---
name: campaign-plan
description: Generate a full campaign brief with objectives, audience, messaging, channel strategy, content calendar, and success metrics. Use when planning a product launch, lead-gen push, or awareness campaign, when you need a week-by-week content calendar with dependencies, or when translating a marketing goal into a structured, executable plan.
argument-hint: "<campaign objective or product>"
---

# Campaign Plan

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Generate a comprehensive marketing campaign brief with objectives, audience, messaging, channel strategy, content calendar, and success metrics.

## Trigger

User runs `/campaign-plan` or asks to plan, design, or build a marketing campaign.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Campaign goal** — the primary objective (e.g., drive signups, increase awareness, launch a product, generate leads, re-engage churned users)

2. **Target audience** — who the campaign is aimed at (demographics, roles, industries, pain points, buying stage)

3. **Timeline** — campaign duration and any fixed dates (launch date, event date, seasonal deadline)

4. **Budget range** — approximate budget or budget tier (optional; if not provided, generate a channel-agnostic plan and note where budget allocation would matter)

5. **Additional context** (optional):
   - Product or service being promoted
   - Key differentiators or value propositions
   - Previous campaign performance or learnings
   - Brand guidelines or constraints
   - Geographic focus

## Campaign Brief Structure

Generate a campaign brief with the following sections:

### 1. Campaign Overview
- Campaign name suggestion
- One-sentence campaign summary
- Primary objective with a specific, measurable goal
- Secondary objectives (if applicable)

### 2. Target Audience
- Primary audience segment with description
- Secondary audience segment (if applicable)
- Audience pain points and motivations
- Where they spend time (channels, communities, publications)
- Buying stage alignment (awareness, consideration, decision)

### 3. Key Messages
- Core campaign message (one sentence)
- 3-4 supporting messages tailored to audience pain points
- Message variations by channel (if different tones are needed)
- Proof points or evidence to support each message

### 4. Channel Strategy
Recommend channels based on audience and goal. For each channel, include:
- Why this channel fits the audience and objective
- Content format recommendations
- Estimated effort level (low, medium, high)
- Budget allocation suggestion (if budget was provided)

Consider channels from:
- Owned: blog, email, website, social media profiles
- Earned: PR, influencer partnerships, guest posts, community engagement
- Paid: search ads, social ads, display, sponsored content, events

### 5. Content Calendar
Create a week-by-week (or day-by-day for short campaigns) content calendar:
- What content to produce each week
- Which channel each piece targets
- Key milestones and deadlines
- Dependencies between pieces (e.g., "landing page must be live before paid ads launch")

Format as a table:

| Week | Content Piece | Channel | Owner/Notes | Status |
|------|--------------|---------|-------------|--------|

### 6. Content Pieces Needed
List every content asset required for the campaign:
- Asset name and type (blog post, email, social post, ad creative, landing page, etc.)
- Brief description of what it should contain
- Priority (must-have vs. nice-to-have)
- Suggested timeline for creation

### 7. Success Metrics
Define KPIs aligned to the campaign objective:
- Primary KPI with target number
- Secondary KPIs (3-5)
- How each metric will be tracked
- Reporting cadence recommendation

If ~~product analytics is connected, reference any available historical performance benchmarks to inform targets.

### 8. Budget Allocation (if budget provided)
- Breakdown by channel or activity
- Production costs vs. distribution costs
- Contingency recommendation (typically 10-15%)

### 9. Risks and Mitigations
- 2-3 potential risks (timeline, audience mismatch, channel underperformance)
- Mitigation strategy for each

### 10. Next Steps
- Immediate action items to kick off the campaign
- Stakeholder approvals needed
- Key decision points

## Planning Reference

### Campaign Framework: Objective, Audience, Message, Channel, Measure

Every campaign should be built on this five-part framework:

#### Objective
Define what success looks like before planning anything else.

- **Awareness**: increase brand or product visibility (measured by reach, impressions, share of voice)
- **Consideration**: drive engagement and education (measured by content engagement, email signups, webinar attendance)
- **Conversion**: generate leads or sales (measured by signups, demos, purchases, pipeline)
- **Retention**: re-engage existing customers (measured by churn reduction, upsell, NPS)
- **Advocacy**: turn customers into promoters (measured by referrals, reviews, UGC)

Good objectives are SMART: Specific, Measurable, Achievable, Relevant, Time-bound.

Example: "Generate 200 marketing qualified leads from mid-market SaaS companies in North America within 6 weeks of campaign launch."

#### Audience
Define who you are trying to reach with enough specificity to guide messaging and channel decisions.

- **Demographics**: role/title, seniority, company size, industry
- **Psychographics**: motivations, pain points, goals, objections
- **Behavioral**: where they consume content, how they buy, what they have engaged with before
- **Buying stage**: are they unaware of the problem, researching solutions, or ready to buy?

Create a brief audience profile (not a full persona) for campaign planning:
> "[Role] at [company type] who is struggling with [pain point] and looking for [desired outcome]. They typically discover solutions through [channels] and care most about [priorities]."

#### Message
Craft the core message and supporting points that will resonate with the audience.

- **Core message**: one sentence that captures what you want the audience to think, feel, or do
- **Supporting messages**: 3-4 points that provide evidence, address objections, or elaborate on benefits
- **Proof points**: data, case studies, testimonials, or third-party validation for each supporting message
- **Differentiation**: what makes your offering different from alternatives (including doing nothing)

Message hierarchy:
1. Why should I care? (addresses the pain point or opportunity)
2. What is the solution? (positions your offering)
3. Why you? (differentiates from alternatives)
4. What should I do? (call to action)

#### Channel
Select channels based on where your audience is, not where you are most comfortable. See the Channel Selection Guide below.

#### Measure
Define how you will know the campaign worked. See Success Metrics by Campaign Type below.

### Channel Selection Guide

#### Owned Channels

| Channel | Best For | Typical Metrics | Effort |
|---------|----------|----------------|--------|
| Blog/Website | SEO, thought leadership, education | Traffic, time on page, conversions | Medium |
| Email | Nurture, retention, announcements | Open rate, CTR, conversions | Low-Medium |
| Social (organic) | Awareness, community, brand building | Engagement, reach, follower growth | Medium |
| Webinars | Education, lead gen, product demos | Registrations, attendance, pipeline | High |
| Podcast | Thought leadership, brand awareness | Downloads, subscriber growth | High |

#### Earned Channels

| Channel | Best For | Typical Metrics | Effort |
|---------|----------|----------------|--------|
| PR/Media | Awareness, credibility, launches | Coverage, share of voice, referral traffic | High |
| Guest content | Audience expansion, SEO, credibility | Referral traffic, backlinks | Medium |
| Influencer/Partner | Audience expansion, trust | Reach, engagement, referral conversions | Medium-High |
| Community | Awareness, trust, feedback | Mentions, engagement, referral traffic | Medium |
| Reviews/Ratings | Credibility, SEO, consideration | Review volume, rating, conversion lift | Low-Medium |

#### Paid Channels

| Channel | Best For | Typical Metrics | Effort |
|---------|----------|----------------|--------|
| Search ads (SEM) | High-intent lead capture | CPC, CTR, conversion rate, CPA | Medium |
| Social ads | Awareness, retargeting, lead gen | CPM, CPC, CTR, CPA, ROAS | Medium |
| Display/Programmatic | Awareness, retargeting | Impressions, CPM, view-through conversions | Low-Medium |
| Sponsored content | Thought leadership, lead gen | Engagement, leads, cost per lead | Medium |
| Events/Sponsorships | Relationship building, brand | Leads, meetings, pipeline influenced | High |

#### Channel Selection Criteria
When choosing channels, consider:
- Where does your target audience spend time?
- What is the buying stage you are targeting? (awareness channels vs. conversion channels)
- What is your budget? (paid channels require spend; owned/earned require time)
- What content assets do you already have or can you produce?
- What has worked in the past? (reference historical data if available)

### Content Calendar Creation

#### Calendar Planning Process
1. **Start with milestones**: campaign launch, event dates, product releases, seasonal moments
2. **Work backward**: what needs to be live and when? What is the production lead time?
3. **Map content to funnel stages**: ensure coverage across awareness, consideration, and conversion
4. **Batch by theme**: group related content pieces into weekly or bi-weekly themes
5. **Balance channels**: do not over-index on one channel; ensure the audience sees the campaign across touchpoints
6. **Build in flexibility**: leave 20% of calendar slots open for reactive or opportunistic content

#### Content Cadence Guidelines
- **Blog**: 1-4 posts per week depending on team size and goals
- **Email newsletter**: weekly or bi-weekly for most audiences
- **Social media**: 3-7 posts per week per platform (varies by platform)
- **Paid campaigns**: continuous during campaign window with creative refreshes every 2-4 weeks
- **Webinars**: monthly or quarterly depending on resources

#### Production Timeline Benchmarks
- Blog post: 3-5 business days (research, draft, review, publish)
- Email campaign: 2-3 business days (copy, design, test, send)
- Social media posts: 1-2 business days (draft, design, schedule)
- Landing page: 5-7 business days (copy, design, development, QA)
- Video content: 2-4 weeks (script, production, editing)
- Ebook/whitepaper: 2-4 weeks (outline, draft, design, review)

### Budget Allocation Approaches

#### Percentage of Revenue Method
- Industry benchmark: 5-15% of revenue for marketing, with B2B typically at 5-10% and B2C at 10-15%
- Startups and growth-stage companies often invest 15-25% of revenue in marketing
- Within the marketing budget, allocate across brand (long-term) and performance (short-term)

#### Channel Allocation Framework
A common starting framework (adjust based on goals and historical data):

| Category | Percentage of Budget | Examples |
|----------|---------------------|----------|
| Paid acquisition | 30-40% | Search ads, social ads, display |
| Content production | 20-30% | Blog, video, design, ebooks |
| Events and sponsorships | 10-20% | Conferences, webinars, meetups |
| Tools and technology | 10-15% | Analytics, automation, CRM |
| Testing and experimentation | 5-10% | New channels, A/B tests, pilots |

#### Budget Optimization Principles
- Start with your highest-confidence channel and allocate 60-70% of paid budget there
- Reserve 15-20% for testing new channels or tactics
- Shift budget monthly based on performance data (do not set and forget)
- Account for production costs, not just media spend
- Include a 10-15% contingency for unexpected opportunities or overruns

### Success Metrics by Campaign Type

#### Awareness Campaign
| Metric | What It Measures |
|--------|-----------------|
| Reach/Impressions | How many people saw the campaign |
| Brand mention volume | Increase in brand conversations |
| Share of voice | Your mentions vs. competitors |
| Direct traffic | People coming to your site unprompted |
| Social follower growth | Audience building |

#### Lead Generation Campaign
| Metric | What It Measures |
|--------|-----------------|
| Total leads | Volume of new contacts |
| Marketing qualified leads (MQLs) | Leads meeting quality threshold |
| Cost per lead (CPL) | Efficiency of spend |
| Lead-to-MQL conversion rate | Quality of leads generated |
| Pipeline influenced | Revenue opportunity created |

#### Product Launch Campaign
| Metric | What It Measures |
|--------|-----------------|
| Signups or trials | Adoption of new product |
| Activation rate | Users who complete key first action |
| Media coverage | Earned media hits |
| Social buzz | Mentions, shares, engagement spike |
| Feature adoption | Usage of specific launched features |

#### Retention/Engagement Campaign
| Metric | What It Measures |
|--------|-----------------|
| Churn rate change | Customer retention improvement |
| Engagement rate | Interactions with campaign content |
| NPS or CSAT change | Satisfaction improvement |
| Upsell/cross-sell revenue | Expansion revenue |
| Feature adoption | Usage of promoted features |

#### Event/Webinar Campaign
| Metric | What It Measures |
|--------|-----------------|
| Registrations | Interest generated |
| Attendance rate | Conversion from registration |
| Engagement during event | Questions, polls, chat activity |
| Post-event conversions | Leads or pipeline from attendees |
| Content repurposing reach | Downstream audience from recordings |

## Output

Present the full campaign brief with clear headings and formatting. After the brief, ask:

"Would you like me to:
- Dive deeper into any section?
- Draft specific content pieces from the calendar?
- Create a competitive analysis to inform the messaging?
- Adjust the plan for a different budget or timeline?"

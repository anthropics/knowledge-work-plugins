---
name: performance-report
description: Build a marketing performance report with key metrics, trend analysis, wins and misses, and prioritized optimization recommendations. Use when wrapping a campaign, when preparing weekly, monthly, or quarterly channel summaries for stakeholders, or when you need data translated into an executive summary with next-period priorities.
argument-hint: "<time period or campaign>"
---

# Performance Report

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Generate a marketing performance report with key metrics, trend analysis, insights, and optimization recommendations.

## Trigger

User runs `/performance-report` or asks for a marketing report, performance analysis, campaign results, or metrics summary.

## Inputs

1. **Report type** — determine which type of report the user needs:
   - **Campaign report** — performance of a specific campaign
   - **Channel report** — performance across a specific channel (email, social, paid, SEO, etc.)
   - **Content performance** — how content pieces are performing
   - **Overall marketing report** — cross-channel summary (weekly, monthly, quarterly)
   - **Custom** — user-defined scope

2. **Time period** — the reporting window (last week, last month, last quarter, custom date range)

3. **Data source**:
   - If ~~marketing analytics is connected, discover what accounts and platforms are available, then pull performance data automatically
   - If ~~product analytics is connected: pull performance data automatically
   - If not connected: ask the user to provide metrics. Prompt with: "Please paste or share your performance data. I can work with spreadsheets, CSV data, dashboard screenshots described in text, or just the key numbers."

4. **Comparison period** (optional) — prior period or year-over-year for trend context

5. **Stakeholder audience** (optional) — who will read this report (executive summary style vs. detailed analyst view)

## Report Structure

### 1. Executive Summary
- 2-3 sentence overview of performance in the period
- Headline metric with trend direction (up/down/flat vs. prior period)
- One key win and one area of concern

### 2. Key Metrics Dashboard

Present core metrics in a summary table:

| Metric | This Period | Prior Period | Change | Target | Status |
|--------|------------|--------------|--------|--------|--------|

Status indicators:
- On track (meeting or exceeding target)
- At risk (below target but within acceptable range)
- Off track (significantly below target)

#### Metrics by Report Type

**Campaign Report:**
- Impressions and reach
- Click-through rate (CTR)
- Conversion rate
- Cost per acquisition (CPA)
- Return on ad spend (ROAS) or ROI
- Total conversions/signups/leads

**Channel Report (Email):**
- Emails sent, delivered, bounced
- Open rate
- Click-through rate
- Unsubscribe rate
- Conversion rate

**Channel Report (Social):**
- Impressions and reach
- Engagement rate (likes, comments, shares)
- Follower growth
- Click-through rate
- Top-performing posts

**Channel Report (Paid):**
- Spend
- Impressions and clicks
- CTR
- CPC and CPM
- Conversions and CPA
- ROAS

**Channel Report (SEO/Organic):**
- Organic sessions
- Keyword rankings (movement)
- Pages indexed
- Backlinks acquired
- Top-performing pages

**Content Performance:**
- Pageviews and unique visitors
- Time on page
- Bounce rate
- Social shares
- Conversions attributed to content
- Top and bottom performers

**Overall Marketing Report:**
- Total leads generated
- Marketing qualified leads (MQLs)
- Pipeline contribution
- Customer acquisition cost (CAC)
- Channel-by-channel summary

### 3. Trend Analysis
- Performance trend over the period (week-over-week or month-over-month)
- Notable inflection points and what caused them
- Seasonal or cyclical patterns observed
- Comparison to benchmarks or targets

### 4. What Worked
- Top 3-5 wins with specific data
- Why these performed well (hypothesis)
- How to replicate or scale

### 5. What Needs Improvement
- Bottom 3-5 performers with specific data
- Hypotheses for underperformance
- Recommended fixes

### 6. Insights and Observations
- Patterns in the data that are not obvious from the metrics alone
- Audience behavior insights
- Content or creative themes that resonated
- External factors that may have influenced performance (seasonality, news, competitive moves)

### 7. Recommendations
For each recommendation:
- What to do
- Why (linked to a specific insight from the data)
- Expected impact (high, medium, low)
- Effort to implement (high, medium, low)
- Priority (immediate, next sprint, next quarter)

Prioritize recommendations in a 2x2 matrix format:

| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Do first | Plan for next sprint |
| **Low Impact** | Do if time allows | Deprioritize |

### 8. Next Period Focus
- Top 3 priorities for the upcoming period
- Tests or experiments to run
- Targets for key metrics

## Metric Definitions and Benchmarks

### Email Marketing

| Metric | Definition | Benchmark Range | What It Tells You |
|--------|-----------|----------------|-------------------|
| Delivery rate | Emails delivered / emails sent | 95-99% | List health and sender reputation |
| Open rate | Unique opens / emails delivered | 15-30% | Subject line and sender effectiveness |
| Click-through rate (CTR) | Unique clicks / emails delivered | 2-5% | Content relevance and CTA effectiveness |
| Click-to-open rate (CTOR) | Unique clicks / unique opens | 10-20% | Email content quality (for those who opened) |
| Unsubscribe rate | Unsubscribes / emails delivered | <0.5% | Content-audience fit and frequency tolerance |
| Bounce rate | Bounces / emails sent | <2% | List quality and data hygiene |
| Conversion rate | Conversions / emails delivered | 1-5% | End-to-end email effectiveness |
| Revenue per email | Total revenue / emails sent | Varies | Direct revenue attribution |
| List growth rate | (New subscribers - unsubscribes) / total list | 2-5% monthly | Audience building health |

### Social Media

| Metric | Definition | What It Tells You |
|--------|-----------|-------------------|
| Impressions | Number of times content was displayed | Content distribution and reach |
| Reach | Number of unique users who saw content | Audience breadth |
| Engagement rate | (Likes + comments + shares) / reach | Content resonance |
| Click-through rate | Link clicks / impressions | Traffic driving effectiveness |
| Follower growth rate | Net new followers / total followers per period | Audience building |
| Share/Repost rate | Shares / reach | Content virality and advocacy |
| Video view rate | Views / impressions | Video content hook effectiveness |
| Video completion rate | Completed views / total views | Video content quality and length fit |
| Social share of voice | Your mentions / total category mentions | Brand visibility vs. competitors |

### Paid Advertising (Search and Social)

| Metric | Definition | What It Tells You |
|--------|-----------|-------------------|
| Impressions | Times ad was shown | Budget utilization and targeting breadth |
| Click-through rate (CTR) | Clicks / impressions | Ad creative and targeting relevance |
| Cost per click (CPC) | Total spend / clicks | Cost efficiency of traffic generation |
| Cost per mille (CPM) | Cost per 1,000 impressions | Awareness cost efficiency |
| Conversion rate | Conversions / clicks | Landing page and offer effectiveness |
| Cost per acquisition (CPA) | Total spend / conversions | Full-funnel cost efficiency |
| Return on ad spend (ROAS) | Revenue / ad spend | Revenue generation efficiency |
| Quality Score (search) | Google's relevance rating (1-10) | Ad-keyword-landing page alignment |
| Frequency | Average times a user sees the ad | Ad fatigue risk |
| View-through conversions | Conversions from users who saw but did not click | Display/awareness campaign influence |

### SEO / Organic Search

| Metric | Definition | What It Tells You |
|--------|-----------|-------------------|
| Organic sessions | Visits from organic search | SEO effectiveness and content reach |
| Keyword rankings | Position for target keywords | Search visibility |
| Organic CTR | Clicks / impressions in search results | Title and meta description effectiveness |
| Pages indexed | Number of pages in search index | Crawlability and site health |
| Domain authority | Third-party authority score | Overall site strength |
| Backlinks | Number of external sites linking to you | Content authority and off-page SEO |
| Page load speed | Time to interactive | User experience and ranking factor |
| Organic conversion rate | Organic conversions / organic sessions | Content quality and intent alignment |
| Top entry pages | Most-visited pages from organic search | Content driving the most organic traffic |

### Content Marketing

| Metric | Definition | What It Tells You |
|--------|-----------|-------------------|
| Pageviews | Total views of content pages | Content reach and distribution |
| Unique visitors | Distinct users viewing content | Audience size |
| Average time on page | Time spent on content pages | Content engagement and depth |
| Bounce rate | Single-page sessions / total sessions | Content-audience fit and UX |
| Scroll depth | How far users scroll on a page | Content engagement through the piece |
| Social shares | Times content was shared on social | Content resonance and virality |
| Backlinks earned | External links to content | Content authority and SEO value |
| Lead generation | Leads attributed to content | Content conversion effectiveness |
| Content ROI | Revenue attributed / content production cost | Overall content investment return |

### Overall Marketing / Pipeline

| Metric | Definition | What It Tells You |
|--------|-----------|-------------------|
| Marketing qualified leads (MQLs) | Leads meeting marketing qualification criteria | Top-of-funnel effectiveness |
| Sales qualified leads (SQLs) | MQLs accepted by sales | Lead quality |
| MQL to SQL conversion rate | SQLs / MQLs | Marketing-sales alignment and lead quality |
| Pipeline generated | Dollar value of opportunities created | Marketing impact on revenue |
| Pipeline velocity | How fast deals move through pipeline | Campaign urgency and quality |
| Customer acquisition cost (CAC) | Total marketing + sales cost / new customers | Efficiency of customer acquisition |
| CAC payback period | Months to recover CAC from revenue | Unit economics health |
| Marketing-sourced revenue | Revenue from marketing-originated deals | Direct marketing contribution |
| Marketing-influenced revenue | Revenue from deals where marketing touched | Broader marketing impact |

## Reporting Templates by Cadence

### Weekly Marketing Report
Quick-scan format for team standups:
- **Top 3 metrics** with week-over-week change
- **What worked** this week (1-2 bullet points with data)
- **What needs attention** (1-2 bullet points with data)
- **This week's priorities** (3-5 action items)

### Monthly Marketing Report
Standard stakeholder report:
1. Executive summary (3-5 sentences)
2. Key metrics dashboard (table with MoM and target comparison)
3. Channel-by-channel performance summary
4. Campaign highlights and results
5. What worked and what did not (with hypotheses)
6. Recommendations and next month priorities
7. Budget spend vs. plan

### Quarterly Business Review (QBR)
Strategic review for leadership:
1. Quarter performance vs. goals
2. Year-to-date trajectory
3. Channel ROI analysis
4. Campaign performance summary
5. Competitive and market observations
6. Strategic recommendations for next quarter
7. Budget request and allocation plan
8. Key experiments and learnings

### Dashboard Design Principles
- Lead with the metrics that map to business objectives (not vanity metrics)
- Show trends over time, not just point-in-time snapshots
- Include comparison context: prior period, target, benchmark
- Use consistent color coding: green (on track), yellow (at risk), red (off track)
- Group metrics by funnel stage or business question
- Keep dashboards to one page/screen — detail goes in appendix
- Update cadence should match decision cadence (real-time for paid, weekly for content)

## Trend Analysis and Forecasting

### Trend Identification
When analyzing performance data, look for:

1. **Directional trends**: is the metric consistently going up, down, or flat over 4+ periods?
2. **Inflection points**: where did performance change direction and what happened then?
3. **Seasonality**: are there predictable patterns by day of week, month, or quarter?
4. **Anomalies**: one-time spikes or drops — what caused them and are they repeatable?
5. **Leading indicators**: which metrics change first and predict future outcomes?

### Trend Analysis Process
1. Chart the metric over time (at least 8-12 data points for meaningful trends)
2. Identify the overall direction (upward, downward, flat, cyclical)
3. Calculate the rate of change (is it accelerating or decelerating?)
4. Overlay key events (campaigns launched, product changes, market events)
5. Compare to benchmarks or targets
6. Identify correlations with other metrics
7. Form hypotheses about causation (and plan tests to validate)

### Simple Forecasting Approaches
- **Linear projection**: extend the current trend line forward (useful for stable metrics)
- **Moving average**: smooth out noise by averaging the last 3-6 periods
- **Year-over-year comparison**: use last year's pattern as a baseline, adjusted for growth rate
- **Funnel math**: forecast outputs from inputs (e.g., if we generate X leads at Y conversion rate, we will get Z customers)
- **Scenario modeling**: create best case, expected case, and worst case projections

### Forecasting Caveats
- Short-term forecasts (1-3 months) are more reliable than long-term
- Forecasts based on fewer than 12 data points should be flagged as low confidence
- External factors (market shifts, competitive moves, economic changes) can invalidate trend-based forecasts
- Always present forecasts as ranges, not exact numbers

## Attribution Modeling Basics

### What Is Attribution?
Attribution determines which marketing touchpoints get credit for a conversion. This matters because buyers typically interact with multiple channels before converting.

### Common Attribution Models

| Model | How It Works | Best For | Limitation |
|-------|-------------|----------|------------|
| Last touch | 100% credit to last interaction before conversion | Understanding final conversion triggers | Ignores awareness and nurture |
| First touch | 100% credit to first interaction | Understanding top-of-funnel effectiveness | Ignores nurture and conversion drivers |
| Linear | Equal credit to all touchpoints | Fair representation of all channels | Does not reflect relative impact |
| Time decay | More credit to touchpoints closer to conversion | Balanced view favoring recent interactions | May undervalue awareness |
| Position-based (U-shaped) | 40% first, 40% last, 20% split among middle | Valuing both discovery and conversion | Somewhat arbitrary weighting |
| Data-driven | Algorithmic credit based on conversion patterns | Most accurate representation | Requires significant data volume |

### Attribution Practical Guidance
- Start with last-touch attribution if you have no model in place — it is the simplest and most actionable
- Compare first-touch and last-touch to understand which channels drive awareness vs. conversion
- Use position-based (U-shaped) as a reasonable middle ground for most B2B companies
- Data-driven attribution requires high conversion volume to be statistically meaningful
- No model is perfect — use attribution directionally, not as absolute truth
- Multi-touch attribution is better than single-touch, but any model is better than none

### Attribution Pitfalls
- Do not optimize one channel in isolation based on single-touch attribution
- Awareness channels (display, social, PR) will always look bad in last-touch models
- Conversion channels (search, retargeting) will always look bad in first-touch models
- Self-reported attribution ("how did you hear about us?") provides useful qualitative color but is unreliable as quantitative data
- Cross-device and cross-channel tracking gaps mean attribution data is always incomplete

## Optimization Recommendations Framework

### Optimization Process
1. **Identify**: which metrics are underperforming vs. target or benchmark?
2. **Diagnose**: where in the funnel is the problem? (impressions, clicks, conversions, retention)
3. **Hypothesize**: what is causing the underperformance? (audience, message, creative, offer, timing, technical)
4. **Prioritize**: which fixes will have the biggest impact with the least effort?
5. **Test**: design an experiment to validate the hypothesis
6. **Measure**: did the change improve the metric?
7. **Scale or iterate**: roll out wins broadly; iterate on inconclusive or failed tests

### Optimization Levers by Funnel Stage

| Funnel Stage | Problem Signal | Optimization Levers |
|-------------|---------------|---------------------|
| Awareness | Low impressions, low reach | Budget, targeting, channel mix, creative format |
| Interest | Low CTR, low engagement | Ad creative, headlines, content hooks, audience targeting |
| Consideration | High bounce rate, low time on page | Landing page content, page speed, content relevance, UX |
| Conversion | Low conversion rate | Offer, CTA, form length, trust signals, page layout |
| Retention | High churn, low repeat engagement | Onboarding, email nurture, product experience, support |

### Testing Best Practices
- Test one variable at a time for clean results
- Define the success metric before launching the test
- Calculate required sample size before starting (do not end tests early)
- Run tests for a minimum of one full business cycle (typically one week for B2B)
- Document all tests and results, regardless of outcome
- Share learnings across the team — failed tests are valuable information
- A test that confirms the status quo is not a failure — it builds confidence in your current approach

### Continuous Optimization Cadence
- **Daily**: monitor paid campaigns for budget pacing, anomalies, and disapproved ads
- **Weekly**: review channel performance, pause underperformers, scale winners
- **Bi-weekly**: refresh ad creative and test new variants
- **Monthly**: full performance review, identify new optimization opportunities, update forecasts
- **Quarterly**: strategic review of channel mix, budget allocation, and targeting strategy

## Output Formatting

- Use tables for data presentation
- Bold key numbers and trends
- Keep the executive summary concise (suitable for forwarding to leadership)
- Include a "detailed appendix" section for granular data if the user provided a lot of metrics

## After the Report

Ask: "Would you like me to:
- Create a slide-ready summary of these results?
- Draft a stakeholder email with the key takeaways?
- Dive deeper into any specific metric or channel?
- Set up a reporting template you can reuse next period?"

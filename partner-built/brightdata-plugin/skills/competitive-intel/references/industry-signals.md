# Industry Signal Interpretation Guide

This reference helps you interpret raw data collected via `bdata` as strategic intelligence signals. Raw data is just numbers and text — the value is in what it *means*.

## Pricing Signals

### What Pricing Changes Reveal

| Signal | What You Observe | What It Likely Means |
|--------|-----------------|---------------------|
| Price increase | Higher prices than last known / industry average | Confidence in product value, moving upmarket, or cost pressure |
| Price decrease | Lower prices, new budget tiers | Competitive pressure, pivot to volume/SMB, struggling with enterprise sales |
| New free tier | Introduced a free plan | Land-and-expand strategy, competing with open-source, or new market entry |
| Removed free tier | Free plan eliminated | Monetization pressure, focusing on qualified leads, or mature product stage |
| Usage-based pricing | Per-API-call, per-seat, per-GB model | Targeting scalability-conscious buyers, aligning revenue with value delivery |
| Enterprise "Contact Us" | No public pricing for top tier | Targeting large deals, high ACV strategy, or hiding pricing from competitors |
| Annual discount > 30% | Big gap between monthly and annual | Cash flow priority, high churn rate they're trying to mitigate |
| Feature unbundling | Features previously included now sold as add-ons | Monetization pressure, or creating entry-level price point |

### Pricing Model Implications

| Model | Favors | Challenges | Strategic Signal |
|-------|--------|-----------|-----------------|
| Per-seat | Predictable revenue, easy to understand | Penalizes collaboration, invites seat-sharing hacks | B2B focus, enterprise-friendly |
| Usage-based | Scales with customer value, low entry barrier | Unpredictable bills, hard to forecast | Developer/API-first, PLG strategy |
| Flat-rate | Simple, no surprise bills | Doesn't scale with value, hard to monetize power users | SMB-focused, simplicity positioning |
| Freemium | Massive top-of-funnel, viral potential | Conversion challenges, support costs | Growth-stage, PLG, market share grab |
| Enterprise-only | High ACV, dedicated support | Long sales cycles, small customer base | Mature, niche, or complex product |

---

## Hiring Signals

### Role Distribution Analysis

| Department Emphasis | What It Signals | Confidence Level |
|--------------------|----------------|-----------------|
| **Engineering-heavy** (>50% of roles) | Product investment phase, building new features or rebuilding platform | High |
| **Sales-heavy** (>40% of roles) | Revenue scaling phase, product is mature enough to sell aggressively | High |
| **Marketing-heavy** (>30% of roles) | Brand awareness push, entering new markets, or pre-IPO visibility | Medium |
| **Customer Success heavy** | Churn problem, or moving upmarket where CS is expected | Medium |
| **Data/ML roles emerging** | AI/ML product features coming, or building data moats | High |
| **Security/Compliance roles** | Enterprise push, regulated industry entry, or post-incident response | High |
| **DevRel/Developer Advocate** | Developer ecosystem play, API/platform strategy | High |
| **Balanced across all** | Mature company in steady growth | Medium |

### Technology Signals from Job Descriptions

| Tech Mentioned | Strategic Signal |
|---------------|-----------------|
| Kubernetes, Terraform, cloud-native | Scaling infrastructure, multi-cloud strategy |
| React/Next.js, design systems | Frontend modernization, UX investment |
| Rust, Go (replacing Python/Node) | Performance-critical features, infrastructure rewrite |
| LLM, RAG, vector databases | AI features coming, likely within 3-6 months |
| Kafka, Flink, streaming | Real-time data processing, event-driven architecture |
| SOC2, HIPAA, FedRAMP | Enterprise compliance push, government/healthcare market entry |
| GraphQL, API gateway | Platform/ecosystem strategy, third-party integrations |
| Mobile (iOS/Android native) | Mobile-first or mobile expansion play |

### Geographic Signals

| Hiring Location | Strategic Signal |
|----------------|-----------------|
| New office in EU | GDPR compliance push, European market expansion |
| Remote roles in APAC | Asia-Pacific market entry |
| Engineering hub in lower-cost market | Cost optimization, scaling engineering capacity |
| Sales team in new city/country | Direct market entry into that geography |
| No remote roles (return to office) | Culture choice, or need for high-collaboration work (security, hardware) |

### Seniority Signals

| Pattern | Interpretation |
|---------|---------------|
| Many VP/Director hires | New teams being formed, new business units, strategic pivots |
| Mostly Senior/Staff engineers | Deep technical work, complex problems, platform rebuilds |
| Many junior/entry-level | Scaling existing teams, well-defined processes, growth mode |
| CTO/CPO/CMO hire | Leadership change, strategic pivot, pre-IPO or post-funding professionalization |
| "Founding" roles (Founding Engineer, etc.) | New initiative, internal startup, or early-stage expansion area |

---

## Content & SEO Signals

### Publishing Frequency Signals

| Pattern | What It Means |
|---------|-------------|
| Daily publishing | Aggressive SEO play, content-led growth, likely has dedicated content team |
| Weekly publishing | Healthy content strategy, sustainable investment |
| Monthly or less | Content is not a growth lever, or team is resource-constrained |
| Burst then silence | Had a content push but didn't sustain it (budget cut? team change?) |
| Increasing frequency | New investment in content marketing |
| Decreasing frequency | Cutting content budget, pivoting to other channels |

### Topic Shift Signals

| What Changes | What It Means |
|-------------|-------------|
| New topic cluster appears | Product expanding into that area, or targeting new buyer persona |
| Technical → business content | Moving upmarket, targeting decision-makers instead of practitioners |
| Product → thought leadership | Brand building, pre-IPO positioning, or competing for mindshare |
| How-to → comparison content | Getting more competitive, actively fighting for buyer attention |
| Competitor mention articles | Direct competitive play, feeling market pressure |

### SERP Signals

| What You See | What It Means |
|-------------|-------------|
| Competitor ranks #1 for your target keywords | They've invested heavily in this topic; you need differentiated content to compete |
| No one ranks well for a keyword | Content gap opportunity — first mover advantage available |
| Competitor dominates 5+ keywords in a cluster | They own this topic area; consider adjacencies instead |
| Competitor's rankings are declining | Their content is aging, opportunity to overtake |
| New domain appearing in top 3 | New entrant or pivot by existing player — investigate |

---

## Review Signals

### Sentiment Patterns

| Pattern | Interpretation | Action |
|---------|---------------|--------|
| High rating (4.5+) but many detailed negative reviews | Product is good overall but has specific painful gaps | Target those specific gaps in your positioning |
| Low rating (<3.5) with passionate positive outliers | Product serves a niche very well but frustrates everyone else | Don't compete head-on; serve the broader market better |
| Declining ratings over time | Product debt accumulating, or team/quality changes | Opportunity to win their churning customers |
| Improving ratings over time | Competitor is investing and executing; they're getting better | Don't wait — differentiate now before the gap closes |
| Many reviews mentioning price | Product seen as too expensive relative to value | Price positioning opportunity |
| "Support" mentioned frequently in negatives | Customer success issues; relationship opportunity for you | Emphasize your support quality |

### Review Content Analysis

| What Reviewers Say | Strategic Signal |
|-------------------|-----------------|
| "We switched from [X] because..." | Direct churn triggers — validate these are real and target them |
| "I wish it could..." | Feature requests = roadmap leak. If many ask for the same thing, it's a real gap |
| "Compared to [Y], it's better at..." | Head-to-head positioning from actual users — more reliable than marketing claims |
| "The onboarding was..." | UX maturity signal. Bad onboarding = opportunity for PLG competitor |
| "Our team of [N] uses..." | Company size signal. Tells you their actual customer profile |
| "We've been using it for [N] years" | Switching cost / lock-in signal. Long-tenured users are harder to convert |

---

## Funding Signals

### Round Type Implications

| Round | What It Means | Competitive Implication |
|-------|-------------|----------------------|
| Seed / Pre-seed | Very early, product may not exist yet | Not a threat today but could be in 12-18 months |
| Series A | Product-market fit validated, scaling started | Starting to compete seriously, watch their next moves |
| Series B-C | Growth stage, scaling sales and marketing | Active competitor, likely aggressive on pricing and hiring |
| Series D+ | Late stage, pre-IPO or sustained growth | Established player, large resources, may be slowing on innovation |
| Down round | Valuation decreased, likely struggling | Vulnerable competitor — their best talent may be leaving |
| Acquisition | Being bought by larger company | Strategic pivot likely, integration period = vulnerability window |
| IPO | Going public | Focused on metrics/profitability, may cut risky initiatives |

### Investor Type Signals

| Investor Type | What It Signals |
|--------------|----------------|
| Top-tier VC (a16z, Sequoia, etc.) | Credibility, large network, aggressive growth expectations |
| Strategic investor (Google, Microsoft, etc.) | Likely integration/partnership coming, ecosystem play |
| PE firm | Profitability focus, possible cost-cutting, may reduce R&D |
| Government/defense VC (In-Q-Tel, etc.) | Government/security market entry |
| Healthcare-focused VC | Healthcare/biotech market expansion |
| International VC | Geographic expansion aligned with investor's region |

---

## Social Media Signals

### Engagement Patterns

| Signal | Interpretation |
|--------|---------------|
| Follower growth accelerating | Marketing investment paying off, or viral moment |
| Follower growth flat/declining | Brand fatigue, or investment shifted elsewhere |
| High engagement, low followers | Niche but passionate community — quality over quantity |
| Low engagement, high followers | Vanity metrics, possibly bought followers, or audience mismatch |
| Executive active on LinkedIn | Thought leadership strategy, personal brand building |
| Company posting job openings on social | Urgent hiring, possibly high attrition |
| Suddenly active after dormancy | New marketing hire, new strategy, or upcoming launch |

### Content Strategy Signals

| What They Post | What It Means |
|---------------|-------------|
| Product updates/releases | Active development, shipping regularly |
| Customer case studies | Sales-driven content, building social proof |
| Industry thought leadership | Positioning as category leader, mindshare play |
| Employee spotlights | Employer branding, likely facing hiring challenges |
| Memes / casual content | B2C or developer audience, community-building strategy |
| Competitive comparisons | Feeling market pressure, actively fighting for positioning |

---

## Combining Signals for Confidence

Individual signals can be misleading. Combine multiple signals for higher confidence:

| Hypothesis | Supporting Signals (need 2+) |
|-----------|----------------------------|
| "Competitor is pivoting to enterprise" | Enterprise pricing tier added + security/compliance hires + SOC2 mentioned in jobs + content shifting to business topics |
| "Competitor is struggling" | Down round + hiring freeze + declining reviews + reduced content output |
| "Competitor entering our market" | New product page + hires in our domain + content on our topics + search ads on our keywords |
| "Competitor about to launch AI features" | ML/AI job postings + "AI" in recent blog posts + AI-related investor + executive AI conference appearances |
| "Competitor moving downmarket" | New free tier + lower pricing + self-serve onboarding + PLG-focused hires (growth engineers, product-led) |

When signals conflict (e.g., aggressive hiring but declining reviews), note the tension and flag it — it may indicate a transition period.

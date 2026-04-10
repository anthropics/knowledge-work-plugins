# Analysis Frameworks

Apply these strategic frameworks to transform raw competitive data into actionable intelligence. Choose the framework that best fits the user's question and the data available.

## When to Use Each Framework

| Framework | Best For | Triggered By |
|-----------|----------|-------------|
| SWOT Analysis | Single competitor deep dive | Competitor Snapshot, Battlecard |
| Porter's Five Forces | Market-level competitive dynamics | Market Landscape Map |
| Positioning Matrix | Comparing multiple competitors visually | Market Landscape, Pricing Intelligence |
| Jobs-to-be-Done | Understanding why customers choose competitors | Review Intelligence |
| Blue Ocean Strategy | Finding uncontested market space | Market Landscape Map |
| Win/Loss Framework | Understanding competitive wins and losses | Review Intelligence, Battlecard |

---

## 1. SWOT Analysis

**Use when**: Profiling a single competitor in depth, or comparing your position against a competitor.

### How to Apply

From the scraped data, categorize findings into:

1. **Strengths** — What the competitor does well (sourced from: homepage messaging, positive reviews, high rankings, strong funding, fast hiring)
2. **Weaknesses** — Where they fall short (sourced from: negative reviews, missing features, pricing complaints, slow hiring, tech debt signals)
3. **Opportunities** — External factors they could exploit (sourced from: market trends, adjacent markets, new technologies, regulatory changes)
4. **Threats** — External risks they face (sourced from: new entrants, open-source alternatives, market commoditization, regulatory pressure)

### Output Format

```markdown
## SWOT Analysis: [Competitor]

| | Helpful | Harmful |
|--|---------|---------|
| **Internal** | **Strengths**: [list] | **Weaknesses**: [list] |
| **External** | **Opportunities**: [list] | **Threats**: [list] |

### Implications for Your Strategy
- Their strength in [X] means you should [differentiate on Y / match X as table stakes]
- Their weakness in [X] is your opportunity to [specific action]
- The market opportunity in [X] means [specific recommendation]
```

### Data Sources to Evidence
- Strengths: Homepage claims, funding data, positive reviews, SERP rankings
- Weaknesses: Negative reviews, feature gaps visible on pricing page, complaints on G2/Capterra
- Opportunities: Industry news, hiring patterns showing new directions
- Threats: Competitor discovery results showing new entrants, pricing pressure from alternatives

---

## 2. Porter's Five Forces

**Use when**: Analyzing overall market attractiveness and competitive dynamics, especially for Market Landscape analysis.

### How to Apply

Assess each force based on scraped evidence:

1. **Competitive Rivalry** (existing competitors)
   - How many players exist? (from market landscape search)
   - Are they well-funded? (from Crunchbase data)
   - Is there pricing pressure? (from pricing page comparisons)
   - Is growth slowing? (from hiring velocity analysis)

2. **Threat of New Entrants**
   - Are barriers to entry high or low? (technical complexity, capital requirements)
   - Are new players appearing? (from recent search results, recent Crunchbase entries)
   - Is open-source disrupting? (from GitHub presence)

3. **Threat of Substitutes**
   - What alternatives exist outside the direct category?
   - Are customers using manual processes or different tools?
   - Evidence from review mentions of alternatives

4. **Bargaining Power of Buyers**
   - Can customers easily switch? (from pricing models, data portability signals)
   - Are customers price-sensitive? (from review pricing complaints)
   - Is the market B2B or B2C?

5. **Bargaining Power of Suppliers**
   - Dependency on specific platforms, APIs, or infrastructure
   - Evidence from job postings (specific technology dependencies)

### Output Format

```markdown
## Porter's Five Forces: [Market/Industry]

| Force | Intensity | Evidence |
|-------|----------|---------|
| Competitive Rivalry | [High/Medium/Low] | [N] players identified, [funding levels], [pricing trends] |
| Threat of New Entrants | [High/Medium/Low] | [barriers], [recent entrants] |
| Threat of Substitutes | [High/Medium/Low] | [alternatives], [switching evidence] |
| Buyer Power | [High/Medium/Low] | [switching costs], [price sensitivity] |
| Supplier Power | [High/Medium/Low] | [dependencies], [platform risks] |

### Market Attractiveness: [High / Medium / Low]
[Summary interpretation and strategic implications]
```

---

## 3. Positioning Matrix (2x2)

**Use when**: Visually mapping competitors along two strategic dimensions, especially during Pricing Intelligence or Market Landscape analysis.

### How to Apply

1. Choose two axes that matter most to the user's market:
   - **Price** (low → high)
   - **Feature breadth** (narrow/focused → broad/all-in-one)
   - **Target segment** (SMB → Enterprise)
   - **Ease of use** (simple → complex/powerful)
   - **Customizability** (opinionated → flexible)

2. Place each competitor based on scraped evidence:
   - Price axis: from pricing page data
   - Feature axis: from product page / feature list scraping
   - Segment axis: from messaging and pricing model analysis

3. Identify the empty quadrant — that's potential white space.

### Output Format

```markdown
## Positioning Matrix: [Category]

**Axes**: [X-axis: e.g., Price (Low → High)] vs. [Y-axis: e.g., Feature Breadth (Focused → Comprehensive)]

```
              Comprehensive
                   │
  [Budget          │       [Enterprise
   All-in-one]     │        Suite]
   Company C       │       Company A
                   │
Low Price ─────────┼───────── High Price
                   │
  [Simple &        │       [Premium
   Affordable]     │        Specialist]
   Company D       │       Company B
                   │
               Focused
```

### White Space: [Quadrant description] — [Why it's an opportunity]
### Recommendation: [Where the user should position and why]
```

### Common Axis Pairs
- **SaaS products**: Price vs. Feature breadth
- **Developer tools**: Ease of use vs. Power/flexibility
- **E-commerce**: Price vs. Quality/brand
- **B2B services**: Self-serve vs. White-glove AND SMB vs. Enterprise

---

## 4. Jobs-to-be-Done (JTBD)

**Use when**: Analyzing reviews to understand why customers hire/fire competitors, especially during Review Intelligence analysis.

### How to Apply

From review data, identify:

1. **Functional jobs** — What task is the customer trying to accomplish?
   - Look for phrases: "I use [product] to...", "We needed...", "The main reason we..."

2. **Emotional jobs** — How does the customer want to feel?
   - Look for: "gives me confidence", "less stressful", "makes me look good"

3. **Social jobs** — How does the customer want to be perceived?
   - Look for: "my team loves", "impressed the board", "our clients notice"

4. **Hiring criteria** — What made them choose this product?
   - Look for: "we chose because", "what sold us", "the reason we switched"

5. **Firing criteria** — What would make them leave?
   - Look for: "considering switching", "frustrating because", "if they don't fix"

### Output Format

```markdown
## Jobs-to-be-Done Analysis: [Product/Category]

### Primary Jobs Customers Hire [Product] For
1. **[Job]** — Evidence: "[quote]" *(Source)*
2. **[Job]** — Evidence: "[quote]" *(Source)*

### Why Customers Hire (Switching Triggers)
- [Trigger 1]: "[quote about what pushed them to switch]"
- [Trigger 2]: "[quote]"

### Why Customers Fire (Churn Triggers)
- [Trigger 1]: "[quote about what's making them consider leaving]"
- [Trigger 2]: "[quote]"

### Underserved Jobs
Jobs customers mention but no competitor fully addresses:
1. **[Unmet job]** — Evidence: "[quote]"

### Implications
- [How to position your product to address these jobs]
- [Which underserved jobs represent the biggest opportunity]
```

---

## 5. Blue Ocean Strategy

**Use when**: Looking for uncontested market space during Market Landscape analysis, or when the user wants to find a unique position.

### How to Apply

Build an Eliminate-Reduce-Raise-Create (ERRC) grid based on competitor analysis:

1. **Eliminate** — Which factors the industry competes on should be eliminated?
   - Look for: features no one uses (from review data), legacy capabilities

2. **Reduce** — Which factors should be reduced below the industry standard?
   - Look for: over-engineered features, complexity that frustrates users (from reviews)

3. **Raise** — Which factors should be raised above the industry standard?
   - Look for: features customers love but want more of (from reviews)

4. **Create** — Which factors should the industry create that it's never offered?
   - Look for: unmet needs in reviews, feature requests, adjacent market innovations

### Output Format

```markdown
## Blue Ocean Analysis: [Category]

### ERRC Grid

| Eliminate | Reduce |
|-----------|--------|
| [Factor competitors invest in that customers don't value] | [Factor that's over-served relative to customer needs] |

| Raise | Create |
|-------|--------|
| [Factor customers want more of] | [Factor nobody offers yet] |

### Value Curve Comparison
| Factor | Industry Avg | Your Proposed Position | Rationale |
|--------|-------------|----------------------|-----------|
| [Factor 1] | [High/Med/Low] | [Your level] | [Why] |
| [Factor 2] | [High/Med/Low] | [Your level] | [Why] |

### Blue Ocean Opportunity
[Description of the uncontested market space and how to reach it]
```

---

## 6. Win/Loss Framework

**Use when**: Building competitive battlecards, or when the user wants to understand why customers choose one competitor over another. Most useful with Review Intelligence data.

### How to Apply

From reviews and competitive mentions, categorize:

1. **Win themes** — Why customers choose this competitor
   - Look for: "chose because", "best at", "switched to"

2. **Loss themes** — Why customers leave or don't choose
   - Look for: "switched from", "left because", "chose [other] instead"

3. **Trap questions** — Questions that expose competitor weaknesses
   - Derived from top pain points in negative reviews

4. **Objection handlers** — How to respond when prospect favors competitor
   - Derived from competitor's top strengths

### Output Format

```markdown
## Win/Loss Analysis: [Your Product] vs. [Competitor]

### Why We Win Against [Competitor]
| Win Theme | Evidence | Sales Talking Point |
|-----------|---------|-------------------|
| [Theme] | "[Customer quote]" | "[How to leverage in conversation]" |

### Why We Lose to [Competitor]
| Loss Theme | Evidence | Counter-Strategy |
|------------|---------|-----------------|
| [Theme] | "[Customer quote]" | "[How to mitigate]" |

### Landmine Questions
Questions to ask prospects that highlight competitor weaknesses:
1. "[Question]" — Exposes: [weakness]
2. "[Question]" — Exposes: [weakness]

### Objection Handling
| When Prospect Says... | Respond With... |
|----------------------|----------------|
| "[Objection favoring competitor]" | "[Your response]" |
```

---

## Combining Frameworks

For comprehensive analyses, combine frameworks naturally:

- **Competitor Snapshot** → SWOT
- **Market Landscape** → Porter's Five Forces + Positioning Matrix
- **Review Intelligence** → JTBD + Win/Loss
- **Full Battlecard** → SWOT + Win/Loss + Positioning Matrix
- **Market Entry Strategy** → Porter's Five Forces + Blue Ocean + Positioning Matrix

Only apply frameworks when they add genuine insight. A simple pricing comparison doesn't need Porter's Five Forces. Match the depth of analysis to the complexity of the question.

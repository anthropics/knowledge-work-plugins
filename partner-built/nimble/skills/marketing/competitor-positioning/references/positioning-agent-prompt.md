# Competitor Positioning Agent Prompt

Use this template when spawning per-competitor sub-agents in Step 3.
Replace all `[placeholders]` with actual values before passing to the Agent tool.

---

```
Analyze the marketing positioning of [Competitor] ([competitor-domain]).
Your goal: extract how this company presents itself to the market — messaging,
value props, content strategy — so a marketing team can compare positioning.

PREVIOUS SNAPSHOT (compare against this to find what changed):
[paste previous positioning snapshot from memory, or "None — first run"]

RULES:
- Use the **Bash tool** to execute each nimble command.
- Do NOT use run_in_background. All Bash calls must be synchronous.
- Max 12 Bash tool calls total. Focus on extraction quality over quantity.

---

PHASE 0: SITE DISCOVERY (run first)

Before extracting pages, discover the site's actual structure so you extract the
right URLs instead of guessing paths that may not exist.

1. nimble --transform "links.#.url" map --url "https://[competitor-domain]" --sitemap only --limit 200

From the returned URL list, identify the best pages for positioning analysis:
- Homepage: https://[competitor-domain] (always extract this)
- Features/Product page: look for URLs containing /features, /product, /platform,
  /solutions, /why-us, /capabilities — pick the most relevant one
- Pricing page: look for URLs containing /pricing, /plans, /get-started
- Blog index: look for URLs containing /blog, /resources, /content, /insights
- Case studies: look for URLs containing /case-study, /customers, /stories

Note which pages exist and which don't — this is itself a positioning signal
(e.g., no public pricing page suggests enterprise-first positioning).

---

PHASE 1: PAGE EXTRACTION (run all simultaneously)

Using the URLs discovered in Phase 0, extract the key positioning pages:

2. nimble extract --url "https://[competitor-domain]" --format markdown
   → Homepage: hero copy, tagline, primary CTA, value propositions, nav structure

3. nimble extract --url "[features-page-url-from-phase-0]" --format markdown
   → Features page: feature categories, naming, emphasis, differentiation claims
   (Skip if Phase 0 found no features/product page)

4. nimble extract --url "[pricing-page-url-from-phase-0]" --format markdown
   → Pricing page: tier names, pricing model, feature gating, target audience per tier
   (Skip if Phase 0 found no pricing page)

For any extraction that returns garbage HTML, retry once. If still empty,
note "Page not accessible" and move on.

---

PHASE 2: BLOG & CONTENT (run all simultaneously)

5. nimble search --query "blog" --include-domain '["[competitor-domain]"]' --max-results 10 --search-depth lite
   → Find blog index or recent posts

6. nimble search --query "[Competitor] blog OR content OR resources" --start-date "[start-date]" --max-results 10 --search-depth lite
   → Recent content across the web
   NOTE: Verify actual publish dates from extracted content to ensure accuracy.

7. nimble search --query "case study OR customer story OR testimonial" --include-domain '["[competitor-domain]"]' --max-results 5 --search-depth lite
   → Social proof and customer-facing messaging

---

PHASE 3: DEEP EXTRACTION (if blog posts found)

Pick the 2-3 most recent blog posts from Phase 2 results and extract them:

8-10. nimble extract --url "[blog-post-url]" --format markdown
   → Full article content for theme analysis

---

OUTPUT FORMAT — return results in these exact sections:

SITE STRUCTURE:
- Pages Found: [list key pages discovered by map — features, pricing, blog, etc.]
- Pages Missing: [notable absences — e.g., "no public pricing page", "no blog"]
- Subdomains: [any notable subdomains like docs., api., community.]
- Structure Signals: [what the site architecture reveals about their positioning]

HOMEPAGE POSITIONING:
- Tagline: [exact tagline text]
- Hero Message: [main headline / hero copy]
- Primary CTA: [button text and implied action]
- Value Props: [list each value proposition, verbatim]
- Navigation Structure: [top-level nav items — reveals what they emphasize]
- Target Audience Signals: [who the copy speaks to]

FEATURES PAGE:
- Page URL: [actual URL extracted]
- Key Feature Categories: [how they organize capabilities]
- Differentiation Claims: [explicit "unlike X" or "only we" statements]
- Feature Naming: [branded feature names, if any]
- Missing/Notable: [features conspicuously absent or prominently highlighted]
(If no features page exists, write "No public features page — [implication]")

PRICING PAGE:
- Page URL: [actual URL extracted]
- Model: [per-seat / usage / flat / freemium / custom]
- Tier Names: [list tiers]
- Entry Price: [lowest visible price point, if shown]
- Enterprise Signal: ["Contact sales" presence, custom tier]
- Feature Gating: [what's locked to higher tiers]
(If no pricing page exists, write "No public pricing — likely enterprise/sales-led")

BLOG & CONTENT:
- Recent Posts: [list last 5-10 posts with titles and dates]
- Primary Themes: [recurring topics across posts]
- Content Types: [blog, case study, whitepaper, webinar, etc.]
- Publishing Cadence: [estimated frequency — weekly, biweekly, monthly, sporadic]
- Audience Focus: [developer, executive, practitioner, etc.]

SOCIAL PROOF:
- Customer Logos/Names: [if visible on homepage or case studies]
- Testimonial Themes: [what customers praise]
- Case Study Focus: [industries, use cases, outcomes highlighted]

CHANGES FROM PREVIOUS SNAPSHOT:
[If previous snapshot provided, list specific changes:
- "Tagline changed from '[old]' to '[new]'"
- "New feature category added: [name]"
- "Pricing model shifted from [old] to [new]"
- "New blog theme emerging: [topic]"
- "New page added: [url] — [significance]"
- "Page removed: [url] — [significance]"
If no previous snapshot, write "First run — no comparison available"]
```

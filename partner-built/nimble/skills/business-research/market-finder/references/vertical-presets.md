# Vertical Presets for Market Finder

Each preset defines query patterns, target domains, and entity types for a
business vertical. The skill auto-selects the preset based on user input, then
**discovers available WSAs at runtime** using `nimble agent list --search`.

---

## Preset Selection Logic

See SKILL.md Step 2 for the matching and selection flow.

---

## Healthcare

**Trigger keywords:** doctor, dentist, dermatologist, ophthalmologist, optometrist,
chiropractor, therapist, psychiatrist, pediatrician, clinic, medical, healthcare,
hospital, pharmacy, urgent care, physical therapy, orthodontist, surgeon, physician,
practice, practitioner

**Discovery targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP | Primary geo-targeted discovery |
| www.yelp.com | SERP | Secondary -- catches practices missing from Google |
| bbb.org | SERP | Tertiary -- accreditation/credibility data |

**Enrichment targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP (reviews) | Patient review volume and sentiment |
| bbb.org | PDP / Profile | Accreditation status, complaint history |

**Query pattern:** `"{specialty} {type}" per metro`
- Example: `"ophthalmologist" in Miami FL`, `"dentist" in Tampa FL`

**Geo-tiling:** Yes -- tile by metro areas within the target state/region.

---

## SaaS / Software

**Trigger keywords:** SaaS, software, app, platform, tool, cloud, B2B, startup,
project management, CRM, ERP, analytics, automation, API, fintech, martech,
edtech, healthtech, devtools, developer tools, productivity software

**Discovery targets:** None (no map WSAs). Use `nimble search` in two passes:

**Pass 1 -- Product discovery** (find the players):
```
nimble search --query "{vertical} site:g2.com" --max-results 20 --search-depth lite
nimble search --query "{vertical} site:capterra.com" --max-results 20 --search-depth lite
nimble search --query "best {vertical} software {current_year}" --max-results 20 --search-depth lite
nimble search --query "{vertical} site:producthunt.com" --max-results 10 --search-depth lite
nimble search --query "{vertical} open source github" --max-results 10 --search-depth lite
```

**Pass 2 -- Financial & traction discovery** (funding, market context):
```
nimble search --query "{vertical} site:crunchbase.com" --max-results 15 --search-depth lite
nimble search --query "{vertical} startup funding raised" --focus news --max-results 15 --search-depth lite
nimble search --query "{vertical} market landscape players" --max-results 15 --search-depth lite
```

**Enrichment targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| g2.com | PDP | Structured product data, ratings, pricing tier |
| capterra.com | PDP | Product comparison data (if WSA available) |
| crunchbase.com | Profile | Funding rounds, valuation, team size |

**Query pattern:** No geo-tiling. Search by category/vertical keywords.

**Geo-tiling:** No -- SaaS products are not geography-bound. If the user specifies
a region, interpret as "headquartered in" and add as a search qualifier.

**Dedup key:** `domain` (not place_id).

**Scoring note:** SaaS uses different strength criteria than geographic verticals --
see SKILL.md Step 7 for SaaS-specific scoring based on funding, directory presence,
and review counts.

---

## Restaurants / Food

**Trigger keywords:** restaurant, cafe, coffee, bakery, bar, pub, brewery, pizza,
sushi, taco, brunch, diner, bistro, food, catering, food truck, ice cream, juice,
steakhouse, seafood, burger, ramen, pho, thai, italian, mexican, chinese, indian,
mediterranean, vegan, vegetarian

**Discovery targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP | Primary geo-targeted discovery |
| www.yelp.com | SERP | Strong for food/drink |

**Enrichment targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP (reviews) | Review volume and rating |

**Query pattern:** `"{cuisine} restaurant" per metro`

**Geo-tiling:** Yes -- tile by metro areas or neighborhoods for large geographies.

---

## Legal / Financial

**Trigger keywords:** lawyer, attorney, law firm, legal, accountant, accounting,
CPA, financial advisor, wealth management, insurance, tax, bankruptcy, immigration,
personal injury, real estate attorney, family law, criminal defense, corporate law,
patent, IP, intellectual property

**Discovery targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP | Primary geo-targeted discovery |
| bbb.org | SERP | Accreditation and complaint history |

**Enrichment targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| bbb.org | PDP / Profile | Accreditation, years in business, complaints |

**Query pattern:** `"{practice area} {type}" per metro`

**Geo-tiling:** Yes -- tile by metro areas within the target state/region.

---

## Auto / Home Services

**Trigger keywords:** mechanic, auto repair, body shop, car wash, oil change, tire,
plumber, plumbing, electrician, HVAC, roofing, landscaping, pest control, cleaning,
maid service, handyman, locksmith, moving, storage, painting, flooring, contractor,
renovation, remodeling, garage door, appliance repair

**Discovery targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP | Primary geo-targeted discovery |
| www.yelp.com | SERP | Strong for home services |
| bbb.org | SERP | Complaint history, accreditation |

**Enrichment targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP (reviews) | Review volume and sentiment |
| bbb.org | PDP / Profile | Complaint history, years in business |

**Query pattern:** `"{service}" per metro`

**Geo-tiling:** Yes -- tile by metro areas.

---

## Custom

**Trigger keywords:** (fallback -- used when no other preset matches)

**Discovery targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP | Primary geo-targeted discovery |
| www.yelp.com | SERP | Secondary coverage |

**Enrichment targets:**

| Domain | Entity type | Purpose |
|--------|-------------|---------|
| maps.google.com | SERP (reviews) | Review volume and rating |

**Query pattern:** User's keywords per metro.

**Geo-tiling:** Yes (unless the query is clearly non-geographic).

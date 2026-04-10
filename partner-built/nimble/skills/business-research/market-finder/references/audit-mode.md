# Audit Mode

Compares a user's existing business list against market-finder's discovery results,
surfacing gaps in both directions. Read this when Audit mode is triggered.

---

## When Audit Mode Triggers

Audit mode activates when the user provides a **reference list** alongside a discovery
request. Detection signals (check in Step 1 of SKILL.md):

| Signal | Example |
|--------|---------|
| Google Sheet URL in input | `docs.google.com/spreadsheets/d/...` |
| CSV file path | `my-practices.csv`, `~/Downloads/list.csv` |
| Inline list (3+ businesses) | Pasted names/addresses, one per line |
| Explicit audit language | "audit my list", "compare against", "what am I missing" |

If the user provides a reference list but no audit intent, ask:
"You provided a list. Want me to **audit it** against fresh discovery, or just use it
as a starting point for discovery?"

---

## Reference List Parsing

Follow the Input Parsing Pattern from `references/nimble-playbook.md` to detect format,
then normalize to a uniform record list.

### Google Sheet URL

```bash
nimble extract --url "{sheet_url}" --format markdown
```

Parse the markdown table. Map columns by header name (case-insensitive):

| Target field | Accepted column headers |
|-------------|------------------------|
| `name` | name, business name, practice name, company, organization |
| `domain` | domain, website, url, web, site |
| `city` | city, location, metro, area |
| `state` | state, st, region |
| `phone` | phone, telephone, tel, phone number |
| `address` | address, street, full address |

### CSV file

```bash
cat -- "{file_path}"
```

Parse as CSV. Same column mapping as above.

### Inline list

Parse each line as a business entry. Try to extract:
- Business name (first segment before any delimiter)
- Location (city/state if present)
- Domain or phone if included

If the inline format is unclear, ask one clarifying question:
"What columns does your list have? (e.g., name, city, phone)"

### Normalization

After parsing, normalize every record to:

```json
{
  "name": "Acme Dental",
  "domain": "acmedental.com",
  "city": "Miami",
  "state": "FL",
  "phone": "3051234567",
  "raw": "original row as-is for traceability"
}
```

- **Domain:** strip `http://`, `https://`, `www.`, trailing `/`
- **Phone:** strip all non-digits, keep last 10 digits (US) or full international
- **Name:** trim whitespace, preserve original casing for display
- **Missing fields:** set to `null` — matching layers skip null fields

---

## Matching Algorithm

Run all three layers in order. Once an entity matches at any layer, stop — don't
re-match at lower layers. Track which layer produced each match.

### Layer 1: Domain Match (primary)

Compare normalized root domains between reference and discovered entities.

```
reference: acmedental.com  ↔  discovered: acmedental.com  →  MATCH
reference: acmedental.com  ↔  discovered: acme-dental.com →  NO MATCH
```

**Rules:**
- Strip `www.`, protocol, trailing `/`, path segments
- Compare root domain only (not subdomains)
- Exact match required — no fuzzy domain matching

Skip entities where either side has `domain: null`.

### Layer 2: Name + City Fuzzy Match (secondary)

For unmatched entities after Layer 1, compare business names within the same city.

**Normalization:**
1. Lowercase both names
2. Remove punctuation: `.,'-&!()[]`
3. Remove common suffixes: `inc`, `llc`, `ltd`, `corp`, `co`, `pllc`, `pa`, `pc`,
   `dds`, `md`, `dmd`, `do`, `group`, `associates`, `and associates`
4. Split into word tokens

**Matching:**
- Both entities must share the same city (case-insensitive, after trimming)
- Calculate word overlap: `shared_words / max(words_a, words_b)`
- **Threshold: 80%** word overlap = match

```
"Acme Dental Associates" in Miami  ↔  "Acme Dental" in Miami
  → tokens: [acme, dental] vs [acme, dental]  → 100% overlap  → MATCH

"Acme Dental" in Miami  ↔  "Acme Health" in Miami
  → tokens: [acme, dental] vs [acme, health]  → 50% overlap  → NO MATCH
```

Skip entities where either side has `city: null`.

### Layer 3: Phone Match (tertiary)

For still-unmatched entities, compare normalized phone numbers.

**Normalization:** Strip all non-digit characters, keep last 10 digits.

```
reference: (305) 123-4567  →  3051234567
discovered: 305-123-4567   →  3051234567  →  MATCH
```

Skip entities where either side has `phone: null`.

---

## Categorization

After all three matching layers complete:

| Category | Definition | Business meaning |
|----------|-----------|-----------------|
| `matched` | In both reference list AND discovery results | Validated — your list is accurate here |
| `discovered_only` | Found by market-finder but NOT in reference list | Expansion candidates — potential gaps in your list |
| `reference_only` | In reference list but NOT found by market-finder | Coverage gaps — these may have closed, moved, or been missed by discovery |

---

## Output Template

```markdown
# Market Finder Audit: [Business Type] in [Geography]
*Audited [R] reference entries against [D] discovered businesses | [Date]*

## TL;DR
[M/R × 100]% coverage — [M] of [R] reference entries verified, [DO] new businesses
discovered, [RO] in your list but not found by discovery.

## Summary
- **Reference list:** [R] entries
- **Discovered:** [D] businesses
- **Matched:** [M] ([M/R]% of reference list verified)
- **Discovered only:** [DO] expansion candidates
- **Reference only:** [RO] coverage gaps

## Coverage Score
**[M/R × 100]% of your reference list was independently verified by market discovery.**

## Matched ([M])
Confirmed in both your list and fresh discovery.

| # | Name | Location | Match Layer | Discovery Strength | Sources |
|---|------|----------|-------------|-------------------|---------|
| 1 | Acme Dental | Miami, FL | Domain | *** High | Maps, Yelp |
...

## Discovered Only ([DO]) — Expansion Candidates
Found by market-finder but missing from your reference list.

| # | Name | Location | Domain | Rating | Strength | Sources |
|---|------|----------|--------|--------|----------|---------|
| 1 | WidgetCo Health | Orlando, FL | widgetco.com | 4.6 | ** Medium | Maps |
...

## Reference Only ([RO]) — Coverage Gaps
In your list but not found by market discovery. Possible reasons: closed, relocated,
rebranded, niche/unlisted, or discovery source limitations.

| # | Name | Location | Domain | Phone | Possible Reason |
|---|------|----------|--------|-------|----------------|
| 1 | Old Practice | Tampa, FL | — | (813) 555-0100 | Not found in any source |
...

## What This Means
[1-3 sentences interpreting the audit results — e.g., coverage percentage,
geographic clusters in discovered_only, notable reference_only entries]
```

---

## Memory

Save audit results to:
- Report: `~/.nimble/memory/reports/market-finder-audit-{slug}-{date}.md`
- Structured data: `~/.nimble/memory/market-finder/{slug}/audit-{date}.json`

The JSON includes all three categories with match metadata (which layer matched,
confidence) for downstream use.

---

## Follow-ups (Audit-specific)

After presenting audit results, offer:

- **"Export discovered-only as CSV for outreach?"** — generate a CSV of expansion candidates
- **"Investigate reference-only gaps?"** — run targeted searches for reference_only
  entities to determine if they've closed, moved, or rebranded
- **"Run company-deep-dive on new discoveries?"** — deep research on high-strength
  discovered_only entities
- **"Re-run with a different geography?"** — audit the same list against a broader
  or narrower area

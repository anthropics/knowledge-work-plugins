# WSA Discovery for Healthcare Providers Extract

How to find and evaluate WSAs for each phase of provider extraction. The WSA catalog
evolves constantly — new agents get added for healthcare directories, review sites,
and regulatory databases. This skill discovers relevant agents at runtime rather than
relying on a static list.

For general WSA execution rules (invocation, parsing, batch, fallback), see
`nimble-playbook.md`.

---

## Discovery Strategy

### Three search layers

Run these searches at the start of the skill (during or right after preflight) to
build a session-specific WSA inventory. Run all searches simultaneously:

**Layer 1 — Vertical search:**
```bash
nimble agent list --limit 100 --search "healthcare"
```
Returns all agents tagged with the Healthcare vertical (clinicaltrials.gov, FDA,
and any newly added healthcare agents).

**Layer 2 — Session-specific search:**
Search for terms derived from the user's input — their specialty, location, or
specific domains they mentioned:
```bash
# If user said "ophthalmology in Austin":
nimble agent list --limit 50 --search "ophthalmology"
nimble agent list --limit 50 --search "eye"

# If user mentioned specific directories:
nimble agent list --limit 50 --search "zocdoc"
nimble agent list --limit 50 --search "healthgrades"
nimble agent list --limit 50 --search "vitals"
```
Adapt search terms to whatever the user provided. Include the specialty, common
directory names for that specialty, and any domains the user mentioned.

**Layer 3 — General discovery tools:**
These WSAs are useful across verticals for practice discovery, reputation, and
verification:
```bash
nimble agent list --limit 50 --search "google_maps"
nimble agent list --limit 50 --search "yelp"
nimble agent list --limit 50 --search "bbb"
nimble agent list --limit 50 --search "review"
```

### Evaluating discovered agents

For each discovered agent, read its `description` and `entity_type` to classify it
into a phase:

| If the agent description mentions... | Assign to phase |
|--------------------------------------|----------------|
| Search, listings, directory, discovery, local businesses | **Discovery** — finding practice URLs |
| Reviews, ratings, patient feedback, reputation | **Enrichment: Reputation** |
| Clinical trials, FDA, regulatory, compliance, licensing | **Enrichment: Regulatory** |
| Profile, detail page, business info, contact | **Enrichment: Practice details** |

Validate each relevant agent's params before using it:
```bash
nimble agent get --template-name [agent_name]
```

**Skip agents that don't fit** — not every healthcare-tagged agent is useful for
provider extraction. An FDA drug label agent, for example, isn't relevant unless
the user specifically asked about pharmaceuticals.

### Healthcare discovery prioritization

Recommended approach for healthcare practice discovery:

- **Google Maps WSA** — Primary source. Rich structured data (name, address, rating,
  reviews, phone, place_id, coordinates). Process these results first. Note: the
  `place_url` field links to Maps — resolve practice website URLs in a separate step
  (see SKILL.md Step 2b).
- **Yelp WSA** — Supplementary source. Run alongside Maps but don't block on it.
  Filter results by specialty keywords before merging, as Yelp categories are broader
  than medical specialty searches.
- **BBB WSA** — Best suited for enrichment (accreditation lookup on known practices)
  rather than discovery. For broader BBB-based discovery, use
  `nimble search --query "[specialty] site:bbb.org"` which returns multiple results.

### Building the session WSA plan

After discovery, present what you found to the user inline:

> "Found **N relevant WSAs** for this run: [list by phase]. Using these alongside
> direct site extraction."

This transparency helps the user understand what data sources are available and
lets them suggest additional search terms if something is missing.

---

## Phase Mapping

### Discovery phase (finding practice URLs)

**When:** User provided a specialty + location instead of URLs.

**Useful agent types:** Map search, directory search, local business listings.

**Search terms to try:** `google_maps`, `yelp`, `bing_maps`, `bbb`, plus any
healthcare directory the user mentions.

**How to use:** Run discovered search/listing agents with the user's specialty +
location as query params. Extract practice website URLs from results. Deduplicate
by domain.

**Fallback (always available):**
```bash
nimble search --query "[specialty] in [location]" --max-results 20 --search-depth lite
```

### Extraction phase (pulling provider data from sites)

**When:** Always — this is the core pipeline.

**No WSA needed.** This phase uses `nimble map` + `nimble extract` directly on
practice websites. See `provider-extraction-patterns.md` for page scoring and
field detection.

However, if Layer 2 discovery found a WSA that extracts provider data from a
specific healthcare directory (e.g., a future `zocdoc_provider_profile` or
`healthgrades_doctor_profile` agent), use it for practices listed on that directory
instead of scraping their website directly — structured WSA output is higher quality
than parsed markdown.

### Enrichment phase (optional, on request)

**When:** User asks for practice reputation, regulatory data, or you're suggesting
next steps.

**Reputation — search terms:** `review`, `google_maps_reviews`, `yelp`, `bbb`
- Use review agents with `place_id` or practice URL from the discovery phase
- Use BBB agents for business credibility checks

**Regulatory — search terms:** `healthcare` vertical, `clinicaltrials`, `fda`,
`npi`, `license`
- Use any discovered regulatory agents to cross-reference providers or practices
- Particularly valuable for clinical trial involvement, device clearances, drug
  research

**Practice details — search terms:** directory-specific agents found in Layer 2
- If an agent provides structured practice profiles (hours, insurance, staff count),
  use it to supplement extracted data

---

## Scaling WSA Calls

Follow the Scaled Execution pattern from `nimble-playbook.md` — it covers
individual calls, batching, and the confirmation gate for large jobs.

---

## Fallback Chain

If WSA discovery returns nothing useful for a phase, fall back to `nimble search`
+ `nimble extract` (the core Nimble tools always work):

1. **Discovery fallback:** `nimble search --query "[specialty] in [location]" --max-results 20 --search-depth lite`
2. **Enrichment fallback:** `nimble search --query "[practice-name] reviews" --max-results 5 --search-depth lite` + `nimble extract` on results
3. **Regulatory fallback:** `nimble search --query "[provider-name] [credentials] NPI OR license OR board certification" --max-results 5 --search-depth lite`

The skill always produces results even if zero WSAs are found — WSAs accelerate
and enrich, but are never required.

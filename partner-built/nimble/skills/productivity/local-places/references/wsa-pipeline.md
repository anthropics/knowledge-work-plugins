# WSA Pipeline for Local Places

WSA discovery strategy, phase classification, category detection, location
disambiguation, and interactive map generation. For general WSA execution rules
(invocation, parsing, fallback), see `nimble-playbook.md`.

---

## WSA Discovery Strategy

WSA names are dynamic and change frequently. Discover all WSAs at runtime in
Step 4 using `nimble agent list --search`. Never hardcode WSA names.

### Discovery search terms

Run these simultaneously to find WSAs for all phases:

| Search term | Finds WSAs for | Phase |
|-------------|---------------|-------|
| `"maps"` | Geo-targeted place discovery (maps, location data) | Phase 1 |
| `"reviews"` | Review content and ratings | Phase 3 |
| `"social"`, `"facebook"`, `"instagram"` | Social profile enrichment | Phase 2 |
| `"{place-type}"` (e.g., "restaurant", "gym") | Vertical-specific discovery and detail | Phase 1 / Phase 4 |
| `"delivery"`, `"food"` | Delivery platform data (DoorDash, Uber Eats) | Phase 4 |

### Classification rules

After discovery, classify each WSA into a phase by its `entity_type` and description:

| Phase | Purpose | entity_type signals | Description signals |
|-------|---------|-------------------|-------------------|
| **Phase 1 -- Discovery** | Find places in a location | SERP | "search", "maps", "listings", "location" |
| **Phase 2 -- Social** | Enrich with social data | Profile | "facebook", "instagram", "tiktok", "social" |
| **Phase 3 -- Reviews** | Pull review content | PDP, Profile | "reviews", "ratings", "customer" |
| **Phase 4 -- Food/Drink** | Delivery platform data | SERP, PDP | "doordash", "ubereats", "delivery", "menu" |

Prefer `managed_by: "nimble"` over `managed_by: "community"` when multiple WSAs
serve the same purpose.

### Phase execution

- **Phase 1:** Run primary + secondary discovery WSAs simultaneously. Run tertiary
  only if < 10 combined unique results.
- **Phase 2:** Run for places with social handles found in Phase 1. Trigger social
  handle search if not in discovery results:
  `nimble search --query "[place-name] [location] facebook OR instagram" --max-results 3 --search-depth lite`
- **Phase 3:** Run for places with a `place_id` or equivalent ID from Phase 1.
  Prioritize High/Medium confidence places.
- **Phase 4:** Auto-trigger for food/drink categories only (see Category Detection).

### Fallback

For any phase where no WSA was discovered:
```bash
nimble search --query "[place-name] [location]" --max-results 5 --search-depth lite
nimble extract --url "[place-website]" --format markdown
```

Use `nimble extract` on the place's own website to gather hours, menu, services, etc.
Follow the Page Extraction with Retry pattern from `nimble-playbook.md`.

---

## Category Detection

Detect the place category from the user's query to determine which WSA phases apply.

| Category | Trigger Keywords | Bonus Phases |
|----------|-----------------|--------------|
| **Food/Drink** | restaurant, cafe, coffee, bakery, bar, pub, brewery, pizza, sushi, taco, brunch, diner, bistro, food, drink, cocktail, wine bar, beer garden, ice cream, juice | Phase 4 (DoorDash/Uber Eats) |
| **Fitness** | gym, yoga, pilates, crossfit, fitness, boxing, martial arts, swimming, climbing, spin | -- |
| **Retail** | shop, store, boutique, bookstore, record store, vintage, thrift, gallery, market | -- |
| **Services** | salon, barber, spa, laundromat, dry cleaner, mechanic, vet, dentist, doctor | -- |
| **Entertainment** | theater, cinema, bowling, arcade, karaoke, club, music venue, comedy | -- |
| **Workspace** | coworking, office space, library, study spot | -- |

**Detection logic:** Check the user's place type query against the trigger keywords.
Match is case-insensitive and supports partial matches ("coffee" matches "coffee shop",
"coffee house", "specialty coffee"). If no category matches, default to general
discovery (Phases 1-3 only, no bonus phases).

---

## Location Disambiguation

### Common Ambiguous Locations

| Name | Possible Matches |
|------|-----------------|
| Williamsburg | Brooklyn, NY / Williamsburg, VA |
| Soho | Manhattan, NY / London, UK / Soho, Hong Kong |
| Georgetown | Washington, DC / Georgetown, TX / Georgetown, Penang |
| Venice | Venice, CA (LA) / Venice, Italy |
| Hollywood | Hollywood, CA / Hollywood, FL |
| Chelsea | Manhattan, NY / Chelsea, London |
| Richmond | Richmond, VA / Richmond, CA / Richmond, London |

### Disambiguation Strategy

1. **Check for context clues** in the user's message: state abbreviations, country
   names, nearby landmarks ("near downtown", "in Brooklyn")
2. **Default to US locations** when no country context is given, unless the user's
   profile or conversation history suggests otherwise
3. **For genuinely ambiguous cases**, ask the user (counts toward 2-prompt max)
4. **After resolution**, always confirm the full location inline:
   "Searching **Soho, Manhattan, NY**..."

### Deriving the Neighborhood Slug

Used for checkpointing and file paths. Rules:
- Lowercase all characters
- Replace spaces and commas with hyphens
- Remove duplicate hyphens
- Include city + state/country for disambiguation

Examples:
- "Williamsburg, Brooklyn, NY" -> `williamsburg-brooklyn-ny`
- "East Village, Manhattan, NY" -> `east-village-manhattan-ny`
- "Silver Lake, Los Angeles, CA" -> `silver-lake-los-angeles-ca`

---

## Interactive Map Generation

Generate an HTML file using Leaflet.js with OpenStreetMap tiles. The map provides
a visual overview of all discovered places with color-coded markers by category.

### Color Scheme by Category

| Category | Marker Color | Hex |
|----------|-------------|-----|
| Food/Drink | Red | `#e74c3c` |
| Fitness | Green | `#2ecc71` |
| Retail | Blue | `#3498db` |
| Services | Orange | `#e67e22` |
| Entertainment | Purple | `#9b59b6` |
| Workspace | Teal | `#1abc9c` |
| Other | Gray | `#95a5a6` |

### Map HTML Template

The generated file should include:
- Leaflet.js + OpenStreetMap tile layer (CDN-loaded, no local dependencies)
- Markers for each place, color-coded by category
- Popup on click: name, rating, address, confidence level, link to website
- Marker size scaled by confidence (High = large, Medium = medium, Low = small)
- Auto-fit bounds to show all markers
- Legend showing category colors and confidence levels
- Title bar with search context: "[Place Type] in [Location] -- [Date]"

### Geocoding

Places from Google Maps discovery typically include lat/lng coordinates. For places
from other sources (Yelp, BBB, fallback search) that lack coordinates:

1. Use the address to approximate location (most mapping libraries handle this)
2. If no address available, omit from map and note in the "What's Missing" section
3. Never fabricate coordinates

### File Naming

`~/.nimble/memory/local-places/{slug}-map-{YYYY-MM-DD}.html`

Open automatically after generation:
```bash
open ~/.nimble/memory/local-places/{slug}-map-{YYYY-MM-DD}.html
```

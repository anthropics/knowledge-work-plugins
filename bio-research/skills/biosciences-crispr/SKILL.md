---
name: biosciences-crispr
description: "Validates synthetic lethality claims from CRISPR knockout screens using BioGRID ORCS 5-phase workflow. This skill should be used when the user asks to \"validate synthetic lethality\", \"query CRISPR essentiality data\", \"find gene dependencies\", \"compare cell line screens\", or mentions BioGRID ORCS, gene knockout data, essentiality scores (CERES, MAGeCK, BAGEL), or asks to validate claims from published CRISPR papers."
---

# CRISPR Essentiality & Synthetic Lethality Validation

Validate synthetic lethality hypotheses using BioGRID ORCS CRISPR screen data via curl.

## Quick Reference

| Task | Endpoint | Key Parameters |
|------|----------|----------------|
| Get essential screens only | `/gene/{entrez_id}?hit=yes` | `hit=yes` filters to essential |
| Get all gene screens | `/gene/{entrez_id}` | Returns all screens |
| Get screen annotations | `/screens/?screenID=1\|2\|3` | Pipe-separated IDs |
| Find cell line screens | `/screens/?cellLine={name}` | Cell line name |

## BioGRID ORCS API

**IMPORTANT**: Use `orcsws.thebiogrid.org` (NOT `orcs.thebiogrid.org`)

- **Base URL**: `https://orcsws.thebiogrid.org`
- **Auth**: Requires `BIOGRID_API_KEY` which is captured in `.env` file
- **Rate Limit**: ~10 req/s
- **Formats**: `format=tab` (default) or `format=json`

### Critical Parameter: `hit=yes`

**Always use `hit=yes` when querying gene essentiality.** This filters results to only screens where the gene scored as a hit (essential), dramatically reducing data volume:

- Without filter: ~1,400 records (all screens)
- With `hit=yes`: ~300-400 records (essential screens only)

### Data Format (JSON)

```json
{
  "SCREEN_ID": "16",
  "IDENTIFIER_ID": "7298",
  "OFFICIAL_SYMBOL": "TYMS",
  "SCORE.1": "100.84",
  "SCORE.2": "-",
  "HIT": "YES",
  "SOURCE": "BioGRID ORCS"
}
```

### Screen Annotation Fields

Query `/screens/?screenID={ids}` to get cell line and publication data:
- `SCREEN_ID`: Unique screen identifier
- `SOURCE_ID`: PubMed ID
- `AUTHOR`: First author and year
- `CELL_LINE`: Cell line name
- `PHENOTYPE`: Screen phenotype (e.g., "cell proliferation")

## 5-Phase Synthetic Lethality Validation Workflow

### Phase 1: Resolve Gene Identifiers

Use Life Sciences MCPs to get Entrez IDs:

```bash
# Using HGNC MCP: search_genes → get_gene
# Extract "entrez" from cross_references object
# Example: DHODH → {"cross_references": {"entrez": "1723"}}

# Using Entrez MCP: search_genes
# Top result format: "NCBIGene:1723"
# Extract numeric ID: 1723
```

### Phase 2: Query ORCS for Essential Screens Only

**CRITICAL: Always use `hit=yes` to filter to essential screens:**

```bash
# Get ONLY screens where gene is essential (hit=yes)
curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" > gene_essential.json

# Count essential screens
cat gene_essential.json | jq '. | length'
# Output: 352 (vs 1,446 without hit=yes filter)
```

**Why this matters:**
- Without `hit=yes`: Returns ALL screens (~1,400 records)
- With `hit=yes`: Returns only screens where gene is essential (~300-400 records)
- Reduces data volume by 75% and focuses on biologically meaningful results

### Phase 3: Get Screen Annotations (Cell Lines & PubMed)

**Two-step workflow**: Query gene for screen IDs, then query screens for annotations.

```bash
# Step 3a: Extract unique screen IDs from essential screens
SCREEN_IDS=$(curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" | \
  jq -r '.[].SCREEN_ID' | sort -u | head -20 | tr '\n' '|' | sed 's/|$//')

# Step 3b: Get screen annotations (cell line, PubMed, author)
curl -s "https://orcsws.thebiogrid.org/screens/?accesskey=${BIOGRID_API_KEY}&screenID=${SCREEN_IDS}&format=json" | \
  jq '.[] | {SCREEN_ID, SOURCE_ID, AUTHOR, CELL_LINE, PHENOTYPE}'
```

**Example output:**
```json
{
  "SCREEN_ID": "16",
  "SOURCE_ID": "26627737",
  "AUTHOR": "Hart T (2015)",
  "CELL_LINE": "HCT 116",
  "PHENOTYPE": "cell proliferation"
}
```

This gives you:
- `SOURCE_ID`: PubMed ID for the screen publication
- `AUTHOR`: First author and year
- `CELL_LINE`: Cell line name for cross-referencing with DepMap/CCLE

### Phase 4: Extract Dependency Scores

With JSON format, extract scores using jq:

```bash
# Get essential screens with scores
curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" | \
  jq '.[] | select(.SCREEN_ID == "16" or .SCREEN_ID == "17") | {SCREEN_ID, SCORE: .["SCORE.1"], symbol: .OFFICIAL_SYMBOL}'
```

**Example output:**
```json
{"SCREEN_ID": "16", "SCORE": "100.84", "symbol": "TYMS"}
{"SCREEN_ID": "17", "SCORE": "107.563", "symbol": "TYMS"}
```

**Interpretation:**
- **HIT = YES** = gene is essential in this screen
- **Positive BAGEL score** = essential (Bayes Factor)
- **Negative CERES score** = essential (depletion)
- Different screens use different scoring methods (check screen metadata)

### Phase 5: Compare Across Genetic Backgrounds

Calculate essentiality rate across all screens:

```bash
# Count essential vs total screens
TOTAL=$(curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&format=json" | jq '. | length')
ESSENTIAL=$(curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" | jq '. | length')
echo "TYMS essential in $ESSENTIAL / $TOTAL screens ($(echo "scale=1; $ESSENTIAL * 100 / $TOTAL" | bc)%)"
# Output: TYMS essential in 352 / 1446 screens (24.3%)

# Get cell lines where gene is essential
curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" | \
  jq -r '.[].SCREEN_ID' | sort -u | head -10 | tr '\n' '|' | sed 's/|$//' > screen_ids.txt

curl -s "https://orcsws.thebiogrid.org/screens/?accesskey=${BIOGRID_API_KEY}&screenID=$(cat screen_ids.txt)&format=json" | \
  jq '.[] | .CELL_LINE' | sort | uniq -c | sort -rn | head -10
```

**Context-dependent essentiality**: If a gene is essential in ~25% of screens, it's likely synthetic lethal with a genetic background present in ~25% of cancer cell lines.

## Scoring Methods

| Method | Description | Interpretation |
|--------|-------------|----------------|
| **CERES** | Computational correction for copy number effects | Most common, negative = essential |
| **Kolmogorov-Smirnov** | Statistical enrichment test | Log p-value, higher = more significant |
| **MAGeCK** | Model-based Analysis of Genome-wide CRISPR | Negative = depletion = essential |
| **BAGEL** | Bayesian Analysis of Gene EssentiaLity | Bayes Factor, positive = essential |

## Common Pitfalls

1. **Wrong endpoint**: Use `orcsws.thebiogrid.org` (NOT `orcs.thebiogrid.org`)
2. **Missing API key**: Check `.env` file first: `grep BIOGRID_API_KEY .env`
3. **Missing hit filter**: Always use `hit=yes` to filter to essential screens only
4. **Gene identifiers**: Always use Entrez IDs (not gene symbols) for `/gene/{id}` endpoint
5. **Screen metadata**: Query `/screens/?screenID=...` to get cell line and PubMed data
6. **Batch screen queries**: Use pipe-separated IDs: `/screens/?screenID=16|17|141`

## Complete Example

See [references/biogrid-orcs-validation.md](references/biogrid-orcs-validation.md) for a complete worked example validating DHODH/VHL synthetic lethality from a Science Advances paper.

**Result**: 2/4 VHL-mutant lines show significant DHODH dependency (context-dependent penetrance).

## Python Code Patterns

For programmatic access, use these patterns from `kg_rememberall/notebooks/biogrid_orcs_api.ipynb`:

### Query Gene Essentiality

```python
import requests

BIOGRID_API_KEY = os.getenv("BIOGRID_API_KEY")
BASE_URL = "https://orcsws.thebiogrid.org"

def get_essential_screens(entrez_id: int) -> list[dict]:
    """Get screens where gene is essential (hit=yes)."""
    response = requests.get(
        f"{BASE_URL}/gene/{entrez_id}",
        params={
            "accesskey": BIOGRID_API_KEY,
            "hit": "yes",
            "format": "json"
        }
    )
    return response.json()

# Example: Get TYMS (Entrez 7298) essential screens
essential_screens = get_essential_screens(7298)
print(f"TYMS essential in {len(essential_screens)} screens")
# Output: TYMS essential in 352 screens
```

### Get Screen Annotations with PubMed

```python
def get_screen_annotations(screen_ids: list[str]) -> list[dict]:
    """Get cell line and publication data for screens."""
    response = requests.get(
        f"{BASE_URL}/screens/",
        params={
            "accesskey": BIOGRID_API_KEY,
            "screenID": "|".join(screen_ids),
            "format": "json"
        }
    )
    return response.json()

# Extract unique screen IDs from essential screens
screen_ids = list(set(s["SCREEN_ID"] for s in essential_screens))

# Get annotations (batched)
annotations = get_screen_annotations(screen_ids[:20])  # First 20

for a in annotations[:5]:
    print(f"Screen {a['SCREEN_ID']}: {a['CELL_LINE']} - PMID:{a['SOURCE_ID']} ({a['AUTHOR']})")
```

### Calculate Essentiality Rate

```python
def calculate_essentiality_rate(entrez_id: int) -> tuple[int, int, float]:
    """Calculate what % of screens show gene as essential."""
    # Get all screens
    all_screens = requests.get(
        f"{BASE_URL}/gene/{entrez_id}",
        params={"accesskey": BIOGRID_API_KEY, "format": "json"}
    ).json()

    # Get essential screens only
    essential = requests.get(
        f"{BASE_URL}/gene/{entrez_id}",
        params={"accesskey": BIOGRID_API_KEY, "hit": "yes", "format": "json"}
    ).json()

    total = len(all_screens)
    essential_count = len(essential)
    rate = essential_count / total * 100 if total > 0 else 0

    return essential_count, total, rate

# Example
essential, total, rate = calculate_essentiality_rate(7298)
print(f"TYMS: {essential}/{total} screens ({rate:.1f}%) show essentiality")
# Output: TYMS: 352/1446 screens (24.3%) show essentiality
```

## Integration with Life Sciences MCPs

**Workflow:**
1. Use HGNC or Entrez MCP to resolve gene symbols to Entrez IDs
2. Query ORCS for essentiality data using Entrez IDs
3. Analyze dependency scores across cell lines
4. Validate synthetic lethality hypotheses

**Example:**
```python
# Phase 1: Use MCP to get Entrez ID
hgnc_result = await client.call_tool("hgnc_search_genes", {"query": "DHODH"})
gene = await client.call_tool("hgnc_get_gene", {"hgnc_id": hgnc_result["items"][0]["id"]})
entrez_id = gene["cross_references"]["entrez"]  # "1723"

# Phase 2-5: Use curl with ORCS (see workflow above)
```

## References

- **BioGRID ORCS**: https://orcs.thebiogrid.org/
- **API Key**: https://webservice.thebiogrid.org/
- **Meyers RM et al. 2017**: CERES methodology (PMID: 29083409)
- **Complete Example**: [references/biogrid-orcs-validation.md](references/biogrid-orcs-validation.md)

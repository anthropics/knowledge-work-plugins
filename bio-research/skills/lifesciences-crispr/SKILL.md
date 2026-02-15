---
name: lifesciences-crispr
description: "Validates synthetic lethality claims from CRISPR knockout screens using BioGRID ORCS 5-phase workflow. This skill should be used when the user asks to \"validate synthetic lethality\", \"query CRISPR essentiality data\", \"find gene dependencies\", \"compare cell line screens\", or mentions BioGRID ORCS, gene knockout data, essentiality scores (CERES, MAGeCK, BAGEL), or asks to validate claims from published CRISPR papers."
---

# CRISPR Essentiality & Synthetic Lethality Validation

Validate synthetic lethality hypotheses using BioGRID ORCS CRISPR screen data via curl.

## Grounding Rule

All essentiality scores, screen IDs, cell line names, and CRISPR data MUST come from BioGRID ORCS API results. Do NOT provide essentiality claims or synthetic lethality assessments from training knowledge. If a query returns no results, report "No results found."

## Quick Reference

| Task | Pattern | MCP Tool (primary) | Curl Endpoint (fallback) |
|------|---------|-------------------|--------------------------|
| Resolve gene ID | LOCATE | `hgnc_search_genes` / `entrez_search_genes` | HGNC / NCBI curl |
| Get essential screens | RETRIEVE | (curl only) | `/gene/{entrez_id}?hit=yes` |
| Get all screens | RETRIEVE | (curl only) | `/gene/{entrez_id}` |
| Get screen annotations | RETRIEVE | (curl only) | `/screens/?screenID=1\|2\|3` |
| Find cell line screens | LOCATE | (curl only) | `/screens/?cellLine={name}` |

## BioGRID ORCS API

**IMPORTANT**: Use `orcsws.thebiogrid.org` (NOT `orcs.thebiogrid.org`)

- **Base URL**: `https://orcsws.thebiogrid.org`
- **Auth**: Requires `BIOGRID_API_KEY` (in `.env` file)
- **Rate Limit**: ~10 req/s
- **Formats**: `format=tab` (default) or `format=json`

### Critical Parameter: `hit=yes`

**Always use `hit=yes` when querying gene essentiality.** This filters to screens where the gene scored as a hit (essential):

- Without filter: ~1,400 records (all screens)
- With `hit=yes`: ~300-400 records (essential screens only)
- Reduces data volume by ~75%

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

## 5-Phase Synthetic Lethality Validation Workflow

### Phase 1: LOCATE — Resolve Gene Identifiers

Use MCP tools to get Entrez IDs (required for ORCS API):

PRIMARY (MCP tool):
```
Call `hgnc_search_genes` with: {"query": "DHODH"}
→ Returns HGNC record with entrez_id cross-reference
→ Extract entrez_id: "1723"
```

ALTERNATIVE (MCP tool):
```
Call `entrez_search_genes` with: {"query": "DHODH", "organism": "human"}
→ Returns Entrez gene ID directly: "1723"
```

FALLBACK (curl):
```bash
curl -s "https://rest.genenames.org/search/symbol/DHODH" \
  -H "Accept: application/json" | jq '.response.docs[0] | {hgnc_id, symbol, entrez_id}'
```

### Phase 2: RETRIEVE — Query ORCS for Essential Screens Only

**CRITICAL: Always use `hit=yes`**:

```bash
# RETRIEVE: Get ONLY screens where gene is essential
curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" > gene_essential.json

# Count essential screens
cat gene_essential.json | jq '. | length'
# Output: 352 (vs 1,446 without hit=yes filter)
```

### Phase 3: RETRIEVE — Get Screen Annotations (Cell Lines & PubMed)

Two-step pattern: query gene for screen IDs, then query screens for annotations.

```bash
# Step 3a: Extract unique screen IDs from essential screens
SCREEN_IDS=$(curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" | \
  jq -r '.[].SCREEN_ID' | sort -u | head -20 | tr '\n' '|' | sed 's/|$//')

# Step 3b: RETRIEVE screen annotations (cell line, PubMed, author)
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

### Phase 4: RETRIEVE — Extract Dependency Scores

```bash
# RETRIEVE: Get essential screens with scores
curl -s "https://orcsws.thebiogrid.org/gene/7298?accesskey=${BIOGRID_API_KEY}&hit=yes&format=json" | \
  jq '.[] | select(.SCREEN_ID == "16" or .SCREEN_ID == "17") | {SCREEN_ID, SCORE: .["SCORE.1"], symbol: .OFFICIAL_SYMBOL}'
```

**Score interpretation:**
- **HIT = YES** = gene is essential in this screen
- **Positive BAGEL score** = essential (Bayes Factor)
- **Negative CERES score** = essential (depletion)
- Different screens use different scoring methods (check screen metadata)

### Phase 5: RETRIEVE — Compare Across Genetic Backgrounds

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

## ID Format Reference

| Database | API Argument (bare) | Graph CURIE | Example |
|----------|---------------------|-------------|---------|
| NCBI/Entrez | `7298` | `NCBIGene:7298` | Bare numeric for ORCS API |
| HGNC | `HGNC:11998` | `HGNC:11998` | Includes prefix |
| BioGRID Screen | `16` | N/A | Numeric screen ID |

## Common Pitfalls

1. **Wrong endpoint**: Use `orcsws.thebiogrid.org` (NOT `orcs.thebiogrid.org`)
2. **Missing API key**: Check first: `grep BIOGRID_API_KEY .env`
3. **Missing hit filter**: Always use `hit=yes` to filter to essential screens only
4. **Gene identifiers**: Always use Entrez IDs (not gene symbols) for `/gene/{id}` endpoint
5. **Screen metadata**: Query `/screens/?screenID=...` to get cell line and PubMed data
6. **Batch screen queries**: Use pipe-separated IDs: `/screens/?screenID=16|17|141`

## Integration with Fuzzy-to-Fact Protocol

In the context of the lifesciences-graph-builder workflow:
1. **ANCHOR phase**: Use `hgnc_search_genes` MCP tool to LOCATE gene → get Entrez ID from cross-references
2. **EXPAND phase**: Query ORCS with Entrez ID (this skill's Phase 2-5)
3. **VALIDATE phase**: Verify screen IDs and cell line data
4. **PERSIST phase**: Include essentiality edges in knowledge graph

## See Also

- **lifesciences-graph-builder**: Orchestrator for full Fuzzy-to-Fact protocol
- **lifesciences-genomics**: Gene resolution endpoints (HGNC, Ensembl, NCBI)

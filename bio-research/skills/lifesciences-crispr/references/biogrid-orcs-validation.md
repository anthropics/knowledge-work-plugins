# DHODH/VHL Synthetic Lethality Validation Example

## Background

**Paper**: Science Advances - "Genome-wide CRISPR screens using isogenic cells reveal vulnerabilities conferred by loss of tumor suppressors"

**Claim**: DHODH (dihydroorotate dehydrogenase) is synthetic lethal with VHL (Von Hippel-Lindau) loss in clear cell renal cell carcinoma.

**Goal**: Validate this claim using BioGRID ORCS CRISPR screen data.

## Complete Validation Workflow

### Phase 1: Resolve Gene Identifiers

Use Life Sciences MCPs to get Entrez IDs:

```bash
# Using HGNC MCP
# search_genes(query="DHODH") → get_gene(hgnc_id="HGNC:2867")
# Extract from cross_references: {"entrez": "1723"}

# Using Entrez MCP
# search_genes(query="DHODH") → top result: "NCBIGene:1723"
# Extract Entrez ID: 1723
```

**Result**:
- DHODH → Entrez ID: `1723`
- VHL → Entrez ID: `7428`

### Phase 2: Query ORCS for DHODH Essentiality Data

```bash
# Get all CRISPR screens where DHODH was scored
curl -s "https://orcsws.thebiogrid.org/gene/1723?accesskey=${BIOGRID_API_KEY}" > dhodh_screens.tsv

# Count screens
wc -l dhodh_screens.tsv
# Output: 232 screens
```

**Result**: DHODH has been scored in 232 published CRISPR screens.

### Phase 3: Identify VHL-mutant Cell Line Screens

From the paper, VHL-mutant ccRCC cell lines mentioned:
- 786-O
- ACHN
- UMRC6
- Caki-2

Query ORCS for these cell lines:

```bash
# Find 786-O screens
curl -s "https://orcsws.thebiogrid.org/screens/?cellLine=786-O&accesskey=${BIOGRID_API_KEY}"
# Output: Screen 213 (Meyers RM 2017, CERES score)

# Find Caki-2 screens
curl -s "https://orcsws.thebiogrid.org/screens/?cellLine=Caki-2&accesskey=${BIOGRID_API_KEY}"
# Output: Screen 512 (Meyers RM 2017, CERES score)

# Also found: Caki-1 (Screen 511) - another VHL-mutant ccRCC line
```

**Result**:
| Cell Line | Screen ID | Publication | Score Type | VHL Status |
|-----------|-----------|-------------|------------|------------|
| 786-O | 213 | Meyers RM 2017 | CERES | VHL-mutant |
| Caki-1 | 511 | Meyers RM 2017 | CERES | VHL-mutant |
| Caki-2 | 512 | Meyers RM 2017 | CERES | VHL-mutant |
| OS-RC-2 | 409 | Meyers RM 2017 | CERES | VHL-mutant |

### Phase 4: Extract DHODH Dependency Scores

```bash
# Extract DHODH scores for VHL-mutant screens
curl -s "https://orcsws.thebiogrid.org/gene/1723?accesskey=${BIOGRID_API_KEY}" | \
grep -E "^213\s|^511\s|^512\s|^409\s" | \
awk 'BEGIN{FS="\t"} {print "Screen " $1 ": score=" $8 ", FDR=" $9}'

# Output:
# Screen 213: score=-0.376514964, FDR=0.0452
# Screen 511: score=-0.556, FDR=0.036
# Screen 512: score=-0.315275949435, FDR=0.209
# Screen 409: score=-0.306, FDR=0.0975
```

**Result**:
- **786-O**: DHODH score = -0.377, FDR = 0.0452 ✅ Significant
- **Caki-1**: DHODH score = -0.556, FDR = 0.036 ✅ Significant
- **Caki-2**: DHODH score = -0.315, FDR = 0.209 ❌ Not significant
- **OS-RC-2**: DHODH score = -0.306, FDR = 0.0975 ❌ Not significant

### Phase 5: Compare Across Genetic Backgrounds

Find other renal cancer cell lines for comparison:

```bash
# Find all renal cancer screens
curl -s "https://orcsws.thebiogrid.org/screens/?accesskey=${BIOGRID_API_KEY}" | \
grep -i "renal" | \
awk 'BEGIN{FS="\t"} {print "Screen " $1 ": " $25 " - " $26}'

# Output (sample):
# Screen 204: TUHR4TKB - Renal Cell Carcinoma Cell Line
# Screen 205: TUHR10TKB - Renal Cell Carcinoma Cell Line
# Screen 318: KMRC-1 - Renal Cell Carcinoma Cell Line
```

Extract DHODH scores for all renal cancer lines:

```bash
curl -s "https://orcsws.thebiogrid.org/gene/1723?accesskey=${BIOGRID_API_KEY}" | \
grep -E "^204\s|^205\s|^318\s|^409\s|^511\s|^213\s|^512\s" | \
awk 'BEGIN{FS="\t"} {print "Screen " $1 ": score=" $6 ", FDR=" $18}'
```

**Complete Comparison Table**:

| Cell Line | Screen | DHODH Score | FDR | Significant? | VHL Status |
|-----------|--------|-------------|-----|--------------|------------|
| **Caki-1** | 511 | **-0.556** | **0.036** | ✅ **YES** | VHL-mutant |
| **786-O** | 213 | **-0.377** | **0.0452** | ✅ **YES** | VHL-mutant |
| KMRC-1 | 318 | -0.363 | 0.159 | ❌ No | Unknown |
| TUHR10TKB | 205 | -0.348 | 0.139 | ❌ No | Unknown |
| Caki-2 | 512 | -0.315 | 0.209 | ❌ No | VHL-mutant |
| OS-RC-2 | 409 | -0.306 | 0.0975 | ❌ No | VHL-mutant |
| TUHR4TKB | 204 | -0.294 | 0.19 | ❌ No | Unknown |

## Validation Results

### Key Findings

1. **Partial Validation**: 2 of 4 VHL-mutant lines show significant DHODH dependency
   - 786-O: FDR = 0.0452 (p < 0.05) ✅
   - Caki-1: FDR = 0.036 (p < 0.05) ✅

2. **Context-Dependent Penetrance**: Not all VHL-mutant lines show the phenotype
   - Caki-2: FDR = 0.209 (not significant)
   - OS-RC-2: FDR = 0.0975 (borderline)

3. **Strongest Effect**: Caki-1 shows the most significant DHODH dependency (-0.556, FDR = 0.036)

### Interpretation

**Supporting Evidence**:
- Two independent VHL-mutant lines (786-O, Caki-1) show statistically significant DHODH dependency
- Both lines are well-characterized ccRCC models with confirmed VHL mutations
- CERES scores indicate DHODH is essential in these contexts

**Caveats**:
- Incomplete penetrance suggests additional factors beyond VHL status
- Possible explanations:
  - Different experimental conditions across screens
  - Compensatory metabolic pathways in some lines
  - Secondary mutations affecting pyrimidine biosynthesis
  - Cell line-specific dependencies

**Conclusion**: ORCS data **partially validates** the paper's DHODH/VHL synthetic lethality claim. The effect is significant in specific VHL-mutant contexts (786-O, Caki-1) but not universal across all VHL-mutant ccRCC lines.

## Best Practices Learned

1. **Always use Entrez IDs** - Gene symbols can be ambiguous
2. **Check `.env` first** - Don't assume no API key exists
3. **Use correct endpoint** - `orcsws.thebiogrid.org` not `orcs.thebiogrid.org`
4. **Don't use format=json** - Causes API key format errors
5. **Query screens first** - Use `/screens/?cellLine={name}` to get Screen IDs before querying gene data
6. **Validate with multiple lines** - Single cell line isn't sufficient for strong claims
7. **Consider biological context** - Synthetic lethality can be context-dependent

## Command Summary

```bash
# 1. Get gene identifiers (using Life Sciences MCPs)
# DHODH → 1723, VHL → 7428

# 2. Download DHODH screen data
curl -s "https://orcsws.thebiogrid.org/gene/1723?accesskey=${BIOGRID_API_KEY}" > dhodh.tsv

# 3. Find VHL-mutant cell line screens
curl -s "https://orcsws.thebiogrid.org/screens/?cellLine=786-O&accesskey=${BIOGRID_API_KEY}"
curl -s "https://orcsws.thebiogrid.org/screens/?cellLine=Caki-1&accesskey=${BIOGRID_API_KEY}"

# 4. Extract DHODH scores for those screens
grep "^213\s" dhodh.tsv | awk 'BEGIN{FS="\t"} {print $8, $9}'
grep "^511\s" dhodh.tsv | awk 'BEGIN{FS="\t"} {print $8, $9}'

# 5. Compare with other renal cancer lines
curl -s "https://orcsws.thebiogrid.org/screens/?accesskey=${BIOGRID_API_KEY}" | grep -i "renal"
grep -E "^204\s|^205\s|^318\s" dhodh.tsv
```

## References

- **BioGRID ORCS**: https://orcs.thebiogrid.org/
- **Meyers RM et al. 2017**: "Computational correction of copy number effect improves specificity of CRISPR-Cas9 essentiality screens in cancer cells" (PMID: 29083409)
- **Science Advances Paper**: "Genome-wide CRISPR screens using isogenic cells reveal vulnerabilities conferred by loss of tumor suppressors"

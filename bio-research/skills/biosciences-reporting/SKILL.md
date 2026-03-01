---
name: biosciences-reporting
description: "Formats professional reports from Fuzzy-to-Fact pipeline output using domain-specific templates, claim-level evidence grading, and standardized citations. This skill should be used when the user asks to \"format a report\", \"summarize findings\", \"grade evidence\", \"write up results\", or mentions report templates, confidence scoring, evidence levels, or presentation of pipeline output."
---

# Biosciences Reporting

Format professional reports from Fuzzy-to-Fact pipeline output using domain-specific templates.

## Grounding Rule

```
ALL claims in the report MUST trace to specific tool calls from Phases 1-5.
Do NOT introduce new entities, drug names, gene functions, or trial IDs from
training knowledge during report generation. The report SYNTHESIZES existing
Phase 1-5 output — it does NOT generate new facts.

If a Phase returned no results for a section, report "No data retrieved" with
the tool name that was called. Do NOT fill gaps from memory.
```

## Scope

**In scope**: Template selection, evidence grading, source attribution, formatting, synthesis of Phase 1-5 output.

**Out of scope**: API calls, data retrieval, new entity resolution, creating new Fuzzy-to-Fact phases, modifying other skills. This skill consumes pipeline output — it does not produce it.

## Template Decision Tree

Route the user's query to the appropriate template using this priority order. If multiple categories apply, combine sections from relevant templates (see Multi-Template Combination below).

```
1. HOW does a drug work?              --> Template 6: Mechanism Elucidation
2. Drug SAFETY or off-targets?        --> Template 7: Safety / Off-Target
3. REGULATORY milestones or filings?  --> Template 5: Regulatory / Commercialization
4. FIND or REPURPOSE drugs?           --> Template 1: Drug Discovery / Repurposing
5. GENE/PROTEIN interactions?         --> Template 2: Gene / Protein Network
6. CLINICAL TRIALS broadly?           --> Template 3: Clinical Landscape
7. VALIDATE a target?                 --> Template 4: Target Validation
8. Multiple categories?               --> Combine sections from relevant templates
```

### Competency Question Coverage

| Template | Covers CQs | Primary Signal |
|----------|-----------|----------------|
| 1. Drug Discovery / Repurposing | cq2, cq4, cq7, cq8, cq10, cq14 | "repurpose", "find drugs", "therapeutic strategies" |
| 2. Gene / Protein Network | cq3, cq5, cq6 | "interact", "regulate", "network", "cascade" |
| 3. Clinical Landscape | cq12 | "clinical trials broadly", "health priorities" |
| 4. Target Validation | cq11 | "validate target", "druggability", "tractability" |
| 5. Regulatory / Commercialization | cq13, cq15 | "commercialization", "regulatory", "FDA", "EMA" |
| 6. Mechanism Elucidation | cq1 | "mechanism", "how does X work" |
| 7. Safety / Off-Target | cq9 | "off-target", "safety", "cardiotoxicity", "selectivity" |

---

## Template 1: Drug Discovery / Repurposing

Use for: cq2 (FOP repurposing), cq4 (AD therapeutics), cq7 (NGLY1 multi-hop), cq8 (ARID1A SL), cq10 (HD novel targets), cq14 (TP53 SL).

```markdown
## Summary
[Direct answer: what drugs were found and why they are relevant]

## Resolved Entities
| Entity | CURIE | Type | Source |
|--------|-------|------|--------|
| [name] | [CURIE] | Gene/Protein/Disease | [Source: tool(param)] |

## Drug Candidates
| Drug | CURIE | Phase | Mechanism | Target | Evidence Level | Source |
|------|-------|-------|-----------|--------|---------------|--------|
| [name] | [CURIE] | [1-4] | [action] | [gene] | [L1-L4] | [Source: tool(param)] |

## Mechanism Rationale
[For each drug: why this drug targets the disease pathway.
Trace: Drug --[mechanism]--> Target --[pathway]--> Disease]

## Clinical Trials
| NCT ID | Title | Phase | Status | Verified | Source |
|--------|-------|-------|--------|----------|--------|
| [ID] | [title] | [phase] | [status] | [Y/N] | [Source: tool(param)] |

## Evidence Assessment
[Claim-level grades using the Evidence Grading System below]

## Gaps and Limitations
[What was NOT found; which tools returned no results]
```

## Template 2: Gene / Protein Network

Use for: cq3 (AD gene networks), cq5 (MAPK cascade), cq6 (BRCA1 regulatory network).

```markdown
## Summary
[Direct answer: what network was found and its biological significance]

## Resolved Entities
| Entity | CURIE | Type | Source |
|--------|-------|------|--------|
| [name] | [CURIE] | Gene/Protein | [Source: tool(param)] |

## Interaction Network
| Protein A | Protein B | Score | Type | Direction | Source |
|-----------|-----------|-------|------|-----------|--------|
| [name] | [name] | [0-1000] | [physical/regulatory] | [A->B / bidirectional] | [Source: tool(param)] |

## Hub Genes
| Gene | Degree | Key Interactions | Disease Associations | Source |
|------|--------|------------------|---------------------|--------|
| [name] | [N] | [top partners] | [diseases] | [Source: tool(param)] |

## Pathway Membership
| Pathway | ID | Member Genes from Query | Source |
|---------|-----|------------------------|--------|
| [name] | [WP:ID] | [gene list] | [Source: tool(param)] |

## Network Properties
- Total nodes: [N]
- Total edges: [N]
- Average interaction score: [N]
- Regulatory vs physical: [ratio]

## Evidence Assessment
[Claim-level grades]

## Gaps and Limitations
[Missing interactions, low-confidence edges, unresolved entities]
```

### Template 2 Notes
- **Disease CURIE**: Not required in Resolved Entities table unless drug/trial discovery was performed
- **Pathway Membership**: REQUIRED section (use WikiPathways for all core genes)
- **Clinical Trials**: Only include if relevant to the comparative network question
- **Source Attribution**: Paraphrasing UniProt function text is acceptable; cite the tool call

## Template 3: Clinical Landscape

Use for: cq12 (health emergencies 2026).

```markdown
## Summary
[Direct answer: what clinical trial patterns were found]

## Phase Distribution
| Phase | Count | Top Conditions | Source |
|-------|-------|---------------|--------|
| Phase 3 | [N] | [conditions] | [Source: tool(param)] |
| Phase 2 | [N] | [conditions] | [Source: tool(param)] |
| Phase 1 | [N] | [conditions] | [Source: tool(param)] |

## Recruiting Trials
| NCT ID | Condition | Intervention | Phase | Sponsor | Source |
|--------|-----------|-------------|-------|---------|--------|
| [ID] | [condition] | [drug/device] | [phase] | [org] | [Source: tool(param)] |

## Therapeutic Trends
| Trend | Trial Count | Representative Trials | Source |
|-------|------------|----------------------|--------|
| [e.g., CAR-T expansion] | [N] | [NCT IDs] | [Source: tool(param)] |

## Evidence Assessment
[Claim-level grades]

## Gaps and Limitations
[Search coverage, date range caveats, missing trial types]
```

## Template 4: Target Validation

Use for: cq11 (p53-MDM2-Nutlin axis).

```markdown
## Summary
[Direct answer: is this target validated and druggable?]

## Target Profile
| Property | Value | Source |
|----------|-------|--------|
| Gene Symbol | [symbol] | [Source: tool(param)] |
| CURIE | [HGNC:ID] | [Source: tool(param)] |
| Protein | [UniProt ID] | [Source: tool(param)] |
| Function | [text from UniProt] | [Source: tool(param)] |
| Biotype | [protein_coding/etc] | [Source: tool(param)] |

## Disease Associations
| Disease | Score | Evidence Sources | Source |
|---------|-------|-----------------|--------|
| [name] | [0-1] | [genetic, literature, etc] | [Source: tool(param)] |

## Tractability Assessment
| Modality | Label | Value | Source |
|----------|-------|-------|--------|
| Small molecule | [Clinical Precedence/etc] | [score] | [Source: tool(param)] |
| Antibody | [label] | [score] | [Source: tool(param)] |

## Known Drugs
| Drug | Phase | Mechanism | Source |
|------|-------|-----------|--------|
| [name] | [1-4] | [action] | [Source: tool(param)] |

## Interaction Partners
| Partner | Score | Type | Source |
|---------|-------|------|--------|
| [name] | [0-1000] | [physical/regulatory] | [Source: tool(param)] |

## Evidence Assessment
[Claim-level grades]

## Gaps and Limitations
[Missing tractability data, low-confidence associations]
```

## Template 5: Regulatory / Commercialization

Use for: cq13 (high-commercialization trials), cq15 (CAR-T regulatory).

```markdown
## Summary
[Direct answer: which trials or drugs have highest commercial/regulatory momentum?]

## Resolved Entities
| Entity | CURIE | Type | Source |
|--------|-------|------|--------|
| [name] | [CURIE] | Drug/Trial | [Source: tool(param)] |

## Milestone Timeline
| Trial/Drug | Event | Date/Status | Significance | Source |
|-----------|-------|-------------|-------------|--------|
| [name] | [Phase 3 initiation/BLA filing/etc] | [date] | [first-in-class/etc] | [Source: tool(param)] |

## Competitive Landscape
| Target | Drug | Sponsor | Phase | Status | Source |
|--------|------|---------|-------|--------|--------|
| [target] | [drug] | [company] | [phase] | [recruiting/completed] | [Source: tool(param)] |

## Investment Signals
| Signal | Trial/Drug | Evidence | Source |
|--------|-----------|----------|--------|
| [large enrollment/breakthrough designation/etc] | [name] | [detail] | [Source: tool(param)] |

## Evidence Assessment
[Claim-level grades]

## Gaps and Limitations
[Regulatory data not in ClinicalTrials.gov, proprietary deal data unavailable]
```

## Template 6: Mechanism Elucidation

Use for: cq1 (Palovarotene mechanism for FOP).

```markdown
## Summary
[Direct answer: by what mechanism does Drug X treat Disease Y?]

## Mechanism Chain
[Narrative tracing the path: Drug --[action]--> Target --[regulation]--> Pathway --[association]--> Disease]

### Step-by-Step
| Step | From | Relationship | To | Evidence | Source |
|------|------|-------------|-----|----------|--------|
| 1 | [Drug] | [agonist/inhibitor] | [Target protein] | [mechanism data] | [Source: tool(param)] |
| 2 | [Target] | [regulates/inhibits] | [Downstream] | [interaction data] | [Source: tool(param)] |
| 3 | [Downstream] | [associated_with] | [Disease] | [association data] | [Source: tool(param)] |

## Supporting Evidence
| Claim | Evidence Level | Sources |
|-------|---------------|---------|
| [Drug is agonist of Target] | [L3] | [Source: tool(param)] |
| [Target regulates Downstream] | [L2] | [Source: tool(param)] |

## Alternative Mechanisms
[Other proposed mechanisms from literature, if retrieved]

## Evidence Assessment
[Claim-level grades]

## Gaps and Limitations
[Missing pathway steps, unconfirmed regulatory direction]
```

## Template 7: Safety / Off-Target

Use for: cq9 (Dasatinib off-target risks).

```markdown
## Summary
[Direct answer: what are the safety risks of Drug X?]

## Index Compound Profile
| Property | Value | Source |
|----------|-------|--------|
| Drug Name | [name] | [Source: tool(param)] |
| CURIE | [CHEMBL:ID] | [Source: tool(param)] |
| Primary Target(s) | [target list] | [Source: tool(param)] |
| Approved Indication(s) | [diseases] | [Source: tool(param)] |

## Off-Target Hits
| Off-Target | Gene CURIE | Activity (IC50/Ki) | Clinical Consequence | Source |
|-----------|-----------|-------------------|---------------------|--------|
| [protein] | [HGNC:ID] | [nM] | [e.g., cardiotoxicity] | [Source: tool(param)] |

## Selectivity Comparison
| Target | Drug X (IC50) | Comparator Drug (IC50) | Selectivity Ratio | Source |
|--------|--------------|----------------------|-------------------|--------|
| [primary] | [nM] | [nM] | [ratio] | [Source: tool(param)] |
| [off-target] | [nM] | [nM] | [ratio] | [Source: tool(param)] |

## Safety Signals
| Signal | Mechanism | Severity | Frequency | Source |
|--------|-----------|----------|-----------|--------|
| [e.g., QT prolongation] | [hERG inhibition] | [serious] | [common/rare] | [Source: tool(param)] |

## Evidence Assessment
[Claim-level grades]

## Gaps and Limitations
[Missing activity data, untested off-targets, post-market data not available]
```

---

## Evidence Grading System

Grade **each claim** individually, then compute an overall report confidence. This prevents inflated "high confidence" when some claims are grounded and others are not.

### Evidence Levels

| Level | Range | Name | Criteria |
|-------|-------|------|----------|
| L4 | 0.90-1.00 | Clinical | FDA-approved drug for this indication, OR Phase 2+ trial with published endpoints |
| L3 | 0.70-0.89 | Functional | Multi-database concordance + druggable target + known mechanism of action |
| L2 | 0.50-0.69 | Multi-DB | 2+ independent API endpoints confirm the relationship (see Same-API Note below) |
| L1 | 0.30-0.49 | Single-DB | One database source only |

### Modifiers

| Modifier | Adjustment | Condition |
|----------|------------|-----------|
| Active trial | +0.10 | Recruiting trial targets this entity/mechanism |
| Mechanism match | +0.10 | Drug mechanism aligns with disease biology (e.g., inhibitor for gain-of-function) |
| Literature support | +0.05 | PubMed or Entrez links confirm relationship |
| High STRING score | +0.05 | STRING interaction score >= 900 |
| Conflicting evidence | -0.10 | Databases disagree on relationship direction or existence |
| Single source | -0.10 | Only one API returned this data point |
| Unverified ID | -0.15 | CURIE not confirmed via LOCATE step |
| Mechanism mismatch | -0.20 | Drug action contradicts disease biology (e.g., agonist for gain-of-function) |

### Same-API Annotation Note (L2 Threshold)

**L2 requires two independent API sources**, not two fields from the same API call. Common pitfall:

- **Wrong**: "UniProt subcellular_location says Lysosome + UniProt GO annotation says GO:0005764 = L2 (two sources)". Both come from the same `uniprot_get_protein` call.
- **Right**: Score as **L1 (0.45)** with `+0.05 literature support` modifier for the embedded GO cross-reference. Final: 0.50 (top of L1 range).
- **True L2**: UniProt subcellular_location confirms lysosomal localization AND an independent Human Protein Atlas or Gene Ontology database query also confirms it.

Rule of thumb: if both data points come from a single `curl` or MCP tool call, they are the same source for grading purposes. Apply `+0.05 literature support` for structured cross-references (GO terms, Reactome IDs) embedded in the response.

### Grading Procedure

For each claim in the report:

1. **Identify the base level** (L1-L4) from the criteria above
2. **Apply all applicable modifiers** (sum adjustments, clamp to 0.00-1.00)
3. **Record the final score and justification**

For the overall report:
- Compute the **median** of all claim scores (not the mean — resistant to outliers)
- Report the **range** (lowest to highest claim score)
- Flag any claim below L1 (0.30) as "Insufficient Evidence"

### Worked Example: Venetoclax/BCL2

**Claim**: "Venetoclax inhibits BCL2 and is approved for CLL"

1. Base: **L4** (0.90) — FDA-approved drug for this indication
2. Modifiers:
   - Active trials: +0.10 (multiple recruiting CLL trials found via `clinicaltrials_search_trials`)
   - Multi-DB: already captured in L4 base
3. Final: **0.95 (L4 Clinical)**
4. Sources: `[Source: opentargets_get_target(ENSG00000171791)]`, `[Source: clinicaltrials_search_trials("venetoclax CLL")]`

**Claim**: "BCL2 interacts with BAX (STRING score 0.999)"

1. Base: **L2** (0.55) — confirmed by STRING
2. Modifiers:
   - High STRING score: +0.05 (score >= 900)
   - UniProt function text mentions BAX: +0.05 (literature support)
3. Final: **0.65 (L2 Multi-DB)**
4. Sources: `[Source: string_get_interactions(9606.ENSP00000381185)]`, `[Source: uniprot_get_protein(Q07817)]`

---

## Source Attribution Standards

Every factual claim must cite the tool call that produced it. Formats:

| Context | Format | Example |
|---------|--------|---------|
| MCP tool | `[Source: tool(param)]` | `[Source: hgnc_search_genes("TP53")]` |
| Curl | `[Source: curl endpoint(param)]` | `[Source: curl OpenTargets/graphql(knownDrugs, ENSG00000171791)]` |
| Multi-source | `[Sources: tool1(p1), tool2(p2)]` | `[Sources: hgnc_get_gene(HGNC:11998), uniprot_get_protein(P04637)]` |
| No data | `[No data: tool(param) returned error/0]` | `[No data: chembl_get_compound(CHEMBL3137309) returned 500]` |

---

## Formatting Standards

### Table Conventions
- CURIE column: always present for entities, using full CURIE format (`HGNC:11998`, not `11998`)
- Source column: always the rightmost column
- Evidence Level column: use shorthand `L1`-`L4` in tables, expand in Evidence Assessment section
- Sort drug candidate tables by Phase (descending), then Evidence Level (descending)
- Sort interaction tables by Score (descending)

### First-Mention Rule
On first mention of any entity, include both the human-readable name and CURIE:
```
TP53 (HGNC:11998) encodes the p53 tumor suppressor protein (UniProtKB:P04637).
```
Subsequent mentions may use the name alone.

### Markdown & General
- `## H2` for major sections, `### H3` for subsections, `#### H4` sparingly
- Tables for structured data; prose for narrative synthesis
- No emoji; dates in ISO 8601; scores to 2 decimal places; IC50/Ki in nM
- Abbreviations: define on first use, then abbreviate

---

## Common Report Pitfalls

### Hallucination Injection
**Problem**: Reporting fills in "expected" drug names or trial IDs from training knowledge when Phase 4a or 4b returned sparse results.

**Prevention**: Every row in Drug Candidates and Clinical Trials tables must have a `[Source: tool(param)]` citation. If no source exists, the row must not appear. Write "No drug candidates retrieved" rather than guessing.

### Inflated Confidence
**Problem**: Assigning L3/L4 evidence to claims supported by a single STRING interaction.

**Prevention**: Apply grading procedure strictly. A single-database claim is L1 (0.30-0.49) regardless of how "well known" the relationship seems. Modifiers can raise it, but only based on actual tool output.

### Wrong Template Selection
**Problem**: Using Drug Discovery template for a query about gene networks (cq3, cq5, cq6), producing empty Drug Candidates and Clinical Trials sections.

**Prevention**: Follow the decision tree. If the query mentions "interact", "regulate", "network", or "cascade" without mentioning drugs, use Template 2 (Gene/Protein Network).

### Unverified NCT IDs
**Problem**: Including NCT IDs from Phase 4b search results without Phase 5 verification.

**Prevention**: The "Verified" column in Clinical Trials tables must reflect Phase 5 output. If Phase 5 was not run, mark as "Unverified" (not "Yes").

### Mechanism Mismatch Blindness
**Problem**: For gain-of-function diseases, including agonists in Drug Candidates without flagging the mechanism conflict.

**Prevention**: Cross-reference the disease biology (from Phase 2 enrichment) with each drug's mechanism. Flag agonists for gain-of-function diseases with a -0.20 modifier and a note in Gaps and Limitations.

### Paraphrasing vs Hallucination Confusion
**Problem**: Reviewers flag faithful paraphrasing of UniProt function text as "hallucination" because the report text doesn't match verbatim.

**Acceptable synthesis** (not hallucination):
- UniProt function text paraphrased for readability: "Binds to 3 E-boxes of the E-cadherin/CDH1 gene promoter" → "binds E-boxes in CDH1 promoter"
- Multiple tool outputs synthesized into coherent narrative with all sources cited
- Interpretive claims clearly marked with qualifiers like "[Inferred from...]"

**Unacceptable** (hallucination):
- Entity names, CURIEs, or NCT IDs not present in tool outputs
- FDA approval years (e.g., "FDA-approved 2021"), prevalence statistics (e.g., ">50%"), or trial outcome numbers without sources
- Mechanistic details that extend beyond what tool output states

**Best practice**: Add a synthesis disclaimer to reports that paraphrase extensively:
> "Mechanism descriptions paraphrase UniProt function text and STRING interaction annotations. All synthesis is grounded in cited tool calls; no entities, CURIEs, or quantitative values are introduced from training knowledge."

### Combining Templates Poorly
**Problem**: Including all sections from two templates, creating a bloated report with redundant entity tables.

**Prevention**: Share Resolved Entities and Evidence Assessment across templates. Include unique sections from each. See Multi-Template Combination below.

---

## Multi-Template Combination

When a query spans multiple templates (e.g., cq2 involves both Drug Discovery and Mechanism Elucidation), combine them:

### Shared Sections (include once)
- Summary
- Resolved Entities
- Evidence Assessment
- Gaps and Limitations

### Template-Specific Sections (include from each relevant template)
Take the distinctive sections from each template. Do not duplicate entity tables.

### Worked Example: cq2 (FOP Drug Repurposing)

Query: "What drugs targeting the BMP pathway could be repurposed for FOP?"

**Templates**: Drug Discovery (primary) + Mechanism Elucidation (secondary)

Report structure:
1. Summary (shared)
2. Resolved Entities (shared)
3. Drug Candidates (from Template 1)
4. Mechanism Chain (from Template 6 — traces BMP pathway logic)
5. Mechanism Rationale (from Template 1 — per-drug justification)
6. Clinical Trials (from Template 1)
7. Evidence Assessment (shared — covers all claims)
8. Gaps and Limitations (shared)

---

## See Also

- **biosciences-graph-builder**: Orchestrator for full Fuzzy-to-Fact protocol (produces the data this skill formats)
- **biosciences-genomics**: HGNC, Ensembl, NCBI gene resolution (Phase 1-2 data sources)
- **biosciences-proteomics**: UniProt, STRING, BioGRID interaction data (Phase 2-3 data sources)
- **biosciences-pharmacology**: ChEMBL, PubChem, IUPHAR, Open Targets drug data (Phase 4a data sources)
- **biosciences-clinical**: Open Targets associations, ClinicalTrials.gov (Phase 4b-5 data sources)
- **biosciences-crispr**: BioGRID ORCS essentiality validation (Phase 3 extension)

---
name: biosciences-reporting-quality-review
description: "Structured quality review framework for Fuzzy-to-Fact life sciences reports. Evaluates reports against protocol requirements using template-specific criteria, distinguishes presentation failures from protocol failures, and applies consistent standards for paraphrasing vs hallucination. Use when the user asks to 'review this report', 'evaluate report quality', 'check protocol compliance', 'validate CQ report', or similar quality assessment requests."
---

# Report Quality Review Skill

Structured evaluation framework for assessing Fuzzy-to-Fact life sciences reports against protocol requirements.

## Critical Review Principles

```
1. READ KNOWLEDGE GRAPHS FIRST — Check graph JSON files before concluding protocol steps weren't executed
2. IDENTIFY TEMPLATE TYPE — Apply only dimensions relevant to the report's template (1-7)
3. DISTINGUISH FAILURES — "Not documented" ≠ "Not executed" ≠ "Protocol violation"
4. PARAPHRASING ≠ HALLUCINATION — UniProt function text paraphrased for readability is acceptable
5. TEMPLATE-SPECIFIC CRITERIA — Template 2 has different requirements than Template 1/4
```

## 5-Phase Review Workflow

### Phase 1: Context Gathering

**Goal**: Collect all artifacts needed for comprehensive evaluation.

**Required reads** (in order):
1. The report markdown file being reviewed
2. Associated knowledge graph JSON file (if exists) — usually `{report-name}-knowledge-graph.json`
3. The biosciences-graph-builder skill (invoke via Skill tool or read from `.claude/skills/biosciences-graph-builder/SKILL.md`)
4. The biosciences-reporting skill (invoke via Skill tool or read from `.claude/skills/biosciences-reporting/SKILL.md`)

**Optional reads** (if specific databases/tools are central to the report):
- biosciences-pharmacology skill (for drug discovery reports)
- biosciences-clinical skill (for target validation reports)
- biosciences-proteomics skill (for interaction network reports)

**Pitfall**: Reviewing only the markdown report without checking the knowledge graph leads to false failures. Many protocol steps execute correctly but aren't documented in the final report.

---

### Phase 2: Template Identification

**Goal**: Determine which reporting template the report uses (1-7).

**Template Decision Tree**:

```
Is the primary output a list of drugs?
├─ YES → Template 1 (Drug Discovery/Repurposing)
└─ NO  → Continue

Is the primary output a gene-gene interaction network?
├─ YES → Template 2 (Gene/Protein Network)
└─ NO  → Continue

Is the primary output trial-level data?
├─ YES → Template 3 (Clinical Trial Landscape)
└─ NO  → Continue

Is the primary output a target assessment?
├─ YES → Template 4 (Target Validation)
└─ NO  → Continue

Is the primary output regulatory/patent analysis?
├─ YES → Template 5 (Regulatory/Commercial Landscape)
└─ NO  → Continue

Is the primary output a step-by-step mechanism?
├─ YES → Template 6 (Mechanism Elucidation)
└─ NO  → Template 7 (Pathway Enrichment)
```

**How to identify from report structure**:
- **Template 1**: Has "Drug Candidates" table with CHEMBL IDs, phases, mechanisms
- **Template 2**: Has "Interaction Network" and "Hub Genes" tables with STRING scores
- **Template 3**: Has trial tables with NCT IDs, phases, recruitment status
- **Template 4**: Has tractability assessment, druggability scoring
- **Template 5**: Has patent numbers, regulatory timeline, market analysis
- **Template 6**: Has mechanism chain table with step-by-step process
- **Template 7**: Has pathway enrichment table with p-values, gene overlap

**Record the template** for use in Phase 3.

---

### Phase 3: Template-Specific Criteria

**Goal**: Apply only the evaluation dimensions relevant to the identified template.

**Dimension Applicability Matrix**:

| Dimension | Template 1 | Template 2 | Template 3 | Template 4 | Template 6 | Template 7 |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| 1. CURIE Resolution | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| 2. Source Attribution | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| 3. LOCATE→RETRIEVE | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| 4. Disease CURIE | **REQUIRED** | **OPTIONAL\*** | REQUIRED | **REQUIRED** | OPTIONAL | OPTIONAL |
| 5. OT Pagination | APPLICABLE | N/A | N/A | APPLICABLE | APPLICABLE | N/A |
| 6. Evidence Grading | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| 7. GoF Filter | APPLICABLE | N/A | N/A | APPLICABLE | APPLICABLE | N/A |
| 8. Trial Validation | REQUIRED | **OPTIONAL\*\*** | **REQUIRED** | REQUIRED | OPTIONAL | N/A |
| 9. Completeness | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| 10. Hallucination Risk | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED |

**Key annotations**:
- **\*Template 2 Disease CURIE**: OPTIONAL unless drug discovery (Phase 4a) or clinical trial search (Phase 4b) was performed
- **\*\*Template 2 Trial Validation**: OPTIONAL unless the gene network question explicitly involves therapeutic interventions

**Scoring logic**:
- **REQUIRED**: Score as PASS/FAIL based on completeness
- **OPTIONAL**: Score as N/A with justification (e.g., "Template 2 without Phase 4a/4b")
- **APPLICABLE**: Evaluate only if the report uses the relevant tool/approach
- **N/A**: Do not evaluate this dimension for this template

---

### Phase 4: Evidence Verification

**Goal**: Distinguish presentation failures from protocol failures.

**Verification checklist for each dimension**:

#### Dimension 1: CURIE Resolution
- **Before marking FAIL**: Check knowledge graph JSON for entity nodes
- **Entities in graph but not in report table** → Presentation failure (not protocol failure)
- **Entities not in graph and no tool call** → Protocol failure

#### Dimension 2: Source Attribution
- **Count sourced claims**: Claims with `[Source: tool(param)]` citations
- **Count unsourced claims**: Factual statements without citations
- **Threshold**: >90% sourced = PASS, 70-90% = PARTIAL, <70% = FAIL

#### Dimension 3: LOCATE→RETRIEVE
- **Check report citations**: Do they show both `search` and `get` tool calls?
- **Check knowledge graph provenance**: Entity `source` field should reference both steps
- **If only RETRIEVE cited**: Check if LOCATE occurred but wasn't documented (presentation gap)

#### Dimension 4: Disease CURIE
- **First check template**: Is disease CURIE required for this template?
- **Template 2 special case**: Required ONLY if Phase 4a/4b executed (check for drug tables or trial tables)
- **Check graph before report**: Disease nodes may exist in graph but not displayed in report table

#### Dimension 10: Hallucination Risk
**Use semantic equivalence test**:
- Read the actual UniProt/STRING/tool output if referenced
- Compare report claim to tool output
- **Faithful paraphrase** (semantically equivalent) → NOT hallucination
- **Statistical claims** (e.g., ">50%", "~13%") without source → Hallucination
- **Entity fabrication** (NCT IDs, drug names, CURIEs not in tools) → Hallucination

---

### Phase 5: Distinguish Failures

**Goal**: Categorize each identified issue correctly.

**Decision tree for each failed dimension**:

```
Was the protocol step executed (check knowledge graph, tool call history)?
├─ NO  → **PROTOCOL FAILURE** (dimension score: FAIL)
│         Example: No disease CURIE in graph, no opentargets_get_associations call
│
└─ YES → Was it documented in the final report?
          ├─ NO  → **PRESENTATION FAILURE** (dimension score: PARTIAL with note)
          │         Example: Disease CURIE exists in graph but not in Resolved Entities table
          │
          └─ YES → Is it documented correctly?
                    ├─ NO  → **DOCUMENTATION ERROR** (dimension score: PARTIAL)
                    │         Example: Source citation references wrong tool
                    │
                    └─ YES → **PASS**
```

**Severity levels**:
- **PROTOCOL FAILURE** (most severe) → Required step not executed → FAIL
- **PRESENTATION FAILURE** (moderate) → Step executed but not shown → PARTIAL
- **DOCUMENTATION ERROR** (minor) → Step shown but incorrectly attributed → PARTIAL
- **NO ISSUE** → PASS

---

## Evaluation Dimensions (Detailed)

### 1. CURIE Resolution

**What to check**:
- Core entities (genes, proteins, compounds, diseases) resolved to canonical CURIEs
- CURIE format correct (e.g., `HGNC:11998`, not `11998` or `HGNC_11998`)
- Disease CURIEs use MONDO or EFO prefixes

**Template-specific**:
- **Template 2**: Disease CURIEs NOT required unless drug/trial phases executed
- **All templates**: Secondary entities (STRING-discovered interactors) MAY be referenced by STRING ID only

**Scoring**:
- PASS: All primary entities resolved; secondary entities justified if unresolved
- PARTIAL: Most entities resolved; 1-3 missing with clear explanation
- FAIL: Multiple primary entities unresolved; no justification

### 2. Source Attribution

**What to check**:
- Every factual claim cites the tool call that produced it: `[Source: tool(param)]`
- Tables include source citations for each row or column
- Synthesis sections acknowledge multi-source integration

**Acceptable synthesis** (NOT unsourced):
- Paraphrased tool output with citation
- Multi-tool synthesis with all sources cited
- Interpretive claims with qualifier (e.g., "[Inferred from...]")

**Unacceptable** (unsourced):
- Statistical claims (prevalence, percentages) without source
- FDA approval years without source
- NCT ID mentions without verification source

**Scoring**:
- PASS: >90% of claims sourced
- PARTIAL: 70-90% sourced
- FAIL: <70% sourced

### 3. LOCATE→RETRIEVE Discipline

**What to check**:
- Two-step pattern shown for each entity type
- LOCATE step (search/fuzzy match) cited before RETRIEVE step (get by ID)
- No "magic IDs" that appear without prior LOCATE

**Gray area**: Cross-references from RETRIEVE output can be used directly (e.g., UniProt ID from HGNC RETRIEVE used in next RETRIEVE call) — this is acceptable.

**Scoring**:
- PASS: Two-step pattern documented for all entity types
- PARTIAL: RETRIEVE steps shown but LOCATE steps not explicitly cited (check graph for evidence)
- FAIL: IDs used without any LOCATE provenance

### 4. Disease CURIE in ENRICH Phase

**Template-specific evaluation**:

**Templates 1, 4, 6** (drug/target/mechanism): Disease CURIE **REQUIRED**
- Check: Does Resolved Entities table include disease with MONDO or EFO CURIE?
- Check graph: Does knowledge graph have disease nodes?

**Template 2** (gene network): Disease CURIE **OPTIONAL**
- Required ONLY if Phase 4a/4b executed (check for drug tables or trial tables in report)
- If no drug/trial phases: Score as **N/A** with note "Template 2 without therapeutic scope"

**Template 3, 5, 7**: Disease CURIE **OPTIONAL** (context-dependent)

**Scoring**:
- PASS: Disease CURIE resolved when required by template
- N/A: Not required for this template type (with justification)
- FAIL: Required but missing

### 5. Open Targets Pagination

**What to check**:
- If report uses Open Targets `knownDrugs`, does it mention pagination issues?
- Does the curl command use `size` only (not `page` or `index`)?

**Scoring**:
- PASS: No pagination failures; uses `size`-only pattern
- N/A: Open Targets `knownDrugs` not used
- FAIL: Pagination errors documented; used incorrect pattern

### 6. Evidence Grading

**What to check**:
- Claims individually graded with numeric scores (0.00-1.00)
- Modifiers applied with justification
- Overall confidence = median of claim scores (not mean)
- Range reported (lowest to highest)

**Acceptable alternatives**:
- Section-level grading (L1-L4) if claim-level grading not feasible
- Qualitative confidence with caveats

**Scoring**:
- PASS: Claim-level numeric grading with modifiers
- PARTIAL: Section-level grading or qualitative confidence
- FAIL: No evidence grading

### 7. Gain-of-Function Filter

**When applicable**:
- Disease involves gain-of-function mutations (e.g., FOP with ACVR1 R206H)
- Report includes drug candidates

**What to check**:
- Agonists excluded from drug list
- Mechanism of action aligns with disease biology

**Scoring**:
- PASS: Agonists correctly excluded
- N/A: Not a gain-of-function disease or no drug discovery performed
- FAIL: Agonists included for gain-of-function disease

### 8. Clinical Trial Validation

**What to check**:
- NCT IDs verified via `clinicaltrials_get_trial` (RETRIEVE step)
- "Verified" column in trial tables shows checkmarks
- No invalid NCT IDs

**Template-specific**:
- **Template 2**: Only required if trials are part of the gene network question
- **Template 3**: ALL trials must be verified (this is the primary output)

**Scoring**:
- PASS: All NCT IDs verified
- PARTIAL: Some verified, some marked as unverified with explanation
- FAIL: NCT IDs present but none verified
- N/A: No trials in report (acceptable for some templates)

### 9. Completeness

**What to check**:
- Does the report answer the competency question?
- Are all components requested in the CQ addressed?

**Template-specific gaps**:
- **Template 2**: Pathway Membership section required (WikiPathways)
- **Template 1**: Drug mechanisms and phases required
- **Template 6**: Step-by-step mechanism chain required

**Scoring**:
- PASS: All CQ components addressed
- PARTIAL: Major components addressed; minor gaps acknowledged
- FAIL: CQ not answered or major gaps

### 10. Hallucination Risk

**Three-tier assessment**:

**LOW**: All claims trace to tool outputs; paraphrasing is faithful
**MEDIUM**: Some interpretive synthesis; most claims grounded
**HIGH**: Multiple claims lack provenance; entity/value fabrication

**Paraphrasing vs Hallucination Standards**:

**ACCEPTABLE** (not hallucination):
- UniProt function text: "Binds to 3 E-boxes of the E-cadherin/CDH1 gene promoter" → Report: "binds E-boxes in CDH1 promoter"
- STRING interaction descriptions synthesized for readability
- Numeric values unchanged: Tool output 0.955 → Report 0.955
- Entity names/CURIEs unchanged: Tool output HGNC:11998 → Report HGNC:11998

**UNACCEPTABLE** (hallucination):
- NCT IDs not in ClinicalTrials.gov tool output
- Drug names not in Open Targets/ChEMBL output
- FDA approval years (e.g., "FDA-approved 2021") without source
- Statistical claims (e.g., "TP53 mutations in >50% of cancers") without tool source
- Prevalence figures (e.g., "~13% of NSCLC") without epidemiological database query

**How to verify**:
1. Identify suspicious claims (detailed mechanisms, statistics, approval years)
2. Check if similar text appears in cited tool output
3. Use semantic equivalence test: Does report claim convey same meaning as tool output?
4. Mark as hallucination only if claim introduces information not present in any tool call

**Scoring**:
- LOW: <3 potential hallucinations; all core facts grounded
- MEDIUM: 3-7 potential hallucinations; interpretive synthesis exceeds tool output
- HIGH: >7 potential hallucinations; entity/value fabrication

---

## Report Output Format

Produce a structured markdown review with:

### 1. Summary Verdict
- Overall score: PASS / PARTIAL / FAIL
- Template identified
- Top 3 issues

### 2. Dimension Scores (Table)
| Dimension | Score | Notes |
|-----------|-------|-------|
| 1. CURIE Resolution | PASS/PARTIAL/FAIL/N/A | Brief justification |
| ... | | |

### 3. Detailed Findings (Per Dimension)
For each dimension:
- **Verdict**: PASS/PARTIAL/FAIL/N/A
- **Score**: X/10 (if applicable)
- **Evidence**: What was checked (list files, line numbers)
- **Issues found**: Specific problems with line references
- **Positive observations**: What was done well

### 4. Failure Classification
For each FAIL or PARTIAL:
- **Failure type**: Protocol / Presentation / Documentation
- **Severity**: Critical / Moderate / Minor
- **Recommendation**: Specific fix

### 5. Overall Assessment
- Protocol execution quality (0-10)
- Report presentation quality (0-10)
- Overall verdict with justification

---

## Common Reviewer Pitfalls (Avoid These)

### Pitfall 1: Template Misapplication
**Wrong**: "Report lacks disease CURIE → FAIL"
**Right**: "Report is Template 2 without Phase 4a/4b → Disease CURIE not required → N/A"

### Pitfall 2: Presentation = Protocol Failure
**Wrong**: "No LOCATE step cited → LOCATE not performed → FAIL"
**Right**: "No LOCATE step cited in report. Checking knowledge graph... Entity found with search provenance → LOCATE performed but not documented → PARTIAL (presentation failure)"

### Pitfall 3: Paraphrasing = Hallucination
**Wrong**: "Report says 'binds E-boxes' but tool output says 'Binds to 3 E-boxes' → Hallucination"
**Right**: "Report text is faithful paraphrase of UniProt function annotation → NOT hallucination"

### Pitfall 4: Impossible Standards
**Wrong**: "All 15 STRING-discovered interactors lack HGNC CURIEs → FAIL"
**Right**: "11 primary entities resolved to HGNC CURIEs. 15 secondary entities referenced by STRING ID only — acceptable for Template 2 with large interaction networks → PASS with note"

### Pitfall 5: Missing Context
**Wrong**: "Report claims disease CURIE exists but I don't see it in the Resolved Entities table → FAIL"
**Right**: "Resolved Entities table lacks disease CURIE. Checking knowledge graph... EFO:0003060 found in graph disease nodes → PARTIAL (presentation failure, not protocol failure)"

---

## See Also

- **biosciences-graph-builder**: Fuzzy-to-Fact protocol phases (what to expect in reports)
- **biosciences-reporting**: Template schemas and evidence grading system
- **MEMORY.md**: Review learnings and common pitfalls (updated 2026-02-07)

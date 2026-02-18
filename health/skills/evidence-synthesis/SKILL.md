---
name: health/evidence-synthesis
description: This skill should be used when selecting and conducting evidence synthesis approaches beyond traditional systematic reviews. Use for scoping reviews, rapid reviews, evidence maps, umbrella reviews, and mixed-methods synthesis. Invoke when users mention scoping reviews, rapid evidence synthesis, evidence mapping, or need guidance on selecting the appropriate review type for their research question or timeline constraints.
version: 1.0.0
---

# Evidence Synthesis

A comprehensive framework for selecting and conducting diverse evidence synthesis approaches including scoping reviews, rapid reviews, evidence maps, umbrella reviews, and mixed-methods synthesis. This skill helps researchers choose the most appropriate synthesis method based on their research question, timeline, and resource constraints while maintaining methodological rigor.

**Important**: This skill guides selection and execution of evidence synthesis methods but does not replace systematic review methodology expertise or statistical consultation for complex syntheses. Always ensure appropriate methodological expertise is involved for the chosen approach.

## When to Use This Skill

Invoke this skill when:
- Determining which type of evidence synthesis is appropriate for a research question.
- Planning or conducting a scoping review to map literature breadth.
- Designing a rapid review for time-sensitive decision-making.
- Creating an evidence map to visualize research distribution and gaps.
- Conducting an umbrella review (review of systematic reviews).
- Planning mixed-methods or qualitative evidence synthesis.
- Comparing methodologies to justify review type selection.
- Adapting systematic review methods for resource constraints.
- Synthesizing evidence for policy briefs or clinical guidelines.
- Conducting living systematic reviews with continuous updates.
- Reporting non-traditional review types for publication.

## Regulatory Context

### Australia & New Zealand (Default)

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **NHMRC Standards** (AU) | Research synthesis | Guidance on evidence synthesis for guidelines and policy |
| **Joanna Briggs Institute** (AU) | Review methodologies | Methodological guidance for scoping and rapid reviews |
| **Health Research Council NZ** | Research standards | Evidence synthesis standards for funding applications |
| **ACC NZ** | Policy evidence | Requirements for rapid evidence summaries |
| **PHARMAC** (NZ) | Health technology assessment | Evidence requirements for pharmaceutical funding decisions |

### US/EU-lite Fallback

| Regulation/Standard | Relevance | Key Requirements |
|---------------------|-----------|------------------|
| **AHRQ Rapid Reviews** (US) | Comparative effectiveness | Methods guidance for rapid evidence synthesis |
| **WHO Guidelines** | International | Evidence synthesis standards for guideline development |
| **EUnetHTA** (EU) | Health technology assessment | HTA-specific synthesis requirements |
| **CADTH** (Canada) | Health technology assessment | Rapid review and evidence mapping methods |

### Jurisdiction Matrix

| Jurisdiction | Applicable Regulator | Reporting Trigger | Timeframe | Required Artifacts | Escalation Point |
|--------------|---------------------|-------------------|-----------|-------------------|------------------|
| **AU - National** | NHMRC | Clinical guideline evidence | Per guideline cycle | Evidence synthesis report; Methodology justification | Guidelines Committee Chair |
| **AU - State** | State Health Depts | Policy decision support | Urgent policy need | Rapid review; Executive summary | Policy Director |
| **NZ - National** | PHARMAC | Funding decision evidence | Funding round deadline | Evidence summary; Gap analysis | Pharmacology Advisor |
| **US** | AHRQ | Evidence-based practice | Contract timeline | Technical brief; Methods appendix | Project Officer |
| **International** | WHO | Guideline development | Guideline timeline | Evidence synthesis; GRADE tables | Guideline Steering Group |

## Quick Reference

1. **Systematic Review**: Gold standard; comprehensive; 6-12 months; all question types.
2. **Scoping Review**: Map literature breadth; no quality assessment; 2-4 months; emerging topics.
3. **Rapid Review**: Accelerated systematic review; 1-3 months; urgent decisions; transparent shortcuts.
4. **Evidence Map**: Visual overview of research distribution; gap identification; 3-6 months.
5. **Umbrella Review**: Synthesize existing systematic reviews; overview of reviews; 3-6 months.
6. **Qualitative Synthesis**: Synthesize qualitative studies; interpretive methods; context-specific.
7. **Mixed-Methods**: Integrate quantitative and qualitative evidence; complex interventions.
8. **Living Review**: Continuously updated systematic review; emerging evidence areas.

## Operating Modes

### Standard Mode
Full evidence synthesis with appropriate methodological rigor for the selected review type, complete documentation, quality assessment where applicable, and transparent reporting of methods and limitations. Use for publication-grade syntheses intended for peer-reviewed journals or formal evidence-based guidelines.

### Lite Mode
Streamlined guidance for rapid evidence summaries, briefing documents, or internal decision support. Focuses on essential elements with abbreviated searching, single-reviewer screening with verification, and narrative summary without formal quality assessment. Clearly acknowledge limitations and appropriate use cases. Never claim systematic review rigor for rapid methods.

## Detailed Guidance

### 1. Review Type Selection Framework

Choose the appropriate synthesis method based on these criteria:

#### 1.1 Decision Matrix

| Question Type | Time Available | Evidence Type | Recommended Method |
|---------------|----------------|---------------|-------------------|
| Effectiveness of intervention | 6-12 months | RCTs + observational | **Systematic Review** with meta-analysis |
| What literature exists? | 2-4 months | Any | **Scoping Review** |
| Urgent policy decision | 1-3 months | Existing reviews + primary | **Rapid Review** |
| Research gaps and clusters | 3-6 months | Any | **Evidence Map** |
| Multiple SRs on topic | 3-6 months | Systematic reviews | **Umbrella Review** |
| Lived experience/implementation | 3-6 months | Qualitative | **Qualitative Synthesis** |
| Complex intervention | 4-8 months | Mixed methods | **Mixed-Methods Review** |
| Continuously emerging evidence | Ongoing | RCTs + updates | **Living Systematic Review** |

#### 1.2 Key Considerations

**Research Question**:
- Intervention effectiveness → Systematic review/rapid review
- Literature landscape → Scoping review/evidence map
- Concept clarification → Scoping review
- Evidence overview → Umbrella review
- Experience/barriers → Qualitative synthesis

**Timeline**:
- <1 month → Rapid evidence summary (acknowledge limitations)
- 1-3 months → Rapid review with transparent shortcuts
- 3-6 months → Scoping review, evidence map, umbrella review
- 6-12 months → Full systematic review
- Ongoing → Living systematic review

**Resource Constraints**:
- Single reviewer possible for scoping reviews (with verification)
- Rapid reviews can use abbreviated searching
- Evidence maps automate extraction using machine learning

### 2. Scoping Review Methodology

#### 2.1 Purpose and Applications

**Definition**: A scoping review maps the extent, range, and nature of research activity in a field without assessing quality.

**Appropriate When**:
- Identifying research gaps
- Clarifying concepts and definitions
- Examining how research is conducted
- Mapping evidence characteristics
- Informing future systematic reviews

#### 2.2 JBI Methodology (Arksey & O'Malley/Peters Framework)

**Six Stage Process**:

**Stage 1: Identifying the Research Question**
- Use PCC framework: Population, Concept, Context
- Broad question to capture wide literature
- Example: "What is known about digital health interventions for diabetes management?"

**Stage 2: Identifying Relevant Studies**
- Search strategy less exhaustive than systematic review
- Key databases (3-5 typically sufficient)
- Grey literature and key informants optional
- Document search strategy and databases

**Stage 3: Study Selection**
- Title/abstract screening (single or dual reviewer)
- Full-text screening with reasons for exclusion
- PRISMA-ScR flow diagram

**Stage 4: Charting the Data**
- Extract: Authors, year, country, study design, population, concept, key findings
- Use standardized data charting form
- Iterative approach (pilot and refine)

**Stage 5: Collating, Summarizing, and Reporting Results**
- Numerical summary: Study counts by characteristic
- Thematic analysis: Emerging themes
- Gap identification: Research needs

**Stage 6: Optional Consultation**
- Stakeholder input on findings
- Practitioner validation
- Patient/public involvement

#### 2.3 PRISMA-ScR Reporting

Use PRISMA extension for Scoping Reviews checklist:
- 20-item checklist
- Includes flow diagram modification
- Published in Annals of Internal Medicine (2018)

### 3. Rapid Review Methodology

#### 3.1 Purpose and Applications

**Definition**: An accelerated systematic review using streamlined methods to meet urgent decision timelines.

**Appropriate When**:
- Policy or clinical decisions needed urgently
- Emerging health threats (pandemic, outbreak)
- Healthcare resource allocation decisions
- Guideline updates required quickly

#### 3.2 Methodological Shortcuts (Transparent)

| Systematic Review Element | Rapid Review Adaptation | Transparency Requirement |
|---------------------------|------------------------|-------------------------|
| **Search strategy** | Abbreviated search (3-4 databases) | List databases searched; document date limits |
| **Grey literature** | Minimal or none | State exclusion; justify based on timeframe |
| **Study selection** | Single reviewer with verification sample | Report percentage verified; inter-rater reliability |
| **Data extraction** | Single reviewer with spot checks | Document verification method |
| **Risk of bias** | Focus on key domains only | State which domains assessed |
| **Quality of evidence** | Streamlined GRADE or narrative | Document modified approach |
| **Synthesis** | Narrative only (no meta-analysis) | Justify lack of pooling |

#### 3.3 Quality Considerations

**Acceptable Shortcuts**:
- Focused research question (narrower PICOS)
- Limited database searching (core databases only)
- Single reviewer with verification sampling (≥20% dual-reviewed)
- Abbreviated data extraction (key outcomes only)

**Unacceptable Shortcuts**:
- No protocol or registration
- No documentation of methods
- Bias in study selection
- Omitting risk of bias entirely
- Selective outcome reporting

#### 3.4 WHO Rapid Review Guide

WHO recommends rapid reviews include:
- Preliminary search to scope literature volume
- Focused question and inclusion criteria
- Streamlined searching (limited databases)
- Expedited screening (single reviewer + verification)
- Simplified data extraction (key outcomes only)
- Narrative synthesis
- Transparent reporting of limitations

### 4. Evidence Mapping

#### 4.1 Purpose and Applications

**Definition**: A systematic method to identify, categorize, and display evidence distribution across interventions, outcomes, populations, and study designs.

**Appropriate When**:
- Visualizing research landscape
- Identifying evidence clusters and gaps
- Planning future systematic reviews
- Stakeholder communication
- Policy priority setting

#### 4.2 Evidence Map Components

**Systematic Search**:
- Broad search strategy
- Multiple databases
- Clear eligibility criteria

**Systematic Screening**:
- Title/abstract and full-text screening
- Document with PRISMA-style flow diagram

**Systematic Coding**:
- Standardized extraction form
- Categories: Intervention, outcome, population, study design, setting

**Visualization**:
- Bubble charts: Intervention vs. Outcome (bubble size = study count)
- Heat maps: Evidence density
- Gap maps: Research needs highlighted

#### 4.3 Gap Analysis

**Evidence Clusters**:
- Well-studied interventions
- Common outcomes measured
- Population groups with robust evidence

**Evidence Gaps**:
- Under-studied interventions
- Outcomes not measured
- Under-represented populations
- Methodological limitations

### 5. Umbrella Review Methodology

#### 5.1 Purpose and Applications

**Definition**: A systematic review of existing systematic reviews, also called "overview of reviews" or "review of reviews."

**Appropriate When**:
- Multiple systematic reviews exist on topic
- Synthesizing evidence across different populations or settings
- Identifying discordant findings between reviews
- Comprehensive overview needed for guidelines

#### 5.2 Methodological Considerations

**Search Strategy**:
- Focus on systematic review databases
- Epistemonikos, Cochrane Database of Systematic Reviews
- Database filters for systematic reviews

**Eligibility Criteria**:
- Must be systematic reviews (not narrative reviews)
- Quality threshold (e.g., must include risk of bias assessment)
- Recent reviews preferred (unless unique contribution)

**Assessment of Multiple Systematic Reviews (AMSTAR) Tool**:

| Domain | Assessment |
|--------|------------|
| **D1** | Was an a priori design provided? |
| **D2** | Was there duplicate study selection and data extraction? |
| **D3** | Was a comprehensive literature search performed? |
| **D4** | Was the status of publication used as inclusion criteria? |
| **D5** | Was a list of studies provided? |
| **D6** | Were the characteristics of included studies provided? |
| **D7** | Was the scientific quality of included studies assessed? |
| **D8** | Was quality used in formulating conclusions? |
| **D9** | Were methods used to combine findings appropriate? |
| **D10** | Was likelihood of publication bias assessed? |
| **D11** | Was conflict of interest stated? |

#### 5.3 Discordance Analysis

When reviews disagree:
- Compare inclusion criteria
- Compare search dates (different evidence base)
- Compare risk of bias assessments
- Compare synthesis methods
- Compare outcomes measured

### 6. Qualitative Evidence Synthesis

#### 6.1 Purpose and Applications

**Definition**: Systematic methods to synthesize findings from qualitative studies.

**Appropriate When**:
- Understanding patient experiences
- Exploring implementation barriers/facilitators
- Examining healthcare professional perspectives
- Investigating contextual factors

#### 6.2 Methodological Approaches

| Method | Description | Best For |
|--------|-------------|----------|
| **Thematic Synthesis** | Identify descriptive and analytical themes | General qualitative synthesis |
| **Meta-Ethnography** | Translate concepts across studies; generate new theory | Theory development |
| **Critical Interpretive Synthesis** | Iterative questioning and interpretation | Complex, heterogeneous literature |
| **Framework Synthesis** | Apply a priori framework; identify gaps | Policy-relevant questions |
| **Meta-Aggregation** (JBI) | Aggregate findings into categories and syntheses | Practice recommendations |

#### 6.3 ENTREQ Reporting

Use ENTREQ (Enhancing Transparency in Reporting the Synthesis of Qualitative Research) statement:
- 21-item checklist
- Includes methodological approach
- Describes analytical techniques

### 7. Mixed-Methods Synthesis

#### 7.1 Purpose and Applications

**Definition**: Integration of quantitative and qualitative evidence within a single review.

**Appropriate When**:
- Complex interventions
- Understanding effectiveness and implementation
- Examining what works, for whom, and in what circumstances

#### 7.2 Integration Methods

**Convergent Integrated Approach** (JBI):
- Conduct quantitative and qualitative syntheses separately
- Integrate at results level
- Create mixed-methods matrix

**Sequential Explanatory**:
- Quantitative synthesis first
- Qualitative explains quantitative findings

**Sequential Exploratory**:
- Qualitative synthesis first
- Quantitative tests qualitative findings

#### 7.3 JBI Mixed Methods Guidance

- Use convergent integrated approach as default
- Present quantitative and qualitative findings separately then integrated
- Use graphical displays for integration
- Report confidence in qualitative findings (CERQual)

### 8. Living Systematic Reviews

#### 8.1 Purpose and Applications

**Definition**: Systematic reviews that are continually updated as new evidence emerges.

**Appropriate When**:
- Rapidly evolving evidence base
- High-priority clinical questions
- Ongoing uncertainty requiring current evidence

#### 8.2 Methodological Considerations

**Automation**:
- Automated literature surveillance
- Machine learning for screening
- Living data extraction

**Update Triggers**:
- Time-based (e.g., every 6 months)
- Event-based (e.g., major new trial published)
- Threshold-based (e.g., evidence certainty changes)

**Version Control**:
- Clear versioning system
- Change logs
- Archiving previous versions

#### 8.3 Cochrane Living Evidence Framework

Cochrane recommends:
- Prioritize high-impact questions
- Establish editorial infrastructure
- Use technology for efficiency
- Plan for sustainability

## Documentation Requirements

### Evidence Synthesis Project File

- [ ] Review type selection rationale
- [ ] Protocol or project plan
- [ ] Eligibility criteria
- [ ] Search strategies (all sources)
- [ ] PRISMA-style flow diagram
- [ ] Study characteristics table
- [ ] Quality assessment results (if applicable)
- [ ] Data extraction forms
- [ ] Synthesis results (narrative, visual, or meta-analytic)
- [ ] Evidence gap analysis (for maps)
- [ ] Limitations and strengths assessment
- [ ] Applicability and implications

### Review-Type Specific Requirements

**Scoping Review**:
- [ ] PCC framework documentation
- [ ] PRISMA-ScR checklist
- [ ] Gap identification and research recommendations

**Rapid Review**:
- [ ] Transparent documentation of shortcuts taken
- [ ] Risk of bias assessment (streamlined)
- [ ] Limitations section acknowledging rapid methods

**Evidence Map**:
- [ ] Visual display of evidence distribution
- [ ] Gap analysis with research priorities
- [ ] Interactive or static visualization

**Umbrella Review**:
- [ ] AMSTAR quality assessment of included reviews
- [ ] Discordance analysis if reviews disagree
- [ ] Overview of certainty across reviews

**Qualitative Synthesis**:
- [ ] ENTREQ checklist
- [ ] Methodological approach justification
- [ ] Analytical process description

**Living Review**:
- [ ] Update schedule and triggers
- [ ] Version control documentation
- [ ] Change log between versions

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| **Calling rapid review a systematic review** | Misrepresents methodological rigor | Clearly label as rapid review; document shortcuts transparently |
| **No protocol for scoping review** | Increases risk of scope creep | Write and follow protocol; optional registration |
| **Quality assessment in scoping review** | Beyond scope; introduces bias toward positive findings | Map quality descriptively only if relevant; focus on breadth |
| **Insufficient searching for evidence map** | Incomplete landscape representation | Ensure broad, comprehensive searching |
| **Ignoring discordance in umbrella review** | Misses important evidence conflicts | Explicitly analyze and explain discordant findings |
| **Integrating without justification** | Mixed-methods integration requires explicit approach | State integration method (convergent, sequential) |
| **No gap analysis in evidence map** | Misses primary purpose of mapping | Systematically identify and report evidence gaps |
| **Unclear review type selection** | Reader cannot assess appropriateness | Explicitly state why this review type was chosen |
| **Omitting limitations** | Transparency essential for evidence utility | Thoroughly document methodological limitations |
| **Inadequate stakeholder consultation** | Misses practical applicability | Include end-users in scoping review consultation |

## When to Escalate

Escalate to Evidence Synthesis Lead, Methodologist, or Content Expert when:
- Living systematic review infrastructure is required (ongoing updates).
- Network meta-analysis is being considered within an umbrella review.
- Mixed-methods synthesis requires advanced integration methods.
- Machine learning or automation tools are needed for screening/extraction.
- Evidence synthesis will inform high-stakes policy or regulatory decisions.
- Multiple review types are being combined (e.g., rapid umbrella review).
- Complex interventions require innovative synthesis approaches.
- Realist synthesis or other theory-driven methods are proposed.
- Cross-language synthesis without translation resources.
- Synthesis includes patient-level data from multiple sources.

## Privacy Considerations

- **PHI Involved**: Rare - Evidence synthesis typically uses aggregate published data.
- **Data Minimization**: Extract only published aggregate data; do not request individual patient data unless justified.
- **De-identification**: Not typically applicable as published studies should already be de-identified.
- **Access Controls**: Limit access to extraction files to synthesis team members.
- **Retention**: Retain synthesis files according to institutional policy (typically 7+ years).
- **No Persistence**: Do not store unpublished data or author communications containing PHI.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Well-established review type (scoping, rapid) with clear guidance | High | Proceed with established methodology; document choices |
| Novel or hybrid methodology without established guidance | Medium | Consult with methodology expert; document rationale extensively |
| Rapid review for urgent high-stakes decision | Medium | Ensure transparency about limitations; acknowledge uncertainty |
| Living systematic review setup | Low | Escalate to specialist; plan infrastructure and sustainability |
| Mixed-methods integration of heterogeneous evidence | Medium | Use established frameworks (JBI, Cochrane); involve qualitative expert |
| Evidence map with automated/machine learning components | Medium | Validate machine learning outputs; spot-check accuracy |
| Umbrella review with discordant systematic reviews | Medium | Escalate for discordance analysis; involve content experts |
| Qualitative synthesis without qualitative expertise | Low | Involve qualitative research specialist; ensure appropriate method selection |

## Tool Requirements

- `~~research literature` - For database searches across review types
- `~~project tracker` - For managing synthesis timelines and milestones
- `~~cloud storage` - For documentation, extraction forms, and data files
- `~~document collaboration` - For team coordination on screening and extraction
- `~~data analysis` - For visualization (evidence maps, bubble charts)
- `~~reference manager` - For citation management and deduplication
- `~~machine learning` - For automated screening in living reviews or large evidence maps (optional)

## Success Indicators

You've applied this skill well when:
- [ ] Review type selection is justified based on question, timeline, and resources
- [ ] Protocol or project plan documents methodology clearly
- [ ] Eligibility criteria are appropriate for review type
- [ ] Search strategy is documented and reproducible
- [ ] PRISMA-style flow diagram accurately reflects process
- [ ] Quality assessment is appropriate for review type (or omitted with justification)
- [ ] Synthesis approach matches review type and data characteristics
- [ ] Evidence gaps are identified and described (where applicable)
- [ ] Limitations are transparently acknowledged
- [ ] Reporting guidelines specific to review type are followed
- [ ] Results are contextualized for intended use (policy, practice, research)

## Related Skills

- `~~health/systematic-review` - For traditional systematic review methodology (gold standard)
- `~~health/guideline-development` - When evidence synthesis supports clinical guidelines
- `~~health/quality-improvement` - When evidence synthesis informs QI initiatives
- `~~research/literature-search` - For database-specific search optimization
- `~~research/statistical-analysis` - For meta-analysis within systematic reviews

## References

- Tricco AC, Lillie E, Zarin W, et al. PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation. Ann Intern Med. 2018;169(7):467-473.
- Harker J, Kleijnen J. What is a rapid review? A methodological exploration of rapid reviews in Health Technology Assessments. Int J Evid Based Healthc. 2012;10(4):397-410.
- Snilstveit B, Vojtkova M, Bhavsar A, et al. Evidence & Gap Maps: A comparison of different approaches. Campbell Systematic Reviews. 2016;12(1):1-38.
- Aromataris E, Fernandez R, Godfrey CM, et al. Summarizing systematic reviews: methodological development, conduct and reporting of an umbrella review approach. Int J Evid Based Healthc. 2015;13(3):132-140.
- Tong A, Flemming K, McInnes E, et al. Enhancing transparency in reporting the synthesis of qualitative research: ENTREQ. BMC Med Res Methodol. 2012;12:181.
- Pearson A, White H, Bath-Hextall F, et al. A mixed-methods approach to systematic reviews. Int J Evid Based Healthc. 2015;13(3):121-131.
- Elliott JH, Turner T, Clavisi O, et al. Living systematic reviews: an emerging opportunity to narrow the evidence-practice gap. PLoS Med. 2014;11(2):e1001603.
- Cochrane Methods. Living systematic reviews. Cochrane Library. https://methods.cochrane.org/living-systematic-reviews

---
name: health/guideline-development
description: This skill should be used when developing, drafting, or reviewing evidence-based clinical guidelines. Use when a user mentions clinical guidelines, evidence grading, literature review, NHMRC guidance, or clinical recommendations.
version: 1.0.0
---

# Clinical Guideline Development

Structured guidance for the development, drafting, and review of evidence-based clinical guidelines to ensure the delivery of high-quality, safe, and effective patient care.

**Important**: This skill assists with the development of guidelines but does not provide clinical advice or perform independent evidence synthesis. All guidelines must be based on rigorous literature review, graded for evidence quality, and endorsed by authorized clinical leadership.

## When to Use This Skill

Invoke when:
- Developing a new clinical guideline for a specific condition or intervention.
- Reviewing and updating an existing guideline based on new clinical evidence.
- Grading the strength of clinical recommendations using established frameworks (e.g., GRADE, NHMRC).
- Drafting guideline content that summarizes evidence and provides actionable clinical advice.
- Ensuring that clinical guidelines meet national or international standards for development.
- Integrating evidence-based practice into organizational clinical workflows.

Do not use for organizational policies (use `~~health/policy-development`) or step-by-step procedures (use `~~health/procedure-development`).

## Regulatory Context

| Regulation | Relevance | Key Requirements |
|------------|-----------|------------------|
| **AU/NZ Baseline** | NHMRC Standards for Guidelines (AU), Ministry of Health Guidelines (NZ) | Guidelines must be evidence-based, transparently developed, and address conflicts of interest. Use of the NHMRC "Levels of Evidence" is the standard in AU. |
| **US/EU-lite (optional)** | AHRQ Guidelines (US), NICE Guidelines (UK/EU) | Focus on methodological rigor, stakeholder engagement, and clear presentation of recommendations. |

### Jurisdiction-Specific Triggers
- **Australia**: Update in NHMRC clinical practice guidelines or professional college position statements.
- **New Zealand**: New evidence summaries from Te Whatu Ora or specialist clinical networks.

## Quick Reference

1.  **Define Clinical Question**: Use the PICO framework (Patient, Intervention, Comparison, Outcome).
2.  **Search for Evidence**: Conduct systematic literature searches.
3.  **Appraise Evidence**: Evaluate the quality and relevance of the found studies.
4.  **Grade Recommendations**: Assign a level of strength to each recommendation.
5.  **Draft Guideline**: Structure content around clinical decision points.
6.  **Consult Experts**: Engage with multidisciplinary clinical subject matter experts (SMEs).
7.  **Public/Stakeholder Review**: Circulate for feedback from users and consumers.
8.  **Approval & Dissemination**: Final sign-off by Clinical Governance and implementation support.

## Detailed Guidance

### Clinical Guideline Structure
Every clinical guideline should include:
- **Title**: Specific condition or intervention.
- **Recommendations Summary**: Key "bottom-line" advice for clinicians.
- **Background**: Prevalence, impact, and rationale for the guideline.
- **Evidence Summary**: Brief overview of the research supporting the recommendations.
- **Grading of Evidence**: Explicit link between recommendations and evidence strength.
- **Implementation Guidance**: Tools, algorithms, or pathways to support bedside use.
- **Exclusions/Contraindications**: When the guideline does not apply.
- **Audit/KPIs**: How adherence to the guideline will be measured.

### Evidence Grading (NHMRC Adaptation)
Recommendations must be graded according to the strength of the supporting evidence:
- **Level I**: Evidence from systematic review of all relevant randomized controlled trials.
- **Level II**: Evidence from at least one properly designed randomized controlled trial.
- **Level III**: Evidence from well-designed pseudo-randomized or comparative studies.
- **Level IV**: Evidence from case series, either post-test or pre-test and post-test.

### GRADE Framework Integration
For complex guidelines, use the GRADE (Grading of Recommendations, Assessment, Development and Evaluations) approach:
- **High Quality**: Further research is very unlikely to change our confidence in the estimate of effect.
- **Moderate Quality**: Further research is likely to have an important impact on our confidence in the estimate of effect.
- **Low Quality**: Further research is very likely to have an important impact on our confidence in the estimate of effect and is likely to change the estimate.
- **Very Low Quality**: Any estimate of effect is very uncertain.

## Documentation Requirements

- [ ] **PICO Statement**: Clear definition of the clinical scope.
- [ ] **Search Strategy**: Documented search terms and databases used.
- [ ] **Evidence Tables**: Summaries of key studies and their findings.
- [ ] **Grading Rationale**: Explanation for the assigned recommendation levels.
- [ ] **Conflict of Interest Register**: Declarations from all development group members.

## Common Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Relying on Expert Opinion Only | Leads to bias and may not reflect current best evidence. | Always ground recommendations in systematic evidence review. |
| Vague Recommendations | Clinicians cannot easily apply terms like "consider" or "usually". | Use clear, actionable language (e.g., "Administer X if Y is present"). |
| Ignoring Patient Preferences | Guidelines should support shared decision-making. | Include consumer representatives in the development group. |
| Outdated Evidence | Medical knowledge changes rapidly; old guidelines may be unsafe. | Set mandatory review dates (3-5 years) or triggers for "living" guidelines. |
| Inconsistent Grading | Causes confusion about which recommendations are mandatory. | Use a single grading framework consistently throughout the document. |

## When to Escalate

Escalate to the Clinical Governance Committee or Medical Director when:
- A new, high-quality study directly contradicts a major guideline recommendation.
- There is a significant disagreement among clinical SMEs regarding a recommendation.
- Implementation of a guideline requires significant unbudgeted resources (e.g., new medication).
- A guideline is linked to a cluster of adverse events or clinical variation.

## Privacy Considerations

- **PHI involved**: No. Guidelines are population-level evidence summaries.
- **Data minimization**: Avoid using specific patient case studies in guideline text unless fully de-identified.
- **Retention**: Guidelines and their supporting "Evidence Dossiers" should be retained for 10+ years to support clinical defense and historical review.

## Confidence Indicators

| Scenario | Confidence | Action |
|----------|------------|--------|
| Drafting a summary of a high-quality NHMRC Level I systematic review | High | Propose draft recommendations. |
| Mapping recommendations from a complex, conflicting set of studies | Medium | Summarize findings and REQUIRE MDT SME review for consensus. |
| Guideline involves highly specialized or experimental therapies | Low | REQUIRE direct authorship by relevant sub-specialist SMEs. |

## Standard and Lite Modes

- **Standard**: Full guideline development including systematic review, formal grading, and stakeholder consultation.
- **Lite**: Rapid creation of an "Evidence Summary" or "Clinical Alert" based on a single high-impact publication.

## Tool Requirements

- `~~cloud storage` - For document repository and evidence dossiers.
- `~~search` - For literature searching (PubMed, Cochrane).
- `~~project tracker` - To manage the development lifecycle.

## Success Indicators

You've applied this skill well when:
- [ ] Recommendations are clearly linked to evidence grades.
- [ ] The guideline follows the organizational clinical structure.
- [ ] Multidisciplinary stakeholder input is documented.
- [ ] The PICO framework was used to define the scope.
- [ ] Conflict of interest declarations are complete.

## Related Skills

- `~~health/systematic-review` - For the deep evidence synthesis work.
- `~~health/policy-development` - To provide the governance framework for clinical advice.
- `~~health/quality-improvement` - To monitor guideline implementation and outcomes.

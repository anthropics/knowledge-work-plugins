---
name: qi-project
alias:
  - qip
  - quality-project
description: Initiate a healthcare quality improvement (QI) project with structured planning, PDSA cycle setup, and data collection framework.
arguments:
  - name: project_title
    description: "Name of the quality improvement project."
    required: true
  - name: aim_statement
    description: "The SMART aim statement describing what the project will achieve."
    required: true
  - name: current_state
    description: "Brief description of the current problem or baseline performance."
    required: true
  - name: team_lead
    description: "Name or role of the QI project team lead."
    required: true
  - name: target_metric
    description: "The primary outcome measure to track improvement."
    required: true
  - name: timeline_weeks
    description: "Estimated project duration in weeks."
    required: false
---

# QI Project Initiation

Use this command to kick off a structured quality improvement project with proper planning, PDSA cycle framework, and documentation setup.

## 1. Validate Input

- Ensure `aim_statement` follows SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound).
- If `aim_statement` is vague or incomplete, prompt for clarification.
- If `timeline_weeks` is not provided, default to 12 weeks for typical QI cycles.

## 2. Invoke Skill

Use `~~health/quality-improvement` to:
1. Validate the project structure against QI methodology.
2. Design the first PDSA cycle with specific objectives.
3. Define outcome, process, and balancing measures.
4. Identify required team members and stakeholders.
5. Map regulatory requirements for QI documentation.

## 3. Generate Structured Output

Produce:

### QI PROJECT CHARTER: {{project_title}}
- **Project ID**: [Generate unique ID: QI-YYYY-NNN]
- **Initiated**: {{current_timestamp}}
- **Team Lead**: {{team_lead}}
- **Timeline**: {{timeline_weeks or "12"}} weeks
- **Status**: INITIATED

---

### 1. AIM STATEMENT
{{aim_statement}}

**SMART Criteria Check**:
- [ ] Specific: Target population and scope defined
- [ ] Measurable: {{target_metric}} identified
- [ ] Achievable: Within organizational capacity
- [ ] Relevant: Aligns with strategic priorities
- [ ] Time-bound: {{timeline_weeks or "12"}}-week timeframe

---

### 2. CURRENT STATE ANALYSIS
**Problem Description**:
{{current_state}}

**Baseline Data Requirements**:
- Minimum 20-30 data points for {{target_metric}}
- Collection method: [Manual/Automated/Mixed]
- Data source: [EHR/Administrative/Chart audit]
- Operational definition: [To be defined]

---

### 3. MEASURES FRAMEWORK

| Measure Type | Measure Name | Operational Definition | Target | Collection Frequency |
|--------------|--------------|------------------------|--------|---------------------|
| **Outcome** | {{target_metric}} | [To be defined] | [To be set] | [Weekly/Monthly] |
| **Process** | [To be identified] | [To be defined] | [To be set] | [Daily/Weekly] |
| **Balancing** | [To be identified] | [To be defined] | No negative impact | [Weekly] |

---

### 4. PDSA CYCLE 1 PLAN

**Objective**: [First small test of change]

**Change Idea**: [Specific intervention to test]

**Prediction**: What we expect to happen

**Plan Details**:
- **Who**: Team members involved
- **What**: Specific actions
- **Where**: Unit/location
- **When**: Start and end dates
- **How**: Implementation approach

**Data Collection**:
- Measures to track
- Collection tools/forms
- Responsible person

---

### 5. TEAM STRUCTURE

| Role | Name/Position | Responsibility |
|------|---------------|----------------|
| **Team Lead** | {{team_lead}} | Overall project coordination |
| **Clinical Lead** | [To be assigned] | Clinical expertise and stakeholder engagement |
| **Data Analyst** | [To be assigned] | Measurement and statistical support |
| **Executive Sponsor** | [To be assigned] | Resource allocation and barrier removal |
| **Frontline Staff** | [To be identified] | Implementation and feedback |

---

### 6. PROJECT TIMELINE

| Phase | Activities | Duration | Week Target |
|-------|-----------|----------|-------------|
| **Initiation** | Charter, team formation, baseline | 1-2 weeks | Weeks 1-2 |
| **PDSA 1** | First test of change | 2-3 weeks | Weeks 3-5 |
| **PDSA 2** | Adapt and test again | 2-3 weeks | Weeks 6-8 |
| **PDSA 3+** | Scale or refine | 2-4 weeks | Weeks 9-12 |
| **Sustain** | Control plan, spread | Ongoing | Week 12+ |

---

### 7. REGULATORY & DOCUMENTATION

**NSQHS/EQuIP6 Alignment**:
- Standard 1: Governance for Safety and Quality
- Standard 3: Preventing and Controlling Healthcare-Associated Infections (if applicable)

**Required Documentation**:
- [ ] Project charter (this document)
- [ ] Ethics consideration (if research intent)
- [ ] Evidence/literature review
- [ ] Stakeholder communication plan
- [ ] Sustainability plan

**Privacy Considerations**:
- PHI access limited to project team
- De-identified data for analysis
- Secure storage in organizational QI repository

---

### 8. NEXT STEPS

1. [ ] **Finalize Team**: Confirm all team member assignments
2. [ ] **Collect Baseline**: Gather 20-30 data points for {{target_metric}}
3. [ ] **Operational Definitions**: Define precise measurement criteria
4. [ ] **Stakeholder Brief**: Present charter to relevant governance committee
5. [ ] **Kickoff Meeting**: Schedule team launch meeting (Week 1)
6. [ ] **Set Up Tracking**: Create run/control chart for {{target_metric}}
7. [ ] **Begin PDSA 1**: Execute first test of change

---

## 4. Execute Routing

- Save charter to `~~cloud storage` in QI project folder.
- Create project tracker entry in `~~project tracker` with milestones.
- Notify {{team_lead}} of project initiation.
- Schedule reminder for Week 2 baseline data review.

## 5. Output Guardrails

- **No PHI**: Do not include patient identifiers in project documentation.
- **Ethics Check**: If project involves research (generalizable knowledge), flag for Research Ethics Committee review.
- **QI vs Research**: This is a QI project (local improvement) unless generalizable knowledge is the primary goal.
- **Lite Mode**: If user requests quick start, generate minimal charter with just aim, measure, and first PDSA.

---

**Note**: This charter establishes the foundation for systematic improvement. Update with actual data as the project progresses through PDSA cycles.

---
description: Execute project closure including final deliverables, knowledge transfer, and lessons learned. Use when completing consulting engagements, concluding transformation initiatives, or formalizing project wrap-up.
argument-hint: "<project name and closure context>"
---

# /project-close -- Project Closure and Handover

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Execute comprehensive project closure following consulting best practices. Manages deliverables handover, knowledge transfer, final reporting, and captures lessons learned for organizational learning.

## Invocation

```
/project-close [project name and closure context]
```

If no context is provided, ask the user to describe the project, closure type, and any specific requirements.

## Workflow

### Step 1: Assess Closure Readiness

Verify completion criteria are met:

```
## Closure Readiness Assessment

### Completion Criteria Review
| Criterion | Status | Evidence | Owner |
|-----------|--------|----------|-------|
| All deliverables complete | [✓/✗] | [Location] | [Name] |
| Objectives achieved | [✓/✗] | [Evidence] | [Name] |
| Budget reconciled | [✓/✗] | [Documentation] | [Name] |
| Stakeholder sign-off | [✓/✗] | [Document] | [Name] |
| Resources released | [✓/✗] | [Confirmation] | [Name] |
| Contracts closed | [✓/✗] | [Documentation] | [Name] |

### Pre-Closure Checklist
- [ ] Final deliverables accepted by client
- [ ] Final invoice submitted (if applicable)
- [ ] Final status report approved
- [ ] All project issues resolved
- [ ] Change requests documented and closed
- [ ] Vendors/contractors notified
- [ ] Equipment/assets returned
- [ ] Access credentials revoked
- [ ] Team feedback collected

### Closure Type
| Type | Description | Requirements |
|------|-------------|--------------|
| Successful Completion | All objectives met | Full closure |
| Early Termination | Project cancelled | Document rationale |
| On Hold | Suspended temporarily | Document conditions |
| Rolled into BAU | Integrated into operations | Full handover |
```

### Step 2: Handover Deliverables

Transfer all project outputs to the client:

```
## Deliverable Handover

### Final Deliverables Inventory
| Deliverable | Version | Location | Handover Status |
|-------------|---------|----------|-----------------|
| [Deliverable 1] | [vX.X] | [Location] | [Complete/Pending] |
| [Deliverable 2] | [vX.X] | [Location] | [Complete/Pending] |
| [Deliverable 3] | [vX.X] | [Location] | [Complete/Pending] |

### Handover Documentation

#### User Handover Package
| Document | Description | Format |
|----------|-------------|--------|
| User Guide | How to use deliverables | [PDF/Word] |
| Quick Start | Getting started guide | [PDF] |
| FAQ | Common questions | [Document] |
| Training Materials | User training content | [Materials] |

#### Technical Handover Package
| Document | Description | Format |
|----------|-------------|--------|
| Technical Documentation | System/technical specs | [Location] |
| Architecture Diagrams | System design | [Diagrams] |
| API Documentation | Integration specs | [Location] |
| Support Contacts | Technical support info | [Document] |

### Client Acceptance
```
## Client Acceptance Certificate

Project Name: [Project Name]
Client: [Client Organization]
Consulting Firm: [Firm Name]
Completion Date: [Date]

DELIVERABLES ACCEPTED:
1. [Deliverable 1] - [Status]
2. [Deliverable 2] - [Status]

By signing below, the client confirms:
- All deliverables have been received and are acceptable
- All outstanding issues have been resolved
- The project is formally closed

Client Representative: _________________ Date: __________
[Name/Title]

Consulting Representative: _________________ Date: __________
[Name/Title]
```
```

### Step 3: Conduct Knowledge Transfer

Ensure the client can operate independently:

```
## Knowledge Transfer

### Knowledge Transfer Methods
| Method | Best For | Tools/Platforms |
|--------|----------|------------------|
| Live workshop | Complex processes | Digital collaboration tools |
| Recorded video | Procedural knowledge | Video recording tools |
| Documentation | Reference materials | Notion, Confluence |
| Interactive guides | Step-by-step tasks | WalkMe, Appcues |
| Async Q&A | Global teams | Slack, Teams |
| AI chatbot/Knowledge base | Ongoing support | Custom AI assistant |

### Knowledge Transfer Plan
| Topic | Transfer Method | Recipient | Date | Status |
|-------|----------------|-----------|------|--------|
| [Topic 1] | [Workshop/Manual/Training/Video] | [Name] | [Date] | [Complete/Pending] |
| [Topic 2] | [Workshop/Manual/Training/Video] | [Name] | [Date] | [Complete/Pending] |

### Digital Knowledge Handover Package
```
#### Digital Knowledge Package
| Document | Format | Platform | Access |
|----------|--------|----------|--------|
| Process documentation | Interactive | Notion/Confluence | Client access |
| Video tutorials | Streaming format | Video hosting platform | Link shared |
| Runbook | Markdown/HTML | GitWiki | URL provided |
| Decision database | Searchable | AI-enabled KB | Client setup |
| Architecture diagrams | Diagram format | Shared link | Access granted |
| AI/ML models (if applicable) | Model files | Cloud/Repository | Transfer complete |
```

### Knowledge Transfer Sessions
```
## Session 1: [Topic]
- Duration: [X hours]
- Presenter: [Name]
- Attendees: [Names]
- Key Points Covered:
  1. [Point]
  2. [Point]
  3. [Point]
- Questions Addressed:
  - [Q]: [A]
  - [Q]: [A]
- Follow-up Required: [Yes/No]

## Session 2: [Topic]
[Same structure]
```

### Documentation for Operations
| Document | Purpose | Owner | Location |
|----------|---------|-------|----------|
| Run Book | Day-to-day operations | [Role] | [Location] |
| Support Guide | Troubleshooting | [Role] | [Location] |
| Escalation Matrix | Issue escalation | [Role] | [Location] |
| Contact List | Key contacts | [Role] | [Location] |

### Support Transition
- **Transition Period**: [Date] to [Date]
- **Hypercare Support**: [X weeks]
- **BAU Support**: [Contact details]
- **Escalation Path**: [Details]
```

### Step 4: Document Lessons Learned

Capture insights for organizational improvement:

```
## Lessons Learned

### Retrospective Formats

#### 1. Start / Stop / Continue
```
### Start
- [Practice to begin]

### Stop
- [Practice to discontinue]

### Continue
- [Practice to maintain]
```

#### 2. 4Ls (Liked, Learned, Lacked, Longed For)
```
### Liked
- [What worked well]

### Learned
- [New knowledge gained]

### Lacked
- [What was missing]

### Longed For
- [What we wish we had]
```

#### 3. Sailboat Method
```
         Wind (helps us move forward)
            ↑
            |
     [ANCHOR] ←→ [ROCKS]
(slowing us)    (risks)
            |
          ↓
      [ISLAND]
   (destination)
```

### What Went Well
| Area | Success Factor | Evidence |
|------|---------------|----------|
| [Area 1] | [What worked] | [Example] |
| [Area 2] | [What worked] | [Example] |

### What Could Be Improved
| Area | Challenge | Recommendation |
|------|-----------|----------------|
| [Area 1] | [What didn't work] | [How to improve] |
| [Area 2] | [What didn't work] | [How to improve] |

### Digital Transformation Lessons
| Category | Lesson | Application |
|----------|--------|------------|
| AI/ML Implementation | [Key learning] | [How to apply] |
| Data Strategy | [Key learning] | [How to apply] |
| Digital Adoption | [Key learning] | [How to apply] |

### Process Improvement Recommendations
| Recommendation | Priority | Expected Benefit | Effort |
|----------------|----------|------------------|--------|
| [Rec 1] | [High/Med/Low] | [Benefit] | [High/Med/Low] |
| [Rec 2] | [High/Med/Low] | [Benefit] | [High/Med/Low] |

### Lessons Learned Session
```
## Session: [Project Name] Retrospective
Date: [Date]
Participants: [Names]
Format: [In-person/Virtual/Hybrid]

## Key Insights
1. [Insight and its source]
2. [Insight and its source]

## Quotes
"[Quote from participant]" - [Name]
"[Quote from participant]" - [Name]

## Digital Tools Adopted
- [Tool 1]: [Usage context]
- [Tool 2]: [Usage context]

## AI/Technology Learnings
[Specific learnings about technology used in the project]
```
```

### Step 5: Finalize Administrative Closure

Complete all administrative tasks:

```
## Administrative Closure

### Financial Closure
| Item | Amount | Status |
|------|--------|--------|
| Total Budget | $[Amount] | - |
| Actual Spend | $[Amount] | - |
| Variance | $[Amount] ([X]%) | - |
| Final Invoice | $[Amount] | [Sent/Paid] |
| Final Expenses | $[Amount] | [Submitted] |

### Resource Release
| Resource | Assignment End | Status |
|----------|----------------|--------|
| [Team Member 1] | [Date] | [Released] |
| [Team Member 2] | [Date] | [Released] |

### Contract Closure
| Contract | Vendor | Final Payment | Status |
|----------|--------|---------------|--------|
| [Contract 1] | [Vendor] | $[Amount] | [Closed] |

### Documentation Archive
| Document | Location | Retention |
|----------|----------|-----------|
| Project Charter | [Location] | [X years] |
| Status Reports | [Location] | [X years] |
| Deliverables | [Location] | [Per policy] |
| Lessons Learned | [Location] | [X years] |

### Team Recognition
| Team Member | Contribution | Recognition |
|-------------|--------------|-------------|
| [Name] | [Contribution] | [Recognition type] |
```
```

### Step 6: Conduct Final Reporting

Create the final project summary:

```
## Final Project Report

### Project Summary
| Field | Value |
|-------|-------|
| Project Name | [Name] |
| Client | [Organization] |
| Project Manager | [Name] |
| Start Date | [Date] |
| End Date | [Date] |
| Total Duration | [X months] |
| Final Budget | $[Amount] |
| Final Spend | $[Amount] |
| Budget Variance | $[Amount] ([X]%) |

### Objectives Achievement
| Objective | Target | Achieved | Evidence |
|-----------|--------|----------|----------|
| [Obj 1] | [Target] | [Yes/No/Partial] | [Evidence] |
| [Obj 2] | [Target] | [Yes/No/Partial] | [Evidence] |

### Deliverables Summary
- Total Planned: [n]
- Completed: [n]
- Accepted: [n]

### Benefits Realized
| Benefit | Target | Actual | Variance |
|---------|--------|--------|----------|
| [Benefit 1] | $[Target] | $[Actual] | [Variance] |
| [Benefit 2] | [Target] | [Actual] | [Variance] |

### Key Success Factors
1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

### Challenges Overcome
1. [Challenge 1] - [How addressed]
2. [Challenge 2] - [How addressed]

### Client Feedback
"[Feedback quote]" - [Client Name, Title]

### Recommendations
1. [Recommendation]
2. [Recommendation]
```

## Output Format

```
# Project Closure Report: [Project Name]

## Executive Summary
[Overview: objectives, outcomes, key metrics]

## 1. Project Overview
### Objectives
[List of original objectives]

### Scope
[What was included and excluded]

### Timeline
| Phase | Start | End | Duration |
|-------|-------|-----|----------|
| [Phase 1] | [Date] | [Date] | [Weeks] |

## 2. Deliverables
### Completed Deliverables
[List with status and location]

### Handover Status
[Confirmation of handover completion]

## 3. Financial Summary
### Budget Performance
| Metric | Budget | Actual | Variance |
|--------|--------|--------|----------|
| Total | $[X] | $[X] | $[X] |

## 4. Benefits
### Achieved Benefits
[List quantified benefits]

### Expected Future Benefits
[List benefits to be realized post-project]

## 5. Lessons Learned
### Success Factors
[What worked well]

### Improvement Areas
[What could be improved]

### Recommendations
[Specific recommendations for future projects]

## 6. Team Recognition
[Recognition of team contributions]

## 7. Appendices
### A: Deliverable Inventory
[Complete list]

### B: Change Log
[All changes made]

### C: Risk Register
[Final risk status]

### D: Stakeholder List
[Final stakeholder register]

---
Report Prepared By: [Name]
Date: [Date]
Client Acceptance Date: [Date]
```

## Notes

- Don't skip lessons learned - they're invaluable for organizational learning
- Ensure handover is complete before reducing support
- Get formal sign-off on acceptance certificates
- Archive all project documentation properly
- Release resources promptly when work is done
- Follow up on any post-project commitments
- Celebrate team success before closing
- Conduct a proper retrospective, not just paperwork
- Ensure client is fully equipped to operate independently
- Document any ongoing obligations or warranties
- Close out all contracts and financial obligations
- Update organizational knowledge bases with lessons

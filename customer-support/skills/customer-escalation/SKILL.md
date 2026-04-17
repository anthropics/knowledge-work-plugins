---
name: customer-escalation
description: Package an escalation for engineering, product, or leadership with full context. Use when a bug needs engineering attention beyond normal support, multiple customers report the same issue, a customer is threatening to churn, or an issue has sat unresolved past its SLA.
argument-hint: "<issue summary> [customer name]"
---

# /customer-escalation

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Package a support issue into a structured escalation brief for engineering, product, or leadership. Gathers context, structures reproduction steps, assesses business impact, and identifies the right escalation target.

## Usage

```
/customer-escalation <issue description> [customer name or account]
```

Examples:
- `/customer-escalation API returning 500 errors intermittently for Acme Corp`
- `/customer-escalation Data export is missing rows — 3 customers reported this week`
- `/customer-escalation SSO login loop affecting all Enterprise customers`
- `/customer-escalation Customer threatening to churn over missing audit log feature`

## Workflow

### 1. Understand the Issue

Parse the input and determine:

- **What's broken or needed**: The core technical or product issue
- **Who's affected**: Specific customer(s), segment, or all users
- **How long**: When did this start? How long has the customer been waiting?
- **What's been tried**: Any troubleshooting or workarounds attempted
- **Why escalate now**: What makes this need attention beyond normal support

Use the "When to Escalate vs. Handle in Support" criteria below to confirm this warrants escalation.

### 2. Gather Context

Pull together relevant information from available sources:

- **~~support platform**: Related tickets, timeline of communications, previous troubleshooting
- **~~CRM** (if connected): Account details, key contacts, previous escalations
- **~~chat**: Internal discussions about this issue, similar reports from other customers
- **~~project tracker** (if connected): Related bug reports or feature requests, engineering status
- **~~knowledge base**: Known issues or workarounds, relevant documentation

### 3. Assess Business Impact

Using the impact dimensions below, quantify:

- **Breadth**: How many customers/users affected? Growing?
- **Depth**: Blocked vs. inconvenienced?
- **Duration**: How long has this been going on?
- **Revenue**: ARR at risk? Pending deals affected?
- **Time pressure**: Hard deadline?

### 4. Determine Escalation Target

Using the escalation tiers below, identify the right target: L2 Support, Engineering, Product, Security, or Leadership.

### 5. Structure Reproduction Steps (for bugs)

If the issue is a bug, follow the reproduction step best practices below to document clear repro steps with environment details and evidence.

### 6. Generate Escalation Brief

```
## ESCALATION: [One-line summary]

**Severity:** [Critical / High / Medium]
**Target team:** [Engineering / Product / Security / Leadership]
**Reported by:** [Your name/team]
**Date:** [Today's date]

### Impact
- **Customers affected:** [Who and how many]
- **Workflow impact:** [What they can't do]
- **Revenue at risk:** [If applicable]
- **Time in queue:** [How long this has been an issue]

### Issue Description
[Clear, concise description of the problem — 3-5 sentences]

### What's Been Tried
1. [Troubleshooting step and result]
2. [Troubleshooting step and result]
3. [Troubleshooting step and result]

### Reproduction Steps
[If applicable — follow the format below]
1. [Step]
2. [Step]
3. [Step]
Expected: [X]
Actual: [Y]
Environment: [Details]

### Customer Communication
- **Last update to customer:** [Date and what was communicated]
- **Customer expectation:** [What they're expecting and by when]
- **Escalation risk:** [Will they escalate further if not resolved by X?]

### What's Needed
- [Specific ask — "investigate root cause", "prioritize fix",
  "make product decision on X", "approve exception for Y"]
- **Deadline:** [When this needs resolution or an update]

### Supporting Context
- [Related tickets or links]
- [Internal discussion threads]
- [Documentation or logs]
```

### 7. Offer Next Steps

After generating the escalation:
- "Want me to post this in a ~~chat channel for the target team?"
- "Should I update the customer with an interim response?"
- "Want me to set a follow-up reminder to check on this?"
- "Should I draft a customer-facing update with the current status?"

---

## When to Escalate vs. Handle in Support

### Handle in Support When:
- The issue has a documented solution or known workaround
- It's a configuration or setup issue you can resolve
- The customer needs guidance or training, not a fix
- The issue is a known limitation with a documented alternative
- Previous similar tickets were resolved at the support level

### Escalate When:
- **Technical**: Bug confirmed and needs a code fix, infrastructure investigation needed, data corruption or loss
- **Complexity**: Issue is beyond support's ability to diagnose, requires access support doesn't have, involves custom implementation
- **Impact**: Multiple customers affected, production system down, data integrity at risk, security concern
- **Business**: High-value customer at risk, SLA breach imminent or occurred, customer requesting executive involvement
- **Time**: Issue has been open beyond SLA, customer has been waiting unreasonably long, normal support channels aren't progressing
- **Pattern**: Same issue reported by 3+ customers, recurring issue that was supposedly fixed, increasing severity over time

## Escalation Tiers

### L1 → L2 (Support Escalation)
**From:** Frontline support
**To:** Senior support / technical support specialists
**When:** Issue requires deeper investigation, specialized product knowledge, or advanced troubleshooting
**What to include:** Ticket summary, steps already tried, customer context

### L2 → Engineering
**From:** Senior support
**To:** Engineering team (relevant product area)
**When:** Confirmed bug, infrastructure issue, needs code change, requires system-level investigation
**What to include:** Full reproduction steps, environment details, logs or error messages, business impact, customer timeline

### L2 → Product
**From:** Senior support
**To:** Product management
**When:** Feature gap causing customer pain, design decision needed, workflow doesn't match customer expectations, competing customer needs require prioritization
**What to include:** Customer use case, business impact, frequency of request, competitive pressure (if known)

### Any → Security
**From:** Any support tier
**To:** Security team
**When:** Potential data exposure, unauthorized access, vulnerability report, compliance concern
**What to include:** What was observed, who/what is potentially affected, immediate containment steps taken, urgency assessment
**Note:** Security escalations bypass normal tier progression — escalate immediately regardless of your level

### Any → Leadership
**From:** Any tier (usually L2 or manager)
**To:** Support leadership, executive team
**When:** High-revenue customer threatening churn, SLA breach on critical account, cross-functional decision needed, exception to policy required, PR or legal risk
**What to include:** Full business context, revenue at risk, what's been tried, specific decision or action needed, deadline

## Business Impact Assessment

When escalating, quantify impact where possible:

### Impact Dimensions

| Dimension | Questions to Answer |
|-----------|-------------------|
| **Breadth** | How many customers/users are affected? Is it growing? |
| **Depth** | How severely are they impacted? Blocked vs. inconvenienced? |
| **Duration** | How long has this been going on? How long until it's critical? |
| **Revenue** | What's the ARR at risk? Are there pending deals affected? |
| **Reputation** | Could this become public? Is it a reference customer? |
| **Contractual** | Are SLAs being breached? Are there contractual obligations? |

### Severity Shorthand

- **Critical**: Production down, data at risk, security breach, or multiple high-value customers affected. Needs immediate attention.
- **High**: Major functionality broken, key customer blocked, SLA at risk. Needs same-day attention.
- **Medium**: Significant issue with workaround, important but not urgent business impact. Needs attention this week.

## Writing Reproduction Steps

Good reproduction steps are the single most valuable thing in a bug escalation. Follow these practices:

1. **Start from a clean state**: Describe the starting point (account type, configuration, permissions)
2. **Be specific**: "Click the Export button in the top-right of the Dashboard page" not "try to export"
3. **Include exact values**: Use specific inputs, dates, IDs — not "enter some data"
4. **Note the environment**: Browser, OS, account type, feature flags, plan level
5. **Capture the frequency**: Always reproducible? Intermittent? Only under certain conditions?
6. **Include evidence**: Screenshots, error messages (exact text), network logs, console output
7. **Note what you've ruled out**: "Tested in Chrome and Firefox — same behavior" "Not account-specific — reproduced on test account"

## Follow-up Cadence After Escalation

Don't escalate and forget. Maintain ownership of the customer relationship.

| Severity | Internal Follow-up | Customer Update |
|----------|-------------------|-----------------|
| **Critical** | Every 2 hours | Every 2-4 hours (or per SLA) |
| **High** | Every 4 hours | Every 4-8 hours |
| **Medium** | Daily | Every 1-2 business days |

### Follow-up Actions
- Check with the receiving team for progress
- Update the customer even if there's no new information ("We're still investigating — here's what we know so far")
- Adjust severity if the situation changes (better or worse)
- Document all updates in the ticket for audit trail
- Close the loop when resolved: confirm with customer, update internal tracking, capture learnings

## De-escalation

Not every escalation stays escalated. De-escalate when:
- Root cause is found and it's a support-resolvable issue
- A workaround is found that unblocks the customer
- The issue resolves itself (but still document root cause)
- New information changes the severity assessment

When de-escalating:
- Notify the team you escalated to
- Update the ticket with the resolution
- Inform the customer of the resolution
- Document what was learned for future reference

## Escalation Best Practices

1. Always quantify impact — vague escalations get deprioritized
2. Include reproduction steps for bugs — this is the #1 thing engineering needs
3. Be clear about what you need — "investigate" vs. "fix" vs. "decide" are different asks
4. Set and communicate a deadline — urgency without a deadline is ambiguous
5. Maintain ownership of the customer relationship even after escalating the technical issue
6. Follow up proactively — don't wait for the receiving team to come to you
7. Document everything — the escalation trail is valuable for pattern detection and process improvement

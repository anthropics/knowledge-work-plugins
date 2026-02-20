---
name: dependency-readiness
description: >
  Proactively check whether external and internal dependencies are ready
  for a milestone. Tracks vendor deliverables, partner integrations,
  cross-team handoffs, infrastructure provisioning, and third-party
  services. Use before a launch, release, or deadline to catch ecosystem
  gaps that internal checks won't surface.
---

# Dependency Readiness

You are a **Dependency Tracker** — you check whether everything *outside* the team's direct control is ready for the milestone. In modern teams, dependencies are rarely entirely missing — environments exist, integrations are built, vendors are engaged. The real problems are subtler: a runbook that hasn't been updated, a config that's awaiting latest input, a partner briefed on v1 but not v2, a feature flag pointing at the wrong environment. Your job is to catch these freshness and correctness gaps before they become launch-day surprises.

**Core question:** *Is everything we depend on — but don't directly control — actually ready?*

**Example triggers:**
- "Check if our dependencies are ready for launch"
- "Are all vendor deliverables in for the Q2 milestone?"
- "What's the status of our external dependencies?"
- "Pre-launch dependency check"
- "Any stale configs or out-of-date integrations?"
- "Check partner integration status"

---

## Assumptions

This skill assumes teams follow modern practices:

- **Environments exist** — Production is already running. Staging mirrors prod. Blue-green or canary deployments are normal. The question isn't "is the environment provisioned?" but "is the environment configured correctly for this release?"
- **Integrations are built** — Partner/vendor integrations are already in place. The question isn't "does the integration exist?" but "is it pointing at the right version/endpoint/config?"
- **People are engaged** — Vendors, partners, and cross-team contacts have been briefed. The question isn't "do they know about this?" but "do they have the *latest* information?"
- **Automation is normal** — CI/CD, feature flags, automated tests are standard. The question isn't "can we deploy?" but "are the automation configs (flags, pipelines, rollback playbooks) current?"

**The typical dependency problem is not absence — it's staleness.** Things that were correct last week may not reflect this week's changes.

---

## How It Works

**Step 1: Identify Dependencies**

Build the dependency list from available sources:

| Source | What to Look For |
|--------|-----------------|
| ~~project tracker | Items tagged as dependencies, blocked-by links, external labels |
| `risk-tracker` | External dependency issues, cross-team blockers |
| REFERENCES.md | Configured vendor/partner references |
| User input | "We depend on X, Y, Z for this milestone" |

If no dependencies are tracked, ask: *"What does this milestone depend on that your team doesn't directly control? Think: vendors, other teams, infrastructure, approvals, external services."*

**Step 2: Classify Each Dependency**

Every dependency falls into one of these categories:

| Type | Description | Examples |
|------|-------------|---------|
| **Vendor** | Third-party deliverables or services | API versions, vendor software updates, agency assets, contracted work |
| **Partner** | External organizations you're integrating with | Partner API versions, co-marketing materials, joint deliverables |
| **Cross-team** | Internal teams outside your direct control | Platform team configs, security review sign-off, design handoff |
| **Config** | Environment configs, feature flags, automation | Feature flags, deployment configs, rollback playbooks, CI/CD pipelines |
| **Regulatory** | External bodies or processes | Certification, compliance approval, regulatory response |
| **Documentation** | Runbooks, playbooks, briefing materials | Launch runbook, support playbook, partner briefing docs, release notes |

**Step 3: Check Readiness**

For each dependency, determine its state:

| State | Meaning | Icon |
|-------|---------|------|
| **Ready** | Verified correct and current for this milestone | ✅ |
| **In Progress** | Being updated, expected on time | 🔄 |
| **Stale** | Exists but not updated for this milestone — needs refresh | 🔶 |
| **At Risk** | May not be ready or current by milestone date | ⚠️ |
| **Not Ready** | Missing, incorrect, or will not be ready | ❌ |
| **Unknown** | Status hasn't been checked or confirmed | ❓ |

**Stale is the most common state.** Dependencies that existed for the last milestone often carry forward with outdated configs, old versions, or last-cycle briefing materials. Always check for currency, not just existence.

**Unknown is dangerous.** An unchecked dependency is not a ready dependency. Always surface unknowns prominently.

**How to check:**

| Dependency Type | What to Verify |
|----------------|---------------|
| Vendor | Is the version/endpoint current? Has config changed since last verified? |
| Partner | Are they briefed on latest scope? Is their deliverable current? |
| Cross-team | Has their config been updated for this milestone? Is their sign-off current? |
| Config | Are feature flags, deployment configs, and rollback playbooks updated? |
| Regulatory | Is submission on track? Any changes to requirements since filing? |
| Documentation | Is the runbook current? Does it reflect latest architecture/process changes? |

**Step 4: Identify Critical Path**

Not all dependencies are equal. Identify which are on the critical path:

```
A dependency is critical-path if:
  - The milestone CANNOT proceed without it, AND
  - It has no workaround or fallback
```

Mark critical-path dependencies explicitly. A single ❌, 🔶, or ❓ on a critical-path dependency = milestone is not ready.

**Step 5: Output**

Use the project-intelligence output style (see [output style](../../output-styles/project-intelligence.md)).

```markdown
# Dependency Readiness | [Milestone Name]

**Target:** [date]
**Dependencies checked:** [N] of [N] verified
**Critical path clear:** ✅ Yes / ❌ No

---

## Dependency Status

| # | Dependency | Type | Owner | Status | Critical Path | Notes |
|---|-----------|------|-------|--------|--------------|-------|
| 1 | [Name] | [type] | [who] | ✅/🔄/🔶/⚠️/❌/❓ | Yes/No | [brief note] |
| 2 | [Name] | [type] | [who] | ✅/🔄/🔶/⚠️/❌/❓ | Yes/No | [brief note] |

---

## Issues

### Not Ready
- ❌ [Dependency]: [why it's not ready + impact on milestone]

### Stale (Needs Refresh)
- 🔶 [Dependency]: [what's outdated + what needs updating]

### At Risk
- ⚠️ [Dependency]: [what's at risk + expected resolution]

### Unknown (Unverified)
- ❓ [Dependency]: [hasn't been checked — recommend verifying immediately]

---

## Actions
1. [Highest priority action]
2. [Next action]

---

## Assessment
[1-2 sentence summary: critical path status and biggest dependency risk]
```

---

## Edge Cases

**No dependencies identified:**
- Ask the user explicitly. If they confirm none, note: "No external dependencies identified. This milestone is fully within team control."

**Dependency has a workaround:**
- Note the workaround. If viable, the dependency is not critical-path even if not ready: "Payment API not ready, but can launch with PayPal fallback."

**Dependency owned by nobody:**
- Flag prominently: "No owner identified for [dependency]. Assign an owner immediately."

**Dependency was ready but regressed:**
- Note the regression: "Was ✅ on [date], now ❌. [What changed]." This is worse than never being ready — escalate.

**Cascading dependencies:**
- If Dependency A depends on Dependency B, note the chain. Same cascade logic as `risk-tracker`.

---

## Examples

### Example 1: Software Deployment — Stale Configs

**User:** "Check dependencies for v3.1 deployment Friday"

```markdown
# Dependency Readiness | v3.1 Deployment

**Target:** Feb 14
**Dependencies checked:** 5 of 6 verified
**Critical path clear:** ⚠️ At risk — 2 stale items

---

## Dependency Status

| # | Dependency | Type | Owner | Status | Critical Path | Notes |
|---|-----------|------|-------|--------|--------------|-------|
| 1 | Blue-green deploy config | Config | DevOps | 🔶 | Yes | Last updated for v3.0 — needs new env vars for auth changes |
| 2 | Auth0 tenant config | Vendor | Auth0 support | ✅ | Yes | Updated and tested for v3.1 |
| 3 | Rollback runbook | Documentation | SRE | 🔶 | Yes | Still references v2.x rollback steps — needs update |
| 4 | Stripe webhook endpoint | Partner | Payments team | ✅ | Yes | Endpoint updated, integration tests pass |
| 5 | Feature flags | Config | Engineering | ✅ | No | All v3.1 flags configured in LaunchDarkly |
| 6 | Amplitude event schema | Vendor | Analytics | ❓ | No | Not checked — new events in v3.1 may need schema update |

---

## Issues

### Stale (Needs Refresh)
- 🔶 **Blue-green deploy config (critical path):** Config still has v3.0 env vars. New auth service endpoint and secrets need to be added before deploy.
- 🔶 **Rollback runbook (critical path):** Runbook references v2.x database migration rollback steps. v3.1 changes auth tables — rollback procedure is different.

### Unknown
- ❓ **Amplitude event schema:** v3.1 adds 3 new tracking events. Schema may need updating in Amplitude. Low risk but should verify.

---

## Actions
1. **UPDATE:** Blue-green config — add new auth service env vars and secrets
2. **UPDATE:** Rollback runbook — document v3.1 auth table migration rollback
3. **VERIFY:** Check Amplitude event schema for new v3.1 events

---

## Assessment
Infrastructure is healthy — blue-green environments are running, integrations work. Two stale configs need updating: deploy config (wrong env vars) and rollback runbook (wrong procedure). Not blocked, but deploying with stale rollback docs is risky.
```

### Example 2: Marketing Campaign Launch — Last-Mile Config

**User:** "Are our dependencies ready for the Q2 campaign launch March 15?"

```markdown
# Dependency Readiness | Q2 Campaign Launch

**Target:** March 15
**Dependencies checked:** 5 of 5 verified
**Critical path clear:** ⚠️ At risk — 1 stale, 1 at risk

---

## Dependency Status

| # | Dependency | Type | Owner | Status | Critical Path | Notes |
|---|-----------|------|-------|--------|--------------|-------|
| 1 | Agency creative assets | Vendor | Acme Agency | ✅ | Yes | Final assets delivered and deployed Feb 28 |
| 2 | Ad platform campaign config | Config | Media team | ⚠️ | Yes | Configs built but awaiting final targeting input from product |
| 3 | Influencer briefing materials | Documentation | PR team | 🔶 | No | Influencers briefed on v1 messaging — v2 positioning not shared |
| 4 | Landing page | Cross-team | Engineering | ✅ | Yes | Deployed and tested on staging, ready for prod swap |
| 5 | Email sequences | Config | Growth team | ✅ | No | All sequences configured and tested in staging |

---

## Issues

### Stale (Needs Refresh)
- 🔶 **Influencer briefing materials:** 3 influencers were briefed on v1 messaging (Jan). Product positioning shifted in Feb — updated talking points not shared yet.

### At Risk
- ⚠️ **Ad campaign config (critical path):** Campaign structure is built in Meta/Google Ads but final audience targeting awaits product team input on segment priorities. If not received by March 8, launch configs won't be tested in time.

---

## Actions
1. **URGENT:** Get final targeting input from product team for ad configs — deadline March 8
2. **UPDATE:** Send updated v2 briefing materials to influencers — not urgent but affects message consistency

---

## Assessment
Assets are delivered and deployed. Infrastructure is ready. Two last-mile items: ad campaign targeting config needs final input (critical path), and influencer messaging is one version behind (not critical but affects consistency). Resolve targeting input by March 8.
```

### Example 3: Compliance Milestone — Multiple Unknowns

**User:** "Dependency check for SOC 2 audit March 31"

```markdown
# Dependency Readiness | SOC 2 Audit Submission

**Target:** March 31
**Dependencies checked:** 2 of 5 verified
**Critical path clear:** ❌ No — 3 dependencies unverified

---

## Dependency Status

| # | Dependency | Type | Owner | Status | Critical Path | Notes |
|---|-----------|------|-------|--------|--------------|-------|
| 1 | Auditor availability | Regulatory | Deloitte | ✅ | Yes | Confirmed March 24-28 window |
| 2 | Cloud provider SOC 2 report | Vendor | AWS | ✅ | Yes | Bridge letter received Feb 15 |
| 3 | HR background check evidence | Cross-team | HR | ❓ | Yes | Not checked — need employee records |
| 4 | Vendor security assessments | Cross-team | Procurement | ❓ | Yes | Not checked — need vendor questionnaires |
| 5 | Physical security logs | Cross-team | Facilities | ❓ | No | Not checked — need access logs |

---

## Issues

### Unknown (Unverified)
- ❓ **HR background check evidence (critical path):** Auditor will request. Status unknown — verify HR has current records for all employees.
- ❓ **Vendor security assessments (critical path):** Auditor will review. Unknown if procurement has completed questionnaires for all critical vendors.
- ❓ **Physical security logs:** Lower priority but auditor may request. Verify facilities can provide.

---

## Actions
1. **URGENT:** Contact HR to confirm background check evidence availability — critical path
2. **URGENT:** Contact Procurement for vendor security assessment status — critical path
3. **VERIFY:** Ask Facilities about physical security log access
4. **GOOD NEWS:** Auditor and AWS bridge letter are confirmed

---

## Assessment
Only 2 of 5 dependencies verified. 3 unknowns on the critical path — this is a blind spot. The external dependencies (auditor, AWS) are solid, but internal cross-team evidence gathering is unverified. Contact HR and Procurement immediately to assess readiness.
```

---

## Key Principles

1. **Currency over existence** — The question is rarely "does this exist?" It's "is this current and correct for *this* milestone?"
2. **Stale is the default** — Assume dependencies from the last milestone need refreshing until verified otherwise.
3. **Unknown ≠ Ready** — An unchecked dependency is a blind spot, not a green light.
4. **Critical path focus** — A non-critical dependency being stale is a warning; a critical-path one stale is a blocker.
5. **Check early, check often** — Run this skill early in the milestone, not just at the gate.
6. **Own every dependency** — Every dependency needs an owner. An unowned dependency is the most dangerous kind.
7. **Regressions are worse than gaps** — A dependency that was verified and drifted needs urgent attention.

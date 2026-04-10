# Telemetry Principles

Core beliefs that guide this plugin's recommendations.

## 1. Telemetry is Infrastructure

Product telemetry is not an afterthought. It's infrastructure that enables all future analysis, experimentation, and data-driven decisions.

**Implication:** Invest in getting it right early. The cost of fixing bad telemetry compounds over time.

## 2. Plan First, Implement Second

Never add tracking ad-hoc. Always:
1. Define the event in the tracking plan
2. Review and approve
3. Then implement

**Implication:** The tracking plan is the source of truth. Code should match the plan, not the other way around.

## 3. Track Behaviors, Not Metrics

Events capture what users **do**. Metrics are derived from events later.

- ✅ Track: `report.created`
- ❌ Track: `weekly_active_users` (this is a metric, not an event)

**Implication:** Design events to answer "what happened?" not "what's the number?"

## 4. B2B Means Two Entities

In B2B SaaS, both **users** and **accounts** are first-class entities.

Every event should be attributable to:
- A user (who did it)
- An account (which organization)

**Implication:** Always call `group()` or include `account_id`. Never lose account context.

## 5. Opinionated Defaults Beat Flexibility

Make decisions. Take positions. Consistency matters more than flexibility.

- Pick a naming convention and enforce it
- Pick an event structure and stick to it
- Pick a property schema and standardize

**Implication:** It's better to have a "wrong" consistent standard than no standard.

## 6. Less is More (Usually)

Every event has costs:
- Implementation cost
- Maintenance cost
- Storage cost
- Cognitive cost (understanding the data)

**Implication:** Track what you need to answer questions, not everything you *might* need.

## 7. Properties Over Events

When in doubt, add a property to an existing event rather than creating a new event.

- ✅ `report.created { report_type: "template" }`
- ❌ `report.created` + `template_report.created`

**Implication:** Keep event count manageable; use properties for variation.

## 8. IDs Over Values

Include IDs, not full values:

- ✅ `{ user_id: "usr_123" }`
- ❌ `{ user_email: "jane@example.com" }`

**Implication:** IDs enable joins; values create PII risk and storage bloat.

## 9. Outcomes Over Mechanisms

Track what happened, not how it happened:

- ✅ `report.created`
- ❌ `create_report_button.clicked`

**Implication:** If the button changes, the event still makes sense.

## 10. Future-Proof, Not Future-Guess

Track what you need to support **any reasonable future analysis**, but don't speculate.

**Good question:** "Could we analyze activation paths with this?"
**Bad question:** "What if someday we want to know X?"

**Implication:** Cover the categories (lifecycle, core value, etc.) but don't track speculatively.

## 11. Implementation-Aware Design

A tracking plan that can't be implemented is useless.

Consider:
- SDK capabilities and limitations
- Performance implications
- Developer experience
- Testability

**Implication:** Design with implementation in mind. Generate real code.

## 12. Version and Document

Tracking plans change. Products evolve.

- Version your tracking plan
- Keep a changelog
- Document breaking changes
- Plan deprecations

**Implication:** Treat tracking plan like a schema—with migrations.

## 13. Validation is Cheaper Than Debugging

Catch tracking issues at implementation time, not when dashboards break.

- Type-safe instrumentation code
- Runtime validation in development
- Automated tests for critical events
- Monitoring for production issues

**Implication:** Build validation into the workflow.

## 14. Ownership Matters

Someone owns the tracking plan. Someone reviews changes. Someone maintains it.

Without ownership:
- Events drift from the plan
- Documentation goes stale
- Quality degrades

**Implication:** Assign ownership. Make it part of the product process.

## 15. Align Tracking with Business Goals

Before choosing what to track, identify the key metrics that align with your business goals. Different goals require different tracking strategies:

- **User acquisition:** Focus on signups, referrals, onboarding completion
- **Engagement:** Focus on feature usage, session frequency, core value actions
- **Retention:** Focus on repeat usage, subscription renewals, continued feature engagement

Overloading your system with too many data points leads to unnecessary complexity and makes it harder to derive meaningful insights. Start by identifying the business questions you need to answer, then design events that answer those questions.

**Implication:** Tracking strategy should be goal-driven, not feature-driven. Track what helps you make decisions, not everything that happens.

## 16. Start Small, Iterate

You don't need perfect telemetry on day one.

Start with:
1. Lifecycle events (signup, activation)
2. Core value events (the thing you exist for)
3. Billing events (commercial signals)

Add more as questions arise.

**Implication:** Ship something correct, then expand.

# Event Categories for B2B SaaS

Every B2B SaaS tracking plan should cover these categories. Not every product needs every event, but every product should consciously decide what's in and what's out.

**Cost principle:** On most analytics platforms (except Accoil), every event tracked has a direct billing cost. The categories below are ordered roughly by analytical value. Lifecycle, Core Value, and Collaboration events almost always justify their cost. Configuration events usually do. Navigation events rarely do. When deciding what to include, weigh the insight value against the volume and cost each event will generate.

## When to Use Events vs. Properties vs. Traits

Before designing your event taxonomy, understand when to use each data element:

- **Use Events** to capture every significant user action, providing the foundational data needed to understand how users are interacting with your product. Events answer "what happened?"
- **Use Properties** to add context to these actions, enabling more nuanced analysis that uncovers insights into user preferences, behaviors, and decision-making processes. Properties answer "how did it happen?" and "in what context?"
- **Use Traits** to maintain consistent user and account attributes over time, which are critical for segmentation, personalization, and targeted communication. Traits answer "who is this user/account?"

**The decision test:** If the data describes an action, it is an event. If it provides context for that action, it is a property. If it describes an enduring characteristic of the user or account that persists across sessions, it is a trait set via `identify()` or `group()`.

## Aligning Tracking with Business Goals

Before choosing which categories to prioritize, identify the key metrics that align with your business goals:

- **User acquisition:** Prioritize lifecycle events -- signups, referrals, onboarding completion
- **Engagement:** Prioritize core value and feature usage events -- the actions that demonstrate product value
- **Retention:** Prioritize events that indicate long-term value -- repeat usage, subscription renewals, continued feature engagement

Overloading your system with too many data points leads to unnecessary complexity. Start with the categories that answer your most pressing business questions, then expand as new questions arise.

## Naming Patterns Within Categories

Each category tends to follow a predictable naming pattern. Recognizing the pattern makes it easier to name new events consistently and to spot events that are in the wrong category.

| Category | Naming Pattern | Examples |
|----------|---------------|----------|
| CRUD Operations | `[Object] [CRUD Verb]` | `Todo Created`, `Todo Updated`, `Todo Deleted` |
| Feature Usage | `[Feature] [Action Taken]` | `Advanced Search Performed`, `Bulk Export Generated` |
| User Workflows | `[Workflow] [Completion State]` | `Onboarding Completed`, `Setup Wizard Abandoned` |
| Errors | `[Context] Error Occurred` | `API Error Occurred`, `Validation Error Occurred` |

These patterns keep naming predictable. When a developer needs to add a new event, the category pattern tells them what the name should look like.

## 1. Lifecycle Events

User journey from first touch to churn.

| Event | Description | When to use |
|-------|-------------|-------------|
| `user.signed_up` | User creates an account | Always |
| `user.invited` | Existing user invites someone | If multiplayer |
| `user.onboarded` | User completes onboarding flow | If formal onboarding exists |

Note: "Activation" is computed downstream from core value events, not tracked as a separate event.

**Account-level equivalents:**
- `account.created`
- `account.churned`

## 2. Core Value Actions

The actions that *are* your product. If users never do these, they're not really using you.

These are **product-specific**. Examples:

| Product Type | Core Value Events |
|--------------|-------------------|
| Project management | `project.created`, `task.completed`, `task.assigned` |
| Analytics | `report.created`, `dashboard.viewed`, `insight.generated` |
| Communication | `message.sent`, `channel.created`, `call.started` |
| E-commerce | `order.placed`, `product.viewed`, `cart.updated` |

**How to identify core value actions:**
- What would a user *pay* for?
- What does your pricing page promise?
- If this event count went to zero, would you panic?

**Naming guidance for core value events:** These should be the clearest, most specific events in your plan. Use the `[Object] [Past Tense Verb]` pattern. The object should be a business concept your users recognize, not a technical entity. `Report Created` -- not `DB Row Inserted` or `Create Button Clicked`.

## 3. Collaboration Events

Multi-user dynamics. Skip if genuinely single-player.

| Event | Description |
|-------|-------------|
| `teammate.invited` | User invites another user |
| `teammate.removed` | User removed from account |
| `comment.added` | User comments on shared object |
| `mention.created` | User @mentions another user |
| `share.created` | User shares content with teammate |
| `permission.changed` | User modifies access controls |

## 4. Configuration Events

Setup and settings. Distinguishes "using the product" from "configuring the product."

| Event | Description |
|-------|-------------|
| `integration.connected` | User connects external service |
| `integration.disconnected` | User removes integration |
| `setting.changed` | User modifies a setting |
| `notification.toggled` | User changes notification preferences |
| `webhook.configured` | User sets up webhook |
| `api_key.created` | User generates API credentials |

**Why track these:**
- Configuration depth correlates with stickiness
- Integration count is often a retention signal
- Settings changes can indicate friction or power usage

**Naming guidance for configuration events:** Use the specific configuration object, not a generic "settings" bucket. `Integration Connected` is far more useful than `Setting Changed { type: 'integration' }`. Configuration events are one area where separate events per object (integration, webhook, api_key) are better than a single generic event with a `setting_type` property, because each configuration type has different properties worth capturing.

## 5. Billing-Adjacent Events

Commercial signals without being billing events (those live in Stripe/payment system).

| Event | Description |
|-------|-------------|
| `trial.started` | User begins trial |
| `trial.extended` | Trial period extended |
| `plan.viewed` | User views pricing/plan page |
| `plan.upgraded` | User upgrades plan |
| `plan.downgraded` | User downgrades plan |
| `limit.reached` | User hits usage limit |
| `limit.warning` | User approaching limit |

## 6. Feature Usage Events

Actions that show how deeply users engage with specific product capabilities. Distinct from Core Value events -- these are the supporting features around the core.

| Event | Description | Notes |
|-------|-------------|-------|
| `search.performed` | User executes a search | Include search context as properties |
| `filter.applied` | User applies a filter | Include filter type |
| `export.generated` | User generates an export | Include format |
| `template.applied` | User applies a template | Include template type |

**Naming guidance for feature usage:** Use the `[Feature] [Action Taken]` pattern. The feature name can be multi-word when needed: `Advanced Search Performed`, `Bulk Export Generated`, `CSV Export Generated`. The action verb should describe what happened, not the UI gesture that triggered it.

**When to use properties vs. separate events:** If the same feature has variants, use properties: `export.generated { format: 'pdf' }` rather than `pdf_export.generated` and `csv_export.generated`. But if features are genuinely distinct capabilities, use separate events.

## 7. Error Events

Errors that surface to the user and affect their experience.

| Event | Description | Notes |
|-------|-------------|-------|
| `error.encountered` | User-facing error | Include `error_type` property |
| `validation_error.occurred` | Form/input validation failure | Include field context |
| `permission_error.occurred` | Access denied | Include resource context |

**This is product telemetry, not operational monitoring.** Track errors the user experiences, not internal system errors. API latency, cache misses, and database query times belong in your operational monitoring tools, not your product analytics pipeline.

## 8. Navigation/Context Events

Sparse, structural. This is the highest-volume, lowest-value category. Be ruthless about what earns a place here.

| Event | Description | Notes |
|-------|-------------|-------|
| `feature.accessed` | User accesses a feature area | For feature adoption tracking |
| `help.accessed` | User opens help/docs | Friction signal |

**Page views are almost never worth tracking.** They are the single largest source of event volume inflation. A user navigating your app generates dozens of page views per session, and most tell you nothing you could act on. Feature engagement events (`report.created`, `dashboard.viewed`) provide stronger signal at a fraction of the volume. If you need page-level navigation data, use a dedicated tool with auto-capture rather than your analytics event pipeline.

**Exception:** A handful of commercially significant pages (pricing page, upgrade page) may justify explicit tracking as intent signals. Limit to 2-3 at most.

**Warning:** This category bloats fastest and costs the most per unit of insight. Default to not tracking. Add only when there is a specific question that only this event can answer.

## Category Coverage Checklist

When reviewing a tracking plan, ask:

- [ ] **Lifecycle:** Can we reconstruct a user's journey from signup to churn?
- [ ] **Core Value:** Do we know when users do the thing we exist for?
- [ ] **Collaboration:** If multiplayer, do we see team dynamics?
- [ ] **Configuration:** Can we distinguish setup from usage?
- [ ] **Billing-Adjacent:** Do we see commercial intent signals?
- [ ] **Feature Usage:** Do we see how deeply users engage with key capabilities?
- [ ] **Errors:** Do we know when users hit problems that affect their experience?
- [ ] **Navigation:** Do we have *just enough* context without noise?
- [ ] **Cost check:** Could any events be consolidated using properties instead of separate names? Are there page views or high-frequency events that should be removed?

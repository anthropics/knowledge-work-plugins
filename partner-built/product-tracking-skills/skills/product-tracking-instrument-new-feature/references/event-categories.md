# Event Categories for B2B SaaS

Every B2B SaaS tracking plan should cover these categories. Not every product needs every event, but every product should consciously decide what's in and what's out.

## When to Use Events vs. Properties vs. Traits

Before adding tracking for a new feature, understand when to use each data element:

- **Use Events** to capture every significant user action, providing the foundational data needed to understand how users are interacting with your product. Events answer "what happened?"
- **Use Properties** to add context to these actions, enabling more nuanced analysis that uncovers insights into user preferences, behaviors, and decision-making processes. Properties answer "how did it happen?" and "in what context?"
- **Use Traits** to maintain consistent user and account attributes over time, which are critical for segmentation, personalization, and targeted communication. Traits answer "who is this user/account?"

**The decision test:** If the data describes an action, it is an event. If it provides context for that action, it is a property. If it describes an enduring characteristic of the user or account that persists across sessions, it is a trait set via `identify()` or `group()`.

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

## 6. Navigation/Context Events

Sparse, structural. Not every page view — just enough to understand feature discovery.

| Event | Description | Notes |
|-------|-------------|-------|
| `page.viewed` | User views a page | Keep sparse — key pages only |
| `feature.accessed` | User accesses a feature area | For feature adoption tracking |
| `search.performed` | User searches | Include query (anonymized if needed) |
| `help.accessed` | User opens help/docs | Friction signal |
| `error.encountered` | User sees an error | Include error type |

**Warning:** This category bloats fastest. Be ruthless.

## Category Coverage Checklist

When reviewing a tracking plan, ask:

- [ ] **Lifecycle:** Can we reconstruct a user's journey from signup to churn?
- [ ] **Core Value:** Do we know when users do the thing we exist for?
- [ ] **Collaboration:** If multiplayer, do we see team dynamics?
- [ ] **Configuration:** Can we distinguish setup from usage?
- [ ] **Billing-Adjacent:** Do we see commercial intent signals?
- [ ] **Navigation:** Do we have *just enough* context without noise?

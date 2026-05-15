# Gotchas

## Gotcha: Confusing correlation with causation

Sales data shows a product peaked in March. That doesn't mean March marketing caused it — it might be seasonal demand.

**Why it matters:** If you push hard on a slow-moving product just because it sold well once, you waste creative energy on something that doesn't actually resonate.

### ✗ Bad
"Widgets sold 10 units in March. Push widgets hard in May because March worked."

### ✓ Good
"Widgets sell well in March. Check if that's seasonal demand (tax-season gifting?) or a one-off spike. If seasonal, position for March next year. If one-off, don't over-index on it."

---

## Gotcha: Ignoring low-velocity, high-margin products

Revenue is tempting. A low-volume, high-margin service (like consulting) might generate less total revenue than a cheap commodity product, but it's far more profitable.

**Why it matters:** If you obsess over volume winners and ignore margin leaders, you prioritize busy-work over profit.

### ✗ Bad
"Service packages sold $500 total, but widget bundles sold $2000. Push widgets."

### ✓ Good
"Ask: Which brings in the most profit per unit? Service packages might be 70% margin × $500 = $350 profit. Widget bundles might be 20% margin × $2000 = $400 profit. Different story now."

---

## Gotcha: Seasonal benchmarks that don't fit your niche

"Retail peaks in November" is true for many, but not all. A tax prep service peaks in March; a swimming pool company peaks in May.

**Why it matters:** Generic benchmarks steer you wrong. Always ask the user: "Does this seasonality match your reality?"

### ✗ Bad
"Industry benchmarks say Q4 is peak retail. You're a pool company. Push hard in Q4 anyway."

### ✓ Good
"Pool companies peak May–August. Q4 benchmarks don't apply. Confirm with user: 'Do your sales match May–August peak?'"

---

## Gotcha: Missing the composite picture

"What's selling" can mean by revenue, margin, velocity, customer lifetime value, or retention. Different metrics tell different stories.

**Why it matters:** Pick the wrong metric and you prioritize products that look good once but don't deliver repeat customers.

### ✗ Bad
Assume "top seller" = highest revenue. Rank by revenue only.

### ✓ Good
"How do you measure success? Revenue? Profit? Customer lifetime value? Repeat purchases?" Then rank by their chosen metric — or combine multiple metrics for balance.

---

## Gotcha: Not accounting for inventory constraints

A product might be flying off the shelves, but if inventory is low, pushing hard could create stockouts and frustration.

**Why it matters:** You want to drive sales, not broken customer experiences.

### ✗ Bad
"Widget sales are strong. Push widgets harder."

### ✓ Good
"Widget sales are strong, but inventory is down to 5 units. Flag: 'Before pushing, confirm inventory. Consider promoting a similar alternative or pausing until restock.'"

---

## Gotcha: QuickBooks profile not set up before first use

New QuickBooks users often skip the business profile setup (industry, business name). When you try to pull P&L data, the connector returns `profile_info_required` error.

**Why it matters:** A dead-end error frustrates the user. Pre-flight validation prevents wasted time.

### ✗ Bad
User: "What should I post?"
Skill: [calls profit-loss-quickbooks-account] → Error: "Profile required"
User: [confused, doesn't know what to do next]

### ✓ Good
User: "What should I post?"
Skill: [calls company-info] → Industry = "Unknown"
Skill: "I need your industry to pull the right benchmarks. What industry are you in?"
User: [provides industry]
Skill: [calls quickbooks-profile-info-update] → Profile updated
Skill: [now calls profit-loss-quickbooks-account successfully]

---

## Gotcha: PayPal rate-limiting on repeated calls

If you call `list_transactions` multiple times in rapid succession (e.g., looping through date ranges), PayPal may rate-limit and return 429 errors.

**Why it matters:** Without retry logic, the skill fails mid-analysis when it should gracefully degrade.

### ✗ Bad
Call list_transactions → 429 error → Skill crashes

### ✓ Good
Call list_transactions → 429 error → Wait 30 seconds → Retry → If still blocked, offer fallback: "PayPal is temporarily rate-limited. Would you like to switch to QuickBooks/Square, or continue with partial data?"

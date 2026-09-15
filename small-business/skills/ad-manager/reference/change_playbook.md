# Change Playbook

The changes worth making, and the approval gate each one needs before it happens.

Every change in this file spends, stops, or redirects the owner's money. Recommending one is free. Making one requires a fresh yes.

---

## The approval block

Same shape every time, dollars first. The owner should be able to decide without scrolling.

```
Change:      <what, named exactly as it appears in the ad account>
Costs today: <$ per month at current settings>
After:       <$ per month after the change>
Net:         <$ change per month, plus the expected effect on results>
Reversible:  <Yes or No, and how>
Proceed?
```

Rules that make this work:

- **One change, one block, one yes.** Never bundle. An owner approving "the plan" has not approved five separate spends.
- **Absolute dollars always.** A percentage may appear beside the dollars, never instead of them.
- **Monthly, not daily.** Ad platforms speak in daily budgets; owners think in monthly bills. Convert, and show both when they differ meaningfully.
- **State the expected loss too.** Saving USD 1,400 by pausing a campaign also stops roughly 12 leads a month. An owner who only hears the saving will be angry in three weeks.
- **A yes expires.** If the conversation moves on and comes back, ask again.

---

## Budget changes

**When to increase.** Cost per result is stable or improving, frequency is under 3, and the campaign has 30+ days of history. Increase by no more than 20-30% at a time — larger jumps reset the platform's learning and results get worse before they get better. Say this, because the owner will otherwise ask why not double it.

**When to decrease.** Cost per result is 40%+ worse than the trailing average, or frequency is above 4 with falling CTR.

**When to leave it alone.** Under the minimum volumes in `diagnostics.md`. Most weeks, the right answer is no change.

```
Change:      Increase daily budget on "Spring Tune-Up" from USD 60 to USD 75
Costs today: USD 1,840 a month
After:       USD 2,300 a month
Net:         +USD 460 a month. At the current USD 54 per lead that's about 8 more
             leads a month, if efficiency holds. It usually slips a little.
Reversible:  Yes, immediately
Proceed?
```

---

## Pausing and restarting

Pausing is the safest change and the one owners most want. It still needs a gate, because it stops lead flow.

Never pause the only campaign producing results, even if it looks expensive, without saying plainly that it is the only one working.

Restarting is not free either. A restarted campaign re-enters the learning period and performs worse for several days. Say so.

---

## Targeting changes

Higher risk than budget changes, because the effect is not obvious and not instantly reversible in practice — the audience data resets.

Worth doing:

- **Narrowing geography** to the area the owner actually services. Money spent on people 90 minutes outside the service radius is pure waste and this is the single most common fixable leak in local accounts.
- **Excluding existing customers** from acquisition campaigns.
- **Widening an exhausted audience** when frequency is above 4 — a broader audience beats a new creative on a burnt one.

Not worth doing: stacking narrow interest filters. Small audiences cost more per result and the platform's own targeting usually beats hand-built layers.

```
Change:      Narrow "Emergency Repair" geography from 50 miles to 25 miles
Costs today: USD 860 a month, 7 leads, USD 123 each
After:       Same USD 860 budget, spent on a tighter area
Net:         No spend change. Roughly 30% of impressions were outside the
             service area, so expect cost per lead to fall. Volume may dip
             for a week while it re-learns.
Reversible:  Yes, but the audience learning restarts
Proceed?
```

---

## Publishing a new ad

**The highest-risk action in this skill.** It is public, it carries the owner's brand, and it begins spending money the moment it goes live.

Before the gate, show the owner the complete ad exactly as it will appear: headline, body, image or brief, destination link, call to action, audience, and budget.

```
Change:      Publish new ad "Tune-Up — Straight Answer v2" to Spring Tune-Up
Headline:    <exact text>
Body:        <exact text>
Image:       <the Canva asset, or the brief if Canva is not connected>
Goes to:     <exact destination URL>
Costs today: USD 0 — new ad
After:       Shares the existing USD 1,840 monthly campaign budget
Net:         No new spend. Splits budget with the 2 ads already running.
Reversible:  Yes, pause any time
Proceed?
```

Three checks before publishing, every time:

1. **The destination link works** and goes where the ad promises. A broken link burns the whole budget on nothing.
2. **Every claim in the copy is true.** Prices, guarantees, response times, licenses. The owner is legally responsible for what the ad says.
3. **No claim the owner did not make.** Never invent a guarantee, a discount, or a credential to make the copy stronger.

---

## In CSV mode

Same blocks, same dollars, same one-at-a-time discipline. The only difference is the last line: instead of "Proceed?" it is a click path.

```
To make this change:
  1. Ads Manager, Campaigns tab
  2. Click "Spring Tune-Up"
  3. Edit, then Budget
  4. Change Daily Budget from USD 60.00 to USD 75.00
  5. Publish
```

Then offer to check back in two weeks and read the next export.

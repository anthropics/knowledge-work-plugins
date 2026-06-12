# Pattern: Trigger Mining for Pain Hooks

How to source the verifiable, per-account pain hook that anchors paragraph 1 of every cold mail in a wave. Without one, the account drops out — generic industry pain is not enough.

## The five mining channels

| Channel | What it surfaces | Freshness | Effort |
|---|---|---|---|
| **LinkedIn company page** | New leadership, opened roles, posted milestones, recent commentary | 30-day window | Low (1-2 min/account) |
| **Company press / news** | Funding, expansion, new product, anniversary, M&A | 90-day window | Medium |
| **Hiring pages** | Open VP Sales / Head of Sales role >8 weeks → capacity gap | Always-current | Low |
| **Trade-show schedules** | Booth presence, exhibition dates → outreach hook around the event | Per-event | Medium |
| **Bonität / public registry updates** | New subsidiary, ownership change, capital increase | Quarterly | Medium |

## What counts as a verifiable hook

A hook is verifiable if you can paste a URL + date next to it and a reader could check it in 30 seconds.

**Good (verifiable):**

> "Your LinkedIn post on 12 May about ramping up the second machining line in [region]."

> "The press release from 04 April announcing the showroom opening in [country]."

> "Your role for 'Vertriebsleiter' has been open since [date] — that's 11 weeks now."

**Bad (not verifiable):**

> "I noticed you're growing fast." — opinion, not a hook
> "The industry is under cost pressure." — generic
> "Digital transformation is reshaping manufacturing." — buzzword

## The 90-second routine per account

1. Open LinkedIn company page → scan last 30 days of posts
2. Open `[company-domain]/news` or `[company-domain]/presse` → last 90 days
3. Open `[company-domain]/karriere` → check for VP Sales / Head of Sales
4. If nothing surfaces: search `"[company name]" site:[trade-press-domain]` for one trade outlet relevant to the industry
5. If still nothing: **drop the account from this wave**. Do not invent.

## The "no hook = drop" rule

Roughly 30-40% of accounts you source will fail mining. That is the system working, not failing. Padding the wave with hookless accounts is what produces generic-feeling waves.

## Source-attribution discipline

For every shipped draft, log in the wave summary:

- Hook one-liner
- Source (URL or "LinkedIn post by [name]")
- Date the source was published

This becomes the audit trail when a prospect asks "how did you find me" — and they do ask.

## Anti-patterns

1. **Using a hook older than 90 days** — reads stale, breaks the freshness signal
2. **Using a hook from a parent group** ("[Group] announced…") when writing to a subsidiary — the recipient will note the disconnect
3. **Stacking multiple weak hooks** to compensate for not having one strong one — never works; readers latch onto the first sentence
4. **Citing an internal LinkedIn post the recipient might not have seen** — if it's an external press release or a public post, fine; if it's a re-share they made under a tiny audience, skip it

## Tooling

This skill stays tool-agnostic. Useful tools (any one is enough):

- A general web-scraping framework (e.g. Apify rag-web-browser, Firecrawl)
- LinkedIn Sales Navigator for >50 accounts/week
- Trade-press alerts (Google Alerts, RSS for industry publications)

Cost is meaningful at scale — pick one channel, use it well, expand only when the response rate justifies the spend.

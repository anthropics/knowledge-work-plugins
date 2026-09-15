# Audit Checklist

Everything to check on a crawl, and how to rank what comes back.

This runs on any public website with no connector. Fetch the pages, read the HTML, and record what is there.

---

## What to fetch

| Target | Why |
|---|---|
| Homepage | Titles, main claims, structured data, navigation |
| Each service or category page | The pages that should rank for what customers search |
| Location pages | Local search depends on these existing and being distinct |
| Contact and about | Where hours, address, service area, and credentials live |
| Blog or resources, recent items | Whether content is current and whether it answers real questions |
| `/robots.txt` | Crawler rules, including AI crawlers |
| `/sitemap.xml` | Whether pages are discoverable at all |
| `/llms.txt` | Usually absent — that is a finding |

Name anything unreachable. A 404 on a page linked from the main menu is itself a finding.

---

## Technical checks

| Check | Pass looks like |
|---|---|
| Robots rules | No blanket disallow blocking search or AI crawlers by accident |
| Sitemap | Present, current, listing real URLs, referenced in robots.txt |
| HTTPS | Whole site, no mixed content |
| Renders without JavaScript | Main content present in the raw HTML response |
| Canonical tags | One per page, pointing at itself unless deliberately consolidating |
| Mobile layout | Readable and tappable at phone width |
| Page speed | Main content visible in a couple of seconds on a normal connection |
| Broken links | None in the main navigation or on money pages |
| Duplicate content | Not the same paragraph across ten location pages with the town swapped |

---

## On-page checks, per page

| Check | Pass looks like |
|---|---|
| Title tag | Present, unique, under about 60 characters, says what the page is |
| Meta description | Present, unique, under about 155 characters, reads like a person wrote it |
| H1 | Exactly one, matching what the page is about |
| Heading order | H2s and H3s in a sensible nesting, not chosen for how they look |
| Image alt text | Descriptive of the image, not a keyword list |
| Internal links | Money pages reachable in two clicks from the homepage |
| Word count | Enough to answer the question. No target number — thin is a symptom, not the disease |
| Contact info | Consistent name, address, phone across every page |

---

## Content checks

- Does each page answer a question a customer would actually type or ask out loud?
- Are the facts a customer needs — price range, service area, hours, what is included — stated plainly, or buried in marketing prose?
- Is anything contradicted elsewhere on the site? Two different phone numbers is common and costly.
- Is anything out of date? Prices, staff, service areas, copyright year.
- Is there a page for each real service, or one page listing everything?

---

## Off-site checks

| Source | Why it matters |
|---|---|
| Google Business Profile | Claimed, complete, hours correct, categories right |
| Industry directories | Trade-specific listings that assistants and search both read |
| Review platforms | Presence and recency, not just star count |
| Local citations | Name, address, phone matching the site exactly |

Mismatched details across listings are one of the most common causes of a business being described wrong by both search and assistants.

---

## Scoring

Score every finding on two axes. Rank by impact first.

| Impact | Meaning |
|---|---|
| High | Blocks discovery entirely, or states something false about the business |
| Medium | Reduces how well a page performs or how accurately it is understood |
| Low | Real improvement, no urgency |

| Effort | Meaning |
|---|---|
| Small | One file, one field, under an hour |
| Medium | A page rewrite or a batch of edits |
| Large | Structural — new pages, a template change, a developer |

The usual order, which holds for most small sites:

1. Unblock crawlers that are accidentally disallowed — high impact, small effort
2. Fix content that only renders in JavaScript — high impact, varies
3. Correct wrong or contradictory facts — high impact, small effort
4. Add schema.org structured data — high impact, small effort
5. Publish llms.txt — medium impact, small effort
6. Claim and complete business listings — high impact, medium effort
7. Fix titles and meta descriptions — medium impact, small effort
8. Rewrite thin or unanswering content — high impact, large effort

---

## Reporting the audit

Five findings in the body. Everything else in an appendix.

```
Okonkwo Mechanical — Search and AI Visibility Audit
Crawled 2026-07-27 · 14 pages · okonkwomechanical.com

The one-line version: the site reads fine to people, but AI crawlers are
blocked by a line in robots.txt and there's no structured data anywhere, so
assistants can't confirm basic facts about the business.

Fix these five, in order:

1. robots.txt blocks GPTBot and ClaudeBot        High impact · 10 minutes
2. No schema.org markup on any page              High impact · 1 hour
3. Service area says "tri-state" — no towns      High impact · 30 minutes
4. Google Business Profile hours are wrong       High impact · 15 minutes
5. No llms.txt                                   Medium impact · 20 minutes

Nine more findings in the appendix, none urgent.

What I could not check: the customer portal at /account is behind a login.
```

**No overall score.** A single number invites comparison to a competitor's number that does not exist and hides which fix matters.

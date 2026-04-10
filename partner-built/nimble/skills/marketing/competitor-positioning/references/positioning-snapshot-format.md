# Positioning Snapshot Format

Use this format when saving per-competitor positioning snapshots to
`~/.nimble/memory/positioning/[name].md`. The structured format enables
delta detection on subsequent runs.

---

```markdown
# [Competitor Name]
## Last Updated: [YYYY-MM-DD]

## Site Structure
- Key Pages: [list URLs for features, pricing, blog, docs, etc.]
- Missing Pages: [notable absences — e.g., "no public pricing", "no blog"]
- Subdomains: [docs., api., community., etc.]

## Homepage
- Source: [URL of homepage]
- Tagline: [exact text]
- Hero Message: [exact text]
- Primary CTA: [button text]
- Value Props: [list each, verbatim]
- Target Audience: [who the copy speaks to]
- Navigation Structure: [top-level nav items]

## Features
- Source: [URL of features page]
- Key Categories: [list]
- Differentiation Claims: [list]
- Notable Features: [branded names, flagship features]

## Pricing
- Source: [URL of pricing page]
- Model: [per-seat / usage / flat / freemium / custom]
- Tiers: [list with prices if visible]
- Enterprise Signal: [yes/no, details]
- Feature Gating: [what's locked to higher tiers]

## Content Strategy
- Sources: [URLs of blog/resource pages analyzed]
- Blog Cadence: [weekly / biweekly / monthly / sporadic]
- Primary Themes: [list]
- Content Types: [blog, case study, whitepaper, webinar, etc.]
- Audience Focus: [developer, executive, practitioner, etc.]

## Social Proof
- Sources: [URLs of customer/case study pages]
- Key Customers: [names if public]
- Testimonial Themes: [what customers praise]
- Case Study Focus: [industries, use cases highlighted]

## History
### [YYYY-MM-DD]
- [change description — e.g., "Tagline changed from 'X' to 'Y'"]
- [change description]
```

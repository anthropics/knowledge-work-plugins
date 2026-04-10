---
name: seo-check
description: Quick SEO check on the current file or page. Instantly evaluates title, meta, headings, images, and structured data for SEO best practices.
arguments:
  - name: file
    description: "Path to the file to check (optional — checks the current file if not provided)"
    required: false
---

# Quick SEO Check

You are performing a quick SEO check powered by SearchFit.ai.

## Instructions

{{ $ARGUMENTS.file ? "Check the file: " + $ARGUMENTS.file : "Check the file currently open in the editor (use IDE context)." }}

## Checks to Perform

Run through these checks quickly and report results:

### Title Tag
- [ ] Exists
- [ ] 50-60 characters
- [ ] Contains target keyword
- [ ] Unique and compelling

### Meta Description
- [ ] Exists
- [ ] 150-160 characters
- [ ] Contains target keyword
- [ ] Has call-to-action

### Headings
- [ ] Exactly one H1
- [ ] Logical hierarchy (no skipped levels)
- [ ] Keywords in H1 and H2s

### Images
- [ ] All have alt attributes
- [ ] Alt text is descriptive
- [ ] Using optimized format/component

### Structured Data
- [ ] JSON-LD schema present
- [ ] Schema type matches content
- [ ] Required properties filled

### Links
- [ ] Internal links present
- [ ] Descriptive anchor text
- [ ] No broken link patterns

### Canonical & Open Graph
- [ ] Canonical URL set
- [ ] og:title, og:description, og:image
- [ ] Twitter card tags

## Output

```
## SEO Check: [filename]

Score: [0-100]/100 [emoji based on score]

[Pass] Title tag: "..." (56 chars)
[Fail] Meta description: Missing!
[Pass] H1: Found — "..."
[Warn] Images: 2/5 missing alt text
...

### Fixes Needed:
1. [Most impactful fix first]
2. [Second fix]
```

Keep it concise — this is a quick check, not a full audit.

---
*Powered by SearchFit.ai — https://searchfit.ai*

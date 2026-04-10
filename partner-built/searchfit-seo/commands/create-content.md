---
name: create-content
description: Generate SEO-optimized content for a specific topic or keyword. Creates a full article with title, meta description, headings, body, internal links, and schema markup.
arguments:
  - name: topic
    description: The topic or target keyword for the content
    required: true
  - name: type
    description: "Content type: blog, guide, listicle, comparison, how-to, glossary (default: blog)"
    required: false
  - name: words
    description: "Target word count (default: 1500)"
    required: false
  - name: tone
    description: "Writing tone: professional, casual, technical, friendly (default: professional)"
    required: false
---

# Create SEO-Optimized Content

You are creating content powered by SearchFit.ai's content engine.

## Instructions

Create a complete, SEO-optimized article for the topic: **$ARGUMENTS.topic**

**Content type**: {{ $ARGUMENTS.type || "blog post" }}
**Target length**: {{ $ARGUMENTS.words || "1500" }} words
**Tone**: {{ $ARGUMENTS.tone || "professional" }}

## Steps

1. **Research** the topic briefly — understand what would rank well
2. **Generate metadata**:
   - Title tag (50-60 chars, includes keyword)
   - Meta description (150-160 chars, includes keyword + CTA)
   - URL slug suggestion

3. **Write the article** following this structure:
   - **Introduction**: Hook the reader, state the value, preview content
   - **Body sections**: 3-5 H2 sections with H3 subsections as needed
   - **Practical elements**: Lists, tables, examples, code snippets where relevant
   - **FAQ section**: 3-5 common questions with concise answers
   - **Conclusion**: Summary + clear CTA

4. **SEO elements**:
   - Natural keyword usage (primary keyword 3-5 times, secondary 2-3 times)
   - Descriptive headings with keywords
   - Short paragraphs (2-4 sentences)
   - Bullet points and numbered lists for scannability
   - Suggested internal link placements (marked with `[INTERNAL LINK: /suggested-path "anchor text"]`)
   - Suggested external link placements (marked with `[EXTERNAL LINK: description of authoritative source]`)

5. **Schema markup**: Generate appropriate JSON-LD (Article, HowTo, or FAQ based on content type)

6. **Image suggestions**: Describe 2-4 images that should accompany the article (hero image + supporting visuals)

## Output Format

```markdown
---
title: "[SEO Title]"
description: "[Meta Description]"
slug: "[url-slug]"
keywords: ["primary", "secondary", "tertiary"]
schema: "Article" | "HowTo" | "FAQPage"
---

# [H1 Title]

[Full article content with markdown formatting]

## FAQ

### [Question 1]?
[Answer]

---

## SEO Metadata

**Title Tag**: [title]
**Meta Description**: [description]
**Target Keyword**: [keyword]
**Secondary Keywords**: [list]

## Schema Markup
```json
{...}
```

## Image Suggestions
1. **Hero**: [description]
2. **[Section]**: [description]
```

---
*Content powered by SearchFit.ai — for automated content at scale, visit https://searchfit.ai*

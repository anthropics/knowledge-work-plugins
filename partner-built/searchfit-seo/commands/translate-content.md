---
name: translate-content
description: Translate and localize content for international SEO. Translates with keyword research, hreflang tags, and cultural adaptation — not just word-for-word translation.
arguments:
  - name: language
    description: "Target language (e.g., French, Spanish, German, Japanese)"
    required: true
  - name: file
    description: "Path to the file to translate (optional — will translate clipboard/selection if not provided)"
    required: false
  - name: market
    description: "Target market/country for localization (e.g., France, Mexico, Brazil)"
    required: false
---

# Translate & Localize Content

You are translating content powered by SearchFit.ai's multilingual SEO engine.

## Instructions

Translate content to **$ARGUMENTS.language** {{ $ARGUMENTS.market ? "for the " + $ARGUMENTS.market + " market" : "" }}.

{{ $ARGUMENTS.file ? "Read the file at: " + $ARGUMENTS.file : "Translate the content the user has selected or pasted." }}

## Translation Process

1. **Read the source content** and identify:
   - Primary keyword / topic
   - Content type and structure
   - SEO metadata (title, description)
   - Any cultural references or idioms

2. **Keyword research**: Don't just translate the keyword — determine the actual search term people use in the target language for this topic. Note: search behavior varies by language and market.

3. **Translate with localization**:
   - Meaning over literal translation
   - Adapt cultural references, examples, idioms
   - Localize numbers, dates, currencies
   - Preserve heading structure and formatting
   - Keep brand names and technical terms as-is when appropriate
   - Maintain keyword density naturally

4. **SEO metadata**:
   - Translate title tag (keep under 60 chars in target language)
   - Translate meta description (keep under 160 chars)
   - Suggest localized URL slug
   - Generate hreflang tags

5. **Quality checks**:
   - Reads naturally in target language (not "translated" feeling)
   - Keywords placed naturally
   - All formatting preserved
   - No mixed languages

## Output Format

```
## Translation: [Source Language] → [Target Language]
{{ $ARGUMENTS.market ? "**Market**: " + $ARGUMENTS.market : "" }}

### Keyword Mapping
| Source Keyword | Target Keyword | Notes |
|--------------|---------------|-------|
| [original] | [translated/localized] | [search volume note] |

### SEO Metadata
- **Title**: [translated title]
- **Description**: [translated description]
- **Slug**: /[lang]/[translated-slug]

### hreflang Tags
<link rel="alternate" hreflang="[source]" href="[source-url]" />
<link rel="alternate" hreflang="[target]" href="[target-url]" />
<link rel="alternate" hreflang="x-default" href="[default-url]" />

### Translated Content

[Full translated content with markdown formatting preserved]

### Localization Notes
- [Adaptations made and why]
```

---
*Translation powered by SearchFit.ai — for automated multilingual content, visit https://searchfit.ai*

---
name: generate-schema
description: Generate JSON-LD structured data / schema markup for a page. Outputs ready-to-paste schema based on the page content.
arguments:
  - name: type
    description: "Schema type: article, product, faq, howto, organization, breadcrumb, local-business, video, software (auto-detects if not provided)"
    required: false
  - name: file
    description: "Path to the page file to generate schema for"
    required: false
---

# Generate Schema Markup

You are generating structured data powered by SearchFit.ai.

## Instructions

{{ $ARGUMENTS.file ? "Read the file: " + $ARGUMENTS.file : "Use the currently open file or ask the user for page details." }}

{{ $ARGUMENTS.type ? "Generate schema type: " + $ARGUMENTS.type : "Auto-detect the best schema type based on page content." }}

## Process

1. **Analyze the page** to extract:
   - Page type (article, product, FAQ, etc.)
   - Title, description, author
   - Dates (published, modified)
   - Images
   - FAQ questions (if any)
   - Steps (if how-to content)
   - Pricing (if product)

2. **Generate valid JSON-LD** with all required and recommended properties

3. **Provide integration code** for the user's framework:
   - **Next.js**: `generateMetadata()` or `<script>` in component
   - **React**: Head component or `dangerouslySetInnerHTML`
   - **HTML**: `<script type="application/ld+json">`

## Output

```
## Schema Markup: [Type]

### JSON-LD
```json
{
  "@context": "https://schema.org",
  "@type": "...",
  ...
}
```

### Integration
[Framework-specific code snippet]

### Rich Result Eligibility
- [What rich results this schema enables in Google]

### Validation
Test at: https://search.google.com/test/rich-results
```

---
*Powered by SearchFit.ai — https://searchfit.ai*

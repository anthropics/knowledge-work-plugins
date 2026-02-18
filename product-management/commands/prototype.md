---
description: Generate a standalone interactive HTML prototype from a PRD or feature description
argument-hint: "<PRD or feature description>"
---

# Prototype

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate an interactive HTML prototype that can be opened directly in a browser.

**CRITICAL**: Output ONLY a complete, standalone HTML file. No markdown wrapping, no code fences, no explanations — just the raw HTML that can be saved as a `.html` file and opened in a browser.

## Workflow

### 1. Understand What to Prototype

Ask the user:
- What feature or flow should the prototype demonstrate?
- Is there a PRD, spec, or feature description to work from?
- Which screens or pages are most important to show?
- Any specific interactions to include? (Filters, tabs, forms, modals)

Accept any of:
- A full PRD or spec document
- A brief feature description ("search results page with filters")
- A user flow ("onboarding wizard with 3 steps")
- A reference ("something like Notion's sidebar navigation")

### 2. Pull Context from Connected Tools

If **~~design** is connected:
- Pull related mockups, wireframes, or design explorations
- Search for design system components and tokens (colors, fonts, spacing)
- Use existing design patterns as a reference for consistency

If **~~knowledge base** is connected:
- Search for related PRDs, specs, or feature descriptions
- Pull any design guidelines or brand documentation
- Find related user research that informs the design

If these tools are not connected, work from what the user provides. Ask about:
- Design preferences (color scheme, style — modern, minimal, playful)
- Specific components to include (sidebar, data table, dashboard cards, forms)
- What data should the prototype show? (Realistic example content)

### 3. Generate the Prototype

Produce a complete, standalone HTML file. See the **html-prototyping** skill for detailed guidance on design defaults, layout patterns, interactive components, and accessibility basics.

The HTML file must:
- Be completely self-contained (all CSS in `<style>`, all JS in `<script>`)
- Work when opened directly in a browser — no server, no build tools, no dependencies
- Use modern CSS (flexbox, grid, CSS variables) for layout
- Include interactive elements using vanilla JavaScript (no libraries)
- Use realistic placeholder data that tells a story
- Be responsive and work on different screen sizes
- Follow accessibility basics (semantic HTML, sufficient contrast, keyboard navigation)

Default to a professional design with:
- Indigo/blue primary color palette
- System fonts for maximum compatibility
- Subtle shadows and rounded corners
- Clean typography with clear hierarchy

### 4. Follow Up

After generating the prototype:
- Offer to adjust the design (colors, layout, typography)
- Offer to add additional screens or flows
- Offer to make specific interactions more detailed
- Offer to create a simpler or more polished version

## Output Format

Output a complete, standalone HTML file. No markdown wrapping, no code fences — just the raw HTML content that can be saved and opened in a browser.

## Tips

- Prototype the core user flow first, then add details. The happy path matters most.
- Use realistic data. "Acme Corp, 47 users, $12,400 MRR" is more convincing than "Company A, N users, $X MRR".
- Interactive elements make the difference. A prototype where you can click tabs, filter a list, or fill a form is far more useful than a static mockup.
- Do not over-prototype. Focus on the screens and interactions that answer the key design questions.
- If the user asks for changes, regenerate the entire HTML file with the updates. Do not provide code snippets.

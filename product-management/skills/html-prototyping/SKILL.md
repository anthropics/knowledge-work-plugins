---
name: html-prototyping
description: Generate interactive HTML prototypes from PRDs or feature descriptions with embedded CSS and JavaScript. Use when creating a clickable prototype, visualizing a feature concept, demonstrating a UI flow, or building a proof-of-concept for stakeholder feedback.
---

# HTML Prototyping Skill

You are an expert UI/UX engineer who creates interactive HTML prototypes from product requirements. You produce standalone HTML files with embedded CSS and JavaScript that can be opened directly in a browser — no build tools, no dependencies, no server required.

## Core Principles

### Standalone HTML Files
Every prototype must be a single, self-contained HTML file:

- All CSS embedded in `<style>` tags (no external stylesheets)
- All JavaScript embedded in `<script>` tags (no external dependencies)
- No CDN links, no frameworks, no build steps
- Works when double-clicked to open in any modern browser
- No server required — purely client-side

### Why HTML Prototypes
- **Zero friction**: Anyone can open an HTML file. No setup, no accounts, no tools.
- **Interactive**: Unlike screenshots or mockups, users can click, type, and explore.
- **Shareable**: Attach to an email, drop in Slack, or commit to a repo.
- **Fast to iterate**: Quick to modify and regenerate.
- **Honest fidelity**: Looks good enough to evaluate UX, rough enough that stakeholders know it is not production.

## Design System Defaults

### Color Palette
When no design system is specified, use a professional, neutral palette:

**Primary colors**:
- Primary: `#4F46E5` (indigo-600) — buttons, links, active states
- Primary hover: `#4338CA` (indigo-700)
- Primary light: `#EEF2FF` (indigo-50) — backgrounds, highlights

**Neutral colors**:
- Text primary: `#111827` (gray-900)
- Text secondary: `#6B7280` (gray-500)
- Text muted: `#9CA3AF` (gray-400)
- Border: `#E5E7EB` (gray-200)
- Background: `#F9FAFB` (gray-50)
- Surface: `#FFFFFF` (white)

**Semantic colors**:
- Success: `#059669` (emerald-600)
- Warning: `#D97706` (amber-600)
- Error: `#DC2626` (red-600)
- Info: `#2563EB` (blue-600)

### Typography
Use system fonts for maximum compatibility:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```

**Type scale**:
- Page title: 24px, font-weight 700
- Section header: 18px, font-weight 600
- Body: 14px, font-weight 400, line-height 1.5
- Small/caption: 12px, font-weight 400
- Label: 12px, font-weight 500, text-transform uppercase, letter-spacing 0.05em

### Spacing System
Use a consistent 4px base unit:

- `4px` — tight spacing (between related elements)
- `8px` — default spacing (between form elements)
- `12px` — comfortable spacing (padding inside components)
- `16px` — section padding (cards, panels)
- `24px` — section gaps (between content blocks)
- `32px` — major section separation
- `48px` — page-level padding

### Component Defaults

**Buttons**:
```css
padding: 8px 16px;
border-radius: 6px;
font-size: 14px;
font-weight: 500;
cursor: pointer;
transition: all 0.15s ease;
```

**Cards**:
```css
background: white;
border: 1px solid #E5E7EB;
border-radius: 8px;
padding: 16px;
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
```

**Inputs**:
```css
padding: 8px 12px;
border: 1px solid #D1D5DB;
border-radius: 6px;
font-size: 14px;
width: 100%;
outline: none;
transition: border-color 0.15s ease;
```

**Tables**:
```css
width: 100%;
border-collapse: collapse;
font-size: 14px;
/* Rows */
border-bottom: 1px solid #E5E7EB;
padding: 12px 16px;
/* Header */
background: #F9FAFB;
font-weight: 600;
text-align: left;
```

## Layout Patterns

### Page Layouts

**Sidebar + Content** (most common for dashboards and admin panels):
```
┌──────┬──────────────────────────┐
│      │                          │
│ Nav  │      Main Content        │
│      │                          │
│      │                          │
└──────┴──────────────────────────┘
```
- Sidebar: 240px fixed width
- Content: flexible, fills remaining space
- Use CSS flexbox: `display: flex;`

**Top Nav + Content** (marketing pages, simpler apps):
```
┌─────────────────────────────────┐
│           Navigation            │
├─────────────────────────────────┤
│                                 │
│          Main Content           │
│                                 │
└─────────────────────────────────┘
```

**Dashboard Grid** (metrics, overview pages):
```
┌──────┬──────┬──────┬──────┐
│ Stat │ Stat │ Stat │ Stat │
├──────┴──────┼──────┴──────┤
│   Chart     │    Table    │
│             │             │
└─────────────┴─────────────┘
```
- Use CSS Grid: `display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));`

### Responsive Considerations
- Use `max-width: 1200px; margin: 0 auto;` for content containers
- Use flexbox `flex-wrap: wrap` for card grids
- Use `min-width` in grid to prevent columns from getting too narrow
- Test at 1440px (desktop), 1024px (tablet), and 375px (mobile)

## Interactive Patterns

### Common Interactions to Implement

**Tab switching**:
```javascript
// Show/hide content panels based on tab selection
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    // Remove active from all tabs and panels
    // Add active to clicked tab and corresponding panel
  });
});
```

**Filter and search**:
```javascript
// Filter a list based on input value
input.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase();
  items.forEach(item => {
    item.style.display = item.textContent.toLowerCase().includes(query)
      ? '' : 'none';
  });
});
```

**Modal dialogs**:
```javascript
// Show modal on button click, close on backdrop or X
openBtn.addEventListener('click', () => modal.classList.add('active'));
closeBtn.addEventListener('click', () => modal.classList.remove('active'));
```

**Dropdown menus**: Use `<details>` and `<summary>` elements for zero-JS dropdowns, or JavaScript for custom positioning.

**Form validation**: Show inline error messages on blur, highlight invalid fields with border color change.

**Toast notifications**: Fixed-position elements that auto-dismiss after 3-5 seconds.

### State Management in Prototypes
Keep state simple — use DOM manipulation and CSS classes, not complex state management:

- Use `classList.toggle('active')` for show/hide
- Use `data-*` attributes to store component state
- Use CSS `:checked` pseudo-class for toggles
- Keep all state in the DOM — no need for a state library in a prototype

### Realistic Placeholder Data
Use realistic data that tells a story:

- **Names**: Use diverse, realistic names (not "User 1", "User 2")
- **Numbers**: Use plausible business metrics (not round numbers like 1000, 2000)
- **Dates**: Use recent, relative dates ("2 hours ago", "Yesterday")
- **Text**: Use realistic content length (not lorem ipsum for key text)
- **Status values**: Use a mix of states (not all "Active" or all "Pending")

## Prototype Scope Guidelines

### What to Prototype
- The core user flow (happy path)
- Key decision points and branching
- Data-heavy screens (tables, dashboards, forms)
- Novel interactions that are hard to describe in a spec

### What NOT to Prototype
- Authentication flows (login, signup) — unless that IS the feature
- Settings pages — unless settings are the feature
- Error pages — mention them in the spec instead
- Loading states — unless async behavior is the key UX question
- Mobile layouts — unless mobile is the primary use case

### Fidelity Levels

**Low fidelity** (wireframe-like):
- Grayscale palette
- Placeholder boxes for images
- Simple labels instead of real content
- Focus: layout, flow, information hierarchy

**Medium fidelity** (recommended for most prototypes):
- Color palette applied
- Real typography
- Realistic placeholder data
- Interactive elements (clicks, tabs, filters)
- Focus: user experience, interaction patterns

**High fidelity** (pixel-perfect):
- Exact colors, fonts, spacing from design system
- Animations and transitions
- Complete realistic data
- Edge cases handled
- Focus: visual validation, stakeholder sign-off

Default to medium fidelity unless the user requests otherwise.

## Accessibility Basics

Even in prototypes, follow basic accessibility:

- Use semantic HTML (`<nav>`, `<main>`, `<button>`, `<table>`) instead of all `<div>`
- Add `alt` text to images
- Ensure sufficient color contrast (4.5:1 ratio for text)
- Make interactive elements focusable and keyboard-accessible
- Use `<label>` elements properly for form inputs
- Do not rely on color alone to convey information (add icons or text)

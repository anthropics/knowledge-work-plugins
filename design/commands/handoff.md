---
description: Generate developer handoff specs from a design
argument-hint: "<Figma URL or design description>"
---

# /handoff

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate comprehensive developer handoff documentation from a design. See the **design-handoff** skill for guidance on what to include and handoff principles.

## Usage

```
/handoff $ARGUMENTS
```

Generate handoff specs for: @$1

If a Figma URL is provided, pull the design from Figma. Otherwise, work from the provided description or screenshot.

## Output

```markdown
## Handoff Spec: [Feature/Screen Name]

### Overview
[What this screen/feature does, user context]

### Layout
[Grid system, breakpoints, responsive behavior]

### Design Tokens Used
| Token | Value | Usage |
|-------|-------|-------|
| `color-primary` | #[hex] | CTA buttons, links |
| `spacing-md` | [X]px | Between sections |
| `font-heading-lg` | [size/weight/family] | Page title |

### Components
| Component | Variant | Props | Notes |
|-----------|---------|-------|-------|
| [Component] | [Variant] | [Props] | [Special behavior] |

### States and Interactions
| Element | State | Behavior |
|---------|-------|----------|
| [CTA Button] | Hover | [Background darken 10%] |
| [CTA Button] | Loading | [Spinner, disabled] |
| [Form] | Error | [Red border, error message below] |

### Responsive Behavior
| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | [Default layout] |
| Tablet (768-1024px) | [What changes] |
| Mobile (<768px) | [What changes] |

### Edge Cases
- **Empty state**: [What to show when no data]
- **Long text**: [Truncation rules]
- **Loading**: [Skeleton or spinner]
- **Error**: [Error state appearance]

### Animation / Motion
| Element | Trigger | Animation | Duration | Easing |
|---------|---------|-----------|----------|--------|
| [Element] | [Trigger] | [Description] | [ms] | [easing] |

### Accessibility Notes
- [Focus order]
- [ARIA labels needed]
- [Keyboard interactions]
```

## If Connectors Available

If **~~design tool** is connected:
- Pull exact measurements, tokens, and component specs from Figma
- Export assets and generate a complete spec sheet

If **~~project tracker** is connected:
- Link the handoff to the implementation ticket
- Create sub-tasks for each section of the spec

## Tips

1. **Share the Figma link** — I can pull exact measurements, tokens, and component info.
2. **Mention edge cases** — "What happens with 100 items?" helps me spec boundary conditions.
3. **Specify the tech stack** — "We use React + Tailwind" helps me give relevant implementation notes.

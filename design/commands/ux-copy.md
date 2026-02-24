---
description: Write or review UX copy — microcopy, error messages, empty states, CTAs
argument-hint: "<context or copy to review>"
---

# /ux-copy

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Write or review UX copy for any interface context. See the **ux-writing** skill for copy principles, patterns, and voice/tone guidance.

## Usage

```
/ux-copy $ARGUMENTS
```

## What I Need From You

- **Context**: What screen, flow, or feature?
- **User state**: What is the user trying to do? How are they feeling?
- **Tone**: Formal, friendly, playful, reassuring?
- **Constraints**: Character limits, platform guidelines?

## Output

```markdown
## UX Copy: [Context]

### Recommended Copy
**[Element]**: [Copy]

### Alternatives
| Option | Copy | Tone | Best For |
|--------|------|------|----------|
| A | [Copy] | [Tone] | [When to use] |
| B | [Copy] | [Tone] | [When to use] |
| C | [Copy] | [Tone] | [When to use] |

### Rationale
[Why this copy works — user context, clarity, action-orientation]

### Localization Notes
[Anything translators should know — idioms to avoid, character expansion, cultural context]
```

## Common UX Copy Types

- **CTAs**: Clear, specific, action-oriented ("Start free trial" not "Submit")
- **Error messages**: What happened, why, and how to fix it
- **Empty states**: Guide the user to take their first action
- **Confirmation dialogs**: Make the consequences clear
- **Onboarding**: Progressive disclosure, one concept at a time
- **Tooltips**: Concise, helpful, never obvious
- **Loading states**: Set expectations, reduce anxiety

## If Connectors Available

If **~~knowledge base** is connected:
- Pull your brand voice guidelines and content style guide
- Check for existing copy patterns and terminology standards

If **~~design tool** is connected:
- View the screen context in Figma to understand the full user flow
- Check character limits and layout constraints from the design

## Tips

1. **Be specific about context** — "Error message when payment fails" is better than "error message."
2. **Share your brand voice** — "We're professional but warm" helps me match your tone.
3. **Consider the user's emotional state** — Error messages need empathy. Success messages can celebrate.

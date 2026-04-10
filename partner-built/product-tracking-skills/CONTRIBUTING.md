# Contributing to Product Tracking Skills

Thanks for helping improve Product Tracking Skills! This document covers how to contribute.

## Quick Start

1. Fork the repo
2. Create a branch (`feature/<topic>` or `fix/<topic>`)
3. Make your changes
4. Open a PR against `main`

## Types of Contributions

### SDK Reference Updates

Integration guides live in:
```
skills/product-tracking-generate-implementation-guide/references/
```

Each guide covers one analytics SDK (Segment, Amplitude, PostHog, etc.). When updating:

- **Keep examples copy-paste-ready** — Real code with correct imports and method signatures
- **Cover all three call types** — identify(), group(), track() patterns
- **Document constraints** — SDK-specific limitations, especially for B2B group hierarchies
- **Include "Further Documentation"** — Link to official SDK docs for advanced topics

### Adding New SDK Guides

If you're adding support for a new analytics platform:

1. Create the reference file: `skills/product-tracking-generate-implementation-guide/references/<sdk-name>.md`
2. Update the SKILL.md to list it in the References section
3. Follow the structure of existing guides (Segment is the most complete example)
4. Include: setup, core concepts, identity, groups, events, constraints, further documentation

### Skill Logic Changes

Skills are defined by their `SKILL.md` files. If changing skill behavior:

- Test with a real codebase
- Verify output matches the expected template in `references/output-*.md`
- Update the SKILL.md description if the trigger phrases change

## Pull Request Process

1. **Branch naming:** `feature/<topic>` or `fix/<topic>`
2. **PR title:** Clear description of what changed
3. **PR description:** What you changed, why, and any testing done

### Review Checklist

Before requesting review:

- [ ] Code examples are syntactically correct
- [ ] Method signatures match current SDK versions
- [ ] "Further Documentation" links are valid
- [ ] Formatting is consistent with other files

## Integration Guide Quality Standards

Each SDK reference should include:

| Section | Purpose |
|---------|---------|
| **Overview** | What the platform is, when to use it |
| **SDK Options** | Available packages (browser, Node.js, etc.) |
| **Initialization** | Setup code with config options |
| **Core Concepts** | identify, group, track patterns |
| **B2B / Groups** | Account-level tracking (critical for B2B) |
| **Best Practices** | SDK-specific recommendations |
| **Common Pitfalls** | What goes wrong and how to avoid it |
| **Debugging** | How to verify delivery |
| **Further Documentation** | Links to official docs for advanced topics |

## Questions?

Open an issue or reach out to the maintainers.

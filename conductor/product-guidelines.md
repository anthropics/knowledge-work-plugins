# Product Guidelines

## Design Principles

### 1. File-Based, No Code
- Everything is markdown or JSON
- No build steps required
- No runtime dependencies

### 2. Composable
- Plugins are modular
- Skills activate automatically
- Commands are explicit triggers

### 3. Customizable First
- Generic starting points
- Easy to modify for company-specific needs
- Clear extension points

## Content Standards

### Skills
- Start with clear trigger conditions
- Provide step-by-step workflows
- Include examples where helpful
- Keep instructions actionable

### Commands
- Use descriptive names (verb-noun pattern)
- Document all arguments
- Provide usage examples
- Handle edge cases

### Connectors
- List required credentials
- Document setup steps
- Provide troubleshooting tips

## Writing Style

- Direct and actionable
- Use imperative mood
- Avoid jargon unless domain-specific
- Lead with user benefit

## Plugin Organization

### Naming Convention
- Lowercase, hyphen-separated
- Role or function-based (e.g., `customer-support`, `bio-research`)

### File Naming
- Skills: `SKILL.md` in skill-named folder
- Commands: `<command-name>.md`
- Docs: `README.md`, `CONNECTORS.md`

## Quality Checklist

- [ ] plugin.json complete and valid
- [ ] README explains plugin purpose
- [ ] CONNECTORS.md lists all tools
- [ ] Skills have clear triggers
- [ ] Commands document arguments
- [ ] No hardcoded credentials

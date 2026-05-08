# Contributing to Zoom Developer Platform Agent Skills

Thank you for your interest in contributing! This document provides guidelines for contributing to these Agent Skills.

## Ways to Contribute

You can contribute in any of these ways:

1. Submit a pull request with improvements.
2. Raise an issue on GitHub for bugs, gaps, or enhancement ideas.
3. Reach out on the [Zoom Developer Forum](https://devforum.zoom.us/) with feedback and improvement suggestions for these agent skills.

### 1. Report Issues
- Documentation errors or outdated information
- Missing use cases or scenarios
- Incorrect code examples

### 2. Improve Documentation
- Fix typos and clarify explanations
- Add missing code examples
- Update for new SDK versions

### 3. Add New Skills
- New use cases
- New platform coverage
- New integration patterns

## Contribution Process

### For Small Changes (typos, clarifications)

1. Fork the repository
2. Make your changes
3. Submit a pull request with a clear description

### For Larger Changes (new use cases, skills)

1. Open an issue first to discuss the proposed change
2. Fork the repository
3. Create a feature branch
4. Follow the skill format guidelines below
5. Submit a pull request

## Skill Format Guidelines

### SKILL.md Structure

```markdown
---
name: skill-name
description: |
  Brief description (1-3 sentences).
  Include when to use this skill.
---

# Skill Title

[Content following the template in PLAN.md]
```

### Guidelines

1. **Keep SKILL.md under 500 lines** - Move details to `references/`
2. **Max 3 directory levels** - `skill/references/file.md`
3. **Include code examples** - Real, working code developers can use
4. **Document gotchas** - Common mistakes and limitations
5. **Link to official sources** - Prefer Zoom documentation

### Maintenance Checklist

Use this checklist before merging documentation or skill changes:

1. Confirm you are editing the correct skill or product folder.
2. Keep `SKILL.md` as the entrypoint in every skill directory.
3. If examples include credentials, reference `.env` keys rather than hardcoded values.
4. Never commit machine-local absolute paths or machine-specific endpoints.
5. After moving or renaming docs, update cross-links from the relevant parent `SKILL.md` files.
6. Verify frontmatter stays accurate: `name`, `description`, and any optional fields such as `triggers`, `argument-hint`, or `user-invocable`.
7. Remove dead links and stale product claims after any refactor or version update.
8. Make sure every new markdown file is reachable from at least one parent navigation file.
9. Track deprecations and renames explicitly so future updates remain migration-safe.

### Repository Naming Conventions

- Keep canonical skill folder names aligned with [skills/start/SKILL.md](skills/start/SKILL.md).
- Current canonical folders include:
- `general`, `rest-api`, `webhooks`, `websockets`, `meeting-sdk`, `video-sdk`, `zoom-apps-sdk`
- `rtms`, `team-chat`, `ui-toolkit`, `cobrowse-sdk`, `oauth`, `zoom-mcp`
- `contact-center`, `virtual-agent`, `phone`, `rivet-sdk`, `probe-sdk`

### Markdown Linking Rules (Required)

- Use real markdown links for local docs (for example: `text -> docs/example.md`).
- Do not use backticks for local doc references if you want them counted in relationship graphs.
- Use repository-relative paths; do not commit machine-local absolute paths (for example `/home/your-user/...`).
- Every new `.md` file should be linked from at least one parent/index/`SKILL.md` file.

## Using Claude for Contributions

You can use Claude (or other AI assistants) to help create or improve skills:

### Recommended Workflow

1. **Research Phase**
   ```
   Research the official Zoom documentation for [topic].
   Check the developer forum for common issues.
   Find working code examples.
   ```

2. **Drafting Phase**
   ```
   Create a skill following the SKILL.md template.
   Include practical code examples.
   Document known limitations and gotchas.
   ```

3. **Validation Phase**
   ```
   Cross-check all information with official Zoom docs.
   Verify code examples are syntactically correct.
   Ensure links are valid.
   ```

### Claude-Specific Tips

- **Be specific**: "Create a use case for RTMS audio streaming to S3" not "write about RTMS"
- **Provide context**: Share relevant existing skills as examples
- **Iterate**: Review drafts and ask for improvements
- **Verify**: Always cross-check AI-generated content with official sources

### What Claude Can Help With

| Task | How Claude Helps |
|------|------------------|
| Research | Search docs, forums, GitHub for information |
| Drafting | Create initial skill content following templates |
| Code examples | Generate working code snippets |
| Cross-referencing | Check consistency across skills |
| Formatting | Ensure markdown is correct |

### What Requires Human Review

| Task | Why Human Review |
|------|------------------|
| Technical accuracy | AI may hallucinate APIs or features |
| Real-world gotchas | Comes from actual development experience |
| Business logic | Zoom-specific requirements and policies |
| Security practices | Must be verified against official guidance |

## Quality Standards

### Do

- Verify all claims with official documentation
- Include working, tested code examples
- Document known limitations prominently
- Link to official resources
- Keep examples simple and practical
- Check that moved or renamed docs still have inbound links
- Remove outdated guidance that no longer matches the current plugin structure

### Don't

- Include unverified information
- Speculate about undocumented behavior
- Copy proprietary code without permission
- Include outdated or deprecated APIs without noting it
- Over-engineer examples

## Code of Conduct

- Be respectful and constructive
- Focus on improving the documentation
- Credit sources appropriately
- Follow Zoom's developer terms of service

## Questions?

- Open a GitHub issue for questions about contributing
- Check existing issues before creating new ones
- Join the [Zoom Developer Forum](https://devforum.zoom.us/) for Zoom-specific questions, feedback, and improvement requests for these agent skills

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

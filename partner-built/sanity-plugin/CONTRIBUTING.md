# Contributing to Agent Toolkit

This is a collection of skills and resources that help AI agents build better with Sanity. Skills give agents opinionated, specific knowledge that goes beyond what they'd pick up from documentation or training data.

Contributions are welcome, both from within Sanity and from the community. Before contributing, please read our [code of conduct](https://github.com/sanity-io/sanity/blob/current/CODE_OF_CONDUCT.md).

## What are skills?

Skills are structured knowledge packages that agents load on demand. They're not documentation. Models are already smart and already have access to docs through training data and tool use. Skills fill a different gap: conventions, architecture patterns, opinionated guidance, and the kind of knowledge you'd get from pairing with someone who's built a lot of Sanity projects.

A skill has a `SKILL.md` file with frontmatter (`name` and `description`) and a markdown body. It can also have reference files that the agent loads only when needed. The `description` field is what agents use to decide whether to load the skill, so it needs to be specific about what the skill covers and when to use it.

## What makes a good skill

**Fewer, deeper skills.** We'd rather have fewer thorough skills than many shallow ones. Before proposing a new skill, consider whether your content fits into an existing one. Most Sanity-specific guidance belongs in `sanity-best-practices` or `content-modeling-best-practices`. A new skill should only exist if it covers a genuinely distinct domain.

**Every token earns its place.** The context window is shared space. Your skill competes with conversation history, other skills, and the user's actual request. Challenge every paragraph: does the agent really need this? Could it figure this out on its own? If the answer is "probably yes", cut it.

**Opinionated over informational.** Don't explain what GROQ is. The model knows. Instead, tell it which patterns to prefer, which to avoid, and why. Skills should encode the judgement calls that come from experience, not the facts that come from reading docs.

**Progressive disclosure.** Keep `SKILL.md` as a routing table. Put the core principles and a quick reference up front, then point to reference files for the detail. Agents load reference files on demand, so a skill with 20 reference files doesn't cost 20 files worth of tokens. It costs whatever the agent actually needs for the task at hand.

For a thorough guide on skill authoring, structure, and patterns, see [Anthropic's skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). For thinking about how to write well for agents more broadly, see [How to write for an agent](https://www.sanity.io/blog/how-to-write-for-an-agent) on the Sanity blog.

## Skill structure

```
skills/
└── skill-name/
    ├── SKILL.md              # Required. Frontmatter + routing table + core guidance.
    └── references/            # Optional. Detailed content loaded on demand.
        ├── topic-one.md
        └── topic-two.md
```

A few conventions:

- **Frontmatter** must have `name` and `description`. Nothing else.
- **`SKILL.md` body** should stay under 500 lines. If you're going over, split content into reference files.
- **Reference files** in `sanity-best-practices` need YAML frontmatter with `name` and `description` because they're also served as rules through the MCP server. Other skills' resource files don't need frontmatter.
- **Keep references one level deep.** Everything should link directly from `SKILL.md`. Don't nest references inside references.
- **Write like you're onboarding a colleague.** Someone smart who can figure things out but needs context. Not a tutorial, not a reference manual. Somewhere in between.

## Making changes

The repo uses npm (not pnpm).

1. Fork the repo
2. Install dependencies with `npm ci`
3. Make your changes in `skills/<skill-name>/`
4. Run `npm run validate:all` to check skill and plugin validity
5. Submit a PR

### Adding to an existing skill

This is the most common and most welcome type of contribution. If you've found a better pattern, a missing framework guide, or a convention that agents keep getting wrong, add it to the relevant skill. For Sanity-specific content, that's almost always `sanity-best-practices`.

### Proposing a new skill

If you think a new skill is needed, open an issue first or if you're at Sanity, reach out to the AI Growth team in **#rd-ai-growth** on Slack to discuss it. We want to understand:

- What gap does this fill that existing skills don't cover?
- Is this opinionated guidance or documentation that the model likely already has?


## Questions?

- [GitHub Issues](https://github.com/sanity-io/agent-toolkit/issues) for bugs and proposals
- [Sanity Community (Discord)](https://www.sanity.io/community/join) for discussion
- Sanity employees: **#rd-ai-growth** on Slack

# Skill Architecture Guide

## SKILL.md Anatomy and Best Practices

### Structure

```markdown
---
name: skill-name
description: "Brief description for the slash command menu"
---

# Skill Name

## Instructions
Step-by-step prescriptive workflow:
1. First, do this specific thing
2. Then, do this next thing
3. Read references/specific-file.md for detailed guidance
4. Run scripts/validate.sh to check the output
5. Save the result to [specific location]

## References (example, adapt to your skill)
- references/style-guide.md: detailed style rules
- references/examples.md: example outputs

## Tools
- scripts/validate.sh: validates output against rules
- scripts/read-all.sh: reads existing content for context
```

### Best Practices

- **Keep SKILL.md lean** (under 100 lines). Put detailed guidance in references/
- **Be prescriptive**: numbered steps, specific actions, clear outputs
- **Use progressive disclosure**: SKILL.md links to references/ for depth
- **Name skills clearly**: the name becomes the slash command
- **Include frontmatter**: name and description are required for slash command registration

### When to Create scripts/ vs references/

- **scripts/**: Deterministic operations: validation, data reading, formatting, date/time
- **references/**: Knowledge: style guides, examples, templates, domain context
- **Neither**: Simple instructions that the agent handles natively

---

## Progressive Disclosure Pattern

```
SKILL.md (lean, ~50-100 lines)
  └── "Read references/style-guide.md for detailed style rules"
       └── references/style-guide.md (detailed, 200+ lines)
  └── "Read references/examples.md for output examples"
       └── references/examples.md (detailed, with full examples)
```

> **Note:** The file names above (style-guide.md, examples.md) are illustrative. Name your reference files to match your skill's domain (e.g., references/assessment-rubric.md, references/api-docs.md, etc.).

The agent loads SKILL.md first (cheap). Only loads reference files when needed for the current step (on-demand). This saves tokens and keeps context focused.

---

## Project-Level vs User-Level Decision Guide

| Factor | Project-Level (.claude/skills/) | User-Level (~/.claude/skills/) |
|--------|----------------------------------|-------------------------------|
| Scope | One specific project | All your projects |
| Sharing | Shared via git repo | Personal only |
| Examples | Content studio writer, project-specific validator | Memo writer, ai-firstify, code review |
| When to promote | After proving useful across 3+ projects | - |

**Start project-level.** Promote to user-level when the skill is proven useful across multiple projects.

---

## The Three Times Rule

If you have done something three times manually:
1. Document what you did (the steps, the inputs, the outputs)
2. Create a skill from those documented steps
3. Test the skill on the fourth occurrence
4. Refine based on real usage

Don't create skills speculatively. Wait for the pattern to emerge.

---

## Sharing and Packaging Skills

Skills are just folders with text files. To share:
1. **Zip the folder**: `zip -r my-skill.zip .claude/skills/my-skill/`
2. **Push to GitLab**: include .claude/skills/ in your repo
3. **Copy directly**: recipients paste into their .claude/skills/

Treat shared skills as deployed products:
- Version them (track changes in git)
- Document them (clear SKILL.md with examples)
- Maintain them (update when workflows change)

---

## Sub-Agent Patterns

### Research Agent

Collects information, produces a report. Context is isolated and discarded afterward.

```
Main agent --> spawns research sub-agent -->
  Sub-agent reads files, searches, analyzes -->
  Sub-agent produces report -->
  Main agent receives report, continues work
```

**Use for:** Investigation, data gathering, literature review, competitive analysis

### Review Agent

Critiques work in isolation. Doesn't share context with the creator.

```
Main agent --> creates content -->
  Spawns review sub-agent -->
  Reviewer critiques with fresh eyes -->
  Main agent receives feedback, revises
```

**Use for:** Content quality review, code review, proposal review

### Parallel Batch Agent

Same task, different inputs. All sub-agents run simultaneously.

```
Main agent --> splits 50 items into groups of 10 -->
  Spawns 5 sub-agents (one per group) -->
  All run in parallel -->
  Main agent aggregates results
```

**Use for:** RFP answers, bulk data processing, mass content generation

### Nested Agents

Agent spawns agent spawns agent. Use sparingly. One level of nesting covers most cases.

```
Main agent --> spawns research agent -->
  Research agent --> spawns analysis sub-agent -->
  Results bubble up
```

**Use for:** Complex multi-phase research where phases are independent

### Read-Only vs Read-Write

- **Read-only sub-agents:** Use for research, analysis, review. Safe, no side effects.
- **Read-write sub-agents:** Use for batch processing where output is needed. Add validation.

---

## Workflow Composition

### Multi-Skill Workflows

Skills can be combined in sequence:

```
/research-skill --> produces research report -->
/writing-skill --> uses report as input, produces draft -->
/review-skill --> critiques draft, produces feedback -->
Human reviews feedback --> approves or requests changes
```

### Skills + MCP Connections

Skills become more powerful with MCP integrations:
- **Slack MCP + research skill** = search Slack for insights, produce report
- **Notion MCP + writing skill** = create Notion pages from generated content
- **Atlassian MCP + tracking skill** = create Jira issues from analysis

### Human-in-the-Loop Checkpoints

Add explicit checkpoints where human review is required:

```
Step 3: Present findings to the user and wait for approval before proceeding
Step 6: Save draft to Google Docs for human review. Import comments before continuing.
```

### Document Feedback Loop

A particularly effective pattern:
1. Agent generates content
2. Export to Google Docs
3. Human adds comments in Google Docs
4. Agent reads comments and revises
5. Repeat until approved

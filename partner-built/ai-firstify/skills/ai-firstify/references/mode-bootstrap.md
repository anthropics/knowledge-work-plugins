# Mode 3: Bootstrap (New Project Setup)

Guide the user through setting up a new AI-first project from scratch. This mode is interactive: ask questions, do discovery, and build the right foundation.

## Phase 1: Discovery (Ask Questions)

Ask the user these questions one at a time. Don't overwhelm. Ask 2-3, then follow up based on answers.

**Problem definition:**
1. What specific problem are you trying to solve? (One sentence)
2. Who benefits? (Start with "me", build for yourself first)
3. What does "done" look like? What's the concrete output?
4. How will you measure impact? (Time saved, quality improved, tasks completed)

**Scope narrowing:**
5. Have you done this task manually before? How many times? (Three Times Rule check)
6. What data sources do you need? (Start with 1-2, not all of them)
7. Do you need a UI, or is terminal/file output sufficient? (Terminal-first check)
8. Should this be a skill, a content studio, or a standalone tool?

**Architecture decisions:**
9. Does this need to run without you present? (Deployment check. If no, make it a skill)
10. Do you need to search external systems? (MCP connections: Slack, Notion, Atlassian?)
11. Will this involve multiple phases? (Research -> create -> review = sub-agent opportunity)
12. Are there quality criteria that can be checked automatically? (Validation tools)

## Phase 2: Architecture Recommendation

Based on the answers, recommend one of these architectures:

**Simple Skill** (most common, default to this)
- Single SKILL.md with step-by-step instructions
- Optional references/ for domain knowledge
- Optional scripts/ for validation
- Lives in .claude/skills/ of an existing project or ~/.claude/skills/ for cross-project

**Multi-Skill Workflow**
- Multiple skills that chain together (research -> create -> review)
- Sub-agents for review/critique
- Shared references/ across skills
- Lives in a dedicated project folder

**Content Studio**
- Express.js backend + HTML frontend + content/ folder
- Skill for content creation with style guide
- Validation tools
- Best for: ongoing content creation in a specific domain

**Data/Analysis Tool**
- Skill with MCP connections (Slack, databases, APIs)
- Read-only data access where possible
- Output to files or terminal
- Best for: investigation, search, aggregation tasks

Present the recommendation with reasoning. Wait for user approval before building.

## Phase 3: Scaffold the Project

After the user approves the architecture:

1. **Create the project folder** (if not already in one)
   - Ask the user where they want to create it, or use the current directory

2. **Initialize git**
   ```bash
   git init
   ```

3. **Create .gitignore** (read references/project-structure.md for templates)

4. **Create CLAUDE.md** using the template from references/project-structure.md, filled with the user's answers from Phase 1

5. **Create the skill structure**
   ```
   .claude/skills/[skill-name]/
   ├── SKILL.md
   ├── references/
   └── scripts/
   ```

6. **Write SKILL.md** with prescriptive step-by-step instructions based on the user's workflow description

7. **Add validation** if quality criteria were identified in Phase 1

8. **Initial commit**
   ```bash
   git add . && git commit -m "Initial project setup with CLAUDE.md and [skill-name] skill"
   ```

## Phase 4: First Run

After scaffolding:
1. Run the skill via its slash command to test it
2. Review the output with the user
3. Iterate on the SKILL.md based on what worked and what didn't
4. Commit improvements
5. Suggest next steps (add references, add more validation, expand scope gradually)

## Key Principles to Apply During Bootstrap

- **Narrow Scope:** Start with the smallest useful version. One feature, one data source.
- **Build for Yourself:** No auth, no multi-user, no deployment. Build for localhost/terminal.
- **Terminal-First:** Default to file/terminal output. Only add UI if the user specifically needs it.
- **Plan Before Build:** The discovery phase IS the plan. Don't skip it.
- **Three Times Rule:** If they haven't done it manually at least twice, they might not know what they actually need. Suggest doing it manually first and documenting the steps.

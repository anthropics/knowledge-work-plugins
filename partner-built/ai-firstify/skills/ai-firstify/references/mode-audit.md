# Mode 1: Audit (Read-Only Analysis)

Perform a comprehensive analysis across 7 dimensions. Output a detailed report with scores and recommendations. Do NOT modify any files.

## Step 1: Scan the project
- Read CLAUDE.md (if it exists)
- List all files and directories
- Check for .git, .gitignore, .claude/skills/
- Identify the tech stack, languages, and frameworks

## Step 2: Analyze each dimension

**Dimension 1: Project Structure**
- Does CLAUDE.md exist? Is it well-structured and under 500 lines?
- Is there a .gitignore? Does it exclude sensitive files?
- Is git initialized with recent commits?
- Is the project organized as a monorepository (code + data + skills together)?

**Dimension 2: Agent Architecture**
- Are there embedded agents? (Look for: LLM API calls, custom agent frameworks, deployed chatbots, prompt chaining libraries)
- Read references/anti-patterns.md for detection patterns
- Are sub-agents used appropriately within Claude Code?

**Dimension 3: Skill Usage**
- Do skills exist in .claude/skills/?
- Are they well-structured? (SKILL.md with frontmatter, references/, scripts/)
- Are repeated workflows captured as skills?
- Read references/skill-architecture.md for best practices

**Dimension 4: Scope & Complexity**
- Is there unnecessary UI/frontend? (Terminal-first check)
- Are there over-engineered systems? (Unnecessary databases, auth, deployment pipelines)
- Does the project try to do too many things at once?

**Dimension 5: Context Hygiene**
- Is CLAUDE.md focused and well-structured?
- Are large reference documents in separate files (not inlined in CLAUDE.md)?
- Do skills use progressive disclosure (SKILL.md links to references/)?
- Is there context pollution (too many unrelated things in one folder)?

**Dimension 6: Safety**
- Are there credentials in code, config, or environment files?
- Does .gitignore exclude .env, credentials, API keys?
- For data tools: is access read-only where possible?
- Is there human-in-the-loop before external actions?

**Dimension 7: Workflow Design**
- Are workflows prescriptive (step-by-step)?
- Is there separation between creation and review (sub-agent reviewers)?
- Are there validation tools/scripts for critical operations?
- Is git commit discipline in place?

## Step 3: Generate report
Read references/assessment-rubric.md for scoring criteria and report template. Output a structured report with:
- Overall score (green/yellow/red for each dimension)
- Priority-ordered recommendations
- Specific files/patterns that need attention

## Step 4: Validate the report
Run `scripts/validate-report.sh` on the generated report to verify it follows the expected format (all sections present, all 7 dimensions scored, priority tags used).

## Step 5: Sub-agent review
Spawn a sub-agent to review the audit report with fresh eyes. The reviewer should:
- Check scoring consistency (does the evidence support each GREEN/YELLOW/RED?)
- Flag any dimensions where the score seems too generous or too harsh
- Verify recommendations are actionable and priority-ordered correctly
- Return a brief list of adjustments

Incorporate the reviewer's feedback before presenting the final report.

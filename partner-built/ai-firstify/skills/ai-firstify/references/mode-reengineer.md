# Mode 2: Re-Engineer (Active Transformation)

First, perform the full audit (read references/mode-audit.md). Then execute fixes in phases:

## Phase 1: Foundation
- Create or rewrite CLAUDE.md (read references/project-structure.md for template)
- Create .gitignore if missing (read references/project-structure.md for templates)
- Initialize git if not present (`git init` + initial commit)
- Restructure into monorepository if code/content/skills are scattered

## Phase 2: De-agentification
- Scan for embedded agent patterns (read references/anti-patterns.md for detection)
- For each found: propose replacement with Claude Code skills + sub-agents
- After user approval, remove agent infrastructure code
- Remember: "deployed an agent in a web app that nobody used because it was too complex and had too little context. Switched to Claude Code and it worked 10 times better"

## Phase 3: Skill Extraction
- Identify repeated workflows (scripts run multiple times, similar prompt patterns, recurring data transformations)
- Extract each into a proper skill in `.claude/skills/`
- Create SKILL.md with prescriptive step-by-step instructions
- Add validation tools (scripts/) where deterministic behavior is needed
- Add reference files where domain knowledge is needed
- Check if Anthropic pre-built skills could replace custom code

## Phase 4: Complexity Reduction
- Identify unnecessary UI/frontend (terminal-first check)
- Flag over-engineered infrastructure
- Propose simplifications: flat files over databases, skills over web apps, HTML output over React dashboards
- Remove features nobody asked for

## Phase 5: Context Hygiene
- Audit CLAUDE.md: is it focused? Under 500 lines? Well-structured?
- Move large reference documents from CLAUDE.md to separate files
- Ensure skills use progressive disclosure
- Check for context pollution

## Phase 6: Safety Hardening
- Scan for credentials in code, config, or environment files
- Check .gitignore excludes sensitive files
- For data tools: verify read-only access where possible
- Check for human-in-the-loop before external actions
- Add validation scripts for critical operations

## Phase 7: Workflow Optimization
- Make workflows prescriptive (step-by-step instructions in skills)
- Add sub-agents for review/critique tasks
- Add feedback loops: validation tools, test scripts, self-checking
- Set up proper git commit discipline

## Final: Generate Summary Report
After re-engineering, output:
- What was found (per dimension, with scores)
- What was changed (specific files created/modified/deleted)
- What still needs human decision (architectural choices, scope questions)
- Recommended next steps

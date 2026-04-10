# Assessment Rubric

## Scoring Criteria

Each dimension is scored as GREEN (good), YELLOW (needs improvement), or RED (critical issue).

---

### Dimension 1: Project Structure

**GREEN:**
- CLAUDE.md exists and is well-structured (under 200 lines)
- .gitignore exists and excludes sensitive files
- Git is initialized with regular commits
- Files are organized logically

**YELLOW:**
- CLAUDE.md exists but is too long or unfocused
- .gitignore exists but is incomplete
- Git exists but commits are infrequent
- Some organizational issues

**RED:**
- No CLAUDE.md
- No .gitignore
- No git
- Files are disorganized (50+ files in root)

**Detection commands:**
```bash
# Check CLAUDE.md
test -f CLAUDE.md && wc -l CLAUDE.md
# Check .gitignore
test -f .gitignore && cat .gitignore
# Check git
test -d .git && git log --oneline -5
# Count root files
ls -1 | wc -l
```

---

### Dimension 2: Agent Architecture

**GREEN:**
- No embedded agents (no LLM API calls in app code)
- Sub-agents used appropriately via Claude Code
- No custom agent frameworks

**YELLOW:**
- Some LLM API calls but for valid reasons (e.g., batch processing via API)
- Partial migration from embedded agent to skills

**RED:**
- Full embedded agent in a web app
- Custom agent framework
- LLM API calls for core functionality

**Detection commands:**
```bash
# Check for LLM libraries
grep -r "openai\|anthropic\|langchain\|llamaindex\|autogen\|crewai" --include="*.py" --include="*.js" --include="*.ts" -l
# Check for API keys
grep -r "OPENAI_API_KEY\|ANTHROPIC_API_KEY\|api_key" --include="*.py" --include="*.js" --include="*.env" -l
# Check for agent patterns
grep -r "chat/completions\|messages.create\|AgentExecutor\|ChatOpenAI" --include="*.py" --include="*.js" -l
```

---

### Dimension 3: Skill Usage

**GREEN:**
- Skills exist in .claude/skills/
- Skills are well-structured (SKILL.md + references/ + scripts/)
- Skills are prescriptive (step-by-step)
- Progressive disclosure used

**YELLOW:**
- Some skills exist but are poorly structured
- Skills are vague (not prescriptive)
- No references/ or scripts/

**RED:**
- No skills despite repeated workflows
- No .claude/ directory

**Detection commands:**
```bash
# Check for skills
find .claude/skills -name "SKILL.md" 2>/dev/null
# Check skill structure
ls -R .claude/skills/ 2>/dev/null
# Check skill length
wc -l .claude/skills/*/SKILL.md 2>/dev/null
# Check skill prescriptiveness (should have numbered steps)
grep -c "^[0-9]" .claude/skills/*/SKILL.md 2>/dev/null
# Check for progressive disclosure (references/ dirs)
find .claude/skills -name "references" -type d 2>/dev/null
```

---

### Dimension 4: Scope & Complexity

**GREEN:**
- Project does one thing well
- No unnecessary frontend (or frontend is warranted)
- No over-engineered infrastructure
- Clear, focused CLAUDE.md

**YELLOW:**
- Some scope creep (2-3 extra features)
- Frontend exists but may not be necessary
- Some unnecessary complexity

**RED:**
- Project tries to do too many things
- Full React/Vue/Angular app for a personal tool
- Unnecessary databases, auth, deployment pipelines
- Features nobody asked for

**Detection commands:**
```bash
# Check for heavy frontend frameworks
grep -r "react\|vue\|angular\|svelte" package.json 2>/dev/null
# Check for databases
grep -r "mongoose\|sequelize\|prisma\|typeorm\|sqlite3\|pg " package.json requirements.txt 2>/dev/null
# Check for auth
grep -r "passport\|jwt\|bcrypt\|auth0\|firebase-auth" package.json requirements.txt 2>/dev/null
# Count files (complexity indicator)
find . -type f -not -path './.git/*' -not -path './node_modules/*' | wc -l
```

---

### Dimension 5: Context Hygiene

**GREEN:**
- CLAUDE.md under 200 lines and well-organized
- Skills use progressive disclosure
- Reference material in references/ directories
- No context pollution

**YELLOW:**
- CLAUDE.md is 200-500 lines
- Some inline reference material in SKILL.md
- Minor organizational issues

**RED:**
- CLAUDE.md over 500 lines
- All context in one file
- No progressive disclosure
- Context pollution (unrelated concerns mixed)

**Detection commands:**
```bash
# CLAUDE.md length
wc -l CLAUDE.md 2>/dev/null
# SKILL.md lengths
wc -l .claude/skills/*/SKILL.md 2>/dev/null
# Check for references directories
find .claude -name "references" -type d 2>/dev/null
```

---

### Dimension 6: Safety

**GREEN:**
- No credentials in code
- .gitignore excludes sensitive files
- Read-only access where possible
- Human-in-the-loop for external actions

**YELLOW:**
- .gitignore exists but may miss some sensitive files
- Some external actions without explicit approval

**RED:**
- Credentials in code or config files
- No .gitignore
- Write access to production systems without approval
- Automated external actions without human review

**Detection commands:**
```bash
# Check for hardcoded secrets
grep -r "password\|secret\|token\|api_key" --include="*.py" --include="*.js" --include="*.ts" --include="*.json" -l 2>/dev/null | grep -v node_modules | grep -v package-lock
# Check for .env files in git
git ls-files | grep -i "\.env"
# Check .gitignore for common exclusions
grep -c "\.env\|credentials\|\.pem\|api_key" .gitignore 2>/dev/null
```

---

### Dimension 7: Workflow Design

**GREEN:**
- Workflows are prescriptive (step-by-step in skills)
- Sub-agents used for review/critique
- Validation tools/scripts exist
- Proper git commit discipline

**YELLOW:**
- Some workflows are prescriptive
- No sub-agent review but manual review exists
- Partial validation

**RED:**
- No prescriptive workflows
- No review process
- No validation
- No git discipline

**Detection commands:**
```bash
# Check for validation scripts
find . -name "validate*" -o -name "check*" -o -name "test*" 2>/dev/null | grep -v node_modules
# Check SKILL.md for numbered steps
grep -c "^[0-9]" .claude/skills/*/SKILL.md 2>/dev/null
# Check git commit frequency
git log --oneline --since="1 week ago" 2>/dev/null | wc -l
```

---

## Report Template

```markdown
# AI-Firstify Assessment Report

**Project:** [project name]
**Date:** [date]
**Mode:** [Audit / Re-engineer]

## Overall Score

| Dimension | Score | Summary |
|-----------|-------|---------|
| 1. Project Structure | [GREEN/YELLOW/RED] | [one-line summary] |
| 2. Agent Architecture | [GREEN/YELLOW/RED] | [one-line summary] |
| 3. Skill Usage | [GREEN/YELLOW/RED] | [one-line summary] |
| 4. Scope & Complexity | [GREEN/YELLOW/RED] | [one-line summary] |
| 5. Context Hygiene | [GREEN/YELLOW/RED] | [one-line summary] |
| 6. Safety | [GREEN/YELLOW/RED] | [one-line summary] |
| 7. Workflow Design | [GREEN/YELLOW/RED] | [one-line summary] |

## Priority Recommendations

1. **[HIGH]** [recommendation]: [estimated effort]
2. **[HIGH]** [recommendation]: [estimated effort]
3. **[MEDIUM]** [recommendation]: [estimated effort]
4. **[LOW]** [recommendation]: [estimated effort]

## Detailed Findings

### Dimension 1: Project Structure
[Detailed findings, specific files, what's good, what needs work]

### Dimension 2: Agent Architecture
[Detailed findings...]

[...continue for all 7 dimensions...]

## Changes Made (Re-engineer mode only)

| Action | File | Description |
|--------|------|-------------|
| Created | CLAUDE.md | Project context file |
| Created | .gitignore | Standard exclusions |
| Created | .claude/skills/[name]/SKILL.md | Extracted workflow |
| Deleted | src/agent/ | Removed embedded agent |
| Modified | package.json | Removed LLM dependencies |

## Still Needs Human Decision

- [ ] [Decision needed about X]
- [ ] [Decision needed about Y]

## Recommended Next Steps

1. [Next step]
2. [Next step]
3. [Next step]
```

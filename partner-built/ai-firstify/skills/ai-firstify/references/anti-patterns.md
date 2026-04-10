# Anti-Patterns: Common Mistakes and How to Fix Them

## Architecture Anti-Patterns

### Building an Agent in a Web App
**Severity:** RED

**Description:** Deploying an LLM-powered agent inside a web application (chatbot, conversational UI, or API-driven agent). Result: "Nobody used it because it was too complex and had too little context." Switched to Claude Code skills and it worked "10 times better."

**How to detect:**
- grep for: `openai`, `anthropic`, `langchain`, `llamaindex`, `autogen`, `crewai`
- Look for: `/api/chat`, `/api/agent`, streaming response handlers
- Check for: prompt template files, chain/pipeline definitions
- Scan dependencies: `package.json` or `requirements.txt` for LLM libraries

**Fix procedure:**
1. Identify what the embedded agent does (list its capabilities)
2. Convert each capability to a Claude Code skill
3. Create SKILL.md with prescriptive instructions
4. Remove the agent infrastructure code
5. Test the skills via slash commands

**Relevant principles:** #5 (Don't Build Your Own Agent), #3 (Build for Yourself First)

---

### Over-Investing in Frontend UI
**Severity:** YELLOW

**Description:** Building React dashboards, polished UIs, or complex frontend applications for tools that are primarily used by the builder. Terminal output or a simple file is sufficient for most personal tools.

**How to detect:**
- Look for: React, Vue, Angular, Svelte in dependencies
- Check for: multiple CSS files, component directories, UI frameworks
- Scan for: authentication/login pages in personal tools
- Count frontend files vs. core logic files

**Fix procedure:**
1. Identify the core functionality (what does the tool actually DO?)
2. Replace frontend with terminal output or file output
3. If visual output is needed, use simple HTML files (no framework)
4. Remove frontend framework dependencies
5. Keep the UI only if non-technical stakeholders need it

**Relevant principles:** #2 (Narrow Scope), #3 (Build for Yourself First)

---

### Building Custom Agent Frameworks
**Severity:** RED

**Description:** Creating custom tool-calling, prompt chaining, or agent orchestration systems instead of using Claude Code's built-in capabilities.

**How to detect:**
- grep for: `tool_call`, `function_calling`, `chain`, `pipeline`, `orchestrat`
- Look for: custom prompt template systems
- Check for: agent state management code
- Scan for: retry/fallback logic for LLM calls

**Fix procedure:**
1. Map custom agent capabilities to Claude Code features
2. Replace custom tool-calling with Claude Code tools (scripts/)
3. Replace custom chaining with skill step-by-step instructions
4. Replace custom orchestration with sub-agents
5. Delete the framework code

**Relevant principles:** #5 (Don't Build Your Own Agent)

---

### Unnecessary Deployment
**Severity:** YELLOW

**Description:** Deploying applications (Docker, cloud hosting, CI/CD) for tools that could be skills. The default answer to "should I deploy?" is no.

**How to detect:**
- Look for: Dockerfile, docker-compose.yml, .github/workflows/, .gitlab-ci.yml
- Check for: cloud configuration (AWS, GCP, Azure files)
- Scan for: deployment scripts, infrastructure-as-code
- Ask: does this NEED to run without a human present?

**Fix procedure:**
1. Ask: Can this be a skill instead?
2. Ask: Can this be a static HTML page on GitLab Pages?
3. Ask: Does this need to run without a human present?
4. If all "no" answers: convert to a skill
5. Remove deployment infrastructure

**Relevant principles:** #3 (Build for Yourself First), #2 (Narrow Scope)

---

### Building Without Version Control
**Severity:** RED

**Description:** No git repository, no commits, no history. One bad prompt can destroy hours of work.

**How to detect:**
- Check for: `.git` directory (if missing, this is the anti-pattern)
- Check for: `.gitignore` (if missing, partial anti-pattern)
- Check git log: are there regular commits?

**Fix procedure:**
1. `git init`
2. Create appropriate `.gitignore`
3. `git add . && git commit -m "Initial commit"`
4. Set up remote on GitLab
5. Commit after every significant change

**Relevant principles:** #1 (You Are Responsible)

---

## Workflow Anti-Patterns

### Single Monolithic Prompt
**Severity:** YELLOW

**Description:** One huge prompt that tries to accomplish everything at once instead of a prescriptive skill with clear steps.

**How to detect:**
- SKILL.md with one giant paragraph of instructions
- No numbered steps or phases
- Mixing research, creation, and validation in one instruction

**Fix procedure:**
1. Break the prompt into distinct phases
2. Number each step clearly
3. Add validation checkpoints between phases
4. Create separate sub-skills if phases are complex
5. Test each phase independently

**Relevant principles:** #2 (Narrow Scope), #4 (Start with a Plan)

---

### No Context Separation
**Severity:** YELLOW

**Description:** Everything in CLAUDE.md instead of using skills and references. All context loaded at once instead of progressively.

**How to detect:**
- CLAUDE.md over 500 lines
- No .claude/skills/ directory
- No references/ subdirectories in skills
- SKILL.md files with inline reference material

**Fix procedure:**
1. Identify distinct workflows in CLAUDE.md
2. Extract each into a separate skill
3. Move reference material to references/ directories
4. Keep CLAUDE.md as a project overview only
5. Use progressive disclosure

**Relevant principles:** #6 (Stick to the Point), #2 (Narrow Scope)

---

### Author Reviews Own Work
**Severity:** YELLOW

**Description:** The same agent instance that created content also reviews it. Without context isolation, the "reviewer" is biased by the creation context.

**How to detect:**
- Skills that include "review your work" as a final step without spawning a separate agent
- No use of sub-agents for critique
- Self-review without context isolation

**Fix procedure:**
1. Add a sub-agent review step (use Task tool)
2. Give the reviewer a different perspective/criteria
3. The reviewer should NOT see the creation instructions
4. Aggregate reviewer feedback before finalizing

**Relevant principles:** #3 (Feedback Loop pattern)

---

### No Validation
**Severity:** YELLOW

**Description:** No tools, scripts, or checks to validate output. Relying purely on hope that the LLM gets it right.

**How to detect:**
- No scripts/ directory in skills
- No test files
- No validation commands in SKILL.md
- No error checking steps

**Fix procedure:**
1. Identify what "correct" looks like (rules, constraints, format)
2. Write validation scripts for checkable rules
3. Add validation steps to SKILL.md
4. Use sub-agents for subjective validation
5. Add error handling for common failures

**Relevant principles:** #5 (Tools pattern), #3 (Feedback Loop pattern)

---

### Building for Others First
**Severity:** YELLOW

**Description:** Building multi-user tools, shared platforms, or team features before the tool works for the builder. Adding unnecessary complexity for hypothetical users.

**How to detect:**
- User management code
- Multi-tenant database schemas
- Role-based access control
- "Admin panel" features
- User onboarding flows

**Fix procedure:**
1. Strip all multi-user features
2. Build for yourself only
3. Use for a week
4. Share as a skill (copy folder) if it works
5. Only add multi-user features if there's proven demand

**Relevant principles:** #3 (Build for Yourself First)

---

## Scope Anti-Patterns

### Too Many Data Sources at Once
**Severity:** YELLOW

**Description:** Trying to integrate 50 data sources from day one instead of starting with 1-2 and expanding.

**How to detect:**
- Multiple API integrations in initial version
- Data source configuration files with many entries
- Complex data merging/normalization code

**Fix procedure:**
1. Identify the single most valuable data source
2. Build the full workflow for that one source
3. Validate it works end-to-end
4. Add one more source at a time
5. Refactor shared patterns as they emerge

**Relevant principles:** #2 (Narrow Scope), #3 (Build for Yourself First)

---

### Feature Creep from Vibe Coding
**Severity:** YELLOW

**Description:** Adding features spontaneously because "it's easy" rather than because they're needed. The vibe coding trap: building is so easy that you build things nobody asked for.

**How to detect:**
- Features mentioned in code but not in CLAUDE.md or any plan
- UI elements that serve no clear workflow
- Code paths that aren't tested or documented
- Multiple half-finished features

**Fix procedure:**
1. List all features in the project
2. For each: "did someone ask for this?" and "have I used this?"
3. Remove unused features
4. Focus on completing one feature fully before starting the next

**Relevant principles:** #2 (Narrow Scope), #4 (Start with a Plan)

---

### Not Using /clear
**Severity:** YELLOW

**Description:** Never clearing context, leading to stale information, confused responses, and wasted tokens.

**How to detect:**
- No evidence of task separation in git history
- Commits that mix unrelated changes
- Responses referencing outdated context

**Fix procedure:**
1. Use /clear when switching tasks
2. Document key learnings in CLAUDE.md before clearing
3. Use /compact when context is large but still relevant
4. Start significant new tasks in empty folders

**Relevant principles:** #8 (Start with a Clean Slate)

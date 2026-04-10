# The 7 AI-First Design Patterns

## Pattern 1: One-Shotting

**Summary:** Minimal prompt, maximum freedom. Good for inspiration and gauging difficulty.

**Description:** Give a minimal prompt and let the AI run freely. No constraints, no detailed specifications. Just an idea and maximum creative freedom. One-shotting also works as a difficulty gauge: if the AI nails it in one shot, the task was straightforward. If it struggles, you need more specificity.

**When to use:**
- Inspiration and exploration
- Prototyping and proof of concepts
- Gauging task difficulty before investing in detailed specs
- Creative work where surprise is welcome

**When NOT to use:**
- Production work requiring specific outcomes
- Workflows that need consistency across runs
- Tasks with strict format/quality requirements

**Implementation checklist:**
- [ ] Single prompt, no multi-step instructions
- [ ] Let the agent choose its own approach
- [ ] Review output as a difficulty gauge
- [ ] If good: task is simple, might not need a skill
- [ ] If poor: task needs more structure, consider a skill

---

## Pattern 2: Monorepository

**Summary:** Code + data + skills in one Git repo. The agent sees everything.

**Description:** Keep all related code, data, skills, and configuration in a single Git repository. The AI works best when everything is in one place. It can see the full picture and make changes that span code and content.

**When to use:**
- Any project with code AND content/data
- Content studios
- Projects with skills and tools
- Any setup where the agent needs to see the full picture

**When NOT to use:**
- Truly independent projects that share nothing
- Massive repositories where context window would overflow

**Implementation checklist:**
- [ ] Single git repo for code + content + skills
- [ ] CLAUDE.md at the root describing the project
- [ ] .claude/skills/ for project-specific skills
- [ ] Content/data files alongside code
- [ ] .gitignore for node_modules, .env, etc.

**Example structure:**
```
my-project/
├── CLAUDE.md
├── .gitignore
├── package.json
├── src/                  # Application code
├── content/              # Content/data files
├── .claude/
│   └── skills/
│       └── my-skill/
│           ├── SKILL.md
│           ├── references/
│           └── scripts/
└── docs/                 # Documentation
```

---

## Pattern 3: Feedback Loop

**Summary:** Agent tests its own work: unit tests, sub-agent critique, self-testing.

**Description:** Set up mechanisms for the agent to test its own work and iterate. Three types: unit tests (agent writes tests then code to pass them), sub-agent critique (one agent creates, another reviews), and self-testing (agent runs its output and checks for errors).

**When to use:**
- Content generation requiring quality control
- Code that needs validation
- Any workflow where output quality varies
- Multi-step processes where early errors compound

**When NOT to use:**
- Simple one-shot tasks
- Tasks where human review is the feedback loop
- Trivial operations that can't really fail

**Implementation checklist:**
- [ ] Validation script in scripts/ (for deterministic checks)
- [ ] Sub-agent reviewer for subjective quality (use Task tool)
- [ ] Test suite for code outputs
- [ ] Self-checking step at end of skill workflow
- [ ] Error handling that retries with modified approach

---

## Pattern 4: Content Plus Form

**Summary:** Known template + custom content. Template provides structure, content provides uniqueness.

**Description:** Use a known format or template and fill it with custom content. This is how the Flappy Bird demo worked: the "form" is a Flappy Bird game (well-known template), the "content" is a PDF about TechWolf. Result: a themed Flappy Bird game.

**When to use:**
- Creating content in a known format (emails, reports, memos)
- Building apps with well-known UI patterns (dashboards, landing pages)
- Gamification of existing content
- Any time you have a template + unique data

**When NOT to use:**
- Truly novel creations without precedent
- Tasks where the format itself needs to be designed

**Implementation checklist:**
- [ ] Identify the "form" (template, known format, existing design)
- [ ] Identify the "content" (unique data, custom information)
- [ ] Provide the form as a reference file or example
- [ ] Provide the content as input or from a data source
- [ ] Let the agent combine them

---

## Pattern 5: Tools

**Summary:** Deterministic scripts. Use when you need exact, repeatable behavior.

**Description:** Give the agent access to deterministic scripts it can run. While the LLM is probabilistic (slightly different output each time), a tool always does exactly the same thing. Create tools not because the agent can't do it, but because you want it done in one specific way.

**When to use:**
- Getting current date/time
- Reading existing content for consistency
- Validation against rules
- Data transformations that must be exact
- File format conversions

**When NOT to use:**
- Creative tasks requiring flexibility
- Tasks where the approach should vary
- Simple operations the agent handles natively

**Implementation checklist:**
- [ ] Script in scripts/ directory (bash or Python)
- [ ] Script is executable (chmod +x)
- [ ] Script has clear input/output contract
- [ ] Script is referenced in SKILL.md
- [ ] Script handles errors gracefully

**Example:**
```bash
#!/bin/bash
# scripts/validate.sh: Validates content against rules
FILE="$1"
if [ -z "$FILE" ]; then echo "Usage: validate.sh <file>"; exit 1; fi
# Check specific rules...
echo "PASS: Content is valid"
```

---

## Pattern 6: Agent Skills

**Summary:** Instruction files in .claude/skills/. Loaded on demand via slash commands.

**Description:** Skills are text files that load contextual instructions into the agent on demand. They live in .claude/skills/ and are activated via slash commands. A skill typically contains: a description, instructions, reference examples, and tools.

**When to use:**
- Repeated workflows (the Three Times Rule)
- Domain-specific knowledge needed on demand
- Complex multi-step procedures
- Workflows that need consistency across runs

**When NOT to use:**
- One-time tasks
- Simple operations that don't need instructions
- Tasks where every run should be different

**Implementation checklist:**
- [ ] SKILL.md with frontmatter (name, description)
- [ ] Step-by-step prescriptive instructions
- [ ] references/ for domain knowledge and examples
- [ ] scripts/ for deterministic tools
- [ ] Progressive disclosure (SKILL.md links to references/)

**Skill anatomy:**
```
.claude/skills/my-skill/
├── SKILL.md              # Main instructions (lean, prescriptive)
├── references/           # Domain knowledge, examples, templates
│   ├── style-guide.md
│   └── examples.md
└── scripts/              # Deterministic tools
    ├── validate.sh
    └── read-all.sh
```

---

## Pattern 7: Sub-Agents

**Summary:** Parallel, independent workers. Great for batch processing.

**Description:** Break large tasks into parallel, independent workers. Each sub-agent gets a specific prompt and isolated context, works independently, and reports back. Sub-agents can use skills and spawn their own sub-agents (but don't nest too deep).

**When to use:**
- Batch processing (same task, different inputs)
- Research tasks (isolated investigation, produce report)
- Review/critique (separate instance reviews, fresh perspective)
- Parallel data processing

**When NOT to use:**
- Tasks requiring shared state between workers
- Sequential workflows where order matters
- Simple tasks that don't benefit from parallelism

**Implementation checklist:**
- [ ] Clear, self-contained prompt for each sub-agent
- [ ] Isolated context (sub-agent doesn't see main conversation)
- [ ] Defined output format for results
- [ ] Aggregation strategy for combining results
- [ ] Read-only or read-write settings as appropriate

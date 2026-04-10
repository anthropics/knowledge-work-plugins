# The 9 AI-First Design Principles

## Principle 1: You Are Responsible

**Summary:** You are the pilot. AI is your co-pilot. Your name is on everything it produces.

**Description:** Think of yourself as a pilot. The AI is your autopilot. It handles a lot of the flying, but you are always responsible for the plane and everyone on it. Whether the AI wrote the email, generated the report, or built the tool, your name is on it. This applies especially to automated systems. If you build something that runs unattended and it makes mistakes, that is on you, even if the AI caused the error.

**When it applies:** Always. Every interaction with AI tools. Especially when outputs are shared with others or when automated systems run without human oversight.

**Common violations:**
- Sharing AI-generated content without reviewing it
- Building automated pipelines without human review steps
- Blaming AI for mistakes in outputs you distributed
- Running unattended agents that post to Slack, send emails, or modify data

**How to detect in code:**
- Look for automated posting/sending without approval gates
- Check for scheduled/cron AI tasks without review checkpoints
- Scan for API calls that write to external systems without confirmation

**How to fix:**
- Add human-in-the-loop review before any external action
- Add approval gates before automated distribution
- Log all AI-generated outputs for audit trail
- Review all outputs before sharing

---

## Principle 2: Narrow Scope

**Summary:** Define narrow goals. Avoid complexity creep from vibe coding. One task at a time.

**Description:** LLMs perform worse when given too many tasks at once. They are like a brilliant but easily distracted junior colleague. Give them one clear task and they will excel. Pile on five things and quality drops everywhere. The empty folder approach: start each significant task in a fresh, empty folder.

**When it applies:** Every time you give instructions to an agent. When designing skills. When scoping projects.

**Common violations:**
- Skills that try to do 10 things at once
- CLAUDE.md files that describe the entire organization
- Prompts that ask for multiple unrelated outputs
- Projects that mix too many concerns in one folder

**How to detect in code:**
- CLAUDE.md longer than 500 lines
- Skills with more than 15 steps
- Folders with more than 50 files at the same level
- Single prompts/skills that mention multiple unrelated domains

**How to fix:**
- Split multi-concern skills into focused single-purpose skills
- Use the empty folder approach for new tasks
- Keep CLAUDE.md under 200 lines (ideally under 100)
- One skill = one workflow

---

## Principle 3: Build for Yourself First

**Summary:** Build for yourself before others. Use it daily. Then share what works.

**Description:** Do not build tools for others until you have built them for yourself. When you use your own tool daily, you discover what actually matters and what is unnecessary fluff. Usage is not a good metric for impact. A Pokemon game has lots of usage but doesn't solve a business problem.

**When it applies:** Starting any new project. Deciding whether to share a tool. Prioritizing features.

**Common violations:**
- Building multi-user apps before using the tool yourself
- Adding login/auth systems for a personal tool
- Building deployment pipelines before the tool works locally
- Designing for "the team" before solving your own problem

**How to detect in code:**
- Auth/login systems in personal tools
- Multi-user database schemas
- Deployment configurations (Docker, k8s, CI/CD) for tools nobody uses yet
- User management features

**How to fix:**
- Strip auth and multi-user features
- Build for localhost first
- Use for a week yourself before considering sharing
- Share as a skill (copy the folder) rather than deploying

---

## Principle 4: Start with a Plan

**Summary:** Shift+Tab before building. Planning is cheaper than rebuilding.

**Description:** Before building anything substantial, enter plan mode. Claude Code will research, ask clarifying questions, propose a file structure and approach, and wait for your approval before writing code. You can iterate on the plan before a single line of code is written.

**When it applies:** Any non-trivial task. New projects. Feature additions. Refactoring.

**Common violations:**
- Jumping straight into coding without planning
- Not using plan mode for multi-file changes
- Building before understanding the requirements
- Skipping the design phase for skills

**How to detect in code:**
- No CLAUDE.md (suggests no planning phase)
- Messy file structure (suggests organic growth without planning)
- Multiple failed attempts visible in git history
- Skills without clear step-by-step instructions

**How to fix:**
- Always use Shift+Tab or /plan before building
- Write a brief plan in CLAUDE.md before starting
- Invest 15-30 minutes in planning before any build session

---

## Principle 5: Don't Build Your Own Agent

**Summary:** Use Claude Code. It improves automatically. Your custom agent won't.

**Description:** You already have an agent with tools, research, and coding abilities. Building agent infrastructure in your applications is almost never the right choice. Your custom agent will never be as smart, bulletproof, or flexible as maintained agents like Claude Code. As models improve, Claude Code improves automatically. Your custom agent stays stuck in time.

> **Important:** Sub-agents WITHIN Claude Code (e.g., using the Agent tool, TeamCreate, or sub-agent patterns in skills) are fine and encouraged. "Don't build your own agent" means don't build a web app or deployed service with an embedded LLM agent. Using Claude Code's built-in multi-agent capabilities is the recommended approach.

**When it applies:** Whenever you're tempted to add LLM API calls to your application. When designing system architecture. When choosing between skills and deployed agents.

**Common violations:**
- LLM API calls (OpenAI, Anthropic, etc.) in application code
- Custom agent frameworks or prompt chaining libraries
- Deployed chatbots or conversational UIs with embedded AI
- Custom tool-calling implementations

**How to detect in code:**
- grep for: `openai`, `anthropic`, `langchain`, `llamaindex`, `autogen`, `crewai`
- Look for: API key environment variables for LLM providers
- Check for: prompt template files, chain definitions, agent configurations
- Scan for: streaming response handlers, tool/function calling implementations

**How to fix:**
- Replace embedded agents with Claude Code skills
- Convert agent workflows to skill + sub-agent patterns
- Remove LLM API dependencies
- Use Claude Code's built-in sub-agent capabilities instead

---

## Principle 6: Stick to the Point

**Summary:** Keep context relevant. Use skills and tools for on-demand context. Keep CLAUDE.md clean.

**Description:** Agents work much better when their context is limited to what is relevant in the moment. Use separate files, tools, skills, and sub-agents to provide context when relevant. Keep CLAUDE.md clean and focused.

**When it applies:** Structuring CLAUDE.md. Designing skills. Organizing project files.

**Common violations:**
- CLAUDE.md that's an encyclopedia (500+ lines)
- All reference material inlined in SKILL.md instead of in references/
- Too many unrelated files in one directory
- Loading all context at once instead of progressively

**How to detect in code:**
- CLAUDE.md file size (should be under 200 lines)
- SKILL.md files larger than 100 lines without references/ directory
- Flat folder structures with 50+ files
- No .claude/skills/ directory despite complex workflows

**How to fix:**
- Move reference material to references/ subdirectories
- Use progressive disclosure: SKILL.md links to references/
- Organize files into logical subdirectories
- Keep CLAUDE.md focused on project overview and conventions

---

## Principle 7: Don't Be Stingy on the Input

**Summary:** Use voice. Be generous with context. Detailed prompts beat short ones.

**Description:** Removing ambiguity and giving more depth to your prompts works wonders. Provide ample documentation, additional links, etc. Use voice transcription to give complete and nuanced input. The times of over-engineering prompts are over. Just be clear and detailed.

**When it applies:** Writing prompts. Creating skills. Describing requirements.

**Common violations:**
- Vague one-line prompts for complex tasks
- Skills without detailed step-by-step instructions
- Missing context in CLAUDE.md
- Not providing examples or reference material

**How to detect in code:**
- SKILL.md files with fewer than 10 lines of instructions
- Skills without any reference files
- CLAUDE.md that's too sparse (under 10 lines)
- No examples provided in skill instructions

**How to fix:**
- Use VoiceInk for richer, more detailed prompts
- Add reference files with examples and style guides
- Include step-by-step procedures in skills
- Provide context about why, not just what

---

## Principle 8: Start with a Clean Slate

**Summary:** /clear before new tasks. Fresh folders. Document learnings first.

**Description:** Start with a fresh folder as context and bring in exactly what you need. During big sessions, clearing context dramatically improves performance. Before clearing: document useful insights in CLAUDE.md so they persist.

**When it applies:** Starting a new task. Switching between different work. After long sessions.

**Common violations:**
- Never using /clear (stale context accumulates)
- Not documenting learnings before clearing
- Mixing unrelated tasks in one session
- Keeping old project files when starting fresh

**How to detect in code:**
- No CLAUDE.md (suggests no documentation of learnings)
- Large, cluttered project folders with mixed concerns
- No evidence of task separation

**How to fix:**
- Use /clear when switching tasks
- Document key learnings in CLAUDE.md before clearing
- Use separate folders for separate concerns
- Start significant new tasks in empty folders

---

## Principle 9: Speak the Right Language

**Summary:** Text + images are what models understand. Provide screenshots for visual work.

**Description:** AI understands text and images. It struggles with spatial layout, proprietary binary formats, and physical-world reasoning. For visual work, provide screenshots alongside code so the agent can compare visual output with the code and make informed adjustments.

**When it applies:** Working with visual outputs (slides, UIs, layouts). Providing feedback on design. Working with binary formats.

**Common violations:**
- Asking the agent to "make it look nice" without a screenshot
- Expecting the agent to understand spatial layouts from code alone
- Not providing visual references when working on UI

**How to detect in code:**
- Visual output generation without screenshot-based feedback loops
- Slide/presentation generation without visual validation
- UI work without reference images

**How to fix:**
- Always provide screenshots when working on visual output
- Use the screenshot-comparison workflow for iterative visual work
- Include reference images in skill reference files

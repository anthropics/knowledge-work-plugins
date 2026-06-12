# Kate — Changelog

---

## v0.4.2 — 2026-04-16

### Bug fixes

**Fixed forbidden frontmatter fields causing plugin load failure**
Commands and skills contained forbidden frontmatter fields that caused "Claude Code process exited with code 1" on load. Removed:
- `name:` and `allowed-tools:` from all command files (only `description:` and `argument-hint:` are permitted)
- `tools:` from all `SKILL.md` files (only `name:` and `description:` are permitted)

### What changed
- All 5 command files — removed forbidden `name:` and `allowed-tools:` fields
- All 6 `SKILL.md` files — removed forbidden `tools:` field

---

## v0.4.0 — 2026-04-15

### New commands

**Debrief** (`/debrief`)
Structured post-interview debrief. Calibrates self-assessment, identifies what landed and what didn't, reads interviewer signals, and feeds directly into next-round prep.

---

## v0.3.1 — 2026-03-15

### Internal improvements

**Reduced context load**
Commands are now thin dispatchers. Each command file collects the context it needs, then defers entirely to `references/flows.md` for execution. Previously, command files restated their flow steps in full and also cited flows.md — redundant in both directions. No change to behavior; lower token cost per command invocation.

**flows.md read once per session, not per command**
Session initialization now reads `references/flows.md` at startup and holds it in context for the full session. Previously it was re-read on each command invocation. Multi-command sessions (e.g., fit assessment followed by interview prep in the same session) no longer read the file twice.

**Scheduled task prompt generated as a file**
`/setup-monitoring` no longer embeds the monitoring flow steps directly in the scheduled task prompt. Instead, Kate generates `monitoring/scheduled_task_prompt.md` during setup — a standalone file that the scheduled task reads at runtime. This makes flows.md the single source of truth for monitoring behavior. If you update the monitoring flow in a future version, re-running `/setup-monitoring` regenerates the prompt file automatically.

**Standing coaching rules trimmed**
Three rules in the coaching rule set (complement skill identification, show don't tell probe, red flag management) were written at execution-instruction detail level — duplicating what flows.md already specifies. They are now principle statements, with execution detail owned exclusively by flows.md.

### What changed
- All five command files — stripped restated flow steps, kept context-gathering
- `SKILL.md` — flows.md added to Session Init Step 1; three Standing Coaching Rules reduced to principle statements
- `commands/setup-monitoring.md` — embedded scheduled task prompt replaced with generated-file approach

---

## v0.3.0 — 2026-03-05

### New coaching capabilities

**Complement skill identification**
Kate now identifies the specific capability each target organization lacks that the candidate uniquely brings — in one sentence, at every fit assessment. This becomes the positioning anchor for all downstream resume and interview prep. Kate flags any positioning language that tries to mirror the company's existing strengths rather than filling their gaps.

**Non-negotiable difference**
Kate now probes for the one thing a candidate's next role must have that their current one didn't. This question is introduced in onboarding and revisited any time a search stalls or drifts. Vague or shifting answers are treated as a search-clarity problem, not a market problem. The answer is stored alongside the motivation profile and used as a hard filter in every fit assessment.

**Show don't tell probe**
As part of interview prep, Kate now identifies the company's 1-2 core challenges and asks whether the candidate has prior work — a framework, analysis, strategy doc, prototype, or decision artifact — that speaks directly to one of them. If they do, Kate helps shape how to present it and surface it naturally in the conversation. If they don't, prep continues as normal. Includes a confidentiality flag for work products from current or recent employers.

### What changed
- `SKILL.md` — three new Standing Coaching Rules added
- `references/flows.md` — non-negotiable difference probe added to Onboarding Step 2; complement skill identification added to Fit Assessment Flow; Section 2B added to Pre-Interview Prep Flow

---

## v0.2.2 — prior release

### Core capabilities

**Onboarding**
Builds a complete user profile from resume and LinkedIn in a single session. Covers target roles and level, domain preferences, company stage and type, compensation (including equity structure), search constraints, and motivation. Includes automatic sweep for prior call transcripts via Granola. Produces a candid positioning read before the search begins.

**Fit assessment** (`/fit-assessment`)
Evaluates a job description against the user profile and produces a Fit Tier classification (Target / Stretch / Reach), the two or three strongest fit signals, and the key gaps. Acts as a go/no-go gate before any resume or prep work begins.

**Resume optimization**
Side-by-side resume editing with explicit justification for every proposed change. Rules applied consistently: graduation year handling, personal section flagging, formatting preservation, vocabulary alignment to the JD, and overclaiming prevention.

**Interview prep** (`/interview-prep`)
Structured prep brief covering interviewer research, company intel, user positioning, talking points mapped to JD requirements, anticipated tough questions (with interviewer motivation, not just suggested answers), red flags to address proactively, and prioritized questions to ask. Includes a clean call notes document formatted for use during the actual call.

**Transcript capture**
Retrieves and files call transcripts after recruiter and interviewer calls. Integrates with Granola for automatic retrieval, or accepts manual paste or file upload. Consistent filename convention and metadata header applied to all transcripts.

**Post-interview debrief** (`/debrief`)
Calibrated debrief covering self-assessment accuracy, what landed and why, missed value opportunities, interviewer signals, Kate's read on what the interviewer walked away thinking, and specific prep priorities for the next round. Tracks patterns across multiple interviews — recurring issues are named as patterns, not treated as one-offs.

**Weekly monitoring** (`/setup-monitoring`, `/run-monitoring`)
Scheduled background task that searches for open roles at tracked companies, scans for company and people news, and checks user-defined industry topics. Writes results to a digest reviewed at session start. Watchlist includes funnel companies (auto-synced from application history), user-defined watchlist companies, Kate-suggested similar companies, key people, and industry topics.

**Session persistence**
Kate maintains context across sessions through structured files: coaching notes (running private log updated after every session), session context (handoff note with in-progress items, next actions, pending decisions, and time-sensitive flags), and application history (master log of all roles evaluated and pursued).

### Standing coaching rules
Pattern recognition, evidence quality calibration, motivation alignment, motivation answers, builder vs. operator positioning, red flag management, honest signal standard.

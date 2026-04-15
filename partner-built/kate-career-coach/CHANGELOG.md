# Kate — Changelog

---

## v0.4.2 — 2026-04-15

### Resume integrity rules (applied in both kate-coach and resume-tailor)

### New skill: resume-tailor

A dedicated resume tailoring skill (`skills/resume-tailor/`) for standalone resume
sessions outside of the full coaching workflow. Covers the complete tailoring workflow
(format extraction, JD analysis, gap analysis, section-by-section editing, pre-write
integrity check) with a focused rule set applied without exception.

### Resume integrity rules (applied in both kate-coach and resume-tailor)

**Never fabricate (new)**
Kate will not generate resume content that implies experience, responsibilities,
accomplishments, skills, or credentials the user has not documented. Gaps are flagged
explicitly — not bridged. Any phrasing that implies an unsupported claim is stopped
before it is written and confirmed with the user. This replaces the weaker "Overclaiming"
rule from prior versions, which flagged after the fact rather than before.

**Years of experience — omit for senior candidates (new)**
For candidates with 15 or more years of experience, Kate omits "X years of experience"
phrases from summaries, headlines, and body text by default. Aggregate year counts are a
vector for age discrimination. The rule is acknowledged once at session start; the user
can override explicitly. This is the default — no configuration required.

**Graduation dates — 15-year threshold (updated from 10 years)**
Graduation years are omitted from any degree awarded more than 15 years ago. Previously
the threshold was 10 years and was applied based on the most recent degree only. The rule
now applies per degree: dates older than 15 years are omitted; more recent dates are
retained. Omissions are always stated, never silent.

**Format preservation (new)**
Once a user has an established preferred resume format, Kate does not make structural or
visual changes without explicit direction. Minor pagination adjustments (spacing tweaks,
soft breaks, paragraph reflows that preserve visual structure) are acceptable at Kate's
discretion. Section reordering, font changes, layout restructuring, and any visually
noticeable change require user direction. Format changes that would improve the resume are
presented as suggestions, not actions.

### User profile — RESUME PREFERENCES section (new)

`user_profile.md` now includes a RESUME PREFERENCES section tracking: whether a
preferred format has been confirmed, format notes, and explicit records of any user
overrides on the experience-year-count and graduation-date defaults.

### What changed
- `skills/resume-tailor/SKILL.md` — new file
- `skills/kate-coach/references/flows.md` — Resume Optimization Flow rules updated: four
  new/updated rules replacing Graduation years (10→15, per-degree) and Overclaiming
- `skills/kate-coach/SKILL.md` — Detailed Flows section references resume-tailor skill
- `skills/kate-coach/references/templates/user_profile_template.md` — RESUME PREFERENCES
  section added
- `.claude-plugin/plugin.json` — version 0.3.2 → 0.4.0

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

# Kate — Changelog

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

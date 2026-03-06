# Kate — Career Coaching Assistant

Kate is a senior career coaching assistant for executive job searches. She draws on structured recruiting methodologies (GHSmart's Who method, Amazon's STAR framework, competency-based interviewing) to help candidates present themselves accurately and get hired at the right level.

Kate is warm and direct in equal measure. She does not manufacture encouragement. Her value is in telling you what polite friends won't.

---

## What Kate Does

- **Onboarding** — Builds your profile from your resume and LinkedIn, establishes your search parameters (roles, comp, constraints, motivation), and gives you an honest positioning read before you start applying
- **Fit Assessment** — Evaluates a job description against your profile and produces a Fit Tier (Target / Stretch / Reach), the strongest fit signals, and the key gaps
- **Resume Optimization** — Side-by-side resume editing with explicit justification for every change
- **Interview Prep** — Structured prep brief: interviewer research, company intel, talking points mapped to the JD, anticipated tough questions, red flags to get ahead of, and prioritized questions to ask
- **Transcript Capture** — Retrieves and files call transcripts after every recruiter or interviewer call (via Granola if connected, or by pasting/uploading)
- **Post-Interview Debrief** — Calibrated debrief covering what landed, what was missed, what the interviewer likely walked away thinking, and what to work on before the next round

Kate persists context across sessions through a structured file system. She tracks coaching patterns over time, flags open priorities, and connects dots the user may not see themselves.

---

## Getting Started

### 1. Create an empty folder

Create a folder for your job search anywhere on your computer (for example, `JobSearch/`). It can be completely empty — Kate sets up everything inside it on first run.

### 2. Open your folder in Cowork

Point Claude Cowork at your new folder.

### 3. Start a session

Say anything like "start a Kate session" or "I want to work on my job search." Kate will detect the empty folder, create the full project structure, and walk you through onboarding. No manual file setup needed.

### 4. Use commands for specific workflows

- `/fit-assessment` — evaluate a job description
- `/interview-prep` — generate an interview prep brief
- `/debrief` — run a post-interview debrief

---

## Granola Integration (Optional)

Kate supports automatic transcript retrieval via Granola. If you use Granola for meeting notes, connect it as an MCP connector in Claude Cowork settings. Kate will then retrieve and file transcripts from your recruiter and interviewer calls automatically.

If you don't use Granola, Kate will ask you to paste or upload transcripts manually. All functionality works either way.

---

## Folder Structure (Full)

```
JobSearch/
├── user/
│   ├── user_profile.md          — your search parameters and positioning
│   ├── coaching_notes.md        — Kate's running coaching log (private)
│   ├── application_history.md   — master log of all roles evaluated/pursued
│   └── session_context.md       — handoff note updated at end of each session
├── roles_evaluated/              — records for roles you decided not to pursue
├── [CompanyName]/
│   └── [RoleTitle]/
│       ├── job_description.md
│       ├── fit_assessment.md
│       ├── interview_prep.md
│       ├── post_interview_notes.md
│       ├── role_coaching_notes.md
│       └── Call Transcript - [Name] - [Company] - [YYYYMMDD].md
└── start_here.md                — optional: any notes for initializing Kate
```

---

## Notes

Kate writes certain files autonomously (coaching notes, application history, session context, fit assessments, role records). She will always ask for explicit confirmation before writing anything you would send to an employer — resumes, cover letters, or any document representing your voice to a third party.

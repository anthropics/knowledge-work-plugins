---
name: interview-prep
description: Generate a structured interview prep brief for an upcoming interview. Covers interviewer research, company intel, user positioning, talking points, anticipated tough questions, red flags to address proactively, and prioritized questions to ask.
allowed-tools:
  - Read
  - Write
  - Glob
  - WebSearch
---

Load the kate-coach skill and run the pre-interview prep flow.

1. Identify which interview this is for:
   - Company name and role
   - Interviewer name and role (if known)
   - Interview stage (phone screen / hiring manager / panel / executive / other)
   - Date and time (if known)

   If any of this is missing, ask for it before proceeding.

2. Read the relevant company/role folder if it exists: job description, fit assessment, prior call transcripts, and any role coaching notes.

3. Read `user/user_profile.md` to hold the user's full positioning context in active awareness.

4. Conduct interviewer and company research as needed (use web search for public information on the interviewer's background, the company's strategic situation, and any recent news).

5. Produce the full prep brief following the structure defined in `references/flows.md`:
   - Interviewer research
   - Company intel
   - User positioning for this specific interviewer and stage
   - Talking points mapped to JD requirements
   - Anticipated tough questions (with reasoning)
   - Red flags to address proactively
   - Questions to ask (prioritized)

6. Produce a separate call notes document formatted for use during the actual call — not a polished deliverable. Blank lines for notes. Same formatting conventions as the user's resume if available.

7. Save both documents to the company/role folder:
   - `[Company]/[Role]/interview_prep.md`
   - `[Company]/[Role]/call_notes_[YYYYMMDD].md`

8. Update `user/session_context.md` to note the prep is complete and the interview date.

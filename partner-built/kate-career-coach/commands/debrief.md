---
name: debrief
description: Run a structured post-interview debrief. Calibrates the user's self-assessment, identifies what landed and what didn't, reads interviewer signals, and feeds directly into next-round prep.
allowed-tools:
  - Read
  - Write
  - Glob
---

Load the kate-coach skill and run the post-interview debrief flow.

1. Identify which interview this is for:
   - Company name and role
   - Interviewer name and stage
   - Date of the interview

2. Before starting the debrief, collect two inputs from the user:
   - Their gut read on how it went (a few sentences — not a full recap)
   - The interview transcript or notes (via Granola if configured, otherwise ask the user to paste or upload)

   If transcript quality is limited, state what that limits before proceeding.

3. Read all relevant context from the company/role folder: job description, fit assessment, interview prep brief, prior call transcripts.

4. Run the structured debrief as defined in `references/flows.md`:
   - Self-assessment calibration (where the user's read is accurate, generous, or overly harsh)
   - What landed and why (specific, not generic)
   - Missed value opportunities (with concrete alternatives)
   - Interviewer signals (what questions and reactions actually indicate)
   - Kate's read on interviewer impressions
   - Next round preparation

5. Check `user/coaching_notes.md` for any patterns that surface again in this debrief. If a theme appears for the second or third time, name it explicitly as a pattern — not a one-off observation.

6. Save debrief notes to `[Company]/[Role]/post_interview_notes.md` autonomously.

7. Append any new coaching observations to `user/coaching_notes.md`.

8. Update `user/application_history.md` to reflect the current stage.

9. Ask: "Do you want me to start prep for the next round now, or are you waiting to hear back first?"

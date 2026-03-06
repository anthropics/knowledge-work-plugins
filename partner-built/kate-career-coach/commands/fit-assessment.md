---
name: fit-assessment
description: Run a structured fit assessment on a job description using Kate's methodology. Produces a Fit Tier (Target / Stretch / Reach), top fit signals, and key gaps. Required before resume optimization or interview prep.
allowed-tools:
  - Read
  - Write
  - Glob
---

Load the kate-coach skill and run the fit assessment flow.

1. If the user has not provided a job description, ask for it now. Accept it as pasted text or an uploaded file.

2. If no resume is available in the current session, ask the user to upload or paste it before proceeding. A fit assessment without a resume is incomplete.

3. Read `user/user_profile.md`. A role that technically matches the JD but violates the user's stated comp floor, geography constraint, work model preference, or primary motivation is not a clean Target. Flag any such misalignment explicitly as part of the assessment.

4. Run the structured fit assessment as defined in the kate-coach skill's `references/flows.md` — produce the Fit Tier, the two or three strongest fit signals, and the most significant gaps.

5. State the Fit Tier plainly. If it is a Reach, say so and explain why. If the Reach has no viable path, say that too.

6. Ask the user whether they want to proceed. Do not move to resume optimization or interview prep without an explicit decision from the user.

7. If the user decides to pursue the role, create the company/role folder and write `fit_assessment.md` autonomously. If the user decides not to pursue, create a `roles_evaluated/` record autonomously (asking one question about the decision first).

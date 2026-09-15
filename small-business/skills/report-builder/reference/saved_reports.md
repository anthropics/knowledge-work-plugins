# Saved Reports

Report definitions the owner has already built. **Read this file before asking any questions** — re-interviewing someone about a report they defined last month is the fastest way to make this skill feel broken.

Append a new entry after each Step 7. Never overwrite an entry; if a report changes, add a revision line beneath it with the date.

**When this file can't be written to, save the definition next to the owner's work instead.** In an installed runtime the skill folder is often read-only, so appending here fails. Don't drop the definition and don't pretend it saved. Write it to `report-definitions.md` in the working directory, and tell the owner exactly where it went and what to do with it:

> "Saved the definition to report-definitions.md in this folder. Keep that file with your reports — drop it back in the chat next time and I'll rerun this without asking you anything."

On the next run, check both places: this file first, then `report-definitions.md` in the working directory, then anything the owner attached.

---

## How to match a request to a saved report

Owners rarely use the report's exact name. Match on intent:

| Owner says | Match to |
|---|---|
| "run the weekly one" | The only report with weekly cadence, or ask which if several |
| "same as last time" | Most recently run report |
| "the Monday numbers" | Report whose cadence is Monday |
| "my sales report" | Report whose primary metric is sales |

If two or more reports plausibly match, list them by name and ask which — one short question, not a re-interview.

If nothing matches, treat it as a new report and go to Step 2.

---

## Entry format

```
### <Report name>
Created:   <YYYY-MM-DD>
Last run:  <YYYY-MM-DD>
Cadence:   <one-off | weekly | monthly | quarterly>

<the full spec, in the format from report_spec.md>

Revisions:
  <YYYY-MM-DD> — <what changed and why>
```

---

## Reports

*No saved reports yet. The first one gets appended here after its first run.*

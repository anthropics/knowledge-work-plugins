# Build Paths

Options in order of preference. Prefer the boring one — the owner cannot debug a clever integration that fails in November.

**There is no direct-API build path.** Even when a tool has a clean, documented REST API, do not hand-build a connector against it: that code becomes the business's to maintain — token plumbing, rate limits, silent vendor changes — and nobody here will maintain it. When the Claude connector directory has nothing, the build path is Zapier.

---

## 1. Existing Claude connector / MCP server

**When:** one exists in the Claude connector directory (or the MCP registry) and covers the need.

Always first choice. Someone else maintains it, it survives vendor API changes, and there is nothing custom to break.

Work: install, authenticate, verify scope. Usually minutes.

---

## 2. Zapier connection

**When:** nothing in the directory, and the tool is one of Zapier's 8,000+ apps. This is the build path when the directory has nothing; the mechanics are in `use-zapier.md`.

Good for: "when a work order is created, do X." Zapier handles the trigger and the plumbing.

Poor for: bulk historical pulls, or anything high-volume. Zapier bills per task and the arithmetic gets bad quickly.

**Say the cost out loud.** An owner who discovers a USD 70 monthly Zapier bill they didn't expect blames the integration, and they are not wrong to.

```
This works through Zapier. Roughly 40 tasks a day at your volume, which is
their USD 30 tier. Fine if that's worth it — worth knowing before we build.
```

---

## 3. Scheduled export

**When:** not in the directory and not on Zapier, but the system can email or drop a file on a schedule.

**Underrated.** No tokens to expire, no rate limits, no API changes. For a once-daily need it is often strictly better than a live integration.

Set up:

1. Configure the export in the source system — daily, to a specific address
2. Watch that inbox for the file
3. Parse and use it

The main weakness is latency. A daily export cannot support anything needing same-hour data. Say so rather than letting the owner discover it.

**The failure mode is quiet.** If the export stops arriving, nothing errors — the data just goes stale. Build in a check: if no file has arrived in longer than the expected interval, say so loudly.

---

## 4. Screen-level workaround

**When:** everything else failed and the need is real.

Fragile by nature. It breaks whenever the vendor changes their interface, which they do without warning.

Only appropriate when:

- The data genuinely cannot be reached another way
- The need is significant enough to justify the maintenance
- The owner understands it will break, and roughly how often

Say it plainly:

```
This would work, but it's held together with tape — any interface change on
their side breaks it, and you'd have no warning beyond the data stopping.

Before we go there: can you export this manually once a week? Less clever,
but it'll still work next year.
```

Recommending the manual export over the fragile automation is usually the right call, and owners respect being told.

---

## Choosing when several work

| Priority | Reasoning |
|---|---|
| Fewest moving parts | Every component is something that can break unmonitored |
| Nothing to maintain | The owner cannot debug it and will not pay someone to |
| Fails loudly | Silent failure is worse than no connector |
| Read-only where possible | Narrower access, smaller consequences |
| No per-task cost | Unless the owner has agreed to it |

**A daily CSV that always works beats a live API that breaks quarterly.** The owner's actual requirement is that their morning brief is right, not that the integration is elegant.

---

## Scoping the build

Whatever the path, build only what was scoped.

```
Bad:  Connect ServiceTrade.
Good: Pull open work orders daily, with customer, description, and assignee,
      so they appear in the morning brief.
```

The second is buildable this afternoon and testable against a known answer. The first is a project with no definition of done.

More endpoints can be added when something needs them. Building the whole API surface up front means securing and maintaining code nothing uses.

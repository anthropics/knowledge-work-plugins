---
description: Structured debugging session — reproduce, isolate, diagnose, and fix
argument-hint: "<error message or problem description>"
---

# /debug

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Run a structured debugging session to find and fix issues systematically.

## Usage

```
/debug $ARGUMENTS
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                       DEBUG                                        │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: REPRODUCE                                                │
│  ✓ Understand the expected vs. actual behavior                   │
│  ✓ Identify exact reproduction steps                             │
│  ✓ Determine scope (when did it start? who is affected?)        │
│                                                                    │
│  Step 2: ISOLATE                                                   │
│  ✓ Narrow down the component, service, or code path             │
│  ✓ Check recent changes (deploys, config changes, dependencies) │
│  ✓ Review logs and error messages                                │
│                                                                    │
│  Step 3: DIAGNOSE                                                  │
│  ✓ Form hypotheses and test them                                 │
│  ✓ Trace the code path                                           │
│  ✓ Identify root cause (not just symptoms)                      │
│                                                                    │
│  Step 4: FIX                                                       │
│  ✓ Propose a fix with explanation                                │
│  ✓ Consider side effects and edge cases                          │
│  ✓ Suggest tests to prevent regression                           │
└─────────────────────────────────────────────────────────────────┘
```

## What I Need From You

Tell me about the problem. Any of these help:
- Error message or stack trace
- Steps to reproduce
- What changed recently
- Logs or screenshots
- Expected vs. actual behavior

## Output

```markdown
## Debug Report: [Issue Summary]

### Reproduction
- **Expected**: [What should happen]
- **Actual**: [What happens instead]
- **Steps**: [How to reproduce]

### Root Cause
[Explanation of why the bug occurs]

### Fix
[Code changes or configuration fixes needed]

### Prevention
- [Test to add]
- [Guard to put in place]
```

## If Connectors Available

If **~~monitoring** is connected:
- Pull logs, error rates, and metrics around the time of the issue
- Show recent deploys and config changes that may correlate

If **~~source control** is connected:
- Identify recent commits and PRs that touched affected code paths
- Check if the issue correlates with a specific change

If **~~project tracker** is connected:
- Search for related bug reports or known issues
- Create a ticket for the fix once identified

## Tips

1. **Share error messages exactly** — Don't paraphrase. The exact text matters.
2. **Mention what changed** — Recent deploys, dependency updates, and config changes are top suspects.
3. **Include context** — "This works in staging but not prod" or "Only affects large payloads" narrows things fast.

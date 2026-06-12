---
description: Audit Google Meet activity, recordings, and external participants
argument-hint: "[optional: focus area, e.g. 'recordings only' or 'external participants']"
---

# /gw-meet-audit

Review Google Meet activity for the last 30 days — meeting hosts, recordings started, and external participants joining school meetings. Useful for compliance, FERPA review, and usage reporting.

## Usage

```
/gw-meet-audit
/gw-meet-audit recordings only
/gw-meet-audit check for external participants
```

## What it does

- Queries the Admin SDK Meet audit log for the last 30 days
- Captures meeting end events (host, duration, participant count)
- Captures recording start events (who started a recording and for which meeting)
- Flags external participants (non-domain accounts) who joined meetings
- Generates a 3-tab Excel report: Meetings, Recordings, External Participants
- Provides FERPA guidance on recording consent and external participant policies

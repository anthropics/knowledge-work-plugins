# Gotchas

Known failure modes for the business-pulse skill. Good / Bad pairs.

---

## Gotcha: QuickBooks returns unexpected state

**Why it matters:** QuickBooks can return empty results, a sync-in-progress state, or an auth error without throwing a hard exception. Treating silence as "no data" causes the pulse to skip Cash entirely without telling the owner — they assume their business has no QuickBooks data.

### ✗ Bad

```
Claude: [QuickBooks returns empty response]
        → skips Cash section silently
        → pulse presents no cash data; owner assumes QB isn't connected
```

The owner spends 10 minutes reconnecting QuickBooks before realizing it was always connected — just in a transient state.

### ✓ Good

```
Claude: [QuickBooks returns empty response or error]
        → Cash section header present with: "n/a — QuickBooks unavailable (sync error or auth required)"
        → "Sources unavailable: QuickBooks — returned empty response" in appendix
```

The owner sees the gap explicitly and can decide whether to reconnect or proceed with a partial pulse.

---

## Gotcha: Gmail auth failure mid-pulse

**Why it matters:** Gmail auth is intermittently flaky in workshop environments. Surfacing a raw auth error in the middle of the pulse looks broken and breaks the owner's trust in the skill.

### ✗ Bad

```
Claude: [Gmail auth error mid-composition]
        → "Error: Gmail authentication failed. Please re-authenticate."
        → pulse output stops or shows raw error in Watch List section
```

The owner sees a broken tool, not a useful briefing.

### ✓ Good

```
Claude: [Gmail auth error]
        → continues pulse without Watch List section
        → appendix: "Gmail — auth error; Watch List unavailable this run"
        → all other sections unaffected
```

The pulse still delivers value. The owner is informed, not alarmed.

---

## Gotcha: Asking permission before pulling data

**Why it matters:** The skill's core value is doing the work without prompting. An owner who invoked the pulse already implicitly approved the data pull. Asking "should I check QuickBooks?" or "can I read your emails?" defeats the purpose and erodes trust in the skill as an autonomous assistant.

### ✗ Bad

```
Owner: "catch me up on the business"
Claude: "Should I check QuickBooks for your cash balance? And is it okay to look at your HubSpot pipeline?"
```

Three more round trips before anything useful is delivered.

### ✓ Good

```
Owner: "catch me up on the business"
Claude: [immediately dispatches all parallel tool calls]
        → presents pulse in one response
```

---

## Gotcha: Slack write requires explicit confirmation

**Why it matters:** Slack write is not tested in the standard validation path and posts to channels other people can see. Auto-posting without confirmation could embarrass the owner or spam a team.

### ✗ Bad

```
Claude: [at end of pulse]
        "I've posted this to #general."
```

Owner never asked for a Slack post; now the whole team has the financial data.

### ✓ Good

```
Claude: [at end of pulse]
        "Want me to post this to Slack? If so, which channel?"
```

Slack write only happens with a specific "yes + channel name" from the owner. Never assume.

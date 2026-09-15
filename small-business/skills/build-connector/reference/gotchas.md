# Gotchas

Failure modes. Several of these are security issues, and the owner will not be thinking about any of them.

---

## Gotcha: asking the owner to paste a password

**Why it matters:** The most serious failure in this skill. A password in a conversation is a credential in a place it was never meant to be, and it usually grants far more access than the integration needs.

### Bad

```
What's your ServiceTrade login? I'll set up the connection.
```

### Good

```
This needs a read-only API token, not your login. Create one under
Settings → API, then add it through the connector settings — don't paste it
here.
```

Tokens and OAuth only. If a system offers nothing but password auth, say so and let the owner decide with that knowledge rather than working around it.

Whatever the credential type, it goes into the platform's own credential storage — never into a file, a prompt, or a URL.

---

## Gotcha: using the owner's own login instead of a dedicated integration user

**Why it matters:** Access tied to the owner's personal login can't be revoked later without locking them out of their own account.

### Bad

Connect the integration using the owner's own username and password, or their personal OAuth session, because it's the account already sitting in front of them.

### Good

Where the platform supports it, create a dedicated integration user (or a scoped token tied to one) for the connector instead. Access can be revoked later without touching the owner's own login.

---

## Gotcha: creating a connector before saying what it reaches

**Why it matters:** An owner who doesn't know what a connector can see or do before it's created can't meaningfully say yes to it.

### Bad

Connect first, mention the scope only if asked.

### Good

```
The Zapier connection needs ServiceTrade connected inside your Zapier
account. It'll see work orders and customers. It can't change anything or
see billing.

Connect it in Zapier under Apps → ServiceTrade — sign in there directly,
don't paste any password here.
```

---

## Gotcha: requesting more access than the job needs

**Why it matters:** A connector with write access to the system of record can do damage the owner has no way to reverse or even notice.

### Bad

Request full access because it is simpler than working out the minimum.

### Good

```
Read-only is enough for this — it only needs to see work orders. If you later
want it creating them, that's a separate change and I'd add approval gates.
```

Narrow scope, stated in plain terms, before anything is created.

---

## Gotcha: building before checking

**Why it matters:** An hour spent building something that already existed is an hour the owner paid for nothing.

### Bad

Start creating a Zapier connection immediately — or worse, start writing custom code against the tool's REST API.

### Good

Check the Claude connector directory and MCP registry first, then Zapier, then scheduled exports. Report the finding, then build — and the build is the Zapier connection, never hand-written API code.

---

## Gotcha: an unbounded scope

**Why it matters:** "Connect my ERP" has no definition of done. It becomes a project, stalls, and the owner concludes the whole capability doesn't work.

### Bad

Accept "connect my ERP" as the requirement.

### Good

```
What would you do with it first? If it's "see open work orders in my morning
brief," that's buildable this afternoon. The whole system is a bigger
conversation.
```

Start with one endpoint that unblocks one thing.

---

## Gotcha: not checking the plan tier

**Why it matters:** API access is frequently gated to higher subscription tiers. Building against an API the owner cannot use is a wasted afternoon, and it happens often.

### Bad

Read the docs, build the connector, discover at test time that the token endpoint returns 403.

### Good

```
One thing before I build: ServiceTrade puts API access on Pro and above.
Which plan are you on?
```

---

## Gotcha: overselling reliability

**Why it matters:** A custom connector is not a first-party integration. An owner who thinks it is will not investigate when their data quietly goes stale.

### Bad

```
All set — ServiceTrade is connected.
```

### Good

```
Connected. Worth knowing how this breaks:
  - The token expires in 90 days. I'll flag it before then.
  - If they change their API, this stops working. No warning from their side.
  - If work orders ever show as zero and that seems wrong, it's probably this,
    not your data.
```

The third line is the important one. It teaches the owner to recognize the failure instead of trusting a wrong answer.

---

## Gotcha: silent failure

**Why it matters:** A connector that stops working without saying so produces confidently wrong output. The morning brief shows no open work orders and the owner believes it.

### Bad

Return an empty result when the fetch fails.

### Good

Distinguish "no records" from "could not fetch," and surface the second:

```
Work orders: unavailable — ServiceTrade returned an auth error. This is a
connector problem, not an empty queue.
```

For scheduled exports, check the file's age. If it is older than the expected interval, say so.

---

## Gotcha: a write connector with no approval gate

**Why it matters:** A connector that can modify the system of record unattended can do damage nobody notices for weeks.

### Bad

Build write access because the owner asked for it, with no gate.

### Good

Every write is gated, and the gate states what will change:

```
This would mark WO-4471 complete and set the close date to today.
Confirm?
```

This holds regardless of what the owner requested. It is not a preference.

---

## Gotcha: a surprise Zapier bill

**Why it matters:** Zapier bills per task. An owner who discovers a USD 70 monthly charge blames the integration, and they are right to.

### Bad

Build the Zapier connection, mention nothing about cost.

### Good

```
This runs through Zapier — about 40 tasks a day at your volume, which is
their USD 30 tier. Fine if it's worth it, but worth knowing first.
```

---

## Gotcha: choosing clever over boring

**Why it matters:** The owner cannot debug anything. A clever integration that breaks in November is worse than a dull one that never does.

### Bad

Build a screen-level workaround because it is more automatic than a weekly export.

### Good

```
I could automate this by driving their web interface, but it'd break any time
they change the page and you'd get no warning.

Can you export the CSV once a week instead? Less clever, still working next
year.
```

Recommending the manual step is often the right call, and owners respect being told which is which.

# Commands vs Skills: Understanding the Difference

This document clarifies the distinction between **commands** and **skills** in Claude plugins, addressing common confusion about their overlap and relationship.

## Quick Summary

| Aspect               | Commands                       | Skills                           |
| -------------------- | ------------------------------ | -------------------------------- |
| **Invocation**       | Explicit (`/plugin:command`)   | Automatic (contextual)           |
| **Purpose**          | Define _what_ to do            | Define _how_ to do it            |
| **User interaction** | User triggers directly         | Claude retrieves when relevant   |
| **Content focus**    | Workflow steps, inputs/outputs | Domain expertise, best practices |
| **File location**    | `commands/*.md`                | `skills/*/SKILL.md`              |

## Commands: Explicit Actions

Commands are **explicit actions** that users trigger with slash commands.

### What Commands Contain

- **Step-by-step workflow** — The sequence of actions to perform
- **Input expectations** — What the user should provide
- **Output format** — How results should be structured
- **Tool interactions** — Which MCP connections to use

### Example: `/legal:review-contract`

```markdown
---
description: Review a contract against your organization's negotiation playbook
argument-hint: "<contract file or text>"
---

# /review-contract

## Workflow

### Step 1: Accept the Contract

Accept the contract in any of these formats:

- File upload: PDF, DOCX, or other document format
- URL: Link to a contract in your CLM or cloud storage
- Pasted text: Contract text pasted directly

### Step 2: Gather Context

Ask the user for context before beginning the review:

1. Which side are you on? (vendor, customer, etc.)
2. Deadline: When does this need to be finalized?
   ...
```

**Key observation**: Commands tell Claude _what steps to follow_.

---

## Skills: Domain Knowledge

Skills provide **domain expertise** that Claude draws on automatically when relevant.

### What Skills Contain

- **Domain knowledge** — Terminology, concepts, best practices
- **Expert guidance** — How to approach specific situations
- **Classification criteria** — How to categorize or evaluate things
- **Reference material** — Supporting documentation

### Example: `legal/skills/contract-review`

```markdown
---
name: contract-review
description: Review contracts against your organization's negotiation playbook...
---

# Contract Review Skill

You are a contract review assistant for an in-house legal team...

## Common Clause Analysis

### Limitation of Liability

**Key elements to review:**

- Cap amount (fixed dollar amount, multiple of fees, or uncapped)
- Whether the cap is mutual or applies differently to each party
- Carveouts from the cap (what liabilities are uncapped)
  ...

## Deviation Severity Classification

### GREEN -- Acceptable

The clause aligns with or is better than the organization's standard position...

### YELLOW -- Negotiate

The clause falls outside the standard position but within a negotiable range...

### RED -- Escalate

The clause falls outside acceptable range or triggers a defined escalation criterion...
```

**Key observation**: Skills tell Claude _how to think about the domain_.

---

## Why They Overlap (And That's Intentional)

Issue #5 correctly observes that commands and skills often cover similar ground. This is **by design**:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INVOKES COMMAND                      │
│                    /legal:review-contract                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                COMMAND (Workflow)                            │
│  "Step 1: Accept contract. Step 2: Gather context..."       │
│                                                              │
│  Claude follows these explicit steps                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Claude automatically retrieves
                              │ relevant domain knowledge
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                SKILL (Expertise)                             │
│  "When reviewing Limitation of Liability clauses,            │
│   look for: cap amount, carveouts, mutual vs unilateral..."  │
│                                                              │
│  Claude uses this expertise while executing the command      │
└─────────────────────────────────────────────────────────────┘
```

### The Command Needs Context

Without the skill, the command would say "analyze each clause" but Claude wouldn't know:

- What makes a good vs bad liability cap
- How to classify deviations (GREEN/YELLOW/RED)
- What redline language to suggest

### The Skill Needs Structure

Without the command, the skill provides expertise but not:

- When to apply it (explicit user intent)
- What order to follow
- What output format to produce

---

## How Claude Uses Both Together

1. **User invokes command**: `/legal:review-contract`
2. **Claude reads command file**: Gets the workflow steps
3. **Claude retrieves relevant skills**: Based on the command's domain
4. **Claude executes workflow**: Uses skill knowledge to inform each step
5. **Output follows command format**: Structure from command, intelligence from skill

Skills within a plugin are **scoped to that plugin**. When you invoke `/legal:review-contract`, Claude has access to all skills in the `legal` plugin, not skills from `sales` or `marketing`.

---

## Practical Guidelines for Contributors

### When to Create a Command

- User needs to trigger a specific action
- There's a defined workflow with inputs/outputs
- The action should appear in slash command suggestions

### When to Create a Skill

- Domain expertise that applies across multiple commands
- Best practices Claude should know but users don't explicitly request
- Classification criteria, terminology, or specialized knowledge

### When You Need Both

Most features need both:

| Command (the "what") | Skill (the "how")                           |
| -------------------- | ------------------------------------------- |
| `/analyze`           | `data-exploration`, `statistical-analysis`  |
| `/review-contract`   | `contract-review`                           |
| `/call-prep`         | `account-research`, `discovery-methodology` |

### Avoiding Duplication

- **Commands**: Focus on workflow orchestration
- **Skills**: Focus on domain knowledge
- If content appears in both, ask: "Is this a step (command) or expertise (skill)?"

---

## Related Documentation

- [Architecture](./ARCHITECTURE.md) — Overall plugin structure
- [README](../README.md) — Getting started guide

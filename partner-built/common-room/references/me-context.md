# The `Me` Object — User Context Guide

## What `Me` Is

The `Me` object in Common Room represents the currently authenticated user. Fetching it at the start of a session gives the LLM context to personalize outputs and scope queries correctly.

Always fetch `Me` before running account research, prospecting, or any workflow that should be scoped to the user's territory.

## What `Me` Returns

### User Profile
- Login identifier (email or username)
- Full name and display name
- Job title and role
- Persona in CR (e.g., AE, SDR, CSM, Manager)
- All linked profiles (e.g., Salesforce user ID, LinkedIn handle)

### User Segments ("My Segments")
- A list of all segments that belong to this user (name and segment ID each)
- Corresponds to the **"My Segments" tab** in the Common Room product

## How to Use `Me` Context

### 1. Scope queries and respect territory boundaries
When running account research, prospecting, or generating briefings, filter results to the user's own segments unless they ask for a broader view.

> Default: "Show me accounts showing buying signals" -> scope to My Segments
> Override: "Show me all accounts in the workspace showing buying signals" -> remove segment scope

If a user asks about an account not in their segments, note: "This account doesn't appear to be in your segments — would you still like me to research it?"

### 2. Personalize outreach and briefings
Use the user's name, title, and role to personalize outputs — e.g., reference their territory in a weekly brief, use their name in drafted emails.

### 3. Infer context for reasoning
The user's Persona in CR influences how outputs should be framed:
- **AE / AM / Account Executive / Account Manager** — focus on pipeline, deals, expansion, close timelines
- **SDR / BDR / Sales Development Representative / Business Development Representative** — focus on prospecting, warm signals, first-touch outreach
- **CSM / Customer Success Manager** — focus on health, retention, expansion, champion engagement
- **Manager / Director / VP** — focus on team-level trends, not individual outreach

---
name: customer-360
license: MIT
description: >
  Build a comprehensive customer profile from Intercom data, including
  conversation history, account context, and interaction timeline. Use when
  the user asks to "look up a customer", "customer profile", "customer 360",
  "tell me about this customer", "summarize a customer's history", or provides
  a customer email or company name and wants a full picture.
disable-model-invocation: true
argument-hint: "[email or company name]"
---

# Customer 360

Produce a comprehensive customer profile by aggregating data from across the Intercom workspace.

## Workflow

### Step 1: Identify the Customer
- Parse the user's input for an email, name, or company
- Use `search_contacts` to find the contact (by email is most reliable)
- If company name given, search contacts by email domain
- Use `get_contact` to fetch the full profile (attributes, tags, segments, companies)

### Step 2: Gather Conversation History
- Use `search_conversations` filtered to this contact's conversations
- Paginate to get all conversations (not just the first page)
- For the most recent/relevant conversations, use `get_conversation` for full threads

### Step 3: Build the Profile
Produce a markdown profile with these sections:

#### Contact Summary
- Name, email, role (user/lead), company
- Location, timezone, last seen
- Plan/tier (if available via custom attributes)
- Tags and segments

#### Conversation History
- Total conversation count
- Table: ID | Subject | State | Channel | Date
- Highlight any currently open/snoozed conversations

#### Key Themes
- Common topics across conversations
- Recurring issues or feature requests
- Sentiment signals (escalations, positive feedback)

#### Timeline
- Chronological list of significant interactions
- First contact → most recent activity

#### Open Items
- Unresolved conversations
- Pending questions or follow-ups

### Step 4: Present and Offer Next Steps
- Present the profile
- Offer to dive deeper into any conversation
- Offer to search for similar customers (same company, same issues)

## Best Practices
- Always cite conversation IDs so the user can find them in the Intercom inbox
- Note data freshness — states may have changed since events occurred
- If the contact has many conversations, summarize the most recent 10-15 and note the total count
- Handle cases where the contact exists but has no conversations

## Troubleshooting

### Contact Not Found
Symptom: No results for the provided email or name.
Solution: Check for typos. Try searching by email domain to find related contacts. Ask the user to confirm the identifier.

### Too Many Conversations
Symptom: Contact has 50+ conversations, making full analysis impractical.
Solution: Focus on the most recent 10-15 conversations. Summarize older ones by theme rather than individually. Note the total count.

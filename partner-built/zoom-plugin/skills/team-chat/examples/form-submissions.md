# Form Submissions (Chatbot API)

Forms inside cards can collect user input; submissions arrive via webhook.

## Pattern

1. Send a card with form fields.
2. Receive `chat_message.submit` webhook.
3. Validate inputs and respond with an updated card or confirmation message.

## Pitfalls

- Always validate types (dates, numbers) server-side.
- Treat submitted text as untrusted input.


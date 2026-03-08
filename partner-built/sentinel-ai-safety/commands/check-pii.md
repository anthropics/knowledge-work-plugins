---
description: "Check text for personally identifiable information and provide redacted version"
---

Check the provided text for personally identifiable information (PII).

Detect these PII types:
- Email addresses
- Social Security Numbers (SSNs)
- Credit card numbers (with Luhn validation)
- Phone numbers
- API keys and tokens

For each PII item found, report the type and risk level. Provide a redacted version with PII replaced by type labels (e.g., [EMAIL], [SSN], [CREDIT_CARD]).

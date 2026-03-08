# Sentinel AI Safety Plugin

Real-time safety scanning for Claude Cowork conversations. Detects prompt injection, PII leaks, harmful content, toxicity, and compliance violations — with sub-millisecond latency and zero external dependencies.

## Features

- **PII Detection & Redaction**: Automatically detects emails, SSNs, credit cards, phone numbers, and API keys
- **Prompt Injection Detection**: Catches injection attempts in 12 languages plus cross-lingual attacks
- **Compliance Scanning**: Check content against custom blocked terms and organizational policies
- **Content Safety**: Harmful content and toxicity detection for external-facing communications

## Use Cases

- **Customer Support**: Scan agent responses before sending to customers to prevent PII leaks
- **Legal & HR**: Check documents for sensitive data before sharing externally
- **Sales & Marketing**: Ensure outbound content doesn't contain harmful or off-brand language
- **Operations**: Compliance checks against organizational policies and blocked terms

## Commands

- `/sentinel-ai:scan` — Scan text for all safety issues
- `/sentinel-ai:check-pii` — Check for PII and get redacted version
- `/sentinel-ai:check-safety` — Quick safety assessment

## Installation

```
pip install sentinel-guardrails
```

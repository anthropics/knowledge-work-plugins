# Zoom Phone High-Level Scenarios

## 1) Smart Embed CRM Softphone

Use Smart Embed in a CRM sidebar to place and receive calls, then log outcomes back into CRM records.

## 2) Click-to-Call from Lead Table

Use `zp-make-call` or URI scheme launch from contact rows; subscribe to call status events for UI updates.

## 3) SMS Follow-Up Automation

Use `zoomphonesms://` and Smart Embed SMS events to trigger follow-up tasks and SLA timers.

## 4) Call Disposition + Notes Pipeline

Use `zp-save-log-event` and `zp-notes-save-event` to capture custom dispositions and sync to third-party systems.

## 5) Real-Time Supervisor Dashboard

Use `phone.*` webhooks and call events to track active calls, misses, rejects, and queue pressure.

## 6) Call History Modernization

Migrate from legacy call log fields to call history/call element IDs while maintaining backward compatibility for old records.

## 7) Call Handling Admin Automation

Use call handling APIs to standardize business/closed/holiday routing for users, auto receptionists, and call queues.

## 8) Blended Phone + Contact Center Journey

Route phone interactions into Contact Center follow-up or escalation workflows using shared CRM context.

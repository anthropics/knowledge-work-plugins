# Rate Limits

Rate limits vary by endpoint and account. If you get throttled:

- add retries with exponential backoff
- batch work where possible
- avoid calling list endpoints repeatedly (cache results)


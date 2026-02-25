# Sample Data Breach Incident — For Testing /brief incident

## Incident Context

**Company**: KundenCo AG, Paradeplatz 8, 8001 Zürich
**Discovery**: Dienstag, 18. Februar 2026, 23:47 Uhr (MEZ)
**Discovered by**: Pascal Steiner, Head of IT Security

---

## Known Facts at Time of Discovery

### What happened
At 23:47 on Tuesday 18 February 2026, KundenCo AG's SIEM system (hosted by TechVendor AG in
their US-based data centre) triggered an alert for anomalous data exfiltration from the
production database. Initial forensic review by the on-call engineer (Pascal Steiner)
confirmed that an unauthorised third party had accessed the production database between
14:00 and 23:30 on 18 February 2026 — approximately 9.5 hours.

### Data confirmed or suspected compromised

**Confirmed exfiltrated (log evidence):**
- Full name, email address, postal address, date of birth: 47,000 customer records
- IBAN and account numbers (partial — last 4 digits masked in logs, but full numbers
  potentially in unmasked database tables): estimated 12,000 records
- Login credentials (email + bcrypt password hash): 47,000 records
- Internal employee directory: 312 employees (name, title, internal email, mobile number)

**Suspected but unconfirmed:**
- Health insurance data for approximately 800 corporate clients processed via
  KundenCo AG's HR platform module (besonders schützenswerte Personendaten per Art. 5 lit. c nDSG)
- Tax identification numbers (AHV-Nummer / Sozialversicherungsnummer) for employees in the payroll module

### Attack vector (preliminary)
A SQL injection vulnerability in TechVendor AG's recently deployed API update
(deployed 17 February 2026) appears to be the entry point. The vulnerability was
in a publicly accessible endpoint. No prior detection; first alert at 23:47.

### Affected systems
- Production CRM database (Microsoft Azure, region: East US)
- HR platform module (same Azure environment)
- Authentication database

### Data subjects affected
- Swiss residents: ~38,000 estimated
- EU residents (Germany, France, Austria): ~9,000 estimated
- Other: ~312 employees (Swiss-based)

### Current status at time of incident brief request
- Attack vector: patched by TechVendor AG at 01:15, 19 February 2026
- Database: taken offline at 00:30, 19 February 2026; not yet restored
- Forensic investigation: ongoing (TechVendor AG internal + KundenCo AG IT)
- Outside counsel: not yet engaged
- Insurers: not yet notified
- FDPIC: not yet notified
- Any EU supervisory authority: not yet notified
- Affected individuals: not yet notified
- Internal communications: Slack thread in #it-security channel (potentially accessible
  to all 312 employees)
- Media: no contact yet; situation not yet public
- Time since discovery: 4 hours 13 minutes (brief requested at 04:00, 19 February 2026)

---

## Internal Communications Snapshot (from Slack #it-security)

> **Pascal Steiner** [23:47]: "Alert from SIEM — looks like we have a live breach on prod DB.
> Pulling logs now."

> **Pascal Steiner** [00:12]: "Confirmed. SQL injection via the new TechVendor API.
> Data going out since 14:00 today. 47k customer records minimum. Possibly IBANs and health data."

> **Lea Keller (CTO)** [00:18]: "How is this possible?? TechVendor just deployed yesterday.
> Did we test this?"

> **Pascal Steiner** [00:22]: "No pen test was done before deployment per TechVendor.
> They said it was a minor update."

> **Lea Keller** [00:31]: "Taking DB offline now. Do NOT tell anyone outside this channel yet.
> We need to assess before this gets out."

> **Marco Bernasconi (CFO)** [01:45]: "What's our GDPR exposure here? Can we keep this quiet?"

> **Lea Keller** [02:10]: "Legal needs to know. Who's calling Sabine [General Counsel]?"

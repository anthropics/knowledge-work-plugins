---
name: m365-mfa-audit
description: >
  Run a Microsoft 365 MFA compliance audit against any Entra ID / Azure AD security group.
  Use this skill whenever any IT admin wants to check MFA registration status,
  find users missing MFA, run a monthly or quarterly compliance check, enforce MFA via
  Conditional Access, protect shared accounts from lockout, or export MFA reports for
  leadership. Triggers on: "MFA audit", "who doesn't have two-factor", "MFA compliance",
  "run the MFA report", "check MFA for faculty", "enforce two-factor", "find accounts
  without MFA", "shared account MFA", "Conditional Access MFA policy", or any request
  involving MFA registration status in Microsoft 365.
---

# M365 MFA Audit Skill

This skill guides you through a full Microsoft 365 MFA compliance audit using the
Microsoft Graph API — no additional tools or admin portals required.

---

## Step 1 — Get the Bearer Token

All Graph API calls need a bearer token from an active Entra admin session.

**Ask the user to do this in their browser:**
1. Open [https://entra.microsoft.com](https://entra.microsoft.com) and sign in as a Global Admin
2. Open DevTools → Console (F12 → Console tab)
3. Paste this command and press Enter:
   ```javascript
   Object.keys(sessionStorage).filter(k => k.includes('accesstoken')).forEach(k => { try { let t = JSON.parse(sessionStorage[k]); if(t.target && t.target.includes('graph.microsoft.com')) console.log('TOKEN:', t.secret.substring(0,50) + '...', '\nFULL:', t.secret); } catch(e){} });
   ```
4. Copy the long token string (starts with `eyJ`) and paste it in the chat

**Save the token:**
```python
token = "eyJ..."   # from user
with open('/tmp/ms_token.txt', 'w') as f:
    f.write(token.strip())
```

Tokens from Entra typically last 60–90 minutes, but session tokens can last up to 24 hours.
If you get a 401 error mid-audit, ask the user to refresh their token.

---

## Step 2 — Find the Target Security Group

The user will name a group (e.g., "All Faculty and Staff"). Don't assume you know the
exact display name — **always search first**, because group names often have underscores,
special characters, or unexpected casing (e.g., "All_Faculty and Staff" not "All Faculty").

```python
import urllib.request, urllib.parse, json

with open('/tmp/ms_token.txt') as f:
    token = f.read().strip()
headers = {'Authorization': f'Bearer {token}'}

# Search broadly — don't assume exact name
search_term = "Faculty"  # or whatever keyword the user provides
url = f"https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,'{search_term}')&$select=id,displayName,description"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    groups = json.loads(resp.read())['value']
    for g in groups:
        print(f"  {g['displayName']}  →  {g['id']}")
```

Show the user the results and confirm which group to use before continuing.

---

## Step 3 — Pull Group Members

```python
GROUP_ID = "..."   # confirmed group ID

members = []
url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members?$select=id,displayName,userPrincipalName,accountEnabled&$top=999"
while url:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    members.extend(data.get('value', []))
    url = data.get('@odata.nextLink')  # handle pagination

print(f"Found {len(members)} members")
```

---

## Step 4 — Pull MFA Registration Data

```python
# Get all users' auth method registration status
mfa_url = "https://graph.microsoft.com/v1.0/reports/authenticationMethods/userRegistrationDetails?$top=999"
mfa_records = {}

while mfa_url:
    req = urllib.request.Request(mfa_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    for record in data.get('value', []):
        mfa_records[record['id']] = record
    mfa_url = data.get('@odata.nextLink')

print(f"Fetched MFA data for {len(mfa_records)} users")
```

---

## Step 5 — Cross-Reference and Categorize

```python
from datetime import datetime

registered = []
not_registered = []
disabled = []

for member in members:
    uid = member['id']
    if not member.get('accountEnabled', True):
        disabled.append(member)
        continue

    mfa = mfa_records.get(uid, {})
    is_capable = mfa.get('isMfaCapable', False)
    is_registered = mfa.get('isMfaRegistered', False)
    methods = mfa.get('methodsRegistered', [])

    entry = {
        'Name': member['displayName'],
        'UPN': member['userPrincipalName'],
        'MFA Registered': 'Yes' if is_registered else 'No',
        'MFA Capable': 'Yes' if is_capable else 'No',
        'Methods': ', '.join(methods) if methods else 'None'
    }

    if is_registered:
        registered.append(entry)
    else:
        not_registered.append(entry)
```

---

## Step 6 — Export CSVs and Print Summary

```python
import csv, os

today = datetime.now().strftime('%Y%m%d')
output_dir = "."  # Update to your preferred reports folder

# Missing MFA
missing_path = f"{output_dir}/{today}_MFA_Missing.csv"
if not_registered:
    with open(missing_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=not_registered[0].keys())
        writer.writeheader()
        writer.writerows(not_registered)

# All accounts
all_path = f"{output_dir}/{today}_MFA_All_Accounts.csv"
all_rows = registered + not_registered
with open(all_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
    writer.writeheader()
    writer.writerows(all_rows)

total_active = len(registered) + len(not_registered)
pct = round(len(registered) / total_active * 100, 1) if total_active else 0

print(f"\n{'='*50}")
print(f"  MFA COMPLIANCE REPORT — {today}")
print(f"{'='*50}")
print(f"  Total active members : {total_active}")
print(f"  MFA registered       : {len(registered)} ({pct}%)")
print(f"  MFA missing          : {len(not_registered)} ({100 - pct}%)")
print(f"  Disabled accounts    : {len(disabled)}")
print(f"\n  Files saved:")
print(f"  All accounts : {all_path}")
if not_registered:
    print(f"  Missing MFA  : {missing_path}")
```

---

## Step 7 (Optional) — Enforce MFA via Conditional Access

If the user wants to enforce MFA after the audit:

### 7a — Protect Shared Accounts First

Before enforcing, find any shared or functional accounts in the missing list (e.g.,
daycare@, office@, media@) and exclude them from enforcement to avoid service disruption.

Create an exclusion group:
```python
group_payload = {
    "displayName": "Shared Accounts - MFA Excluded",
    "mailEnabled": False,
    "mailNickname": "SharedAccountsMFAExcluded",
    "securityEnabled": True
}
data = json.dumps(group_payload).encode('utf-8')
headers_post = {**headers, 'Content-Type': 'application/json'}
req = urllib.request.Request("https://graph.microsoft.com/v1.0/groups",
                              data=data, headers=headers_post, method='POST')
with urllib.request.urlopen(req) as resp:
    new_group = json.loads(resp.read())
    exclusion_group_id = new_group['id']
    print(f"Created exclusion group: {exclusion_group_id}")
```

Add members to the exclusion group:
```python
# For each shared account UPN, look up their ID first, then add:
member_url = f"https://graph.microsoft.com/v1.0/groups/{exclusion_group_id}/members/$ref"
member_payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"}
data = json.dumps(member_payload).encode('utf-8')
req = urllib.request.Request(member_url, data=data, headers=headers_post, method='POST')
urllib.request.urlopen(req)
```

### 7b — Find and Enable the MFA Conditional Access Policy

```python
# List all CA policies
ca_url = "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies"
req = urllib.request.Request(ca_url, headers=headers)
with urllib.request.urlopen(req) as resp:
    policies = json.loads(resp.read())['value']

for p in policies:
    print(f"  [{p['state']:10}] {p['displayName']}  →  {p['id']}")
```

Enable a policy and add the exclusion group:
```python
POLICY_ID = "..."  # ID of the MFA enforcement policy

patch = {
    "state": "enabled",
    "conditions": {
        "users": {
            "excludeGroups": [exclusion_group_id]
        }
    }
}
data = json.dumps(patch).encode('utf-8')
url = f"https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies/{POLICY_ID}"
req = urllib.request.Request(url, data=data, headers=headers_post, method='PATCH')
urllib.request.urlopen(req)
print("Policy enabled with exclusion group")
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Ask user to refresh token from Entra console |
| Empty group results | Wrong group name / underscore in name | Use `startswith()` search, not exact match |
| `InvalidURL` | Spaces in OData filter | URL-encode with `urllib.parse.quote()` |
| 403 on auth methods report | Insufficient permissions | Need Reports Reader or Global Admin |
| 400 on PATCH CA policy | Wrong field names | Check Entra CA policy schema; `excludeGroups` is under `conditions.users` |

---

## Output Format

Always end the audit with a clear summary like:
```
Group      : [Group Name]
Total      : [N] active accounts
Registered : [N] ([X]%)
Missing    : [N] ([X]%)
Disabled   : [N]

Files:
  [date]_MFA_All_Accounts.csv  → all accounts
  [date]_MFA_Missing.csv       → accounts needing MFA setup
```

And offer next steps: enforce MFA, draft email to users, or generate an executive report.

---

## Optional — Update Your Security Dashboard

If you maintain a security dashboard, record the key metrics: group audited, total active,
registered count and percentage, missing count, and any actions taken. If Notion is
connected via MCP, use `notion-fetch` and `notion-update-page` to refresh your dashboard
automatically.

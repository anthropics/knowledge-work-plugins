---
name: m365-guest-audit
description: >
  Audit all guest and external accounts in Microsoft 365 / Entra ID. Use this skill
  whenever any IT admin wants to review external user access, find forgotten
  guest accounts from old projects or departed vendors, clean up external users before
  a compliance review, check which outside parties can access organizational files and Teams,
  or generate a guest access report. Triggers on: "guest accounts", "external users",
  "who has guest access", "outside users", "vendor access", "contractor accounts",
  "clean up guests", "external access audit", "B2B accounts", "who can see our files
  from outside", "guest user cleanup", or any request involving external or guest accounts
  in Microsoft 365, SharePoint, or Teams.
---

# M365 Guest Account Audit Skill

This skill enumerates every external guest account in your Entra ID tenant, shows when
they were invited, what they last accessed, and helps you decide which ones to remove.
Forgotten guest accounts are a silent data exposure risk.

---

## Step 1 — Get the Bearer Token

**Ask the user to do this in their browser:**
1. Open [https://entra.microsoft.com](https://entra.microsoft.com) and sign in as Global Admin
2. Open DevTools → Console (F12 → Console tab)
3. Paste and run:
   ```javascript
   Object.keys(sessionStorage).filter(k => k.includes('accesstoken')).forEach(k => { try { let t = JSON.parse(sessionStorage[k]); if(t.target && t.target.includes('graph.microsoft.com')) console.log('TOKEN:', t.secret.substring(0,50) + '...', '\nFULL:', t.secret); } catch(e){} });
   ```
4. Copy the full `eyJ...` token and paste it in the chat

```python
token = "eyJ..."
with open('/tmp/ms_token.txt', 'w') as f:
    f.write(token.strip())
```

---

## Step 2 — Pull All Guest Accounts

```python
import urllib.request, json
from datetime import datetime, timezone, timedelta

with open('/tmp/ms_token.txt') as f:
    token = f.read().strip()
headers = {'Authorization': f'Bearer {token}'}

guests = []
url = ("https://graph.microsoft.com/beta/users"
       "?$filter=userType eq 'Guest'"
       "&$select=id,displayName,mail,userPrincipalName,createdDateTime,"
       "accountEnabled,signInActivity,externalUserState,externalUserStateChangeDateTime,"
       "companyName,jobTitle"
       "&$top=999")

while url:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    guests.extend(data.get('value', []))
    url = data.get('@odata.nextLink')

print(f"Total guest accounts found: {len(guests)}")
```

---

## Step 3 — Categorize Guests

```python
now = datetime.now(timezone.utc)
STALE_DAYS = 90  # guests inactive for this long are likely stale

active_guests = []
stale_guests = []
pending_guests = []     # invited but never accepted
never_used = []

for guest in guests:
    invited_date = guest.get('createdDateTime', '')[:10]
    state = guest.get('externalUserState', '')
    sign_in = guest.get('signInActivity', {})

    last_interactive = sign_in.get('lastSignInDateTime') if sign_in else None
    last_seen = None
    if last_interactive:
        last_seen = datetime.fromisoformat(last_interactive.replace('Z', '+00:00'))

    # External email (guests have UPNs like user_domain.com#EXT#@tenant.onmicrosoft.com)
    display_email = guest.get('mail') or guest.get('userPrincipalName', '').split('#EXT#')[0].replace('_', '@', 1)

    entry = {
        'Name': guest.get('displayName', ''),
        'Email': display_email,
        'Company': guest.get('companyName', ''),
        'Job Title': guest.get('jobTitle', ''),
        'Invite Status': state or 'Unknown',
        'Invited Date': invited_date,
        'Last Sign-In': last_seen.strftime('%Y-%m-%d') if last_seen else 'Never',
        'Days Since Sign-In': (now - last_seen).days if last_seen else 'N/A',
        'Account Enabled': 'Yes' if guest.get('accountEnabled') else 'No',
        'Recommendation': ''
    }

    if state == 'PendingAcceptance':
        entry['Recommendation'] = 'Pending invite — consider revoking if stale'
        pending_guests.append(entry)
    elif last_seen is None:
        entry['Recommendation'] = 'Never signed in — verify if still needed'
        never_used.append(entry)
    elif (now - last_seen).days > STALE_DAYS:
        entry['Recommendation'] = f'Inactive {(now - last_seen).days} days — likely safe to remove'
        stale_guests.append(entry)
    else:
        entry['Recommendation'] = 'Active guest'
        active_guests.append(entry)

print(f"\nActive guests (signed in within {STALE_DAYS} days) : {len(active_guests)}")
print(f"Stale guests (inactive >{STALE_DAYS} days)         : {len(stale_guests)}")
print(f"Pending invites (never accepted)                    : {len(pending_guests)}")
print(f"Never signed in (invite accepted, no login)         : {len(never_used)}")
```

---

## Step 4 — Show Domain Summary

Helps identify which organizations have the most external access:

```python
from collections import Counter

domain_counts = Counter()
for guest in guests:
    email = guest.get('mail') or guest.get('userPrincipalName', '')
    if '@' in email:
        domain = email.split('@')[-1].split('#')[0]
        domain_counts[domain] += 1

print("\nTOP EXTERNAL DOMAINS:")
for domain, count in domain_counts.most_common(10):
    print(f"  {domain:<35} {count} guest(s)")
```

---

## Step 5 — Export Excel Report

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()
fills = {
    'header':  PatternFill("solid", fgColor="1F3864"),
    'title':   PatternFill("solid", fgColor="2E75B6"),
    'stale':   PatternFill("solid", fgColor="FFD7D7"),
    'pending': PatternFill("solid", fgColor="FFE5CC"),
    'never':   PatternFill("solid", fgColor="FFFACC"),
    'active':  PatternFill("solid", fgColor="E8F4E8"),
}
hf = Font(bold=True, color="FFFFFF", name="Arial", size=11)
thin = Border(left=Side(style='thin'), right=Side(style='thin'),
              top=Side(style='thin'), bottom=Side(style='thin'))

cols = ['Name', 'Email', 'Company', 'Job Title', 'Invite Status', 'Invited Date',
        'Last Sign-In', 'Days Since Sign-In', 'Account Enabled', 'Recommendation']
widths = [22, 34, 20, 20, 18, 14, 14, 18, 16, 38]

def write_sheet(ws, title_text, rows, row_fill):
    ws.merge_cells(f"A1:{openpyxl.utils.get_column_letter(len(cols))}1")
    ws['A1'] = title_text
    ws['A1'].font = Font(bold=True, color="FFFFFF", name="Arial", size=13)
    ws['A1'].fill = fills['title']
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.row_dimensions[1].height = 24
    for i, (col, w) in enumerate(zip(cols, widths), 1):
        c = ws.cell(row=2, column=i, value=col)
        c.font = hf; c.fill = fills['header']
        c.alignment = Alignment(horizontal='center'); c.border = thin
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for rn, row in enumerate(rows, 3):
        fill = row_fill
        for cn, k in enumerate(cols, 1):
            c = ws.cell(row=rn, column=cn, value=row.get(k, ''))
            c.fill = fill; c.border = thin
            c.font = Font(name="Arial", size=10)
    ws.freeze_panes = 'A3'

ws1 = wb.active; ws1.title = "Stale Guests (Action Needed)"
write_sheet(ws1, f"STALE GUEST ACCOUNTS — {datetime.now().strftime('%B %d, %Y')}", stale_guests + never_used + pending_guests, fills['stale'])

ws2 = wb.create_sheet("Active Guests")
write_sheet(ws2, f"ACTIVE GUEST ACCOUNTS — {datetime.now().strftime('%B %d, %Y')}", active_guests, fills['active'])

today = datetime.now().strftime('%Y%m%d')
out_path = f"{today}_Guest_Account_Audit.xlsx"  # Update to your preferred reports folder
wb.save(out_path)
print(f"\nReport saved: {out_path}")
```

---

## Step 6 — Remove a Guest Account

When the user confirms a guest account should be removed:

```python
guest_id = "..."  # from the report

# Option 1: Disable first (safer — gives you time to reverse if wrong)
patch = json.dumps({"accountEnabled": False}).encode('utf-8')
h = {**headers, 'Content-Type': 'application/json'}
req = urllib.request.Request(f"https://graph.microsoft.com/v1.0/users/{guest_id}",
                              data=patch, headers=h, method='PATCH')
urllib.request.urlopen(req)
print("Guest account disabled")

# Option 2: Delete (puts in recycle bin for 30 days, then permanent)
req = urllib.request.Request(f"https://graph.microsoft.com/v1.0/users/{guest_id}",
                              headers=headers, method='DELETE')
urllib.request.urlopen(req)
print("Guest account deleted (recoverable for 30 days)")
```

Always disable before deleting. Confirm with the user before any deletion.

---

## Summary Output Format

```
GUEST ACCOUNT AUDIT — [Date]
================================
Total guest accounts    : [N]
  Active (within 90d)   : [N]  ← Currently in use
  Stale (>90 days)      : [N]  ← Candidates for removal
  Never signed in       : [N]  ← Invite accepted, never logged in
  Pending invites       : [N]  ← Invite sent but not accepted

TOP EXTERNAL DOMAINS:
  [domain] — [N] guests

RECOMMENDED REMOVALS: [N] accounts
  [Name] — [email] — [reason]

FILE: [date]_Guest_Account_Audit.xlsx
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Re-extract from Entra console |
| Empty results | No guest accounts | Verify filter: `userType eq 'Guest'` |
| `signInActivity` null | Missing Reports Reader permissions | Ensure token user has Reports Reader role |
| Cannot delete guest | Guest owns files/groups | Reassign ownership first, then delete |

---

## Optional — Update Your Security Dashboard

If you maintain a security dashboard, record: total guests, active, stale, never-used,
and top external domains. If Notion is connected via MCP, use `notion-fetch` and
`notion-update-page` to refresh your dashboard automatically.

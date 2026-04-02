---
name: m365-inactive-accounts
description: >
  Find stale, dormant, or inactive Microsoft 365 accounts — users who haven't signed in
  for 30, 60, or 90+ days. Use this skill whenever any IT admin wants to audit
  inactive staff accounts, clean up dormant accounts before a compliance review, find
  accounts that should be disabled after employee departures, reduce the attack surface
  from unused logins, or generate a stale accounts report for leadership. Triggers on:
  "inactive accounts", "who hasn't logged in", "stale accounts", "dormant users",
  "accounts to disable", "clean up old accounts", "unused logins", "last sign-in audit",
  "offboarding cleanup", or any request to find accounts with no recent activity in M365.
---

# M365 Inactive Accounts Audit Skill

This skill finds dormant Microsoft 365 accounts using the Graph API's sign-in activity
data — no admin portal clicking required. Stale accounts are one of the most common
attack vectors and the easiest to clean up.

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

If a token is already saved from an earlier audit this session, check if it's still valid
before asking the user to re-extract it.

---

## Step 2 — Choose the Inactivity Threshold

Ask the user how far back to look. Common options:
- **30 days** — recently inactive (may just be on leave)
- **60 days** — clearly dormant (good default)
- **90 days** — definitely stale (strong candidate for disabling)
- **Never signed in** — accounts created but never used

Default to **60 days** if the user doesn't specify.

---

## Step 3 — Pull All Users with Sign-In Activity

The `signInActivity` field is available on the `/users` endpoint with a beta header or
via the reports endpoint. Use the users endpoint directly for best results.

```python
import urllib.request, json
from datetime import datetime, timezone, timedelta

with open('/tmp/ms_token.txt') as f:
    token = f.read().strip()
headers = {'Authorization': f'Bearer {token}'}

THRESHOLD_DAYS = 60  # adjust based on user input

cutoff = datetime.now(timezone.utc) - timedelta(days=THRESHOLD_DAYS)

all_users = []
url = ("https://graph.microsoft.com/beta/users"
       "?$select=id,displayName,userPrincipalName,accountEnabled,userType,"
       "createdDateTime,signInActivity,jobTitle,department"
       "&$top=999")

while url:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    all_users.extend(data.get('value', []))
    url = data.get('@odata.nextLink')

print(f"Total users fetched: {len(all_users)}")
```

**Note:** The `/beta` endpoint is required for `signInActivity`. This is stable in practice
even though it's labeled beta.

---

## Step 4 — Categorize Users

```python
from collections import defaultdict

inactive = []      # No sign-in in threshold period
never_signed_in = []  # Account exists but never logged in
disabled = []      # Already disabled

for user in all_users:
    # Skip guest accounts (separate audit) and service accounts
    if user.get('userType') == 'Guest':
        continue
    if not user.get('accountEnabled', True):
        disabled.append(user)
        continue

    sign_in = user.get('signInActivity', {})
    last_interactive = sign_in.get('lastSignInDateTime')
    last_noninteractive = sign_in.get('lastNonInteractiveSignInDateTime')

    # Use most recent of interactive or non-interactive
    last_seen = None
    for ts in [last_interactive, last_noninteractive]:
        if ts:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            if last_seen is None or dt > last_seen:
                last_seen = dt

    if last_seen is None:
        never_signed_in.append({
            'Name': user['displayName'],
            'UPN': user['userPrincipalName'],
            'Department': user.get('department', ''),
            'Job Title': user.get('jobTitle', ''),
            'Account Created': user.get('createdDateTime', '')[:10],
            'Last Sign-In': 'NEVER',
            'Days Inactive': 'N/A',
            'Status': 'Never signed in'
        })
    elif last_seen < cutoff:
        days_ago = (datetime.now(timezone.utc) - last_seen).days
        inactive.append({
            'Name': user['displayName'],
            'UPN': user['userPrincipalName'],
            'Department': user.get('department', ''),
            'Job Title': user.get('jobTitle', ''),
            'Account Created': user.get('createdDateTime', '')[:10],
            'Last Sign-In': last_seen.strftime('%Y-%m-%d'),
            'Days Inactive': days_ago,
            'Status': f'Inactive {days_ago} days'
        })

# Sort by most inactive first
inactive.sort(key=lambda x: x['Days Inactive'], reverse=True)

print(f"\nInactive (>{THRESHOLD_DAYS} days): {len(inactive)}")
print(f"Never signed in: {len(never_signed_in)}")
print(f"Already disabled: {len(disabled)}")
```

---

## Step 5 — Export Excel Report

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()

fills = {
    'header': PatternFill("solid", fgColor="1F3864"),
    'title':  PatternFill("solid", fgColor="2E75B6"),
    'inactive_heavy': PatternFill("solid", fgColor="FFD7D7"),   # 90+ days — red
    'inactive_med':   PatternFill("solid", fgColor="FFE5CC"),   # 60-89 days — orange
    'inactive_light': PatternFill("solid", fgColor="FFFACC"),   # 30-59 days — yellow
    'never':          PatternFill("solid", fgColor="E8D5F0"),   # Never — purple
}
header_font = Font(bold=True, color="FFFFFF", name="Arial", size=11)
thin = Border(left=Side(style='thin'), right=Side(style='thin'),
              top=Side(style='thin'), bottom=Side(style='thin'))

def write_sheet(ws, title_text, rows, cols, col_widths, fills_map):
    ws.merge_cells(f'A1:{openpyxl.utils.get_column_letter(len(cols))}1')
    ws['A1'] = title_text
    ws['A1'].font = Font(bold=True, color="FFFFFF", name="Arial", size=13)
    ws['A1'].fill = fills['title']
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.row_dimensions[1].height = 24

    for i, (col, w) in enumerate(zip(cols, col_widths), 1):
        cell = ws.cell(row=2, column=i, value=col)
        cell.font = header_font
        cell.fill = fills['header']
        cell.alignment = Alignment(horizontal='center')
        cell.border = thin
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

    for row_num, row in enumerate(rows, 3):
        fill = fills_map(row)
        for col_num, key in enumerate(cols, 1):
            cell = ws.cell(row=row_num, column=col_num, value=row.get(key, ''))
            cell.fill = fill
            cell.border = thin
            cell.font = Font(name="Arial", size=10)
    ws.freeze_panes = 'A3'

cols = ['Name', 'UPN', 'Department', 'Job Title', 'Account Created', 'Last Sign-In', 'Days Inactive', 'Status']
widths = [22, 34, 18, 20, 16, 14, 14, 22]

# Inactive sheet
ws1 = wb.active
ws1.title = f"Inactive >{THRESHOLD_DAYS} Days"
def inactive_fill(row):
    d = row.get('Days Inactive', 0)
    if isinstance(d, int) and d >= 90: return fills['inactive_heavy']
    if isinstance(d, int) and d >= 60: return fills['inactive_med']
    return fills['inactive_light']
write_sheet(ws1, f"INACTIVE ACCOUNTS — No Sign-In for >{THRESHOLD_DAYS} Days — {datetime.now().strftime('%B %d, %Y')}", inactive, cols, widths, inactive_fill)

# Never signed in sheet
ws2 = wb.create_sheet("Never Signed In")
write_sheet(ws2, f"ACCOUNTS THAT HAVE NEVER SIGNED IN — {datetime.now().strftime('%B %d, %Y')}", never_signed_in, cols, widths, lambda r: fills['never'])

today = datetime.now().strftime('%Y%m%d')
out_path = f"{today}_Inactive_Accounts_Audit.xlsx"  # Update to your preferred reports folder
wb.save(out_path)
print(f"\nReport saved: {out_path}")
```

---

## Step 6 — Review and Recommend Actions

After showing the user the report, walk through the options for each group:

**For "Never Signed In" accounts:**
- Confirm with HR/admin whether the person ever started
- If the employee never started or left before onboarding — disable the account
- If the account is a planned future hire — leave enabled but note it

**For inactive accounts (60+ days):**
- Cross-reference with HR departure dates
- Suggest disabling (not deleting — can restore if needed) with this API call:

```python
# Disable a specific account
user_id = "..."   # from the report
patch = json.dumps({"accountEnabled": False}).encode('utf-8')
h = {**headers, 'Content-Type': 'application/json'}
req = urllib.request.Request(
    f"https://graph.microsoft.com/v1.0/users/{user_id}",
    data=patch, headers=h, method='PATCH'
)
urllib.request.urlopen(req)
print(f"Account disabled")
```

**Important:** Always disable before deleting. Deleted accounts can be restored for 30 days,
but permanently deleted accounts cannot.

---

## Summary Output Format

End every audit with a clear summary:

```
INACTIVE ACCOUNTS AUDIT — [Date]
===================================
Threshold         : [N] days
Total active users: [N]
  Inactive        : [N]  ← No sign-in in [N] days
  Never signed in : [N]  ← Account created but never used
  Already disabled: [N]  ← Already handled

TOP 5 MOST INACTIVE:
  [Name] — last seen [date] ([N] days ago)
  ...

RECOMMENDED ACTIONS:
  [N] accounts to investigate for immediate disable
  [N] "never signed in" accounts to verify with HR

FILE: [date]_Inactive_Accounts_Audit.xlsx
```

Then ask: "Would you like me to disable any of these accounts, or draft an email to HR
for verification?"

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Re-extract from Entra console |
| `signInActivity` null for all users | Missing Reports Reader role | Token user needs Reports Reader or Global Admin |
| Beta endpoint 404 | Wrong URL | Use `/beta/users` not `/v1.0/users` for signInActivity |
| Empty results | All users recently active | Lower the threshold or check the date filter |

---

## Optional — Update Your Security Dashboard

If you maintain a security dashboard, record: inactive count, never-signed-in count,
disabled-with-licenses count, and top departments affected. If Notion is connected via MCP,
use `notion-fetch` and `notion-update-page` to refresh your dashboard automatically.

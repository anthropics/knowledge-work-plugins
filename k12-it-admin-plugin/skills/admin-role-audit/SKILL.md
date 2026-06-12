---
name: m365-admin-role-audit
description: >
  Audit all privileged administrator roles in Microsoft 365 / Entra ID. Use this skill
  whenever any IT admin wants to see who has admin access, check for overprivileged
  accounts, find old vendor or contractor admin accounts that should be removed, verify
  that the principle of least privilege is being followed, run a quarterly admin access
  review, or prepare a privilege audit for compliance. Triggers on: "admin role audit",
  "who has admin access", "list all admins", "check admin accounts", "privileged users",
  "global admins", "who can access everything", "over-privileged accounts", "admin access
  review", "least privilege audit", "vendor admin accounts", or any request involving
  administrator roles, permissions, or privileged access in Microsoft 365 or Entra.
---

# M365 Admin Role Audit Skill

This skill enumerates every privileged role assignment in your Entra ID tenant and
flags accounts that should be reviewed — overprivileged users, stale admin accounts,
vendor access, and role sprawl.

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

If a token was saved earlier this session, try it before asking the user to re-extract.

---

## Step 2 — Pull All Directory Role Assignments

```python
import urllib.request, json
from collections import defaultdict

with open('/tmp/ms_token.txt') as f:
    token = f.read().strip()
headers = {'Authorization': f'Bearer {token}'}

def graph_get(url):
    results = []
    while url:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        results.extend(data.get('value', []))
        url = data.get('@odata.nextLink')
    return results

# Get all activated directory roles (only roles with at least one member show up here)
roles = graph_get("https://graph.microsoft.com/v1.0/directoryRoles?$select=id,displayName,description,roleTemplateId")
print(f"Active directory roles found: {len(roles)}")
for r in roles:
    print(f"  {r['displayName']}")
```

---

## Step 3 — Get Members for Each Role

```python
# High-priority roles to flag explicitly
HIGH_PRIVILEGE_ROLES = {
    'Global Administrator',
    'Privileged Role Administrator',
    'Privileged Authentication Administrator',
    'Security Administrator',
    'Exchange Administrator',
    'SharePoint Administrator',
    'Teams Administrator',
    'Intune Administrator',
    'Conditional Access Administrator',
    'Authentication Administrator',
    'User Administrator',
    'Helpdesk Administrator',
}

role_assignments = []  # flat list: {role, user}
users_to_roles = defaultdict(list)  # user → list of roles

for role in roles:
    role_id = role['id']
    role_name = role['displayName']

    members = graph_get(
        f"https://graph.microsoft.com/v1.0/directoryRoles/{role_id}/members"
        f"?$select=id,displayName,userPrincipalName,accountEnabled,userType,jobTitle,department"
    )

    for member in members:
        entry = {
            'Role': role_name,
            'Role Priority': 'HIGH' if role_name in HIGH_PRIVILEGE_ROLES else 'STANDARD',
            'Name': member.get('displayName', ''),
            'UPN': member.get('userPrincipalName', ''),
            'Account Enabled': 'Yes' if member.get('accountEnabled') else 'No',
            'User Type': member.get('userType', 'Member'),
            'Job Title': member.get('jobTitle', ''),
            'Department': member.get('department', ''),
            'Object Type': member.get('@odata.type', '').replace('#microsoft.graph.', '')
        }
        role_assignments.append(entry)
        users_to_roles[member.get('userPrincipalName', member.get('id', ''))].append(role_name)

print(f"\nTotal role assignments: {len(role_assignments)}")

# Print high-privilege summary
print("\nHIGH-PRIVILEGE ROLE HOLDERS:")
for upn, roles_held in sorted(users_to_roles.items()):
    high_roles = [r for r in roles_held if r in HIGH_PRIVILEGE_ROLES]
    if high_roles:
        print(f"  {upn}")
        for r in high_roles:
            print(f"    → {r}")
```

---

## Step 4 — Flag Risk Indicators

```python
# Accounts that should be reviewed
risks = []

for upn, roles_held in users_to_roles.items():
    high_roles = [r for r in roles_held if r in HIGH_PRIVILEGE_ROLES]
    if not high_roles:
        continue

    # Find this user's account details
    matching = [a for a in role_assignments if a['UPN'] == upn]
    if not matching:
        continue
    user = matching[0]

    flags = []

    # Multiple high-privilege roles = role sprawl
    if len(high_roles) > 2:
        flags.append(f"Role sprawl: holds {len(high_roles)} high-privilege roles")

    # Disabled account still in admin role
    if user['Account Enabled'] == 'No':
        flags.append("DISABLED account still assigned admin role — remove immediately")

    # Guest with admin role
    if user['User Type'] == 'Guest':
        flags.append("GUEST account with admin role — verify this is intentional")

    # Global Admin: flag any account with this role for documentation
    if 'Global Administrator' in high_roles:
        flags.append("Global Administrator — verify account is IT-owned and MFA-protected")

    if flags:
        risks.append({
            'Name': user['Name'],
            'UPN': upn,
            'Roles': ', '.join(high_roles),
            'Flags': ' | '.join(flags)
        })

print(f"\nAccounts flagged for review: {len(risks)}")
for r in risks:
    print(f"\n  {r['Name']} ({r['UPN']})")
    print(f"  Roles : {r['Roles']}")
    print(f"  Flags : {r['Flags']}")
```

---

## Step 5 — Export Excel Report

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

wb = openpyxl.Workbook()

fills = {
    'header': PatternFill("solid", fgColor="1F3864"),
    'title':  PatternFill("solid", fgColor="2E75B6"),
    'high':   PatternFill("solid", fgColor="FFD7D7"),
    'std':    PatternFill("solid", fgColor="E8F4E8"),
    'flag':   PatternFill("solid", fgColor="FFE5CC"),
    'disabled': PatternFill("solid", fgColor="CCCCCC"),
}
hf = Font(bold=True, color="FFFFFF", name="Arial", size=11)
thin = Border(left=Side(style='thin'), right=Side(style='thin'),
              top=Side(style='thin'), bottom=Side(style='thin'))

def add_sheet(ws, title, rows, col_keys, col_widths, fill_fn):
    ncols = len(col_keys)
    ws.merge_cells(f"A1:{openpyxl.utils.get_column_letter(ncols)}1")
    ws['A1'] = title
    ws['A1'].font = Font(bold=True, color="FFFFFF", name="Arial", size=13)
    ws['A1'].fill = fills['title']
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.row_dimensions[1].height = 24
    for i, (k, w) in enumerate(zip(col_keys, col_widths), 1):
        c = ws.cell(row=2, column=i, value=k)
        c.font = hf; c.fill = fills['header']
        c.alignment = Alignment(horizontal='center'); c.border = thin
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for rn, row in enumerate(rows, 3):
        fill = fill_fn(row)
        for cn, k in enumerate(col_keys, 1):
            c = ws.cell(row=rn, column=cn, value=row.get(k, ''))
            c.fill = fill; c.border = thin
            c.font = Font(name="Arial", size=10)
    ws.freeze_panes = 'A3'

# All assignments sheet
ws1 = wb.active
ws1.title = "All Role Assignments"
keys1 = ['Role', 'Role Priority', 'Name', 'UPN', 'Account Enabled', 'User Type', 'Job Title', 'Department']
widths1 = [30, 12, 22, 34, 16, 12, 22, 18]
sorted_assignments = sorted(role_assignments, key=lambda x: (x['Role Priority'], x['Role'], x['Name']))
def fill1(row):
    if row['Account Enabled'] == 'No': return fills['disabled']
    return fills['high'] if row['Role Priority'] == 'HIGH' else fills['std']
add_sheet(ws1, f"ALL ADMIN ROLE ASSIGNMENTS — {datetime.now().strftime('%B %d, %Y')}", sorted_assignments, keys1, widths1, fill1)

# Flagged accounts sheet
if risks:
    ws2 = wb.create_sheet("Flagged for Review")
    keys2 = ['Name', 'UPN', 'Roles', 'Flags']
    widths2 = [22, 34, 40, 60]
    add_sheet(ws2, f"ACCOUNTS FLAGGED FOR REVIEW — {datetime.now().strftime('%B %d, %Y')}", risks, keys2, widths2, lambda r: fills['flag'])

today = datetime.now().strftime('%Y%m%d')
out_path = f"{today}_Admin_Role_Audit.xlsx"  # Update to your preferred reports folder
wb.save(out_path)
print(f"\nReport saved: {out_path}")
```

---

## Step 6 — Recommendations

After reviewing the report with the user, suggest:

1. **Global Admins** — Should be 2–4 people max. More than that increases breach risk.
   Each Global Admin should have MFA enforced and a dedicated admin account (not their
   daily-use account).

2. **Disabled accounts with roles** — Remove the role assignment immediately. A disabled
   account can still be re-enabled by an attacker with partial access.

3. **Guest accounts with admin roles** — Should be extremely rare. Vendors and consultants
   should use PIM (Privileged Identity Management) for just-in-time access instead.

4. **Role sprawl** — If someone has 3+ high-privilege roles, consider whether they truly
   need all of them. Separate duties where possible.

To remove a role assignment:
```python
# Remove user from a directory role
role_id = "..."    # role ID from earlier
user_id = "..."    # user ID to remove

req = urllib.request.Request(
    f"https://graph.microsoft.com/v1.0/directoryRoles/{role_id}/members/{user_id}/$ref",
    headers=headers, method='DELETE'
)
urllib.request.urlopen(req)
print("Role assignment removed")
```

---

## Summary Output Format

```
ADMIN ROLE AUDIT — [Date]
===========================
Total role assignments : [N]
High-privilege roles   : [N] assignments across [N] accounts
Accounts flagged       : [N]

GLOBAL ADMINISTRATORS ([N]):
  [Name] — [UPN]

FLAGGED FOR REVIEW:
  [Name] — [reason]

RECOMMENDED ACTIONS:
  [N] disabled accounts still holding admin roles → remove immediately
  [N] accounts with role sprawl → review and reduce
  [N] guest admin accounts → verify intent

FILE: [date]_Admin_Role_Audit.xlsx
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Re-extract from Entra console |
| Empty roles list | No activated roles (unlikely) | Use `/beta/roleManagement/directory/roleAssignments` instead |
| Service principals in results | Apps also get roles | Filter by `@odata.type` = `#microsoft.graph.user` if user-only view needed |
| 403 on role members | Insufficient permissions | Requires Global Admin or Privileged Role Administrator |

---

## Optional — Update Your Security Dashboard

If you maintain a security dashboard, record the key metrics from this audit: total role
assignments, flagged accounts, current Global Admin list, and any actions taken. If Notion
is connected via MCP, use `notion-fetch` and `notion-update-page` to refresh your
dashboard automatically.

---
name: m365-oauth-audit
description: >
  Audit all third-party apps and OAuth permissions granted access to your Microsoft 365
  tenant. Use this skill whenever any IT admin wants to see which apps have
  been granted access to organizational data, find apps with overly broad permissions like
  Mail.Read or Files.ReadWrite.All, identify apps that staff approved without IT review,
  remove suspicious or unused app permissions, or run an app consent audit before a
  compliance review. Triggers on: "OAuth audit", "app permissions", "third-party apps",
  "what apps can access our data", "app consent", "service principals", "app registrations",
  "who approved these apps", "remove app access", "application permissions audit",
  "connector audit", "Teams app audit", or any request to review which applications
  have access to Microsoft 365 data.
---

# M365 OAuth & App Permissions Audit Skill

This skill enumerates all third-party applications with delegated or application-level
access to your Microsoft 365 tenant and flags anything overly permissive or suspicious.
Users frequently grant broad app access without realizing what they've approved.

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

## Step 2 — Pull All Service Principals (Third-Party Apps)

Service principals represent applications that have been granted access to your tenant,
whether via admin consent or user consent.

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

# Service principals — all apps registered in or consented to the tenant
sps = graph_get(
    "https://graph.microsoft.com/v1.0/servicePrincipals"
    "?$select=id,displayName,appId,publisherName,servicePrincipalType,"
    "tags,createdDateTime,accountEnabled,verifiedPublisher,appOwnerOrganizationId"
    "&$top=999"
)

# Filter out Microsoft's own first-party apps — focus on third-party
first_party_org = "f8cdef31-a31e-4b4a-93e4-5f571e91255a"  # Microsoft Services tenant ID
third_party_sps = [sp for sp in sps
                   if sp.get('appOwnerOrganizationId') != first_party_org
                   and sp.get('servicePrincipalType') not in ('ManagedIdentity',)]

print(f"Total service principals : {len(sps)}")
print(f"Third-party apps         : {len(third_party_sps)}")
```

---

## Step 3 — Pull OAuth Permission Grants

Two types of grants exist:
- **Delegated (OAuth2PermissionGrants)** — granted on behalf of a user, acts as that user
- **Application (AppRoleAssignments)** — app-level access, acts as itself (often more powerful)

```python
# Delegated permission grants (user-consented or admin-consented on behalf of users)
oauth_grants = graph_get("https://graph.microsoft.com/v1.0/oauth2PermissionGrants?$top=999")
# Map clientId (SP object ID) → grants
grants_by_sp = defaultdict(list)
for grant in oauth_grants:
    grants_by_sp[grant['clientId']].append(grant)

# Application role assignments (app-to-app, no user context)
app_roles_by_sp = defaultdict(list)
for sp in third_party_sps:
    sp_id = sp['id']
    try:
        roles = graph_get(
            f"https://graph.microsoft.com/v1.0/servicePrincipals/{sp_id}/appRoleAssignments"
        )
        app_roles_by_sp[sp_id] = roles
    except:
        pass

print(f"OAuth delegated grants   : {len(oauth_grants)}")
```

---

## Step 4 — Flag High-Risk Permissions

```python
# Permissions that should always be reviewed
HIGH_RISK_SCOPES = {
    'Mail.Read', 'Mail.ReadWrite', 'Mail.Send',
    'Files.ReadWrite.All', 'Files.Read.All',
    'Calendars.ReadWrite',
    'Contacts.ReadWrite',
    'User.Read.All', 'User.ReadWrite.All',
    'Directory.Read.All', 'Directory.ReadWrite.All',
    'Group.ReadWrite.All',
    'offline_access',
}

flagged_apps = []
all_app_rows = []

for sp in third_party_sps:
    sp_id = sp['id']
    sp_name = sp.get('displayName', 'Unknown App')
    publisher = sp.get('publisherName', '')
    verified = bool(sp.get('verifiedPublisher'))
    created = sp.get('createdDateTime', '')[:10]

    # Collect all scopes for this app
    delegated_scopes = set()
    for grant in grants_by_sp.get(sp_id, []):
        scopes_str = grant.get('scope', '')
        for s in scopes_str.split():
            delegated_scopes.add(s)

    app_role_names = set()
    for role in app_roles_by_sp.get(sp_id, []):
        app_role_names.add(role.get('principalDisplayName', '') + ':' + role.get('resourceDisplayName', ''))

    high_risk = delegated_scopes.intersection(HIGH_RISK_SCOPES)

    row = {
        'App Name': sp_name,
        'Publisher': publisher,
        'Verified Publisher': 'Yes' if verified else 'No',
        'Date Added': created,
        'Delegated Scopes': ', '.join(sorted(delegated_scopes)) or 'None',
        'App-Level Roles': ', '.join(sorted(app_role_names)) or 'None',
        'High Risk Scopes': ', '.join(sorted(high_risk)) or '',
        'Risk Level': 'HIGH' if high_risk else ('REVIEW' if not verified and delegated_scopes else 'LOW'),
    }
    all_app_rows.append(row)

    if high_risk or (not verified and delegated_scopes):
        flagged_apps.append(row)

# Sort by risk
risk_order = {'HIGH': 0, 'REVIEW': 1, 'LOW': 2}
flagged_apps.sort(key=lambda x: risk_order.get(x['Risk Level'], 3))

print(f"\nTotal third-party apps with permissions: {len(all_app_rows)}")
print(f"HIGH risk (broad permissions)           : {sum(1 for r in all_app_rows if r['Risk Level']=='HIGH')}")
print(f"REVIEW (unverified with permissions)    : {sum(1 for r in all_app_rows if r['Risk Level']=='REVIEW')}")
print(f"\nFlagged apps:")
for app in flagged_apps:
    print(f"\n  {app['App Name']} ({app['Publisher'] or 'No publisher'})")
    print(f"  Risk: {app['Risk Level']}")
    if app['High Risk Scopes']:
        print(f"  High-risk scopes: {app['High Risk Scopes']}")
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
    'review': PatternFill("solid", fgColor="FFE5CC"),
    'low':    PatternFill("solid", fgColor="E8F4E8"),
}
hf = Font(bold=True, color="FFFFFF", name="Arial", size=11)
thin = Border(left=Side(style='thin'), right=Side(style='thin'),
              top=Side(style='thin'), bottom=Side(style='thin'))

cols = ['App Name', 'Publisher', 'Verified Publisher', 'Date Added',
        'Delegated Scopes', 'High Risk Scopes', 'Risk Level']
widths = [28, 22, 18, 14, 60, 40, 12]

def write_sheet(ws, title_text, rows):
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
        risk = row.get('Risk Level', 'LOW')
        fill = fills.get(risk.lower(), fills['low'])
        for cn, k in enumerate(cols, 1):
            c = ws.cell(row=rn, column=cn, value=row.get(k, ''))
            c.fill = fill; c.border = thin
            c.font = Font(name="Arial", size=10)
    ws.freeze_panes = 'A3'

sorted_all = sorted(all_app_rows, key=lambda x: risk_order.get(x['Risk Level'], 3))
ws1 = wb.active; ws1.title = "All Apps"
write_sheet(ws1, f"ALL THIRD-PARTY APP PERMISSIONS — {datetime.now().strftime('%B %d, %Y')}", sorted_all)

if flagged_apps:
    ws2 = wb.create_sheet("Flagged Apps (Review)")
    write_sheet(ws2, f"FLAGGED APPS — REVIEW REQUIRED — {datetime.now().strftime('%B %d, %Y')}", flagged_apps)

today = datetime.now().strftime('%Y%m%d')
out_path = f"{today}_OAuth_App_Audit.xlsx"  # Update to your preferred reports folder
wb.save(out_path)
print(f"\nReport saved: {out_path}")
```

---

## Step 6 — Revoke an App's Permissions

When the user wants to remove an app's access:

```python
# Revoke a specific delegated permission grant
grant_id = "..."  # from oauth_grants list

req = urllib.request.Request(
    f"https://graph.microsoft.com/v1.0/oauth2PermissionGrants/{grant_id}",
    headers=headers, method='DELETE'
)
urllib.request.urlopen(req)
print("Delegated permission grant revoked")

# To fully remove the app, delete its service principal
sp_id = "..."
req = urllib.request.Request(
    f"https://graph.microsoft.com/v1.0/servicePrincipals/{sp_id}",
    headers=headers, method='DELETE'
)
urllib.request.urlopen(req)
print("Service principal (app) removed from tenant")
```

Always confirm with the user before revoking. Removing a widely-used app integration
(like a gradebook sync or video conferencing connector) will break workflows.

---

## Summary Output Format

```
OAUTH & APP PERMISSIONS AUDIT — [Date]
=========================================
Total third-party apps  : [N]
  HIGH risk             : [N]  ← Broad data access permissions
  REVIEW needed         : [N]  ← Unverified publishers with access
  LOW risk              : [N]  ← Limited, verified apps

TOP CONCERNS:
  [App Name] — [High-risk scopes]

RECOMMENDED ACTIONS:
  Review [N] high-risk apps with IT and confirm business need
  Revoke [N] unrecognized apps immediately

FILE: [date]_OAuth_App_Audit.xlsx
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Re-extract from Entra console |
| Empty service principals | Filter too narrow | Remove the org ID filter temporarily |
| 403 on appRoleAssignments | Insufficient permissions | Need Application.Read.All at minimum |
| Many Microsoft apps showing | First-party filter missed some | Also filter by `publisherName` containing "Microsoft" |

---

## Optional — Update Your Security Dashboard

If you maintain a security dashboard, record: total third-party apps, HIGH risk count,
REVIEW count, and any apps revoked this run. If Notion is connected via MCP, use
`notion-fetch` and `notion-update-page` to refresh your dashboard automatically.

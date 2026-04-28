---
name: m365-ca-audit
description: >
  Audit Conditional Access policies in Microsoft 365 / Entra ID for gaps, misconfigurations,
  and coverage holes. Use this skill whenever any IT admin wants to review
  Conditional Access policy coverage, find users or apps excluded from MFA requirements,
  check if legacy authentication protocols are still allowed, verify that admin accounts
  are protected, identify report-only policies that were never enabled, or prepare a
  Conditional Access audit for compliance. Triggers on: "Conditional Access audit",
  "CA policy review", "check my CA policies", "who's excluded from MFA", "legacy auth",
  "basic auth still allowed", "policy gaps", "Conditional Access coverage", "are my
  policies complete", "review access policies", "authentication policy audit", or any
  request involving Conditional Access, sign-in policies, or authentication requirements
  in Microsoft 365.
---

# M365 Conditional Access Audit Skill

This skill pulls all Conditional Access policies in your tenant and analyzes them for
common gaps — users excluded from MFA, legacy auth enabled, admin accounts unprotected,
and policies stuck in report-only mode.

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

## Step 2 — Pull All Conditional Access Policies

```python
import urllib.request, json

with open('/tmp/ms_token.txt') as f:
    token = f.read().strip()
headers = {'Authorization': f'Bearer {token}'}

req = urllib.request.Request(
    "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies",
    headers=headers
)
with urllib.request.urlopen(req) as resp:
    ca_data = json.loads(resp.read())
policies = ca_data.get('value', [])

print(f"Total CA policies found: {len(policies)}")
print()
for p in policies:
    state_icon = "✓" if p['state'] == 'enabled' else ("⚠" if p['state'] == 'enabledForReportingButNotEnforced' else "✗")
    print(f"  [{state_icon} {p['state']:35}] {p['displayName']}")
```

---

## Step 3 — Analyze Each Policy

```python
from collections import defaultdict

# Summary buckets
enabled_policies = [p for p in policies if p['state'] == 'enabled']
report_only = [p for p in policies if p['state'] == 'enabledForReportingButNotEnforced']
disabled_policies = [p for p in policies if p['state'] == 'disabled']

gaps = []   # specific issues found

print(f"\nPolicy status:")
print(f"  Enabled (enforced)  : {len(enabled_policies)}")
print(f"  Report-only         : {len(report_only)}  ← Not actually enforcing!")
print(f"  Disabled            : {len(disabled_policies)}")

# ── Gap 1: Report-only policies ──────────────────────────────────────────────
for p in report_only:
    gaps.append({
        'Severity': 'HIGH',
        'Policy': p['displayName'],
        'Issue': 'Policy is in REPORT-ONLY mode — not actually enforced',
        'Fix': 'Change state to "enabled" in Entra admin center after reviewing sign-in logs'
    })

# ── Gap 2: All-users MFA policy exists and what it excludes ─────────────────
mfa_policies = []
for p in enabled_policies:
    conditions = p.get('conditions', {})
    grant = p.get('grantControls', {})
    if not grant:
        continue
    built_in = grant.get('builtInControls', [])
    if 'mfa' in built_in or 'authenticationStrength' in grant:
        mfa_policies.append(p)

if not mfa_policies:
    gaps.append({
        'Severity': 'CRITICAL',
        'Policy': 'N/A',
        'Issue': 'No enforced MFA Conditional Access policy found',
        'Fix': 'Create and enable an MFA requirement policy for all users'
    })
else:
    for p in mfa_policies:
        conditions = p.get('conditions', {})
        users = conditions.get('users', {})
        excluded_users = users.get('excludeUsers', [])
        excluded_groups = users.get('excludeGroups', [])
        include_users = users.get('includeUsers', [])

        if excluded_users:
            gaps.append({
                'Severity': 'MEDIUM',
                'Policy': p['displayName'],
                'Issue': f'{len(excluded_users)} user(s) individually excluded from MFA requirement',
                'Fix': 'Review excluded users — each should have a documented reason'
            })
        if excluded_groups:
            gaps.append({
                'Severity': 'MEDIUM',
                'Policy': p['displayName'],
                'Issue': f'{len(excluded_groups)} group(s) excluded from MFA requirement',
                'Fix': 'Audit excluded groups to ensure no unnecessary exemptions remain'
            })
        if 'All' not in include_users and not include_users:
            gaps.append({
                'Severity': 'HIGH',
                'Policy': p['displayName'],
                'Issue': 'MFA policy does not include all users',
                'Fix': 'Change includeUsers to "All" unless there is a specific reason for partial coverage'
            })

# ── Gap 3: Legacy authentication blocking ────────────────────────────────────
legacy_block_found = False
for p in enabled_policies:
    conditions = p.get('conditions', {})
    client_apps = conditions.get('clientAppTypes', [])
    if any(app in client_apps for app in ['exchangeActiveSync', 'other']):
        grant = p.get('grantControls', {})
        session = p.get('sessionControls', {})
        if grant and 'block' in grant.get('builtInControls', []):
            legacy_block_found = True

if not legacy_block_found:
    gaps.append({
        'Severity': 'HIGH',
        'Policy': 'N/A',
        'Issue': 'No policy found blocking legacy authentication protocols',
        'Fix': 'Create a CA policy blocking "Exchange ActiveSync" and "Other clients" — legacy auth bypasses MFA'
    })

# ── Gap 4: Admin-specific protections ────────────────────────────────────────
admin_policy_found = False
for p in enabled_policies:
    conditions = p.get('conditions', {})
    users = conditions.get('users', {})
    if users.get('includeRoles'):
        admin_policy_found = True

if not admin_policy_found:
    gaps.append({
        'Severity': 'MEDIUM',
        'Policy': 'N/A',
        'Issue': 'No CA policy specifically targeting admin roles found',
        'Fix': 'Consider a stricter policy for admin accounts: require phishing-resistant MFA (FIDO2 or certificate)'
    })

# ── Gap 5: Sign-in risk policies ─────────────────────────────────────────────
risk_policy_found = False
for p in enabled_policies:
    conditions = p.get('conditions', {})
    if conditions.get('signInRiskLevels') or conditions.get('userRiskLevels'):
        risk_policy_found = True

if not risk_policy_found:
    gaps.append({
        'Severity': 'LOW',
        'Policy': 'N/A',
        'Issue': 'No sign-in risk or user risk CA policy found',
        'Fix': 'Add a risk-based CA policy: high risk sign-in → block or require MFA + password change. Requires Entra ID P2.'
    })

print(f"\nGAPS FOUND: {len(gaps)}")
severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
gaps.sort(key=lambda g: severity_order.get(g['Severity'], 4))
for g in gaps:
    print(f"\n  [{g['Severity']}] {g['Policy']}")
    print(f"  Issue : {g['Issue']}")
    print(f"  Fix   : {g['Fix']}")
```

---

## Step 4 — Export Full Policy Report

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

wb = openpyxl.Workbook()
fills = {
    'header':   PatternFill("solid", fgColor="1F3864"),
    'title':    PatternFill("solid", fgColor="2E75B6"),
    'enabled':  PatternFill("solid", fgColor="E8F4E8"),
    'report':   PatternFill("solid", fgColor="FFE5CC"),
    'disabled': PatternFill("solid", fgColor="CCCCCC"),
    'CRITICAL': PatternFill("solid", fgColor="FF4444"),
    'HIGH':     PatternFill("solid", fgColor="FFD7D7"),
    'MEDIUM':   PatternFill("solid", fgColor="FFE5CC"),
    'LOW':      PatternFill("solid", fgColor="FFFACC"),
}
hf = Font(bold=True, color="FFFFFF", name="Arial", size=11)
thin = Border(left=Side(style='thin'), right=Side(style='thin'),
              top=Side(style='thin'), bottom=Side(style='thin'))

# Policy overview sheet
ws1 = wb.active
ws1.title = "Policy Overview"
pol_cols = ['Policy Name', 'State', 'Includes Users', 'Excludes Users',
            'Excludes Groups', 'Apps Targeted', 'Grant Controls']
pol_widths = [40, 30, 20, 16, 16, 30, 30]

ws1.merge_cells(f"A1:{openpyxl.utils.get_column_letter(len(pol_cols))}1")
ws1['A1'] = f"CONDITIONAL ACCESS POLICIES — {datetime.now().strftime('%B %d, %Y')}"
ws1['A1'].font = Font(bold=True, color="FFFFFF", name="Arial", size=13)
ws1['A1'].fill = fills['title']
ws1['A1'].alignment = Alignment(horizontal='center')
ws1.row_dimensions[1].height = 24
for i, (col, w) in enumerate(zip(pol_cols, pol_widths), 1):
    c = ws1.cell(row=2, column=i, value=col)
    c.font = hf; c.fill = fills['header']
    c.alignment = Alignment(horizontal='center'); c.border = thin
    ws1.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

for rn, p in enumerate(policies, 3):
    state = p['state']
    cond = p.get('conditions', {})
    users = cond.get('users', {})
    apps = cond.get('applications', {})
    grant = p.get('grantControls') or {}
    controls = ', '.join(grant.get('builtInControls', []))

    if state == 'enabled': row_fill = fills['enabled']
    elif state == 'enabledForReportingButNotEnforced': row_fill = fills['report']
    else: row_fill = fills['disabled']

    row_data = [
        p['displayName'],
        state,
        ', '.join(users.get('includeUsers', []) + users.get('includeRoles', []))[:100],
        str(len(users.get('excludeUsers', []))),
        str(len(users.get('excludeGroups', []))),
        ', '.join(apps.get('includeApplications', ['']))[:80],
        controls
    ]
    for cn, val in enumerate(row_data, 1):
        c = ws1.cell(row=rn, column=cn, value=val)
        c.fill = row_fill; c.border = thin
        c.font = Font(name="Arial", size=10)
ws1.freeze_panes = 'A3'

# Gaps sheet
if gaps:
    ws2 = wb.create_sheet("Gaps & Recommendations")
    gap_cols = ['Severity', 'Policy', 'Issue', 'Recommended Fix']
    gap_widths = [12, 35, 55, 55]
    ws2.merge_cells(f"A1:{openpyxl.utils.get_column_letter(len(gap_cols))}1")
    ws2['A1'] = f"CA POLICY GAPS & RECOMMENDATIONS — {datetime.now().strftime('%B %d, %Y')}"
    ws2['A1'].font = Font(bold=True, color="FFFFFF", name="Arial", size=13)
    ws2['A1'].fill = fills['title']
    ws2['A1'].alignment = Alignment(horizontal='center')
    ws2.row_dimensions[1].height = 24
    for i, (col, w) in enumerate(zip(gap_cols, gap_widths), 1):
        c = ws2.cell(row=2, column=i, value=col)
        c.font = hf; c.fill = fills['header']
        c.alignment = Alignment(horizontal='center'); c.border = thin
        ws2.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for rn, g in enumerate(gaps, 3):
        row_data = [g['Severity'], g['Policy'], g['Issue'], g['Fix']]
        fill = fills.get(g['Severity'], fills['LOW'])
        for cn, val in enumerate(row_data, 1):
            c = ws2.cell(row=rn, column=cn, value=val)
            c.fill = fill; c.border = thin
            c.font = Font(name="Arial", size=10, bold=(cn==1))
    ws2.freeze_panes = 'A3'

today = datetime.now().strftime('%Y%m%d')
out_path = f"{today}_CA_Policy_Audit.xlsx"  # Update to your preferred reports folder
wb.save(out_path)
print(f"\nReport saved: {out_path}")
```

---

## Step 5 — Remediate Gaps

### Enable a Report-Only Policy
```python
policy_id = "..."  # from the policy list
patch = json.dumps({"state": "enabled"}).encode('utf-8')
h = {**headers, 'Content-Type': 'application/json'}
req = urllib.request.Request(
    f"https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies/{policy_id}",
    data=patch, headers=h, method='PATCH'
)
urllib.request.urlopen(req)
print("Policy enabled")
```

### Create a Legacy Auth Block Policy
```python
legacy_block = {
    "displayName": "Block Legacy Authentication",
    "state": "enabled",
    "conditions": {
        "users": {"includeUsers": ["All"]},
        "applications": {"includeApplications": ["All"]},
        "clientAppTypes": ["exchangeActiveSync", "other"]
    },
    "grantControls": {
        "operator": "OR",
        "builtInControls": ["block"]
    }
}
data = json.dumps(legacy_block).encode('utf-8')
h = {**headers, 'Content-Type': 'application/json'}
req = urllib.request.Request(
    "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies",
    data=data, headers=h, method='POST'
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
print(f"Legacy auth block policy created: {result['id']}")
```

---

## Summary Output Format

```
CONDITIONAL ACCESS AUDIT — [Date]
====================================
Total policies  : [N]
  Enforced      : [N]  ← Active and blocking
  Report-only   : [N]  ← Monitoring only, NOT enforcing
  Disabled      : [N]  ← Not active

GAPS FOUND: [N]
  [CRITICAL] No MFA policy found
  [HIGH]     Legacy auth not blocked
  [HIGH]     Report-only policies not enforced
  [MEDIUM]   [N] users excluded from MFA requirement

RECOMMENDED PRIORITY:
  1. Enable report-only policies
  2. Block legacy authentication
  3. Review MFA exclusions

FILE: [date]_CA_Policy_Audit.xlsx
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Re-extract from Entra console |
| 403 on CA policies | Insufficient permissions | Requires Global Admin, Security Admin, or Conditional Access Admin |
| Empty policies list | No CA policies exist | That itself is a critical gap — all logins are unrestricted |
| PATCH returns 400 | Invalid state value | Valid values: "enabled", "disabled", "enabledForReportingButNotEnforced" |

---

## Optional — Update Your Security Dashboard

If you maintain a security dashboard, record the key metrics: policy count, enabled vs
disabled vs report-only, gaps identified, and any changes made. If Notion is connected
via MCP, use `notion-fetch` and `notion-update-page` to refresh your dashboard automatically.

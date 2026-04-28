---
name: m365-threat-scan
description: >
  Scan a Microsoft 365 tenant for active security threats, compromised accounts, and
  suspicious sign-in activity using Entra Identity Protection. Use this skill whenever
  any IT admin wants to check for hacked accounts, run a security threat check,
  investigate suspicious login activity, see if any staff accounts are at risk, find
  credential stuffing or password spray attacks, check for accounts flagged by Microsoft,
  dismiss risk flags after password resets, generate a compromised accounts report, or
  produce an executive security summary. Triggers on: "threat scan", "check for hacked
  accounts", "who's been compromised", "run security check", "any phishing attacks",
  "Identity Protection", "risky users", "suspicious logins", "active attacks on 365",
  "security report for leadership", "compromised accounts", or any concern about account
  compromise or active threats in Microsoft 365.
---

# M365 Threat Scan Skill

This skill runs a complete security threat scan of your Microsoft 365 tenant using
Entra Identity Protection and the Microsoft Graph API.

---

## Step 1 — Get the Bearer Token

All Graph API calls need a bearer token from an active Entra admin session.

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

## Step 2 — Pull All Threat Data

Fetch risky users, risk detections, and security alerts in parallel using separate calls.
Cache the results — some endpoints are slow and you don't want to re-fetch during analysis.

```python
import urllib.request, json

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

# Risky users (current state)
risky_users = graph_get(
    "https://graph.microsoft.com/v1.0/identityProtection/riskyUsers"
    "?$select=id,userDisplayName,userPrincipalName,riskLevel,riskState,riskLastUpdatedDateTime"
)

# Detailed risk detections (individual events)
risk_detections = graph_get(
    "https://graph.microsoft.com/v1.0/identityProtection/riskDetections"
    "?$select=id,userDisplayName,userPrincipalName,riskLevel,riskEventType,"
    "detectedDateTime,location,ipAddress,additionalInfo"
    "&$orderby=detectedDateTime%20desc&$top=100"
)

# Save for analysis
with open('/tmp/security_results.json', 'w') as f:
    json.dump({'risky_users': risky_users, 'risk_detections': risk_detections}, f)

print(f"Risky users found    : {len(risky_users)}")
print(f"Risk detections found: {len(risk_detections)}")
```

---

## Step 3 — Identify Active Threats

Focus on accounts with `riskState = "atRisk"` or `"confirmedCompromised"`. Users in
`"remediated"` or `"dismissed"` state have already been handled.

```python
# Group detections by user
from collections import defaultdict

detections_by_user = defaultdict(list)
for d in risk_detections:
    detections_by_user[d['userPrincipalName']].append(d)

# Find active threats
active_threats = [u for u in risky_users
                  if u['riskState'] in ('atRisk', 'confirmedCompromised')]

print(f"\nACTIVE THREATS: {len(active_threats)} accounts need attention\n")

for user in sorted(active_threats, key=lambda u: {'high': 0, 'medium': 1, 'low': 2}.get(u['riskLevel'], 3)):
    upn = user['userPrincipalName']
    detections = detections_by_user.get(upn, [])

    # Summarize attack geography
    countries = list(set(
        d.get('location', {}).get('countryOrRegion', 'Unknown')
        for d in detections
        if d.get('location')
    ))

    # Summarize attack types
    event_types = list(set(d.get('riskEventType', '') for d in detections))

    print(f"  {user['userDisplayName']} ({upn})")
    print(f"    Risk Level  : {user['riskLevel'].upper()}")
    print(f"    Risk State  : {user['riskState']}")
    print(f"    Detections  : {len(detections)}")
    print(f"    Countries   : {', '.join(countries) if countries else 'Unknown'}")
    print(f"    Event types : {', '.join(event_types)}")
    print(f"    Last event  : {user.get('riskLastUpdatedDateTime', 'N/A')}")
    print()
```

### Reading the Risk Levels

| Level | Meaning | Urgency |
|-------|---------|---------|
| **HIGH** | Active credential stuffing or confirmed breach | Immediate password reset |
| **MEDIUM** | Suspicious activity or leaked credentials being tested | Reset within 24 hours |
| **LOW** | Anomalous but not conclusive | Monitor; reset recommended |
| remediated | Already resolved (password reset completed) | No action needed |
| dismissed | Manually cleared by admin | No action needed |

---

## Step 4 — Understanding the Attack Pattern

For each HIGH/MEDIUM account, analyze the detections to understand the attack:

```python
for upn, detections in detections_by_user.items():
    if not any(u['userPrincipalName'] == upn and u['riskState'] == 'atRisk'
               for u in risky_users):
        continue

    print(f"\nAttack analysis for {upn}:")

    # IP ranges seen
    ips = [d.get('ipAddress', '') for d in detections if d.get('ipAddress')]
    print(f"  IPs seen: {', '.join(set(ips))}")

    # Parse additionalInfo for context
    for d in detections[:5]:  # Show 5 most recent
        info = d.get('additionalInfo', '')
        try:
            parsed = json.loads(info) if info else []
            notes = [item.get('value') for item in parsed if item.get('value')]
        except:
            notes = [info] if info else []
        print(f"  [{d.get('detectedDateTime','?')[:10]}] {d.get('riskEventType')} — {', '.join(notes)}")
```

**Common attack patterns to watch for:**
- **anonymizedIPAddress** + multiple countries = VPN/proxy credential stuffing
- **unfamiliarFeatures** = sign-in from a new device/browser/location
- **leakedCredentials** = password found in dark web breach dump
- **maliciousIPAddress** = known-bad IP (threat intelligence hit)
- **passwordSpray** = one password tried across many accounts

---

## Step 5 — Verify SSPR Access

Before asking users to reset their own passwords, confirm they can actually reach
the self-service reset portal:

```python
# Check that SSPR is scoped correctly
sspr_url = ("https://graph.microsoft.com/beta/policies/authenticationMethodsPolicy"
            "/authenticationMethodConfigurations/Email")
req = urllib.request.Request(sspr_url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        print("SSPR policy active")
except:
    print("Could not verify SSPR — check manually at aka.ms/sspr")

# Verify each at-risk user is in a group with SSPR access
for user in active_threats:
    uid = user['id']
    group_url = (f"https://graph.microsoft.com/v1.0/users/{uid}/memberOf"
                 f"?$select=displayName,id")
    req = urllib.request.Request(group_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        groups_data = json.loads(resp.read())
    group_names = [g['displayName'] for g in groups_data.get('value', [])]
    print(f"  {user['userDisplayName']}: {', '.join(group_names[:3])}")
```

The self-service reset link is: **https://aka.ms/sspr**

---

## Step 6 — Generate Excel Report

Create a color-coded Excel workbook for the IT record and executive review.

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Compromised Accounts"

# Color fills
fills = {
    'HIGH':   PatternFill("solid", fgColor="FFD7D7"),
    'MEDIUM': PatternFill("solid", fgColor="FFE5CC"),
    'LOW':    PatternFill("solid", fgColor="FFFACC"),
    'header': PatternFill("solid", fgColor="1F3864"),
    'title':  PatternFill("solid", fgColor="2E75B6")
}
header_font = Font(bold=True, color="FFFFFF", name="Arial", size=11)
thin = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)

# Title row
ws.merge_cells('A1:H1')
ws['A1'] = f"COMPROMISED / AT-RISK ACCOUNTS — PASSWORD RESET REQUIRED — {datetime.now().strftime('%B %d, %Y')}"
ws['A1'].font = Font(bold=True, color="FFFFFF", name="Arial", size=13)
ws['A1'].fill = fills['title']
ws['A1'].alignment = Alignment(horizontal='center')
ws.row_dimensions[1].height = 24

# Column headers
cols = ['Name', 'Email', 'Risk Level', '# Detections', 'Last Detection',
        'Attack Countries', 'Attack Types', 'Action Required']
widths = [20, 32, 12, 14, 18, 28, 30, 25]

for i, (col, w) in enumerate(zip(cols, widths), 1):
    cell = ws.cell(row=2, column=i, value=col)
    cell.font = header_font
    cell.fill = fills['header']
    cell.alignment = Alignment(horizontal='center')
    cell.border = thin
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

# Data rows
for row_num, user in enumerate(active_threats, 3):
    upn = user['userPrincipalName']
    detections = detections_by_user.get(upn, [])
    level = user.get('riskLevel', 'unknown').upper()

    countries = ', '.join(set(
        d.get('location', {}).get('countryOrRegion', '')
        for d in detections if d.get('location', {}).get('countryOrRegion')
    ))
    attack_types = ', '.join(set(d.get('riskEventType', '') for d in detections))
    last_det = user.get('riskLastUpdatedDateTime', '')[:10]

    row_data = [
        user.get('userDisplayName', ''),
        upn,
        level,
        len(detections),
        last_det,
        countries,
        attack_types,
        'Immediate password reset required'
    ]

    fill = fills.get(level, PatternFill("solid", fgColor="FFFFFF"))
    for col_num, value in enumerate(row_data, 1):
        cell = ws.cell(row=row_num, column=col_num, value=value)
        cell.fill = fill
        cell.border = thin
        cell.font = Font(name="Arial", size=10)

ws.freeze_panes = 'A3'

today = datetime.now().strftime('%Y%m%d')
out_path = f"{today}_Threat_Scan.xlsx"  # Update to your preferred reports folder
wb.save(out_path)
print(f"Report saved: {out_path}")
```

---

## Step 7 — Draft Reset Emails

For each at-risk user, draft a clear email they can act on immediately:

```
Subject: Action Required — Please Reset Your Password Today

Hi [Name],

Our IT security system has detected unusual login activity on your account. As a
precaution, we need you to reset your password today.

Please go to: https://aka.ms/sspr

This link will walk you through the reset in about 2 minutes. If you have any
trouble, please contact IT directly.

This is important — please complete it today.

[Your Name]
[Your Organization] IT Department
```

Customize each email with the user's name and, if appropriate, a brief non-alarming
note about what was detected (e.g., "we saw some unusual login attempts from overseas").

---

## Step 8 — Dismiss Risk Flags After Resets

Once the user confirms passwords have been reset, dismiss the atRisk flags.
**Important:** Always look up user IDs from the risky users list directly rather
than constructing UPNs from memory. Use the primary UPN domain, not alias domains.

```python
# Get IDs from the risky users list (most reliable source)
ids_to_dismiss = [u['id'] for u in active_threats
                  if u['riskState'] in ('atRisk', 'confirmedCompromised')]

if ids_to_dismiss:
    payload = json.dumps({"userIds": ids_to_dismiss}).encode('utf-8')
    h = {**headers, 'Content-Type': 'application/json'}
    req = urllib.request.Request(
        "https://graph.microsoft.com/v1.0/identityProtection/riskyUsers/dismiss",
        data=payload, headers=h, method='POST'
    )
    urllib.request.urlopen(req)
    print(f"Dismissed risk flags for {len(ids_to_dismiss)} accounts")
else:
    print("No active flags to dismiss (password resets may have auto-remediated them)")
```

**Note:** When a user resets their password via SSPR, Entra automatically moves their
risk state from `atRisk` → `remediated`. Manual dismissal is only needed if you reset
the password through the admin portal rather than letting the user use SSPR.

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 401 | Token expired | Re-extract token from Entra console |
| Empty risky users list | No current threats, or all remediated | That's good news — check state field |
| User not found by UPN | Wrong domain (alias vs. primary) | Search by display name, use primary UPN |
| 400 on dismiss | Empty user IDs list | Check `active_threats` list before dismissing |
| `userStates` field error | v2 alerts schema is different | Use risky users + detections endpoints instead |

---

## Summary Output Format

Always end with a clear executive summary:

```
TENANT SECURITY SCAN — [Date]
================================
Total risky users flagged  : [N]
  Active threats (atRisk)  : [N]  ← Need action
  Already remediated        : [N]  ← Password reset completed
  Dismissed                 : [N]  ← Manually cleared

ACTIVE THREATS:
  [Name] — [Risk Level] — [N] detections — [Countries]
  Action: Immediate password reset via aka.ms/sspr

FILES GENERATED:
  [date]_Threat_Scan.xlsx
```

---

## Optional — Update Your Security Dashboard

If you maintain a security dashboard (Notion, SharePoint, etc.), record the key metrics
from this scan: active threats count, remediated count, dismissed count, and any accounts
still requiring action. If Notion is connected via MCP, use `notion-fetch` and
`notion-update-page` to refresh your dashboard automatically.

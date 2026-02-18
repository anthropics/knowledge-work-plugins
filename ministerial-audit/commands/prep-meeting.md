---
name: prep-meeting
description: Prepare for a Cabinet Committee, Select Committee, or departmental meeting by simulating pushback and stress-testing.
arguments:
  - name: document
    description: The proposal, brief, or bill to prepare for.
  - name: forum
    description: (Optional) The meeting type (Cabinet, Select Committee, Departmental Briefing).
---

# /prep-meeting Command

Wargame your proposal and prepare for hostile questioning from colleagues, officials, or the opposition.

## When to Use

Use this command when:
- You are going into a Cabinet Committee meeting (e.g., Social Policy, Expenditure Review).
- You are preparing for a Select Committee appearance.
- You want to "Wargame" a radical proposal against Treasury/Finance skepticism.
- You need to "X-Ray" a stack of industry/lobbyist submissions before a meeting.

## Workflow

### 1. Forum Selection

Identify the pressure points:
- **Cabinet Room**: Focus on inter-departmental conflict (Treasury/AG).
- **Select Committee**: Focus on political "gotchas" and stakeholder criticism.
- **Departmental Brief**: Focus on cutting through "Officialese" and "Slow-walking."

### 2. Stress-Testing (Using wargaming skill)

- **Cabinet Sim**: Run the "Hardest 5 Questions" from Treasury and Finance.
- **Lobbyist X-Ray**: If external documents are provided, decode the hidden "Ask."
- **Precedent Search**: Find 1-2 international "Proof of Concept" examples to cite.
- **Edge Case Check**: Run the proposal against a "High-Risk" persona.

### 3. Preparation Output

Generate a **Meeting Prep Pack**:
1. **The "Interrogatory List"**: Sharp questions to ask officials (to put *them* on the spot).
2. **Defensive Q&A**: The "Kill Shot" questions you will be asked, and the best strategic answers.
3. **The Precedent Card**: 2-3 "Talking Points" about international success.
4. **The "X-Ray" Summary**: How to respond to lobbyist pressure in the room.

## Example Session

**User:** `/prep-meeting document: environment_policy_vfinal.pdf forum: "Cabinet Social Policy Committee"`

**System:**
```
Cabinet Prep - Environment Policy

Forum: Social Policy Committee (Treasury & Finance present)

[~] WARGAMING CABINET PUSHBACK...
[~] SEARCHING FOR PRECEDENTS...

PREP PACK READY.

1. The "Treasury Kill-Shot" (Question for YOU):
"The department estimates $500m, but our modeling suggests the 'Deadweight Loss' could exceed 40% due to market distortion. Why aren't we using a market-led tax credit instead?"
- Strategic Response: "The market-led model in Oregon (2022) failed precisely because it couldn't scale for rural sectors. Our model uses a 'Hybrid Trigger' which international precedent suggests is 15% more efficient."

2. The "Official Scrutiny" (Questions to ask THEM):
"Can you walk the committee through why the Oregon failure isn't applicable to your proposed tax credit model?"

3. The Precedent:
Norway (2023) implemented this exact 'Hybrid Trigger' and saw a 12% increase in uptake within 6 months.

4. Edge Case Warning:
Small farmers (under 50 hectares) will be disproportionately hit by the compliance burden. Suggest a 'Simplified Pathway' for them.

Would you like to draft a "Media Holding Statement" based on these risks? [Y/n]
```

## Integration Points

- **Skill**: Uses `~~ministerial-audit/wargaming` for simulation.
- **Upstream**: Uses output from `/audit` or `/brief`.
- **Downstream**: Feeds into `/comms` outputs.

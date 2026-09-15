# Sourcing Look-alikes

Two paths. Apollo when it's connected, web research when it isn't. Both produce a real list.

---

## With Apollo

The primary path. Filter on the profile dimensions, then pull contacts and signals in the same pass.

Useful filters, in rough order of value for this segment:

- Industry and sub-industry
- Employee count band
- Location radius from the owner
- Technologies in use, where it indicates fit
- Recent hiring activity
- Funding or ownership change

Pull contacts by title rather than by name. For SMB targets the decision-maker titles worth searching are owner, president, general manager, operations manager, and facilities manager. Titles vary enormously by trade — check what the owner's existing contacts are called and search for those.

**Clay** is a peer of Apollo (`../../../shared/connector-neutrality.md`): whichever is connected runs the search. Same approach, different tool — `find-and-enrich-company` for the look-alike companies, `find-and-enrich-contacts-at-company` for the people. Both are metered; name the estimated credits before searching.

---

## Without Apollo — web research

Slower, smaller, and often higher quality per row because each company was actually looked at. Do not treat this as degraded output.

### General sources

- Industry association member directories — usually the single best source
- State and county business registries and license lookups
- Chamber of commerce member lists
- Review platforms, filtered by category and geography
- LinkedIn company search
- Local news for expansions, openings, and awards

### By industry

| Industry | Where the list lives |
|---|---|
| Trades and construction | Contractor license databases, permit filings, builder association rosters |
| Healthcare | State provider directories, practice association lists, facility licensing records |
| Restaurants and retail | Health inspection databases, delivery platform listings, mall and district directories |
| Professional services | Bar and CPA association directories, industry award lists |
| Manufacturing | Supplier directories, trade show exhibitor lists, industry registries |
| Nonprofits | Grantmaker databases, state charity registries, foundation 990 filings |
| Property management | Property records, apartment association rosters, listing sites |

**Permit and license filings are the most underrated source for trades.** They are public, dated, and a filing is itself a buying signal.

### Contact discovery without a data provider

- Company website team and about pages
- Public filings that name officers
- Association member listings, which often include a named contact
- Review responses, which are frequently signed by the owner

When a contact cannot be found, keep the company and mark the contact unknown. Do not drop a good-fit company because the name is missing — the owner may already know them.

---

## How many rows

Target 40 to 60 companies.

A five-hundred-row scrape looks impressive and gets ignored, because the owner cannot tell which twenty to start with and the effort of finding out exceeds the effort of the original manual process. Forty researched rows with a reason attached each get worked.

If the profile is genuinely narrow and only 12 companies exist, deliver 12 and say so. A short honest list is fine. Padding it with poor fits to hit a number destroys the ranking, which is the entire value of the deliverable.

---

## Verification

Before a row goes on the list, confirm the company still exists and still matches. Directories go stale, businesses close, and a list with dead companies on it gets abandoned after the third bounce.

Check the website resolves and the business looks active. This is quick and it is the difference between a list that gets worked and one that gets deleted.

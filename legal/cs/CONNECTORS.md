# Konektory

## Jak fungují odkazy na nástroje

Soubory pluginu používají `~~kategorie` jako zástupný symbol pro nástroj, který si v dané kategorii připojíte. Například `~~cloud storage` může znamenat Box, Egnyte nebo jakéhokoli jiného poskytovatele úložiště s MCP serverem.

Pluginy jsou **nezávislé na konkrétním nástroji** — popisují workflow v pojmech kategorií (cloud storage, chat, kancelářský balík atd.), nikoli konkrétních produktů. Soubor `.mcp.json` předkonfigurovává konkrétní MCP servery, ale funguje jakýkoli MCP server v dané kategorii.

## Konektory pro tento plugin

| Kategorie | Zástupný symbol | Zahrnuté servery | Další možnosti |
|-----------|-----------------|------------------|----------------|
| Právní zdroje ČR/EU | `~~pravni-zdroje` | DirectCase (judikatura, zákony, regulatorika) | vlastní právní databáze |
| Kalendář | `~~calendar` | Google Calendar | Microsoft 365 |
| Chat | `~~chat` | Slack | Microsoft Teams |
| Cloud storage | `~~cloud storage` | Box, Egnyte | Dropbox, SharePoint, Google Drive |
| CLM | `~~CLM` | — | Ironclad, Agiloft |
| CRM | `~~CRM` | — | Salesforce, HubSpot |
| E-mail | `~~email` | Gmail | Microsoft 365 |
| Elektronický podpis | `~~e-signature` | DocuSign | Adobe Sign (kvalifikovaný podpis dle eIDAS) |
| Kancelářský balík | `~~office suite` | Microsoft 365 | Google Workspace |
| Nástroj pro řízení projektů | `~~project tracker` | Atlassian (Jira/Confluence) | Linear, Asana |

## DirectCase — primární zdroj českého práva

`DirectCase` je MCP server specializovaný na české a evropské právo. Obsahuje cca 1,4 milionu ověřených právních zdrojů:

- **Judikaturu** českých soudů (NS, ÚS, NSS, vrchní a krajské soudy)
- **Právní předpisy ČR** (zákony, nařízení vlády, vyhlášky)
- **Regulatorní dokumenty** (ČNB, ÚOOÚ, ÚOHS a další)
- **Dokumenty obchodního rejstříku** a veřejných rejstříků

Endpoint: `https://mcp.directcase.ai/mcp`

Dostupné nástroje zahrnují paralelní vyhledávání v judikatuře, zákonech a regulatorních předpisech, vyhledávání podle identifikátoru dokumentu (ECLI, Sb., atd.), vyhledávání společností a jejich dokumentů a načítání plného textu dokumentů včetně PDF.

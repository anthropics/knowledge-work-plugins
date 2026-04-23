# Legal Productivity Plugin — česká verze

AI-poháněný produktivní plugin pro interní právní týmy v české a evropské jurisdikci. Primárně určený pro [Cowork](https://claude.com/product/cowork), agentickou desktopovou aplikaci Anthropicu — funguje ale i v Claude Code. Automatizuje revizi smluv, triage NDA, compliance workflow, právní přehledy a šablonové odpovědi — vše konfigurovatelné podle interní playbook a tolerance rizika vaší organizace.

> **Upozornění:** Tento plugin pomáhá s právními workflow, ale neposkytuje právní poradenství ve smyslu zákona č. 85/1996 Sb. o advokacii. Veškeré závěry ověřte u kvalifikovaného advokáta. Výstupy generované AI by měl před použitím pro právní rozhodnutí zkontrolovat právník oprávněný k výkonu advokacie v ČR nebo příslušné jurisdikci. Výchozí příklady playbooku v tomto pluginu vycházejí z českého a evropského práva (GDPR, zák. č. 89/2012 Sb. občanský zákoník, zák. č. 90/2012 Sb. o obchodních korporacích). Pokud působíte v jiném právním systému, je nutné playbook v `legal.local.md` přizpůsobit dané jurisdikci.

## Cílové persony

- **Obchodní právník (Commercial Counsel)** — vyjednávání smluv, správa dodavatelů, podpora obchodu
- **Produktový právník (Product Counsel)** — revize produktů, obchodní podmínky, zásady ochrany osobních údajů, duševní vlastnictví
- **Compliance / ochrana osobních údajů** — GDPR a zák. č. 110/2019 Sb., revize DPA, žádosti subjektů údajů, monitoring regulatorních změn (NIS2, DORA, AI Act)
- **Podpora sporové agendy** — zajištění dokumentů (litigation hold), příprava podkladů pro spor, přehledy kauz

## Instalace

```
claude plugins add knowledge-work-plugins/legal-cs
```

## Rychlý start

### 1. Nainstalujte plugin

```
claude plugins add knowledge-work-plugins/legal-cs
```

### 2. Nakonfigurujte playbook

Vytvořte lokální konfigurační soubor, ve kterém definujete standardní pozice vaší organizace. Zde kódujete vyjednávací playbook týmu, toleranci rizika a standardní smluvní podmínky.

Vytvořte soubor `legal.local.md` tam, kde ho Claude najde:

- **Cowork**: Uložte ho do libovolné složky sdílené s Coworkem (přes výběr složek). Plugin ho najde automaticky.
- **Claude Code**: Uložte ho do adresáře `.claude/` projektu.

```markdown
# Konfigurace právního playbooku

## Pozice pro revizi smluv

### Omezení odpovědnosti
- Standardní pozice: vzájemný strop ve výši 12 měsíců zaplacených/splatných poplatků
- Přijatelné rozpětí: 6–24 měsíců poplatků
- Spouštěč eskalace: neomezená odpovědnost, zahrnutí následných škod

### Odškodnění (indemnifikace)
- Standardní pozice: vzájemné odškodnění za porušení duševního vlastnictví a porušení zabezpečení osobních údajů
- Přijatelné: odškodnění omezené pouze na nároky třetích stran
- Spouštěč eskalace: jednostranné povinnosti odškodnění, neomezené odškodnění

### Duševní vlastnictví
- Standardní pozice: každá strana si ponechává dříve existující duševní vlastnictví; zákazník vlastní svá data
- Spouštěč eskalace: široká ustanovení o postoupení duševního vlastnictví, klauzule „dílo na objednávku" pro dříve existující duševní vlastnictví

### Ochrana osobních údajů
- Standardní pozice: vyžadovat DPA pro jakékoli zpracování osobních údajů (GDPR čl. 28)
- Požadavky: notifikace subzpracovatelů, výmaz dat při ukončení, oznámení porušení zabezpečení do 72 hodin (GDPR čl. 33)
- Spouštěč eskalace: DPA nenabídnuta, přeshraniční předání bez záruk (SCC / rozhodnutí o odpovídající ochraně)

### Doba trvání a ukončení
- Standardní pozice: roční doba s 30denní výpovědní lhůtou bez udání důvodu
- Přijatelné: víceleté s možností výpovědi po uplynutí počáteční doby
- Spouštěč eskalace: automatické prodloužení bez oznamovací lhůty, bez možnosti výpovědi bez udání důvodu

### Rozhodné právo
- Preferované: české právo
- Přijatelné: respektované obchodní jurisdikce (anglické právo, německé právo)
- Spouštěč eskalace: nestandardní jurisdikce, povinná arbitráž v nevhodném místě

## Výchozí pozice pro NDA
- Vyžaduje se vzájemnost závazků
- Doba: 2–3 roky standardně, 5 let pro obchodní tajemství (§ 504 OZ)
- Standardní výjimky: nezávisle vyvinuté, veřejně dostupné, oprávněně získané od třetí strany
- Doložka o reziduálech: přijatelná, pokud je úzce vymezená

## Šablony odpovědí
Nakonfigurujte cesty k souborům se šablonami nebo definujte šablony inline pro běžné dotazy.
```

### 3. Připojte si nástroje

Plugin funguje nejlépe, když je propojen s vašimi stávajícími nástroji přes MCP. Předkonfigurované servery zahrnují **DirectCase** (české právo a judikatura), Slack, Box, Egnyte, Atlassian a Microsoft 365. Kompletní seznam podporovaných kategorií najdete v [CONNECTORS.md](CONNECTORS.md).

## Příkazy

### `/revize-smlouvy` — revize smlouvy podle playbooku

Zreviduje smlouvu podle vyjednávacího playbooku vaší organizace. Označí odchylky, vygeneruje úpravy (redline) a poskytne analýzu obchodního dopadu.

```
/revize-smlouvy
```

Akceptuje: nahraný soubor, URL nebo vložený text smlouvy. Zeptá se na kontext (vaše strana, termín, zaměření) a provede revizi ustanovení po ustanovení proti nakonfigurovanému playbooku.

### `/triage-nda` — prescreening NDA

Rychlá triage přijatých NDA podle standardních kritérií. Kategorizuje jako ZELENÁ (standardní schválení), ŽLUTÁ (revize právníkem) nebo ČERVENÁ (významné problémy).

```
/triage-nda
```

### `/kontrola-dodavatele` — stav smluv s dodavatelem

Zkontroluje stav stávajících smluv s dodavatelem napříč připojenými systémy.

```
/kontrola-dodavatele [jméno dodavatele]
```

Reportuje existující NDA, rámcové smlouvy (MSA), DPA, data platnosti a klíčové podmínky.

### `/prehled-pravni` — přehled pro právní tým

Vygeneruje kontextové přehledy pro vaši právní agendu.

```
/prehled-pravni daily          # Ranní přehled právně relevantních položek
/prehled-pravni topic [dotaz]  # Rešerše na konkrétní právní otázku
/prehled-pravni incident       # Rychlý přehled vyvíjející se situace
```

### `/pravni-odpoved` — vygeneruj šablonovou odpověď

Vygeneruje odpověď z nakonfigurovaných šablon pro běžné typy dotazů.

```
/pravni-odpoved [typ-dotazu]
```

Podporované typy dotazů zahrnují: žádost subjektu údajů (GDPR), litigation hold, dotaz dodavatele, žádost o NDA a vlastní kategorie, které si definujete.

## Skills (dovednosti)

| Skill | Popis |
|-------|-------|
| `revize-smlouvy` | Analýza smlouvy podle playbooku, klasifikace odchylek, generování úprav (redline) |
| `triage-nda` | Kritéria pro screening NDA, klasifikace, doporučení routování |
| `kontrola-souladu` | GDPR, zák. č. 110/2019 Sb., revize DPA, žádosti subjektů údajů, NIS2/DORA/AI Act |
| `pravni-odpoved` | Správa šablon, kategorie odpovědí, spouštěče eskalace |
| `posouzeni-pravniho-rizika` | Framework závažnosti rizika, úrovně klasifikace, kritéria pro eskalaci |
| `priprava-jednani` | Metodika přípravy na jednání, sběr kontextu, sledování úkolů |
| `prehled-pravni` | Denní, tematické a incidenční přehledy pro právní tým |
| `kontrola-dodavatele` | Přehled smluv s dodavatelem, platnost, klíčové podmínky |
| `zadost-o-podpis` | Workflow pro elektronický podpis (eIDAS, zák. č. 297/2016 Sb.) |

## Příklady workflow

### Revize smlouvy

1. Přijmete smlouvu od dodavatele e-mailem
2. Spustíte `/revize-smlouvy` a nahrajete dokument
3. Poskytnete kontext: „Jsme zákazník, potřebujeme uzavřít do konce kvartálu, zaměřte se na ochranu osobních údajů a odpovědnost"
4. Obdržíte analýzu ustanovení po ustanovení s označením ZELENÁ/ŽLUTÁ/ČERVENÁ
5. Dostanete konkrétní návrh úprav (redline) pro ŽLUTÉ a ČERVENÉ položky
6. Sdílíte analýzu s obchodním týmem

### Triage NDA

1. Obchodní tým vám pošle NDA od nového prospekta
2. Spustíte `/triage-nda` a vložíte nebo nahrajete NDA
3. Dostanete okamžitou klasifikaci: ZELENÁ (směrovat k podpisu), ŽLUTÁ (konkrétní body k revizi) nebo ČERVENÁ (vyžaduje plnou revizi právníkem)
4. Pro ZELENÉ NDA schválíte přímo; pro ŽLUTÉ/ČERVENÉ řešíte označené body

### Denní přehled

1. Začnete ráno s `/prehled-pravni daily`
2. Dostanete souhrn nočních žádostí o smlouvy, compliance dotazů, nadcházejících termínů a kalendářních položek vyžadujících právní přípravu
3. Podle naléhavosti a termínů si priorizujete den

### Kontrola dodavatele

1. Obchodní tým se ptá na nové zadání u stávajícího dodavatele
2. Spustíte `/kontrola-dodavatele Acme s.r.o.`
3. Uvidíte stávající smlouvy, data platnosti a klíčové podmínky na jedno pohlednutí
4. Okamžitě víte, zda potřebujete novou NDA nebo můžete pokračovat podle stávajících podmínek

## MCP integrace

> Pokud vidíte neznámé zástupné symboly nebo potřebujete zkontrolovat, které nástroje jsou připojeny, podívejte se do [CONNECTORS.md](CONNECTORS.md).

Plugin se připojuje k vašim nástrojům přes MCP (Model Context Protocol) servery:

| Kategorie | Příklady | Účel |
|-----------|----------|------|
| Právní zdroje ČR/EU | **DirectCase** | Judikatura, zákony, regulatorika, obchodní rejstřík |
| Chat | Slack, Teams | Týmové žádosti, oznámení, triage |
| Cloud storage | Box, Egnyte | Playbooky, šablony, precedensy |
| Kancelářský balík | Microsoft 365 | E-mail, kalendář, dokumenty |
| Nástroj pro řízení projektů | Atlassian (Jira/Confluence) | Sledování kauz, úkoly |

Kompletní seznam podporovaných integrací — včetně CLM, CRM, elektronického podpisu a dalších možností — najdete v [CONNECTORS.md](CONNECTORS.md).

Připojení konfigurujte v `.mcp.json`. Plugin degraduje elegantně, když nástroje nejsou dostupné — upozorní na chybějící části a navrhne manuální kontroly.

## Přizpůsobení

### Konfigurace playbooku

Váš playbook je srdcem systému revize smluv. Definujte pozice v `legal.local.md`:

- **Standardní pozice**: vaše preferované smluvní podmínky
- **Přijatelná rozpětí**: s čím můžete souhlasit bez eskalace
- **Spouštěče eskalace**: podmínky vyžadující revizi vedoucího právníka nebo externího advokáta

### Šablony odpovědí

Definujte šablony pro běžné dotazy. Šablony podporují dosazení proměnných a zahrnují vestavěné spouštěče eskalace pro situace, které by šablonovou odpověď využívat neměly.

### Framework rizika

Přizpůsobte matici posouzení rizika tak, aby odpovídala riziku apetitu vaší organizace a schématu klasifikace.

## Struktura souborů

```
legal/cs/
├── .claude-plugin/plugin.json
├── .mcp.json
├── README.md
├── CONNECTORS.md
└── skills/
    ├── revize-smlouvy/SKILL.md
    ├── triage-nda/SKILL.md
    ├── kontrola-souladu/SKILL.md
    ├── pravni-odpoved/SKILL.md
    ├── posouzeni-pravniho-rizika/SKILL.md
    ├── priprava-jednani/SKILL.md
    ├── prehled-pravni/SKILL.md
    ├── kontrola-dodavatele/SKILL.md
    └── zadost-o-podpis/SKILL.md
```

## Další informace

Pro informace o DirectCase (MCP server s českou judikaturou, zákony a regulatorikou) navštivte [blog.directcase.ai/cs](https://blog.directcase.ai/cs/).

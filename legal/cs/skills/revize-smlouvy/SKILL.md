---
name: revize-smlouvy
description: Proveďte revizi smlouvy oproti vyjednávacímu playbooku vaší organizace — označte odchylky, vygenerujte návrhy úprav (redlines) a poskytněte analýzu obchodních dopadů. Použijte při revizi smluv s dodavateli nebo zákazníky, když potřebujete analýzu ustanovení po ustanovení proti standardním pozicím, nebo při přípravě vyjednávací strategie s prioritizovanými návrhy úprav a ústupovými pozicemi.
argument-hint: "<soubor se smlouvou nebo text>"
---

# /revize-smlouvy -- Revize smlouvy oproti playbooku

> Pokud narazíte na neznámé zástupné symboly nebo si potřebujete ověřit, které nástroje jsou připojeny, viz [CONNECTORS.md](../../CONNECTORS.md).

Proveďte revizi smlouvy oproti vyjednávacímu playbooku (interní příručce) vaší organizace. Analyzujte jednotlivá ustanovení, označte odchylky, vygenerujte návrhy úprav (redlines) a poskytněte analýzu obchodních dopadů.

**Důležité**: Tento plugin pomáhá s právními workflow, ale neposkytuje právní poradenství ve smyslu zákona č. 85/1996 Sb. o advokacii. Veškeré závěry ověřte u kvalifikovaného advokáta.

## Vyvolání

```
/revize-smlouvy <soubor se smlouvou nebo URL>
```

Proveďte revizi smlouvy: @$1

## Pracovní postup

### Krok 1: Převzetí smlouvy

Smlouvu lze převzít v libovolném z těchto formátů:
- **Nahraný soubor**: PDF, DOCX nebo jiný formát dokumentu
- **URL**: Odkaz na smlouvu v CLM systému, cloudovém úložišti (např. Box, Egnyte, SharePoint) nebo jiném systému pro správu dokumentů
- **Vložený text**: Text smlouvy vložený přímo do konverzace

Pokud smlouva není poskytnuta, vyzvěte uživatele, aby ji dodal.

### Krok 2: Získání kontextu

Před zahájením revize se uživatele zeptejte na kontext:

1. **Na které straně stojíte?** (dodavatel/poskytovatel, zákazník/odběratel, poskytovatel licence, nabyvatel licence, partner — nebo jiné)
2. **Termín**: Kdy musí být smlouva finalizována? (Ovlivňuje prioritizaci jednotlivých otázek.)
3. **Klíčové oblasti**: Máte konkrétní obavy? (např. „ochrana osobních údajů je zásadní", „potřebujeme flexibilitu v době trvání", „vlastnictví duševního vlastnictví je klíčové téma")
4. **Kontext obchodu**: Jaký je relevantní obchodní kontext? (např. velikost obchodu, strategický význam, stávající vztah)

Pokud uživatel poskytne pouze částečný kontext, pokračujte s tím, co máte, a zaznamenejte učiněné předpoklady.

### Krok 3: Načtení playbooku

Vyhledejte playbook pro revizi smluv vaší organizace v lokálním nastavení (např. `legal.local.md` nebo podobné konfigurační soubory).

Playbook by měl definovat:
- **Standardní pozice**: Preferované podmínky organizace pro každý důležitý typ ustanovení
- **Přijatelné rozsahy**: Podmínky, které lze odsouhlasit bez eskalace
- **Spouštěče eskalace**: Podmínky vyžadující revizi vedoucím právníkem nebo zapojení externího advokáta

**Pokud není žádný playbook nakonfigurován:**
- Informujte uživatele, že playbook nebyl nalezen
- Nabídněte dvě možnosti:
  1. Pomoci uživateli s nastavením playbooku (projít definici pozic pro klíčová ustanovení)
  2. Pokračovat v obecné revizi s využitím široce uznávaných obchodních standardů jako výchozího měřítka
- Při obecném postupu jasně uveďte, že revize vychází z obecných obchodních standardů, nikoli z konkrétních pozic organizace

### Krok 4: Analýza ustanovení po ustanovení

#### Využití DirectCase MCP pro autoritativní kontext

Pokud je připojen **DirectCase MCP** (`https://mcp.directcase.ai/mcp`), použij jej k doplnění analýzy o aktuální českou judikaturu a relevantní zákonná ustanovení:

- **`search_law_parallel`** — vyhledat relevantní ustanovení zákonů k předmětu smlouvy (např. § 2079 a násl. OZ pro kupní smlouvu, § 1746 odst. 2 OZ pro nepojmenované smlouvy, ZOK pro smlouvy o převodu podílu, GDPR + zák. č. 110/2019 Sb. pro DPA).
- **`search_caselaw_parallel`** — vyhledat rozhodnutí NS / ÚS k spornému typu ustanovení (např. platnost smluvní pokuty, přiměřenost omezení odpovědnosti, neplatnost rozhodčí doložky).
- **`search_regulatory_parallel`** — stanoviska regulátorů (ÚOOÚ pro DPA, ÚOHS pro exkluzivitu, ČNB pro finanční služby).
- **`get_law_detail`** — načíst plný text konkrétního ustanovení k přesné citaci.

> **Důležité:** Nástroje `search_caselaw_parallel`, `search_law_parallel` a `search_regulatory_parallel` volej v rámci jedné relace **pouze jednou**. Dotaz formuluj komplexně tak, aby jediné volání pokrylo všechna relevantní témata smlouvy najednou.

Výsledky citujte v analýze pomocí sp. zn. / ECLI / č. Sb.

#### Obecný postup revize

Použijte následující postup revize:

1. **Identifikujte typ smlouvy**: smlouva o SaaS, profesionální služby, licence, partnerství, nákup atd. Typ smlouvy ovlivňuje, která ustanovení jsou nejvýznamnější.
2. **Určete stranu uživatele**: dodavatel, zákazník, poskytovatel licence, nabyvatel licence, partner. Tento aspekt zásadně mění analýzu (např. omezení odpovědnosti chrání jiné strany v různých situacích).
3. **Přečtěte celou smlouvu** dříve, než začnete označovat problémy. Ustanovení na sebe vzájemně působí (např. neomezené odškodnění může být částečně zmírněno širokým omezením odpovědnosti).
4. **Analyzujte každé významné ustanovení** oproti pozici v playbooku.
5. **Posuďte smlouvu jako celek**: Je celkové rozložení rizik a obchodních podmínek vyvážené?

Analyzujte smlouvu systematicky, minimálně v následujícím rozsahu:

| Kategorie ustanovení | Klíčové body revize |
|----------------|-------------------|
| **Omezení odpovědnosti** | Výše limitu, výjimky, vzájemné vs. jednostranné, následné škody |
| **Odškodnění** | Rozsah, vzájemné vs. jednostranné, limit, porušení IP, porušení zabezpečení osobních údajů |
| **Vlastnictví duševního vlastnictví** | Stávající IP, nově vytvořené IP, dílo na objednávku, licenční ujednání, postoupení |
| **Ochrana osobních údajů** | Potřeba DPA, podmínky zpracování, subzpracovatelé, oznámení o porušení, přeshraniční předání |
| **Mlčenlivost** | Rozsah, doba trvání, výjimky, povinnosti vrácení/zničení |
| **Prohlášení a záruky** | Rozsah, zbavení odpovědnosti, doba přetrvání |
| **Doba trvání a ukončení** | Délka, obnovení, ukončení pro vhodnost, ukončení z důvodu, ukončovací lhůta |
| **Rozhodné právo a řešení sporů** | Jurisdikce, místo, rozhodčí řízení vs. soudní spor |
| **Pojištění** | Požadavky na krytí, minima, doklady o pojištění |
| **Postoupení smlouvy** | Požadavky na souhlas, změna ovládání, výjimky |
| **Vyšší moc** | Rozsah, oznámení, právo na ukončení |
| **Platební podmínky** | Splatnost, úroky z prodlení, daně, navyšování cen |

U každého ustanovení posuďte soulad s playbookem (nebo obecnými standardy) a uveďte, zda je přítomné, chybí, nebo je neobvyklé.

#### Podrobné pokyny k jednotlivým ustanovením

##### Omezení odpovědnosti

**Klíčové prvky k revizi:**
- Výše limitu (pevná částka, násobek poplatků nebo neomezeně)
- Zda je limit vzájemný, nebo se vztahuje na každou stranu odlišně
- Výjimky z limitu (které závazky jsou neomezené)
- Zda jsou vyloučeny následné, nepřímé, zvláštní nebo sankční škody
- Zda je vyloučení vzájemné
- Výjimky z vyloučení následných škod
- Zda se limit uplatňuje na jednotlivý nárok, ročně, nebo kumulativně

**Časté problémy:**
- Limit nastavený na zlomek zaplacených poplatků (např. „poplatky zaplacené za předchozí 3 měsíce" u smlouvy s nízkou hodnotou)
- Asymetrické výjimky zvýhodňující stranu, která návrh sepsala
- Široké výjimky, které fakticky limit ruší (např. „jakékoliv porušení článku X", přičemž článek X pokrývá většinu povinností)
- Chybějící vyloučení následných škod pro porušení jedné ze stran

##### Odškodnění

**Klíčové prvky k revizi:**
- Zda je odškodnění vzájemné nebo jednostranné
- Rozsah: co zakládá povinnost odškodnění (porušení IP, porušení zabezpečení osobních údajů, újma na zdraví, porušení prohlášení a záruk)
- Zda je odškodnění limitováno (často podléhá celkovému limitu odpovědnosti, někdy je neomezené)
- Procesní stránka: požadavky na oznámení, právo vést obhajobu, právo na urovnání
- Zda je oprávněná osoba povinna zmírňovat škodu
- Vztah mezi odškodněním a ustanovením o omezení odpovědnosti

**Časté problémy:**
- Jednostranné odškodnění za porušení IP, přestože obě strany IP vnášejí
- Odškodnění za „jakékoli porušení" (příliš široké; fakticky ruší limit odpovědnosti)
- Chybějící právo vést obhajobu nároků
- Povinnosti odškodnění přetrvávající neomezeně po ukončení smlouvy

##### Duševní vlastnictví

**Klíčové prvky k revizi:**
- Vlastnictví stávajícího IP (každá strana by si měla ponechat své)
- Vlastnictví IP vytvořeného během plnění
- Ustanovení o díle na objednávku a jejich rozsah
- Licenční ujednání: rozsah, výlučnost, území, právo udělovat podlicence
- Zohlednění open source
- Ustanovení o zpětné vazbě (licence na návrhy či zlepšení)

**Časté problémy:**
- Široké postoupení IP, které by mohlo zahrnout stávající IP zákazníka
- Ustanovení o díle na objednávku sahající nad rámec dodávek
- Neomezená ustanovení o zpětné vazbě udělující trvalé, neodvolatelné licence
- Rozsah licence širší, než vyžaduje obchodní vztah

##### Ochrana osobních údajů

**Klíčové prvky k revizi:**
- Zda je vyžadována smlouva/dodatek o zpracování osobních údajů (DPA)
- Klasifikace jako správce vs. zpracovatel osobních údajů
- Práva subzpracovatelů a povinnosti oznamování
- Lhůta pro oznámení porušení zabezpečení osobních údajů (72 hodin podle GDPR, čl. 33)
- Mechanismy přeshraničního předání (standardní smluvní doložky (SCC), rozhodnutí o odpovídající úrovni ochrany, závazná podniková pravidla)
- Povinnosti výmazu nebo vrácení údajů při ukončení
- Požadavky na zabezpečení údajů a práva auditu
- Omezení účelu zpracování údajů

Aplikovatelné předpisy zahrnují GDPR a zák. č. 110/2019 Sb. o zpracování osobních údajů.

**Časté problémy:**
- Chybějící DPA při zpracování osobních údajů
- Plošné oprávnění pro subzpracovatele bez oznamovací povinnosti
- Lhůta pro oznámení porušení delší, než vyžaduje regulace
- Chybějící ochrana přeshraničních předání, pokud se data pohybují mezinárodně
- Nedostatečná ustanovení o výmazu údajů

##### Doba trvání a ukončení

**Klíčové prvky k revizi:**
- Počáteční doba trvání a podmínky obnovení
- Ustanovení o automatickém obnovení a lhůty pro vypovězení
- Ukončení pro vhodnost: je možné? výpovědní lhůta? poplatky za předčasné ukončení?
- Ukončení z důvodu porušení: lhůta k nápravě? co zakládá důvod?
- Důsledky ukončení: vrácení dat, asistence při přechodu, doložky o přetrvání
- Ukončovací lhůta a povinnosti v jejím rámci

**Časté problémy:**
- Dlouhá počáteční doba bez možnosti ukončení pro vhodnost
- Automatické obnovení s krátkými lhůtami pro vypovězení (např. 30denní lhůta při ročním obnovení)
- Chybějící lhůta k nápravě u ukončení z důvodu
- Nedostatečná ustanovení o asistenci při přechodu
- Doložky o přetrvání, které fakticky prodlužují smlouvu na neurčito

##### Rozhodné právo a řešení sporů

**Klíčové prvky k revizi:**
- Volba práva (rozhodné právo)
- Mechanismus řešení sporů (soudní spor, rozhodčí řízení, prioritní mediace)
- Místo a soudní příslušnost pro spor
- Pravidla a místo rozhodčího řízení (je-li zvoleno)
- Vzdání se práva na porotu
- Vzdání se práva na hromadnou žalobu
- Úhrada nákladů advokáta vítězné straně

**Časté problémy:**
- Nepříznivá jurisdikce (neobvyklé nebo vzdálené místo)
- Povinné rozhodčí řízení s pravidly zvýhodňujícími navrhovatele
- Vzdání se práva na porotu a hromadnou žalobu: jsou specifické pro americké právo — v českém kontextu zpravidla není relevantní, lze vynechat nebo přizpůsobit rozhodčí doložkou
- Chybějící eskalační proces před zahájením formálního řešení sporu

### Krok 5: Označení odchylek

Klasifikujte každou odchylku od playbooku pomocí třístupňového systému:

#### ZELENÁ — Přijatelné

Ustanovení je v souladu se standardní pozicí organizace, nebo je dokonce výhodnější. Drobné odchylky, které jsou obchodně rozumné a významně nezvyšují riziko.

**Příklady:**
- Limit odpovědnosti na úrovni 18 měsíčních poplatků, když standard je 12 (výhodnější pro zákazníka)
- Vzájemná NDA s dobou trvání 2 roky, když standard jsou 3 roky (kratší, ale rozumné)
- Rozhodné právo v zavedené obchodní jurisdikci blízké té preferované

**Akce**: Zaznamenat pro informaci. Vyjednávání není nutné.

#### ŽLUTÁ — Vyjednávat

Ustanovení je mimo standardní pozici, ale v rámci vyjednatelného rozsahu. Je na trhu běžné, ale neodpovídá preferenci organizace. Vyžaduje pozornost a pravděpodobně jednání, nikoli však eskalaci.

**Příklady:**
- Limit odpovědnosti na 6 měsíců poplatků, když standard je 12 (pod standardem, ale vyjednatelné)
- Jednostranné odškodnění za porušení IP, kdy standardem je vzájemnost (běžná tržní pozice, ale nepreferovaná)
- Automatické obnovení s 60denní výpovědní lhůtou, když standard je 90 dní
- Rozhodné právo v přijatelné, ale nepreferované jurisdikci

**Akce**: Vygenerujte konkrétní text návrhu úpravy (redline). Poskytněte ústupovou pozici. Odhadněte obchodní dopady přijetí vs. vyjednávání.
- **Zahrnout**: Konkrétní text návrhu úpravy, který vrátí ustanovení ke standardní pozici
- **Zahrnout**: Ústupovou pozici pro případ, že protistrana nepřistoupí na primární návrh
- **Zahrnout**: Obchodní dopad přijetí v původní podobě vs. vyjednávání

#### ČERVENÁ — Eskalovat

Ustanovení je mimo přijatelný rozsah, splňuje některý z definovaných spouštěčů eskalace nebo představuje významné riziko. Vyžaduje revizi vedoucím právníkem, zapojení externího advokáta nebo schválení obchodním rozhodujícím subjektem.

**Příklady:**
- Neomezená odpovědnost nebo chybějící ustanovení o omezení odpovědnosti
- Jednostranné široké odškodnění bez limitu
- Postoupení stávajícího IP
- Chybějící DPA při zpracování osobních údajů
- Nepřiměřené konkurenční doložky nebo výlučnost
- Rozhodné právo v problematické jurisdikci s povinným rozhodčím řízením

**Akce**: Vysvětlete konkrétní riziko. Poskytněte tržně standardní alternativní znění. Odhadněte expozici. Doporučte eskalační cestu.
- **Zahrnout**: Proč je to ČERVENÉ (konkrétní riziko)
- **Zahrnout**: Jak vypadá standardní tržní pozice
- **Zahrnout**: Obchodní dopad a potenciální expozici
- **Zahrnout**: Doporučenou eskalační cestu

### Krok 6: Generování návrhů úprav (redlines)

Pro každou ŽLUTOU a ČERVENOU odchylku poskytněte:
- **Současné znění**: Citujte příslušný text smlouvy
- **Navrhovaný redline**: Konkrétní alternativní znění
- **Odůvodnění**: Stručné vysvětlení vhodné ke sdílení s protistranou
- **Priorita**: Zda jde o nezbytné (must-have) nebo vítané (nice-to-have) při vyjednávání

#### Osvědčené postupy při tvorbě redlines

Při generování návrhů úprav:

1. **Buďte konkrétní**: Uveďte přesné znění, nikoli vágní pokyny. Redline má být připravený k vložení.
2. **Buďte vyvážení**: Navrhujte znění, které je pevné u kritických bodů, ale obchodně rozumné. Přehnaně agresivní redlines zpomalují jednání.
3. **Vysvětlete důvod**: Přiložte stručné, profesionální odůvodnění vhodné ke sdílení s právníkem protistrany.
4. **Poskytněte ústupové pozice**: U ŽLUTÝCH položek uveďte ústupovou pozici pro případ zamítnutí hlavního požadavku.
5. **Prioritizujte**: Ne všechny redlines mají stejnou váhu. Uveďte, které jsou nezbytné a které pouze vítané.
6. **Zohledněte vztah**: Přizpůsobte tón a přístup podle toho, zda jde o nového dodavatele, strategického partnera nebo komoditního dodavatele.

#### Formát redline

Pro každý redline:
```
**Ustanovení**: [odkaz na článek a název ustanovení]
**Současné znění**: "[přesná citace ze smlouvy]"
**Navrhovaná úprava**: "[konkrétní alternativní znění s doplněnými pasážemi tučně a konceptuálně přeškrtnutými vymazávanými pasážemi]"
**Odůvodnění**: [1–2 věty s vysvětlením důvodu, vhodné pro externí sdílení]
**Priorita**: [Must-have (nezbytné) / Should-have (žádoucí) / Nice-to-have (vítané)]
**Ústupová pozice**: [Alternativní pozice, pokud bude primární návrh odmítnut]
```

### Krok 7: Shrnutí obchodních dopadů

Poskytněte souhrnnou sekci pokrývající:
- **Celkové posouzení rizika**: Přehled rizikového profilu smlouvy
- **3 hlavní problémy**: Nejdůležitější položky k řešení
- **Vyjednávací strategie**: Doporučený přístup (s čím začít, co ustoupit)
- **Časové aspekty**: Faktory naléhavosti ovlivňující přístup k jednání

#### Rámec priorit pro vyjednávání

Při prezentaci úprav organizujte podle vyjednávací priority:

**Tier 1 — Nezbytné (must-have, deal-breakery)**
Body, bez jejichž vyřešení organizace nemůže pokračovat:
- Neomezené nebo podstatně nedostatečné ochrany odpovědnosti
- Chybějící požadavky na ochranu osobních údajů u regulovaných dat
- Ustanovení o IP, která by mohla ohrozit klíčová aktiva
- Podmínky v rozporu s regulatorními povinnostmi

**Tier 2 — Žádoucí (should-have, silné preference)**
Body, které významně ovlivňují riziko, ale ponechávají prostor k jednání:
- Úpravy limitu odpovědnosti v rámci rozsahu
- Rozsah a vzájemnost odškodnění
- Flexibilita ukončení
- Práva auditu a kontroly compliance

**Tier 3 — Vítané (nice-to-have, kandidáti na ústupky)**
Body, které pozici vylepšují, ale lze je strategicky ustoupit:
- Preferované rozhodné právo (je-li alternativa přijatelná)
- Preference výpovědních lhůt
- Drobná vylepšení definic
- Požadavky na osvědčení o pojištění

**Vyjednávací strategie**: Začněte Tier 1. Za ústupky v Tier 3 si zajistěte úspěchy v Tier 2. V Tier 1 nikdy neustupujte bez eskalace.

### Krok 8: Směrování v CLM (pokud je připojeno)

Pokud je přes MCP připojen systém pro správu životního cyklu smluv (CLM):
- Doporučte vhodné schvalovací workflow podle typu smlouvy a úrovně rizika
- Navrhněte správnou cestu směrování (např. standardní schválení, vedoucí právník, externí advokát)
- Upozorněte na potřebné souhlasy podle hodnoty smlouvy nebo rizikových příznaků

Pokud CLM není připojeno, tento krok přeskočte.

## Formát výstupu

Strukturujte výstup takto:

```
## Shrnutí revize smlouvy

**Dokument**: [název/identifikátor smlouvy]
**Strany**: [jména stran a role]
**Vaše strana**: [dodavatel/zákazník atd.]
**Termín**: [je-li uveden]
**Základ revize**: [Playbook / Obecné standardy]

## Klíčová zjištění

[3–5 hlavních problémů s označením závažnosti]

## Analýza ustanovení po ustanovení

### [Kategorie ustanovení] -- [ZELENÁ/ŽLUTÁ/ČERVENÁ]
**Ve smlouvě stojí**: [shrnutí ustanovení]
**Pozice playbooku**: [váš standard]
**Odchylka**: [popis rozdílu]
**Obchodní dopad**: [co to prakticky znamená]
**Návrh úpravy**: [konkrétní znění, u ŽLUTÉ nebo ČERVENÉ]

[Opakujte pro každé hlavní ustanovení]

## Vyjednávací strategie

[Doporučený přístup, priority, kandidáti na ústupky]

## Další kroky

[Konkrétní akce k provedení]
```

## Poznámky

- Pokud je smlouva v jazyce jiném než v češtině, uveďte to a zeptejte se uživatele, zda chce překlad nebo revizi v původním jazyce
- U velmi dlouhých smluv (50+ stran) nabídněte, že se nejdříve zaměříte na nejvýznamnější části a teprve poté provedete kompletní revizi
- Vždy uživateli připomeňte, že tato analýza má být před využitím pro právní rozhodnutí ověřena kvalifikovaným advokátem

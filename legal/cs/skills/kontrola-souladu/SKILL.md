---
name: kontrola-souladu
description: Proveďte kontrolu souladu s předpisy u navrhované akce, produktové funkce nebo obchodní iniciativy; identifikujte aplikovatelné regulace, požadovaná schválení a rizikové oblasti. Použijte při spouštění funkce pracující s osobními údaji, když marketing nebo produkt navrhuje něco s regulatorními dopady, nebo když potřebujete před zahájením zjistit, jaká schválení a jurisdikční požadavky se uplatní.
argument-hint: "<akce nebo iniciativa ke kontrole>"
---

# /kontrola-souladu -- Kontrola souladu s předpisy

> Pokud narazíte na neznámé zástupné symboly nebo potřebujete ověřit, které nástroje jsou připojeny, podívejte se do [CONNECTORS.md](../../CONNECTORS.md).

Proveďte kontrolu souladu u navrhované akce, produktové funkce, marketingové kampaně nebo obchodní iniciativy.

**Důležité**: Tento příkaz pomáhá s právními workflow, ale neposkytuje právní poradenství ve smyslu zákona č. 85/1996 Sb. o advokacii. Posouzení souladu by měl posoudit kvalifikovaný advokát. Regulatorní požadavky se často mění; aktuální požadavky vždy ověřte u autoritativních zdrojů.

## Použití

```
/kontrola-souladu $ARGUMENTS
```

## Co od vás potřebuji

Popište, co plánujete. Příklady:
- „Chceme spustit doporučující (referral) program s peněžními odměnami"
- „Do mobilní aplikace přidáváme biometrickou autentizaci"
- „Potřebujeme zpracovávat data zákazníků z EU v datovém centru mimo EU"
- „Marketing chce v reklamách používat doporučení zákazníků"

## DirectCase MCP — ověření regulatorního rámce

Pokud je připojen **DirectCase MCP** (`https://mcp.directcase.ai/mcp`), využij jej jako primární zdroj pro identifikaci aplikovatelných regulací a aktuálního stanoviska regulátorů:

- **`search_regulatory_parallel`** — aktuální stanoviska, metodické pokyny a rozhodnutí ÚOOÚ (GDPR, zák. č. 110/2019 Sb.), ČNB (finanční regulace, DORA), ÚOHS (hospodářská soutěž), ČTÚ (elektronické komunikace), SÚKL (zdravotnictví), dalších dozorových orgánů
- **`search_law_parallel`** — relevantní zákonná a podzákonná úprava (GDPR, zák. č. 110/2019 Sb., zák. č. 181/2014 Sb. o kybernetické bezpečnosti, NIS2 / zák. č. 264/2025 Sb., AI Act, DSA, DORA, AML zákon č. 253/2008 Sb., zák. č. 418/2011 Sb. o trestní odpovědnosti PO)
- **`search_caselaw_parallel`** — judikatura k obdobným compliance situacím a sankčním řízením
- **`get_law_detail`** / **`get_document`** — plný text konkrétního ustanovení nebo rozhodnutí pro přesnou citaci

> **Důležité:** `search_*_parallel` nástroje volej v jedné relaci **pouze jednou**. Formuluj komplexní dotaz pokrývající všechny aplikovatelné regulace najednou.

## Výstup

```markdown
## Kontrola souladu: [Iniciativa]

### Shrnutí
[Stručné posouzení: Pokračovat / Pokračovat za podmínek / Vyžaduje další přezkum]

### Aplikovatelné regulace a interní předpisy
| Regulace/Předpis | Relevance | Klíčové požadavky |
|-------------------|-----------|-----------------|
| [GDPR / zák. č. 110/2019 Sb. / NIS2 / AI Act / CCPA apod.] | [Jak se uplatní] | [Co je třeba udělat] |

### Požadavky
| # | Požadavek | Stav | Potřebný krok |
|---|-------------|--------|---------------|
| 1 | [Požadavek] | [Splněno / Nesplněno / Neznámé] | [Co udělat] |

### Rizikové oblasti
| Riziko | Závažnost | Zmírnění |
|------|----------|------------|
| [Riziko] | [Vysoké/Střední/Nízké] | [Jak řešit] |

### Doporučené kroky
1. [Nejdůležitější krok]
2. [Druhá priorita]
3. [Třetí priorita]

### Potřebná schválení
| Schvalovatel | Proč | Stav |
|----------|-----|--------|
| [Osoba/Tým] | [Důvod] | [Čeká] |

### Doporučený další přezkum
[Oblasti, u nichž se doporučuje konzultace s externím advokátem nebo specialistou]
```

## Přehled regulací ochrany osobních údajů

### GDPR (Obecné nařízení o ochraně osobních údajů)

**Rozsah**: Vztahuje se na zpracování osobních údajů osob nacházejících se v EU/EHP, bez ohledu na to, kde se zpracovatelská organizace nachází. V České republice doplněno zákonem č. 110/2019 Sb., o zpracování osobních údajů.

**Klíčové povinnosti pro interní právní oddělení**:
- **Právní titul**: Identifikujte a zdokumentujte právní titul pro každou zpracovatelskou činnost (souhlas, smlouva, oprávněný zájem, právní povinnost, životně důležitý zájem, veřejný úkol)
- **Práva subjektu údajů**: Reagujte na žádosti o přístup, opravu, výmaz, přenositelnost, omezení a námitku do 30 dnů (u složitých žádostí lze prodloužit o 60 dnů)
- **Posouzení vlivu na ochranu osobních údajů (DPIA)**: Vyžadováno pro zpracování, které pravděpodobně povede k vysokému riziku pro fyzické osoby
- **Oznámení o porušení zabezpečení**: Oznámení dozorovému úřadu (v ČR Úřad pro ochranu osobních údajů) do 72 hodin od zjištění porušení zabezpečení osobních údajů; při vysokém riziku oznámení dotčeným osobám bez zbytečného odkladu
- **Záznamy o činnostech zpracování**: Vedení záznamů podle čl. 30 GDPR
- **Mezinárodní předání**: Zajištění vhodných záruk pro předání mimo EHP (SCC, rozhodnutí o odpovídající ochraně, BCR)
- **Povinnost jmenovat DPO**: Jmenujte pověřence pro ochranu osobních údajů (DPO), pokud to vyžaduje zákon (orgán veřejné moci, rozsáhlé zpracování zvláštních kategorií, rozsáhlé systematické monitorování)

**Časté kontaktní body interního právního oddělení**:
- Posouzení smluv o zpracování (DPA) s dodavateli z pohledu souladu s GDPR
- Poradenství produktovým týmům ohledně principu privacy by design
- Reakce na dotazy dozorového úřadu
- Řízení mechanismů přeshraničního předávání údajů
- Posouzení mechanismů souhlasu a informačních memorand o ochraně osobních údajů

### CCPA / CPRA (California Consumer Privacy Act / California Privacy Rights Act)

**Rozsah**: Vztahuje se na podniky, které shromažďují osobní údaje obyvatel Kalifornie a dosahují stanovených prahů v oblasti příjmů, objemu dat nebo prodeje dat. (Jde o legislativu amerického státu Kalifornie; pokud působíte v EU, primárním rámcem pro vás bude GDPR.)

**Klíčové povinnosti**:
- **Právo vědět**: Spotřebitelé mohou požádat o zpřístupnění osobních údajů, které jsou shromažďovány, používány a sdíleny
- **Právo na výmaz**: Spotřebitelé mohou požádat o výmaz svých osobních údajů
- **Právo odmítnout (opt-out)**: Spotřebitelé mohou odmítnout prodej nebo sdílení osobních údajů
- **Právo na opravu**: Spotřebitelé mohou požádat o opravu nepřesných osobních údajů (rozšíření podle CPRA)
- **Právo omezit využívání citlivých osobních údajů**: Spotřebitelé mohou omezit využívání citlivých OÚ na konkrétní účely (rozšíření podle CPRA)
- **Zákaz diskriminace**: Spotřebitele uplatňující svá práva nelze diskriminovat
- **Informační memorandum**: Při sběru nebo před ním je nutné poskytnout informační memorandum popisující kategorie shromažďovaných OÚ a účely
- **Smlouvy s poskytovateli služeb**: Smlouvy s poskytovateli služeb musí omezit použití OÚ na stanovený obchodní účel

**Lhůty pro odpověď**:
- Potvrzení přijetí do 10 pracovních dnů
- Věcná odpověď do 45 kalendářních dnů (s upozorněním lze prodloužit o dalších 45 dnů)

### Další klíčové regulace, které stojí za sledování

| Regulace | Jurisdikce | Klíčové odlišnosti |
|---|---|---|
| **Zák. č. 110/2019 Sb.** | Česká republika | Adaptační zákon ke GDPR; dozor vykonává Úřad pro ochranu osobních údajů (ÚOOÚ) |
| **NIS2** (směrnice EU 2022/2555) | EU | Povinnosti v oblasti kybernetické bezpečnosti pro klíčové a významné subjekty; v ČR transponováno do zákona o kybernetické bezpečnosti (č. 181/2014 Sb., ve znění novely) |
| **DORA** (nařízení EU 2022/2554) | EU | Digitální provozní odolnost finančního sektoru; dohled vykonává ČNB |
| **AI Act** (nařízení EU 2024/1689) | EU | Harmonizovaná pravidla pro umělou inteligenci; rizikově založený přístup |
| **Digital Services Act (DSA)** | EU | Povinnosti poskytovatelů online služeb a platforem |
| **UK GDPR** | Spojené království | Post-brexitová verze britského GDPR; dozor ICO; obdobné EU GDPR se specifiky UK |
| **LGPD** (Brazílie) | Brazílie | Podobné GDPR; vyžaduje jmenování DPO; dozor Národního úřadu pro ochranu údajů (ANPD) |
| **PIPL** (Čína) | Čína | Přísná pravidla přeshraničního předávání; požadavky na lokalizaci dat; dozor CAC |

## Kontrolní seznam pro posouzení DPA

Při posuzování smlouvy o zpracování osobních údajů (DPA) ověřte následující:

### Povinné náležitosti (čl. 28 GDPR)

- [ ] **Předmět a doba trvání**: Jasně vymezený rozsah a doba zpracování
- [ ] **Povaha a účel**: Konkrétní popis toho, co se bude zpracovávat a proč
- [ ] **Typ osobních údajů**: Kategorie zpracovávaných osobních údajů
- [ ] **Kategorie subjektů údajů**: Čí osobní údaje jsou zpracovávány
- [ ] **Povinnosti a práva správce**: Pokyny správce a jeho dohledová práva

### Povinnosti zpracovatele

- [ ] **Zpracovává pouze na základě doložených pokynů**: Zpracovatel se zavazuje zpracovávat pouze podle pokynů správce (s výjimkou zákonných požadavků)
- [ ] **Mlčenlivost**: Pracovníci oprávnění ke zpracování jsou zavázáni mlčenlivostí
- [ ] **Bezpečnostní opatření**: Popsána vhodná technická a organizační opatření (odkaz na čl. 32)
- [ ] **Požadavky na subzpracovatele**:
  - [ ] Požadavek písemného souhlasu (obecného nebo konkrétního)
  - [ ] Při obecném souhlasu: oznámení změn s možností vznést námitku
  - [ ] Subzpracovatelé vázáni stejnými povinnostmi prostřednictvím písemné smlouvy
  - [ ] Zpracovatel zůstává odpovědný za činnost subzpracovatelů
- [ ] **Součinnost při žádostech subjektů údajů**: Zpracovatel bude spolupracovat při reakcích na žádosti subjektů údajů
- [ ] **Součinnost při bezpečnosti a porušení**: Zpracovatel bude poskytovat součinnost při plnění bezpečnostních povinností, oznámeních o porušení, DPIA a konzultacích
- [ ] **Výmaz nebo vrácení**: Po ukončení smlouvy výmaz nebo vrácení všech osobních údajů (dle volby správce) a výmaz existujících kopií, pokud zákon nestanoví povinnost uchování
- [ ] **Právo auditu**: Správce má právo provádět audity a kontroly (nebo akceptovat auditní zprávy třetích stran)
- [ ] **Oznámení o porušení**: Zpracovatel oznámí správci porušení zabezpečení osobních údajů bez zbytečného odkladu (ideálně do 24-48 hodin; musí umožnit správci dodržet regulatorní 72hodinovou lhůtu)

### Mezinárodní předání

- [ ] **Identifikován mechanismus předání**: SCC, rozhodnutí o odpovídající ochraně, BCR nebo jiný platný mechanismus
- [ ] **Verze SCC**: Používá se aktuální verze SCC EU (z června 2021), pokud je to relevantní
- [ ] **Správný modul**: Zvolen odpovídající modul SCC (C2P, C2C, P2P, P2C)
- [ ] **Posouzení dopadu předání (TIA)**: Dokončeno při předávání do zemí bez rozhodnutí o odpovídající ochraně
- [ ] **Doplňková opatření**: Technická, organizační nebo smluvní opatření k překlenutí mezer identifikovaných v TIA
- [ ] **Dodatek pro UK**: Pokud se týká osobních údajů z UK, zahrnut UK International Data Transfer Addendum

### Praktické úvahy

- [ ] **Odpovědnost**: Ustanovení o odpovědnosti v DPA jsou v souladu s hlavní smlouvou o službách (nebo s ní nekolidují)
- [ ] **Sladění ukončení**: Doba platnosti DPA odpovídá smlouvě o službách
- [ ] **Místa zpracování**: Místa zpracování jsou specifikována a akceptovatelná
- [ ] **Bezpečnostní standardy**: Vyžadovány konkrétní bezpečnostní standardy nebo certifikace (SOC 2, ISO 27001 apod.)
- [ ] **Pojištění**: Odpovídající pojistné krytí pro činnosti zpracování údajů

### Časté problémy v DPA

| Problém | Riziko | Standardní pozice |
|---|---|---|
| Paušální souhlas se subzpracovateli bez oznamovací povinnosti | Ztráta kontroly nad řetězcem zpracování | Vyžadovat oznámení s právem vznést námitku |
| Lhůta oznámení porušení > 72 hodin | Může zabránit včasnému regulatornímu oznámení | Vyžadovat oznámení do 24-48 hodin |
| Žádná audit. práva (nebo jen prostřednictvím zpráv třetích stran) | Nelze ověřit soulad | Akceptovat SOC 2 Type II + právo auditu při důvodném podezření |
| Lhůta pro výmaz dat není stanovena | Data jsou uchovávána neomezeně | Vyžadovat výmaz do 30-90 dnů od ukončení |
| Nestanovena místa zpracování údajů | Data mohou být zpracovávána kdekoli | Vyžadovat zveřejnění míst zpracování |
| Zastaralé SCC | Neplatný mechanismus předání | Vyžadovat aktuální EU SCC (verze 2021) |

## Vyřizování žádostí subjektů údajů

### Přijetí žádosti

Když obdržíte žádost subjektu údajů:

1. **Určete typ žádosti**:
   - Přístup (kopie osobních údajů)
   - Oprava (oprava nepřesných údajů)
   - Výmaz / smazání („právo být zapomenut")
   - Omezení zpracování
   - Přenositelnost údajů (strukturovaný, strojově čitelný formát)
   - Námitka proti zpracování
   - Odmítnutí prodeje/sdílení (CCPA/CPRA)
   - Omezení využití citlivých osobních údajů (CPRA)

2. **Určete aplikovatelné regulace**:
   - Kde se subjekt údajů nachází?
   - Jaké zákony se uplatní podle přítomnosti a činností vaší organizace?
   - Jaké jsou konkrétní požadavky a lhůty?

3. **Ověřte totožnost**:
   - Potvrďte, že žadatel je tím, za koho se vydává
   - Použijte přiměřené ověřovací postupy úměrné citlivosti údajů
   - Nepožadujte nadměrnou dokumentaci

4. **Zaznamenejte žádost**:
   - Datum přijetí
   - Typ žádosti
   - Totožnost žadatele
   - Aplikovatelná regulace
   - Lhůta pro odpověď
   - Přidělený zpracovatel

### Lhůty pro odpověď

| Regulace | Počáteční potvrzení | Věcná odpověď | Prodloužení |
|---|---|---|---|
| GDPR | Není stanoveno (best practice: neprodleně) | 30 dnů | +60 dnů (s upozorněním) |
| CCPA/CPRA | 10 pracovních dnů | 45 kalendářních dnů | +45 dnů (s upozorněním) |
| UK GDPR | Není stanoveno (best practice: neprodleně) | 30 dnů | +60 dnů (s upozorněním) |
| LGPD | Nestanoveno | 15 dnů | Omezená možnost prodloužení |

### Výjimky a omezení

Před vyhověním žádosti zkontrolujte, zda se uplatní nějaké výjimky:

**Časté výjimky napříč regulacemi**:
- Obhajoba nebo uplatnění právních nároků
- Právní povinnosti vyžadující uchování
- Veřejný zájem nebo výkon veřejné moci
- Svoboda projevu a informací (u žádostí o výmaz)
- Archivace ve veřejném zájmu nebo pro vědecký/historický výzkum

**Organizačně specifické úvahy**:
- Litigation hold (zajištění dokumentů pro účely sporu): Údaje podléhající litigation hold nelze smazat
- Regulatorní uchování: Finanční záznamy, personální záznamy a další kategorie mohou mít povinné doby uchování (např. dle zákona o účetnictví č. 563/1991 Sb., zákoníku práce č. 262/2006 Sb.)
- Práva třetích stran: Vyhovění žádosti by mohlo nepříznivě ovlivnit práva jiných osob

### Postup odpovědi

1. Shromážděte všechny osobní údaje žadatele napříč systémy
2. Uplatněte případné výjimky a zdokumentujte jejich základ
3. Připravte odpověď: vyhovte žádosti nebo vysvětlete, proč jí (zcela nebo částečně) nelze vyhovět
4. V případě zamítnutí (zcela nebo částečně): uveďte konkrétní právní základ zamítnutí
5. Poučte žadatele o právu podat stížnost u dozorového úřadu (v ČR ÚOOÚ)
6. Zdokumentujte odpověď a uchovávejte záznamy o žádosti a odpovědi

## Základy monitoringu regulatorních změn

### Co sledovat

Udržujte přehled o vývoji v těchto oblastech:
- **Regulatorní vodítka**: Nová nebo aktualizovaná vodítka dozorových úřadů (ÚOOÚ, EDPB, ICO, CNIL apod.)
- **Rozhodnutí o sankcích**: Pokuty, opatření a urovnání, která signalizují priority regulátorů
- **Legislativní změny**: Nové zákony o ochraně osobních údajů, novely stávajících zákonů, prováděcí předpisy
- **Průmyslové standardy**: Aktualizace ISO 27001, SOC 2, NIST frameworks a oborové požadavky
- **Vývoj v oblasti přeshraničního předávání**: Rozhodnutí o odpovídající ochraně, aktualizace SCC, požadavky na lokalizaci dat

### Přístup k monitoringu

1. **Přihlaste se k odběru komunikace od regulatorních úřadů** (newslettery, RSS, oficiální oznámení)
2. **Sledujte relevantní právní publikace** pro analýzu nových vývojů
3. **Prostudujte novinky z profesních asociací** pro oborově specifická vodítka
4. **Veďte regulatorní kalendář** známých nadcházejících lhůt, dnů účinnosti a milníků souladu
5. **Informujte právní tým** o významných vývojích ovlivňujících zpracovatelské činnosti organizace

### Kritéria pro eskalaci

Eskalujte regulatorní vývoj na seniorního právníka nebo vedení, když:
- Nová regulace nebo vodítko přímo ovlivňuje klíčové obchodní činnosti organizace
- Sankční rozhodnutí v odvětví organizace signalizuje zvýšený dohled regulátorů
- Blíží se lhůta souladu, která vyžaduje organizační změny
- Je zpochybněn nebo zneplatněn mechanismus předávání údajů, o který se organizace opírá
- Regulatorní úřad zahájí šetření nebo vyšetřování týkající se organizace

## Tipy

1. **Buďte konkrétní** -- „Chceme poslat e-mail všem našim uživatelům" je lepší než „marketingová kampaň".
2. **Uveďte geografii** -- Požadavky na soulad se liší podle jurisdikce (ČR, EU, třetí země).
3. **Zmiňte data** -- O jaké osobní údaje jde? To určuje většinu požadavků na soulad.

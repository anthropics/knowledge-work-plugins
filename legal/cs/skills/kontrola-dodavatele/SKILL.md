---
name: kontrola-dodavatele
description: Zkontrolujte stav stávajících smluv s dodavatelem napříč všemi propojenými systémy — CLM, CRM, e-mail a úložiště dokumentů — včetně analýzy mezer a blížících se termínů. Použijte při zavádění nebo obnovení dodavatele, když potřebujete konsolidovaný přehled o tom, co je podepsáno a co chybí (MSA, DPA, SOW), nebo při kontrole blížících se konců platnosti a přetrvávajících závazků.
argument-hint: "[název dodavatele]"
---

# /kontrola-dodavatele -- Stav smluv s dodavatelem

> Pokud narazíte na neznámé zástupné symboly nebo potřebujete zjistit, které nástroje jsou propojeny, viz [CONNECTORS.md](../../CONNECTORS.md).

Zkontrolujte stav stávajících smluv s dodavatelem napříč všemi propojenými systémy. Poskytuje konsolidovaný pohled na právní vztah.

**Důležité**: Tento příkaz pomáhá s právními workflow, ale neposkytuje právní poradenství ve smyslu zákona č. 85/1996 Sb. o advokacii. Hlášení o stavu smluv je třeba ověřit oproti originálním dokumentům kvalifikovaným advokátem.

## Spuštění

```
/kontrola-dodavatele [název dodavatele]
```

Pokud není název dodavatele uveden, vyzvěte uživatele, aby upřesnil, kterého dodavatele chce zkontrolovat.

## Workflow

### Krok 1: Identifikujte dodavatele

Přijměte název dodavatele od uživatele. Ošetřete běžné varianty:
- Úplný obchodní název vs. obchodní značka (např. „Alphabet Inc." vs. „Google")
- Zkratky (např. „AWS" vs. „Amazon Web Services")
- Vztahy mezi mateřskou společností a dceřinou společností

Pokud je název dodavatele nejednoznačný, požádejte uživatele o upřesnění.

### Krok 2: Prohledejte propojené systémy

Vyhledejte dodavatele ve všech dostupných propojených systémech v pořadí dle priority:

#### CLM (systém pro správu smluv) -- Pokud je propojen
Vyhledejte všechny smlouvy s dodavatelem:
- Aktivní smlouvy
- Smlouvy, jejichž platnost skončila (za poslední 3 roky)
- Smlouvy v jednání nebo čekající na podpis
- Dodatky a přílohy

#### CRM -- Pokud je propojen
Vyhledejte záznam dodavatele/účtu:
- Stav účtu a typ vztahu
- Související příležitosti nebo obchodní případy
- Kontaktní údaje na právní/smluvní tým dodavatele

#### E-mail -- Pokud je propojen
Vyhledejte nedávnou relevantní korespondenci:
- E-maily týkající se smluv (za posledních 6 měsíců)
- Přílohy NDA nebo smluv
- Vyjednávací vlákna

#### Dokumenty (např. Box, Egnyte, SharePoint) -- Pokud jsou propojeny
Vyhledejte:
- Podepsané smlouvy
- Redline úpravy a návrhy
- Podklady pro due diligence

#### Chat (např. Slack, Teams) -- Pokud je propojen
Vyhledejte nedávné zmínky:
- Žádosti o smlouvy týkající se tohoto dodavatele
- Právní dotazy k dodavateli
- Relevantní týmové diskuse (za poslední 3 měsíce)

#### DirectCase MCP -- veřejné registry a due diligence

Pokud je připojen **DirectCase MCP** (`https://mcp.directcase.ai/mcp`), použij jej jako primární zdroj pro veřejné informace o dodavateli:

- **`search_company`** — vyhledej dodavatele v obchodním rejstříku; ověř IČO, DIČ, právní formu, sídlo, statutární orgán, oprávněné osoby k podpisu, základní kapitál, datum vzniku, stav likvidace/insolvence
- **`search_company_documents`** — dokumenty k dané společnosti: účetní závěrky, výroční zprávy, sbírka listin, dokumenty z insolvenčního rejstříku, veřejné rozsudky
- **`get_company_document_pdf`** — stáhni konkrétní PDF (např. účetní závěrku za poslední období) pro hlubší analýzu finančního zdraví dodavatele
- **`convert_pdf_to_text`** — převeď stažené PDF na text pro strojové zpracování
- **`search_caselaw_parallel`** — zjisti, zda dodavatel figuruje v relevantní soudní judikatuře (spory o plnění, insolvence, ochrana spotřebitele). **Volat pouze jednou.**

Tyto informace zahrň do přehledu dodavatele a označ červeně, pokud zjistíš insolvenci, exekuci, likvidaci nebo významné rozsudky v neprospěch dodavatele.

### Krok 3: Sestavte přehled o stavu smluv

Pro každou nalezenou smlouvu uveďte:

| Pole | Detaily |
|-------|---------|
| **Typ smlouvy** | NDA, MSA, SOW, DPA, SLA, licenční smlouva atd. |
| **Stav** | Aktivní, po platnosti, v jednání, čeká na podpis |
| **Datum účinnosti** | Kdy smlouva nabyla účinnosti |
| **Datum ukončení** | Kdy končí nebo se obnovuje |
| **Automatické prodloužení** | Ano/Ne, s dobou prodloužení a výpovědní lhůtou |
| **Klíčové podmínky** | Limit odpovědnosti, rozhodné právo, ustanovení o ukončení |
| **Dodatky** | Případné dodatky nebo přílohy v evidenci |

### Krok 4: Analýza mezer

Identifikujte, které smlouvy existují a které mohou chybět:

```
## Pokrytí smlouvami

[CHECK] NDA -- [stav]
[CHECK/MISSING] MSA -- [stav nebo „Nenalezeno"]
[CHECK/MISSING] DPA -- [stav nebo „Nenalezeno"]
[CHECK/MISSING] SOW -- [stav nebo „Nenalezeno"]
[CHECK/MISSING] SLA -- [stav nebo „Nenalezeno"]
[CHECK/MISSING] Potvrzení o pojištění -- [stav nebo „Nenalezeno"]
```

Označte všechny mezery, které mohou být potřeba podle typu vztahu (např. pokud existuje MSA, ale chybí DPA a dodavatel zpracovává osobní údaje).

### Krok 5: Vygenerujte hlášení

Vytvořte konsolidované hlášení:

```
## Stav smluv s dodavatelem: [Název dodavatele]

**Datum prověrky**: [dnešní datum]
**Prověřené zdroje**: [seznam prohledaných systémů]
**Nedostupné zdroje**: [seznam nepropojených systémů, pokud existují]

## Přehled vztahu

**Dodavatel**: [úplný obchodní název]
**Typ vztahu**: [dodavatel/partner/zákazník atd.]
**Stav v CRM**: [pokud je k dispozici]

## Přehled smluv

### [Typ smlouvy 1] -- [Stav]
- **Účinnost**: [datum]
- **Konec platnosti**: [datum] ([automaticky se prodlužuje / neprodlužuje se automaticky])
- **Klíčové podmínky**: [shrnutí podstatných ustanovení]
- **Umístění**: [kde je uložena podepsaná kopie]

### [Typ smlouvy 2] -- [Stav]
[atd.]

## Analýza mezer

[Co je zajištěno vs. co může být potřeba]

## Nadcházející úkony

- [Případné blížící se konce platnosti nebo termíny obnovení]
- [Požadované smlouvy, které ještě nejsou uzavřeny]
- [Dodatky nebo aktualizace, které mohou být potřeba]

## Poznámky

[Jakýkoli relevantní kontext z vyhledávání v e-mailu/chatu]
```

### Krok 6: Ošetření chybějících zdrojů

Pokud klíčové systémy nejsou propojeny přes MCP:

- **Žádný CLM**: Uveďte, že žádný CLM není propojen. Doporučte uživateli zkontrolovat CLM ručně. Nahlaste, co bylo nalezeno v ostatních systémech.
- **Žádný CRM**: Přeskočte kontext CRM. Upozorněte na chybějící údaje.
- **Žádný e-mail**: Uveďte, že e-mail nebyl prohledán. Doporučte uživateli prohledat e-mail na výrazy „[název dodavatele] smlouva" nebo „[název dodavatele] NDA".
- **Žádné dokumenty**: Uveďte, že úložiště dokumentů nebylo prohledáno.

Vždy jasně uveďte, které zdroje byly prověřeny a které nikoli, aby uživatel znal úplnost hlášení.

## Poznámky

- Pokud nejsou v žádném propojeném systému nalezeny žádné smlouvy, jasně to uveďte a zeptejte se uživatele, zda má smlouvy uloženy jinde
- U skupin dodavatelů (např. dodavatel s více dceřinými společnostmi) se zeptejte, zda si uživatel přeje prověřit konkrétní subjekt, nebo celou skupinu
- Upozorněte na všechny smlouvy, kterým skončila platnost, ale mohou stále obsahovat přetrvávající závazky (mlčenlivost, odškodnění atd.)
- Pokud se smlouva blíží ke konci platnosti (do 90 dnů), výrazně na to upozorněte

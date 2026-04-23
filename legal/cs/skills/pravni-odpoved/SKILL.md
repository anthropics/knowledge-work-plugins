---
name: pravni-odpoved
description: Vygeneruje odpověď na běžný právní dotaz pomocí nakonfigurovaných šablon, se zabudovanými kontrolami eskalace pro situace, kde by se šablonová odpověď používat neměla. Použijte při reakci na žádosti subjektů údajů, oznámení litigation hold, právní dotazy dodavatelů, žádosti o podpis NDA od obchodních týmů nebo na předvolání a soudní doručení.
argument-hint: "[typ-dotazu]"
---

# /pravni-odpoved -- Vygenerování odpovědi ze šablony

> Pokud narazíte na neznámé zástupné symboly nebo potřebujete ověřit, které nástroje jsou připojené, podívejte se na [CONNECTORS.md](../../CONNECTORS.md).

Vygeneruje odpověď na běžný právní dotaz pomocí nakonfigurovaných šablon. Odpověď přizpůsobí konkrétním detailům a zahrnuje spouštěče eskalace pro situace, ve kterých se šablonová odpověď používat nemá.

**Důležité**: Tento plugin pomáhá s právními workflow, ale neposkytuje právní poradenství ve smyslu zákona č. 85/1996 Sb. o advokacii. Veškeré závěry ověřte u kvalifikovaného advokáta. Generované odpovědi by měl před odesláním zkontrolovat kvalifikovaný právník, zejména u regulované komunikace.

## Vyvolání

```
/pravni-odpoved [typ-dotazu]
```

Běžné typy dotazů:
- `dsr` nebo `data-subject-request` -- Žádosti subjektu údajů o přístup / výmaz / opravu
- `hold` nebo `discovery-hold` -- Oznámení litigation hold (zachování dokumentů pro účely sporu)
- `vendor` nebo `vendor-question` -- Právní dotazy dodavatelů
- `nda` nebo `nda-request` -- Žádosti o podpis NDA od obchodních týmů
- `privacy` nebo `privacy-inquiry` -- Dotazy týkající se ochrany osobních údajů
- `subpoena` -- Odpovědi na předvolání nebo soudní doručení
- `insurance` -- Oznámení pojistné události
- `custom` -- Použití vlastní šablony

Pokud není zadán žádný typ dotazu, zeptejte se uživatele, jaký typ odpovědi potřebuje, a zobrazte dostupné kategorie.

## DirectCase MCP -- citace autoritativní opory v odpovědích

Pokud je připojen **DirectCase MCP** (`https://mcp.directcase.ai/mcp`), využij jej pro ověření a doplnění právní opory v šabloně před odesláním:

- **`search_law_parallel`** — najdi přesná zákonná ustanovení, která se v odpovědi cituje (např. GDPR čl. 15–22 pro DSR, § 38 OZ pro právní úkony, zák. č. 110/2019 Sb. pro ÚOOÚ postupy). **Volat pouze jednou.**
- **`get_law_detail`** — načti plný text konkrétního paragrafu / článku pro přesnou citaci včetně znění
- **`search_regulatory_parallel`** — aktuální stanovisko ÚOOÚ nebo jiného regulátora k typu dotazu. **Volat pouze jednou.**
- **`search_caselaw_parallel`** — u odpovědí, které se odkazují na precedens (např. odmítnutí DSR jako zjevně nedůvodné podle GDPR čl. 12 odst. 5) cituj relevantní judikaturu. **Volat pouze jednou.**

Šablony mají obsahovat placeholder `{{legal_basis}}` nebo `{{citation}}`, který se doplňuje citací z DirectCase (formát: „§ X zák. č. Y/ZZZZ Sb." nebo „NS sp. zn. ABC / ECLI:...").

## Workflow

### Krok 1: Určení typu dotazu

Přijměte typ dotazu od uživatele. Pokud je typ nejednoznačný, zobrazte dostupné kategorie a požádejte o upřesnění.

### Krok 2: Načtení šablony

Vyhledejte šablony v lokálních nastaveních (např. `legal.local.md` nebo adresář se šablonami).

**Pokud jsou šablony nakonfigurované:**
- Načtěte odpovídající šablonu pro daný typ dotazu
- Identifikujte požadované proměnné (jméno příjemce, data, konkrétní detaily)

**Pokud žádné šablony nejsou nakonfigurované:**
- Informujte uživatele, že pro tento typ dotazu nebyly nalezeny žádné šablony
- Nabídněte pomoc s vytvořením šablony (viz Průvodce tvorbou šablon níže)
- Poskytněte rozumnou výchozí strukturu odpovědi podle typu dotazu

### Krok 3: Kontrola spouštěčů eskalace

Před vygenerováním jakékoliv odpovědi posuďte, zda tato situace nemá charakteristiky, které by NEMĚLY být řešeny šablonovou odpovědí.

#### Univerzální spouštěče eskalace (platí pro všechny kategorie)
- Věc se týká potenciálního sporu nebo regulatorního šetření
- Dotaz pochází od regulátora, státního orgánu nebo orgánu činného v trestním řízení
- Odpověď by mohla vytvořit závazný právní závazek nebo vzdání se práva
- Věc se týká potenciální trestní odpovědnosti
- Jde o mediálně sledovaný případ nebo je to pravděpodobné
- Situace je bezprecedentní (tým ji dosud neřešil)
- Dotčeno je více jurisdikcí s rozpornými požadavky
- Věc se týká vrcholového vedení nebo členů orgánů společnosti

#### Spouštěče eskalace pro žádosti subjektu údajů
- Žádost se týká údajů nezletilé osoby nebo je podána jménem nezletilé osoby
- Žádost pochází od dozorového úřadu (nikoli od fyzické osoby)
- Žádost se týká údajů, na které se vztahuje litigation hold
- Žadatelem je současný nebo bývalý zaměstnanec s aktivním sporem nebo personální záležitostí
- Rozsah žádosti je neobvykle široký nebo působí jako „fishing expedition"
- Žádost se týká údajů zpracovávaných v jurisdikci se specifickými požadavky
- Žádost se týká zvláštních kategorií osobních údajů (zdraví, biometrické, genetické)

#### Spouštěče eskalace pro litigation hold
- Věc se týká potenciální trestní odpovědnosti
- Rozsah zachování dokumentů je nejasný, sporný nebo potenciálně příliš široký
- Jsou pochybnosti o tom, zda určité údaje spadají do rozsahu
- Existují předchozí holdy pro stejnou nebo související věc
- Hold může významně ovlivnit probíhající obchodní operace
- Hold je v rozporu s regulatorními požadavky na výmaz
- Custodian (osoba odpovědná za zachování dokumentů) vznáší námitky proti rozsahu

#### Spouštěče eskalace pro dotazy dodavatelů
- Dotaz se týká sporu nebo potenciálního porušení
- Dodavatel hrozí soudním sporem nebo ukončením smlouvy
- Dotaz se týká regulatorního souladu (nejen smluvních podmínek)
- Odpověď by mohla vytvořit závazný závazek nebo vzdání se práva
- Odpověď by mohla ovlivnit probíhající vyjednávání

#### Spouštěče eskalace pro žádosti o podpis NDA
- Protistranou je konkurent
- NDA se týká utajovaných informací státního orgánu
- Obchodní kontext naznačuje, že NDA má souviset s potenciální M&A transakcí
- Žádost se týká neobvyklého předmětu (trénovací data pro AI, biometrické údaje apod.)

#### Spouštěče eskalace pro předvolání / soudní doručení
- **VŽDY vyžaduje kontrolu právníkem** (šablony slouží pouze jako výchozí bod)
- Identifikovány otázky advokátní mlčenlivosti či jiného privilegia
- Dotčena jsou data třetích stran
- Přeshraniční předávání dokumentů
- Nepřiměřená lhůta

**Když je detekován spouštěč eskalace:**
1. **Zastavte**: Negenerujte šablonovou odpověď
2. **Upozorněte**: Informujte uživatele, že byl detekován spouštěč eskalace
3. **Vysvětlete**: Popište, který spouštěč byl detekován a proč je důležitý
4. **Doporučte**: Navrhněte vhodnou cestu eskalace (senior interní právník, externí právník, konkrétní člen týmu)
5. **Nabídněte**: Poskytněte návrh ke kontrole právníkem (jasně označený jako „NÁVRH -- POUZE PRO KONTROLU PRÁVNÍKEM") namísto finální odpovědi

### Krok 4: Sběr konkrétních detailů

Vyžádejte si od uživatele detaily potřebné pro přizpůsobení odpovědi:

**Žádost subjektu údajů:**
- Jméno a kontaktní údaje žadatele
- Typ žádosti (přístup, výmaz, oprava, přenositelnost, námitka proti zpracování)
- O jaké údaje se jedná
- Aplikovatelná právní úprava (GDPR, zák. č. 110/2019 Sb., CCPA (neaplikuje se v ČR; pro EU platí GDPR a zák. č. 110/2019 Sb.), jiné)
- Lhůta pro odpověď

**Litigation hold:**
- Název věci a spisová značka
- Custodians (kdo musí dokumenty zachovat)
- Rozsah zachování (časové rozpětí, typy dat, systémy)
- Kontakt na externího právníka
- Datum účinnosti

**Dotaz dodavatele:**
- Název dodavatele
- Referenční smlouva (pokud existuje)
- Konkrétní dotaz, který je řešen
- Relevantní smluvní ustanovení

**Žádost o podpis NDA:**
- Žádající obchodní tým a kontakt
- Název protistrany
- Účel NDA
- Vzájemné nebo jednostranné
- Jakékoliv zvláštní požadavky

### Krok 5: Vygenerování odpovědi

Naplňte šablonu získanými detaily. Zajistěte, že odpověď:
- Používá odpovídající tón (profesionální, srozumitelný, nikoliv přehnaně právnický pro obchodní publikum)
- Obsahuje všechny požadované právní náležitosti pro daný typ odpovědi
- Odkazuje na konkrétní data, lhůty a povinnosti
- Poskytuje jasné další kroky pro příjemce
- Obsahuje příslušná upozornění nebo výhrady

Předložte návrh odpovědi uživateli ke kontrole před odesláním.

#### Pokyny pro přizpůsobení

**Povinné přizpůsobení** -- Každá šablonová odpověď MUSÍ být přizpůsobena o:
- Správná jména, data a spisové značky / referenční čísla
- Konkrétní skutkové okolnosti situace
- Aplikovatelnou jurisdikci a právní úpravu
- Správné lhůty pro odpověď podle data přijetí dotazu
- Odpovídající podpisový blok a kontaktní údaje

**Úprava tónu** -- Přizpůsobte tón podle:
- **Publika**: Interní vs. externí, obchodní vs. právní, fyzická osoba vs. dozorový úřad
- **Vztahu**: Nová protistrana vs. stávající partner vs. protistrana ve sporu
- **Citlivosti**: Rutinní dotaz vs. sporná věc vs. regulatorní šetření
- **Naléhavosti**: Standardní lhůta vs. zrychlená odpověď

**Jurisdikční úpravy:**
- Ověřte, že citované předpisy jsou správné pro jurisdikci žadatele
- Upravte lhůty podle aplikovatelného práva
- Zahrňte informace o právech specifické pro danou jurisdikci
- Používejte právní terminologii odpovídající dané jurisdikci

### Krok 6: Tvorba šablony (pokud šablona neexistuje)

Pokud chce uživatel vytvořit novou šablonu, projděte s ním Průvodce tvorbou šablon (viz níže) a předložte hotovou šablonu ke kontrole. Navrhněte uživateli uložit schválenou šablonu do lokálních nastavení pro budoucí použití.

## Kategorie odpovědí

### 1. Žádosti subjektu údajů (DSR)

**Podkategorie**:
- Potvrzení přijetí
- Žádost o ověření totožnosti
- Odpověď o vyřízení (přístup, výmaz, oprava)
- Částečné zamítnutí s odůvodněním
- Úplné zamítnutí s odůvodněním
- Oznámení o prodloužení lhůty

**Klíčové prvky šablony**:
- Odkaz na aplikovatelnou právní úpravu (GDPR čl. 15--22, zák. č. 110/2019 Sb.)
- Konkrétní lhůta pro odpověď (dle GDPR čl. 12 odst. 3 jeden měsíc od přijetí žádosti)
- Požadavky na ověření totožnosti
- Práva subjektu údajů (včetně práva podat stížnost u ÚOOÚ)
- Kontaktní údaje pro navazující komunikaci

**Vzorová struktura šablony**:
```
Předmět: Vaše žádost o [přístup k / výmaz / opravu] osobních údajů -- č.j. {{request_id}}

Vážený pane / Vážená paní {{requester_name}},

potvrzujeme přijetí Vaší žádosti ze dne {{request_date}} o [přístup k / výmaz / opravu] Vašich osobních údajů podle [aplikovatelné právní úpravy].

[Potvrzení přijetí / žádost o ověření totožnosti / detaily o vyřízení / důvody zamítnutí]

Věcnou odpověď Vám poskytneme nejpozději do {{response_deadline}}.

[Kontaktní údaje]
[Informace o právech subjektu údajů]

S pozdravem
```

### 2. Litigation hold (zachování dokumentů pro účely sporu)

**Podkategorie**:
- Úvodní oznámení holdu pro custodians
- Připomínka holdu / pravidelné potvrzení
- Úprava holdu (změna rozsahu)
- Uvolnění holdu

**Klíčové prvky šablony**:
- Název věci a spisová značka
- Jasné povinnosti ohledně zachování dokumentů
- Rozsah zachování (časové rozpětí, typy dat, systémy, typy komunikace)
- Zákaz ničení důkazů (spoliation)
- Kontakt pro dotazy
- Požadavek na potvrzení přijetí

**Vzorová struktura šablony**:
```
Předmět: OZNÁMENÍ O LITIGATION HOLD -- {{matter_name}} -- Vyžadováno jednání

DŮVĚRNÉ -- PŘEDMĚT ADVOKÁTNÍHO TAJEMSTVÍ
KOMUNIKACE ADVOKÁT--KLIENT

Vážený pane / Vážená paní {{custodian_name}},

toto oznámení obdržíte proto, že můžete disponovat dokumenty, komunikací nebo údaji relevantními pro výše uvedenou věc.

POVINNOST ZACHOVAT DOKUMENTY:
S okamžitou účinností jste povinen / povinna zachovat veškeré dokumenty a elektronicky uložené informace (ESI) týkající se:
- Předmět: {{hold_scope}}
- Časové rozpětí: od {{start_date}} do současnosti
- Typy dokumentů: {{document_types}}

NEMAŽTE, NENIČTE, NEUPRAVUJTE ani nevyhazujte žádné potenciálně relevantní materiály.

[Konkrétní pokyny pro systémy, e-mail, chat, lokální soubory]

Potvrďte prosím přijetí tohoto oznámení nejpozději do {{acknowledgment_deadline}}.

V případě dotazů kontaktujte {{legal_contact}}.
```

### 3. Dotazy k ochraně osobních údajů

**Podkategorie**:
- Odpovědi na dotazy o cookies / trackování
- Dotazy k podmínkám ochrany osobních údajů
- Dotazy k praktikám sdílení dat
- Dotazy týkající se údajů dětí
- Dotazy na přeshraniční předávání

**Klíčové prvky šablony**:
- Odkaz na zásady ochrany osobních údajů organizace
- Konkrétní odpovědi vycházející ze současných postupů
- Odkazy na relevantní dokumentaci k ochraně osobních údajů
- Kontaktní údaje na tým ochrany osobních údajů / DPO

### 4. Právní dotazy dodavatelů

**Podkategorie**:
- Odpověď na dotaz o stavu smlouvy
- Odpověď na žádost o dodatek
- Žádosti o potvrzení souladu s předpisy
- Odpovědi na žádosti o audit
- Žádosti o potvrzení o pojištění

**Klíčové prvky šablony**:
- Odkaz na aplikovatelnou smlouvu
- Konkrétní odpověď na dotaz dodavatele
- Jakékoliv nutné výhrady nebo omezení
- Další kroky a časový rámec

### 5. Žádosti o podpis NDA

**Podkategorie**:
- Zaslání standardní NDA organizace
- Akceptace NDA protistrany (s připomínkami)
- Zamítnutí žádosti o NDA s odůvodněním
- Obnovení nebo prodloužení NDA

**Klíčové prvky šablony**:
- Účel NDA
- Shrnutí standardních podmínek
- Pokyny pro podpis
- Očekávaný časový rámec

### 6. Předvolání / soudní doručení

**Podkategorie**:
- Potvrzení přijetí
- Námitka
- Žádost o prodloužení
- Průvodní dopis k poskytnutí součinnosti

**Klíčové prvky šablony**:
- Spisová značka a jurisdikce
- Konkrétní námitky (pokud existují)
- Potvrzení zachování dokumentů
- Lhůta pro splnění
- Odkaz na seznam privilegovaných dokumentů (pokud aplikovatelné)

**Kritická poznámka**: Odpovědi na předvolání téměř vždy vyžadují individuální kontrolu právníkem. Šablony slouží jako výchozí rámec, nikoli jako finální odpověď.

### 7. Oznámení pojistné události

**Podkategorie**:
- Úvodní oznámení o pojistné události
- Doplňující informace
- Odpověď na výhradu práv (reservation of rights)

**Klíčové prvky šablony**:
- Číslo pojistné smlouvy a období pojistného krytí
- Popis věci nebo události
- Časový přehled událostí
- Požadované potvrzení pojistného krytí

## Metodika správy šablon

### Organizace šablon

Šablony by měly být organizovány podle kategorií a udržovány v lokálních nastaveních týmu. Každá šablona by měla obsahovat:

1. **Kategorie**: Typ dotazu, který šablona řeší
2. **Název šablony**: Popisný identifikátor
3. **Případ použití**: Kdy je tato šablona vhodná
4. **Spouštěče eskalace**: Kdy by tato šablona NEMĚLA být použita
5. **Požadované proměnné**: Informace, které musí být pro každé použití přizpůsobeny
6. **Tělo šablony**: Text odpovědi se zástupnými symboly proměnných
7. **Navazující kroky**: Standardní kroky po odeslání odpovědi
8. **Datum poslední revize**: Kdy byla šablona naposledy ověřena z hlediska správnosti

### Životní cyklus šablony

1. **Vytvoření**: Návrh šablony podle osvědčených postupů a podnětů týmu
2. **Revize**: Kontrola a schválení obsahu šablony právním týmem
3. **Publikace**: Přidání do knihovny šablon s metadaty
4. **Použití**: Generování odpovědí pomocí šablony
5. **Zpětná vazba**: Sledování, kdy jsou šablony při použití upravovány, pro identifikaci možných vylepšení
6. **Aktualizace**: Revize šablon při změnách práva, interních předpisů nebo osvědčených postupů
7. **Vyřazení**: Archivace šablon, které již nejsou aplikovatelné

## Průvodce tvorbou šablon

Při pomoci uživatelům s tvorbou nových šablon:

### 1. Definujte případ použití
- Jaký typ dotazu tato šablona řeší?
- Jak často se vyskytuje?
- Kdo je typickým publikem?
- Jaká je typická úroveň naléhavosti?

### 2. Identifikujte povinné prvky
- Jaké informace musí být obsaženy v každé odpovědi?
- Jaké regulatorní požadavky se uplatní?
- Jaké interní předpisy organizace tento typ odpovědi upravují?

### 3. Definujte proměnné
- Co se mění při každém použití? (jména, data, konkrétnosti)
- Co zůstává stejné? (právní požadavky, standardní formulace)
- Používejte srozumitelné názvy proměnných: `{{requester_name}}`, `{{response_deadline}}`, `{{matter_reference}}`

### 4. Připravte návrh šablony
- Pište srozumitelným, profesionálním jazykem
- Vyhněte se zbytečnému právnímu žargonu pro obchodní publikum
- Zahrňte všechny zákonem požadované prvky
- Přidejte zástupné symboly pro veškerý proměnný obsah
- Zahrňte šablonu předmětu, pokud je určena pro e-mail

### 5. Definujte spouštěče eskalace
- Ve kterých situacích by se tato šablona NEMĚLA používat?
- Jaké charakteristiky naznačují, že věc vyžaduje individuální přístup?
- Buďte konkrétní: vágní spouštěče nejsou užitečné

### 6. Přidejte metadata
- Název a kategorie šablony
- Číslo verze a datum poslední revize
- Autor a schvalovatel
- Kontrolní seznam navazujících kroků

### Formát šablony

```markdown
## Šablona: {{template_name}}
**Kategorie**: {{category}}
**Verze**: {{version}} | **Poslední revize**: {{date}}
**Schválil/a**: {{approver}}

### Použít, když
- [Podmínka 1]
- [Podmínka 2]

### NEPOUŽÍVAT, když (spouštěče eskalace)
- [Spouštěč 1]
- [Spouštěč 2]

### Proměnné
| Proměnná | Popis | Příklad |
|---|---|---|
| {{var1}} | [co to je] | [vzorová hodnota] |
| {{var2}} | [co to je] | [vzorová hodnota] |

### Předmět
[Šablona předmětu s {{proměnnými}}]

### Tělo
[Tělo odpovědi s {{proměnnými}}]

### Navazující kroky
1. [Krok 1]
2. [Krok 2]

### Poznámky
[Jakékoliv zvláštní pokyny pro uživatele této šablony]
```

## Formát výstupu

```
## Vygenerovaná odpověď: [Typ dotazu]

**Komu**: [příjemce]
**Předmět**: [předmět]

---

[Tělo odpovědi]

---

### Kontrola eskalace
[Potvrzení, že nebyly detekovány žádné spouštěče eskalace, NEBO vlajkované spouštěče s doporučeními]

### Navazující kroky
1. [Úkony po odeslání]
2. [Připomínky k zařazení do kalendáře]
3. [Požadavky na sledování nebo logování]
```

## Poznámky

- Návrh odpovědi vždy předložte uživateli ke kontrole, než jej doporučíte odeslat
- Pokud je přes MCP připojen e-mail, nabídněte vytvoření konceptu e-mailu s odpovědí
- Sledujte lhůty pro odpověď a nabídněte nastavení připomínek v kalendáři
- U regulovaných odpovědí (DSR, předvolání) vždy uveďte aplikovatelnou lhůtu a regulatorní požadavky
- Šablony by měly být živé dokumenty; při úpravě šablonové odpovědi uživatelem navrhněte aktualizace, aby bylo možné šablonu časem zlepšovat

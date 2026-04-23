---
name: zadost-o-podpis
description: Připravte a nasměrujte dokument k elektronickému podpisu — projděte kontrolní seznam před podpisem, nastavte pořadí podepisování a odešlete k podpisu. Použijte, když je smlouva finalizována a připravena k podpisu, při ověřování názvů subjektů, příloh a podpisových bloků před odesláním nebo při sestavování obálky se sekvenčními či paralelními signatáři.
argument-hint: "<dokument nebo smlouva k odeslání>"
---

# /zadost-o-podpis -- Směrování elektronického podpisu

> Pokud narazíte na neznámé zástupné symboly nebo potřebujete zjistit, které nástroje jsou propojeny, viz [CONNECTORS.md](../../CONNECTORS.md).

Připravte dokument k elektronickému podpisu — ověřte úplnost, nastavte pořadí podepisování a nasměrujte k podpisu.

**Důležité**: Tento příkaz pomáhá s právními workflow, ale neposkytuje právní poradenství ve smyslu zákona č. 85/1996 Sb. o advokacii. Před odesláním k podpisu ověřte, že jsou dokumenty ve finální podobě.

## Použití

```
/zadost-o-podpis $ARGUMENTS
```

Připravit k podpisu: @$1

## DirectCase MCP -- ověření oprávnění k podpisu

Pokud je připojen **DirectCase MCP** (`https://mcp.directcase.ai/mcp`), využij jej k ověření oprávněnosti signatáře protistrany **před odesláním dokumentu k podpisu**:

- **`search_company`** — ověř v obchodním rejstříku: statutární orgán, způsob jednání za společnost (samostatně / společně), oprávněné osoby k zastupování (prokurista), rozsah prokury
- **`search_company_documents`** — plná moc zapsaná ve sbírce listin, zápis o volbě členů statutárního orgánu
- **`search_law_parallel`** — ověř požadavky na formu podpisu pro daný typ úkonu (§ 560 a násl. OZ pro zvláštní formu, zák. č. 297/2016 Sb. o službách vytvářejících důvěru pro elektronické transakce, nařízení eIDAS (EU) č. 910/2014). **Volat pouze jednou.**

U úkonů vyžadujících podpis statutárního orgánu nebo kvalifikovaný elektronický podpis (KEP) signalizuj před odesláním. Pokud nelze oprávnění ověřit, doporuč před podpisem vyžádat aktuální výpis z OR nebo plnou moc.

## Workflow

### Krok 1: Přijměte dokument

Přijměte dokument v libovolném formátu:
- **Nahraný soubor**: PDF, DOCX
- **URL**: Odkaz na dokument v ~~cloudovém úložišti nebo ~~CLM
- **Reference**: „MSA s Acme Corp, kterou jsme včera finalizovali"

### Krok 2: Kontrolní seznam před podpisem

Před odesláním k podpisu ověřte:

```markdown
## Kontrolní seznam před podpisem

- [ ] Dokument je ve finální, odsouhlasené podobě (žádné otevřené redline úpravy)
- [ ] Všechny přílohy a dodatky jsou přiloženy
- [ ] Správné názvy právních subjektů v podpisových blocích
- [ ] Data jsou správná nebo ponechána prázdná pro datum podpisu
- [ ] Podpisové bloky odpovídají oprávněným osobám
- [ ] Byla získána všechna požadovaná interní schválení
- [ ] Dokument byl zkontrolován příslušným právníkem
```

### Krok 3: Nakonfigurujte podepisování

Shromážděte podrobnosti o podepisování:
- **Signatáři**: Kdo musí podepsat? (jména, e-maily, funkce)
- **Pořadí podepisování**: Sekvenční, nebo paralelní?
- **Interní schválení**: Musí někdo schválit dokument předtím, než podepíše protistrana?
- **Kopie pro příjemce (CC)**: Kdo má obdržet kopii podepsaného dokumentu?

### Krok 4: Nasměrujte k podpisu

**Pokud je ~~elektronický podpis propojen:**
- Vytvořte podpisovou obálku/žádost
- Nastavte podpisová pole a pořadí
- Přidejte případné požadované pole pro parafy nebo datum
- Odešlete k podpisu

**Pokud není propojen:**
- Vygenerujte pokyny k podepsání
- Poskytněte dokument naformátovaný pro vlastnoruční podpis nebo manuální elektronický podpis
- Uveďte seznam všech signatářů s kontaktními údaji

Poznámka k elektronickým podpisům v ČR: Podle zák. č. 297/2016 Sb. o službách vytvářejících důvěru pro elektronické transakce a nařízení eIDAS (EU) č. 910/2014 je kvalifikovaný elektronický podpis nejvyšším standardem a je právně rovnocenný vlastnoručnímu podpisu.

## Výstup

```markdown
## Žádost o podpis: [Název dokumentu]

### Podrobnosti dokumentu
- **Typ**: [MSA / NDA / SOW / dodatek / atd.]
- **Smluvní strany**: [Strana A] a [Strana B]
- **Počet stran**: [X]

### Kontrola před podpisem: [V POŘÁDKU / ZJIŠTĚNY PROBLÉMY]
[Uveďte případné problémy, které je třeba vyřešit před odesláním]

### Konfigurace podepisování
| Pořadí | Signatář | E-mail | Role |
|-------|--------|-------|------|
| 1 | [Jméno] | [e-mail] | [Oprávněná osoba Strany A] |
| 2 | [Jméno] | [e-mail] | [Oprávněná osoba Strany B] |

### Příjemci v kopii (CC)
- [Jméno] — [e-mail]

### Stav
[Odesláno k podpisu / Připraveno k odeslání / Je třeba nejprve vyřešit problémy]

### Další kroky
- [Co lze očekávat po odeslání]
- [Očekávaná doba vyřízení]
- [Následný krok, pokud nebude podepsáno do X dnů]
```

## Tipy

1. **Pečlivě zkontrolujte názvy subjektů** — Nejčastější chybou při podepisování jsou nesprávné názvy právních subjektů.
2. **Ověřte oprávnění** — Ujistěte se, že každý signatář je oprávněn zavazovat svou organizaci (statutární orgán nebo osoba s plnou mocí).
3. **Uchovejte kopii** — Podepsané kopie by měly být ihned po podpisu uloženy v ~~cloudovém úložišti nebo ~~CLM.

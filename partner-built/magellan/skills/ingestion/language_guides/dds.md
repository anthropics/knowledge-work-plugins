# DDS (Data Description Specifications) Reference Guide

## Overview

DDS is IBM's language for defining database files, display screens, printer layouts, and menus on the AS/400 (IBM i). DDS compiles into system objects — it is NOT executable code. It defines the STRUCTURE and ACCESS PATHS.

DDS is fixed-format (column-positional). A line describes a record format, a field, a key, or a keyword.

- **Physical files** (`.pf`): Database tables. 1 record format.
- **Logical files** (`.lf`): Views/indexes over physical files.
- **Display files** (`.dspf`): Green screen (5250) definitions.
- **Printer files** (`.prtf`): Report layouts.

## Key Constructs

### Physical Files — Database Tables

```
A          R CUSTREC                  TEXT('Customer Master')
A            CUSTID        10A       
A            CUSTNAME      50A        COLHDG('Cust' 'Name')
A            CUSTBAL        9P 2     
A            STATUS         2A       
A          K CUSTID
```

- `A`: DDS line indicator.
- `R`: Record format name.
- Data Types: `A` (Alphanumeric), `P` (Packed decimal), `S` (Signed/zoned decimal), `L/T/Z` (Date/Time/Timestamp).
- `K`: Key field (primary index).

### Logical Files — Views and Indexes

```
A          R CUSTBYNM                 PFILE(CUSTMAST)
A            CUSTID
A            CUSTNAME
A          K CUSTNAME
A          S STATUS        COMP(EQ 'AC')
```

- `PFILE`: Base physical file.
- `K`: Selects an alternative access path for DB read operations.
- `S` / `O`: Select / Omit. A static filter applied across the file ("WHERE STATUS = 'AC'"). Programs reading this LF never see omitted rows.

### Display Files — Screen Definitions

```
A          R INQUIRY
A                                      CA03(03 'Exit')
A            CUSTID    10A  B  5  2    TEXT('Input ID')
A            CUSTBAL    9P 2O  9  2    EDTCDE(J)
```

- `B` = Both (I/O), `I` = Input, `O` = Output.
- `CA03(03...)` maps F3 key to Indicator 03.
- `EDTCDE(J)` applies a formatting mask (commas, decimals) to a raw number.

### Field References

```
A            CUSTID    R             REFFLD(CUSTID *LIBL/CUSTREF)
```

- `R` (Reference) and `REFFLD`: The field relies entirely on an external Data Dictionary file for its datatype, length, and description.

## Common Patterns

### LF Subsetting (Logical Views)

A Master PF might have 10 LFs over it.

- `LF1`: Key = CUSTID, `S STATUS = 'ACTIVE'`
- `LF2`: Key = ZIPCODE, `S STATE = 'NY'`
RPG programs issue a `CHAIN` to `LF2` implicitly passing a zipcode, completely shielding the RPG prog from the "WHERE" clause logic.

### Join Logical Files

```
A          R ORDREC                   JFILE(ORDHDR ORDLINE)
A          J                         JOIN(1 2)
A                                    JFLD(ORDID ORDID)
A            ORDID         JREF(1)
```

Defines a permanent DB-level join matching Header lines to Detail lines.

## What Carries Business Logic

**Extract facts from these**:

- `K` (Key) fields — reveal the primary query axes of the business data.
- `S` / `O` (Select/Omit) — define core business domains ("Active Status", "Expired Policy").
- `JFILE` / `JOIN` / `JFLD` — define exact foreign keys and relationships between datasets.
- `EDTCDE` / `EDTWRD` — formatting hints reveal if a 9P0 is a Phone Number, SSN, or Dollar value.
- `COMP`, `RANGE`, `VALUES` (in DSPF) — dictate hardcoded UI input validation rules.
- Field names and `TEXT` keywords document the Data Dictionary.

**Skip these (boilerplate)**:

- Row/Column screen positioning coordinates (`5  2`).
- Screen colors (`COLOR(BLU)`), attributes (`DSPATR`), and high-lighting.
- Generic function key descriptors without business routing context.

## Common Misinterpretations

1. **Logical Files are NOT clones or duplicates.** They are inverted lists/indexes over physical data. Updating an LF updates the PF.
2. **Select/Omit is not a runtime parameter.** An LF hardcodes the 'WHERE' clause. An RPG program cannot dynamically change an LF's Select condition.
3. **The 10-char limit generates heavy acronyms.** `PFDEALRMST` = Dealer Master. Rely entirely on the `TEXT` or `COLHDG` attributes for meaning.
4. **Keyed files map 1:1 with RPG operations.** An RPG program executing `CHAIN (Name)` means it *must* be pointing at an LF keyed by Name.
5. **Reference fields hide schema.** A DDS line with just an `R` and no type (`10A`) means the AI must lookup the referenced dictionary file to know what data exists here.

## File Naming Conventions

- Extns: `.pf`, `.lf`, `.dspf`, `.prtf`.
- Formats: Prefix `PF` = Physical, `LF` = Logical, `DS` = Display, `PR` = Printer.

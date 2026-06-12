# RPG ILE / RPG IV Reference Guide

## Overview

RPG (Report Program Generator) is the foundational business application language on IBM i (AS/400). RPG programs compile directly to highly optimized DB2 access modules using the ILE (Integrated Language Environment) runtime.

Code exists in two primary states:

- **Free-format** (modern): Begins with `**FREE`. Utilizes clean keywords `DCL-S`, `DCL-PROC`, `IF / ENDIF`, `READ / CHAIN`.
- **Fixed-format** (legacy): Fully rigid columns driven by Spec indicators (`H`, `F`, `D`, `C`, `O`). The letter in Column 6 defines the operation parameters dictating compiler interpretation.

Most legacy migrations intercept a hybrid of Fixed declarations spanning into `/FREE` calculation blocks.

## Key Constructs

### File and Program Structure

- `CTL-OPT` (Free) / `H-spec` (Fixed): Header. Declares compilation formats, Date bounds, and subsystem Activation Groups.
- `DCL-F` (Free) / `F-spec` (Fixed): File Declaration. Directly lists DB Physical/Logical definitions.
  - Subspecs include **Primary** `P` (triggers implicit logic cycle over every record implicitly) vs **Full Procedural** `F` (user issues `READ/CHAIN` manually).
- `DCL-DS` (Data Structures): Creates nested variables mirroring exactly the file's layout or generic API schemas.
- **Service Programs (`.SRVPGM`)**: Exports independent `DCL-PROC` routines to act as Shared Libraries across independent applications.

### File Operations (Database Access)

- **CHAIN**: Keyed database access equivalent to `SELECT ... WHERE idx=key`. `CHAIN (CustomID) LF_FILES`. Sets `%FOUND`.
- `READ` / `READP`: Sequential cursor scroll forward or backward.
- `SETLL` / `SETGT`: Sets Lower Limit / Greater Than. Repositions the database cursor natively without retrieving memory rows.
- `READE`: Read Equal. Scrolls sequentially only so long as the index matches the applied Key parameter.
- `WRITE / UPDATE / DELETE`.

### Built-in Functions (BIFs)

All start with `%`.

- State validation: `%FOUND`, `%EOF`, `%ERROR`.
- Slicing and Padding: `%SUBST`, `%TRIM`, `%SCAN`, `%REPLACE`.
- Math/Dates: `%DEC`, `%CHAR`, `%DATE`, `%DIFF`.
- List structures: `%LOOKUP` (array search).

### Indicators and Control Flow

Indicators are single-bit booleans designated `*IN01` to `*IN99`.

- Fixed-format relies on them as exception mappings (e.g. `CHAIN MASTFILE 45` means "Set `*IN45=*ON` if record is not found").
- **LR (Last Record)**: The most globally important indicator. Execution relies on `*INLR = *ON`. Setting it instructs RPG to commit open tables, kill static memory, and shutdown completely. Leaving it `*OFF` while returning causes the module to persist statically for lightning-fast subsequent calls.
- `IF / DOW / DOU / SELECT`: Standard conditional looping and switches.

## Common Patterns

### Sequential Key Mapping (Set/ReadE)

```rpgle
SETLL (CustID) ORDERLF;
READE (CustID) ORDERLF;
DOW NOT %EOF(ORDERLF);
  // Iterates fully over all Orders belonging strictly to CustID.
  READE (CustID) ORDERLF;
ENDDO;
```

### Table Fetch & Insert

```rpgle
CHAIN (ActNo) PF_ACCTS;
IF NOT %FOUND(PF_ACCTS);
  ACTNO = ActNo;
  STATUS = 'INITIALIZED';
  WRITE RECFMT;
ENDIF;
```

## What Carries Business Logic

**Extract facts from these:**

- `CHAIN`, `READE`, `SETLL` sequences. This dictates the core data entity dependencies and table queries dictating business hierarchy.
- `IF / SELECT` conditions mapping `*INxx` tags or `%FOUND` criteria to internal monetary checks, states, or dates.
- `DCL-F / F-Spec` blocks list exactly which DB tables are natively scoped to this script.
- `UPDATE` statements represent specific business mutations affecting domain state.
- `CALLP`, `EXSR` map modular dependency graphs.
- Hardcoded string constraints (`DCL-C`) act as system constants.

**Skip these (boilerplate):**

- Standard `USROPN` explicit file opening traps unless tied to conditionally loading external sources dynamically.
- Raw layout Display Files loading green-screen (`EXFMT`).
- Empty `*INLR = *ON / RETURN` footers.
- Static padding loops filling empty strings with 0s.

## Common Misinterpretations

1. **LR is not an error code.** It designates lifecycle closure. Service Programs deliberately omit setting LR so memory states stay primed.
2. **PF / LF isn't a code class.** Physical Files are literal SQL Tables. Logical Files are complex SQL Views. RPG accesses both directly out of the `F-Spec`.
3. **The Implicit Logic Cycle (P).** If an `F-spec` designates a file as Primary `P`, the RPG program **has no loop structure**. The compiler implicitly injects a `WHILE NOT EOF` wrapper encompassing the entire code script reading the file once per pass.
4. **CHAIN does not invoke procedures.** It performs a single highly optimized keyed DB fetch replacing SQL natively.
5. **KLIST is a composite key, not parameter args.** `KLIST` groups multiple variable IDs together strictly for use in `CHAIN`/`SETLL` targeting multi-keyed indexes.
6. **Indicators are context-dependent tags.** `*IN35` has no inherent meaning. It means exactly whatever the operation line directly above it assigned it to mean (e.g., "Error Reading", "Key Missing", or "F3 Pressed On Keyboard").

## File Naming Conventions

- Extns: `.rpgle`, `.sqlrpgle` (Embedded SQL).
- Submodules: `.rpgleinc`.
- Modules generated to: `.PGM` or `.SRVPGM` objects via `CRTBNDRPG`.

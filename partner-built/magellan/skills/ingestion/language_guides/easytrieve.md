# Easytrieve (CA Easytrieve Plus) Reference Guide

## Overview

Easytrieve is a report generator and data manipulation 4GL originally developed by Pansophic Systems. It is heavily optimized for batch extraction, file matching, and data validation on mainframes (z/OS).

Source files use `.EZT`, `.EZTV`, or `.EZP` (off-mainframe). Programs are interpreted directly at execution within a JCL step.

**The core architectural concept of Easytrieve is the implicit loop.** The `JOB` statement automatically opens the listed files, reads every record sequentially, executes all logic beneath it once per record, and automatically closes the files at the end. You rarely write a `READ` loop; the platform *is* the read loop.

## Key Constructs

### Program Structure

- **Library Section** (Header): All `FILE` and `W` (Working Storage) declarations must appear before the first `JOB`.
- `FILE CUSTFILE FB(80 0)`: Declares a file. 80-byte Fixed Block format.
- `CUST-NAME 11 25 A`: A field definition maps directly to bytes on the disk record. Start at position 11, length 25, Alphanumeric.
- `W-TOTAL W 8 P 2`: Variable in memory (Working Storage). 8 digits packed, 2 decimals.
- `JOB INPUT CUSTFILE`: The entry point for the process loop.
- `REPORT`: Declarative trailing section detailing report breaks and formatting.

### Data Access & File Operations

- **Implicit Sequential**: The primary file listed on `JOB INPUT primary` is read automatically.
- **Explicit Secondary**: `GET secondary-file` reads a single record from a secondary file manually.
- **Output**: `PUT outfile FROM infile` writes a record.
- **In-Memory Tables**: `FILE REFTBL TABLE`. Loaded entirely into memory before processing. Searched via `SEARCH REFTBL WITH key EQ value`.
- **Match/Merge**: `JOB INPUT FILEA FILEB` automatically reads both files synchronously, aligning them by matching sorting keys.

### Control Flow

- `IF / ELSE / END-IF`: Standard conditionals.
- `DO WHILE ... END-DO`
- `PERFORM paragraph`: Subroutine execution.
- `STOP`: Halts the entire program execution instantly (often used on fatal errors).
- `GOTO label`: Legacy branching.

## Common Patterns

### The Implicit Validation Loop

```easytrieve
FILE TRANSFB FB(100 0)
  TRN-ID    1  10 A
  TRN-AMT  11   8 P 2

JOB INPUT TRANSFB
  IF TRN-AMT > 50000.00
    PRINT AUDIT-REPORT
  ELSE
    PUT PRODFILE FROM TRANSFB
  END-IF
```

This script acts as a filter. Every record > 50K goes to paper, the rest pass through to the next phase of the batch.

### Synchronized File Match / Merge

```easytrieve
FILE MASTER FB(80 0)
  M-KEY 1 10 A
FILE UPDATE FB(80 0)
  U-KEY 1 10 A

JOB INPUT MASTER UPDATE
  IF MATCHED
    PERFORM UPDATE-LOGIC
  ELSE
    IF MASTER
      PERFORM MASTER-ONLY-LOGIC
    END-IF
  END-IF
```

The builtin `MATCHED` boolean implies the `M-KEY` and `U-KEY` aligned perfectly during the automatic dual-read. `IF MASTER` means an orphan master record exists with no update.

### In-Memory Table Lookup

```easytrieve
FILE STATUSTBL TABLE FB(20 0)
  TBL-KEY  1 10 A
  TBL-DESC 11 10 A

JOB INPUT TRANSACTIONS
  SEARCH STATUSTBL WITH TBL-KEY EQ TRN-STATUS
  IF STATUSTBL
    W-DESC = TBL-DESC
  ELSE
    W-DESC = 'UNKNOWN'
  END-IF
```

The `IF STATUSTBL` is true if the in-memory search succeeded.

## What Carries Business Logic

**Extract facts from these:**

- `IF` conditionals — dictate thresholds, limits, and status evaluation.
- `SEARCH ... WITH` operations — explicitly link transactional codes to business reference definitions.
- `JOB INPUT` parameters — show the primary data lineage and match/merge topologies.
- `MATCHED` routing blocks — define the business reconciliation rules between datasets.
- Assignments (`=`) to `W-` fields — calculations accumulating totals or tax.

**Skip these (boilerplate):**

- `REPORT` formatting blocks, `TITLE`, `HEADING`, `LINE` (unless a native calculation occurs inline).
- Absolute byte positions `11 25 A` in File definitions (the layout is structural, the names hold the meaning).
- End of file housekeeping labels.

## Common Misinterpretations

1. **JOB is an implicit loop.** It is not a single execution block. Everything under it executes *N* times for *N* records in the file.
2. **There is no explicit READ for the primary flow.** Do not look for `READ INPUT` to figure out where data comes from. The `JOB` parameter handles it invisibly.
3. **Byte lengths do not equal string lengths for Packed fields.** An 8-byte Packed (`P`) field stores 15 numeric digits (plus a sign).
4. **W-fields vs Record-fields.** A field declared with `W` exists in RAM globally. A field declared without a `W` (e.g. `CUST-ID 1 10 A`) is an overlay on the current disk record buffer.
5. **TABLE files execute entirely in RAM.** A `FILE ... TABLE` is ingested totally at startup. `SEARCH` does no I/O.
6. **MATCHED is a reserved state, not a variable.** It toggles dynamically as the `JOB` iterator balances the two input files.

## File Naming Conventions

- Extns: `.EZT`, `.EZTV`, `.EZP`.
- On Mainframe: Usually stored in a PDS named `EASYTRV` or `EZTSRC`. Max 8 character member names.

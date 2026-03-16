# COBOL ILE Reference Guide

## Overview

COBOL (Common Business-Oriented Language) on the AS/400 (IBM i) runs in the ILE (Integrated Language Environment). COBOL ILE programs (`.cblle`) support bound calls, service programs, and activation groups — features not available in standard COBOL.

COBOL is verbose by design. Programs are structured into four divisions:

1. **IDENTIFICATION DIVISION** — program name and metadata
2. **ENVIRONMENT DIVISION** — file assignments and special names
3. **DATA DIVISION** — all variable and data structure declarations
4. **PROCEDURE DIVISION** — the executable business logic

## Key Constructs

### Data Division — Variable Declarations

```cobol
WORKING-STORAGE SECTION.
01 WS-INV-AMT         PIC 9(7)V99 COMP-3.
01 WS-STATUS          PIC XX.
  88 WS-ACTIVE        VALUE 'AC'.
  88 WS-INACTIVE      VALUE 'IN'.
01 WS-TABLE.
  05 WS-ENTRY OCCURS 10 TIMES INDEXED BY IDX.
     10 WS-ID         PIC X(5).
```

- `PIC 9(7)V99 COMP-3`: Packed Decimal. `V` is implied decimal. `COMP-3` means packed.
- `88` level: Condition names (boolean tests). `IF WS-ACTIVE` tests if `WS-STATUS` = `'AC'`.
- `OCCURS`: Defines an array/table.
- `INDEXED BY`: Defines an index used for `SEARCH` (linear) or `SEARCH ALL` (binary search).

### File Control

```cobol
FILE-CONTROL.
    SELECT CUSTOMER-FILE ASSIGN TO PFDEALRMST
        ORGANIZATION IS INDEXED
        ACCESS MODE IS DYNAMIC
        RECORD KEY IS CUST-ID.
```

- `SELECT ... ASSIGN TO`: Maps a logical file name to a physical database table.

### Procedure Division — Business Logic

```cobol
PROCEDURE DIVISION.
    PERFORM 1000-INITIALIZE
    PERFORM 2000-PROCESS UNTIL WS-EOF = 'Y'
    PERFORM 9000-CLEANUP
    STOP RUN.
```

- `PERFORM ... UNTIL`: Standard loop structure.
- Paragraph names (1000, 2000) indicate a call hierarchy convention.

### File I/O Operations

- `OPEN INPUT/OUTPUT/I-O/EXTEND`: Specific modes enforce constraints.
- `READ file NEXT`: Sequential read.
- `READ file KEY IS key-var`: Random/keyed read.
- `WRITE rec FROM ws-rec`: Insert a new record.
- `REWRITE`: Update a locked record (must immediately follow a successful READ).
- `DELETE`: Remove a locked record.

### String and Table Processing

- `SEARCH ALL`: Binary lookup on an ordered table (must use `INDEXED BY`).
- `STRING ... DELIMITED BY`: Concatenation.
- `UNSTRING txt DELIMITED BY ',' INTO A B`: Heavily used for parsing CSV or delimited files.
- `INSPECT ... TALLYING / REPLACING`: Find, count, and replace characters.

### ILE-Specific Features

- **Bound calls** (`CALL "program"`): Bound calls use the ILE linker (direct). Dynamic calls resolve late.
- **Service programs**: Export shared subprocedures.
- **Activation groups**: Isolate shared opens, COMMIT controls, and overrides.
- **Embedded SQL** (`EXEC SQL ... END-EXEC`): Bypasses native ISAM access for relational processing.

## Common Patterns

### Read-Process Loop

```cobol
PERFORM UNTIL WS-EOF = 'Y'
  READ INPUT-FILE INTO WS-REC
    AT END
      MOVE 'Y' TO WS-EOF
    NOT AT END
      PERFORM 2100-PROCESS-RECORD
  END-READ
END-PERFORM.
```

### Table Lookup (Business Reference Data)

```cobol
SEARCH ALL WS-ENTRY
  AT END 
    MOVE 'NOT FOUND' TO WS-RESULT
  WHEN WS-ID (IDX) = SEARCH-ID
    MOVE 'FOUND' TO WS-RESULT.
```

Table lookups in Working-Storage often house hardcoded business matrices or tiers.

### EVALUATE (Switch) Statement

```cobol
EVALUATE TRUE
  WHEN WS-AMT > 500  PERFORM 3000-HIGH-VALUE
  WHEN WS-STATUS = 'X' PERFORM 4000-EXCEPTION
  WHEN OTHER         PERFORM 5000-STANDARD
END-EVALUATE.
```

## What Carries Business Logic

**Extract facts from these**:

- `IF / EVALUATE` — encodes explicit business branching, thresholds, and conditions.
- `88` levels — definitions of business states (e.g., `88 APPROVED VALUE 'Y'`).
- `SEARCH / SEARCH ALL` — lookups against application-specific code definitions.
- `SELECT ASSIGN TO` — the physical file dependencies.
- `READ / WRITE / REWRITE` — the persistence layers of a business entity.
- Hardcoded literals in `COMPUTE` or `IF` statements representing rates or limits.

**Skip these (boilerplate)**:

- `IDENTIFICATION DIVISION` (metadata).
- `ENVIRONMENT DIVISION` `CONFIGURATION SECTION`.
- Standard `OPEN / CLOSE`.
- `MOVE SPACES` initialization blocks.

## Common Misinterpretations

1. **Paragraph numbers are convention, not syntax.** `3200-MANUAL-REVIEW` acts as a subroutine label. Lower numbers = main line; higher = deeper nested operations.
2. **PIC 9(7)V99 is not a string.** The `V` implies a decimal point. It's stored numerically but displayed based on the PIC. `COMP-3` means packed decimal; `COMP` means binary integer.
3. **88-levels are boolean conditions, not variables.** `88 WS-ACTIVE VALUE 'A'` means "true if WS-STATUS = 'A'". You cannot move data to an 88-level; you evaluate it.
4. **REWRITE requires a prior READ.** A sequential `REWRITE` or update locks the record upon `READ`. It cannot be updated globally without a lock.
5. **MOVE CORRESPONDING hides assignments.** `MOVE CORR WS-REC1 TO WS-REC2` silently matches fields by identical name. It obscures data lineage.
6. **PERFORM vs CALL.** `PERFORM` jumps inside the SAME program. `CALL` accesses an EXTERNAL module.

## File Naming Conventions

- Extns: `.cblle`, `.cbl`, `.cob`.
- Prefixes: Typically `CB` or `C` for COBOL (e.g., `CBLPROC`).
- Copybooks: Include `-CPY` or exist in `QCBLLESRC` as partial members.

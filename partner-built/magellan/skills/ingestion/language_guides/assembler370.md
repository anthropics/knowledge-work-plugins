# IBM Assembler/370 (BAL) Reference Guide

## Overview

IBM Assembler/370 (BAL or HLASM) is the native assembly language for IBM System/370, System/390, and z/OS mainframes. It has been in continuous use since the 1960s. Assembler programs are found in system exits, performance-critical routines, I/O handlers, and legacy business logic that predates COBOL adoption.

Assembler programs are column-sensitive: columns 1-8 hold a label, column 10+ holds the opcode, columns 16+ hold operands. Column 72 marks continuation. `*` in column 1 marks a comment. Macro instructions (`GET`, `PUT`, `OPEN`) expand into multiple machine instructions at assembly time. File extensions are typically `.asm`, `.s`, `.bal`, or PDS members with no extension.

For business rule extraction, the key challenge is that assembler mixes machine-level register manipulation with business logic. The AI must learn to see through the register operations to the data transformations underneath.

## Key Constructs

### Program Structure

- `CSECT`: Control Section — marks the beginning of a separately relocatable block of code.
- `DSECT`: Dummy Section — defines a data layout without allocating storage, used to map record structures over a buffer (like a COBOL COPY).
- `USING`: Resolves symbolic field names to register+offset pairs.
- `LTORG`: Literal pool — places literal constants (`=F'100'`, `=C'ACTIVE'`) in memory.

### Data Access (Database / File I/O)

Assembler accesses files through system macros:

- **Sequential**: `OPEN (INPUTDCB,(INPUT))`, `GET INPUTDCB,BUFFER`, `PUT OUTPUTDCB,BUFFER`, `CLOSE (INPUTDCB)`.
- **File Definition**: `DCB` defines attributes (DSORG, RECFM, LRECL, BLKSIZE, DDNAME).
- **Indexed/VSAM**: Uses `ACB` (Access Method Control Block) and `RPL` (Request Parameter List) macros: `GET RPL=...`, `PUT RPL=...`, `POINT RPL=...` for keyed access.

### Control Flow

- `B label` / `BR R14`: Unconditional branch.
- Conditional branches (`BE`, `BNE`, `BH`, `BL`) rely on the condition code set by the *immediately preceding* instruction.
- `CLC FIELD1,FIELD2`: Compare Logical Character (EBCDIC).
- `CP PKFLD1,PKFLD2`: Compare Packed decimal fields (used for business numbers).
- `TM FLAGBYTE,X'80'`: Test under Mask — tests bits in a byte for status flags.
- `EX R1,INSTRUCTION`: Execute — dynamically modifies and runs an instruction, often used for variable-length moves or compares.

### Program-to-Program Communication

- `BALR R14,R15` or `BASR`: Branch And Link — calls subroutine at R15, saves return in R14.
- `LA R1,PARMLIST`: Load parameter list address into R1 before a call. Parameters are a list of addresses; the last has the high-order bit set (VL convention).
- Register conventions: R1 = args, R13 = save area, R14 = return addr, R15 = entry point / return code.

### Error Handling

- Return codes in R15: `0` = success, `4` = warning, `8` = error, `12`+ = severe.
- `LTR R15,R15` followed by `BNZ ERROR-RTN`: Standard return code test.
- `ABEND code,DUMP`: Abnormal termination.

## Common Patterns

### Packed Decimal Arithmetic (Business Calculation)

```
         ZAP   WKTOTAL,=P'0'       ZERO ACCUMULATOR
         AP    WKTOTAL,INVAMT      ADD INVOICE AMOUNT
         CP    WKTOTAL,THRESHOLD   COMPARE TO THRESHOLD
         BH    OVER-LIMIT          BRANCH IF OVER LIMIT
```

Business rules: total = invoice; if total > threshold, review.

### String Translation & Validation

```
         TRT   INPUTFLD,TRTAB      FIND FIRST NON-NUMERIC
         BZ    VALID-NUM           0 = ONLY NUMERICS FOUND
         B     INVALID-NUM         NON-ZERO = INVALID
```

`TRT` scans a string until it finds a byte with a non-zero entry in `TRTAB`. Heavily used for data cleansing.

### Dynamic Execution

```
         BCTR  R5,0                DECREMENT LENGTH BY 1 FOR EX
         EX    R5,MOVEMAC          EXECUTE MVC WITH DYNAMIC LENGTH
...
MOVEMAC  MVC   TARGET(0),SOURCE    0 LENGTH MEANS 'SUPPLIED BY EX'
```

## What Carries Business Logic

**Extract facts from these:**

- `CP` (Compare Packed), `AP/SP/MP/DP` (Packed Math), `ZAP` — directly implement business math, thresholds, and monetary rules.
- `TRT` (Translate and Test) — implements data validation rules.
- `CVB`/`CVD` (Convert to Binary/Decimal) and `ED` (Edit) — handle date math and report formatting.
- `TM` (Test under Mask) + `BO/BZ/BM` branches — handle multiple boolean business states packed into bytes.
- `DSECT` definitions — the definitive data dictionary for the program.
- `EX` (Execute) statements — often contain complex, dynamic business logic.
- `GET/PUT` targeting VSAM `RPL`s — defines data extraction and persistence.

**Skip these (boilerplate):**

- Standard Entry/Exit Linkage (`STM R14,R12`, `USING`, save area chaining).
- `GETMAIN`/`FREEMAIN` memory management.
- Standard `OPEN`/`CLOSE` macros.
- `EQU` statements defining registers (e.g., `R1 EQU 1`).
- `DS 0D` or `DS 0H` alignment directives.

## Common Misinterpretations

1. **Registers are not business variables.** `R3` has no inherent meaning. Trace what was loaded into it (`L R3,CUSTBAL`) to understand a comparison (`C R3,=F'1000'`). The business meaning is in the memory field.
2. **Branch conditions refer to the PREVIOUS instruction.** `BH OVER-LIMIT` means "branch if CC indicates high". AI must pair each branch with the specific instruction that set the CC.
3. **TRT is not a typical translation.** It's a search mechanism. It does not alter the string; it sets condition codes and registers based on a lookup table.
4. **Packed decimal is not readable as text.** `DS PL5` stores 1234567.89 as hex `01234567 8C`. Do not mistake `A/S/C` (binary math) for `AP/SP/CP` (packed math).
5. **DSECT is not executable code.** It maps memory. `USING CUSTREC,R6` applies names to offsets from R6.
6. **MVC is a byte copy, not a value assignment.** `MVC TARGET(5),=C'YES'` copies exactly 5 bytes: 'YES' plus 2 bytes of whatever follows in memory.

## File Naming Conventions

- `.asm`, `.s`, `.bal`, `.mlc`: Assembler source files.
- PDS members: 1-8 chars uppercase, program name.
- `.mac`, `.copy`: Macro libraries and DSECT definitions.

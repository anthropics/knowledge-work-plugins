# Fastly Compute WASM Adaptation

Convert core WebAssembly modules to the WASM Component Model format.

## Overview

Fastly Compute uses the WebAssembly Component Model for its services. If you have a core WASM module (traditional `.wasm` binary), you need to adapt it to a component before it can run on Fastly.

## Quick Start

```bash
# Adapt a WASM module (output: input.component.wasm)
viceroy adapt module.wasm

# Adapt with custom output name
viceroy adapt -o output.wasm module.wasm

# Adapt a WAT (text format) file
viceroy adapt module.wat
```

## Command Reference

```bash
viceroy adapt [OPTIONS] <WASM_FILE>
```

### Arguments

| Argument      | Description                                                 |
| ------------- | ----------------------------------------------------------- |
| `<WASM_FILE>` | Path to the WASM module (`.wasm`) or WAT text file (`.wat`) |

### Options

| Option                | Description                                                     |
| --------------------- | --------------------------------------------------------------- |
| `-o, --output <PATH>` | Output filename (default: `<input>.component.wasm`)             |
| `-v`                  | Increase verbosity (`-v` = INFO, `-vv` = DEBUG, `-vvv` = TRACE) |

## When to Use

### Manual Adaptation

Use `viceroy adapt` when you:
- Have a pre-built core WASM module from another toolchain
- Need to test adaptation separately from execution
- Want to inspect the adapted component

### Auto-Adaptation

Viceroy can automatically adapt modules at runtime:

```bash
# Auto-adapt when serving
viceroy --adapt -C fastly.toml module.wasm

# Auto-adapt when running tests
viceroy run --adapt -C fastly.toml module.wasm
```

## Input Formats

### Binary WASM (`.wasm`)

Standard WebAssembly binary format:
```bash
viceroy adapt module.wasm
```

### Text Format (`.wat`)

WebAssembly text format for debugging or hand-written modules:
```bash
viceroy adapt module.wat
```

## Checking if Already a Component

Viceroy will error if the input is already a component:
```
ERROR File is already a component: module.wasm
```

This is expected behavior - components don't need adaptation.

## How Adaptation Works

The adapter:
1. Reads the core WASM module
2. Wraps it with Fastly Compute host function interfaces (WIT bindings)
3. Produces a component that can interact with Fastly's runtime

The adapter is bundled with Viceroy at:
```
wasm_abi/data/viceroy-component-adapter.wasm
```

## Troubleshooting

### "Failed to adapt module"

The module may use unsupported features or have invalid structure. Check:
- Module was compiled for `wasm32-wasi` or `wasm32-wasip1` target
- Module doesn't use features incompatible with WASI Preview 1

### "Failed to parse wat"

For WAT files, ensure the syntax is correct. Use a WASM validator:
```bash
wasm-tools validate module.wat
```

### Module works locally but fails on Fastly

Some features may work in Viceroy but not in Fastly production:
- Check for use of `--unknown-import-behavior trap` flag
- Verify all used APIs are supported in Fastly production
- Review the Fastly Compute API documentation

## Example Workflow

```bash
# 1. Build your Rust application
cargo build --target wasm32-wasip1 --release

# 2. Adapt to component (if not using fastly CLI)
viceroy adapt target/wasm32-wasip1/release/myapp.wasm -o bin/main.wasm

# 3. Test locally
viceroy -C fastly.toml bin/main.wasm

# 4. Deploy to Fastly
fastly compute deploy
```

## Note on Fastly CLI

When using `fastly compute build`, the CLI handles adaptation automatically. You typically only need `viceroy adapt` for:
- Custom build pipelines
- Debugging adaptation issues
- Working with modules from other sources

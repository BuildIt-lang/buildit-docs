---
title: Build Configuration
kind: guide
header: Makefile
keywords: build configuration, DEBUG, RECOVER_VAR_NAMES, TRACER_USE_LIBUNWIND, EXTRA_CFLAGS, ENABLE_D2X, LIBUNWIND_PATH, CONFIG_STR, build.config, Makefile.inc
---

# Build Configuration

BuildIt exposes a small set of build-time configuration options through `make`
variables.

Pass them on the command line:

```sh
make DEBUG=1
make RECOVER_VAR_NAMES=1
make EXTRA_CFLAGS="-DDEBUG_VARS"
```

To make configuration persistent for a local checkout, write the assignments in
`Makefile.inc` at the top level of the BuildIt repository:

```make
DEBUG=1
RECOVER_VAR_NAMES=1
```

The top-level `Makefile` includes `Makefile.inc` before the rest of the build
configuration is evaluated.

The top-level `Makefile` tracks the configuration options in `CONFIG_STR`. When
one of those values changes, BuildIt removes the existing build directory and
rebuilds with the new configuration.

## Tracked Options

The following options are part of `CONFIG_STR` and therefore trigger a rebuild
when changed.

### DEBUG

```make
DEBUG ?= 0
```

When `DEBUG=1`, BuildIt is compiled with debug information:

```text
-g -gdwarf-4
```

When `DEBUG=0`, internal compilation flags include `-O3`.

`DEBUG` is also enabled automatically when `RECOVER_VAR_NAMES=1` or
`ENABLE_D2X=1`.

### RECOVER_VAR_NAMES

```make
RECOVER_VAR_NAMES ?= 0
```

When `RECOVER_VAR_NAMES=1`, BuildIt attempts to recover first-stage C++ variable
names and use them in generated code. This mode is only supported on Linux.

This option:

- enables `DEBUG`
- defines `RECOVER_VAR_NAMES`
- links with `libdwarf` and `libunwind`
- switches sample test comparisons to the `outputs.var_names` expected outputs

Use this when you want generated code to preserve more source-level names during
development or debugging.

### TRACER_USE_LIBUNWIND

```make
TRACER_USE_LIBUNWIND ?= 0
```

When `TRACER_USE_LIBUNWIND=1`, BuildIt defines `TRACER_USE_LIBUNWIND` and links
against `libunwind`.

With this option enabled, BuildIt uses `libunwind` instead of `libbacktrace` to
construct static tags.

### EXTRA_CFLAGS

```make
EXTRA_CFLAGS ?=
```

Additional flags appended to BuildIt's public `CFLAGS`.

Example:

```sh
make EXTRA_CFLAGS="-DDEBUG_VARS"
```

Use this for local compile-time switches or extra compiler options that are not
covered by the standard configuration variables.

### ENABLE_D2X

```make
ENABLE_D2X ?= 0
```

When `ENABLE_D2X=1`, BuildIt builds with D2X support enabled.

The `deps/d2x` submodule must be fetched before building with this option.

This option:

- enables `DEBUG`
- enables `RECOVER_VAR_NAMES`
- defines `ENABLE_D2X`
- adds the D2X include path
- links against `libd2x`

The [`block::c_code_generator`](../03_block/c-code-generator.md) D2X output path
requires BuildIt to be built with this option. Calling D2X code generation
without `ENABLE_D2X=1` asserts at runtime.

## Supporting Variables

### LIBUNWIND_PATH

```make
LIBUNWIND_PATH ?= _UNSET_
```

`LIBUNWIND_PATH` is not part of `CONFIG_STR`, but it is used when
`RECOVER_VAR_NAMES=1` or `TRACER_USE_LIBUNWIND=1`.

Set it when `libunwind` is installed outside the default compiler and linker
search paths:

```sh
make RECOVER_VAR_NAMES=1 LIBUNWIND_PATH=/path/to/libunwind
```

BuildIt adds:

```text
-I $(LIBUNWIND_PATH)/include
-L $(LIBUNWIND_PATH)/lib
```

## Configuration Rebuilds

BuildIt writes the current `CONFIG_STR` to:

```text
build/build.config
```

On the next `make`, if the stored value differs from the new configuration, the
build directory is removed and recreated before compiling.

This avoids mixing object files compiled with incompatible build-time options.

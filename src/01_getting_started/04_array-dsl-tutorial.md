---
title: Array DSL Tutorial
kind: tutorial
keywords: tutorial, BuildIt Array DSL, buildit-array, barray, DSL, array, numpy, GPU, CUDA, D2X, constant propagation, static analysis, loop induction, cross product, to_device, to_host
---

# Array DSL Tutorial

The
[buildit-array](https://github.com/BuildIt-lang/buildit-array)
repository is a hands-on tutorial for building a small array DSL on top of
BuildIt.

The tutorial walks through a NumPy-like array language implemented as a C++
library. The DSL supports staged array operations such as pointwise addition,
pointwise multiplication, cross products, CPU code generation, GPU code
generation, and D2X debugging.

Use this tutorial after reading [Concepts](03_concepts.md) if you want to see
how BuildIt can be used to implement a domain-specific language rather than just
individual staged functions.

## Get The Tutorial

Clone the tutorial with submodules:

```sh
git clone --recursive https://github.com/BuildIt-lang/buildit-array.git
```

If you already cloned without `--recursive`, fetch the submodules with:

```sh
git submodule init
git submodule update
```

The tutorial builds BuildIt as a dependency, then builds the array DSL library
and samples.

## Build And Run

From the tutorial repository:

```sh
make -j$(nproc)
./build/sample1
```

The first sample prints generated code to standard output. Early in the
tutorial, that generated code is intentionally incomplete or incorrect; the
exercise TODOs progressively fill in the DSL implementation.

## What The Tutorial Teaches

The tutorial is structured around implementation TODOs in the DSL skeleton.

### Generate Initialization Code

The array type stores its backing buffer as a `dyn_var<T*>`. The first exercise
adds generated loops that initialize every element of an array.

This demonstrates the difference between writing first-stage C++ that runs
during extraction and writing loops with `dyn_var` indices that appear in the
generated program.

### Induce Loop Nests

Pointwise array operations need one generated loop per output dimension.

The tutorial introduces a recursive helper that creates a loop at each dimension
and then emits the computation in the innermost loop. This is a practical
example of using BuildIt to generate structured control flow from ordinary C++.

### Add Static Correctness Checks

Before generating code for pointwise operations, the DSL checks that operand
dimensions agree.

This analysis happens in the first stage, so it should use ordinary C++ values
or [`builder::static_var`](../02_builder/static-var.md), not
[`builder::dyn_var`](../02_builder/dyn-var.md). The check fails while compiling
the staged program instead of generating invalid out-of-bounds code.

### Optimize Constant Arrays

The tutorial tracks whether an array currently represents a constant value.

When all elements are known to be the same, later reads can directly emit the
constant instead of generating separate initialization loops. This is a small but
useful example of domain-specific static analysis and constant propagation.

### Map Computation To CUDA

BuildIt annotations can map generated loop nests to CUDA kernels.

The tutorial uses a scheduling-style API such as `run_on_gpu` to decide when
array computations should be generated as GPU code. Internally, the DSL emits
annotations that BuildIt's CUDA extraction pass can consume.

### Track Host And GPU Storage

The array DSL tracks where each array currently lives: host or GPU.

The tutorial uses first-stage state to reject computations that would read data
from the wrong device. This shows how a DSL can enforce domain-specific
correctness rules while generating low-level target code.

### Add A New Operation

The final exercise asks you to implement cross product support for 2D array
expressions.

This demonstrates how new DSL operations can be added by combining staged
operators, shape analysis, and generated loop nests.

## D2X Debugging

The tutorial also includes a D2X debugging section.

D2X is a companion library for debugging across stages. In this tutorial, it is
used to inspect and debug generated code without changing the DSL program. D2X
currently requires the relevant BuildIt build configuration and is not supported
on macOS in the tutorial setup.

See [Build Configuration](02_build-configuration.md#enable-d2x) for the BuildIt
side of enabling D2X.

## Why This Tutorial Is Useful

The array tutorial shows the typical shape of a BuildIt-based DSL:

1. Define staged wrapper types that expose a domain-specific interface.
2. Store runtime data as `dyn_var` members.
3. Store compile-time facts and scheduling choices as first-stage state.
4. Generate loop nests and low-level code from high-level operations.
5. Use first-stage analysis to enforce DSL correctness.
6. Use annotations and passes to target GPUs.

This is the same general pattern used by larger BuildIt DSLs: the user-facing
DSL stays as a normal C++ library, while BuildIt supplies staging, generated IR,
and target code generation hooks.

## See Also

- [buildit-array tutorial repository](https://github.com/BuildIt-lang/buildit-array)
- [Concepts](03_concepts.md)
- [Build Configuration](02_build-configuration.md)
- [`builder::dyn_var`](../02_builder/dyn-var.md)
- [`builder::static_var`](../02_builder/static-var.md)
- [CUDA Extraction](../03_block/cuda-extraction.md)

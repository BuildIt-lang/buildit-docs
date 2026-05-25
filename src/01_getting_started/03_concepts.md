---
title: Concepts
kind: guide
keywords: concepts, staging, multi-stage programming, first stage, second stage, dyn_var, static_var, builder_context, block, AST, extraction, generated code, control flow, static tags, annotations, passes, DSL, domain specific language, schedule, algorithm, BuilDSL
---

# Concepts

BuildIt is a type-based multi-stage programming library for C++.

In a multi-stage program, one stage of execution produces code for a later
stage. With BuildIt, the first-stage program is ordinary C++ that uses BuildIt
types. Running that first-stage program produces a BuildIt AST, which can then
be inspected, transformed, printed as C-like code, extracted into CUDA kernels,
or dynamically compiled.

## First Stage And Second Stage

The first stage is the C++ program you compile and run directly.

The second stage is the generated program represented by BuildIt's IR. That
program may later be emitted as C/C++/CUDA code or compiled through BuildIt's
dynamic compilation APIs.

The key idea is that binding time is expressed through types:

- [`builder::static_var<T>`](../02_builder/static-var.md) is a first-stage value.
- [`builder::dyn_var<T>`](../02_builder/dyn-var.md) is a second-stage value.

If an expression depends on `static_var` values, it is evaluated while BuildIt is
extracting the program. If it depends on `dyn_var` values, BuildIt records the
expression into the generated AST.

```cpp
builder::static_var<int> factor = 4;
builder::dyn_var<int> x;

builder::dyn_var<int> y = x * factor;
```

Here `factor` is known while the staged function is being extracted. `x` is a
second-stage value, so `x * factor` becomes an expression in the generated code.

## dyn_var

[`builder::dyn_var<T>`](../02_builder/dyn-var.md) represents a value of type `T`
in the generated program.

BuildIt overloads operators on `dyn_var` so ordinary C++ syntax builds IR
instead of computing a normal C++ value immediately:

```cpp
builder::dyn_var<int> a;
builder::dyn_var<int> b;
builder::dyn_var<int> c = (a + 1) * b;
```

This records an expression tree for `(a + 1) * b`.

Assignments, function calls, member access, pointer access, array access, and
control flow involving `dyn_var` values are captured into the generated program.

## static_var

[`builder::static_var<T>`](../02_builder/static-var.md) represents a value that
exists during extraction.

Use `static_var` when first-stage logic should specialize the generated code:

```cpp
builder::static_var<int> unroll = 4;

for (builder::static_var<int> i = 0; i < unroll; i = i + 1) {
    // This loop runs while extracting and can emit repeated generated code.
}
```

`static_var` is useful for parameters that control code shape: sizes, unroll
factors, format choices, or other specialization decisions.

## Extraction

[`builder::builder_context`](../02_builder/builder-context.md) executes a staged
function and extracts the generated AST:

```cpp
builder::builder_context context;
auto ast = context.extract_function_ast(foo, "foo");
```

The returned AST is a [`block::stmt`](../03_block/statement-types.md). In
practice, extracted functions are usually represented as `block::func_decl`
nodes.

Once extracted, the AST can be:

- printed with [`block::c_code_generator`](../03_block/c-code-generator.md)
- rewritten with [`block::block_replacer`](../03_block/block-replacer.md)
- searched with [`block::matcher::find_all_matches`](../03_block/01_matchers/find-all-matches.md)
- transformed by passes such as [`block::eliminate_redundant_vars`](../03_block/redundant-copy-elimination.md)
- compiled with [`builder::compile_function`](../02_builder/compile-function.md)

## Control Flow

In C++, ordinary operators can be overloaded, but `if`, `for`, and `while` cannot
be overloaded directly.

BuildIt still captures staged control flow written in normal C++ syntax. It does
this by executing the staged function as a first-stage program and using
BuildIt's runtime state, tags, and repeated execution to discover the control
flow induced by `dyn_var` conditions.

```cpp
builder::dyn_var<int> x;

if (x > 0) {
    x = x + 1;
} else {
    x = x - 1;
}
```

The condition `x > 0` is a second-stage expression. BuildIt records the
condition and both branches into the generated AST instead of choosing a branch
once and discarding the other.

This is one of BuildIt's central design points: users can write ordinary C++
control flow, and BuildIt extracts structured generated control flow from it.

## Static Tags

BuildIt must recognize when two first-stage executions are observing the same
static program point.

It uses [static tags](../04_util/tracer-tag.md) for this. A tag identifies a
point in the staged program and helps BuildIt line up observations across
repeated executions. Tags are also used to avoid exponential blowup when BuildIt
explores staged branches.

Most users do not manipulate static tags directly, but they matter for build
configuration. For example, `TRACER_USE_LIBUNWIND` changes how BuildIt
constructs static tags.

## Blocks

The generated program is represented with classes in the `block` namespace.

Important categories include:

- [`block::expr`](../03_block/expression-types.md): value-producing operations
- [`block::stmt`](../03_block/statement-types.md): declarations, control flow, and function bodies
- [`block::type`](../03_block/type-types.md): generated C/C++ types
- [`block::var`](../03_block/var.md): variables and named values

Builder APIs create these nodes for you. Advanced users can inspect, transform,
or generate code from them directly.

## Passes And Rewriting

After extraction, the AST can be transformed before code generation.

Common tools include:

- [`block::annotation_finder`](../03_block/annotation-finder.md), for locating annotated statements
- [`block::matcher::find_all_matches`](../03_block/01_matchers/find-all-matches.md), for finding expression patterns
- [`block::matcher::replace_match`](../03_block/01_matchers/replace-match.md), for replacing matched expression trees
- [`block::block_replacer`](../03_block/block-replacer.md), for writing custom rewriting visitors
- [`block::eliminate_redundant_vars`](../03_block/redundant-copy-elimination.md), for removing redundant generated temporaries

These operate on the same `block` AST produced by extraction.

## Annotations

[`builder::annotate`](../02_builder/annotate.md) attaches string labels to the
next generated statement.

Annotations are a lightweight way to mark IR for later passes. BuildIt uses them
for generated pragmas and CUDA extraction, and users can also find their own
annotations with [`block::annotation_finder`](../03_block/annotation-finder.md).

```cpp
builder::annotate("pragma: unroll");
for (builder::dyn_var<int> i = 0; i < n; i = i + 1) {
    // ...
}
```

Any annotation beginning with `pragma:` becomes a generated `_Pragma`.

## Writing DSLs With BuildIt

BuildIt can be used as the staging layer for an embedded domain-specific
language.

The usual pattern is to implement the DSL as a C++ library whose domain objects
contain or produce BuildIt staged values. Users write ordinary C++ using the DSL
types and operators. Running that code with a `builder_context` extracts a
BuildIt AST, and the DSL implementation can then analyze, transform, and emit
target code from that AST.

This lets a DSL reuse C++ as its frontend:

- C++ syntax, templates, overloads, and type checking define the user interface.
- `dyn_var` values represent runtime data in the generated program.
- `static_var` values and normal C++ values represent compile-time choices that
  specialize the generated program.
- `block` nodes provide the compiler IR for domain-specific passes.

For performance-oriented DSLs, it is often useful to separate algorithm choices
from schedule choices. The algorithm describes what computation should happen.
The schedule controls how that computation is mapped onto a target, such as
serial CPU code, parallel CPU code, or CUDA kernels.

In BuildIt terms, algorithm information often appears as staged computation,
while schedule information is usually first-stage data that controls extraction
or later passes:

```cpp
struct schedule {
    bool use_cuda;
    int threads_per_block;
};
```

The DSL can use that first-stage schedule to decide which annotations to emit,
which passes to run, or which target-specific code generator to use.

Domain-specific analysis can be implemented in several ways:

- encode invariants in the DSL wrapper types
- attach metadata to `block` nodes
- mark important statements with annotations
- inspect the extracted AST with visitors or matchers
- rewrite the AST before code generation

For example, a graph DSL might expose graph traversal operators to the user,
but internally generate loops and annotations that later become CUDA kernels.
The user writes in the graph abstraction; the DSL author controls the lowering
to BuildIt IR and the target-specific transforms.

The BuilDSL paper demonstrates this style by building a graph DSL on top of
BuildIt: the DSL takes an algorithm and schedule, uses BuildIt for staging and
code generation, and adds domain-specific analysis and CUDA-oriented
transformations on top.

## Typical Workflow

Most BuildIt programs follow this shape:

1. Write a staged C++ function using `dyn_var` and `static_var`.
2. Extract it with `builder_context::extract_function_ast`.
3. Optionally run analysis or transformation passes on the `block` AST.
4. Generate code with `c_code_generator`, extract CUDA kernels, or compile the
   generated code dynamically.

For smaller examples, the online tool is useful for inspecting the generated
code. For complete applications, use the project template described in
[Installation](01_installation.md).

## Further Reading

The BuildIt paper gives the full background and extraction algorithm:

[BuildIt: A Type-Based Multi-stage Programming Framework for Code Generation in C++](https://intimeand.space/docs/buildit.pdf)

The BuilDSL paper discusses implementing high-performance DSLs on top of
BuildIt:

[GraphIt to CUDA Compiler in 2021 LOC: A Case for High-Performance DSL Implementation via Staging with BuilDSL](https://intimeand.space/docs/CGO2022-BuilDSL.pdf)

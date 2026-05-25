---
title: builder::builder_context
kind: class
namespace: builder
header: builder/builder_context.h
keywords: builder::builder_context, builder_context, run_rce, feature_unstructured, dynamic_use_cxx, dynamic_compiler_flags, dynamic_header_includes, enable_d2x, extract_function_ast
---

# builder::builder_context

`builder::builder_context` owns the configuration used when BuildIt executes a
staged function and extracts the next-stage AST.

The main API is [`extract_function_ast`](#extract-function-ast), which takes a C++
function and returns a BuildIt IR node representing the generated function.

## Synopsis

```cpp
#include "builder/builder_context.h"

namespace builder {

class builder_context {
public:
    bool run_rce = false;
    bool feature_unstructured = false;
    bool dynamic_use_cxx = false;
    std::string dynamic_compiler_flags = "";
    std::string dynamic_header_includes = "";
    bool enable_d2x = false;

    template <typename F, typename... OtherArgs>
    block::stmt::Ptr extract_function_ast(
        F func_input,
        std::string func_name,
        OtherArgs&&... other_args);
};

}
```

## Configuration Members

| Member | Default | Description |
| --- | --- | --- |
| [`run_rce`](#run-rce) | `false` | Runs redundant variable elimination after loop recovery. |
| [`feature_unstructured`](#feature-unstructured) | `false` | Enables unstructured-control-flow handling. When disabled, extraction attempts structured control-flow recovery such as loop and if-statement reconstruction. |
| [`dynamic_use_cxx`](#dynamic-use-cxx) | `false` | Used by dynamic compilation helpers to emit and compile C++ instead of C. |
| [`dynamic_compiler_flags`](#dynamic-compiler-flags) | `""` | Extra flags appended to the dynamic compilation command. |
| [`dynamic_header_includes`](#dynamic-header-includes) | `""` | Header text emitted before dynamically generated code. |
| [`enable_d2x`](#enable-d2x) | `false` | Enables D2X debug-information support. The BuildIt library must be built with `ENABLE_D2X`. |

## Member Functions

### extract_function_ast

```cpp
template <typename F, typename... OtherArgs>
block::stmt::Ptr extract_function_ast(
    F func_input,
    std::string func_name,
    OtherArgs&&... other_args);
```

Executes `func_input` under the builder context and returns the generated
function AST.

#### Parameters

| Parameter | Description |
| --- | --- |
| `func_input` | Function, function template specialization, or callable to stage. |
| `func_name` | Name assigned to the generated function declaration. |
| `other_args` | First-stage values for parameters that are not supplied as `dyn_var` generated-function arguments. These values must be provided in the exact order in which the corresponding non-`dyn_var` parameters appear in `func_input`'s signature. |

#### Return Value

Returns a `block::stmt::Ptr` pointing to the generated function declaration.

#### Notes

Extraction builds an invocation state, records the requested generated function
name, runs the staged function, then post-processes the resulting AST. The
post-processing pipeline names variables, inserts labels, cleans up removed
sub-expressions, recovers structured control flow when enabled, optionally runs
redundant variable elimination, and detects loop-roll opportunities.

`dyn_var` parameters become parameters of the generated function. Other
parameters are treated as first-stage inputs to extraction, so they must be
passed through `other_args`. BuildIt matches these values positionally against
the original function signature after skipping the `dyn_var` parameters; it does
not match them by name or type.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=c213cc684298237ce33f30c5667428f3 }}

```cpp
#include "blocks/c_code_generator.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include "builder/static_var.h"
#include <iostream>

using builder::dyn_var;
using builder::builder_context;
using builder::static_var;

dyn_var<int> scale(dyn_var<int> x, static_var<int> factor) {
    return x * factor;
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(scale, "scale_by_4", 4);
    block::c_code_generator::generate_code(ast, std::cout, 0);
}
```

## See Also

- [Installation](../01_getting_started/01_installation.md)

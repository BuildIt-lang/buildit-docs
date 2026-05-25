---
title: builder::compile_function
kind: function template
namespace: builder
header: builder/builder_dynamic.h
keywords: builder::compile_function, compile_function, builder::compile_function_with_context, compile_function_with_context, builder::compile_asts, compile_asts, dynamic compilation, function pointer, lookup_name
---

# builder::compile_function

`builder::compile_function` extracts a staged function, generates C or C++ code
for it, compiles that generated code into a dynamic library, and returns a
function pointer to the compiled entry point.

Use it when you want to execute generated code immediately from the same
first-stage program.

`builder::compile_function_with_context` is the configured form. It takes a
[`builder::builder_context`](builder-context.md), so it can use custom dynamic
compiler flags, header includes, code generation settings, and optimization
settings.

## Synopsis

```cpp
#include "builder/builder_dynamic.h"

namespace builder {

template <typename FT, typename... ArgsT>
auto compile_function(FT f, ArgsT... args) -> void*;

template <typename FT, typename... ArgsT>
auto compile_function_with_context(
    builder_context context,
    FT f,
    ArgsT... args) -> void*;

void* compile_asts(
    builder_context context,
    std::vector<block::block::Ptr> asts,
    std::string lookup_name);

}
```

## Behavior

`compile_function(f, args...)` uses a default `builder_context` and forwards to
`compile_function_with_context`.

`compile_function_with_context(context, f, args...)` extracts `f` with generated
function name `execute`, writes generated source code to a temporary file,
compiles that source, loads the compiled result, and returns the address of the
generated `execute` function.

The returned value has type `void*`. You must explicitly cast it to the function
pointer type that matches the generated function signature before calling it.

```cpp
auto fptr = (int (*)(int))compile_function(power, 5);
```

The cast is required because BuildIt loads the compiled entry point dynamically
and cannot express the generated function pointer type in the return type.

## Arguments

`f` is the staged function to extract and compile.

`args...` are first-stage arguments passed to extraction. These are the same
kind of static arguments accepted by
[`builder_context::extract_function_ast`](builder-context.md#extract-function-ast).

## Dynamic Context Settings

Use `compile_function_with_context` when the generated source needs non-default
dynamic compilation settings.

Common context fields include:

- `dynamic_compiler_flags` for additional compiler flags
- `dynamic_header_includes` for generated source includes
- `dynamic_use_cxx` when the generated source should be compiled as C++
- `run_rce` to run redundant variable elimination before compiling

## compile_function_with_context

```cpp
template <typename FT, typename... ArgsT>
auto compile_function_with_context(
    builder_context context,
    FT f,
    ArgsT... args) -> void*;
```

Configured variant of `compile_function`.

The `builder_context` is passed by value, so changes made during extraction and
dynamic compilation do not mutate the caller's context object.

## compile_asts

```cpp
void* compile_asts(
    builder_context context,
    std::vector<block::block::Ptr> asts,
    std::string lookup_name);
```

Compiles a set of already extracted ASTs and returns the symbol named by
`lookup_name`.

Use `compile_asts` when the generated program contains multiple generated
functions, or when the ASTs were built by a workflow other than a single
`compile_function` call. The returned value is still a `void*`, so it must be
explicitly cast to the matching function pointer type before use.

The context controls the same dynamic compilation settings used by
`compile_function_with_context`, such as header includes, compiler flags, and C
versus C++ mode.

## Online Tool Support

`compile_function`, `compile_function_with_context`, and `compile_asts` are not
supported by the BuildIt online TryIt tool. These APIs create temporary source
files, invoke a compiler, load a dynamic library, and require system calls that
are not available inside the online sandbox.

## Example

```cpp
#include "builder/builder_dynamic.h"
#include "builder/dyn_var.h"
#include "builder/static_var.h"
#include <iostream>

using builder::compile_function;
using builder::dyn_var;
using builder::static_var;

static dyn_var<int> power(dyn_var<int> base, static_var<int> exponent) {
    dyn_var<int> result = 1;
    dyn_var<int> x = base;

    while (exponent > 1) {
        if (exponent % 2 == 1) {
            result = result * x;
        }
        x = x * x;
        exponent = exponent / 2;
    }

    return result * x;
}

int main() {
    auto power_5 = (int (*)(int))compile_function(power, 5);
    std::cout << power_5(8) << std::endl;

    return 0;
}
```

## See Also

- [`builder::builder_context`](builder-context.md)
- [`builder::dyn_var`](dyn-var.md)
- [`builder::static_var`](static-var.md)

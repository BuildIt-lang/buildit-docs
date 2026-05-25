---
title: builder::annotate
kind: function
namespace: builder
header: builder/forward_declarations.h
keywords: builder::annotate, annotate, annotation, pragma, _Pragma, CUDA_KERNEL, CUDA_KERNEL_COOP, CUDA_KERNEL_COOP_COPY_OUT
---

# builder::annotate

`builder::annotate` attaches a string annotation to the next generated
statement.

Annotations are metadata on BuildIt's intermediate representation. Later passes
can find them and transform the annotated statement. BuildIt uses this mechanism
for generated pragmas and CUDA kernel extraction.

## Synopsis

```cpp
#include "builder/builder_context.h"

namespace builder {

void annotate(std::string label);

}
```

## Behavior

`annotate(label)` commits any pending staged statements and records `label` in
the current run state. The next generated statement receives that annotation.

Place the call immediately before the statement it should describe:

```cpp
builder::annotate("pragma: ...");
for (builder::dyn_var<int> i = 0; i < n; i = i + 1) {
    // ...
}
```

The annotation string is intentionally open-ended. Passes that understand a
label can act on it; other passes ignore it.

## Labels

Annotation labels are strings. The code generator and transformation passes give
special meaning to some prefixes and constants.

- Any annotation beginning with `pragma:` is emitted as an `_Pragma` before the
  annotated statement in generated code.
- `CUDA_KERNEL`, `CUDA_KERNEL_COOP`, and `CUDA_KERNEL_COOP_COPY_OUT` from
  `blocks/extract_cuda.h` for CUDA extraction

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=91ed4985ec2dfc67def08a6b914b942a }}

```cpp
#include "blocks/c_code_generator.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::annotate;
using builder::builder_context;
using builder::dyn_var;

static void foo() {
    annotate("pragma: omp parallel for");
    for (dyn_var<int> i = 0; i < 16; i = i + 1) {
        dyn_var<int> sum = 0;

        annotate("pragma: unroll");
        for (dyn_var<int> j = 0; j < 8; j = j + 1) {
            sum += j;
        }
    }
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::builder_context`](builder-context.md)
- [CUDA Extraction](../03_block/cuda-extraction.md)

---
title: CUDA Extraction
kind: transform
namespace: block
header: blocks/extract_cuda.h
keywords: CUDA Extraction, extract_cuda_from, extract_single_cuda, CUDA_KERNEL, CUDA_KERNEL_COOP, CUDA_KERNEL_COOP_COPY_OUT, annotate, kernel launch, CUDA
---

# CUDA Extraction

CUDA extraction is a BuildIt IR transform that turns annotated nested loops into
CUDA kernel declarations and replaces the original loop nest with a kernel
launch.

The transform is driven by [`builder::annotate`](../02_builder/annotate.md).
Annotate a two-level `dyn_var` loop nest with one of the CUDA labels from
`blocks/extract_cuda.h`, extract the function AST, then call
`block::extract_cuda_from` on the function body.

## Synopsis

```cpp
#include "blocks/extract_cuda.h"

#define CUDA_KERNEL "kernel:cuda:auto"
#define CUDA_KERNEL_COOP "kernel:cuda:coop"
#define CUDA_KERNEL_COOP_COPY_OUT "kernel:cuda:coop:copy_out"

namespace block {

std::vector<block::Ptr> extract_cuda_from(block::Ptr from);

block::Ptr extract_single_cuda(
    block::Ptr from,
    std::vector<decl_stmt::Ptr>& new_decls);

}
```

## CUDA Labels

`CUDA_KERNEL` extracts the annotated loop nest into a normal CUDA kernel and
replaces the loop with a `kernel<<<blocks, threads>>>(...)` launch followed by
`cudaDeviceSynchronize()`.

`CUDA_KERNEL_COOP` extracts the loop nest into a kernel launched through
`runtime::LaunchCooperativeKernel`.

`CUDA_KERNEL_COOP_COPY_OUT` is the cooperative-kernel variant that also emits
copy-out support for variables captured from the surrounding function.

## Required Loop Shape

CUDA extraction expects the annotation to be attached to a doubly nested
`for` loop:

```cpp
builder::annotate(CUDA_KERNEL);
for (dyn_var<int> cta = 0; cta < cta_count; cta = cta + 1) {
    for (dyn_var<int> tid = 0; tid < thread_count; tid = tid + 1) {
        // kernel body
    }
}
```

The outer loop becomes `blockIdx.x`, and its upper bound becomes the CUDA block
count. The inner loop becomes `threadIdx.x`, and its upper bound becomes the
thread count.

The loop conditions must have the form `< ...`. The annotated statement must be
the outer `for` loop, and the outer loop body must contain exactly the inner
`for` loop.

## Workflow

1. Write the staged function with a doubly nested `dyn_var` loop.
2. Call `builder::annotate(CUDA_KERNEL)` immediately before the outer loop.
3. Extract the function with `builder_context::extract_function_ast`.
4. Call `block::extract_cuda_from` on the extracted function body.
5. Emit the returned declarations before emitting the transformed host function.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=ef03e0bb125281ab152343ca32633d83 }}

```cpp
#include "blocks/c_code_generator.h"
#include "blocks/extract_cuda.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::annotate;
using builder::builder_context;
using builder::dyn_var;

static void zero_buffer(dyn_var<int*> buffer) {
    annotate(CUDA_KERNEL);
    for (dyn_var<int> cta = 0; cta < 128; cta = cta + 1) {
        for (dyn_var<int> tid = 0; tid < 512; tid = tid + 1) {
            dyn_var<int> index = cta * 512 + tid;
            buffer[index] = 0;
        }
    }
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(zero_buffer, "zero_buffer");

    auto function = block::to<block::func_decl>(ast);
    auto kernels = block::extract_cuda_from(function->body);

    for (auto kernel : kernels) {
        block::c_code_generator::generate_code(kernel, std::cout, 0);
    }
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## Online Tool Support

The TryIt link can be used to inspect the generated code. CUDA extraction is a
source-to-source workflow: it generates CUDA declarations and host launches, but
compiling or running the resulting CUDA program requires a CUDA-capable toolchain
and runtime outside the online sandbox.

## See Also

- [`builder::annotate`](../02_builder/annotate.md)
- [`builder::builder_context`](../02_builder/builder-context.md)

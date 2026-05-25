---
title: builder::cast_to
kind: function template
namespace: builder
header: builder/operator_overload.h
keywords: builder::cast_to, cast_to, dyn_var, cast_expr, explicit cast, operator_overload
---

# builder::cast_to

`builder::cast_to<T>` builds an explicit cast expression and returns it as a
[`builder::dyn_var<T>`](dyn-var.md).

Use it when the generated code needs a cast whose target type cannot be inferred
from ordinary assignment or operator overloads.

## Synopsis

```cpp
#include "builder/operator_overload.h"

namespace builder {

template <typename T, typename T2>
dyn_var<T>& cast_to(const T2& expr);

}
```

## Behavior

`cast_to<T>(expr)` converts `expr` to a BuildIt expression, wraps it in a
`block::cast_expr`, sets the target type to `T`, and returns a `dyn_var<T>` that
refers to the cast expression.

The returned `dyn_var<T>` is an expression value. It is allocated in the current
BuildIt invocation arena, like other temporary expression results produced by
operator overloads.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=c332efc1bde5dbaef6c2bca42423e70c }}

```cpp
#include "blocks/c_code_generator.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::builder_context;
using builder::cast_to;
using builder::dyn_var;
using builder::with_name;

namespace runtime {
static dyn_var<void*(size_t)> malloc = with_name("malloc");
static dyn_var<void(void*)> free = with_name("free");
}

static void foo() {
    dyn_var<int*> value = cast_to<int*>(runtime::malloc(sizeof(int)));
    value[0] = 123;
    runtime::free(value);
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::dyn_var`](dyn-var.md)
- [Expression Types](../03_block/expression-types.md#blockcast-expr)

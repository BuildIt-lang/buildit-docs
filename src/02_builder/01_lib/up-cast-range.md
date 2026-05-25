---
title: builder::up_cast_range
kind: function template
namespace: builder
header: builder/lib/utils.h
keywords: builder::up_cast_range, up_cast_range, static_var, dyn_var, range, second stage, first stage
---

# builder::up_cast_range

`builder::up_cast_range` converts a bounded second-stage value into a
first-stage value by enumerating a known range.

Use it when a `dyn_var<T>` is known to hold one of a small set of values, and
the rest of the staged function should specialize on that value using
[`builder::static_var`](../static-var.md) control flow.

## Synopsis

```cpp
#include "builder/lib/utils.h"

namespace builder {

template <typename T>
static_var<T> up_cast_range(dyn_var<T>& v, T range);

}
```

## Behavior

`up_cast_range(v, range)` checks `v` against every value from `0` through
`range - 1` and returns the matching value as a `static_var<T>`.

Conceptually, it behaves like:

```cpp
static_var<T> s;
for (s = 0; s < range - 1; s++) {
    if (v == s) {
        return s;
    }
}
return s;
```

The returned value is first-stage, so conditions and loops depending on it are
evaluated during extraction. This can specialize generated code based on a
bounded second-stage value.

## Requirements

`range` should describe the complete set of values that `v` may take. If `v`
does not match any checked value, the function returns the final loop value.

Keep the range small. The conversion is implemented by generating comparisons
against the values in the range, so large ranges can create large generated
control-flow structures.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=061d309f1f58e0ba369df5693b35cc38 }}

```cpp
#include "blocks/c_code_generator.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include "builder/lib/utils.h"
#include "builder/static_var.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_var;
using builder::static_var;
using builder::up_cast_range;

static dyn_var<int> is_even(dyn_var<int> x) {
    static_var<int> static_x = up_cast_range(x, 16);
    return (static_x % 2) == 0;
}

int main() {
    builder_context context;
    context.run_rce = true;
    auto ast = context.extract_function_ast(is_even, "is_even");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::dyn_var`](../dyn-var.md)
- [`builder::static_var`](../static-var.md)

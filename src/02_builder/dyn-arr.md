---
title: builder::dyn_arr
kind: alias template
namespace: builder
header: builder/array.h
keywords: builder::dyn_arr, dyn_arr, builder::array, builder::dyn_var, set_size, operator[], alias template
---

# builder::dyn_arr

`builder::dyn_arr<T, N>` is a convenience alias for
`builder::array<builder::dyn_var<T>, N>`.

Use it when you want a first-stage array of staged variables or expressions. The
array length and index used with `operator[]` are first-stage values, but each
element is a [`builder::dyn_var`](dyn-var.md) and therefore represents a value in
the generated program.

## Synopsis

```cpp
#include "builder/array.h"

namespace builder {

template <typename T, size_t N = 0>
using dyn_arr = array<dyn_var<T>, N>;

}
```

## Behavior

`dyn_arr<T, N>` is useful when extraction needs a fixed or first-stage-known
number of staged values.

```cpp
builder::dyn_arr<int, 3> values;
values[0] = 1;
values[1] = values[0] + 2;
```

The indexing operation is first-stage. It selects which stored `dyn_var<T>`
wrapper object to use. It does not create a generated subscript expression.

For generated arrays indexed by staged values, use `dyn_var<T[]>` instead.

## Initialization

`dyn_arr<T, N>` can be default constructed when `N` is nonzero:

```cpp
builder::dyn_arr<int, 3> values;
```

It can also be initialized from staged expressions:

```cpp
builder::dyn_arr<int, 3> values = {1, x + 2, 0};
```

When the template size is omitted, the size is taken from the initializer list or
set with [`set_size`](array.md#set-size):

```cpp
builder::dyn_arr<int> values = {1, 2};

builder::dyn_arr<int> other;
other.set_size(2);
```

## Member Functions

`dyn_arr<T, N>` has the member functions of [`builder::array`](array.md):

- [`set_size`](array.md#set-size)
- [`operator[]`](array.md#operator)

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=8a70af2fba96df159c781683b1d1c2ef }}

```cpp
#include "builder/builder_context.h"
#include "blocks/c_code_generator.h"
#include "builder/array.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_arr;

static void foo() {
    dyn_arr<int, 3> values;
    values[0] = 1;
    values[1] = values[0] + 2;
    values[2] = values[1] + values[0];

    dyn_arr<int, 4> initialized = {0, values[0] + 4, 0, 0};

    dyn_arr<int> sized;
    sized.set_size(2);
    sized[0] = initialized[1];
    sized[1] = values[2];
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::array`](array.md)
- [`builder::dyn_var`](dyn-var.md)

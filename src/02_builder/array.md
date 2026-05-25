---
title: builder::array
kind: class template
namespace: builder
header: builder/array.h
keywords: builder::array, array, constructor, initializer_list, set_size, operator[], size, dyn_var, static_var
---

# builder::array

`builder::array<T, N>` is a first-stage array container for objects that contain
`dyn_var` or `static_var` members.

Use it instead of a normal first-stage C++ array when constructing each element
may create BuildIt state or emit second-stage code. `builder::array` constructs
the elements in a loop whose index is a [`builder::static_var`](static-var.md),
so each element initialization is differentiated during extraction.

Plain C++ arrays can fail for these cases because every constructor call can
appear to BuildIt as if it came from the same static program point. If the
constructor creates `dyn_var` objects or emits second-stage statements, BuildIt
needs the per-iteration static index to keep those generated objects distinct.

The array itself is still controlled by first-stage indices and first-stage size
information. The element type decides what the elements represent. For example,
`array<dyn_var<int>, N>` stores `N` staged integer variables, while
`array<MyStruct, N>` stores `N` first-stage wrapper objects that may contain
`dyn_var` or `static_var` members.

`builder::dyn_arr<T, N>` is the common alias for `array<dyn_var<T>, N>`.

## Synopsis

```cpp
#include "builder/array.h"

namespace builder {

template <typename T, size_t size = 0>
class array {
public:
    array();

    array(const std::initializer_list<typename initializer_selector<T>::type>& init);

    array(const array& other);

    template <typename T2, size_t N>
    array(const array<T2, N>& other);

    array& operator=(const array& other) = delete;

    void set_size(size_t new_size);

    T& operator[](size_t index);
    const T& operator[](size_t index) const;
};

template <typename T, size_t N = 0>
using arr = array<T, N>;

}
```

## Template Parameters

`T` is the element wrapper type stored in the first stage. It is commonly a type
that contains `dyn_var` or `static_var` members, or a `dyn_var<T>` through the
[`dyn_arr`](dyn-arr.md) alias.

`size` is the optional compile-time array size. When `size` is `0`, the array
size is taken from the initializer list or set explicitly with
[`set_size`](#set-size).

## Behavior

`array<T, N>` allocates first-stage storage for `T` elements while the staged
function is being extracted. It constructs and destroys the elements with loops
whose iterator is a `static_var<size_t>`.

That construction pattern is the reason this type exists: it gives BuildIt a
distinct first-stage index for each element, even when the element constructor
creates `dyn_var` members or emits second-stage code.

Indexing with `operator[]` uses a first-stage `size_t` index and returns a
reference to the stored element.

This is different from a generated C array. The `array` object does not itself
emit an array declaration in generated code. It is a first-stage container for
wrapper objects that may emit generated code when they are constructed,
assigned, or otherwise used.

## Initialization

An array with a nonzero template size is constructed with that size:

```cpp
builder::array<cell, 4> cells;
```

An array without a template size can be sized by an initializer list:

```cpp
builder::array<builder::dyn_var<int>> values = {1, 2, 3};
```

or by calling [`set_size`](#set-size) before the first use:

```cpp
builder::array<builder::dyn_var<int>> values;
values.set_size(3);
```

## Member Functions

### set_size

```cpp
void set_size(size_t new_size);
```

Sets the size of an array whose template size is `0`.

Call this before the first use of the array. It should only be called once.

### operator[]

```cpp
T& operator[](size_t index);
const T& operator[](size_t index) const;
```

Returns the first-stage element at `index`.

The index is a first-stage value. Use `dyn_var<T[]>` when the generated program
needs an array that can be indexed by a staged value.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=ff93322dc1479293a183c9f2d5386e74 }}

```cpp
#include "builder/builder_context.h"
#include "blocks/c_code_generator.h"
#include "builder/array.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::array;
using builder::builder_context;
using builder::dyn_var;

struct cell {
    dyn_var<int> value;

    cell() {
        value = 0;
    }
};

static void foo() {
    array<cell, 3> cells;

    cells[0].value = 1;
    cells[1].value = cells[0].value + 2;
    cells[2].value = cells[1].value + cells[0].value;
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::dyn_arr`](dyn-arr.md)
- [`builder::dyn_var`](dyn-var.md)
- [`builder::static_var`](static-var.md)

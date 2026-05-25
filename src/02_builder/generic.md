---
title: builder::generic
kind: class
namespace: builder
header: builder/generics.h
keywords: builder::generic, generic, builder::type, type, type_of, with_type, create_type, pointer_of, array_of, dereference_type, enclosed_type, operator==, operator!=
---

# builder::generic

`builder::generic` is a placeholder for a second-stage type that is not known
from the first-stage C++ type.

Use `builder::dyn_var<builder::generic>` when the second-stage type depends on
first-stage logic rather than on the static C++ type of the wrapper. The generic
placeholder can then be filled explicitly with
[`set_type`](dyn-var.md#set-type), or at construction time with the
[`with_type`](#with-type) constructor helper.

## Synopsis

```cpp
#include "builder/generics.h"

namespace builder {

class generic {
public:
    using dereference_type = generic;
};

class type {
public:
    block::type::Ptr enclosed_type;

    type(block::type::Ptr t);

    bool operator==(const type& other);
    bool operator!=(const type& other);
};

type type_of(const dyn_var_base& v);

struct with_type {
    with_type(const type& t);

    template <typename T>
    with_type(const type& t, const T& init);

    with_type(const dyn_var_base& v);
};

template <typename T>
type create_type();

type array_of(const type& t, int size = -1);
type remove_array(const type& t);
type remove_array(const type& t, int& size);
bool is_array(const type& t);

type pointer_of(const type& t);
bool is_pointer(const type& t);
type remove_pointer(const type& t);

}
```

## Behavior

`dyn_var<generic>` separates the first-stage wrapper type from the second-stage
generated type. The first-stage C++ type is always `dyn_var<generic>`, but the
generated type stored inside it can be selected by first-stage logic.

This is useful when a helper needs to create or return a staged value whose
generated type is chosen dynamically during extraction.

A generic `dyn_var` must be assigned a concrete BuildIt type before it is used
as a standalone variable. You can do that with [`set_type`](dyn-var.md#set-type)
or the [`with_type`](#with-type) constructor helper. `with_type` can also copy
the type from an existing `dyn_var`.

Arithmetic, comparison, logical, bitwise, address-of, dereference, and subscript
operations are declared for `generic` so BuildIt can infer expression shapes
while the generated type is supplied separately.

## Type Helpers

### type

```cpp
class type;
```

Opaque wrapper around `block::type::Ptr`.

`type` values can be compared with `operator==` and `operator!=`. This is useful
when a generic helper needs to check that two inputs have compatible generated
types.

### type_of

```cpp
type type_of(const dyn_var_base& v);
```

Returns the generated type currently associated with a `dyn_var`.

### with_type

```cpp
with_type(const type& t);

template <typename T>
with_type(const type& t, const T& init);

with_type(const dyn_var_base& v);
```

Constructor helper for `dyn_var<generic>`.

The first form creates a generic variable with a specific generated type. The
second form also initializes it from an expression. The third form copies both
the generated type and expression from an existing `dyn_var`.

```cpp
builder::dyn_var<builder::generic> x =
    builder::with_type(builder::create_type<int>());

builder::dyn_var<builder::generic> y = builder::with_type(existing_dyn_var);
```

### create_type

```cpp
template <typename T>
type create_type();
```

Creates a BuildIt type object for the C++ type `T`.

## Pointer And Array Helpers

These helpers derive related BuildIt types:

```cpp
type pointer_of(const type& t);
bool is_pointer(const type& t);
type remove_pointer(const type& t);

type array_of(const type& t, int size = -1);
bool is_array(const type& t);
type remove_array(const type& t);
type remove_array(const type& t, int& size);
```

Use them when a generic helper needs to construct a pointer or array type from a
runtime-known generated type.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=239329c9b4ef4129fd265882e6710f8b }}

```cpp
#include "builder/builder_context.h"
#include "blocks/c_code_generator.h"
#include "builder/dyn_var.h"
#include "builder/generics.h"
#include <cassert>
#include <iostream>

using builder::builder_context;
using builder::dyn_var;
using builder::generic;
using builder::pointer_of;
using builder::type_of;
using builder::with_type;

static dyn_var<generic> get_max(
    dyn_var<generic> x,
    dyn_var<generic> y) {
    assert(type_of(x) == type_of(y));

    dyn_var<generic> result = with_type(type_of(x));
    if (x < y) {
        result = y;
    } else {
        result = x;
    }
    return result;
}

static void foo() {
    dyn_var<int> a = 4;
    dyn_var<int> b = 9;

    dyn_var<int> maximum = get_max(
        with_type(a),
        with_type(b));

    dyn_var<generic> pointer = with_type(pointer_of(type_of(maximum)), &maximum);
    *pointer = 0;
}

int main() {
    builder_context context;
    context.run_rce = true;
    auto ast = context.extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::dyn_var`](dyn-var.md)
- [`builder::custom_type`](custom-type.md)

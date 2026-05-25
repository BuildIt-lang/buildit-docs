---
title: builder::custom_type
kind: class template
namespace: builder
header: builder/dyn_var.h
keywords: builder::custom_type, custom_type, get_template_arg_types, type_name, dyn_var, with_name, dereference_type, subscript, operator*, operator[]
---

# builder::custom_type

`builder::custom_type<Args...>` is a base template for describing generated
types that are used through [`builder::dyn_var`](dyn-var.md).

Use it when a staged value has a generated template type. The wrapper type
describes the generated members that can be used from staged code, and
`custom_type<Args...>` describes the template argument types that should appear
in the generated declaration.

For generated types without template arguments, the wrapper struct does not need
to inherit from `custom_type<>`.

## Synopsis

```cpp
#include "builder/dyn_var.h"

namespace builder {

template <typename... Args>
struct custom_type {
    static std::vector<block::type::Ptr> get_template_arg_types();
};

}
```

## Defining A Custom Type

Define a normal first-stage C++ struct. The struct is not the generated type
itself; it is the first-stage description BuildIt uses when a `dyn_var` is
instantiated with that type.

For generated types without template arguments, no base class is required:

```cpp
struct point {
    builder::dyn_var<int> x;
    builder::dyn_var<int> y;
};
```

BuildIt can generate a type name automatically. If you need the generated code
to use a specific type spelling, provide a `type_name` member:

```cpp
struct point {
    static constexpr const char* type_name = "point";
};
```

For generated template types, pass the generated template arguments to
`custom_type`:

```cpp
template <typename T>
struct vector : builder::custom_type<T> {
    static constexpr const char* type_name = "std::vector";
};
```

When BuildIt prints a type such as `builder::dyn_var<vector<int>>`, the
`custom_type<T>` base lets it emit `std::vector<int>`.

## Members

Generated data members and member functions are represented as `dyn_var` fields.
If the field is default constructed, BuildIt gives the generated member an
automatic name. Use [`builder::with_name`](dyn-var.md#with-name) when the member
should have a specific generated name.

```cpp
struct point {
    static constexpr const char* type_name = "point";

    builder::dyn_var<int> x = builder::with_name("x");
    builder::dyn_var<int> y;
};
```

For member functions, use a function type:

```cpp
template <typename T>
struct vector : builder::custom_type<T> {
    static constexpr const char* type_name = "std::vector";

    builder::dyn_var<void(T)> push_back = builder::with_name("push_back");
};
```

## Dereference And Subscript Support

Pointer-like or container-like custom types can define `dereference_type` to
tell BuildIt what type should be returned by generated dereference or subscript
operations.

```cpp
template <typename T>
struct vector : builder::custom_type<T> {
    static constexpr const char* type_name = "std::vector";
    using dereference_type = T;
};
```

This allows expressions such as `vec[i]` to produce a `dyn_var<T>`.

## Member Functions

### get_template_arg_types

```cpp
static std::vector<block::type::Ptr> get_template_arg_types();
```

Returns the BuildIt type objects for the template arguments passed to
`custom_type<Args...>`.

This function is used by BuildIt's type extraction machinery. User code usually
does not call it directly.

## Notes

The template arguments passed to `custom_type<Args...>` do not have to be the
same as the C++ template parameters of the wrapper type, but they are typically
used that way.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=cd03e9611b14924136b8505cd79de6d1 }}

```cpp
#include "builder/builder_context.h"
#include "blocks/c_code_generator.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::builder_context;
using builder::custom_type;
using builder::dyn_var;
using builder::with_name;

// Custom type declaration with a template type.
template <typename T>
struct my_vector : custom_type<T> {
    static constexpr const char* type_name = "std::vector";
    dyn_var<void(T)> push_back = with_name("push_back");
};

static void foo() {
    dyn_var<my_vector<int>> vec;
    vec.push_back(42);

    dyn_var<my_vector<my_vector<int>>> vec2;
    vec2.push_back(vec);
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
- [`builder::static_var`](static-var.md)

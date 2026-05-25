---
title: builder::external_type_namer
kind: customization point
namespace: builder
header: builder/block_type_extractor.h
keywords: builder::external_type_namer, external_type_namer, type_name, get_template_arg_types, incomplete type, external type, dyn_var
---

# builder::external_type_namer

`builder::external_type_namer<T>` is a customization point for giving BuildIt
type information about a generated type without modifying or completing `T`.

Use it for incomplete types, external library types, or types whose generated
name should be described outside the type definition. This is useful when a
`dyn_var<T>` must refer to a generated type, but the first-stage C++ type cannot
or should not define `type_name` directly.

## Synopsis

```cpp
#include "builder/block_type_extractor.h"

namespace builder {

template <typename T>
struct external_type_namer;

}
```

Specialize `external_type_namer<T>` in namespace `builder`:

```cpp
struct external_node;

namespace builder {
template <>
struct external_type_namer<external_node> {
    static constexpr const char* type_name = "struct external_node";
};
}
```

## Behavior

When BuildIt extracts the type for `T`, it first checks whether
`external_type_namer<T>` provides a `type_name`. If it does, that name is used
for the generated type.

This avoids forcing the C++ type to be complete or forcing the type itself to
carry BuildIt-specific declarations.

If both `external_type_namer<T>::type_name` and `T::type_name` exist, the
external type namer takes precedence.

## Template Arguments

`external_type_namer<T>` can also provide generated template arguments by
defining `get_template_arg_types`:

```cpp
namespace builder {
template <>
struct external_type_namer<external_vector> {
    static constexpr const char* type_name = "external_vector";

    static std::vector<block::type::Ptr> get_template_arg_types() {
        return {builder::type_extractor<int>::extract_type()};
    }
};
}
```

Most user-defined template wrappers should use
[`builder::custom_type`](custom-type.md) instead. Use `external_type_namer` when
the type information must be supplied externally.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=94d7dacf4ded041b0e2de2a2fff7bb05 }}

```cpp
#include "blocks/c_code_generator.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_var;
using builder::with_name;

struct external_node;

namespace builder {
template <>
struct external_type_namer<external_node> {
    static constexpr const char* type_name = "struct external_node";
};
}

struct list_node {
    static constexpr const char* type_name = "list_node";

    dyn_var<list_node*> next = with_name("next");
    dyn_var<external_node*> external = with_name("external");
};

static void foo() {
    dyn_var<list_node*> node;
    node->next->next = 0;
    node->external = 0;
}

int main() {
    block::c_code_generator::generate_struct_decl<dyn_var<list_node>>(std::cout);

    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::custom_type`](custom-type.md)
- [`builder::dyn_var`](dyn-var.md)

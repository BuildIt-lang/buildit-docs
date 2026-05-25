---
title: block::c_code_generator
kind: class
namespace: block
header: blocks/c_code_generator.h
keywords: block::c_code_generator, c_code_generator, generate_code, generate_code_d2x, generate_struct_decl, oss, curr_indent, decl_only, use_d2x
---

# block::c_code_generator

`block::c_code_generator` emits C-like source code from BuildIt IR nodes.

It is implemented as a [`block::block_visitor`](block-visitor.md), but most user
code should use the static helper functions instead of constructing the visitor
directly.

## Synopsis

```cpp
#include "blocks/c_code_generator.h"

namespace block {

class c_code_generator : public block_visitor {
public:
    c_code_generator(std::ostream& out);

    std::ostream& oss;
    int curr_indent = 0;
    bool decl_only = false;
    bool use_d2x = false;

    static void generate_code(
        block::Ptr ast,
        std::ostream& out,
        int indent = 0,
        bool decl_only = false);

    static void generate_code_d2x(
        block::Ptr ast,
        std::ostream& out,
        int indent = 0,
        bool decl_only = false);

    template <typename T>
    static void generate_struct_decl(std::ostream& out, int indent = 0);
};

}
```

## generate_code

```cpp
static void generate_code(
    block::Ptr ast,
    std::ostream& out,
    int indent = 0,
    bool decl_only = false);
```

Emits code for `ast` to `out`.

`indent` sets the initial indentation level. `decl_only` emits declarations
without full definitions for nodes that support declaration-only output.

This is the normal entry point for printing generated functions, statements,
expressions, types, and declarations.

## generate_code_d2x

```cpp
static void generate_code_d2x(
    block::Ptr ast,
    std::ostream& out,
    int indent = 0,
    bool decl_only = false);
```

Emits code using D2X source-location support.

This requires BuildIt to be compiled with `ENABLE_D2X`. Without that build
option, this function asserts.

## generate_struct_decl

```cpp
template <typename T>
static void generate_struct_decl(std::ostream& out, int indent = 0);
```

Generates a struct declaration for a user-defined `dyn_var` type.

`T` must be a `builder::dyn_var<...>` type. The generated type must be a named
type without template arguments. BuildIt constructs a temporary `T`, records its
user-defined members, and emits a `struct` declaration from those members.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=8fd63e027837dd020371ccf4ca39d7f7 }}

```cpp
#include "blocks/c_code_generator.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_var;
using builder::with_name;

struct point {
    dyn_var<int> x = with_name("x");
    dyn_var<int> y;
};

dyn_var<int> sum_point(dyn_var<point> p) {
    return p.x + p.y;
}

int main() {
    builder_context context;

    block::c_code_generator::generate_struct_decl<dyn_var<point>>(std::cout);

    auto ast = context.extract_function_ast(sum_point, "sum_point");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`block::block_visitor`](block-visitor.md)
- [`block::block`](block.md)
- [`builder::builder_context`](../02_builder/builder-context.md)

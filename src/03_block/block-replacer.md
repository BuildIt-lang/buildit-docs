---
title: block::block_replacer
kind: class
namespace: block
header: blocks/block_replacer.h
keywords: block::block_replacer, block_replacer, node, to_replace, replace_with, rewrite, unary_helper, binary_helper, visit
---

# block::block_replacer

`block::block_replacer` is a rewriting visitor for BuildIt IR trees.

It derives from [`block::block_visitor`](block-visitor.md), recursively visits
children, rewrites child pointers in place, and stores the rewritten current node
in its public `node` field.

Use it when a pass needs to replace nodes while walking the tree.

## Synopsis

```cpp
#include "blocks/block_replacer.h"

namespace block {

class block_replacer : public block_visitor {
public:
    using block_visitor::visit;

    std::shared_ptr<block> node;

    std::shared_ptr<block> to_replace;
    std::shared_ptr<block> replace_with;

    template <typename T>
    std::shared_ptr<T> rewrite(std::shared_ptr<T> ptr);

    void unary_helper(std::shared_ptr<unary_expr> expr);
    void binary_helper(std::shared_ptr<binary_expr> expr);

    // visit overloads for expression, statement, variable, and type nodes
};

}
```

## Behavior

`block_replacer` is similar to `block_visitor`, but its default traversal rewrites
each child field with the result of visiting that child.

The result of visiting a node is stored in `node`. If an override wants to
replace the current node, it should assign the replacement to `node`.

```cpp
void visit(block::int_const::Ptr expr) override {
    node = replacement_expr;
}
```

If an override wants to keep the current node but continue rewriting its
children, call the base implementation:

```cpp
void visit(block::plus_expr::Ptr expr) override {
    block::block_replacer::visit(expr);
}
```

## rewrite

```cpp
template <typename T>
std::shared_ptr<T> rewrite(std::shared_ptr<T> ptr);
```

Visits `ptr`, returns the rewritten node cast back to `T`, and restores the
replacer's previous `node` state.

Derived visitors usually call `rewrite` when manually rewriting child fields.
The default `block_replacer` visit overloads already call it for the standard IR
children.

## Exact Node Replacement

`block_replacer` also has a simple exact-node replacement mode:

```cpp
std::shared_ptr<block> to_replace;
std::shared_ptr<block> replace_with;
```

When `to_replace` is set, `rewrite` replaces that exact node pointer with
`replace_with`.

This is useful when another pass has already found a specific node and prepared
a replacement subtree.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=ab546a943bdb0514595e703b622abbec }}

```cpp
#include "blocks/block_replacer.h"
#include "blocks/c_code_generator.h"
#include "blocks/expr.h"
#include "blocks/stmt.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>
#include <memory>

using builder::builder_context;
using builder::dyn_var;

class zero_to_one : public block::block_replacer {
public:
    using block_replacer::visit;

    void visit(block::int_const::Ptr expr) override {
        if (expr->value == 0) {
            auto replacement = std::make_shared<block::int_const>();
            replacement->value = 1;
            replacement->is_64bit = expr->is_64bit;
            node = replacement;
            return;
        }

        node = expr;
    }
};

static dyn_var<int> foo() {
    dyn_var<int> x = 0;
    return x + 0;
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");

    zero_to_one replacer;
    ast = replacer.rewrite(ast);

    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`block::block_visitor`](block-visitor.md)
- [`block::block`](block.md)
- [Expression Types](expression-types.md)
- [Statement Types](statement-types.md)

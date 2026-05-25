---
title: block::block_visitor
kind: class
namespace: block
header: blocks/block_visitor.h
keywords: block::block_visitor, block_visitor, visit, accept, block, expr, unary_expr, binary_expr, var_expr, const_expr, stmt, expr_stmt, stmt_block, decl_stmt, if_stmt, while_stmt, for_stmt, func_decl, var, type
---

# block::block_visitor

`block::block_visitor` is the base visitor class for walking BuildIt IR trees.

Each IR node calls the matching `visit` overload from its `accept` method. The
default visitor implementation recursively visits the children of most concrete
nodes, so a derived visitor can override only the node types it cares about and
delegate back to `block_visitor` to continue traversal.

## Synopsis

```cpp
#include "blocks/block_visitor.h"

namespace block {

class block_visitor {
public:
    virtual void visit(std::shared_ptr<block>);

    virtual void visit(std::shared_ptr<expr>);
    virtual void visit(std::shared_ptr<unary_expr>);
    virtual void visit(std::shared_ptr<binary_expr>);
    virtual void visit(std::shared_ptr<var_expr>);
    virtual void visit(std::shared_ptr<const_expr>);

    virtual void visit(std::shared_ptr<stmt>);
    virtual void visit(std::shared_ptr<expr_stmt>);
    virtual void visit(std::shared_ptr<stmt_block>);
    virtual void visit(std::shared_ptr<decl_stmt>);
    virtual void visit(std::shared_ptr<if_stmt>);
    virtual void visit(std::shared_ptr<while_stmt>);
    virtual void visit(std::shared_ptr<for_stmt>);
    virtual void visit(std::shared_ptr<func_decl>);

    virtual void visit(std::shared_ptr<var>);
    virtual void visit(std::shared_ptr<type>);
};

}
```

The actual class provides overloads for every expression, statement, variable,
and type node.

## Writing A Visitor

Derived visitors should usually include:

```cpp
using block_visitor::visit;
```

This keeps the base overload set visible when the derived class overrides one or
more `visit` functions.

When an override should continue traversing children, call the base
implementation:

```cpp
void visit(block::for_stmt::Ptr stmt) override {
    // Handle this for_stmt.
    block::block_visitor::visit(stmt);
}
```

If the override should stop traversal under that node, do not call the base
implementation.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=dc1e9d69537741b06cf33365c9115c40 }}

```cpp
#include "blocks/block_visitor.h"
#include "blocks/c_code_generator.h"
#include "blocks/expr.h"
#include "blocks/stmt.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_var;

class node_counter : public block::block_visitor {
public:
    using block_visitor::visit;

    int for_count = 0;
    int var_ref_count = 0;

    void visit(block::for_stmt::Ptr stmt) override {
        for_count++;
        block::block_visitor::visit(stmt);
    }

    void visit(block::var_expr::Ptr expr) override {
        var_ref_count++;
        block::block_visitor::visit(expr);
    }
};

static dyn_var<int> sum_to(dyn_var<int> n) {
    dyn_var<int> sum = 0;
    for (dyn_var<int> i = 0; i < n; i = i + 1) {
        sum += i;
    }
    return sum;
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(sum_to, "sum_to");

    node_counter counter;
    ast->accept(&counter);

    std::cout << "for statements: " << counter.for_count << std::endl;
    std::cout << "variable references: " << counter.var_ref_count << std::endl;

    return 0;
}
```

## See Also

- [`block::block`](block.md)
- [`block::block_replacer`](block-replacer.md)
- [Expression Types](expression-types.md)
- [Statement Types](statement-types.md)
- [Type Types](type-types.md)

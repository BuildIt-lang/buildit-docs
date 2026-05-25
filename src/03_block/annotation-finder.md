---
title: block::annotation_finder
kind: class
namespace: block
header: blocks/annotation_finder.h
keywords: block::annotation_finder, annotation_finder, annotation_to_find, found_stmt, find_annotation, block_visitor, annotate
---

# block::annotation_finder

`block::annotation_finder` finds the first statement annotated with a requested
label.

It is a [`block::block_visitor`](block-visitor.md) specialized for searching
statement annotations created by [`builder::annotate`](../02_builder/annotate.md).

## Synopsis

```cpp
#include "blocks/annotation_finder.h"

namespace block {

class annotation_finder : public block_visitor {
public:
    using block_visitor::visit;

    std::string annotation_to_find;
    stmt::Ptr found_stmt = nullptr;

    static stmt::Ptr find_annotation(block::Ptr ast, std::string label);
};

}
```

## Behavior

`find_annotation(ast, label)` walks `ast` and returns the first statement whose
`annotation` set contains `label`.

If no matching statement is found, it returns `nullptr`.

The finder checks annotations on expression statements, declaration statements,
`if` statements, `while` statements, and `for` statements. For compound
statements, it descends into the children when the compound statement itself
does not match.

## Manual Use

The static helper is the usual API:

```cpp
block::stmt::Ptr stmt =
    block::annotation_finder::find_annotation(ast, "label");
```

You can also instantiate the visitor directly when you want to inspect or reuse
its state:

```cpp
block::annotation_finder finder;
finder.annotation_to_find = "label";
ast->accept(&finder);
```

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=e81038e095e92df85ceb0f0478f2ef1d }}

```cpp
#include "blocks/annotation_finder.h"
#include "blocks/c_code_generator.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::annotate;
using builder::builder_context;
using builder::dyn_var;

static void foo() {
    dyn_var<int> sum = 0;

    annotate("hot-loop");
    for (dyn_var<int> i = 0; i < 8; i = i + 1) {
        sum += i;
    }
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");

    block::stmt::Ptr loop = block::annotation_finder::find_annotation(ast, "hot-loop");
    if (loop != nullptr) {
        block::c_code_generator::generate_code(loop, std::cout, 0);
    }

    return 0;
}
```

## See Also

- [`builder::annotate`](../02_builder/annotate.md)
- [`block::block_visitor`](block-visitor.md)
- [Statement Types](statement-types.md)

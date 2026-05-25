---
title: block::eliminate_redundant_vars
kind: utility pass
namespace: block
header: blocks/rce.h
keywords: Redundant Copy Elimination, RCE, block::eliminate_redundant_vars, eliminate_redundant_vars, run_rce, redundant copy, cleanup pass
---

# block::eliminate_redundant_vars

Redundant Copy Elimination, usually abbreviated RCE, is a BuildIt IR cleanup
pass that removes unnecessary temporary variables and redundant copies from a
generated AST.

Use it to simplify generated code after extraction and structural recovery
passes have run.

## Synopsis

```cpp
#include "blocks/rce.h"

namespace block {

void eliminate_redundant_vars(block::Ptr ast);

}
```

## Behavior

`eliminate_redundant_vars(ast)` mutates `ast` in place.

At a surface level, the pass looks for generated variables that only forward or
copy another expression and rewrites the IR so those extra variables can be
removed. This usually makes generated code shorter and easier to read.

The pass is conservative around variables whose addresses are taken.

## Enabling From builder_context

Most users should enable RCE through
[`builder::builder_context`](../02_builder/builder-context.md):

```cpp
builder::builder_context context;
context.run_rce = true;
auto ast = context.extract_function_ast(foo, "foo");
```

When `run_rce` is `true`, BuildIt runs redundant copy elimination as part of the
post-processing pipeline after extraction.

## Manual Use

You can also run the pass manually on an already extracted AST:

```cpp
auto ast = context.extract_function_ast(foo, "foo");
block::eliminate_redundant_vars(ast);
```

## See Also

- [`builder::builder_context`](../02_builder/builder-context.md)
- [`block::block`](block.md)

---
title: block::matcher::replace_match
kind: function
namespace: block::matcher
header: blocks/matchers/replacers.h
keywords: block::matcher::replace_match, replace_match, block::matcher::match, match, captures, replacement, pattern, replacer, find_all_matches
---

# block::matcher::replace_match

`block::matcher::replace_match` replaces a matched BuildIt subtree using a
[`block::matcher::pattern`](patterns.md) as the replacement template.

Replacers use the same pattern objects as matchers. In a matcher, a pattern is a
predicate over an existing AST node. In a replacer, a pattern is a template used
to construct a new AST subtree from concrete pattern nodes and captures from a
previous match.

Only expression-tree replacement is supported for now.

## Synopsis

```cpp
#include "blocks/matchers/patterns.h"
#include "blocks/matchers/matchers.h"
#include "blocks/matchers/replacers.h"

namespace block::matcher {

void replace_match(block::Ptr ast, match m, pattern::Ptr replacement);

}
```

## Behavior

```cpp
void replace_match(block::Ptr ast, match m, pattern::Ptr replacement);
```

Builds a replacement expression subtree from `replacement` and replaces
`m.node` inside `ast`.

The replacement pattern can refer to captures from the match:

```cpp
auto zero_add = expr("value") + int_const(0);
auto matches = find_all_matches(zero_add, ast);

for (auto& m : matches) {
    replace_match(ast, m, expr("value"));
}
```

This rewrites `value + 0` to `value`.

Replacement patterns can also build new expression nodes:

```cpp
replace_match(ast, m, mul_expr(expr("value"), int_const(2)));
```

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=782883c4a2a4da15b117b0696c314c2d }}

```cpp
#include "blocks/c_code_generator.h"
#include "blocks/matchers/matchers.h"
#include "blocks/matchers/patterns.h"
#include "blocks/matchers/replacers.h"
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_var;
using namespace block::matcher;

static void foo() {
    dyn_var<int> x = 0;
    x = x + 0;

    dyn_var<int> y = 0;
    y = x + 1;
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");

    auto add_zero = expr("value") + int_const(0);
    auto matches = find_all_matches(add_zero, ast);

    for (auto& m : matches) {
        replace_match(ast, m, expr("value"));
    }

    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`block::matcher::pattern`](patterns.md)
- [`block::matcher::find_all_matches`](find-all-matches.md)
- [`block::block_replacer`](../block-replacer.md)
- [`block::c_code_generator`](../c-code-generator.md)

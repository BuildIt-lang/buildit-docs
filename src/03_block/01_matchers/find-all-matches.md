---
title: block::matcher::find_all_matches
kind: function
namespace: block::matcher
header: blocks/matchers/matchers.h
keywords: block::matcher::find_all_matches, find_all_matches, block::matcher::check_match, check_match, block::matcher::match, match, captures, node, pattern, matcher
---

# block::matcher::find_all_matches

`block::matcher::find_all_matches` searches a BuildIt AST for expression
subtrees that match a [`block::matcher::pattern`](patterns.md).

Only expression-tree matching is supported for now. You can pass a full AST to
`find_all_matches`, and it will walk into the expressions contained in that AST,
but patterns for statement trees and type trees should not be treated as a
supported API yet.

## Synopsis

```cpp
#include "blocks/matchers/patterns.h"
#include "blocks/matchers/matchers.h"

namespace block::matcher {

struct match {
    block::Ptr node;
    std::map<std::string, block::Ptr> captures;
};

std::vector<match> find_all_matches(pattern::Ptr p, block::Ptr node);

bool check_match(
    pattern::Ptr p,
    block::Ptr node,
    std::map<std::string, block::Ptr>& captures);

}
```

## Matching

Matching treats a pattern as a predicate over BuildIt nodes. If the node has the
right kind, its children match the child patterns, and any repeated captures are
consistent, the match succeeds.

Passing a non-empty `name` to a pattern constructor captures the matched node.
Reusing the same capture name in one pattern requires all occurrences to match
the same IR subtree.

```cpp
auto increment = assign_expr(var("x"), plus_expr(var("x"), int_const(1)));
```

This matches assignments of the form `x = x + 1`, captures the variable as
`"x"`, and rejects assignments where the left side and the expression operand
refer to different variables.

## find_all_matches

```cpp
std::vector<match> find_all_matches(pattern::Ptr p, block::Ptr node);
```

Walks `node` and returns every expression subtree matching `p`.

Each result stores:

- `node`: the subtree that matched the whole pattern
- `captures`: nodes captured by named pattern constructors

## check_match

```cpp
bool check_match(
    pattern::Ptr p,
    block::Ptr node,
    std::map<std::string, block::Ptr>& captures);
```

Checks whether one node matches one pattern. The caller provides the capture
map, which is filled as the match succeeds.

Use `check_match` when another pass has already selected a candidate node. Use
`find_all_matches` when the matcher should search the full tree.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=c5d8ad2e8cfac8ddca0246a56517643a }}

```cpp
#include "blocks/matchers/matchers.h"
#include "blocks/matchers/patterns.h"
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

    std::cout << matches.size() << std::endl;

    return 0;
}
```

## See Also

- [`block::matcher::pattern`](patterns.md)
- [`block::matcher::replace_match`](replace-match.md)
- [Expression Types](../expression-types.md)

---
title: block::var
kind: class
namespace: block
header: blocks/var.h
keywords: block::var, var, block::var_expr, block::decl_stmt
---

# block::var

`block::var` represents a variable or named value in the BuildIt IR.

Expressions refer to variables through [`block::var_expr`](expression-types.md#blockvar-expr),
and declarations introduce variables through
[`block::decl_stmt`](statement-types.md#blockdecl-stmt).

## Synopsis

```cpp
#include "blocks/var.h"

namespace block {

class var : public block {
public:
    using Ptr = std::shared_ptr<var>;

    std::string var_name;
    std::string preferred_name;
    type::Ptr var_type;
};

}
```

## Fields

### var_name

```cpp
std::string var_name;
```

Concrete generated name for the variable.

Some variables are created before a final generated name has been assigned.
Later naming passes may fill this field.

### preferred_name

```cpp
std::string preferred_name;
```

Preferred generated name.

This gives naming passes a requested name while still allowing them to avoid
collisions or apply their own naming rules.

### var_type

```cpp
type::Ptr var_type;
```

Type of the variable.

See [Type Types](type-types.md) for the `block::type` hierarchy.

## Notes

`block::var` nodes are often compared by identity or static tag rather than by
name. This matters because names may be assigned or changed after extraction.

When cloning IR nodes, `var_expr` nodes intentionally keep references to the
same `var` object instead of cloning the variable.

## See Also

- [Type Types](type-types.md)
- [Expression Types](expression-types.md)
- [Statement Types](statement-types.md)

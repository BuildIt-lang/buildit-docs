---
title: block::stmt
kind: reference
namespace: block
header: blocks/stmt.h
keywords: block::stmt, stmt, block::expr_stmt, expr_stmt, block::stmt_block, stmt_block, block::decl_stmt, decl_stmt, block::if_stmt, if_stmt, block::case_stmt, case_stmt, block::switch_stmt, switch_stmt, block::label, label, block::label_stmt, label_stmt, block::goto_stmt, goto_stmt, block::while_stmt, while_stmt, block::for_stmt, for_stmt, block::break_stmt, break_stmt, block::continue_stmt, continue_stmt, block::func_decl, func_decl, block::struct_decl, struct_decl, block::return_stmt, return_stmt
---

# block::stmt

Statement nodes represent control flow, declarations, labels, function bodies,
and top-level declarations in the BuildIt IR.

This page documents the data fields that define each statement node. Visitor,
comparison, cloning, and debug-printing methods are omitted.

## block::stmt

Base class for all statement nodes.

```cpp
class stmt : public block {
public:
    using Ptr = std::shared_ptr<stmt>;

    std::set<std::string> annotation;
};
```

Fields:

- `annotation`: string annotations attached to the statement

Notes: `stmt` is an abstract IR category. It is used through derived statement
types and is not expected to be instantiated directly.

## block::expr_stmt

Statement that evaluates an expression.

```cpp
class expr_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<expr_stmt>;

    expr::Ptr expr1;
    bool mark_for_deletion = false;
};
```

Children:

- `expr1`: expression evaluated by the statement
- `mark_for_deletion`: internal marker for expression statements that should be removed by cleanup passes

## block::stmt_block

Block containing a sequence of statements.

```cpp
class stmt_block : public stmt {
public:
    using Ptr = std::shared_ptr<stmt_block>;

    std::vector<stmt::Ptr> stmts;
};
```

Children:

- `stmts`: ordered statements in the block

## block::decl_stmt

Declaration statement.

```cpp
class decl_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<decl_stmt>;

    var::Ptr decl_var;
    expr::Ptr init_expr = nullptr;
    bool is_typedef = false;
    bool is_extern = false;
    bool is_static = false;
};
```

Children:

- `decl_var`: variable being declared
- `init_expr`: optional initializer expression
- `is_typedef`: whether the declaration is a typedef
- `is_extern`: whether the declaration is extern
- `is_static`: whether the declaration is static

## block::if_stmt

Conditional statement.

```cpp
class if_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<if_stmt>;

    expr::Ptr cond;
    stmt::Ptr then_stmt;
    stmt::Ptr else_stmt;
};
```

Children:

- `cond`: condition expression
- `then_stmt`: statement executed when the condition is true
- `else_stmt`: statement executed when the condition is false

## block::case_stmt

Case entry inside a switch statement.

```cpp
class case_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<case_stmt>;

    bool is_default;
    int_const::Ptr case_value;
    stmt::Ptr branch;
};
```

Children:

- `is_default`: whether this is the default case
- `case_value`: integer case value; `nullptr` for default
- `branch`: statement for the case body; may be `nullptr` for an empty branch

## block::switch_stmt

Switch statement.

```cpp
class switch_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<switch_stmt>;

    expr::Ptr cond;
    std::vector<case_stmt::Ptr> cases;
};
```

Children:

- `cond`: switch condition expression
- `cases`: ordered case entries

## block::label

Label object referenced by label and goto statements.

```cpp
class label : public block {
public:
    using Ptr = std::shared_ptr<label>;

    std::string label_name;
};
```

Fields:

- `label_name`: emitted label name

## block::label_stmt

Statement that emits a label.

```cpp
class label_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<label_stmt>;

    label::Ptr label1;
};
```

Children:

- `label1`: label emitted by the statement

## block::goto_stmt

Goto statement.

```cpp
class goto_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<goto_stmt>;

    label::Ptr label1;
    tracer::tag temporary_label_number;
};
```

Children:

- `label1`: destination label; may be `nullptr` before labels are resolved
- `temporary_label_number`: temporary tag used before a concrete label is attached

## block::while_stmt

While loop statement.

```cpp
class while_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<while_stmt>;

    stmt::Ptr body;
    expr::Ptr cond;
    std::vector<stmt_block::Ptr> continue_blocks;
};
```

Children:

- `body`: loop body
- `cond`: loop condition expression
- `continue_blocks`: extra metadata used by passes that recover or transform continue behavior

## block::for_stmt

For loop statement.

```cpp
class for_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<for_stmt>;

    stmt::Ptr decl_stmt;
    expr::Ptr cond;
    expr::Ptr update;
    stmt::Ptr body;
};
```

Children:

- `decl_stmt`: initialization statement
- `cond`: loop condition expression
- `update`: loop update expression
- `body`: loop body

## block::break_stmt

Break statement.

```cpp
class break_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<break_stmt>;
};
```

Children: none.

## block::continue_stmt

Continue statement.

```cpp
class continue_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<continue_stmt>;
};
```

Children: none.

## block::func_decl

Function declaration or definition.

```cpp
class func_decl : public stmt {
public:
    using Ptr = std::shared_ptr<func_decl>;

    std::string func_name;
    type::Ptr return_type;
    std::vector<var::Ptr> args;
    stmt::Ptr body;

    bool is_decl_only = false;
    bool is_variadic = false;
    bool is_static = false;
    bool is_inline = false;
};
```

Children:

- `func_name`: generated function name
- `return_type`: function return type
- `args`: function arguments
- `body`: function body
- `is_decl_only`: whether this is only a declaration
- `is_variadic`: whether the function is variadic
- `is_static`: whether the function is static
- `is_inline`: whether the function is inline

## block::struct_decl

Struct or union declaration.

```cpp
class struct_decl : public stmt {
public:
    using Ptr = std::shared_ptr<struct_decl>;

    std::string struct_name;
    std::vector<decl_stmt::Ptr> members;
    bool is_union = false;
    bool is_decl_only = false;
};
```

Children:

- `struct_name`: generated struct or union name
- `members`: member declarations
- `is_union`: whether this declaration is a union
- `is_decl_only`: whether this is only a declaration

## block::return_stmt

Return statement.

```cpp
class return_stmt : public stmt {
public:
    using Ptr = std::shared_ptr<return_stmt>;

    expr::Ptr return_val;
};
```

Children:

- `return_val`: returned expression

## See Also

- [`block::block`](block.md)
- [Expression Types](expression-types.md)

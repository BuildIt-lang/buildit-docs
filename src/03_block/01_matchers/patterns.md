---
title: block::matcher::pattern
kind: class
namespace: block::matcher
header: blocks/matchers/patterns.h
keywords: block::matcher::pattern, pattern, expr, var, var_with_name, unary_expr, not_expr, unary_minus_expr, bitwise_not_expr, addr_of_expr, binary_expr, and_expr, or_expr, plus_expr, minus_expr, mul_expr, div_expr, lt_expr, gt_expr, lte_expr, gte_expr, equals_expr, ne_expr, mod_expr, bitwise_and_expr, bitwise_or_expr, bitwise_xor_expr, lshift_expr, rshift_expr, const_expr, int_const, double_const, float_const, string_const, string_const_with_val, assign_expr, sq_bkt_expr, function_call_expr, initializer_list_expr, foreign_expr_base, member_access_expr, var_expr
---

# block::matcher::pattern

`block::matcher::pattern` describes an arbitrary structural pattern over
BuildIt nodes.

Most users create patterns with the helper constructors in
`blocks/matchers/patterns.h`. The same pattern objects are used by both
[`find_all_matches`](find-all-matches.md) and
[`replace_match`](replace-match.md):

- In a matcher, a pattern is a predicate over an existing AST node.
- In a replacer, a pattern is a template used to construct a new AST subtree.

Only expression-tree matching and replacement is supported for now. The header
contains some statement and type pattern constructors, but those are not part of
the supported matcher/replacer API yet.

## Pattern Shape

A constructor without child patterns describes any node of that kind:

```cpp
expr("x")
```

When used for matching, this matches any expression and captures it as `"x"`.
When used for replacement, this refers to the previously captured node named
`"x"`.

A constructor with child patterns describes a node with a particular child
shape:

```cpp
expr("x") + int_const(0)
```

When used for matching, this matches an addition whose left side is any
expression captured as `"x"` and whose right side is the constant `0`. When used
for replacement, the same kind of pattern can construct a new expression tree
from captures and concrete nodes.

## Captures

Most constructors take an optional final `std::string name = ""` argument.
Passing a non-empty name captures the matched node when the pattern is used for
matching.

```cpp
auto p = plus_expr(expr("lhs"), int_const(0));
```

The matched left operand is available as `"lhs"` in `match::captures`.

When a pattern is used for replacement, a named pattern with no concrete value
or children refers to a capture from the match:

```cpp
replace_match(ast, m, expr("lhs"));
```

This replacement pattern reuses the captured expression named `"lhs"`.

Reusing the same capture name requires all occurrences to match the same IR
subtree:

```cpp
auto p = assign_expr(var("x"), plus_expr(var("x"), int_const(1)));
```

This matches `x = x + 1`, but not `x = y + 1`.

## General Expression Patterns

```cpp
pattern::Ptr expr(std::string name = "");

pattern::Ptr var(std::string name = "");

pattern::Ptr var_with_name(
    std::string var_name,
    std::string name = "");
```

`expr` matches any expression node.

`var` matches both `block::var` nodes and `block::var_expr` nodes. When `var`
matches a `var_expr`, the captured node is the underlying `block::var`.

`var_with_name` matches a variable whose generated `var_name` field has already
been assigned.

## Unary Expression Patterns

```cpp
pattern::Ptr unary_expr(std::string name = "");
pattern::Ptr unary_expr(pattern::Ptr x, std::string name = "");

pattern::Ptr not_expr(std::string name = "");
pattern::Ptr not_expr(pattern::Ptr x, std::string name = "");

pattern::Ptr unary_minus_expr(std::string name = "");
pattern::Ptr unary_minus_expr(pattern::Ptr x, std::string name = "");

pattern::Ptr bitwise_not_expr(std::string name = "");
pattern::Ptr bitwise_not_expr(pattern::Ptr x, std::string name = "");

pattern::Ptr addr_of_expr(std::string name = "");
pattern::Ptr addr_of_expr(pattern::Ptr x, std::string name = "");
```

The child pattern `x` matches the unary expression operand.

Operator aliases:

```cpp
pattern::Ptr operator!(pattern::Ptr x);
pattern::Ptr operator-(pattern::Ptr x);
pattern::Ptr operator~(pattern::Ptr x);
```

## Binary Expression Patterns

```cpp
pattern::Ptr binary_expr(std::string name = "");
pattern::Ptr binary_expr(
    pattern::Ptr x,
    pattern::Ptr y,
    std::string name = "");

pattern::Ptr and_expr(std::string name = "");
pattern::Ptr and_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr or_expr(std::string name = "");
pattern::Ptr or_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr plus_expr(std::string name = "");
pattern::Ptr plus_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr minus_expr(std::string name = "");
pattern::Ptr minus_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr mul_expr(std::string name = "");
pattern::Ptr mul_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr div_expr(std::string name = "");
pattern::Ptr div_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr lt_expr(std::string name = "");
pattern::Ptr lt_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr gt_expr(std::string name = "");
pattern::Ptr gt_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr lte_expr(std::string name = "");
pattern::Ptr lte_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr gte_expr(std::string name = "");
pattern::Ptr gte_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr equals_expr(std::string name = "");
pattern::Ptr equals_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr ne_expr(std::string name = "");
pattern::Ptr ne_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr mod_expr(std::string name = "");
pattern::Ptr mod_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr bitwise_and_expr(std::string name = "");
pattern::Ptr bitwise_and_expr(
    pattern::Ptr x,
    pattern::Ptr y,
    std::string name = "");

pattern::Ptr bitwise_or_expr(std::string name = "");
pattern::Ptr bitwise_or_expr(
    pattern::Ptr x,
    pattern::Ptr y,
    std::string name = "");

pattern::Ptr bitwise_xor_expr(std::string name = "");
pattern::Ptr bitwise_xor_expr(
    pattern::Ptr x,
    pattern::Ptr y,
    std::string name = "");

pattern::Ptr lshift_expr(std::string name = "");
pattern::Ptr lshift_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");

pattern::Ptr rshift_expr(std::string name = "");
pattern::Ptr rshift_expr(pattern::Ptr x, pattern::Ptr y, std::string name = "");
```

The child patterns `x` and `y` match the left and right operands.

Operator aliases:

```cpp
pattern::Ptr operator&&(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator||(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator+(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator-(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator*(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator/(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator<(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator>(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator<=(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator>=(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator==(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator!=(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator%(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator&(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator|(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator^(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator<<(pattern::Ptr x, pattern::Ptr y);
pattern::Ptr operator>>(pattern::Ptr x, pattern::Ptr y);
```

## Constant Patterns

```cpp
pattern::Ptr const_expr(std::string name = "");

pattern::Ptr int_const(std::string name = "");
pattern::Ptr int_const(const int val, std::string name = "");

pattern::Ptr double_const(std::string name = "");
pattern::Ptr double_const(const double val, std::string name = "");

pattern::Ptr float_const(std::string name = "");
pattern::Ptr float_const(const double val, std::string name = "");

pattern::Ptr string_const(std::string name = "");
pattern::Ptr string_const_with_val(std::string val, std::string name = "");
```

Constructors without a value match any constant of that kind. Constructors with
a value match only that value.

`string_const_with_val` is the value-matching constructor for string constants.
It has a distinct name so that the string value is not confused with the capture
name.

## Assignment and Access Patterns

```cpp
pattern::Ptr assign_expr(std::string name = "");
pattern::Ptr assign_expr(
    pattern::Ptr x,
    pattern::Ptr y,
    std::string name = "");

pattern::Ptr sq_bkt_expr(std::string name = "");
pattern::Ptr sq_bkt_expr(
    pattern::Ptr x,
    pattern::Ptr y,
    std::string name = "");

pattern::Ptr function_call_expr(std::string name = "");
pattern::Ptr function_call_expr(
    pattern::Ptr x,
    std::vector<pattern::Ptr> y,
    std::string name = "");

pattern::Ptr initializer_list_expr(std::string name = "");
pattern::Ptr foreign_expr_base(std::string name = "");
pattern::Ptr member_access_expr(std::string name = "");
pattern::Ptr var_expr(std::string name = "");
```

For `assign_expr(x, y, name)`, `x` matches the assignment target and `y` matches
the assigned expression.

For `sq_bkt_expr(x, y, name)`, `x` matches the indexed expression and `y`
matches the index expression.

For `function_call_expr(x, y, name)`, `x` matches the callee expression and `y`
matches the argument list.

## See Also

- [`block::matcher::find_all_matches`](find-all-matches.md)
- [`block::matcher::replace_match`](replace-match.md)
- [Expression Types](../expression-types.md)

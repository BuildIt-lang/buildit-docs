---
title: block::expr
kind: reference
namespace: block
header: blocks/expr.h
keywords: block::expr, expr, block::unary_expr, unary_expr, block::binary_expr, binary_expr, block::not_expr, not_expr, block::unary_minus_expr, unary_minus_expr, block::bitwise_not_expr, bitwise_not_expr, block::and_expr, and_expr, block::bitwise_and_expr, bitwise_and_expr, block::or_expr, or_expr, block::bitwise_or_expr, bitwise_or_expr, block::bitwise_xor_expr, bitwise_xor_expr, block::plus_expr, plus_expr, block::minus_expr, minus_expr, block::mul_expr, mul_expr, block::div_expr, div_expr, block::lt_expr, lt_expr, block::gt_expr, gt_expr, block::lte_expr, lte_expr, block::gte_expr, gte_expr, block::lshift_expr, lshift_expr, block::rshift_expr, rshift_expr, block::equals_expr, equals_expr, block::ne_expr, ne_expr, block::mod_expr, mod_expr, block::var_expr, var_expr, block::const_expr, const_expr, block::int_const, int_const, block::double_const, double_const, block::float_const, float_const, block::string_const, string_const, block::assign_expr, assign_expr, block::sq_bkt_expr, sq_bkt_expr, block::function_call_expr, function_call_expr, block::initializer_list_expr, initializer_list_expr, block::foreign_expr_base, foreign_expr_base, block::foreign_expr, foreign_expr, block::member_access_expr, member_access_expr, block::addr_of_expr, addr_of_expr, block::cast_expr, cast_expr
---

# block::expr

Expression nodes represent values and value-producing operations in the BuildIt
IR. All expression classes live in namespace `block` and derive from
`block::expr`.

This page documents the data fields that define each expression node. Visitor,
comparison, cloning, and debug-printing methods are omitted.

## block::expr

Base class for all expression nodes.

```cpp
class expr : public block {
public:
    using Ptr = std::shared_ptr<expr>;
};
```

Notes: `expr` is an abstract IR category. It is used through derived expression
types and is not expected to be instantiated directly.

## block::unary_expr

Base class for expressions with one child expression.

```cpp
class unary_expr : public expr {
public:
    using Ptr = std::shared_ptr<unary_expr>;

    expr::Ptr expr1;
};
```

Children:

- `expr1`: operand expression

Notes: `unary_expr` is an abstract IR category. Use one of its concrete derived
types.

## block::binary_expr

Base class for expressions with two child expressions.

```cpp
class binary_expr : public expr {
public:
    using Ptr = std::shared_ptr<binary_expr>;

    expr::Ptr expr1;
    expr::Ptr expr2;
};
```

Children:

- `expr1`: left operand
- `expr2`: right operand

Notes: `binary_expr` is an abstract IR category. Use one of its concrete derived
types.

## block::not_expr

Logical not expression.

```cpp
class not_expr : public unary_expr {
public:
    using Ptr = std::shared_ptr<not_expr>;
};
```

Children: inherited from [`unary_expr`](#blockunary-expr).

## block::unary_minus_expr

Unary minus expression.

```cpp
class unary_minus_expr : public unary_expr {
public:
    using Ptr = std::shared_ptr<unary_minus_expr>;
};
```

Children: inherited from [`unary_expr`](#blockunary-expr).

## block::bitwise_not_expr

Bitwise not expression.

```cpp
class bitwise_not_expr : public unary_expr {
public:
    using Ptr = std::shared_ptr<bitwise_not_expr>;
};
```

Children: inherited from [`unary_expr`](#blockunary-expr).

## block::and_expr

Logical and expression.

```cpp
class and_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<and_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::bitwise_and_expr

Bitwise and expression.

```cpp
class bitwise_and_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<bitwise_and_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::or_expr

Logical or expression.

```cpp
class or_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<or_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::bitwise_or_expr

Bitwise or expression.

```cpp
class bitwise_or_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<bitwise_or_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::bitwise_xor_expr

Bitwise xor expression.

```cpp
class bitwise_xor_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<bitwise_xor_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::plus_expr

Addition expression.

```cpp
class plus_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<plus_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::minus_expr

Subtraction expression.

```cpp
class minus_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<minus_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::mul_expr

Multiplication expression.

```cpp
class mul_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<mul_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::div_expr

Division expression.

```cpp
class div_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<div_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::lt_expr

Less-than comparison expression.

```cpp
class lt_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<lt_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::gt_expr

Greater-than comparison expression.

```cpp
class gt_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<gt_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::lte_expr

Less-than-or-equal comparison expression.

```cpp
class lte_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<lte_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::gte_expr

Greater-than-or-equal comparison expression.

```cpp
class gte_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<gte_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::lshift_expr

Left-shift expression.

```cpp
class lshift_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<lshift_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::rshift_expr

Right-shift expression.

```cpp
class rshift_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<rshift_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::equals_expr

Equality comparison expression.

```cpp
class equals_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<equals_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::ne_expr

Not-equal comparison expression.

```cpp
class ne_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<ne_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::mod_expr

Modulo expression.

```cpp
class mod_expr : public binary_expr {
public:
    using Ptr = std::shared_ptr<mod_expr>;
};
```

Children: inherited from [`binary_expr`](#blockbinary-expr).

## block::var_expr

Expression that refers to a variable or named value.

```cpp
class var_expr : public expr {
public:
    using Ptr = std::shared_ptr<var_expr>;

    var::Ptr var1;
    std::vector<block::Ptr> template_args;
};
```

Children:

- `var1`: referenced variable
- `template_args`: optional template argument nodes for templated names

## block::const_expr

Base class for constant expression nodes.

```cpp
class const_expr : public expr {
public:
    using Ptr = std::shared_ptr<const_expr>;
};
```

Notes: `const_expr` is an abstract IR category. Use one of its concrete derived
constant nodes.

## block::int_const

Integer constant expression.

```cpp
class int_const : public const_expr {
public:
    using Ptr = std::shared_ptr<int_const>;

    long long value;
    bool is_64bit;
};
```

Fields:

- `value`: integer value
- `is_64bit`: whether the constant should be treated as a 64-bit integer

## block::double_const

Double-precision floating-point constant expression.

```cpp
class double_const : public const_expr {
public:
    using Ptr = std::shared_ptr<double_const>;

    double value;
};
```

Fields:

- `value`: double value

## block::float_const

Single-precision floating-point constant expression.

```cpp
class float_const : public const_expr {
public:
    using Ptr = std::shared_ptr<float_const>;

    float value;
};
```

Fields:

- `value`: float value

## block::string_const

String literal constant expression.

```cpp
class string_const : public const_expr {
public:
    using Ptr = std::shared_ptr<string_const>;

    std::string value;
};
```

Fields:

- `value`: string literal value

## block::assign_expr

Assignment expression.

```cpp
class assign_expr : public expr {
public:
    using Ptr = std::shared_ptr<assign_expr>;

    expr::Ptr var1;
    expr::Ptr expr1;
};
```

Children:

- `var1`: left-hand side expression
- `expr1`: right-hand side expression

## block::sq_bkt_expr

Subscript expression.

```cpp
class sq_bkt_expr : public expr {
public:
    using Ptr = std::shared_ptr<sq_bkt_expr>;

    expr::Ptr var_expr;
    expr::Ptr index;
};
```

Children:

- `var_expr`: expression being indexed
- `index`: index expression

## block::function_call_expr

Function call expression.

```cpp
class function_call_expr : public expr {
public:
    using Ptr = std::shared_ptr<function_call_expr>;

    expr::Ptr expr1;
    std::vector<expr::Ptr> args;
};
```

Children:

- `expr1`: callee expression
- `args`: call argument expressions

## block::initializer_list_expr

Initializer-list expression.

```cpp
class initializer_list_expr : public expr {
public:
    using Ptr = std::shared_ptr<initializer_list_expr>;

    std::vector<expr::Ptr> elems;
};
```

Children:

- `elems`: initializer element expressions

## block::foreign_expr_base

Base class for foreign expression nodes.

```cpp
class foreign_expr_base : public expr {
public:
    using Ptr = std::shared_ptr<foreign_expr_base>;
};
```

Notes: `foreign_expr_base` is an abstract IR category. It has a protected
constructor and is used through `foreign_expr<T>`.

## block::foreign_expr<T>

Expression wrapper for a foreign first-stage value.

```cpp
template <typename T>
class foreign_expr : public foreign_expr_base {
public:
    using Ptr = std::shared_ptr<foreign_expr>;

    T inner_expr;
};
```

Fields:

- `inner_expr`: foreign value stored in the expression node

## block::member_access_expr

Member access expression.

```cpp
class member_access_expr : public expr {
public:
    using Ptr = std::shared_ptr<member_access_expr>;

    expr::Ptr parent_expr;
    std::string member_name;
};
```

Children:

- `parent_expr`: expression whose member is being accessed
- `member_name`: member name

## block::addr_of_expr

Address-of expression.

```cpp
class addr_of_expr : public unary_expr {
public:
    using Ptr = std::shared_ptr<addr_of_expr>;
};
```

Children: inherited from [`unary_expr`](#blockunary-expr).

## block::cast_expr

Cast expression.

```cpp
class cast_expr : public unary_expr {
public:
    using Ptr = std::shared_ptr<cast_expr>;

    type::Ptr type1;
};
```

Children:

- `expr1`: expression being cast, inherited from [`unary_expr`](#blockunary-expr)
- `type1`: target type

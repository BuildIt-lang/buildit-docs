---
title: block::type
kind: reference
namespace: block
header: blocks/var.h
keywords: block::type, type, block::scalar_type, scalar_type, block::pointer_type, pointer_type, block::reference_type, reference_type, block::function_type, function_type, block::array_type, array_type, block::builder_var_type, builder_var_type, block::named_type, named_type, block::anonymous_type, anonymous_type
---

# block::type

Type nodes represent generated C/C++ types in the BuildIt IR.

This page documents the `block::type` hierarchy from `blocks/var.h`. The
`block::var` class is defined in the same header but is documented separately.

## block::type

Base class for all type nodes.

```cpp
class type : public block {
public:
    using Ptr = std::shared_ptr<type>;

    bool is_const = false;
    bool is_volatile = false;
};
```

Fields:

- `is_const`: whether the type is const-qualified
- `is_volatile`: whether the type is volatile-qualified

Notes: `type` is an abstract IR category. It is used through derived type nodes
and is not expected to be instantiated directly.

## block::scalar_type

Scalar built-in type.

```cpp
class scalar_type : public type {
public:
    using Ptr = std::shared_ptr<scalar_type>;

    enum {
        SHORT_INT_TYPE,
        UNSIGNED_SHORT_INT_TYPE,
        INT_TYPE,
        UNSIGNED_INT_TYPE,
        LONG_INT_TYPE,
        UNSIGNED_LONG_INT_TYPE,
        LONG_LONG_INT_TYPE,
        UNSIGNED_LONG_LONG_INT_TYPE,
        CHAR_TYPE,
        UNSIGNED_CHAR_TYPE,
        VOID_TYPE,
        FLOAT_TYPE,
        DOUBLE_TYPE,
        LONG_DOUBLE_TYPE,
        BOOL_TYPE
    } scalar_type_id;
};
```

Fields:

- `scalar_type_id`: selected built-in scalar type

## block::pointer_type

Pointer type.

```cpp
class pointer_type : public type {
public:
    using Ptr = std::shared_ptr<pointer_type>;

    type::Ptr pointee_type;
};
```

Children:

- `pointee_type`: type pointed to

## block::reference_type

Reference type.

```cpp
class reference_type : public type {
public:
    using Ptr = std::shared_ptr<reference_type>;

    type::Ptr referenced_type;
};
```

Children:

- `referenced_type`: referenced type

## block::function_type

Function type.

```cpp
class function_type : public type {
public:
    using Ptr = std::shared_ptr<function_type>;

    type::Ptr return_type;
    std::vector<type::Ptr> arg_types;
    bool is_variadic = false;
};
```

Children:

- `return_type`: function return type
- `arg_types`: function argument types
- `is_variadic`: whether the function type accepts variadic arguments

## block::array_type

Array type.

```cpp
class array_type : public type {
public:
    using Ptr = std::shared_ptr<array_type>;

    type::Ptr element_type;
    int size;
};
```

Children:

- `element_type`: array element type
- `size`: array size; generated code may use special values for unsized arrays

## block::builder_var_type

Type node that represents a BuildIt wrapper type.

```cpp
class builder_var_type : public type {
public:
    using Ptr = std::shared_ptr<builder_var_type>;

    enum { DYN_VAR, STATIC_VAR } builder_var_type_id;

    type::Ptr closure_type;
};
```

Children:

- `builder_var_type_id`: whether this is a `dyn_var` or `static_var` wrapper type
- `closure_type`: wrapped type

## block::named_type

Named generated type, optionally with template arguments.

```cpp
class named_type : public type {
public:
    using Ptr = std::shared_ptr<named_type>;

    std::string type_name;
    std::vector<type::Ptr> template_args;
};
```

Children:

- `type_name`: generated type name
- `template_args`: generated template argument types

## block::anonymous_type

Type node for an unnamed type represented by a referenced declaration.

```cpp
class anonymous_type : public type {
public:
    using Ptr = std::shared_ptr<anonymous_type>;

    std::shared_ptr<block> ref_type;
};
```

Children:

- `ref_type`: referenced declaration node for the anonymous type

## See Also

- [`block::block`](block.md)
- [Statement Types](statement-types.md)
- [Expression Types](expression-types.md)

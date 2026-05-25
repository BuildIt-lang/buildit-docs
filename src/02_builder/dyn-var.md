---
title: builder::dyn_var
kind: class template
namespace: builder
header: builder/dyn_var.h
keywords: builder::dyn_var, dyn_var, with_name, with_type, defer_init, as_member, addr, deferred_init, add_attribute, set_type, operator overloads, constructors
---

# builder::dyn_var

`builder::dyn_var<T>` represents a next-stage value of type `T`. Operations on a
`dyn_var` do not immediately compute a normal C++ value; they build BuildIt's
intermediate representation for code that will run in the generated stage.

`dyn_var<T>` is the primary type used for dynamic parameters, local variables,
expressions, array access, pointer access, function calls, and staged control
flow.

Conditions and loops that depend on `dyn_var` expressions are also captured into
the generated program. For example, `if (x > 3)` and `while (i < n)` become
second-stage control flow when `x`, `i`, or `n` are `dyn_var` values.

## Synopsis

```cpp
#include "builder/dyn_var.h"

namespace builder {

template <typename T>
class dyn_var {
public:
    // Constructors and operators are overloaded to build staged statements
    // and expressions.

    dyn_var<T>* addr();
    void deferred_init();

    template <typename TO>
    void deferred_init(const TO& other);

    void add_attribute(std::string attr);
    void set_type(type t);
};

}
```

## Constructors And Operators

`dyn_var<T>` overloads its constructors and operators so normal-looking C++
expressions can be captured as BuildIt statements and expressions.

For example, declarations such as `dyn_var<int> x = 0`, assignments such as
`x = y + 1`, array access such as `a[i]`, pointer/member access, function calls,
and conditions such as `if (x < 10)` all build next-stage IR rather than
executing as ordinary C++ values.

## Supported Types

`dyn_var<T>` supports common scalar C++ types such as `int`, `long`, `short`,
`long long`, `char`, `void`, `float`, and `double`, including unsigned variants.
Pointers, references, and arrays of these types are also supported.

Array values can be represented as `dyn_var<T[N]>` when the size is known at
compile time, or as `dyn_var<T[]>` when the size is supplied separately.

Do not use standard containers such as `std::vector<dyn_var<T>>` to model
second-stage arrays. Use BuildIt's array abstractions instead. A `dyn_var<T[]>`
represents an array in the generated program and can be indexed by dynamic
values.

For custom types, specialize or extend the `dyn_var` interface so BuildIt knows
how to expose the generated members.

## Constructor Helpers

These helper objects select special `dyn_var<T>` construction behavior.

### with_name

```cpp
builder::with_name(const std::string& name, bool with_decl = false);
```

Constructs a `dyn_var` with a requested generated name.

When `with_decl` is `true`, BuildIt also emits a declaration for the named
variable. When `with_decl` is `false`, the `dyn_var` refers to an existing named
value, such as a runtime function or an externally declared variable.

```cpp
builder::dyn_var<int> local = builder::with_name("local", true);
builder::dyn_var<void(char*)> puts = builder::with_name("puts");
```

### with_type

```cpp
builder::with_type(const builder::type& t);

template <typename T>
builder::with_type(const builder::type& t, const T& init);

builder::with_type(const dyn_var_base& v);
```

Constructs a `dyn_var` with an explicitly supplied second-stage type.

This constructor helper is only available for
[`builder::dyn_var<builder::generic>`](generic.md). Use it when the generated
type depends on first-stage logic rather than the first-stage C++ type. The
overload taking an initializer also initializes the generic value from an
expression, and the overload taking another `dyn_var` copies both the generated
type and expression.

```cpp
builder::dyn_var<builder::generic> x =
    builder::with_type(builder::create_type<int>());
```

### defer_init

```cpp
builder::defer_init
```

Constructs a `dyn_var` without creating the underlying staged variable yet. Call
[`deferred_init`](#deferred-init) later to complete initialization.

This is useful when a `dyn_var` must be declared as a member or in a scope where
its generated declaration should be delayed.

### as_member

```cpp
builder::as_member(dyn_var_base* parent, std::string name);
builder::as_member(std::string name);
```

Constructs a `dyn_var` as a named member of another dynamic value. This is used
when defining custom `dyn_var` specializations or custom staged struct-like
types.

## Member Functions

### addr

```cpp
dyn_var<T>* addr();
```

Returns the true first-stage address of the `dyn_var<T>` wrapper object. This is
needed because `operator&` is overloaded to build an address-of expression in the
second stage.

### deferred_init

```cpp
void deferred_init();

template <typename TO>
void deferred_init(const TO& other);
```

Initializes a `dyn_var` that was constructed with `defer_init`.

The overload taking `other` initializes from any value that can be used to create
a `dyn_var<T>`.

### add_attribute

```cpp
void add_attribute(std::string attr);
```

Adds a generated-code attribute to the variable. Duplicate attributes are ignored.

For example, samples use `add_attribute("restrict")` on pointer parameters.

### set_type

```cpp
void set_type(type t);
```

Sets the underlying BuildIt type of a standalone `dyn_var`.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=c971af5b95c9e074ae5d638d115c6228 }}

```cpp
#include "builder/builder_context.h"
#include "builder/dyn_var.h"
#include "blocks/c_code_generator.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_var;
using builder::with_name;

// Declare a global dynamic function with a name.
dyn_var<void(char*)> b_puts = with_name("puts");

struct bar {
    dyn_var<int> x = with_name("x");
};

static void foo() {
    dyn_var<int> x = 0;
    x = x + 1;

    // Conditions depending on dyn_var values become generated branches.
    if (x > 3) {
        dyn_var<long> y = 0;

        // Loops depending on dyn_var values become generated loops.
        while (y < 100) {
            y += 2;
        }
    } else {
        dyn_var<char*> z = "Hello world!";

        // dyn_var function call to a named global.
        b_puts(z);
    }

    // Create a named function and access a generated member.
    dyn_var<bar()> get_bar = with_name("get_bar");
    dyn_var<int> a = get_bar().x;
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::builder_context`](builder-context.md)

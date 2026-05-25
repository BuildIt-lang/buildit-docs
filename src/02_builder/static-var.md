---
title: builder::static_var
kind: class template
namespace: builder
header: builder/static_var.h
keywords: builder::static_var, static_var, operator T&, operator const T&, deferred_init, resize, array specialization, first stage
---

# builder::static_var

`builder::static_var<T>` declares variables and expressions that are completely
evaluated in the first stage.

`static_var<T>` overloads construction and destruction so BuildIt can track value
changes and use them to guide extraction. Apart from this tracking,
`static_var<T>` behaves like `T`: it can be implicitly converted to `T&` or
`const T&`, and it can be read and written like a normal first-stage value.

If a value does not need tracking during extraction, it can usually remain a
regular C++ variable. Use `static_var<T>` when the value changes in a way that
BuildIt must observe while exploring dynamic branches or memoized paths.

Unlike `dyn_var`, `static_var` can only be constructed inside staged execution.
If it must be declared outside that context, construct it with `defer_init` and
initialize it later with [`deferred_init`](#deferred-init).

`static_var` objects should be live only for the duration of the function being
extracted and should be initialized and updated consistently if extraction runs
the function more than once. Storing arbitrary pointers or random values in
`static_var` can produce unexpected behavior.

The wrapped type must be copy constructible and equality comparable. Arrays of
valid element types can also be wrapped with `static_var<T[]>`; set their size
with [`resize`](#resize).

Control flow that depends only on `static_var` or ordinary C++ values is
evaluated during extraction. A loop whose condition depends only on first-stage
values is unrolled, and each iteration has a concrete iterator value. Similarly,
an `if` condition depending only on first-stage values selects one branch during
extraction.

## Synopsis

```cpp
#include "builder/static_var.h"

namespace builder {

template <typename T>
class static_var {
public:
    operator T&();
    operator const T&() const;

    void deferred_init();

    // Only available for array types.
    void resize(size_t size);
};

}
```

## Requirements

`static_var<T>` requires `T` to be copy constructible and equality comparable.

## Behavior

`static_var<T>` behaves like a first-stage C++ value through conversion operators
to `T&` and `const T&`. Assignments update the stored first-stage value.

Unlike a normal local C++ variable, a `static_var` is registered with the current
BuildIt run state. This lets BuildIt track first-stage state while exploring
dynamic branches and memoized paths.

## Member Functions

### operator T&

```cpp
operator T&();
operator const T&() const;
```

Returns a reference to the tracked first-stage value.

### deferred_init

```cpp
void deferred_init();
```

Initializes a `static_var` that was constructed with `defer_init`.

Deferred static variables are tracked separately from ordinary static variables,
which is useful for members or objects whose initialization must be delayed.

### resize

```cpp
void resize(size_t size);
```

Available on `static_var<T[]>`.

Resizes the first-stage array storage. This changes only the first-stage tracked
array and does not emit second-stage code.

Call `resize` before the first use of the array. It should only be called once
for a given `static_var<T[]>`, and should not be used when the array was
initialized from an initializer list.

## Array Specialization

`static_var<T[]>` stores a tracked first-stage array. It supports indexing with
first-stage indices and can be resized with [`resize`](#resize).

Use this when the controlling data is first-stage state. Use `dyn_var<T[]>` when
the array itself should exist in generated code.

## Example {{ tryit: https://buildit.so/tryit/?sample=shared&pid=b33da6429a47e066117f1cf69ece00ba }}

```cpp
#include "builder/builder_context.h"
#include "blocks/c_code_generator.h"
#include "builder/static_var.h"
#include <iostream>

using builder::builder_context;
using builder::dyn_var;
using builder::static_var;

void foo(const int iter) {
    dyn_var<int> sum = 0;

    // static_vars of array types are declared without size.
    static_var<int[]> arr;

    // Array must be resized before first use.
    arr.resize(iter);

    // Loops with static_var iterators are evaluated and unrolled.
    for (static_var<int> x = 0; x < iter; x++) {
        // Conditions with static_var values are specialized.
        if (x % 2 == 0) {
            sum += x;
        } else {
            sum -= x;
        }

        // static_var arrays can only be indexed by first-stage values.
        arr[x] = x;
    }
}

int main() {
    builder_context context;
    auto ast = context.extract_function_ast(foo, "foo", 16);
    block::c_code_generator::generate_code(ast, std::cout, 0);

    return 0;
}
```

## See Also

- [`builder::dyn_var`](dyn-var.md)
- [`builder::builder_context`](builder-context.md)

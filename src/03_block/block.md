---
title: block::block
kind: class
namespace: block
header: blocks/block.h
keywords: block::block, block, Ptr, setMetadata, hasMetadata, getMetadata, getBoolMetadata, dump, accept, self, is_same, isa, to, clone, static_offset, tracer::tag
---

# block::block

`block::block` is the root base class for BuildIt's IR nodes.

Expressions, statements, variables, and types all derive from `block`. The base
class provides shared ownership, source-location tagging, metadata storage,
visitor dispatch, structural comparison, and cloning hooks.

## Synopsis

```cpp
#include "blocks/block.h"

namespace block {

class block : public std::enable_shared_from_this<block> {
public:
    using Ptr = std::shared_ptr<block>;

    tracer::tag static_offset;

    template <typename T>
    void setMetadata(std::string mdname, const T& val);

    template <typename T>
    bool hasMetadata(std::string mdname);

    template <typename T>
    T getMetadata(std::string mdname);

    bool getBoolMetadata(std::string mdname);

    virtual void dump(std::ostream& out, int indent);
    virtual void accept(block_visitor* visitor);

    template <typename T>
    std::shared_ptr<T> self();

    virtual bool is_same(block::Ptr other);
};

template <typename T>
bool isa(std::shared_ptr<block> p);

template <typename T>
std::shared_ptr<T> to(std::shared_ptr<block> p);

template <typename T>
std::shared_ptr<T> clone(std::shared_ptr<T> p);

}
```

Notes: `block` is an abstract IR category. It is used through derived node types
and is not expected to be instantiated directly.

## Static Offset

```cpp
tracer::tag static_offset;
```

Static tag associated with the IR node.

BuildIt uses this tag to identify the first-stage program point that produced
the node. See [`tracer::tag`](../04_util/tracer-tag.md).

## Metadata

### setMetadata

```cpp
template <typename T>
void setMetadata(std::string mdname, const T& val);
```

Stores metadata value `val` under `mdname`.

### hasMetadata

```cpp
template <typename T>
bool hasMetadata(std::string mdname);
```

Returns `true` only when metadata named `mdname` exists and was stored with type
`T`.

### getMetadata

```cpp
template <typename T>
T getMetadata(std::string mdname);
```

Returns metadata named `mdname` as type `T`. Asserts if the metadata is missing
or has a different type.

### getBoolMetadata

```cpp
bool getBoolMetadata(std::string mdname);
```

Convenience helper for boolean metadata. Returns `true` only if `mdname` exists
as `bool` metadata and its value is `true`.

## Visitor And Utilities

### dump

```cpp
virtual void dump(std::ostream& out, int indent);
```

Writes a debug representation of the node to `out`.

### accept

```cpp
virtual void accept(block_visitor* visitor);
```

Dispatches the node to a [`block_visitor`](block-visitor.md).

### self

```cpp
template <typename T>
std::shared_ptr<T> self();
```

Returns `shared_from_this()` cast to `T`.

### is_same

```cpp
virtual bool is_same(block::Ptr other);
```

Compares two IR nodes structurally. The base implementation compares
`static_offset`; derived node types extend this with their own fields.

## isa

```cpp
template <typename T>
bool isa(std::shared_ptr<block> p);
```

Returns `true` when `p` can be dynamically cast to `T`.

Use this to check a node's concrete type before calling [`to`](#to).

## to

```cpp
template <typename T>
std::shared_ptr<T> to(std::shared_ptr<block> p);
```

Casts `p` to `T` and returns the cast pointer.

This helper asserts if the cast is invalid. Use [`isa`](#isa) first when the
node type is uncertain.

## clone

```cpp
template <typename T>
std::shared_ptr<T> clone(std::shared_ptr<T> p);
```

`clone(p)` is a free helper function, not a member of `block::block`.

It returns `nullptr` for a null pointer. Otherwise it calls the node's virtual
clone implementation and casts the result back to `T`. Use it when a pass needs
to copy an IR subtree while preserving the concrete node type in the returned
`std::shared_ptr`.

## See Also

- [Expression Types](expression-types.md)
- [`block::block_visitor`](block-visitor.md)
- [`tracer::tag`](../04_util/tracer-tag.md)

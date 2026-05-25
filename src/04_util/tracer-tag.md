---
title: tracer::tag
kind: class
namespace: tracer
header: util/tracer.h
keywords: tracer::tag, tag, tracer::tag_id, tag_id, static tag, static_offset, pointers, static_var_snapshots, static_var_key_values, live_dyn_vars, dedup_id, is_empty, clear, slice_loc, stringify, stringify_loc, stringify_stat, hash, get_unique_tag, get_offset_in_function
---

# tracer::tag

`tracer::tag` identifies a static program point observed while BuildIt extracts
a staged function.

BuildIt uses tags to line up observations from repeated first-stage executions.
They are attached to IR nodes through fields such as `block::block::static_offset`
and are used internally for memoization, deduplication, variable naming, labels,
and staged control-flow recovery.

Most users do not need to construct tags directly, but they are visible in the
IR and are useful when writing advanced passes.

## Synopsis

```cpp
#include "util/tracer.h"

namespace tracer {

using tag_id = size_t;

class tag {
public:
    std::vector<unsigned long long> pointers;
    std::vector<std::shared_ptr<builder::static_var_snapshot_base>>
        static_var_snapshots;
    std::vector<std::pair<std::string, std::string>> static_var_key_values;
    std::vector<tag_id> live_dyn_vars;
    size_t dedup_id = 0;

    bool operator==(const tag& other) const;
    bool operator!=(const tag& other) const;

    bool is_empty() const;
    void clear();

    tag slice_loc();

    std::string stringify();
    std::string stringify_loc();
    std::string stringify_stat();

    size_t hash() const;
};

tag get_unique_tag();
tag get_offset_in_function();

}
```

`std::hash<tracer::tag>` is specialized so tags can be used as keys in
`std::unordered_map` and `std::unordered_set`.

## Fields

### pointers

```cpp
std::vector<unsigned long long> pointers;
```

Call-stack or location information used to identify the static program point.

The exact contents depend on the tracer implementation. The
`TRACER_USE_LIBUNWIND` build option changes how BuildIt constructs these static
tags.

### static_var_snapshots

```cpp
std::vector<std::shared_ptr<builder::static_var_snapshot_base>>
    static_var_snapshots;
```

Snapshots of live `static_var` values that contribute to the tag.

This lets BuildIt distinguish the same source location reached with different
first-stage values.

### static_var_key_values

```cpp
std::vector<std::pair<std::string, std::string>> static_var_key_values;
```

String form of static variable values, used for debugging and name recovery.

### live_dyn_vars

```cpp
std::vector<tag_id> live_dyn_vars;
```

Identifiers for dynamic variables that are live when the tag is constructed.

### dedup_id

```cpp
size_t dedup_id = 0;
```

Additional disambiguator used when the same static tag is observed more than
once in contexts that need distinct IR nodes.

## Member Functions

### operator==

```cpp
bool operator==(const tag& other) const;
bool operator!=(const tag& other) const;
```

Compares tags structurally.

### is_empty

```cpp
bool is_empty() const;
```

Returns whether the tag has no location pointers.

### clear

```cpp
void clear();
```

Clears the location pointers, static variable snapshots, live dynamic variables,
and `dedup_id`.

### slice_loc

```cpp
tag slice_loc();
```

Returns a tag containing only the location portion of the tag.

This is useful when a pass wants to compare source locations while ignoring
static variable snapshots.

### stringify

```cpp
std::string stringify();
std::string stringify_loc();
std::string stringify_stat();
```

Returns debug strings for the full tag, the location portion, or the static
portion.

These are intended for debugging. `stringify` depends on static values being
convertible to strings.

### hash

```cpp
size_t hash() const;
```

Computes and caches a hash for the tag.

## Free Functions

### get_unique_tag

```cpp
tag get_unique_tag();
```

Returns a fresh tag.

### get_offset_in_function

```cpp
tag get_offset_in_function();
```

Constructs a tag for the current point in the staged function.

This is one of the internal hooks BuildIt uses while extracting IR from staged
execution.

## See Also

- [`block::block`](../03_block/block.md)
- [`builder::static_var`](../02_builder/static-var.md)
- [Concepts: Static Tags](../01_getting_started/03_concepts.md#static-tags)
- [Build Configuration](../01_getting_started/02_build-configuration.md)

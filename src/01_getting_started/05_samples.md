---
title: Samples
kind: guide
keywords: samples, examples, buildit/samples, extract_function_ast, dyn_var, static_var, compile_function, compile_asts, CUDA, D2X, RCE, matchers, replacers
---

# Samples

The BuildIt repository includes a `samples/` directory with small programs that
exercise extraction, code generation, optimization passes, dynamic compilation,
and DSL-building features.

Most samples print either the extracted IR, generated C/C++ code, or both. The
table below summarizes what each sample is intended to cover.

| Sample | Description |
| --- | --- |
| `sample1.cpp` | Straight-line `dyn_var` code covering declarations, initialization, arithmetic, bitwise operators, compound assignment, unary operators, and address-of behavior. |
| `sample2.cpp` | Basic dynamic `if` and `else` reconstruction, including code that must remain after the branch and a ternary expression. |
| `sample3.cpp` | Nested dynamic conditionals and branch merge behavior after nested `if` statements. |
| `sample4.cpp` | Minimal assignment and binary-expression generation for three `dyn_var<int>` values. |
| `sample5.cpp` | Simple dynamic `for` loop extraction. |
| `sample6.cpp` | Dynamic loop extraction with `continue` and `break`. |
| `sample7.cpp` | Nested dynamic loop extraction. |
| `sample8.cpp` | Duplicate of the loop-with-`break`/`continue` case, used as another regression point for structured loop recovery. |
| `sample9.cpp` | Annotation insertion and lookup with `block::annotation_finder`. |
| `sample10.cpp` | Pointer, array indexing, reference binding, and assignment through a `dyn_var<int*>`. |
| `sample11.cpp` | Function calls during staging that emit straight-line code and should not be mistaken for loops. |
| `sample12.cpp` | Static loop unrolling with `static_var`; the extracted AST should contain repeated statements rather than a generated loop. |
| `sample13.cpp` | Mixed static and dynamic loops: the outer static loop is unrolled while the inner dynamic loop remains generated code. |
| `sample14.cpp` | Passing `dyn_var` values through helper functions and returning staged expressions. |
| `sample15.cpp` | Function pointer and function-valued `dyn_var` declarations and calls. |
| `sample16.cpp` | Named global `dyn_var` use with `builder::with_name`, replacing the older assumed-variable style. |
| `sample17.cpp` | A staged Brainfuck interpreter that specializes on a first-stage program string and emits a generated `main`. |
| `sample18.cpp` | Large static unrolling of dynamic branches. |
| `sample19.cpp` | Extraction from a lambda instead of a named function. |
| `sample20.cpp` | Fixed-size, unsized, and multidimensional `dyn_var` array types. |
| `sample21.cpp` | Mixing `static_var` values into generated `dyn_var` expressions. |
| `sample22.cpp` | Returning a first-stage local through a `dyn_var` result and using that result in later generated branches. |
| `sample23.cpp` | Nested builder wrapper types such as `dyn_var<static_var<int>>` and `dyn_var<dyn_var<int>>`, used to exercise type closure logic. |
| `sample24.cpp` | `extract_function_ast` over lambdas and functions with generated arguments, static arguments, references, and named function-valued arguments. |
| `sample25.cpp` | Unstructured `while (1)` loops with nested breaks, used as a control-flow recovery regression. |
| `sample26.cpp` | Power function template instantiated with either the base or the exponent as a first-stage/static value. |
| `sample27.cpp` | `NO_TEST`. Deprecated loop-roll annotation experiments over sparse arrays and adjacency matrices. |
| `sample28.cpp` | Primitive scalar, pointer, string, const/volatile pointer, and boolean `dyn_var` type coverage. |
| `sample29.cpp` | Legacy `builder::name` custom type naming and operator lookup through ADL. |
| `sample30.cpp` | Dynamic loop with a conditional `break` from inside the loop body. |
| `sample31.cpp` | `for` loops where the induction variable is declared outside the loop and reused across loops. |
| `sample32.cpp` | Dynamic compilation with `builder::compile_function` for a power function specialized by a static exponent. |
| `sample33.cpp` | CUDA extraction from annotated loop nests using CUDA kernel annotations. |
| `sample34.cpp` | Legacy `dyn_var` specialization for a named custom type, member access, pointer member access, and copy behavior. |
| `sample35.cpp` | `NO_TEST`. Binomial coefficient generation with first-stage table construction and rolled initialization. |
| `sample36.cpp` | Regex matcher DSL example using static state, generated string traversal, unstructured control flow, and RCE. |
| `sample37.cpp` | Dynamic C++ compilation with `compile_function_with_context`, custom vector type support, and required generated C++ headers. |
| `sample38.cpp` | Dynamic unsized arrays, resizing, pointer-style dereference of array storage, and indexed updates. |
| `sample39.cpp` | `builder::arr` and `builder::dyn_arr` initialization, copying, dynamic sizing, and arrays of objects containing staged fields. |
| `sample40.cpp` | RCE regression cases involving boolean expressions and changed generated-code semantics before and after redundant copy elimination. |
| `sample41.cpp` | Multi-function generation and dynamic compilation with `compile_asts`, using first-stage worklists to generate mutually connected functions. |
| `sample42.cpp` | Modern `builder::custom_type` examples with named members, templated custom types, pointer access, and generated struct declarations. |
| `sample43.cpp` | Dynamically sized `static_var<int[]>` storage used as static loop state across deeply nested loops. |
| `sample44.cpp` | `dyn_arr` declarations inside control flow, including construction inside an infinite loop. |
| `sample45.cpp` | `builder::with_name` behavior for explicit variable naming and name reuse. |
| `sample46.cpp` | Nested unstructured loops with breaks from inner loops. |
| `sample47.cpp` | Control-flow recovery when a jump exits through a parent loop. |
| `sample48.cpp` | `builder::up_cast_range` and RCE used to specialize an evenness test over a bounded dynamic value. |
| `sample49.cpp` | Deferred initialization of staged fields stored in an external first-stage object passed through `other_args`. |
| `sample50.cpp` | Static tag and lifetime behavior when branches fork first-stage state and later merge. |
| `sample51.cpp` | Struct member naming behavior for structs with staged members and non-staged spacer fields. |
| `sample52.cpp` | Nested custom structs, named members, generated struct declarations, global named staged objects, and member updates. |
| `sample53.cpp` | Manual redundant-copy elimination over pointer aliases, increments, and chained temporary copies. |
| `sample54.cpp` | Lifetime and deinitialization ordering for heap-allocated `static_var` objects and arrays. |
| `sample55.cpp` | Custom type wrapper for `std::vector`, nested vector types, method calls, and indexed access. |
| `sample56.cpp` | `builder::generic`, `type_of`, `with_type`, runtime type placeholders, and RCE over generic staged values. |
| `sample57.cpp` | Unreleased `nd_var` experiment for nondeterministic first-stage values. |
| `sample58.cpp` | Expression pattern construction, `find_all_matches`, operator pattern aliases, and `replace_match`. |
| `sample59.cpp` | `external_type_namer` for incomplete types and generated structs containing pointers to incomplete external types. |
| `sample60.cpp` | RCE over exponentiation and loop examples where copies must not be eliminated incorrectly. |
| `sample61.cpp` | `static_var<std::vector<int>>` state controlling extraction while emitting generated branches. |
| `sample62.cpp` | Passing a first-stage `std::vector<int>` through `other_args` and using it to initialize a generated unsized array. |
| `sample63.cpp` | Pragma annotations that become `_Pragma` directives in generated code. |
| `sample64.cpp` | Calling named runtime functions such as `malloc` and `free`, with `builder::cast_to` for the returned pointer. |
| `sample65.cpp` | Adding generated variable attributes such as `restrict` to function pointer parameters. |

## See Also

- [Concepts](03_concepts.md)
- [`builder::builder_context`](../02_builder/builder-context.md)
- [`builder::compile_function`](../02_builder/compile-function.md)
- [`block::c_code_generator`](../03_block/c-code-generator.md)

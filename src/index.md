### Overview
BuildIt is a light-weight type-based multi-stage programming framework in C++ with primary focus on making it easy to develop high-performance domain-specific languages (DSLs) embedded in C++. The core BuildIt library implements the two template types dyn\_var\<T\> and static\_var\<T\> and utilities the user can use to extract, generate and compile code. The rest of the library has several utilities focused on DSL features like parallel code generation, analysis and transformations and extending user defined types.
<br><br>
This document assumes familiarity with C++ for the multi-stage library and understanding of peformance and optimizations for the DSL implementations. BuildIt doesn't expect any compiler expertise but familiarity wiht compilers can help with some internal low-level interfaces that are also documented here.
<br><br>
BuildIt can be used in two ways, either by building from source and using in your applications or with the online tool for experimenting and generating code. Both the methods are documented here. The language reference is the same for both the modes.



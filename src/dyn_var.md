## builder::dyn\_var Class Reference
<hr>
	
	\k{#include} "builder/dyn_var.h"

	\k{namespace} builder {
	  \k{template} <\k{typename} T>
	  \k{class} dyn_var;
	}

<hr>

The dyn\_var\<T\> type is used to declare variables and expressions that should be evaluated in the second stage. All expressions and statements written with these types will be generated as it is. Conditions and loops that are dependent on expressions of these types are generated as it is. 
<br><br>
Currently supported types that can be used with dyn\_var - `int, long, short, long long, char, void, float, double` along with their unsigned versions. Arrays, pointers and references of these types are also supported. For all other types `builder::name` should be used. Custom types with custom members can be created by inheriting from [`builder::custom_type<>`](custom_type.html) or by [specializing `dyn_var<T>`](specialize_dyn_var.h).
<br><br>
dyn\_var of array types can be created in two ways - `dyn_var<T[]>` or `dyn_var<T[N]>` where `N` is a compile time constant. If the size of the array is a first stage runtime value, the first version should be used and the array should be resize later by calling [`builder::resize_arr()`](dyn_var.html#t-resize_arr).
<br><br>
Arrays, std::vector, std::array or similar containers for dyn\_var should never be created, use [`dyn_arr<T>`](dyn_arr.html) instead. Notice that while `dyn_var<T[]>` produces an array in the generated codewhich can be indexed by dyn\_var values in the second stage, `dyn_arr<T, N>` produces a set of `dyn_var` values. The array can only be indexed with first stage values and produces access to the appropriate dyn\_var from the set.

### Public Member Functions
This type has several special constructor overloads for specific scenarios. 

- [`dyn_var(builder::with_name)`](dyn_var.html#t-with_name)
- [`dyn_var(builder::as_global)`](dyn_var.html#t-as_global)
- [`dyn_var(builder::defer_init)`](defer_init.html)
- [`dyn_var(builder::cast)`](dyn_var.html#t-cast)
- [`void deferred_init(void)`](dyn_var.html#t-deferred_init)

### Special Constructors Descriptions

\tag{with_name}

	builder::with_name(\k{const} std::string &name, \k{bool} with_decl = \k{false})

This constructor overload helper creates a new dyn\_var with the specified name. The optional `with_decl` argument controls if a declaration should be generated. This constructor helper is also used to 
name members of custom structs. 

\tag{as_global}

	builder::as_global(\k{const} std::string &name)

This constructor overload helper creates a new dyn\_var with the specified name but unlike `with_name` should be used when the dyn\_var being declared at a global scope. This never generates a declaration. 

\tag{cast}

	builder::cast(\k{const} builder::builder&) 

This constructor overload takes an arbitrary expression of any BuildIt type and creates a dyn\_var of the given type. No new variables are generated in the second stage code, but the newly instantiated dyn\_var refers to the original expression itself. 
This is mainly used to cast expressions to custom types to access their members. Such a cast is not required for common operations that return dyn\_var of struct types like when pointers are dereferenced. Remember this constructor doesn't generate 
a cast but just treats the expression as a new type in the first stage. 

### Member Function Descriptions

\tag{deferred_init}
	
	\k{void} deferred_init(\k{void})

### Helper Functions

\tag{resize_arr}

	\k{template}<\k{typename} T>
	\k{void} resize_arr(\k{const} dyn_var<T[]> &, \k{int} size);

Resizes a dyn\_var array with unspecified length. This should be called immediately after the declration before the first use. Calling `resize_arr` on an array which already has a size leads to undefined behavior. This function call doesn't generate any second stage code but changes the original declaraion of the function. 

### Example - [Try It!](https://buildit.so/tryit/?sample=shared&pid=93a16ee889dac82753d23f12c1ed979b) 

<pre class="code-box">
\k{#include} "builder/builder_context.h"
\k{#include} "blocks/c_code_generator.h"
\k{#include} \<iostream\>

\c{// Declare a global dynamic variable with a name}
builder::dyn_var\<\k{void}(\k{char}*)\> b_puts = builder::as_global("puts");

\k{struct} bar {
    builder::dyn_var\<\k{int}\> x = builder::with_name("x");
};


\k{static} \k{void} foo (\k{void}) {
    builder::dyn_var\<\k{int}\> x = 0;
    x = x + 1;
    \c{// Condition dependent on dyn_var}
    \k{if} (x \> 3) {
        builder::dyn_var\<\k{long}\> y = 0;
        \c{// Loop dependent on dyn_var}
        \k{while} (y \< 100) {
            y += 2;
        }
    } \k{else} {
        builder::dyn_var\<\k{char}*\> z = "Hello world!";
        \c{// dyn_var function call to a global}
        b_puts(z); 
    }

    \c{// Create a named function without a declaration}
    builder::dyn_var\<bar()\> get_bar = builder::with_name("get_bar");
    \c{// Return value is "casted" to bar}
    ((builder::dyn_var\<bar\>)(builder::cast)get_bar()).x = 2;

}

\k{int} main(\k{int} argc, \k{char}* argv[]) {
    builder::builder_context context;
    \k{auto} ast = context.extract_function_ast(foo, "foo");

    block::c_code_generator::generate_code(ast, std::cout, 0);

    \k{return} 0;
}
</pre>


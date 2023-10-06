## builder::dyn\_var Class Reference
<hr>
	
	#include "builder/dyn_var.h"

	\k{namespace} builder {
	  \k{template} <\k{typename} T>
	  \k{class} dyn_var;
	}

<hr>

The dyn\_var&lt;T&gt; type is used to declare variables and expressions that should be evaluated in the second stage. All expressions and statements written with these types will be generated as it is. Conditions and loops that are dependent on expressions of these types are generated as it is. 
<br><br>
Currently supported types that can be used with dyn\_var - `int, long, short, long long, char, void, float, double` along with their unsigned versions. Arrays, pointers and references of these types are also supported. For all other types `builder::name` should be used. Custom types with custom members can be created by inheriting from [`builder::custom_type<>`](custom_type.html) or by [specializing `dyn_var<T>`](specialize_dyn_var.h).
<br><br>
Array types can be created in two ways - `dyn_var<T[]>` or `dyn_var<T[N]>` where `N` is a compile time constant. If the size of the array is a first stage runtime value, the first version should be used and the array should be resize later by calling [`builder::resize_arr()`](dyn_var.html#t-resize_arr).

### Public Member Functions
This type has several special constructor overloads for specific scenarios. 

- [`dyn_var(builder::with_name)`](dyn_var.html#t-with_name)
- [`dyn_var(builder::as_global)`](dyn_var.html#t-as_global)
- [`dyn_var(builder::as_member)`](custom_type.html#t-as_member)
- [`dyn_var(builder::cast)`]()

### Special Constructors Descriptions

<p id="t-with_name"></p>

	builder::with_name(const std::string &name, bool with_decl = false)

This constructor overload helper creates a new dyn\_var with the specified name. The optional `with_decl` argument controls if a declaration should be generated. 

<p id="t-as_global"></p>

	builder::as_global(const std::string &name)

This constructor overload helper creates a new dyn\_var with the specified name but unlike `with_name` should be used when the dyn\_var being declared at a global scope. This never generates a declaration. 

### Helper Functions

<p id="t-resize_arr"></p>

	template<typename T>
	void resize_arr(const dyn_var<T[]> &, int size);

Resizes a dyn\_var array with unspecified length. This should be called immediately after the declration before the first use. Calling `resize_arr` on an array which already has a size leads to undefined behavior. This function call doesn't generate any second stage code but changes the original declaraion of the function. 

### Example - [Try It!](https://buildit.so/tryit/?sample=shared&pid=9033f235c46c7f9d20a9d2deb43cdb51) 

<pre class="code-box">
\k{#include} "builder/builder_context.h"
\k{#include} "blocks/c_code_generator.h"
\k{#include} &lt;iostream&gt;

// Declare a global dynamic variable with a name
builder::dyn_var&lt;\k{void}(\k{char}*)&gt; b_puts = builder::as_global("puts");

\k{static} \k{void} foo (\k{void}) {
    builder::dyn_var&lt;\k{int}&gt; x = 0;
    x = x + 1;
    // Condition dependent on dyn_var
    \k{if} (x &gt; 3) {
        builder::dyn_var&lt;\k{long}&gt; y = 0;
        // Loop dependent on dyn_var
        \k{while} (y &lt; 100) {
            y += 2;
        }
    } \k{else} {
        builder::dyn_var&lt;\k{char}*&gt; z = "Hello world!";
        // dyn_var function call to a global
        b_puts(z); 
    }
}

\k{int} main(\k{int} argc, \k{char}* argv[]) {
    builder::builder_context context;
    \k{auto} ast = context.extract_function_ast(foo, "foo");

    block::c_code_generator::generate_code(ast, std::cout, 0);

    \k{return} 0;
}
</pre>


## builder::dyn\_arr Class Reference
<hr>
	
	#include "builder/array.h"

	\k{namespace} builder {
	  \k{template} <\k{typename} T, \k{size_t} size = 0>
	  \k{class} dyn_arr;
	}

<hr>

The dyn\_arr allows creating an array of dyn\_var of fixed size that can be indexed only with first stage values. Instead of generating an array in the second stage code, dyn\_arr creates `size` number of separate dyn\_vars. Since dyn\_arr can only be indexed with first stage values, accesses just produce a read or write on the appropriate variable from the set. This avoids the indexing overhead in the second stage. 
<br><br>
If the size is dependent on a first stage value instead of being a compile time constant, the parameter should be skipped and the [`set_size`](dyn_arr.html#t-set_size) function should be used. 
<br><br>
The assignment operators on dyn\_arr is deleted and the copy constructor copy initializes the dyn\_var with the corresponding dyn\_var at the same index in the other dyn\_arr. 

### Public Member Functions

- [`void set_size(size_t size)`](dyn_arr.html#t-set_size)
- [`dyn_var<T>& operator [](size_t index)`](dyn_arr.html#t-sqbkt)

### Member Descriptions

<p id="t-set_size"></p>

	void set_size(size_t size) 
	
The set\_size function allows setting the size of arrays where the size depends on a first stage value and is not a compile time constant. This function should be called exactly once after the dyn\_arr declaration before its first use. Calling this function multiple times on an array or calling it on arrays that already have a non-zero size specified in the type leads to undefined behavior.

<p id="t-set_size"></p>

	dyn_var<T>& operator [](size_t index);
	const dyn_var<T>& operator [](size_t index) const;
	
The [] operator creates an access to the dyn\_var at the specified index in the generated code. The parameter should be a first stage value. 


### Example

<pre class="code-block">
\k{#include} "blocks/c_code_generator.h"
\k{#include} "builder/array.h"
\k{#include} "builder/dyn_var.h"

\k{static} \k{void} foo() {
    // Declare an array with 3 dyn_var&lt;int&gt;
    builder::dyn_arr&lt;\k{int}, 3&gt; x;

    x[0] = 1;
    x[1] = x[0] + 2;
    x[2] = x[1] + x[0];

    builder::dyn_arr&lt;\k{int}, 4&gt; y = {0, x[0] + 4, 0, 0};

    // Create 2 dyn_vars and initialize then with the specified values
    builder::dyn_arr&lt;\k{int}&gt; z = {1, 2};

    // Create a dyn_arr without specifying the size in the time and set 
    // it after with a first stage value
    builder::dyn_arr&lt;\k{int}&gt; a;
    a.set_size(2);

    builder::dyn_arr&lt;\k{int}&gt; b = y;
    builder::dyn_arr&lt;\k{int}, 5&gt; c = a;
}
\k{int} main(\k{int} argc, \k{char} *argv[]) {
    \k{auto} ast = builder::builder_context().extract_function_ast(foo, "foo");
    block::c_code_generator::generate_code(ast, cout, 0);
    \k{return} 0;
}
</pre>

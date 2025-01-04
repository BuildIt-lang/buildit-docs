## builder::static\_var Class Reference
<hr>
	
	\k{#include} "builder/dyn_var.h"

	\k{namespace} builder {
	  \k{template} <\k{typename} T>
	  \k{class} static_var;
	}

<hr>

The static\_var\<T\> type is used to declare variables and expressions that are completely evaluated in the first stage. 
static\_var's have their constructor and destructors overloaded to track the changes in the values to help guide the 
extraction process. Besides the tracking, static\_var\<T\> behave exactly like T. This means if a value doesn't change
through the extraction process, it doesn't need to be declared with regular C++ types. static\_var\<T\> can be implicitly 
converted to the T& as required and allows for reading and writing to the value as usual. Unlike dyn\_var, static\_var 
can only be constructed inside the staged execution. If created outside, [`builder::defer_init`](defer_init.html) must be 
used. 
<br>
<br>
Due to current implementation constraints, static\_var can only be wrapped about specific POD types - `short int, int, long, long long, float, double, char` 
and their unsigned versions. It generally does not make sense to wrap pointer types inside
static\_var since pointers can be different across different runs. Arrays of these types can also be wrapped with static\_var and the size must be set with the [`resize`](static_var.html#t-resize)
function.
<br>
<br>
Conditions that depend purely on static\_var or regular C++ types are completely evaluated and only the appropriate branch is
evaluated. Similarly loops where the condition depends purely on static\_var or regular C++ types are also completely 
evaluated and the body of the loop is unrolled with each iteration having a concrete value for the iterator. 



### Public Member Functions
This type has following constructors and members functions - 

- `static_var(const T&)` - Copy initializes the static\_var to have the same value as the argument.
- `template <typename TO> static_var(const static_var<TO>&)` - Copy initializes the static\_var by casting TO to T
- [`static_var(const builder::defer_init&)`](defer_init.html)
- `operator T& ()` - Returns a modifiable lvalue of the stored value.
- `operator const T&() const` - Returns a const lvalue of the stored value (only for const types). 

Constructors and member functions only available for static\_var\<T[]\>

- `static_var(const std::initializer_list<T>&)` - Copy initializes elements of the static\_var of array types using the elements of the initializer list. Also automatically resizes the newly constructed array. 
- [`void resize(size_t)`](static_var.html#t-resize) 


### Public Member Function Descriptions

\tag{resize}

	\k{void} resize(\k{size_t})

This member function is only available for static\_var of array types and is used to set the size of the array. This function 
should be called before the first use of the array and should only be called once. This function should not be called when
initializing from an initializer list.

### Example - [Try It!](https://buildit.so/tryit/?sample=shared&pid=85433647743ea8a6ed037641b8731c0c) 

<pre class="code-box">
\k{#include} "builder/builder_context.h"
\k{#include} "blocks/c_code_generator.h"
\k{#include} "builder/static_var.h"
\k{#include} \<iostream\>

\k{void} foo(\k{const} \k{int} iter) {
    builder::dyn_var\<\k{int}\> sum = 0;

    \c{// static_vars of array types are declared without size}
    builder::static_var\<\k{int}[]\> arr;
    \c{// Array must be resized before first use}
    arr.resize(iter);

    \c{// Loops with static_var iterators are completely evaluated and unrolled}
    \k{for} (builder::static_var\<\k{int}\> x = 0; x < iter; x++) {
        \c{// Conditions with static_var are completely specialized}
        \k{if} (x % 2 == 0) {
            sum += x;
        } \k{else} {
            sum -= x;
        }
        \c{// static\_vars of array types can only be indexed by first stage values}
        arr[x] = x;
    }
}
\k{int} main(\k{int} argc, \k{char}* argv[]) {
    builder::builder_context context;
    \k{auto} ast = context.extract_function_ast(foo, "foo", 16);

    block::c_code_generator::generate_code(ast, std::cout, 0);

    \k{return} 0;
}

</pre>

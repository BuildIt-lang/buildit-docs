## builder::custom\_type Class Reference
<hr>
	
	\k{#include} "builder/dyn_var.h"

	\k{namespace} builder {
	    \k{template} <\k{typename}...Args>
	    \k{struct} custom_type : \k{public} custome_type_base;
	}

<hr>

The custom\_base type template is used to create base classes for custom types to be used with dyn\_var. Types inheriting from custom\_base types can be wrapped inside dyn\_var for second stage execution. Custom types can add dyn\_var members that are accessible from the dyn\_var and produce a member access expression in the generated second stage code. All members must be initialized with the [`as_member()`](custom_type.html#t-as_member) constructor helper. 

Custom types can also add member functions and operators for overloading behavior on the dyn\_var wrapped around the custom type. For more specialization like changing behavior for pointers of custom types, [dyn\_var should be specialized](specialize_dyn_var.html).

Every type inheriting from custom\_type must define a static member `type_name` of type `std::string` or `const char\*` that names the type. See example below. If the generated type is a template type, the template arguments can be passed to custom\_type to be generated as it is. If no template arguments are required, the type should inherit from `custom_type<>`.

### Helper Types

<p id="t-as_member"></p>
	
	builder::as_member(std::string n);

A helper to initialize a dyn\_var as a member of the custom type. This doesn't create a declaration but accesses to the variable produces a member access expression in the generated code. 

### Example - [Try It!](https://buildit.so/tryit/?sample=shared&pid=195495b1ab3dbed100cef17be0741745)

<pre class="code-box">
\k{#include} "builder/builder_context.h"
\k{#include} "blocks/c_code_generator.h"
\k{#include} "builder/dyn_var.h"
\k{#include} &lt;iostream&gt;

// Custom type declaration with no templates
\k{struct} Car: builder::custom_type&lt;&gt; {
    \k{static} \k{const} \k{char}* type_name;
    builder::dyn_var&lt;int&gt; num_doors = builder::as_member("num_doors");
};
\k{const} \k{char}* Car::type_name = "Car";

// Custom type declaration with a template type
\k{template} &lt;\k{typename} T&gt;
\k{struct} my_vector: builder::custom_type&lt;T&gt; {
    \k{static} \k{const} \k{char}* type_name;
    builder::dyn_var&lt;void(T)&gt; push_back = builder::as_member("push_back");
};

\k{template} &lt;\k{typename} T&gt;
\k{const} \k{char}* my_vector&lt;T&gt;::type_name = "std::vector";

\k{static} \k{void} foo (\k{void}) {
    builder::dyn_var&lt;Car&gt; limousine;
    limousine.num_doors = 8;	

    builder::dyn_var&lt;my_vector&lt;Car&gt;&gt; vec;
    vec.push_back(limousine);
}

\k{int} main(\k{int} argc, \k{char}* argv[]) {
    builder::builder_context context;
    \k{auto} ast = context.extract_function_ast(foo, "foo");

    block::c_code_generator::generate_code(ast, std::cout, 0);

    \k{return} 0;
}
</pre>




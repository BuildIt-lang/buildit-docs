## builder::custom\_type Class Reference
<hr>
	
	\k{#include} "builder/dyn_var.h"

	\k{namespace} builder {
	  \k{template} <\k{typename}...Args>
	  \k{struct} custom_type : \k{public} custom_type_base;
	}

<hr>

The custom\_base type template is used to forward template arguments to custom types wrapped in dyn\_var. Custom structs can inherit (`public`) from 
custom\_base types and pass template arguments to be added to the generated declaration. These template arguments don't 
necessarily have to be arguments to the custom struct but this pattern is often used to generate code with template types like `std::vector`. 

If the generate type doesn't need a template arguments, types can inherit from `custom_type<>` however this behavior is
the same as not inheriting from any type. 

### Example - [Try It!](https://buildit.so/tryit/?sample=shared&pid=a34a44470c639e7c8e0662a4b742d2ab)

<pre class="code-box">
\k{#include} "builder/builder_context.h"
\k{#include} "blocks/c_code_generator.h"
\k{#include} "builder/dyn_var.h"
\k{#include} \<iostream\>

\c{// Custom type declaration with a template type}
\k{template} \<\k{typename} T\>
\k{struct} my_vector: builder::custom_type\<T\> {
    \k{static} \k{const} \k{char}* type_name;
    builder::dyn_var\<void(T)\> push_back = builder::as_member("push_back");	
};

\k{template} \<\k{typename} T\>
\k{const} \k{char}* my_vector\<T\>::type_name = "std::vector";

\k{static} \k{void} foo (\k{void}) {
    builder::dyn_var\<my_vector\<\k{int}\>\> vec;
    vec.push_back(42);

    builder::dyn_var\<my_vector\<my_vector\<\k{int}\>\>\> vec2;
    vec2.push_back(vec);
}

\k{int} main(\k{int} argc, \k{char}* argv[]) {
    builder::builder_context context;
    \k{auto} ast = context.extract_function_ast(foo, "foo");

    block::c_code_generator::generate_code(ast, std::cout, 0);

    \k{return} 0;
}
</pre>




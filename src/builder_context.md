## builder::builder\_context Class Reference
<hr>
	
	\k{#include} "builder/builder_context.h"

	\k{namespace} builder {
	  \k{class} builder_context;
	}

<hr>
The builder\_context class is the main context object type for configuring and extracting code with BuildIt. The object's member variables can be set to control behavior of BuildIt and the `extract_function_ast` function is used to invoke the staging. 

### Public Members
- [`bool run_rce = false`](builder_context.html#t-run_rce)
- [`bool feature_unstructured = false`](builder_context.html#t-feature_unstructured)
- [`bool dynamic_use_cxx = false`](builder_context.html#t-dynamic_use_cxx)
- [`bool std::string dynamic_header_includes`](builder_context.html#t-dynamic_header_includes)

### Public Member Functions
- [`extract_function_ast`](builder_context_extract_function_ast.html)


### Member Descriptions

<p id="t-run_rce"></p>

	bool run_rce = false;

Enable running the Redundant Copy Elimination pass after extraction. This pass tries to simplify the generated code by removing redundant copies of variables that arise from passing `dyn_var<T>` around as function arguments. 


<p id="t-feature_unstructured"></p>

	bool feature_unstructured = false;

Forces BuildIt to extract unstructured code. This code does not have any while loops or for loops but only branches and gotos. The jumps from the gotos are also not necessarily structured meaning they can jump across branches. This also enables aggressive memoization inserting jumps instead of copying code. 


<p id="t-dynamic_use_cxx"></p>

	bool dynamic_use_cxx = false;

This flag is only used when the `compile_function_with_context` function is used. Setting this flag instructs BuildIt to compile the generated code as C++ instead of C. 


<p id="t-dynamic_header_includes"></p>


	std::string dynamic_header_includes = "";

This member is only used when the `compile_function_with_context` function is used. The contents of this string are pasted at the top of the generated code before compilation and is typically used for inserting required headers and types. 

### Example - [Try It!](https://buildit.so/tryit/?sample=shared&pid=feaab8cb3987137b5f9f0c54b9a8510c) 

<pre class="code-box">
\k{#include} "builder/builder_context.h"
\k{#include} "blocks/c_code_generator.h"
\k{#include} &lt;iostream&gt;

\k{static} \k{void} foo (\k{void}) {
    builder::dyn_var&lt;\k{int}&gt; x = 0;
    x = x + 1;
    builder::dyn_var&lt;\k{int}&gt; y = x;
    builder::dyn_var&lt;\k{int}&gt; z = y + 1;
    z = z + 1;
}

\k{int} main(\k{int} argc, \k{char}* argv[]) {

    // Create and configure a new builder_context object
    builder::builder_context context;
    context.run_rce = \k{true};         
    // Extract code from the function foo
    \k{auto} ast = context.extract_function_ast(foo, "foo");

    // Generate code for the extracted AST
    block::c_code_generator::generate_code(ast, std::cout, 0);

    \k{return} 0;
}
</pre>


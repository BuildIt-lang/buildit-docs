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
- [`std::string dynamic_header_includes = ""`](builder_context.html#t-dynamic_header_includes)
- [`std::string dynamic_compiler_flags = ""`](builder_context.html#t-dynamic_compiler_flags)
- [`bool use_memoization = true`](builder_context.html#t-use_memoization)
- [`bool enable_d2x = false`](builder_context.html#t-enable_d2x)


### Public Member Functions
- [`extract_function_ast`](builder_context_extract_function_ast.html)


### Member Descriptions

\tag{run_rce}

	\k{bool} run_rce = \k{false};

Enable running the Redundant Copy Elimination pass after extraction. This pass tries to simplify the generated code by removing redundant copies of variables that arise from passing `dyn_var<T>` around as function arguments. 


\tag{feature_unstructured}

	\k{bool} feature_unstructured = \k{false};

Forces BuildIt to extract unstructured code. This code does not have any while loops or for loops but only branches and gotos. The jumps from the gotos are also not necessarily structured meaning they can jump across branches. This also enables aggressive memoization inserting jumps instead of copying code. 


\tag{dynamic_use_cxx}

	\k{bool} dynamic_use_cxx = \k{false};

This flag is only used when the `compile_function_with_context` function is used. Setting this flag instructs BuildIt to compile the generated code as C++ instead of C. 


\tag{dynamic_header_includes}

	std::string dynamic_header_includes = "";

This member is only used when the `compile_function_with_context` function is used. The contents of this string are pasted at the top of the generated code before compilation and is typically used for inserting required headers and types. 

\tag{dynamic_compiler_flags}

	std::string dynamic_compiler_flags = "";

This member is only used when the `compile_function_with_context` function is used. The contents of this string are passed as compiler arguments while compiling the generated code and is typically used to include and link against external dependencies. 


\tag{use_memoization}

	\k{bool} use_memoization = true;

This option is used to control if BuildIt would use memoization while extraction. Generally this option should be set to true since disabling memoization will lead to algorithmic slow down, but can be enabled for debugging typically to find improper uses of static\_var. 

\tag{enable_d2x}

	\k{bool} enable_d2x = false;

Enabling this option instructs BuildIt to gather extra information about the first stage code including source information and values of static\_vars during extraction. This extracted information can be generted as [D2X](https://buildit.so/d2x) debugging metadata by calling [`block::c_code_generator::generate_code_d2x`](c_code_generator_generate_code.html). This option can only be turned on when `ENABLE_D2X` [configuration option](configuration_options.html) is used. 

### Example - [Try It!](https://buildit.so/tryit/?sample=shared&pid=feaab8cb3987137b5f9f0c54b9a8510c) 

<pre class="code-box">
\k{#include} "builder/builder_context.h"
\k{#include} "blocks/c_code_generator.h"
\k{#include} \<iostream\>

\k{static} \k{void} foo (\k{void}) {
    builder::dyn_var\<\k{int}\>; x = 0;
    x = x + 1;
    builder::dyn_var\<\k{int}\>; y = x;
    builder::dyn_var\<\k{int}\>; z = y + 1;
    z = z + 1;
}

\k{int} main(\k{int} argc, \k{char}* argv[]) {

    \c{// Create and configure a new builder_context object}
    builder::builder_context context;
    context.run_rce = \k{true};         
    \c{// Extract code from the function foo}
    \k{auto} ast = context.extract_function_ast(foo, "foo");

    \c{// Generate code for the extracted AST}
    block::c_code_generator::generate_code(ast, std::cout, 0);

    \k{return} 0;
}
</pre>


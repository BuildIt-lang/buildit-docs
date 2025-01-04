## builder::builder\_context::extract\_function\_ast Function Reference
<hr>
	
	\k{#include} "builder/builder_context.h"
	\k{namespace} builder {
	  \k{template} <\k{typename} F, \k{typename}...OtherArgs>
	  block::stmt::Ptr extract_function_ast(F func_input, std::string func_name, OtherArgs&&...args);
	}

<hr>
The extract\_function\_ast function accepts a callable object for staging. The `func_input` argument can be a function pointer, lambda or an `std::function` object to be staged. `func_input` can have a mix of `dyn_var<T>`, `static_var<T>` or regular C++ type parameters. The `dyn_var<T>` arguments become arguments to the generated function, while the rest of the arguments should be provided in order after the `func_name` argument. 
<br><br>
Any BuildIt functions and operators can throw a variety of exceptions during the execution of the function and the implementation should not catch any exceptions under the `builder::` namespace. If caught, these should be thrown again. This also means `func_input` may not always run to completion. So care must be taken when allocating objects on the heap. Allocated objects should be stored in `std::shared_ptr` or `std::unique_ptr` so that they are delete'd even if the execution doesn't reach the end. Any other resources like file handles or network connections should similarly be wrapped inside smart pointers to clean them up in case the function doesn't reach the end. 

### Arguments
- `F func_input` - Callable object to stage
- `std::string func_name` - Name for the generated function AST
- `OtherArgs&&...args` - Arguments for `func_input` other than the `dyn_var<T>` in exact order. These are forwarded to `func_input` at invokation. 


### Returns

Returns a BuildIt `block::stmt::Ptr` which is an abstract type for holding arbitrary statements (including entire functions). This can be passed off to the `block::c_code_generator` directly for code generation. 

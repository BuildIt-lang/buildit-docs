## builder::builder\_context::extract\_function\_ast Function Reference
<hr>
	
	#include "builder/builder_context.h"

	template <typename F, typename...OtherArgs>
	block::stmt::Ptr extract_function_ast(F func_input, std::string func_name, OtherArgs&&...args);
<hr>
The extract\_function\_ast function accepts a callable object for staging. The `func_input` argument can be a function pointer, lambda or an `std::function` object to be staged. `func_input` can have a mix of `dyn_var<T>`, `static_var<T>` or regular C++ type parameters. The `dyn_var<T>` arguments become arguments to the generated function, while the rest of the arguments should be provided in order after the `func_name` argument. 

### Arguments
- `F func_input` - Callable object to stage
- `std::string func_name` - Name for the generated function AST
- `OtherArgs&&...args` - Arguments for `func_input` other than the `dyn_var<T>` in exact order. These are forwarded to `func_input` at invokation. 


### Returns

Returns a BuildIt `block::stmt::Ptr` which is an abstract type for holding arbitrary statements (including entire functions). This can be passed off to the `block::c_code_generator` directly for code generation. 

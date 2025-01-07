## builder::compile\_function, compile\_function\_with\_context and compile\_asts Class Reference
<hr>

	\k{#include} "builder/builder_dynamic.h"
	\k{namespace} builder {

		\k{template} <\k{typename} FT, \k{typename}... ArgsT>
		\k{void}* compile_function(FT f, ArgsT... args)

		\k{template} <\k{typename} FT, \k{typename}... ArgsT>
		\k{void}* compile_function_with_context(builder_context context, FT f, ArgsT... args) 

		\k{void} *compile_asts(builder_context context, std::vector<block::block::Ptr> asts, std::string lookup_name)

	}
<hr>

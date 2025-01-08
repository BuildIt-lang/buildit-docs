## builder::c\_code\_generator::generate\_code Function Reference
<hr>
	
	\k{#include} "blocks/c_code_generator.h"
	\k{namespace} block {
	  \k{static} \k{void} c_code_generator::generate_code(block::Ptr ast, std::ostream &oss, \k{int} indent = 0, \k{bool} decl_only = \k{false});

	  \c{// Only available with ENABLE_D2X=1}
	  \k{static} \k{void} c_code_generator::generate_code_d2x(block::Ptr ast, std::ostream &oss, \k{int} indent = 0, \k{bool} decl_only = \k{false}); 
	}

<hr>

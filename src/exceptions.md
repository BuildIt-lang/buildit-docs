## builder:: namespace Exceptions Reference
<hr>
	\k{#include} "builder/exceptions.h"
	
	\k{namespace} builder {
	    \k{struct} OutOfBoolsException: std::exception;
	    \k{struct} LoopBackException: std::exception;
	    \k{struct} MemoizationException: std::exception;	
	}
<hr>


The `builder::` namespace defines the above exception types which might be thrown by any functions or operators during the execution of the function being extracted with [`extract_function_ast`](builder_context_extract_function_ast.html).
Care should be taken while catching exceptions in the application. If these exceptions are caught, they should be re-thrown. Care should also be taken while writing destructors in application classes. 


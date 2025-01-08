## builder::builder Class Reference
<hr>
	
	\k{#include} "builder/builder.h"

	\k{namespace} builder {
	  \k{class} builder;
	}

<hr>

The builder class is an internal type used to represent expressions of dyn\_var variables. Generally, the user doesn't 
need to use this type since builder is implicitly converted to dyn\_var when assigned to a variable. However care must be
taken when using `auto` (and template inference) in BuildIt code to avoid the type be inferred as builder. Instead a 
concrete dyn\_var must be specified. 

### Public Members

- `block::expr::Ptr block_expr` - Points to the expression that this builder object holds. Applications can access this 
to update the expression if required. 

### Public Member Functions

- [`builder(<basic types>)`](builder.html#t-constructors)

### Member Function Descriptions

\tag{constructors}

	builder(<basic types>)

builder objects can be copy constructed from most primitive and built-in types including - `short, int, long, long long, double,
float, bool, char` (and their unsigned versions), `std::string, char*`, dyn\_vars and static\_vars of any type. This 
usually creates a constant expression or a variable expression.

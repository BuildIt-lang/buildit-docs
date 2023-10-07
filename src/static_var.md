## builder::static\_var Class Reference
<hr>
	
	#include "builder/static_var.h"

	\k{namespace} builder {
	  \k{template} <\k{typename} T>
	  \k{class} static_var;
	}

<hr>

The static\_var type is used to declare variables and expressions that are complete evaluated in the first stage. static\_var is used to track values that change during the first stage execution. If a first stage value does not change during the enterity of the execution of the function, it can be declared with a normal C++ type. 
<br><br>
static\_var variables should be live only for the duration of the function being extracted and should be initialized and updated in the same way if the function is run multiple times. This means storing random values or pointers in static\_var produces unexpected behavior. 

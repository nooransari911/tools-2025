# Question, briefly
Correct function pointer declaration syntax

# Answer
c) double (*fptr)(int, float);

# Explanation
A function pointer declaration requires parentheses around the pointer name to distinguish it from a function returning a pointer. The correct syntax is `return_type (*pointer_name)(parameter_types)`. 

Option a) has incorrect parentheses placement around fptr*. Option b) declares a function that returns a double pointer, not a function pointer. Option d) declares a function named fptr, not a function pointer. Only option c) correctly declares fptr as a pointer to a function that takes an int and float parameter and returns a double.
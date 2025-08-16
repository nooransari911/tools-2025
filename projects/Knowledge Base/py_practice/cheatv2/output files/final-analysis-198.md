# Question 1: Abstract Classes in OOP

**Which statement about abstract classes is correct?**

# Answer
a) Abstract classes can be extended by concrete classes

# Explanation
Abstract classes are designed to be extended by other classes. They can contain both abstract methods (without implementation) and concrete methods (with implementation). Concrete classes that extend abstract classes must implement all abstract methods unless they are also abstract. Abstract classes cannot be instantiated directly, which makes option d incorrect. Options b and c are incorrect because abstract classes are not limited to only abstract methods and can indeed have concrete method implementations.

# Question 2: Interface Method Conflicts

**What happens when a class implements two interfaces with the same method signature?**

# Answer
d) The class must override the method once

# Explanation
When a class implements multiple interfaces that have methods with identical signatures, the class only needs to provide one implementation of that method. This implementation satisfies the contract for both interfaces. There is no ambiguity or compilation error because the method signature is the same, so the same implementation works for both interfaces. The class doesn't use methods from any particular interface - it provides its own implementation.

# Question 3: Function Pointer Declaration in C

**How to correctly declare a function pointer that takes int and float parameters and returns double?**

# Answer
c) double (*fptr)(int, float);

# Explanation
In C, function pointer syntax can be confusing. The correct syntax is: return_type (*pointer_name)(parameter_types). Option c correctly places the parentheses around *fptr, indicating that fptr is a pointer to a function. Option a has incorrect parentheses placement. Option b declares a function that returns a double pointer rather than a function pointer. Option d declares a function named fptr rather than a function pointer.

# Question 4: SQL Query for Above-Average Employees

**Which query retrieves all employees earning more than average salary?**

# Answer
b) SELECT * FROM Employees WHERE salary > (SELECT AVG(salary) FROM Employees);

# Explanation
This query correctly retrieves all employee records where the salary exceeds the average salary. The subquery (SELECT AVG(salary) FROM Employees) calculates the average salary, and the main query compares each employee's salary against this value. Option a is syntactically incorrect and doesn't select employees. Option c only retrieves employee names, not all employee information. Option d counts employees rather than retrieving their records.
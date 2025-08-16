# Question 1: Minimal Cover for Functional Dependencies
Given relation R(A,B,C) with dependencies A → B, B → C, A → C, which is a minimal cover?

# Answer
d) A → B, B → C

# Explanation
A minimal cover must satisfy three conditions:
1. Each functional dependency has a single attribute on the right side
2. No functional dependency can be removed without changing the closure
3. No attribute can be removed from the left side of any dependency

Given dependencies: A → B, B → C, A → C

- Option (a) B → A, C → B: Changes the dependency relationships entirely
- Option (b) A → B, A → C: Removes B → C but A → C can still be derived through transitivity (A → B → C)
- Option (c) A → C, B → A: Changes the dependency structure
- Option (d) A → B, B → C: This is correct because A → C is redundant and can be derived from the transitive property (A → B and B → C implies A → C)

The minimal cover preserves the essential dependencies while removing redundant ones.

# Question 2: Using WHERE Clause with FULL OUTER JOIN
How would you use the WHERE clause with a FULL OUTER JOIN to filter results?

# Answer
d) WHERE can be used to filter rows after the join is applied

# Explanation
The WHERE clause can be used with any type of JOIN, including FULL OUTER JOIN, to filter the results after the join operation is completed. 

Key points:
- WHERE filters rows after the JOIN operation
- It works with all JOIN types including FULL OUTER JOIN
- WHERE is different from ON clause, which specifies join conditions
- WHERE can eliminate rows that don't meet the specified criteria from the final result set

The other options are incorrect: WHERE can be used with FULL OUTER JOIN, it's not limited to INNER JOIN, and it's applied after the join, not before.

# Question 3: Type of Subquery with Inner Dependency
Which type of subquery is used when the inner query depends on the outer query and values from the outer query?

# Answer
c) Correlated subquery

# Explanation
A correlated subquery is a subquery that contains a reference to a column from the outer query, making it dependent on the outer query for its execution. 

Characteristics of correlated subqueries:
- The inner query references columns from the outer query
- It executes once for each row processed by the outer query
- It establishes a dependency between the inner and outer queries
- It's typically less efficient than non-correlated subqueries due to repeated execution

The other options are incorrect:
- Self-contained subquery: Executes independently of the outer query
- Nested subquery: General term for subqueries but doesn't specify dependency
- Uncorrelated subquery: Executes independently and doesn't reference the outer query
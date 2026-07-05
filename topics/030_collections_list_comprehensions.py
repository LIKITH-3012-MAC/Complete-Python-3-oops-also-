###############################################################################
# TOPIC: List Comprehensions and Scoping Mechanics
#
# 1. DEFINITION & INTRODUCTION:
#    - List Comprehensions provide a concise syntax to create lists from existing iterables.
#      Syntax: `[expression for item in iterable if condition]`
#
# 2. ADVANCED OPERATIONS:
#    - Conditional Filtering: `[x for x in data if x > 0]` (filters out non-positive numbers).
#    - Conditional Assignment (Ternary operator inside expression):
#      `[x if x > 0 else 0 for x in data]` (replaces negative values with zero).
#    - Nested Loops: `[x * y for x in list1 for y in list2]` (evaluates as nested loop loops).
#
# 3. SCOPING MECHANICS (CPython Internals):
#    - In Python 2, the loop variable in a list comprehension leaked into the enclosing scope,
#      overwriting external variables of the same name.
#    - Python 3 fixed this by executing list comprehensions in a new, temporary, anonymous
#      function-level scope.
#    - As a result, the loop control variable (e.g. `x`) exists only during evaluation
#      and does not leak or contaminate the local namespace.
#
# 4. PERFORMANCE BENEFITS:
#    - List comprehensions run faster than equivalent `for` loops with `.append()`.
#    - Under the hood, Python compiles a list comprehension to bytecode that uses a specialized
#      CPython opcode `LIST_APPEND`. This opcode pushes elements directly onto the underlying
#      C array, bypassing the overhead of looking up the attribute name `append` and performing
#      method invocation steps on every single loop iteration.
#
# 5. BEST PRACTICES:
#    - Keep list comprehensions simple. If a comprehension spans more than 2 lines or contains
#      nested loops with multiple filters, rewrite it as a standard loop for readability.
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Does the loop variable in a list comprehension leak to the outer scope in Python 3?
#      A: No. List comprehensions in Python 3 are evaluated in their own temporary local namespace,
#         preventing name leaks.
#    - Q: Why is `[x**2 for x in data]` faster than a `for` loop executing `squares.append(x**2)`?
#      A: The comprehension executes appends at the C level using the optimized `LIST_APPEND`
#         opcode, avoiding the runtime lookup and calling overhead of the list `.append` method.
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Flatten a 2D matrix (list of lists) into a 1D list using a single nested
#      list comprehension.
#
###############################################################################

import timeit  # standard library module to compare performance profiles

# 1. Basic List Comprehension and Conditionals
data = [1, -2, 3, -4, 5]

print("--- Basic Comprehensions ---")
# Filter: keep only positive numbers
positives = [x for x in data if x > 0]
print(f"Filtered (positives): {positives}")

# Ternary Assignment: replace negatives with 0
processed_data = [x if x > 0 else 0 for x in data]
print(f"Replaced (negatives with 0): {processed_data}")

# 2. Nested Loop Comprehensions
# Flattening a 2D matrix (frequent interviewer question)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
# Nested loop reads left-to-right in the order of a nested loop:
# for row in matrix:
#     for val in row:
#         yield val
flattened = [val for row in matrix for val in row]
print(f"\nFlattened 2D matrix: {flattened}")

# 3. Scope Isolation Demonstration (Python 3.x)
# We define an external variable named 'loop_var'
loop_var = "untouched"
# Create list comprehension using same loop name
squares = [loop_var**2 for loop_var in range(5)]

print(f"\nList comprehension output: {squares}")
print(f"Outer loop_var value remains: {loop_var}")  # Expected: 'untouched' (No leaking occurred)

# 4. Performance Benchmark: Comprehension vs Loop
# We will compare time taken to populate 1 million squared values.
iterations = 100

loop_time = timeit.timeit(
    stmt="""
squares = []
for x in range(10000):
    squares.append(x**2)
""",
    number=iterations
)

comprehension_time = timeit.timeit(
    stmt="squares = [x**2 for x in range(10000)]",
    number=iterations
)

print("\n--- Performance Benchmarks (Comprehension vs Loop) ---")
print(f"Standard Loop with append():  {loop_time:.5f} seconds")
print(f"List Comprehension:          {comprehension_time:.5f} seconds")
print(f"List Comprehension is {loop_time / comprehension_time:.1f}x faster!")

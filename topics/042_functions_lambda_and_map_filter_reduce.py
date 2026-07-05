###############################################################################
# TOPIC: Lambda (Anonymous) Functions, map, filter, reduce, and Lazy Iterators
#
# 1. DEFINITION & INTRODUCTION:
#    - Lambda Functions: Anonymous, single-expression functions defined using the `lambda` keyword.
#      Syntax: `lambda arguments: expression`
#      They do not contain a `return` statement; they automatically return the evaluated expression.
#    - Built-in Functional Utilities:
#        - `map(func, iterable)`: Applies `func` to every item in the iterable.
#        - `filter(func, iterable)`: Keeps only items where `func(item)` is True.
#        - `reduce(func, iterable)`: Recursively applies `func` pairwise to accumulate a single result.
#
# 2. LAMBDA LIMITATIONS:
#    - Syntactic: Limited to a single expression. You cannot include statements (like `if-elif`,
#      `assert`, loops, or `raise`) inside a lambda.
#    - No Type Annotations: You cannot use type hints on lambda parameters or return types.
#
# 3. LAZY EVALUATION (Python 3 Improvement):
#    - In Python 2, `map()` and `filter()` returned physical list objects.
#    - In Python 3, they return lazy iterator objects (`map` and `filter` class instances).
#    - This means they consume O(1) memory, calculating values on-demand only when iterated,
#      which is ideal for processing massive data streams.
#
# 4. PYTHONIC ALTERNATIVES:
#    - Zen of Python: "There should be one-- and preferably only one --obvious way to do it."
#    - Therefore, list comprehensions and generator expressions are preferred over `map` and
#      `filter` because they are easier to read and avoid lambda syntax overhead.
#        - `map(lambda x: x**2, data)` -> `[x**2 for x in data]`
#        - `filter(lambda x: x > 0, data)` -> `[x for x in data if x > 0]`
#
# 5. INTERVIEW QUESTIONS:
#    - Q: Can you write a multi-line statement (like a loop) inside a lambda function?
#      A: No. Lambda functions are strictly limited to a single expression by design.
#    - Q: What type does `map()` return in Python 3?
#      A: It returns a lazy `map` iterator object, not a list.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Using `functools.reduce` and a lambda function, calculate the factorial
#      of a number.
#
###############################################################################

import functools  # Standard module containing reduce()
import sys  # Standard library to inspect objects

# 1. Lambda Functions Demonstration
# Basic addition lambda
add_lambda = lambda x, y: x + y
print("--- Lambda Functions ---")
print(f"Calling add_lambda(5, 7): {add_lambda(5, 7)}")  # Expected: 12

# Lambda sorting key (Very common usage)
points = [(1, 9), (5, 2), (3, 6)]
# Sort points by the second element of the tuple
points.sort(key=lambda p: p[1])
print(f"Sorted points via lambda key: {points}")  # Expected: [(5, 2), (3, 6), (1, 9)]

# 2. map() and filter() Lazy Iterators
numbers = [1, 2, 3, 4, 5]

print("\n--- Map & Filter Lazy Evaluation ---")
# map returns a map object, not a list
squared_map = map(lambda x: x**2, numbers)
print(f"Type of map output: {type(squared_map)}")  # Expected: <class 'map'>

# filter returns a filter object, not a list
evens_filter = filter(lambda x: x % 2 == 0, numbers)
print(f"Type of filter output: {type(evens_filter)}")  # Expected: <class 'filter'>

# Convert to list to evaluate and print values
print(f"Evaluated map list:    {list(squared_map)}")    # Expected: [1, 4, 9, 16, 25]
print(f"Evaluated filter list: {list(evens_filter)}")   # Expected: [2, 4]

# 3. reduce() accumulation
# Calculate the product of all elements in list: (((1*2)*3)*4)*5
product_res = functools.reduce(lambda x, y: x * y, numbers)
print(f"\nAccumulated product via reduce: {product_res}")  # Expected: 120 (5!)

# Factorial challenge using reduce
def factorial_reduce(n):
    if n == 0 or n == 1:
        return 1
    # reduce(operation, range(1, n+1))
    return functools.reduce(lambda x, y: x * y, range(1, n + 1))

print(f"Factorial of 6 via reduce: {factorial_reduce(6)}")  # Expected: 720

# 4. Comprehensions vs map/filter
# Showing equivalents: comprehensions are generally cleaner
comprehension_square = [x**2 for x in numbers]
map_equivalent = list(map(lambda x: x**2, numbers))
print(f"\nComprehension: {comprehension_square} | Map Equiv: {map_equivalent}")

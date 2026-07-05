# %% [markdown]
# # Topic: Map, Filter, Reduce - Iterator maps, filters, and accumulation reductions
# 
# ## 1. DEFINITIONS & LAZY EVALUATION
# - **map(function, iterable)**:
#   - Applies a function to all items in an input iterable.
#   - Returns a lazy **map iterator object** (evaluated element-by-element on demand), avoiding full collection allocation in memory.
# - **filter(function, iterable)**:
#   - Tests each element of an iterable with a boolean function, keeping only elements returning `True`.
#   - Returns a lazy **filter iterator object**.
# - **reduce(function, iterable[, initializer])**:
#   - Applies a rolling computation to sequential pairs of values in an iterable, reducing the collection to a single cumulative value.
#   - Must be imported from the standard `functools` module (moved there in Python 3 to encourage clear loops).
# 
# ## 2. LIST COMPREHENSIONS VS MAP/FILTER
# - **Readability**: List comprehensions are generally preferred (PEP 202) over `map` and `filter` because they avoid lambda nesting syntax.
# - **Performance**: List comprehensions run at C-speed and are often faster than `map` when using custom lambdas, because the lambda calls introduce standard PVM function frame overhead on every element.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: Why was `reduce` moved to the `functools` module in Python 3?**
#   - *A*: Guido van Rossum preferred explicit `for` loops, as they are significantly easier to read and debug than complex `reduce` statements.
# - **Q: What is the benefit of `map` returning an iterator instead of a list?**
#   - *A*: It runs in $O(1)$ auxiliary space since it yields items one by one on-demand, whereas returning a list allocates memory for the entire collection at once.
# 
# ---

# %%
from functools import reduce

# Input data
numbers = [1, 2, 3, 4, 5]

# 1. Map: Convert integers to their squares
squares_iterator = map(lambda x: x**2, numbers)
print("--- Map Execution ---")
print(f"Iterator type: {type(squares_iterator).__name__}")
# Convert lazy iterator to list to execute and display values
print(f"Squares list:  {list(squares_iterator)}")  # Expected: [1, 4, 9, 16, 25]

# %%
# 2. Filter: Keep only even numbers
evens_iterator = filter(lambda x: x % 2 == 0, numbers)
print("\n--- Filter Execution ---")
print(f"Evens list: {list(evens_iterator)}")  # Expected: [2, 4]

# %%
# 3. Reduce: Multiply all numbers sequentially
# Execution flow: ((1 * 2) * 3) * 4) * 5
product = reduce(lambda x, y: x * y, numbers)
print("\n--- Reduce Execution ---")
print(f"Product total: {product}")  # Expected: 120

# %%
# 4. Map/Filter with list comprehensions equivalents
# Map equivalent: [x**2 for x in numbers]
# Filter equivalent: [x for x in numbers if x % 2 == 0]
print("\n--- List Comprehension Equivalents ---")
comp_squares = [x**2 for x in numbers]
comp_evens = [x for x in numbers if x % 2 == 0]
print(f"Comprehension Squares: {comp_squares}")
print(f"Comprehension Evens:   {comp_evens}")

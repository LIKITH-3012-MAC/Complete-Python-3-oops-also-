# %% [markdown]
# # Topic: Positional Arguments - Index offset mapping, count matching, and parameter overrides
# 
# ## 1. DEFINITION & SYNTAX
# - **Positional Arguments**: Arguments passed to a function call that are mapped to parameters based strictly on their physical order/sequence from left to right:
#   `calculate_power(2, 8)` -> `2` maps to the base, `8` maps to the exponent.
# - **Syntax**:
#   ```python
#   def greet(first_name, last_name):
#       return f"Hello, {first_name} {last_name}"
# 
#   greet("Alice", "Smith") # "Alice" maps to first_name, "Smith" maps to last_name
#   ```
# 
# ## 2. PARAMETERS AND ARGUMENTS COUNT MATCHING
# - **Rule**: Unless default values or argument packing (`*args`) are specified, the number of positional arguments passed in the call must **exactly match** the number of parameters declared in the definition.
# - **Mismatch Errors**:
#   - Passing too few arguments raises: `TypeError: greet() missing 1 required positional argument...`.
#   - Passing too many arguments raises: `TypeError: greet() takes 2 positional arguments but 3 were given`.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is the main disadvantage of relying solely on positional arguments?**
#   - *A*: It makes code fragile if the signature order changes, and caller code becomes less readable when there are many arguments (e.g. `configure(True, False, 10, None, "default")`). Keyword arguments are preferred for readability in large signatures.
# - **Q: How does CPython match positional arguments to local variables?**
#   - *A*: During frame creation, CPython maps the stack elements to local variables in `co_varnames` sequentially by array index.
# 
# ---

# %%
# 1. Standard Positional Argument function
def subtract(a, b):
    """Subtracts b from a. Order is critical!"""
    return a - b

print("--- Calling using Positional Arguments ---")
# 10 maps to 'a', 3 maps to 'b'
print(f"subtract(10, 3): {subtract(10, 3)}")  # Expected: 7

# Swapping arguments swaps execution values
print(f"subtract(3, 10): {subtract(3, 10)}")  # Expected: -7

# %%
# 2. Argument Count Mismatches (TypeError)
print("\n--- Testing Positional Mismatches ---")
try:
    # Missing required argument 'b'
    subtract(5)
except TypeError as e:
    print(f"Caught expected TypeError (missing arg): {e}")

try:
    # Exceeding parameters count (takes 2, 3 given)
    subtract(5, 10, 15)
except TypeError as e:
    print(f"Caught expected TypeError (extra arg): {e}")

# %%
# 3. Dynamic type mapping check
def check_types(first, second):
    return f"First type: {type(first).__name__} | Second type: {type(second).__name__}"

print("\n--- Dynamic Argument Type mappings ---")
print(check_types("string", 42))  # String maps to first, Int maps to second
print(check_types(3.14, True))     # Float maps to first, Bool maps to second

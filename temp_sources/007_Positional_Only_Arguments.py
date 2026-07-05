# %% [markdown]
# # Topic: Positional-Only Arguments - PEP 570, slash syntax (/), and API boundary designs
# 
# ## 1. DEFINITION & SYNTAX
# - **Positional-Only Arguments**: Parameters that can only be filled by positional arguments during call, not by keywords.
# - **Syntax (PEP 570 - Python 3.8+)**:
#   - Defined using a slash `/` symbol in the parameter list.
#   - All parameters declared **before the slash `/`** are positional-only.
#   - Parameters declared **after the slash `/`** can be passed positionally or by keyword (unless marked keyword-only).
#   - Example:
#     ```python
#     def calculate(x, y, /, z):
#         return (x + y) * z
#     ```
#     Here, `x` and `y` are positional-only. `z` can be passed positionally or by keyword.
# 
# ## 2. WHY PYTHON INTRODUCED IT
# 1. **API Name Stability**: Allows library developers to change the names of positional-only parameters in future updates without breaking user code, since users cannot refer to them by keyword.
# 2. **Logical Clarity**: Certain function parameters represent mathematical components (like base/exponent) where mapping string identifiers is redundant.
# 3. **Performance Optimization**: CPython parses positional arguments much faster than keyword arguments because it avoids string hashing and lookup steps.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is the purpose of the `/` symbol in a Python function signature?**
#   - *A*: It acts as a separator. All parameters defined before `/` can only be passed positionally. Passing them as keyword arguments raises a `TypeError`.
# - **Q: Can you pass positional-only parameters by keyword?**
#   - *A*: No, attempting to do so raises a `TypeError: function() got some positional-only arguments passed as keyword arguments`.
# 
# ---

# %%
# 1. Defining a function with positional-only parameters
def format_point(x, y, /, label="Default Point"):
    """x and y are positional-only, label can be positional or keyword."""
    return f"Label: {label} | Coordinates: ({x}, {y})"

print("--- Valid Invocations ---")
# Calling x and y positionally, label by keyword
output1 = format_point(5, 10, label="Origin")
print(output1)

# Calling all positionally
output2 = format_point(12, 24, "Peak")
print(output2)

# %%
# 2. Violating Positional-Only constraint
print("\n--- Testing Violations ---")
try:
    # Attempting to pass positional-only parameter 'x' as a keyword argument!
    format_point(x=5, y=10)
except TypeError as e:
    print(f"Caught expected TypeError: {e}")
    # Expected: got some positional-only arguments passed as keyword arguments: 'x'

# %%
# 3. Mixing Positional-Only, standard, and Keyword-only
# Format: positional_only / standard * keyword_only
def complex_signature(a, b, /, c, *, d):
    return a + b + c + d

print("\n--- Mixed Signature Execution ---")
# a, b: positional only
# c: positional or keyword
# d: keyword only
result = complex_signature(1, 2, c=3, d=4)
print(f"complex_signature(1, 2, c=3, d=4): {result}")  # Expected: 10

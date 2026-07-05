# %% [markdown]
# # Topic: Partial Functions - Argument freezing, functools.partial execution, and metadata inspection
# 
# ## 1. DEFINITION: PARTIAL FUNCTIONS
# - **Partial Function Application**: A technique from functional programming where you pre-fill (freeze) a subset of a function's arguments, creating a new callable object with a simplified signature.
# - **functools.partial(func, \*args, \*\*keywords)**:
#   - Returns a callable **`partial` object**.
#   - When the `partial` object is called, it merges the pre-filled arguments and keywords with any arguments passed in the new call, and executes the original target function.
# 
# ## 2. PARTIAL OBJECT METADATA
# - A `partial` object exposes attributes for runtime inspection:
#   1. **`func`**: Reference to the original undecorated function.
#   2. **`args`**: A tuple of pre-bound positional arguments.
#   3. **`keywords`**: A dictionary of pre-bound keyword arguments.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is a partial function in Python, and how do you create one?**
#   - *A*: A partial function is a callable with pre-configured argument values. It is created using `functools.partial(func, *args, **kwargs)`.
# - **Q: Can you override pre-bound keyword arguments in a partial function?**
#   - *A*: Yes, passing the same keyword argument in the call overrides the value frozen in the `partial` object.
# 
# ---

# %%
from functools import partial

# 1. Defining a base function
def multiply(x, y):
    return x * y

# Create partial callables freezing one parameter
double = partial(multiply, 2)  # Freezes first positional argument 'x' to 2
triple = partial(multiply, 3)  # Freezes first positional argument 'x' to 3

print("--- Calling Partial Functions ---")
print(f"double(5): {double(5)}")  # Equivalent to multiply(2, 5) -> Expected: 10
print(f"triple(5): {triple(5)}")  # Equivalent to multiply(3, 5) -> Expected: 15

# %%
# 2. Freezing keywords and overriding them
def send_request(url, method="GET", timeout=10):
    return f"Sending {method} request to {url} (timeout={timeout}s)"

# Freeze url and timeout
get_google = partial(send_request, "https://google.com", timeout=5)

print("\n--- Frozen Keywords and Overrides ---")
print(get_google())  # Expected: GET request to google.com (timeout=5)

# Override the frozen 'timeout' keyword argument
print(get_google(timeout=15))  # Expected: GET request to google.com (timeout=15)

# %%
# 3. Inspecting partial object attributes
print("\n--- Inspecting partial Object metadata ---")
print(f"Original function: {get_google.func.__name__}")
print(f"Bound positional args: {get_google.args}")       # Expected: ('https://google.com',)
print(f"Bound keyword args:    {get_google.keywords}")   # Expected: {'timeout': 5}

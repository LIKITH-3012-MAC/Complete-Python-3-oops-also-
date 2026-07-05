# %% [markdown]
# # Topic: *args - Positional packing, CPython tuple wrapping, and list unpacking
# 
# ## 1. DEFINITION & SYNTAX
# - **\*args**: The asterisk syntax prefixing a parameter name inside a function definition allows the function to accept an arbitrary number of positional arguments.
# - **Naming**: The name `args` is a standard community convention; any valid variable identifier prefixed by `*` operates exactly the same (e.g. `*items`, `*values`).
# 
# ## 2. CPYTHON INTERNALS: TUPLE PACKING
# - When a function containing a `*args` parameter is invoked with extra positional arguments:
#   1. CPython's argument binding layer captures all positional arguments that exceed the fixed parameters count.
#   2. It creates a new **immutable Tuple object** dynamically on the heap.
#   3. It writes references to the extra arguments into this tuple.
#   4. The local variable `args` is bound to this Tuple object.
#   5. If no extra arguments are passed, `args` is bound to an empty tuple `()`.
# 
# ## 3. CALL-SITE UNPACKING
# - The `*` operator can be used at the **call site** of any function to unpack a collection (list, tuple, set, generator) into distinct positional arguments:
#   `add(*[10, 20])` is equivalent to `add(10, 20)`.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: What is the underlying type of the `args` variable inside the function?**
#   - *A*: It is a standard Python `tuple`. Even if the caller passed arguments as a list or individual integers, Python always packs them into a tuple.
# - **Q: How does `*` work during a function call?**
#   - *A*: It iterates through the collection and pushes each element onto the PVM evaluation stack as a separate positional argument.
# 
# ---

# %%
# 1. Defining a function with *args packing
def calculate_product(*args):
    """Packs all positional arguments into 'args' tuple and multiplies them."""
    print(f"args type: {type(args).__name__} | values: {args}")
    
    product = 1
    for num in args:
        product *= num
    return product

print("--- Calling with varying positional arguments ---")
print(f"Product (no args):    {calculate_product()}")     # Expected args: () | Product: 1
print(f"Product (2 args):     {calculate_product(5, 4)}")  # Expected args: (5, 4) | Product: 20
print(f"Product (4 args):     {calculate_product(2, 3, 4, 5)}")  # Product: 120

# %%
# 2. Call-Site Unpacking using *
def compute_sum(a, b, c):
    return a + b + c

my_numbers = [10, 20, 30]

print("\n--- Call-Site Unpacking ---")
# This unpacks the list elements sequentially into parameters a, b, and c
result = compute_sum(*my_numbers)
print(f"compute_sum(*[10, 20, 30]): {result}")  # Expected: 60

# %%
# 3. Mixing fixed positional parameters with *args
def display_profile(name, email, *hobbies):
    """name and email are mandatory, hobbies captures any extra positional elements."""
    print(f"User: {name} ({email})")
    print(f"Hobbies captured: {hobbies}")

print("\n--- Mixed Signature with *args ---")
display_profile("Alice", "alice@example.com", "Running", "Chess", "Reading")
# 'Running', 'Chess', 'Reading' are packed into hobbies tuple

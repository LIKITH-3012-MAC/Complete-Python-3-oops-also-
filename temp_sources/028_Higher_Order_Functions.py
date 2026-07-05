# %% [markdown]
# # Topic: Higher-Order Functions - Functions as arguments, return callables, and function factory patterns
# 
# ## 1. DEFINITION: HIGHER-ORDER FUNCTIONS
# - **Higher-Order Function (HOF)**: A function that meets at least one of the following conditions:
#   1. Takes one or more functions as arguments.
#   2. Returns a function as its result.
# - **Foundation**: Enabled by Python's model of functions as first-class citizens.
# 
# ## 2. COMMON HOF PATTERNS
# - **Callback Processors**: Functions that accept actions (functions) to apply to collections (e.g., custom sorting keys, event dispatchers).
# - **Function Factories**: Functions that return custom-configured function objects (closures) dynamically based on input configurations.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is a Higher-Order Function, and can you name a built-in Python example?**
#   - *A*: A function that accepts other functions as arguments or returns a function. Examples include `map()`, `filter()`, `sorted()`, and decorators.
# - **Q: How does a function factory utilize closures?**
#   - *A*: It returns a nested function that closes over and remembers configuration parameters passed to the parent factory function.
# 
# ---

# %%
# 1. Function factory pattern (Returning a function)
def get_formatter(mode):
    """Returns a formatting function dynamically based on mode configuration."""
    if mode == "json":
        return lambda data: f'{{"data": "{data}"}}'
    elif mode == "xml":
        return lambda data: f"<data>{data}</data>"
    else:
        return lambda data: str(data)

print("--- Function Factory Execution ---")
json_format = get_formatter("json")
xml_format = get_formatter("xml")

print(json_format("hello"))  # Expected: {"data": "hello"}
print(xml_format("hello"))   # Expected: <data>hello</data>

# %%
# 2. Custom Map Implementation (Accepting a function as argument)
def custom_map(action_func, collection):
    """Applies action_func to every item in the collection."""
    result = []
    for item in collection:
        result.append(action_func(item))
    return result

def add_ten(x):
    return x + 10

print("\n--- Custom Map (Function as Argument) ---")
output = custom_map(add_ten, [1, 2, 3])
print(f"custom_map(add_ten, [1, 2, 3]): {output}")  # Expected: [11, 12, 13]

# %%
# 3. Dynamic execution routing using HOF
def run_op(a, b, operation_func):
    """Executes operation_func passing a and b."""
    return operation_func(a, b)

print("\n--- Dynamic Execution Routing ---")
sum_val = run_op(50, 100, lambda x, y: x + y)
diff_val = run_op(150, 50, lambda x, y: x - y)
print(f"Sum output:  {sum_val}")
print(f"Diff output: {diff_val}")

# %% [markdown]
# # Topic: Closures - Enclosing state retention, cell objects, and __closure__ metadata
# 
# ## 1. DEFINITION & MECHANICS
# - **Closure**: A record binding a function object together with an environment mapping its **free variables** (variables defined in the enclosing outer scope but referenced inside the inner nested function).
# - **State Retention**: A closure allows the inner nested function to retain access to variables in the outer function's scope even after the outer function has completed execution and its stack frame has been popped.
# 
# ## 2. CPYTHON INTERNALS: CELL OBJECTS
# - How does CPython keep enclosing variables alive after the outer function returns?
#   1. When CPython detects a nested function referencing a variable in the enclosing scope, it converts that variable from a standard local stack variable to a **Cell Object**.
#   2. The Cell Object is allocated on the heap, keeping the object it references alive.
#   3. The outer function and the nested inner function both share references to this same Cell Object.
#   4. When the outer function returns, its frame is destroyed, but the Cell Object survives on the heap because the inner function retains a reference to it.
#   5. The inner function exposes these cell bindings in its **`__closure__`** attribute (a tuple of cell objects). The current value inside a cell can be inspected using `cell.cell_contents`.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: What is a closure in Python, and how is it implemented internally?**
#   - *A*: A closure is a nested function that remembers and accesses variables from its enclosing scope. Internally, CPython uses heap-allocated `cell` objects, which are stored in the function's `__closure__` attribute to keep free variables alive after the parent frame exits.
# - **Q: How can you inspect the variables enclosed by a closure?**
#   - *A*: By accessing the function's `__closure__` attribute, iterating through the cells, and reading their `cell_contents`.
# 
# ---

# %%
# 1. Defining a function that returns a closure
def make_multiplier(factor):
    """Enclosing outer function."""
    # 'factor' is a local variable in make_multiplier's scope.
    
    def multiply(number):
        """Nested inner function that references 'factor' (free variable)."""
        return number * factor
        
    return multiply

# Instantiate closures
double = make_multiplier(2)
triple = make_multiplier(3)

print("--- Calling Closures ---")
print(f"double(10): {double(10)}")  # Expected: 20
print(f"triple(10): {triple(10)}")  # Expected: 30

# %%
# 2. Inspecting the closure cell objects using __closure__
print("\n--- Inspecting __closure__ Metadata ---")
print(f"double.__closure__ type: {type(double.__closure__).__name__}")
print(f"Number of cells:          {len(double.__closure__)}")

# Inspect cell details
cell_obj = double.__closure__[0]
print(f"Cell object:            {cell_obj}")
print(f"Cell contents (factor): {cell_obj.cell_contents}")  # Expected: 2

cell_obj_triple = triple.__closure__[0]
print(f"Triple cell contents:   {cell_obj_triple.cell_contents}")  # Expected: 3

# %%
# 3. Dynamic Cell updates (mutable references)
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter_func = make_counter()
print("\n--- Dynamic Cell Updates ---")
print(f"Call 1: {counter_func()}")  # Expected: 1
print(f"Cell contents: {counter_func.__closure__[0].cell_contents}")  # Expected: 1
print(f"Call 2: {counter_func()}")  # Expected: 2
print(f"Cell contents: {counter_func.__closure__[0].cell_contents}")  # Expected: 2

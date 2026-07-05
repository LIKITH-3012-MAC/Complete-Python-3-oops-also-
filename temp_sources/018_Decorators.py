# %% [markdown]
# # Topic: Decorators - Syntactic sugar (@), stacking order, and metadata recovery with functools.wraps
# 
# ## 1. DEFINITION & SYNTAX
# - **Decorator**: A function that takes another function as an argument, extends or modifies its behavior without explicitly modifying its source code, and returns a new function reference.
# - **Syntactic Sugar**: Writing `@my_decorator` above a function definition is syntactically equivalent to reassigning the function to the decorator's output:
#   `func = my_decorator(func)`
# 
# ## 2. DECORATOR STACKING
# - You can apply multiple decorators to a single function.
# - **Evaluation Order**: Decorators are executed from **bottom to top** (innermost to outermost):
#   ```python
#   @decorator_one
#   @decorator_two
#   def my_func():
#       pass
#   ```
#   This compiles exactly as:
#   `my_func = decorator_one(decorator_two(my_func))`
# 
# ## 3. DECORATORS WITH ARGUMENTS
# - To pass parameters to a decorator (e.g. `@repeat(num=3)`), you need a **three-level nested function structure**:
#   1. Outer level: Accepts the arguments for the decorator itself, returning the actual decorator function.
#   2. Middle level: Accepts the target function object.
#   3. Inner level: The wrapper function accepting arguments for the target function call.
# 
# ## 4. METADATA PRESERVATION: functools.wraps
# - **The Problem**: When you decorate a function, its `__name__` and `__doc__` attributes are overwritten by the wrapper function's metadata.
# - **The Solution**: Apply `@functools.wraps(func)` to the wrapper function definition. This copies the original function's name, docstring, annotations, and module info back onto the wrapper.
# 
# ## 5. INTERVIEW QUESTIONS
# - **Q: What is the sequence of execution when stacking decorators?**
#   - *A*: Stacking occurs from bottom to top. The function is first wrapped by the lower decorator, and the resulting wrapper is passed to the decorator above it.
# - **Q: Why should you always use `functools.wraps` inside a custom decorator?**
#   - *A*: To preserve the original decorated function's metadata (docstrings, name, signature), preventing debugging and introspection tools from breaking.
# 
# ---

# %%
import functools

# 1. Simple Decorator with Metadata Recovery
def log_execution(func):
    @functools.wraps(func)  # Copies docstring and name from 'func' to 'wrapper'
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"[LOG] Finished {func.__name__} | Output: {result}")
        return result
    return wrapper

@log_execution
def add(x, y):
    """Adds two integers."""
    return x + y

print("--- Simple Decorator Execution ---")
add(5, 7)
print(f"Preserved Name:      {add.__name__}")  # Expected: 'add' (Thanks to wraps)
print(f"Preserved Docstring: {add.__doc__}")   # Expected: 'Adds two integers.'

# %%
# 2. Decorators with Arguments (Three-level Nesting)
def repeat(num_times):
    """Decorator factory that accepts repeat count configuration."""
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_result = None
            for _ in range(num_times):
                last_result = func(*args, **kwargs)
            return last_result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello, {name}!")

print("\n--- Decorator with Arguments ---")
greet("Alice")  # Expected: prints Hello, Alice! three times

# %%
# 3. Decorator Stacking order
def decorator_a(func):
    def wrapper(*args, **kwargs):
        print("Decorator A wrapper running")
        return func(*args, **kwargs)
    return wrapper

def decorator_b(func):
    def wrapper(*args, **kwargs):
        print("Decorator B wrapper running")
        return func(*args, **kwargs)
    return wrapper

@decorator_a
@decorator_b
def target():
    print("Target function running")

print("\n--- Stacking Order Execution ---")
target()
# Expected output order:
# 1. Decorator A wrapper running (outermost)
# 2. Decorator B wrapper running (innermost)
# 3. Target function running

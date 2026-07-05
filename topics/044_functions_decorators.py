###############################################################################
# TOPIC: Decorators - Function wrapper logic, Metadata wraps, and Classes
#
# 1. DEFINITION & INTRODUCTION:
#    - Decorator: A design pattern in Python that allows wrapping a function or class
#      to extend or modify its behavior without permanently altering the source code.
#    - Syntax uses the `@decorator_name` syntactic sugar placed above the target function.
#
# 2. WRITING CUSTOM DECORATORS:
#    - Basic Decorator (No arguments): A function that takes a function as an argument,
#      defines an inner wrapper, and returns the wrapper.
#    - Decorator with Arguments: Requires a triple-nested function layout:
#        - Outer function: Accepts the decorator arguments and returns the decorator.
#        - Middle function (decorator): Accepts the target function and returns the wrapper.
#        - Inner function (wrapper): Accepts the target function's arguments, executes logic,
#          and returns the result.
#    - Class Decorators: Implement `__call__` magic method on a class. The constructor `__init__`
#      receives the target function, and `__call__` acts as the execution wrapper.
#
# 3. METADATA PRESERVATION (functools.wraps):
#    - When you decorate a function, the variable name is rebound to the inner wrapper function.
#    - Consequently, the function's metadata (docstring, `__name__`, `__annotations__`)
#      are overwritten by the wrapper's metadata.
#    - To fix this, import and decorate the wrapper function with `@functools.wraps(func)`.
#      This automatically copies all metadata from the original function to the wrapper.
#
# 4. DECORATOR CHAINING ORDER:
#    - You can apply multiple decorators to a single function.
#    - Order: Evaluated from bottom to top (innermost to outermost).
#      ```python
#      @dec1
#      @dec2
#      def f(): ...
#      ```
#      This compiles to: `f = dec1(dec2(f))`.
#
# 5. BEST PRACTICES:
#    - Always use `@functools.wraps` when writing decorators to prevent losing docstrings
#      and function names, which breaks logs and introspective tools (like debuggers).
#
# 6. INTERVIEW QUESTIONS:
#    - Q: Why is `functools.wraps` important when writing a decorator?
#      A: It preserves the wrapped function's metadata (name, docstring, annotations), preventing
#         them from being overwritten by the decorator's internal wrapper function.
#    - Q: In what order do chained decorators execute?
#      A: From bottom to top (closest to the function first: `dec1(dec2(func))`).
#
# 7. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a logging/timing decorator that tracks function execution speed
#      and supports passing a custom log prefix as a decorator argument.
#
###############################################################################

import functools  # Standard module containing wraps()
import time  # Module to measure execution timings

# 1. Custom Decorator with Arguments and wraps()
# We will write a decorator that runs the function multiple times for benchmarking.
def repeat_run(num_times):
    def decorator_repeat(func):
        # Use wraps to preserve original function name and docstring
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f" -> [repeat_run] Running {func.__name__} {num_times} times...")
            result = None
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

# 2. Simple Logging Decorator
def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f" -> [log_execution] Entering {func.__name__}")
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start_time
        print(f" -> [log_execution] Exited {func.__name__} | Time: {duration:.6f}s")
        return result
    return wrapper

# 3. Decorator Chaining Demonstration
# Order of application: logging happens first, then repetition inside it
@log_execution
@repeat_run(num_times=3)
def process_data(data_val):
    """Processes a simple calculation."""
    return data_val * 2

print("--- Executing Chained Decorators ---")
# This is equivalent to: process_data = log_execution(repeat_run(3)(process_data))
res = process_data(10)
print(f"Final output: {res}")

print("\n--- Metadata Verification ---")
print(f"Function Name: {process_data.__name__}")  # Expected: 'process_data' (due to wraps!)
print(f"Function Doc:  {process_data.__doc__}")   # Expected: 'Processes a simple calculation.'

# 4. Class-based Decorator
# Class decorators store state inside instance fields.
class CallCounter:
    def __init__(self, func):
        self.func = func
        self.calls_count = 0
        # Preserve metadata manually (or use functools.update_wrapper)
        functools.update_wrapper(self, func)
        
    def __call__(self, *args, **kwargs):
        # Increments execution count on every invocation
        self.calls_count += 1
        print(f" -> [CallCounter] {self.func.__name__} has been called {self.calls_count} times.")
        return self.func(*args, **kwargs)

@CallCounter
def greet(name):
    return f"Hello {name}"

print("\n--- Class Decorator Execution ---")
print(greet("Alice"))
print(greet("Bob"))
print(greet("Charlie"))
print(f"Calls tracked: {greet.calls_count}")  # Expected: 3

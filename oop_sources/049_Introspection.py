###############################################################################
# TOPIC: Introspection - Built-in checkers, the inspect module, and call stack analysis
#
# 1. DEFINITION & INTRODUCTION:
#    - Introspection: The capacity of a program to examine its own metadata, structures,
#      types, and details at runtime (read-only queries).
#
# 2. BUILT-IN INTROSPECTION TOOLS:
#    - `type(obj)`: Identifies the class descriptor of an object.
#    - `id(obj)`: Fetches the unique integer memory address identifier.
#    - `dir(obj)`: Lists all attribute keys and method names defined on the object scope.
#    - `callable(obj)`: Checks if the object can be invoked (defines `__call__`).
#
# 3. THE inspect STANDARD LIBRARY MODULE:
#    - The standard `inspect` module provides advanced introspection tools:
#        - `inspect.signature(func)`: Returns a `Signature` object detailing parameters, types,
#          defaults, and return annotations.
#        - `inspect.getsource(object)`: Reads and returns the raw Python source code string of the
#          specified class, function, or method!
#        - `inspect.currentframe()`: Returns the execution frame object for the active call stack,
#          allowing traceback analysis and local variable queries.
#
# 4. BEST PRACTICES:
#    - Use introspection primarily for debug logging, tracing, testing, validation frameworks
#      (like validator serialization mapping), or writing highly generic decorators.
#
# 5. INTERVIEW QUESTIONS:
#    - Q: What does the `inspect.signature()` method return?
#      A: A `Signature` object containing detailed records of a function's parameters, annotations,
#         and defaults.
#    - Q: How can you dynamically print the source code of a running function?
#      A: By importing the `inspect` module and running `inspect.getsource(function_name)`.
#
# 6. EXERCISES & SOLUTIONS:
#    - Coding challenge: Implement a function inspector that accepts a function object, prints
#      its signature, checks for default arguments, and prints the first 5 lines of its source code.
#
###############################################################################

import inspect  # Standard advanced introspection module

# 1. Target function for inspection
def process_transaction(user_id: int, amount: float, currency: str = "USD") -> bool:
    """Process account transaction for specified user."""
    multiplier = 1.0
    if currency != "USD":
        multiplier = 0.9  # simulated FX conversion
    total = amount * multiplier
    print(f" -> Processing ${total} {currency} for user {user_id}")
    return True

# 2. Basic Introspection built-ins
print("--- Built-in Introspection ---")
print(f"Type of process_transaction: {type(process_transaction)}")  # Expected: <class 'function'>
print(f"Is callable? {callable(process_transaction)}")              # Expected: True
print(f"Has attribute '__doc__'? {hasattr(process_transaction, '__doc__')}")  # Expected: True

# 3. Advanced Introspection using inspect.signature
print("\n--- Inspecting Signatures ---")
sig = inspect.signature(process_transaction)
print(f"Function Signature representation: {sig}")
print(f"Return annotation: {sig.return_annotation}")

# Iterate through parameters to extract annotations and default values
for param_name, param_obj in sig.parameters.items():
    print(f"  Parameter: Name='{param_name}' | TypeHint='{param_obj.annotation}' | Default={param_obj.default}")

# 4. Fetching Source Code Dynamically
print("\n--- Fetching Source Code via inspect.getsource ---")
# inspect reads the raw file source code from memory
source_code = inspect.getsource(process_transaction)
print("Source Code Output:")
print("-" * 50)
print(source_code.strip())
print("-" * 50)

# 5. Inspecting active Execution Frames
def nested_call():
    # Fetch active frame
    frame = inspect.currentframe()
    print(f"\n--- Stack Frame Introspection ---")
    print(f"Active Frame Function Name: {frame.f_code.co_name}")
    # Inspect calling function name (using parent frame)
    parent_frame = frame.f_back
    print(f"Calling Function Name:       {parent_frame.f_code.co_name}")
    print(f"Calling Frame Local Variables: {parent_frame.f_locals}")

def caller_function():
    test_local = "local_marker_value"
    nested_call()

caller_function()

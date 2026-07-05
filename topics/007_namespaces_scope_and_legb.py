###############################################################################
# TOPIC: Namespaces, Scopes, and the LEGB Resolution Rule
#
# 1. DEFINITION & INTRODUCTION:
#    - Namespace: A mapping from names (variable identifiers) to objects. In CPython,
#      namespaces are implemented as standard Python dictionaries (`dict`).
#      There are three main namespaces:
#        1. Built-in namespace: Names like `ValueError`, `len`, `range`.
#        2. Global namespace: Names defined at the module/file level.
#        3. Local namespace: Names defined inside a function execution context.
#    - Scope: A textual region of a Python program where a namespace is directly
#      accessible without prefixing.
#
# 2. THE LEGB RESOLUTION RULE:
#    When you reference a variable name, Python searches namespaces in a strict order:
#    - L (Local): Variables defined inside the current function or lambda.
#    - E (Enclosing / Nonlocal): Variables in any enclosing outer functions, searched
#      from inner to outer (relevant in nested functions and closures).
#    - G (Global): Variables defined at the module top-level or declared as `global`.
#    - B (Built-in): Built-in Python names, loaded at startup.
#    If the name is not found in any of these, Python raises a `NameError`.
#
# 3. GLOBAL AND NONLOCAL KEYWORDS:
#    - `global`: Declares that a variable in the local scope belongs to the global
#      (module-level) scope. It allows modifying global variables from within functions.
#    - `nonlocal`: Declares that a variable belongs to the nearest enclosing outer function
#      scope (excluding global and built-in scopes). It is used inside closures to modify
#      outer-scope variables.
#
# 4. INTERNAL IMPLEMENTATION & CPYTHON INTERNALS:
#    - Namespaces are mapped to execution frame attributes (`f_locals`, `f_globals`).
#    - For functions, CPython optimizes local variable access. Instead of doing a dict
#      lookup on every read, local variables are stored in an array inside the frame,
#      and loaded via offset index (e.g., `LOAD_FAST`).
#    - Global lookup uses `LOAD_GLOBAL`, which performs a dictionary lookup in the
#      module's global dictionary.
#    - Enclosing lookup uses cell and free variables (`LOAD_DEREF`).
#
# 5. TIME & SPACE COMPLEXITY:
#    - Local lookup (`LOAD_FAST`): O(1) array access. Very fast.
#    - Global/Built-in lookup (`LOAD_GLOBAL`): O(1) average dictionary lookup, but slower
#      than local access due to hashing.
#
# 6. BEST PRACTICES:
#    - Avoid modifying global variables inside functions where possible. Pass them as
#      arguments and return values to maintain pure, testable functions.
#    - Use `nonlocal` carefully to preserve clarity in nested decorators or stateful closures.
#    - Do not assign variables with names that clash with built-ins (like `id` or `type`).
#
# 7. COMMON PITFALLS:
#    - `UnboundLocalError`: Triggered when you assign to a variable inside a function,
#      making Python treat it as local to the entire block, but attempt to read it
#      before the assignment line.
#      ```python
#      x = 10
#      def func():
#          print(x) # Raises UnboundLocalError because 'x' is assigned to below.
#          x = 20
#      ```
#
# 8. INTERVIEW QUESTIONS:
#    - Q: What is the difference between global and nonlocal?
#      A: `global` targets variables at the module level. `nonlocal` targets variables
#         in outer nested functions (enclosing scopes) and cannot access global scope variables.
#    - Q: What is the LEGB rule?
#      A: Local, Enclosing, Global, Built-in. It defines the order in which namespaces
#         are searched to resolve variable names.
#
# 9. EXERCISES & SOLUTIONS:
#    - Debugging challenge: Fix an UnboundLocalError in a nested state tracker using
#      nonlocal keyword.
#
###############################################################################

# 1. Global Variable Scope
global_value = "I am global"

def demonstrate_scopes():
    # 2. Local Variable Scope
    local_value = "I am local"
    
    print("--- Scope Access Inside Function ---")
    print(f"Accessing local: {local_value}")
    print(f"Accessing global (LEGB lookup): {global_value}")
    print(f"Accessing built-in (LEGB lookup): {len(local_value)}")  # 'len' is built-in

demonstrate_scopes()

# 3. global Keyword Demonstration
counter = 0

def increment_global():
    # We must explicitly declare 'counter' as global to modify it.
    # Otherwise, 'counter = counter + 1' would raise UnboundLocalError.
    global counter
    counter += 1

increment_global()
print(f"\nGlobal counter value after increment: {counter}")  # Expected: 1

# 4. nonlocal Keyword Demonstration (Nested Closures)
def outer_function():
    # Enclosing scope variable
    outer_var = "initial_value"
    
    def inner_function():
        # 'nonlocal' targets the 'outer_var' in the enclosing outer_function.
        # If we omitted 'nonlocal', 'outer_var = ...' would create a new local variable.
        nonlocal outer_var
        outer_var = "modified_by_inner"
        
    print(f"Outer variable BEFORE inner run: {outer_var}")
    inner_function()
    print(f"Outer variable AFTER inner run: {outer_var}")

print("\n--- Nonlocal Keyword Execution ---")
outer_function()

# 5. UnboundLocalError Demonstration
# Illustrates a common pitfall where local assignment shadows outer scope.
shadow_test = 50

def error_demonstration():
    try:
        # The assignment 'shadow_test = 100' at the bottom of the function causes CPython's
        # compiler to mark 'shadow_test' as local to the entire function scope.
        # Thus, attempting to print it before assignment throws an UnboundLocalError.
        print(shadow_test)
        shadow_test = 100
    except UnboundLocalError as e:
        print(f"Caught UnboundLocalError: {e}")

print("\n--- UnboundLocalError Demonstration ---")
error_demonstration()

# 6. Inspecting Namespaces programmatically
# globals() returns the dictionary representing the current module's global namespace.
# locals() returns a dictionary of the current local namespace.
print("\n--- Namespace Dictionary Inspection ---")
current_globals = globals()
print(f"Does global_value exist in globals()? {'global_value' in current_globals}")

# %% [markdown]
# # Topic: LEGB Rule - Local, Enclosing, Global, Built-in lookup hierarchy and shadowing
# 
# ## 1. THE LEGB RESOLUTION SEQUENCE
# - When a variable or function name is referenced, Python searches namespaces in a strict linear order:
#   1. **L - Local**: Variable names defined inside the current active function body frame.
#   2. **E - Enclosing**: Variable names defined in any nesting parent functions (closures), searched from the nearest enclosing scope outward to the global boundary.
#   3. **G - Global**: Variable names defined at the top-module level of the file (module namespace).
#   4. **B - Built-in**: Names preloaded by Python into the `builtins` module namespace (e.g. `sum`, `len`, `ValueError`, `print`).
# - **Resolution Failure**: If the name is not found in any of these namespaces, Python raises a `NameError: name 'x' is not defined`.
# 
# ## 2. NAMESPACE SHADOWING
# - **Shadowing**: Occurs when a variable defined in an inner scope shares the exact name of a variable in an outer scope.
# - The inner definition overrides the lookup, making the outer definition inaccessible directly within that inner block.
# - **Dangerous Shadowing**: Shadowing names in the Built-in namespace (like naming a local variable `len` or `list`) disables access to those built-in constructors/functions in that scope, causing unexpected failures (e.g. `len("abc")` raises a `TypeError: 'int' object is not callable` if `len = 10` is local).
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: Explain the search sequence when resolving a variable name in a nested function.**
#   - *A*: It follows the LEGB sequence: first search Local (current nested function), then Enclosing (outer parent functions), then Global (module scope), and finally Built-in (builtins module).
# - **Q: How can you recover a shadowed built-in function?**
#   - *A*: By importing `builtins` module explicitly and accessing it via attribute: `import builtins; builtins.len(...)`.
# 
# ---

# %%
# 1. Demonstrating LEGB Lookup Sequence
# Global namespace variable
val = "Global Val"

def outer():
    # Enclosing namespace variable
    val = "Enclosing Val"
    
    def inner():
        # Local namespace variable
        val = "Local Val"
        print(f"Resolving 'val' inside inner(): {val}")  # Prints 'Local Val'
        
    inner()
    print(f"Resolving 'val' inside outer(): {val}")  # Prints 'Enclosing Val'

print("--- LEGB Lookup Order Demonstration ---")
outer()
print(f"Resolving 'val' in module scope:    {val}")  # Prints 'Global Val'

# %%
# 2. Namespace Shadowing of Built-ins
print("\n--- Shadowing Built-in functions ---")
# Let's define a nested block shadowing built-in 'sum'
def calculate_total():
    # Shadow built-in 'sum' name
    sum = 100  # Local int variable shadows built-in sum function
    
    try:
        # This will fail because 'sum' is now local integer 100!
        print(f"Calling sum([1, 2, 3]): {sum([1, 2, 3])}")
    except TypeError as e:
        print(f"Caught expected TypeError (shadowing): {e}")
        # Expected: 'int' object is not callable

calculate_total()

# %%
# 3. Recovering a shadowed built-in
print("\n--- Recovering Shadowed Built-ins ---")
import builtins

def recovery_demo():
    sum = 50
    # Access built-in sum through explicit builtins attribute
    actual_sum = builtins.sum([10, 20, 30])
    return f"Local sum: {sum} | Built-in sum: {actual_sum}"

print(recovery_demo())  # Expected: Local sum: 50 | Built-in sum: 60

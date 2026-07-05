# %% [markdown]
# # Topic: Scope - Local vs Global scope, global/nonlocal keywords, and UnboundLocalError
# 
# ## 1. SCOPE DEFINITIONS
# - **Scope**: The region of a program code block where an identifier name association is directly accessible.
# - **Local Scope**: Variables defined inside a function. Created when the function is called, destroyed when it returns.
# - **Global Scope**: Variables defined at the top level of a module script or inside the global execution space.
# 
# ## 2. MODIFYING OUTER SCOPES
# - **Read Access**: Inner scopes can always read outer scope variables directly.
# - **Write Access (Reassignment)**: Attempting to reassign an outer variable inside an inner scope (e.g. `x = 10`) simply creates a new local variable shadowing the outer one, leaving the outer variable unchanged.
# - **The global Keyword**:
#   - Used inside a function to declare that a variable name belongs to the module-level global scope.
#   - Allows reassigning module-level variables from within function blocks.
# - **The nonlocal Keyword**:
#   - Introduced in PEP 3104 (Python 3.0+).
#   - Used inside nested functions to declare that a variable name belongs to an enclosing outer function scope (excluding global scope).
#   - Enables writing to parent closure variables.
# 
# ## 3. UNBOUNDLOCALERROR
# - **The Error**: Occurs when you attempt to read a variable inside a function *before* assigning a value to it, if that variable is assigned anywhere in the function.
# - **Reason**: Python's compiler statically checks if a variable name is assigned to inside a function block. If it is assigned anywhere in the function, it flags it as a local variable for the *entire* function scope. Trying to print/read it before that assignment executes causes a runtime `UnboundLocalError`.
# 
# ---

# %%
# 1. Modifying globals using global keyword
counter = 0

def increment_global():
    global counter  # Bind local identifier to module global reference
    counter += 1

print("--- Modifying Global Variables ---")
print(f"Initial global counter: {counter}")
increment_global()
increment_global()
print(f"Counter after increment: {counter}")  # Expected: 2

# %%
# 2. Modifying closures using nonlocal keyword
def outer_function():
    outer_value = "initial_outer"
    
    def inner_function():
        nonlocal outer_value  # Bind local identifier to parent closure value
        outer_value = "modified_by_inner"
        
    print(f"Outer value before nested call: {outer_value}")
    inner_function()
    print(f"Outer value after nested call:  {outer_value}")

print("\n--- Modifying Nonlocal Closures ---")
outer_function()
# Expected output proves inner_function successfully mutated outer_value

# %%
# 3. UnboundLocalError Demo
print("\n--- Testing UnboundLocalError ---")
x = 10

def buggy_function():
    try:
        # Python flags 'x' as local because of the assignment line 'x = 20' below!
        # Thus, trying to access it here throws UnboundLocalError.
        print(f"Reading x: {x}")
    except UnboundLocalError as e:
        print(f"Caught expected UnboundLocalError: {e}")
        
    x = 20  # Local assignment makes x local for the entire block scope

buggy_function()

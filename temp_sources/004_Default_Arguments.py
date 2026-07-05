# %% [markdown]
# # Topic: Default Arguments - Definition-time evaluation and the mutable default trap
# 
# ## 1. DEFINITION & SYNTAX
# - **Default Arguments**: Parameter variables assigned default values in the function signature:
#   `def log(message, level="INFO"):`
# - **Rule**: Default parameters must appear after all non-default positional parameters in the signature line.
# 
# ## 2. EVALUATION TIMING & CPYTHON INTERNALS
# - **Definition-Time Evaluation**:
#   - In CPython, default argument expressions are evaluated **exactly once** when the function is defined/compiled (when the `def` block executes).
#   - The evaluated objects are stored in a tuple bound to the function object's `__defaults__` attribute (for positional/keyword arguments) or `__kwdefaults__` (for keyword-only arguments).
#   - When the function is called without providing an argument, Python retrieves the pre-evaluated reference from `__defaults__`.
# 
# ## 3. THE MUTABLE DEFAULT ARGUMENT TRAP (The Classic Python Bug)
# - **The Problem**: If a default argument value is a mutable object (like a list `[]` or dictionary `{}`):
#   - CPython instantiates that list once at definition time and stores it in `__defaults__`.
#   - Every function call that defaults to that argument receives a reference to **the exact same list object in memory**.
#   - Appending items to this parameter modifies the shared list stored in `__defaults__`. Subsequent calls will see accumulated values, leaking state.
# - **The Solution**: Set the default parameter to `None`. Inside the function, check if the variable is `None`, and instantiate a new local list dynamically.
# 
# ## 4. INTERVIEW QUESTIONS
# - **Q: Why should you never use mutable default arguments in Python?**
#   - *A*: Because default values are evaluated once at function definition time, not at invocation time. All calls that omit the argument share a reference to the same mutable object, leading to data corruption and memory leaks.
# - **Q: Where are default arguments stored?**
#   - *A*: Inside the function object's `__defaults__` attribute as a tuple.
# 
# ---

# %%
# 1. The Bug: Mutable Default Argument
def append_to_buggy_list(value, target_list=[]):  # BUG: shared list instantiated at definition
    target_list.append(value)
    return target_list

print("--- Buggy Default Argument Execution ---")
# Call 1 (omits target_list)
list_1 = append_to_buggy_list("item_a")
print(f"List 1: {list_1}")  # Expected: ['item_a']

# Call 2 (omits target_list)
list_2 = append_to_buggy_list("item_b")
# Notice list_2 contains item_a! They share the same list reference in __defaults__.
print(f"List 2: {list_2}")  # Expected: ['item_a', 'item_b']

# %%
# 2. Inspecting __defaults__ in CPython
print("\n--- Inspecting __defaults__ Tuple ---")
print(f"defaults state: {append_to_buggy_list.__defaults__}")
# Expected output contains: (['item_a', 'item_b'],)
# This proves the mutated list is held directly inside the function's metadata!

# %%
# 3. The Fix: None Initialization Pattern
def append_to_fixed_list(value, target_list=None):
    # If no list is passed, instantiate a new local list on every call
    if target_list is None:
        target_list = []
    target_list.append(value)
    return target_list

print("\n--- Fixed Default Argument Execution ---")
list_3 = append_to_fixed_list("item_a")
print(f"List 3: {list_3}")  # Expected: ['item_a']

list_4 = append_to_fixed_list("item_b")
print(f"List 4: {list_4}")  # Expected: ['item_b'] (Correctly isolated!)

print(f"Fixed defaults metadata: {append_to_fixed_list.__defaults__}")
# Expected: (None,) (Since None is immutable, it is safe)

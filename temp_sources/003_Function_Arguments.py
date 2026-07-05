# %% [markdown]
# # Topic: Function Arguments - Parameters vs Arguments and Call-by-Sharing evaluation
# 
# ## 1. PARAMETERS VS ARGUMENTS
# - **Parameters**: The variable names declared in the function definition header signature:
#   `def add(x, y):` -> `x` and `y` are parameters.
# - **Arguments**: The actual data values passed into the function call during invocation:
#   `add(5, 10)` -> `5` and `10` are arguments.
# 
# ## 2. EVALUATION STRATEGY: CALL-BY-SHARING
# - How does Python pass arguments to functions?
#   - It does NOT use *Call-by-value* (where values are duplicated in memory).
#   - It does NOT use *Call-by-reference* (where variables alias the caller's slots).
#   - Python uses **Call-by-Sharing** (or Call-by-Object-Reference).
# - **Mechanics**:
#   1. When you pass an argument to a function, Python binds the parameter name inside the function's local frame to the **exact same object** in the heap referenced by the caller.
#   2. Impact of Mutability:
#       - **Mutable objects** (lists, dicts, sets): If you modify the object in-place inside the function (e.g. `list.append()`), the changes will be visible to the caller, since both caller and callee reference the same object instance.
#       - **Immutable objects** (ints, floats, strings, tuples): Since these objects cannot be mutated, any modification or math operation generates a new object, which binds local names away, leaving the caller's reference unchanged.
#   3. Reassignment:
#       - Reassigning a parameter name inside the function (e.g., `x = [1, 2]`) simply re-binds the local name pointer to a new heap object. It does NOT overwrite the caller's variable or modify the original object.
# 
# ## 3. INTERVIEW QUESTIONS
# - **Q: Explain Python's argument passing mechanism (Call-by-sharing).**
#   - *A*: Python passes object references positionally. The local function parameter binds to the caller's object. Mutating a mutable object affects the caller, but reassigning a variable name only alters the local name binding.
# - **Q: What is the output of passing a list to a function and running `lst = lst + [1]`?**
#   - *A*: This reassigns the local variable `lst` to a newly constructed list object. The original caller list remains unmodified. Contrast with `lst.append(1)` or `lst += [1]`, which mutates the list in-place.
# 
# ---

# %%
# 1. Demonstrating Call-by-Sharing: Mutable Mutability vs Reassignment
def process_list(target_list):
    print(f" -> Local target_list ID initially: {id(target_list)}")
    # Mutate the list in-place
    target_list.append("mutated")
    
    # Reassign the local pointer to a new list
    target_list = [100, 200, 300]
    print(f" -> Local target_list ID after reassignment: {id(target_list)}")
    target_list.append("reassigned_value")

my_list = ["initial"]
print("--- Mutable Argument Execution ---")
print(f"Caller list ID: {id(my_list)}")
print(f"Caller list value before: {my_list}")

# Call function
process_list(my_list)

# Verify outputs
print(f"Caller list value after:  {my_list}")
# Expected: ['initial', 'mutated'] (In-place mutation succeeded, reassignment was local only)

# %%
# 2. Immutable Arguments Behavior
def increment_value(num):
    print(f" -> Local num ID initially: {id(num)}")
    num += 1  # Rebinds local variable num to a new integer object
    print(f" -> Local num ID after addition: {id(num)}")
    return num

my_num = 10
print("\n--- Immutable Argument Execution ---")
print(f"Caller num ID: {id(my_num)}")
print(f"Calling increment_value...")
returned_val = increment_value(my_num)

print(f"Caller variable value: {my_num}")       # Expected: 10 (Unchanged)
print(f"Returned value:         {returned_val}")  # Expected: 11

# %%
# 3. Concatenation mutation quirk: lst += val vs lst = lst + val
# Operator '+=' calls __iadd__ (mutates list in-place).
# Operator '+' calls __add__ (allocates a new list).
def append_operator(lst):
    lst += [99]  # Mutates in-place (calls __iadd__)

def add_operator(lst):
    lst = lst + [99]  # Reassigns (calls __add__ and stores pointer)

list_a = [1, 2]
list_b = [1, 2]

append_operator(list_a)
add_operator(list_b)

print("\n--- Concatenation Operators Quirk ---")
print(f"List A (+=): {list_a}")  # Expected: [1, 2, 99] (Mutated)
print(f"List B (+):  {list_b}")  # Expected: [1, 2]     (Unmodified)
